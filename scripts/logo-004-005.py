"""Generate logo experiment 004-005: rotate text, convert, then fit."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-003.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-005.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-005.png"
FONT_PATH = ROOT / "fonts" / "Days_One" / "DaysOne-Regular.ttf"


def load_previous_successful_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_003", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_rotated_text(experiment, layout):
    font = bpy.data.fonts.load(str(FONT_PATH), check_existing=True)
    material = layout.make_logo_material()

    curve = bpy.data.curves.new("PLANETBUILDER Days One Rotated Source", type="FONT")
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

    text = bpy.data.objects.new("PLANETBUILDER Days One Rotated Text", curve)
    text.data.materials.append(material)
    bpy.context.collection.objects.link(text)
    text.rotation_euler.z = radians(45.0)
    bpy.context.view_layer.objects.active = text
    text.select_set(True)

    # Blender preserves the requested rotation during conversion. Once the text
    # is a mesh, bake that transform into its vertices before envelope fitting.
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    text.name = "PLANETBUILDER Days One Rotated Fitted Mesh"
    text.data.name = "PLANETBUILDER Days One Rotated Fitted Mesh"
    text["font_choice"] = "Days One"
    text["construction"] = "Text rotated 45 degrees counter-clockwise before mesh fitting"
    return text


def main():
    experiment = load_previous_successful_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH

    def create_rotated_and_converted_text(layout):
        return make_rotated_text(experiment, layout)

    experiment.create_and_convert_text = create_rotated_and_converted_text
    experiment.main()


if __name__ == "__main__":
    main()
