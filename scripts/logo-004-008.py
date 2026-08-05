"""Generate logo experiment 004-008: pitch, roll, and yaw before fitting."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-007.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-008.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-008.png"
FONT_PATH = ROOT / "fonts" / "Days_One" / "DaysOne-Regular.ttf"

PITCH_DEGREES = 30.0
ROLL_DEGREES = 20.0
YAW_DEGREES = 15.0


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_007", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_rotated_text(experiment, spacing_experiment, layout):
    font = bpy.data.fonts.load(str(FONT_PATH), check_existing=True)
    material = layout.make_logo_material()

    curve = bpy.data.curves.new("PLANETBUILDER Days One XYZ Source", type="FONT")
    curve.body = spacing_experiment.LOGO_TEXT
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

    text = bpy.data.objects.new("PLANETBUILDER Days One XYZ Text", curve)
    text.data.materials.append(material)
    bpy.context.collection.objects.link(text)
    bpy.context.view_layer.objects.active = text
    text.select_set(True)
    bpy.ops.object.convert(target="MESH")

    text.rotation_euler.x = radians(PITCH_DEGREES)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    text.rotation_euler.z = radians(ROLL_DEGREES)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    text.rotation_euler.y = radians(YAW_DEGREES)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

    text.name = "PLANETBUILDER Days One XYZ Fitted Mesh"
    text.data.name = "PLANETBUILDER Days One XYZ Fitted Mesh"
    text["font_choice"] = "Days One"
    text["pitch_degrees"] = PITCH_DEGREES
    text["roll_degrees"] = ROLL_DEGREES
    text["yaw_degrees"] = YAW_DEGREES
    return text


def main():
    experiment = load_previous_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.PITCH_DEGREES = PITCH_DEGREES
    experiment.YAW_DEGREES = YAW_DEGREES

    previous_loader = experiment.load_spacing_experiment
    spacing_experiment = previous_loader()
    layout = spacing_experiment.load_layout_helpers()

    def create_xyz_rotated_text(_spacing_experiment, _layout):
        return make_rotated_text(experiment, spacing_experiment, layout)

    experiment.make_pitched_and_yawed_text = create_xyz_rotated_text
    experiment.main()


if __name__ == "__main__":
    main()
