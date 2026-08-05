"""Generate logo 005-005 with the camera, key, and fill ten percent closer."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-004.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-005.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-005.png"
CAMERA_DISTANCE = 18.9


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_004", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    lighting = experiment.load_lighting_experiment()
    shape = lighting.load_shape_experiment()
    shape.CAMERA_DISTANCE = CAMERA_DISTANCE

    lighting.load_shape_experiment = lambda: shape
    experiment.load_lighting_experiment = lambda: lighting
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
