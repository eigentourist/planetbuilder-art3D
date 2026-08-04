"""Generate logo experiment 003-001: 3D ribbon guide conversion."""

from math import atan2, cos, pi, radians, sin
from pathlib import Path

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "blendfiles" / "logo-003-001.blend"
RENDER_PATH = ROOT / "renders" / "logo-003-001.png"

RIBBON_WIDTH = 0.105
RIBBON_DEPTH = 0.105
EDGE_BEVEL = 0.002
BEVEL_SEGMENTS = 3
PATH_SAMPLES_PER_SEGMENT = 24
CAP_SEGMENTS = 12

REFERENCE_STROKE_THICKNESS = 0.21
INITIAL_EDGE_GAP = REFERENCE_STROKE_THICKNESS * 2.0
INITIAL_CENTER_SEPARATION = REFERENCE_STROKE_THICKNESS + INITIAL_EDGE_GAP
LOWER_DROP = REFERENCE_STROKE_THICKNESS * 2.0
ARC_WIDTH_FACTOR = 1.2
RIGHT_ANCHOR_Y = 1.74
UPPER_ROTATION_DEGREES = -5.0


BASE_POINTS = (
    ((-5.2, -1.65, 0.0), (-5.55, -2.08, 0.0), (-4.72, -0.98, 0.0)),
    ((-3.35, 0.05, 0.0), (-4.05, -0.55, 0.0), (-2.63, 0.61, 0.0)),
    ((-0.75, 1.26, 0.0), (-1.72, 1.02, 0.0), (0.02, 1.45, 0.0)),
    ((1.05, 1.58, 0.0), (0.35, 1.49, 0.0), (2.00, 1.69, 0.0)),
    ((4.16, 1.74, 0.0), (3.15, 1.74, 0.0), (4.52, 1.74, 0.0)),
    ((5.2, 1.74, 0.0), (4.80, 1.74, 0.0), (5.55, 1.74, 0.0)),
)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def make_cream_material():
    material = bpy.data.materials.new("Orange Cream Soda Cream")
    material.diffuse_color = (1.0, 0.79, 0.48, 1.0)
    material.use_nodes = True
    principled = material.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (1.0, 0.79, 0.48, 1.0)
    principled.inputs["Metallic"].default_value = 0.0
    principled.inputs["Roughness"].default_value = 0.88
    if "Specular IOR Level" in principled.inputs:
        principled.inputs["Specular IOR Level"].default_value = 0.08
    return material


def widen_upper_arc(coordinate):
    x, y, z = coordinate
    return (x, RIGHT_ANCHOR_Y + (y - RIGHT_ANCHOR_Y) / ARC_WIDTH_FACTOR, z)


def make_centerline(name, points, location_y, rotation_degrees):
    curve = bpy.data.curves.new(f"{name} Centerline", type="CURVE")
    curve.dimensions = "3D"
    curve.fill_mode = "FULL"
    curve.resolution_u = PATH_SAMPLES_PER_SEGMENT
    curve.render_resolution_u = PATH_SAMPLES_PER_SEGMENT
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, (co, left, right) in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = "FREE"
        point.handle_right_type = "FREE"
        point.handle_left = left
        point.handle_right = right

    centerline = bpy.data.objects.new(f"{name} Centerline Guide", curve)
    centerline.location.y = location_y
    centerline.rotation_euler.z = radians(rotation_degrees)
    centerline.display_type = "WIRE"
    centerline.hide_render = True
    centerline["purpose"] = "Temporary centerline guide; exclude from GLB exports"
    bpy.context.collection.objects.link(centerline)
    return centerline


def cubic_bezier(p0, p1, p2, p3, t):
    inverse = 1.0 - t
    return (
        inverse**3 * p0
        + 3.0 * inverse**2 * t * p1
        + 3.0 * inverse * t**2 * p2
        + t**3 * p3
    )


def sample_centerline(points, location_y, rotation_degrees):
    samples = []
    for segment_index in range(len(points) - 1):
        p0 = Vector(points[segment_index][0])
        p1 = Vector(points[segment_index][2])
        p2 = Vector(points[segment_index + 1][1])
        p3 = Vector(points[segment_index + 1][0])
        start_step = 0 if segment_index == 0 else 1
        for step in range(start_step, PATH_SAMPLES_PER_SEGMENT + 1):
            samples.append(cubic_bezier(p0, p1, p2, p3, step / PATH_SAMPLES_PER_SEGMENT))

    transform = Matrix.Translation((0.0, location_y, 0.0)) @ Matrix.Rotation(
        radians(rotation_degrees), 4, "Z"
    )
    return [transform @ point for point in samples]


def make_rounded_ribbon_outline(path):
    half_width = RIBBON_WIDTH / 2.0
    tangents = []
    normals = []
    for index, point in enumerate(path):
        if index == 0:
            tangent = path[1] - point
        elif index == len(path) - 1:
            tangent = point - path[index - 1]
        else:
            tangent = path[index + 1] - path[index - 1]
        tangent.z = 0.0
        tangent.normalize()
        tangents.append(tangent)
        normals.append(Vector((-tangent.y, tangent.x, 0.0)))

    left = [point + normal * half_width for point, normal in zip(path, normals)]
    right = [point - normal * half_width for point, normal in zip(path, normals)]
    outline = list(left)

    end_angle = atan2(normals[-1].y, normals[-1].x)
    for step in range(1, CAP_SEGMENTS + 1):
        angle = end_angle - pi * step / CAP_SEGMENTS
        outline.append(path[-1] + Vector((cos(angle), sin(angle), 0.0)) * half_width)

    outline.extend(reversed(right[:-1]))

    start_angle = atan2(normals[0].y, normals[0].x)
    for step in range(1, CAP_SEGMENTS):
        angle = start_angle - pi - pi * step / CAP_SEGMENTS
        outline.append(path[0] + Vector((cos(angle), sin(angle), 0.0)) * half_width)
    return outline


def make_ribbon_mesh(name, path, material):
    outline = make_rounded_ribbon_outline(path)
    mesh = bpy.data.meshes.new(f"{name} Mesh")
    mesh.from_pydata([tuple(vertex) for vertex in outline], [], [list(range(len(outline)))])
    mesh.validate(verbose=False)
    mesh.update()

    ribbon = bpy.data.objects.new(name, mesh)
    ribbon.data.materials.append(material)
    ribbon["geometry_role"] = "Temporary 3D ribbon guide; exclude from GLB exports"
    bpy.context.collection.objects.link(ribbon)

    bpy.context.view_layer.objects.active = ribbon
    ribbon.select_set(True)

    solidify = ribbon.modifiers.new("105 mm Ribbon Depth", type="SOLIDIFY")
    solidify.thickness = RIBBON_DEPTH
    solidify.offset = 0.0
    solidify.use_even_offset = True
    solidify.use_quality_normals = True
    bpy.ops.object.modifier_apply(modifier=solidify.name)

    bevel = ribbon.modifiers.new("2 mm Rounded Edges", type="BEVEL")
    bevel.width = EDGE_BEVEL
    bevel.segments = BEVEL_SEGMENTS
    bevel.limit_method = "ANGLE"
    bevel.angle_limit = radians(20.0)
    bevel.harden_normals = True
    bpy.ops.object.modifier_apply(modifier=bevel.name)

    for polygon in ribbon.data.polygons:
        polygon.use_smooth = False
    ribbon.data.validate(verbose=False)
    ribbon.data.update()

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=radians(66.0), island_margin=0.025)
    bpy.ops.object.mode_set(mode="OBJECT")

    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    ribbon.select_set(False)
    return ribbon


def point_camera_at(camera, target):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def make_camera():
    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0.0, 0.0, 21.0)
    camera_data.type = "PERSP"
    camera_data.lens = 60.0
    camera_data.sensor_width = 36.0
    camera_data.clip_start = 0.1
    camera_data.clip_end = 100.0
    point_camera_at(camera, (0.0, 0.0, 0.0))
    bpy.context.scene.camera = camera
    return camera


def make_skylight(camera):
    light_data = bpy.data.lights.new("Soft White Skylight", type="AREA")
    light_data.color = (1.0, 0.95, 0.88)
    light_data.energy = 1400.0
    light_data.shape = "DISK"
    light_data.size = 8.0
    light = bpy.data.objects.new("Soft White Skylight", light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0.0, 5.5, camera.location.z)
    point_camera_at(light, (0.0, 0.0, 0.0))
    return light


def configure_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 675
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = False
    scene.render.filepath = str(RENDER_PATH)
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    background.inputs["Strength"].default_value = 0.0


def main():
    clear_scene()
    material = make_cream_material()
    half_separation = INITIAL_CENTER_SEPARATION / 2.0
    upper_points = tuple(
        tuple(widen_upper_arc(coordinate) for coordinate in point)
        for point in BASE_POINTS
    )

    upper_y = half_separation
    lower_y = -half_separation - LOWER_DROP
    make_centerline("Upper", upper_points, upper_y, UPPER_ROTATION_DEGREES)
    make_centerline("Lower", BASE_POINTS, lower_y, 0.0)

    upper_path = sample_centerline(upper_points, upper_y, UPPER_ROTATION_DEGREES)
    lower_path = sample_centerline(BASE_POINTS, lower_y, 0.0)
    make_ribbon_mesh("Upper 3D Ribbon Guide", upper_path, material)
    make_ribbon_mesh("Lower 3D Ribbon Guide", lower_path, material)

    camera = make_camera()
    make_skylight(camera)
    configure_render()
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
