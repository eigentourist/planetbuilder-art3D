"""Generate logo 006-011 with forty-degree yaw before arc placement."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-010.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-011.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-011.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_010", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    experiment.YAW_DEGREES = 40.0
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
