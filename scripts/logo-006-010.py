"""Generate logo 006-010 by placing characters on the arc after shared X/Y rotation."""

from importlib.util import module_from_spec, spec_from_file_location
from math import atan2, cos, pi, radians, sin
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
ARC_HELPERS_SCRIPT = ROOT / "scripts" / "logo-006-003.py"
SHAPE_SCRIPT = ROOT / "scripts" / "logo-004-014.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-010.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-010.png"

BASELINE_RADIUS = 10.0
PITCH_DEGREES = 20.0
YAW_DEGREES = 20.0
CAMERA_DISTANCE = 18.9

COLOR_STOPS = (
    (0.0, (0.65, 0.015, 0.008, 1.0), 0.3, "Red"),
    (1.0 / 3.0, (1.0, 0.16, 0.015, 1.0), 0.25, "Orange"),
    (2.0 / 3.0, (1.0, 0.62, 0.04, 1.0), 0.2, "Yellow"),
    (1.0, (1.0, 0.82, 0.58, 1.0), 0.1, "Cream"),
)


def load_module(name, path):
    sys.dont_write_bytecode = True
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arrangement_center(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    minimum = Vector(tuple(min(point[axis] for point in points) for axis in range(3)))
    maximum = Vector(tuple(max(point[axis] for point in points) for axis in range(3)))
    return (minimum + maximum) / 2.0


def rotate_group_then_place_on_arc(characters, shape):
    bpy.context.view_layer.update()
    shared_center = shape.bounds_center(characters)
    pitch = Matrix.Rotation(radians(PITCH_DEGREES), 4, "X")
    yaw = Matrix.Rotation(radians(YAW_DEGREES), 4, "Y")
    shared = Matrix.Translation(shared_center) @ yaw @ pitch @ Matrix.Translation(-shared_center)

    source_centers = []
    transformed_baselines = []
    for obj in characters:
        x_values = [vertex.co.x for vertex in obj.data.vertices]
        local_center_x = (min(x_values) + max(x_values)) / 2.0
        source_center = obj.location.x + local_center_x
        source_centers.append(source_center)
        baseline = obj.matrix_world @ Vector((local_center_x, 0.0, 0.0))
        transformed_baselines.append(shared @ baseline)
        obj.data.transform(shared @ obj.matrix_world)
        obj.matrix_world = Matrix.Identity(4)
        obj["pitch_degrees"] = PITCH_DEGREES
        obj["shared_yaw_degrees"] = YAW_DEGREES

    first_center = source_centers[0]
    total_arc_length = source_centers[-1] - first_center
    for obj, source_center, baseline in zip(characters, source_centers, transformed_baselines):
        arc_length = source_center - first_center
        remaining_arc = total_arc_length - arc_length
        theta = pi / 2.0 + remaining_arc / BASELINE_RADIUS
        tangent_x = sin(theta)
        tangent_y = -cos(theta)

        for vertex in obj.data.vertices:
            vertex.co.x -= baseline.x
            vertex.co.y -= baseline.y
        obj.data.update()
        obj.location = (BASELINE_RADIUS * cos(theta), BASELINE_RADIUS * sin(theta), 0.0)
        obj.rotation_euler.z = atan2(tangent_y, tangent_x)
        obj["baseline_radius"] = BASELINE_RADIUS
        obj["baseline_arc_length"] = arc_length
        obj["baseline_angle_radians"] = theta
        obj["transform_order"] = "Shared X/Y rotation, then circular placement and tangent Z rotation"

    bpy.context.view_layer.update()
    center = arrangement_center(characters)
    for obj in characters:
        obj.location -= center
        obj["arc_arrangement_center_offset"] = tuple(center)
    bpy.context.view_layer.update()
    return total_arc_length / BASELINE_RADIUS


def main():
    arc = load_module("logo_006_003", ARC_HELPERS_SCRIPT)
    shape = load_module("logo_004_014", SHAPE_SCRIPT)
    roll = shape.load_roll_experiment()
    orientation = roll.load_previous_experiment()
    spacing = orientation.load_spacing_experiment()
    layout = spacing.load_layout_helpers()
    base = layout.load_version_003_helpers()

    base.clear_scene()
    shape.configure_text_curve = arc.configure_text_curve
    arc.COLOR_STOPS = COLOR_STOPS
    material_helpers = load_module("logo_006_001", arc.MATERIAL_SCRIPT)
    material = arc.make_text_order_material(material_helpers)
    characters = shape.make_character_meshes(material)
    arc.assign_gradient_attribute(characters)
    occupied_angle = rotate_group_then_place_on_arc(characters, shape)

    camera = base.make_camera()
    camera.location.z = CAMERA_DISTANCE
    base.point_camera_at(camera, (0.0, 0.0, 0.0))
    lighting = load_module("logo_005_001", arc.LIGHTING_SCRIPT)
    arc.make_current_lighting(lighting, base, camera)
    base.configure_render()
    bpy.context.scene.render.filepath = str(RENDER_PATH)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)

    triangles = sum(
        sum(max(0, len(polygon.vertices) - 2) for polygon in obj.data.polygons)
        for obj in characters
    )
    print(
        f"Placed {len(characters)} character meshes over {occupied_angle:.3f} radians "
        f"after shared X/Y rotation; approximately {triangles} triangles"
    )


if __name__ == "__main__":
    main()
