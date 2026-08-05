"""Generate logo version 005 experiment 001 with a soft three-light arrangement."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-014.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-001.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-001.png"

REFERENCE_ENERGY = 1400.0


def load_shape_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_014", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_area_light(base, name, location, intensity, size, color):
    light_data = bpy.data.lights.new(name, type="AREA")
    light_data.color = color
    light_data.energy = REFERENCE_ENERGY * intensity
    light_data.shape = "DISK"
    light_data.size = size
    light = bpy.data.objects.new(name, light_data)
    bpy.context.collection.objects.link(light)
    light.location = location
    light["relative_intensity"] = intensity
    light["placement_description"] = name
    base.point_camera_at(light, (0.0, 0.0, 0.0))
    return light


def make_three_light_rig(base, camera):
    key = make_area_light(
        base,
        "Key Light",
        (-6.5, 6.0, camera.location.z - 3.0),
        1.0,
        8.0,
        (1.0, 0.93, 0.82),
    )
    fill = make_area_light(
        base,
        "Fill Light",
        (0.0, 3.0, camera.location.z - 1.0),
        0.3,
        9.0,
        (0.82, 0.88, 1.0),
    )
    rim = make_area_light(
        base,
        "Rim Light",
        (1.0, 5.5, -5.0),
        0.5,
        4.5,
        (1.0, 0.82, 0.65),
    )
    return key, fill, rim


def main():
    experiment = load_shape_experiment()

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

    roll = experiment.load_roll_experiment()
    orientation = roll.load_previous_experiment()
    spacing = orientation.load_spacing_experiment()
    layout = spacing.load_layout_helpers()
    base = layout.load_version_003_helpers()

    base.make_skylight = lambda camera: make_three_light_rig(base, camera)
    layout.load_version_003_helpers = lambda: base
    spacing.load_layout_helpers = lambda: layout
    orientation.load_spacing_experiment = lambda: spacing
    roll.load_previous_experiment = lambda: orientation
    experiment.load_roll_experiment = lambda: roll
    experiment.configure_text_curve = configure_text_curve
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
