"""Generate logo experiment 004-009: fit first, then roll the composition."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-007.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-009.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-009.png"

PITCH_DEGREES = 30.0
YAW_DEGREES = 15.0
ROLL_DEGREES = 20.0
CAMERA_DISTANCE = 26.0


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_007", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def composition_center(objects):
    points = []
    for obj in objects:
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    minimum = Vector((min(point.x for point in points), min(point.y for point in points), min(point.z for point in points)))
    maximum = Vector((max(point.x for point in points), max(point.y for point in points), max(point.z for point in points)))
    return (minimum + maximum) / 2.0


def roll_as_group(objects):
    pivot = bpy.data.objects.new("Logo Shared Roll Pivot", None)
    bpy.context.collection.objects.link(pivot)
    pivot.location = composition_center(objects)
    pivot["purpose"] = "Shared composition pivot for final positive Z rotation"

    for obj in objects:
        world_transform = obj.matrix_world.copy()
        obj.parent = pivot
        obj.matrix_world = world_transform
    pivot.rotation_euler.z = radians(ROLL_DEGREES)
    return pivot


def main():
    experiment = load_previous_experiment()
    experiment.PITCH_DEGREES = PITCH_DEGREES
    experiment.YAW_DEGREES = YAW_DEGREES
    spacing = experiment.load_spacing_experiment()
    layout = spacing.load_layout_helpers()
    base = layout.load_version_003_helpers()
    base.clear_scene()
    guide_material = base.make_cream_material()
    half_separation = base.INITIAL_CENTER_SEPARATION / 2.0
    upper_points = tuple(
        tuple(base.widen_upper_arc(coordinate) for coordinate in point)
        for point in base.BASE_POINTS
    )

    upper_y = half_separation
    lower_y = -half_separation - base.LOWER_DROP
    upper_centerline = base.make_centerline(
        "Upper", upper_points, upper_y, base.UPPER_ROTATION_DEGREES
    )
    lower_centerline = base.make_centerline("Lower", base.BASE_POINTS, lower_y, 0.0)
    upper_path = base.sample_centerline(upper_points, upper_y, base.UPPER_ROTATION_DEGREES)
    lower_path = base.sample_centerline(base.BASE_POINTS, lower_y, 0.0)
    upper_ribbon = base.make_ribbon_mesh("Upper 3D Ribbon Guide", upper_path, guide_material)
    lower_ribbon = base.make_ribbon_mesh("Lower 3D Ribbon Guide", lower_path, guide_material)

    for guide in (upper_centerline, lower_centerline):
        experiment.set_geometric_origin(guide)
        guide.rotation_euler.y = radians(YAW_DEGREES)
    for ribbon in (upper_ribbon, lower_ribbon):
        ribbon.rotation_euler.y = radians(YAW_DEGREES)
        ribbon["yaw_degrees"] = YAW_DEGREES

    rotated_upper_path = experiment.yaw_path_about_origin(upper_path, upper_ribbon.location)
    rotated_lower_path = experiment.yaw_path_about_origin(lower_path, lower_ribbon.location)
    text = experiment.make_pitched_and_yawed_text(spacing, layout)
    spacing.fit_mesh_to_guides(text, rotated_upper_path, rotated_lower_path)

    roll_as_group((upper_centerline, lower_centerline, upper_ribbon, lower_ribbon, text))
    text["roll_degrees"] = ROLL_DEGREES
    upper_ribbon["roll_degrees"] = ROLL_DEGREES
    lower_ribbon["roll_degrees"] = ROLL_DEGREES

    camera = base.make_camera()
    camera.location.z = CAMERA_DISTANCE
    base.point_camera_at(camera, (0.0, 0.0, 0.0))
    base.make_skylight(camera)
    base.configure_render()
    bpy.context.scene.render.filepath = str(RENDER_PATH)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
