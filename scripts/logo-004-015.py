"""Generate logo experiment 004-015 with Blender 5.2-compatible text alignment."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-014.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-015.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-015.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_014", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()

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

    experiment.configure_text_curve = configure_text_curve
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
