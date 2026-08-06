"""Generate logo 005-012 with ten-degree shared character and guide yaw."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-011.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-012.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-012.png"
YAW_DEGREES = 10.0


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_011", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    fitting_experiment = load_previous_experiment()
    curvature_experiment = fitting_experiment.load_previous_experiment()
    rim_size_experiment = curvature_experiment.load_previous_experiment()
    rim_position_experiment = rim_size_experiment.load_previous_experiment()
    key_experiment = rim_position_experiment.load_previous_experiment()
    guide_removal = key_experiment.load_previous_experiment()
    camera_experiment = guide_removal.load_previous_experiment()
    shape_experiment = camera_experiment.load_previous_experiment()
    lighting = shape_experiment.load_lighting_experiment()
    shape = lighting.load_shape_experiment()

    shape.YAW_DEGREES = YAW_DEGREES

    lighting.load_shape_experiment = lambda: shape
    shape_experiment.load_lighting_experiment = lambda: lighting
    camera_experiment.load_previous_experiment = lambda: shape_experiment
    guide_removal.load_previous_experiment = lambda: camera_experiment
    key_experiment.load_previous_experiment = lambda: guide_removal
    rim_position_experiment.load_previous_experiment = lambda: key_experiment
    rim_size_experiment.load_previous_experiment = lambda: rim_position_experiment
    curvature_experiment.load_previous_experiment = lambda: rim_size_experiment
    fitting_experiment.load_previous_experiment = lambda: curvature_experiment
    fitting_experiment.BLEND_PATH = BLEND_PATH
    fitting_experiment.RENDER_PATH = RENDER_PATH
    fitting_experiment.main()


if __name__ == "__main__":
    main()
