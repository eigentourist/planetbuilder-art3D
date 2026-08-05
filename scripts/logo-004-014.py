"""Generate logo experiment 004-014 with one independently adjustable mesh per character."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-009.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-014.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-014.png"
FONT_PATH = ROOT / "fonts" / "Days_One" / "DaysOne-Regular.ttf"

LOGO_TEXT = "PLANETBUILDER"
PITCH_DEGREES = 20.0
YAW_DEGREES = 15.0
ROLL_DEGREES = 4.0
CAMERA_DISTANCE = 21.0
VERTICAL_MARGIN_FRACTION = 0.15
LEFT_LETTER_WIDTH_SCALE = 1.18
RIGHT_LETTER_WIDTH_SCALE = 1.0


def load_roll_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_009", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def configure_text_curve(curve, body, font):
    curve.body = body
    curve.font = font
    curve.align_x = "LEFT"
    curve.align_y = "BASELINE"
    curve.size = 1.0
    curve.space_character = 1.0
    curve.extrude = 0.0505
    curve.bevel_depth = 0.002
    curve.bevel_resolution = 2
    curve.fill_mode = "BOTH"
    curve.resolution_u = 4


def text_bounds(body, font):
    curve = bpy.data.curves.new("Temporary Days One Spacing Measure", type="FONT")
    configure_text_curve(curve, body, font)
    obj = bpy.data.objects.new("Temporary Days One Spacing Measure", curve)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.update()
    minimum = min(corner[0] for corner in obj.bound_box)
    maximum = max(corner[0] for corner in obj.bound_box)
    bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.curves.remove(curve)
    return minimum, maximum


def make_character_meshes(material):
    font = bpy.data.fonts.load(str(FONT_PATH), check_existing=True)
    meshes = []
    for index, character in enumerate(LOGO_TEXT):
        prefix_maximum = text_bounds(LOGO_TEXT[: index + 1], font)[1]
        character_minimum, character_maximum = text_bounds(character, font)

        curve = bpy.data.curves.new(f"Character {index + 1:02d} {character} Source", type="FONT")
        configure_text_curve(curve, character, font)
        obj = bpy.data.objects.new(f"Character {index + 1:02d} {character}", curve)
        obj.data.materials.append(material)
        obj.location.x = prefix_maximum - character_maximum
        bpy.context.collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.convert(target="MESH")
        obj.select_set(False)
        obj["character"] = character
        obj["character_index"] = index
        obj["font_choice"] = "Days One"
        obj["spacing_source"] = "Right edge of progressively measured full-string prefix"
        obj["original_character_width"] = character_maximum - character_minimum
        meshes.append(obj)

    minimum = min(obj.location.x + min(vertex.co.x for vertex in obj.data.vertices) for obj in meshes)
    maximum = max(obj.location.x + max(vertex.co.x for vertex in obj.data.vertices) for obj in meshes)
    offset = -(minimum + maximum) / 2.0
    for obj in meshes:
        obj.location.x += offset
    return meshes


def bounds_center(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    minimum = Vector(tuple(min(point[axis] for point in points) for axis in range(3)))
    maximum = Vector(tuple(max(point[axis] for point in points) for axis in range(3)))
    return (minimum + maximum) / 2.0


def apply_shared_orientation(objects):
    center = bounds_center(objects)
    pitch = Matrix.Rotation(radians(PITCH_DEGREES), 4, "X")
    yaw = Matrix.Rotation(radians(YAW_DEGREES), 4, "Y")
    shared = Matrix.Translation(center) @ yaw @ pitch @ Matrix.Translation(-center)
    for obj in objects:
        obj.data.transform(shared @ obj.matrix_world)
        obj.matrix_world = Matrix.Identity(4)
        obj["pitch_degrees"] = PITCH_DEGREES
        obj["yaw_degrees"] = YAW_DEGREES


def fit_character_meshes(meshes, upper_path, lower_path, spacing):
    vertices = [vertex for obj in meshes for vertex in obj.data.vertices]
    source_min_x = min(vertex.co.x for vertex in vertices)
    source_max_x = max(vertex.co.x for vertex in vertices)
    source_min_y = min(vertex.co.y for vertex in vertices)
    source_max_y = max(vertex.co.y for vertex in vertices)
    source_width = source_max_x - source_min_x
    source_height = source_max_y - source_min_y

    for vertex in vertices:
        horizontal = (vertex.co.x - source_min_x) / source_width
        vertical = (vertex.co.y - source_min_y) / source_height
        target_x = spacing.TEXT_LEFT + horizontal * (spacing.TEXT_RIGHT - spacing.TEXT_LEFT)
        lower = spacing.interpolate_path_at_x(lower_path, target_x)
        upper = spacing.interpolate_path_at_x(upper_path, target_x)
        gap = upper.y - lower.y
        fitted_lower = lower.y + gap * VERTICAL_MARGIN_FRACTION
        fitted_upper = upper.y - gap * VERTICAL_MARGIN_FRACTION
        vertex.co.x = target_x
        vertex.co.y = fitted_lower + vertical * (fitted_upper - fitted_lower)

    for obj in meshes:
        obj.data.validate(verbose=False)
        obj.data.update()


def widen_characters(meshes):
    centers = []
    for obj in meshes:
        values = [vertex.co.x for vertex in obj.data.vertices]
        centers.append((min(values) + max(values)) / 2.0)
    logo_left = min(centers)
    logo_right = max(centers)

    for obj, center in zip(meshes, centers):
        progress = (center - logo_left) / (logo_right - logo_left)
        scale = LEFT_LETTER_WIDTH_SCALE + progress * (
            RIGHT_LETTER_WIDTH_SCALE - LEFT_LETTER_WIDTH_SCALE
        )
        for vertex in obj.data.vertices:
            vertex.co.x = center + (vertex.co.x - center) * scale
        obj.data.update()
        obj["horizontal_width_scale"] = scale
        obj["horizontal_scale_center"] = center


def main():
    roll_experiment = load_roll_experiment()
    orientation = roll_experiment.load_previous_experiment()
    spacing = orientation.load_spacing_experiment()
    layout = spacing.load_layout_helpers()
    base = layout.load_version_003_helpers()
    base.clear_scene()

    guide_material = base.make_cream_material()
    half_separation = base.INITIAL_CENTER_SEPARATION / 2.0
    upper_points = tuple(tuple(base.widen_upper_arc(value) for value in point) for point in base.BASE_POINTS)
    upper_y = half_separation
    lower_y = -half_separation - base.LOWER_DROP
    upper_centerline = base.make_centerline("Upper", upper_points, upper_y, base.UPPER_ROTATION_DEGREES)
    lower_centerline = base.make_centerline("Lower", base.BASE_POINTS, lower_y, 0.0)
    upper_path = base.sample_centerline(upper_points, upper_y, base.UPPER_ROTATION_DEGREES)
    lower_path = base.sample_centerline(base.BASE_POINTS, lower_y, 0.0)
    upper_ribbon = base.make_ribbon_mesh("Upper 3D Ribbon Guide", upper_path, guide_material)
    lower_ribbon = base.make_ribbon_mesh("Lower 3D Ribbon Guide", lower_path, guide_material)

    for guide in (upper_centerline, lower_centerline):
        orientation.set_geometric_origin(guide)
        guide.rotation_euler.y = radians(YAW_DEGREES)
    for ribbon in (upper_ribbon, lower_ribbon):
        ribbon.rotation_euler.y = radians(YAW_DEGREES)
        ribbon["yaw_degrees"] = YAW_DEGREES
    orientation.YAW_DEGREES = YAW_DEGREES
    rotated_upper_path = orientation.yaw_path_about_origin(upper_path, upper_ribbon.location)
    rotated_lower_path = orientation.yaw_path_about_origin(lower_path, lower_ribbon.location)

    characters = make_character_meshes(layout.make_logo_material())
    apply_shared_orientation(characters)
    fit_character_meshes(characters, rotated_upper_path, rotated_lower_path, spacing)
    widen_characters(characters)

    roll_experiment.ROLL_DEGREES = ROLL_DEGREES
    assembly = (upper_centerline, lower_centerline, upper_ribbon, lower_ribbon, *characters)
    roll_experiment.roll_as_group(assembly)
    for obj in characters:
        obj["roll_degrees"] = ROLL_DEGREES

    camera = base.make_camera()
    camera.location.z = CAMERA_DISTANCE
    base.point_camera_at(camera, (0.0, 0.0, 0.0))
    base.make_skylight(camera)
    base.configure_render()
    bpy.context.scene.render.filepath = str(RENDER_PATH)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)

    triangles = sum(
        sum(max(0, len(polygon.vertices) - 2) for polygon in obj.data.polygons)
        for obj in characters
    )
    print(f"Created {len(characters)} character meshes, approximately {triangles} triangles")


if __name__ == "__main__":
    main()
