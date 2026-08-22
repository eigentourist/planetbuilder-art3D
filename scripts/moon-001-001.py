"""Create the first textured desert-moon design experiment."""

from math import atan, degrees
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "blendfiles" / "moon-001-001.blend"
RENDER_PATH = ROOT / "renders" / "moon-001-001.png"
BASE_COLOR_PATH = ROOT / "textures" / "desert-moon.png"
NORMAL_PATH = ROOT / "textures" / "desert-moon" / "desert-moon_normal.png"
ORM_PATH = ROOT / "textures" / "desert-moon" / "desert-moon_orm.png"
HEIGHT_PATH = ROOT / "textures" / "desert-moon" / "desert-moon_height.png"

MOON_RADIUS = 3.0
SPHERE_SEGMENTS = 96
SPHERE_RINGS = 64
CAMERA_FOCAL_LENGTH = 50.0
CAMERA_DISTANCE = 60.0
RENDER_WIDTH = 1200
RENDER_HEIGHT = 675


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def point_at(obj, target=(0.0, 0.0, 0.0)):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def load_texture(name, path, color_space):
    image = bpy.data.images.load(str(path), check_existing=True)
    image.name = name
    image.colorspace_settings.name = color_space
    return image


def make_material():
    material = bpy.data.materials.new("Desert Moon Material")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (900, 80)
    principled = nodes.new("ShaderNodeBsdfPrincipled")
    principled.location = (620, 80)
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])

    base_color = nodes.new("ShaderNodeTexImage")
    base_color.name = "Base Color (sRGB)"
    base_color.label = "desert-moon.png — sRGB"
    base_color.image = load_texture("Desert Moon Base Color", BASE_COLOR_PATH, "sRGB")
    base_color.extension = "REPEAT"
    base_color.location = (-620, 300)
    links.new(base_color.outputs["Color"], principled.inputs["Base Color"])

    orm = nodes.new("ShaderNodeTexImage")
    orm.name = "ORM (Non-Color)"
    orm.label = "R=AO (deferred), G=Roughness, B=Metallic"
    orm.image = load_texture("Desert Moon ORM", ORM_PATH, "Non-Color")
    orm.extension = "REPEAT"
    orm.location = (-620, 40)
    separate = nodes.new("ShaderNodeSeparateColor")
    separate.mode = "RGB"
    separate.location = (-340, 40)
    links.new(orm.outputs["Color"], separate.inputs["Color"])
    links.new(separate.outputs["Green"], principled.inputs["Roughness"])
    links.new(separate.outputs["Blue"], principled.inputs["Metallic"])

    normal = nodes.new("ShaderNodeTexImage")
    normal.name = "Normal (Non-Color)"
    normal.image = load_texture("Desert Moon Normal", NORMAL_PATH, "Non-Color")
    normal.extension = "REPEAT"
    normal.location = (-620, -240)
    normal_map = nodes.new("ShaderNodeNormalMap")
    normal_map.name = "OpenGL Tangent Normal"
    normal_map.space = "TANGENT"
    normal_map.inputs["Strength"].default_value = 1.0
    normal_map.location = (-330, -240)
    links.new(normal.outputs["Color"], normal_map.inputs["Color"])

    height = nodes.new("ShaderNodeTexImage")
    height.name = "Height (Non-Color)"
    height.image = load_texture("Desert Moon Height", HEIGHT_PATH, "Non-Color")
    height.extension = "REPEAT"
    height.location = (-620, -500)
    bump = nodes.new("ShaderNodeBump")
    bump.name = "Subtle Height Bump"
    bump.inputs["Strength"].default_value = 0.15
    bump.inputs["Distance"].default_value = 0.1
    bump.location = (20, -250)
    links.new(height.outputs["Color"], bump.inputs["Height"])
    links.new(normal_map.outputs["Normal"], bump.inputs["Normal"])
    links.new(bump.outputs["Normal"], principled.inputs["Normal"])

    material["ambient_occlusion_usage"] = "ORM red retained but not applied in Blender"
    material["roughness_source"] = "ORM green"
    material["metallic_source"] = "ORM blue"
    return material


def make_moon(material):
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=SPHERE_SEGMENTS,
        ring_count=SPHERE_RINGS,
        radius=MOON_RADIUS,
        location=(0.0, 0.0, 0.0),
    )
    moon = bpy.context.object
    moon.name = "Desert Moon"
    moon.data.name = "Desert Moon Mesh"
    moon.data.materials.append(material)
    for polygon in moon.data.polygons:
        polygon.use_smooth = True
    moon["texture_projection"] = "Standard equirectangular UV"
    moon["radius_blender_units"] = MOON_RADIUS
    moon["normal_map_convention"] = "OpenGL tangent-space Y+"
    return moon


def make_camera():
    camera_data = bpy.data.cameras.new("Moon Camera")
    camera_data.lens = CAMERA_FOCAL_LENGTH
    camera = bpy.data.objects.new("Moon Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0.0, -CAMERA_DISTANCE, 0.0)
    point_at(camera)
    bpy.context.scene.camera = camera
    camera["framing_goal"] = "Centered; moon approximately one quarter of frame height"
    return camera


def make_area_light(name, location, power, size, description):
    data = bpy.data.lights.new(name, type="AREA")
    data.energy = power
    data.shape = "DISK"
    data.size = size
    light = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(light)
    light.location = location
    point_at(light)
    light["placement_description"] = description
    return light


def make_lighting():
    make_area_light(
        "Key Light",
        (8.0, -12.0, 8.0),
        100.0,
        1.5,
        "Above, camera-right, and slightly in front of the camera-facing moon",
    )
    make_area_light(
        "Fill Light",
        (0.0, -10.0, 8.0),
        60.0,
        1.5,
        "Slightly above the camera axis",
    )
    make_area_light(
        "Rim Light",
        (0.0, 8.0, 8.0),
        40.0,
        1.5,
        "Behind the moon, above, and centered",
    )


def configure_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = RENDER_WIDTH
    scene.render.resolution_y = RENDER_HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.render.filepath = str(RENDER_PATH)
    scene.world.color = (0.0, 0.0, 0.0)
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    background.inputs["Strength"].default_value = 0.0
    scene.view_settings.look = "AgX - Medium High Contrast"


def main():
    clear_scene()
    material = make_material()
    moon = make_moon(material)
    camera = make_camera()
    make_lighting()
    configure_render()

    triangle_count = sum(len(polygon.vertices) - 2 for polygon in moon.data.polygons)
    vertical_fov = 2.0 * atan((camera.data.sensor_width / (RENDER_WIDTH / RENDER_HEIGHT)) / (2.0 * camera.data.lens))
    moon["triangle_count"] = triangle_count
    moon["camera_vertical_fov_degrees"] = degrees(vertical_fov)

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)
    print(
        f"Created moon radius {MOON_RADIUS:.1f} with {triangle_count} triangles; "
        f"rendered {RENDER_WIDTH}x{RENDER_HEIGHT} to {RENDER_PATH}"
    )


if __name__ == "__main__":
    main()
