"""Generate logo 006-003 with characters placed on a radius-one circular baseline."""

from importlib.util import module_from_spec, spec_from_file_location
from math import atan2, cos, pi, sin
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SHAPE_SCRIPT = ROOT / "scripts" / "logo-004-014.py"
MATERIAL_SCRIPT = ROOT / "scripts" / "logo-006-001.py"
LIGHTING_SCRIPT = ROOT / "scripts" / "logo-005-001.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-003.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-003.png"

BASELINE_RADIUS = 1.0
PITCH_DEGREES = 20.0
YAW_DEGREES = 10.0
CAMERA_DISTANCE = 18.9
GRADIENT_ATTRIBUTE = "logo_gradient"

COLOR_STOPS = (
    (0.0, (0.65, 0.015, 0.008, 1.0), 0.4, "Red"),
    (1.0 / 3.0, (1.0, 0.16, 0.015, 1.0), 0.3, "Orange"),
    (2.0 / 3.0, (1.0, 0.62, 0.04, 1.0), 0.2, "Yellow"),
    (1.0, (1.0, 0.82, 0.58, 1.0), 0.1, "Cream"),
)


def load_module(name, path):
    sys.dont_write_bytecode = True
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def configure_text_curve(curve, body, font):
    curve.body = body
    curve.font = font
    curve.align_x = "LEFT"
    curve.align_y = "BOTTOM_BASELINE"
    curve.size = 1.0
    curve.space_character = 1.0
    curve.extrude = 0.0505
    curve.bevel_depth = 0.002
    curve.bevel_resolution = 2
    curve.fill_mode = "BOTH"
    curve.resolution_u = 4


def make_text_order_material(material_helpers):
    material_helpers.COLOR_STOPS = COLOR_STOPS
    material = material_helpers.make_gradient_material(None)
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    color_ramp = nodes["Deep Red Orange Yellow Cream"]
    color_ramp.name = "Red Orange Yellow Cream"
    roughness_ramp = nodes["Roughness 0.45 to 0.15"]
    roughness_ramp.name = "Roughness 0.4 to 0.1"

    attribute = nodes.new("ShaderNodeAttribute")
    attribute.name = "Text-Order Gradient Coordinate"
    attribute.attribute_name = GRADIENT_ATTRIBUTE
    links.new(attribute.outputs["Fac"], color_ramp.inputs["Fac"])
    links.new(attribute.outputs["Fac"], roughness_ramp.inputs["Fac"])

    coordinate_node = nodes.get("Logo-Wide Coordinates")
    gradient_origin = coordinate_node.object if coordinate_node else None
    for name in ("Logo-Wide Coordinates", "Global Left-to-Right Axis", "Normalize Logo X"):
        node = nodes.get(name)
        if node:
            nodes.remove(node)
    if gradient_origin:
        bpy.data.objects.remove(gradient_origin, do_unlink=True)

    material["gradient_basis"] = "Original text-order coordinate stored per vertex before arc placement"
    material["color_sequence"] = "Red, orange, yellow, cream"
    material["roughness_sequence"] = "0.4, 0.3, 0.2, 0.1"
    return material


def assign_gradient_attribute(characters):
    positions = [obj.location.x + vertex.co.x for obj in characters for vertex in obj.data.vertices]
    minimum = min(positions)
    maximum = max(positions)
    width = maximum - minimum
    for obj in characters:
        attribute = obj.data.attributes.new(GRADIENT_ATTRIBUTE, type="FLOAT", domain="POINT")
        for vertex in obj.data.vertices:
            attribute.data[vertex.index].value = (obj.location.x + vertex.co.x - minimum) / width


def place_characters_on_arc(characters):
    source_centers = []
    local_centers = []
    for obj in characters:
        x_values = [vertex.co.x for vertex in obj.data.vertices]
        local_center = (min(x_values) + max(x_values)) / 2.0
        local_centers.append(local_center)
        source_centers.append(obj.location.x + local_center)

    first_center = source_centers[0]
    for obj, source_center, local_center in zip(characters, source_centers, local_centers):
        arc_length = source_center - first_center
        theta = pi - arc_length / BASELINE_RADIUS
        tangent_x = sin(theta)
        tangent_y = -cos(theta)

        for vertex in obj.data.vertices:
            vertex.co.x -= local_center
        obj.data.update()
        obj.location = (
            BASELINE_RADIUS * cos(theta),
            BASELINE_RADIUS * sin(theta),
            0.0,
        )
        obj.rotation_euler.z = atan2(tangent_y, tangent_x)
        obj["baseline_radius"] = BASELINE_RADIUS
        obj["baseline_arc_length"] = arc_length
        obj["baseline_angle_radians"] = theta
        obj["baseline_orientation"] = "Local tangent, clockwise from circle leftmost point"


def make_current_lighting(lighting, base, camera):
    key, fill, rim = lighting.make_three_light_rig(base, camera)
    key.location.x = abs(key.location.x)
    key["placement_description"] = "Above, right, and slightly in front of the camera"
    base.point_camera_at(key, (0.0, 0.0, 0.0))
    rim.location.x = -5.5
    rim.data.size = 8.0
    rim["placement_description"] = "Behind the logo, above, and toward the left side"
    rim["size_description"] = "Large"
    base.point_camera_at(rim, (0.0, 0.0, 0.0))
    return key, fill, rim


def main():
    shape = load_module("logo_004_014", SHAPE_SCRIPT)
    material_helpers = load_module("logo_006_001", MATERIAL_SCRIPT)
    lighting = load_module("logo_005_001", LIGHTING_SCRIPT)
    roll = shape.load_roll_experiment()
    orientation = roll.load_previous_experiment()
    spacing = orientation.load_spacing_experiment()
    layout = spacing.load_layout_helpers()
    base = layout.load_version_003_helpers()

    base.clear_scene()
    shape.configure_text_curve = configure_text_curve
    material = make_text_order_material(material_helpers)
    characters = shape.make_character_meshes(material)
    assign_gradient_attribute(characters)
    place_characters_on_arc(characters)

    shape.PITCH_DEGREES = PITCH_DEGREES
    shape.YAW_DEGREES = YAW_DEGREES
    shape.apply_shared_orientation(characters)

    camera = base.make_camera()
    camera.location.z = CAMERA_DISTANCE
    base.point_camera_at(camera, (0.0, 0.0, 0.0))
    make_current_lighting(lighting, base, camera)
    base.configure_render()
    bpy.context.scene.render.filepath = str(RENDER_PATH)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)

    triangles = sum(
        sum(max(0, len(polygon.vertices) - 2) for polygon in obj.data.polygons)
        for obj in characters
    )
    total_arc = characters[-1]["baseline_arc_length"]
    print(
        f"Placed {len(characters)} character meshes over {total_arc:.3f} radians "
        f"on radius {BASELINE_RADIUS:.3f}; approximately {triangles} triangles"
    )


if __name__ == "__main__":
    main()
