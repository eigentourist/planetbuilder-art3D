"""Generate logo 006-014 with forty-five-degree yaw on the radius-fifteen arc."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-013.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-014.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-014.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_013", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    transform_order_experiment = experiment.load_previous_experiment()
    pre_rotation_arc = transform_order_experiment.load_pre_rotation_arc_experiment()
    pre_rotation_arc.YAW_DEGREES = 45.0

    transform_order_experiment.load_pre_rotation_arc_experiment = lambda: pre_rotation_arc
    experiment.load_previous_experiment = lambda: transform_order_experiment
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
