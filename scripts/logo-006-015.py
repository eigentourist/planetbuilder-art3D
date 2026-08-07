"""Generate logo 006-015 with thirteen-degree pitch and forty-five-degree yaw."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-014.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-015.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-015.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_014", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    yaw_experiment = load_previous_experiment()
    radius_experiment = yaw_experiment.load_previous_experiment()
    transform_order_experiment = radius_experiment.load_previous_experiment()
    pre_rotation_arc = transform_order_experiment.load_pre_rotation_arc_experiment()
    preferred_arc = pre_rotation_arc.load_previous_experiment()
    radius_ten_experiment = preferred_arc.load_previous_experiment()
    centered_experiment = radius_ten_experiment.load_previous_experiment()
    arc_experiment = centered_experiment.load_arc_experiment()

    arc_experiment.PITCH_DEGREES = 13.0

    centered_experiment.load_arc_experiment = lambda: arc_experiment
    radius_ten_experiment.load_previous_experiment = lambda: centered_experiment
    preferred_arc.load_previous_experiment = lambda: radius_ten_experiment
    pre_rotation_arc.load_previous_experiment = lambda: preferred_arc
    transform_order_experiment.load_pre_rotation_arc_experiment = lambda: pre_rotation_arc
    radius_experiment.load_previous_experiment = lambda: transform_order_experiment
    yaw_experiment.load_previous_experiment = lambda: radius_experiment
    yaw_experiment.BLEND_PATH = BLEND_PATH
    yaw_experiment.RENDER_PATH = RENDER_PATH
    yaw_experiment.main()


if __name__ == "__main__":
    main()
