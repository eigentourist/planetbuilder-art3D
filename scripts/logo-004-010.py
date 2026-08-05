"""Generate logo experiment 004-010: reduce final roll and restore framing."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-009.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-010.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-010.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_009", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.ROLL_DEGREES = 10.0
    experiment.CAMERA_DISTANCE = 21.0
    experiment.main()


if __name__ == "__main__":
    main()
