"""Generate logo 005-004 without individual yaw or additional character widening."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-001.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-004.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-004.png"


def load_lighting_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_001", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    lighting = load_lighting_experiment()
    shape = lighting.load_shape_experiment()

    def preserve_fitted_character_widths(objects):
        for obj in objects:
            obj["horizontal_width_scale"] = 1.0
            obj["horizontal_occupancy_method"] = "No additional per-character widening"

    shape.widen_characters = preserve_fitted_character_widths
    lighting.load_shape_experiment = lambda: shape
    lighting.BLEND_PATH = BLEND_PATH
    lighting.RENDER_PATH = RENDER_PATH
    lighting.main()


if __name__ == "__main__":
    main()
