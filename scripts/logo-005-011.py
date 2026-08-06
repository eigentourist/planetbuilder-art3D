"""Generate logo 005-011 without final Z rotation and with a 3% guide allowance."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-010.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-011.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-011.png"
GUIDE_ALLOWANCE_FRACTION = 0.03


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_010", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    curvature_experiment = load_previous_experiment()
    rim_size_experiment = curvature_experiment.load_previous_experiment()
    rim_position_experiment = rim_size_experiment.load_previous_experiment()
    key_experiment = rim_position_experiment.load_previous_experiment()
    guide_removal = key_experiment.load_previous_experiment()
    camera_experiment = guide_removal.load_previous_experiment()
    shape_experiment = camera_experiment.load_previous_experiment()
    lighting = shape_experiment.load_lighting_experiment()
    shape = lighting.load_shape_experiment()
    roll = shape.load_roll_experiment()

    shape.VERTICAL_MARGIN_FRACTION = -GUIDE_ALLOWANCE_FRACTION
    roll.ROLL_DEGREES = 0.0

    shape.load_roll_experiment = lambda: roll
    lighting.load_shape_experiment = lambda: shape
    shape_experiment.load_lighting_experiment = lambda: lighting
    camera_experiment.load_previous_experiment = lambda: shape_experiment
    guide_removal.load_previous_experiment = lambda: camera_experiment
    key_experiment.load_previous_experiment = lambda: guide_removal
    rim_position_experiment.load_previous_experiment = lambda: key_experiment
    rim_size_experiment.load_previous_experiment = lambda: rim_position_experiment
    curvature_experiment.load_previous_experiment = lambda: rim_size_experiment
    curvature_experiment.BLEND_PATH = BLEND_PATH
    curvature_experiment.RENDER_PATH = RENDER_PATH
    curvature_experiment.main()


if __name__ == "__main__":
    main()
