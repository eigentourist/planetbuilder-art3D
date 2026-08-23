"""Generate a baked three-layer nebula background for Godot."""

from math import radians
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-001.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-001.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-001-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-001-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-001-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)

PREVIEW_SIZE = (1200, 675)
PRODUCTION_SIZE = (3840, 2160)
LAYER_SIZE = (2048, 2048)

LAYER_SETTINGS = (
    {
        "name": "Cloud 01 Green",
        "seed": 1.7,
        "scale": 2.15,
        "detail": 5.0,
        "roughness": 0.68,
        "distortion": 0.22,
        "color_dark": (0.012, 0.055, 0.018, 1.0),
        "color_mid": (0.025, 0.34, 0.10, 1.0),
        "color_bright": (0.25, 0.78, 0.34, 1.0),
        "rotation": radians(-7.0),
        "offset": (-2.6, 1.8),
        "scale_xy": (1.18, 1.12),
        "suggested_speed_degrees_per_second": 0.18,
    },
    {
        "name": "Cloud 02 Purple",
        "seed": 8.4,
        "scale": 1.72,
        "detail": 6.0,
        "roughness": 0.72,
        "distortion": 0.34,
        "color_dark": (0.028, 0.008, 0.055, 1.0),
        "color_mid": (0.22, 0.025, 0.34, 1.0),
        "color_bright": (0.68, 0.09, 0.48, 1.0),
        "rotation": radians(9.0),
        "offset": (2.7, -1.8),
        "scale_xy": (1.22, 1.16),
        "suggested_speed_degrees_per_second": -0.13,
    },
    {
        "name": "Cloud 03 Filaments",
        "seed": 15.2,
        "scale": 3.3,
        "detail": 3.2,
        "roughness": 0.58,
        "distortion": 0.62,
        "color_dark": (0.035, 0.006, 0.045, 1.0),
        "color_mid": (0.30, 0.025, 0.26, 1.0),
        "color_bright": (0.78, 0.17, 0.24, 1.0),
        "rotation": radians(-3.0),
        "offset": (0.8, 0.4),
        "scale_xy": (1.10, 1.10),
        "suggested_speed_degrees_per_second": 0.08,
    },
)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def make_camera(aspect=1.0):
    data = bpy.data.cameras.new("Nebula Camera")
    data.type = "ORTHO"
    data.ortho_scale = 10.0
    camera = bpy.data.objects.new("Nebula Camera", data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0.0, 0.0, 10.0)
    camera.rotation_euler = (0.0, 0.0, 0.0)
    bpy.context.scene.camera = camera
    camera["fixed_title_camera"] = True
    camera["aspect_ratio"] = aspect
    return camera


def configure_render(width, height, filepath, transparent):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = transparent
    scene.render.filepath = str(filepath)
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    background.inputs["Strength"].default_value = 0.0
    scene.view_settings.look = "AgX - Medium High Contrast"


def make_plane(name, size=20.0, z=0.0):
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0.0, 0.0, z))
    plane = bpy.context.object
    plane.name = name
    return plane


def make_cloud_material(settings):
    material = bpy.data.materials.new(f"{settings['name']} Procedural Material")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (760, 0)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (520, 0)
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (280, -120)
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (280, 100)
    emission.inputs["Strength"].default_value = 1.0

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-900, 0)
    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-700, 0)
    mapping.inputs["Scale"].default_value = (1.0, 0.72, 1.0)
    noise = nodes.new("ShaderNodeTexNoise")
    noise.noise_dimensions = "4D"
    noise.location = (-430, 40)
    noise.inputs["Scale"].default_value = settings["scale"]
    noise.inputs["Detail"].default_value = settings["detail"]
    noise.inputs["Roughness"].default_value = settings["roughness"]
    noise.inputs["Distortion"].default_value = settings["distortion"]
    noise.inputs["W"].default_value = settings["seed"]

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-120, 50)
    color_ramp = ramp.color_ramp
    first = color_ramp.elements[0]
    first.position = 0.30
    first.color = (*settings["color_dark"][:3], 0.0)
    middle = color_ramp.elements.new(0.52)
    middle.color = (*settings["color_mid"][:3], 0.20)
    high = color_ramp.elements.new(0.68)
    high.color = (*settings["color_bright"][:3], 0.62)
    last = color_ramp.elements[1]
    last.position = 0.84
    last.color = (*settings["color_bright"][:3], 0.80)

    links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], emission.inputs["Color"])
    links.new(ramp.outputs["Alpha"], mix.inputs[0])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])

    material["baked_for_runtime"] = True
    material["procedural_seed"] = settings["seed"]
    return material


def render_cloud_layers():
    clear_scene()
    make_camera(aspect=1.0)
    generated = []
    for index, (settings, path) in enumerate(zip(LAYER_SETTINGS, CLOUD_PATHS), start=1):
        plane = make_plane(f"Generator {settings['name']}", size=10.0)
        plane.data.materials.append(make_cloud_material(settings))
        configure_render(*LAYER_SIZE, path, transparent=True)
        bpy.ops.render.render(write_still=True)
        generated.append(path)
        bpy.data.objects.remove(plane, do_unlink=True)
        print(f"Baked transparent cloud layer {index}: {path}")
    return generated


def make_image_material(name, path):
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (460, 0)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (220, 0)
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (-20, -120)
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (-20, 100)
    image_node = nodes.new("ShaderNodeTexImage")
    image_node.location = (-320, 80)
    image_node.image = bpy.data.images.load(str(path), check_existing=True)
    image_node.image.colorspace_settings.name = "sRGB"
    image_node.extension = "EXTEND"
    links.new(image_node.outputs["Color"], emission.inputs["Color"])
    links.new(image_node.outputs["Alpha"], mix.inputs[0])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    return material


def build_composite_scene():
    clear_scene()
    camera = make_camera(aspect=16.0 / 9.0)
    camera.data.ortho_scale = 10.0

    for index, (settings, path) in enumerate(zip(LAYER_SETTINGS, CLOUD_PATHS), start=1):
        plane = make_plane(settings["name"], size=20.5, z=float(index) * 0.1)
        plane.data.materials.append(make_image_material(f"{settings['name']} Baked Material", path))
        plane.location.x = settings["offset"][0]
        plane.location.y = settings["offset"][1]
        plane.rotation_euler.z = settings["rotation"]
        plane.scale.x = settings["scale_xy"][0]
        plane.scale.y = settings["scale_xy"][1]
        plane["godot_layer_order"] = index
        plane["suggested_rotation_speed_degrees_per_second"] = settings[
            "suggested_speed_degrees_per_second"
        ]
        plane["runtime_technique"] = "Pre-baked RGBA layer; animate transform and modulation only"


def render_background():
    clear_scene()
    make_camera(aspect=16.0 / 9.0)
    configure_render(*PRODUCTION_SIZE, BACKGROUND_PATH, transparent=False)
    bpy.ops.render.render(write_still=True)


def render_composite_and_preview():
    build_composite_scene()
    configure_render(*PRODUCTION_SIZE, COMPOSITE_PATH, transparent=False)
    bpy.ops.render.render(write_still=True)
    configure_render(*PREVIEW_SIZE, PREVIEW_PATH, transparent=False)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


def main():
    render_cloud_layers()
    render_background()
    render_composite_and_preview()
    print(f"Saved nebula scene: {BLEND_PATH}")
    print(f"Saved preview: {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
