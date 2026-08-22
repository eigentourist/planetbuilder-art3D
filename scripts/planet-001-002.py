"""Render the forest planet with the camera twenty percent closer."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "planet-001-001.py"
BLEND_PATH = ROOT / "blendfiles" / "planet-001-002.blend"
RENDER_PATH = ROOT / "renders" / "planet-001-002.png"
CAMERA_DISTANCE = 36.0


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("planet_001_001", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.CAMERA_DISTANCE = CAMERA_DISTANCE
    experiment.main()


if __name__ == "__main__":
    main()
