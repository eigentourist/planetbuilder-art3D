"""Generate logo experiment 004-007: pitched and yawed fitted lettering."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys

import bpy
from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-003.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-007.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-007.png"
FONT_PATH = ROOT / "fonts" / "Days_One" / "DaysOne-Regular.ttf"

PITCH_DEGREES = 35.0
YAW_DEGREES = 15.0


def load_spacing_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_003", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def set_geometric_origin(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    obj.select_set(False)


def yaw_path_about_origin(path, origin):
    rotation = Matrix.Rotation(radians(YAW_DEGREES), 4, "Y")
    center = Vector(origin)
    return [center + rotation @ (point - center) for point in path]


def make_pitched_and_yawed_text(experiment, layout):
    font = bpy.data.fonts.load(str(FONT_PATH), check_existing=True)
    material = layout.make_logo_material()

    curve = bpy.data.curves.new("PLANETBUILDER Days One Pitch-Yaw Source", type="FONT")
    curve.body = experiment.LOGO_TEXT
    curve.font = font
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = 1.0
    curve.space_character = 1.0
    curve.extrude = 0.0505
    curve.bevel_depth = 0.002
    curve.bevel_resolution = 2
    curve.fill_mode = "BOTH"
    curve.resolution_u = 4

    text = bpy.data.objects.new("PLANETBUILDER Days One Pitch-Yaw Text", curve)
    text.data.materials.append(material)
    bpy.context.collection.objects.link(text)
    bpy.context.view_layer.objects.active = text
    text.select_set(True)
    bpy.ops.object.convert(target="MESH")

    text.rotation_euler.x = radians(PITCH_DEGREES)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    text.rotation_euler.y = radians(YAW_DEGREES)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    text.name = "PLANETBUILDER Days One Pitch-Yaw Fitted Mesh"
    text.data.name = "PLANETBUILDER Days One Pitch-Yaw Fitted Mesh"
    text["font_choice"] = "Days One"
    text["pitch_degrees"] = PITCH_DEGREES
    text["yaw_degrees"] = YAW_DEGREES
    return text


def main():
    experiment = load_spacing_experiment()
    layout = experiment.load_layout_helpers()
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
        set_geometric_origin(guide)
        guide.rotation_euler.y = radians(YAW_DEGREES)
    for ribbon in (upper_ribbon, lower_ribbon):
        ribbon.rotation_euler.y = radians(YAW_DEGREES)
        ribbon["yaw_degrees"] = YAW_DEGREES

    rotated_upper_path = yaw_path_about_origin(upper_path, upper_ribbon.location)
    rotated_lower_path = yaw_path_about_origin(lower_path, lower_ribbon.location)

    text = make_pitched_and_yawed_text(experiment, layout)
    experiment.fit_mesh_to_guides(text, rotated_upper_path, rotated_lower_path)

    camera = base.make_camera()
    base.make_skylight(camera)
    base.configure_render()
    bpy.context.scene.render.filepath = str(RENDER_PATH)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
