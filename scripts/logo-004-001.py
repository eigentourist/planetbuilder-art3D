"""Generate logo experiment 004-001: initial PLANETBUILDER font fit."""

from importlib.util import module_from_spec, spec_from_file_location
from math import atan2
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "blendfiles" / "logo-004-001.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-001.png"
FONT_PATH = ROOT / "fonts" / "Goldman" / "Goldman-Bold.ttf"
BASE_SCRIPT_PATH = ROOT / "scripts" / "logo-003-001.py"

LOGO_TEXT = "PLANETBUILDER"
TEXT_LEFT = -4.62
TEXT_RIGHT = 4.62
HEIGHT_FRACTION = 0.70
WIDTH_FRACTION = 0.78


def load_version_003_helpers():
    spec = spec_from_file_location("logo_003_001", BASE_SCRIPT_PATH)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_logo_material():
    material = bpy.data.materials.new("Warm Retro Orange")
    material.diffuse_color = (1.0, 0.18, 0.025, 1.0)
    material.use_nodes = True
    principled = material.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = (1.0, 0.18, 0.025, 1.0)
    principled.inputs["Metallic"].default_value = 0.0
    principled.inputs["Roughness"].default_value = 0.72
    if "Specular IOR Level" in principled.inputs:
        principled.inputs["Specular IOR Level"].default_value = 0.12
    if "Emission Color" in principled.inputs:
        principled.inputs["Emission Color"].default_value = (0.28, 0.018, 0.002, 1.0)
    if "Emission Strength" in principled.inputs:
        principled.inputs["Emission Strength"].default_value = 0.16
    return material


def interpolate_path_at_x(path, x_coordinate):
    for index in range(len(path) - 1):
        left = path[index]
        right = path[index + 1]
        if left.x <= x_coordinate <= right.x:
            width = right.x - left.x
            factor = 0.0 if abs(width) < 1e-8 else (x_coordinate - left.x) / width
            point = left.lerp(right, factor)
            tangent = right - left
            tangent.z = 0.0
            tangent.normalize()
            return point, tangent
    endpoint_index = 0 if x_coordinate < path[0].x else -1
    neighbor_index = 1 if endpoint_index == 0 else -2
    tangent = path[neighbor_index] - path[endpoint_index]
    if endpoint_index == -1:
        tangent.negate()
    tangent.z = 0.0
    tangent.normalize()
    return path[endpoint_index].copy(), tangent


def make_letter(character, index, font, material, position, angle, target_height, slot_width):
    curve = bpy.data.curves.new(f"Glyph {index + 1:02d} {character}", type="FONT")
    curve.body = character
    curve.font = font
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = 1.0
    curve.extrude = 0.0505
    curve.bevel_depth = 0.002
    curve.bevel_resolution = 3
    curve.fill_mode = "BOTH"
    curve.resolution_u = 12

    letter = bpy.data.objects.new(f"Letter {index + 1:02d} {character}", curve)
    letter.data.materials.append(material)
    bpy.context.collection.objects.link(letter)
    bpy.context.view_layer.update()

    natural_width = max(letter.dimensions.x, 0.001)
    natural_height = max(letter.dimensions.y, 0.001)
    scale_y = target_height / natural_height
    proportional_width = natural_width * scale_y
    target_width = min(proportional_width, slot_width * WIDTH_FRACTION)
    scale_x = target_width / natural_width

    letter.scale = (scale_x, scale_y, 1.0)
    letter.location = (position.x, position.y, 0.0)
    letter.rotation_euler.z = angle
    letter["font_choice"] = "Goldman Bold"
    letter["placement_role"] = "Initial fitted logo glyph"
    return letter


def add_fitted_logo(base, upper_path, lower_path):
    font = bpy.data.fonts.load(str(FONT_PATH), check_existing=True)
    material = make_logo_material()
    slot_width = (TEXT_RIGHT - TEXT_LEFT) / (len(LOGO_TEXT) - 1)

    letters = []
    for index, character in enumerate(LOGO_TEXT):
        x_coordinate = TEXT_LEFT + slot_width * index
        upper_point, upper_tangent = interpolate_path_at_x(upper_path, x_coordinate)
        lower_point, lower_tangent = interpolate_path_at_x(lower_path, x_coordinate)
        center = (upper_point + lower_point) / 2.0
        local_gap = max(upper_point.y - lower_point.y, 0.2)
        target_height = local_gap * HEIGHT_FRACTION
        average_tangent = upper_tangent + lower_tangent
        average_tangent.normalize()
        angle = atan2(average_tangent.y, average_tangent.x)
        letters.append(
            make_letter(
                character,
                index,
                font,
                material,
                center,
                angle,
                target_height,
                slot_width,
            )
        )

    for letter in letters:
        letter.select_set(True)
    bpy.context.view_layer.objects.active = letters[0]
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    bpy.ops.object.select_all(action="DESELECT")
    return letters


def main():
    base = load_version_003_helpers()
    base.clear_scene()
    guide_material = base.make_cream_material()
    half_separation = base.INITIAL_CENTER_SEPARATION / 2.0
    upper_points = tuple(
        tuple(base.widen_upper_arc(coordinate) for coordinate in point)
        for point in base.BASE_POINTS
    )

    upper_y = half_separation
    lower_y = -half_separation - base.LOWER_DROP
    base.make_centerline("Upper", upper_points, upper_y, base.UPPER_ROTATION_DEGREES)
    base.make_centerline("Lower", base.BASE_POINTS, lower_y, 0.0)
    upper_path = base.sample_centerline(upper_points, upper_y, base.UPPER_ROTATION_DEGREES)
    lower_path = base.sample_centerline(base.BASE_POINTS, lower_y, 0.0)
    base.make_ribbon_mesh("Upper 3D Ribbon Guide", upper_path, guide_material)
    base.make_ribbon_mesh("Lower 3D Ribbon Guide", lower_path, guide_material)

    add_fitted_logo(base, upper_path, lower_path)
    camera = base.make_camera()
    base.make_skylight(camera)
    base.configure_render()
    bpy.context.scene.render.filepath = str(RENDER_PATH)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
