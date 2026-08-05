"""Generate logo experiment 004-011: gentler pitch and roll with fuller corridor occupancy."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-009.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-011.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-011.png"

PITCH_DEGREES = 20.0
YAW_DEGREES = 15.0
ROLL_DEGREES = 5.0
CAMERA_DISTANCE = 21.0
VERTICAL_MARGIN_FRACTION = 0.08


def load_roll_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_009", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    roll_experiment = load_roll_experiment()
    orientation_experiment = roll_experiment.load_previous_experiment()
    spacing_experiment = orientation_experiment.load_spacing_experiment()

    spacing_experiment.VERTICAL_MARGIN_FRACTION = VERTICAL_MARGIN_FRACTION
    orientation_experiment.load_spacing_experiment = lambda: spacing_experiment
    roll_experiment.load_previous_experiment = lambda: orientation_experiment

    roll_experiment.BLEND_PATH = BLEND_PATH
    roll_experiment.RENDER_PATH = RENDER_PATH
    roll_experiment.PITCH_DEGREES = PITCH_DEGREES
    roll_experiment.YAW_DEGREES = YAW_DEGREES
    roll_experiment.ROLL_DEGREES = ROLL_DEGREES
    roll_experiment.CAMERA_DISTANCE = CAMERA_DISTANCE
    roll_experiment.main()


if __name__ == "__main__":
    main()
