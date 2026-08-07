"""Generate logo 006-016 with roughness increasing from red to cream."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-015.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-016.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-016.png"

COLOR_STOPS = (
    (0.0, (0.65, 0.015, 0.008, 1.0), 0.1, "Red"),
    (1.0 / 3.0, (1.0, 0.16, 0.015, 1.0), 0.15, "Orange"),
    (2.0 / 3.0, (1.0, 0.62, 0.04, 1.0), 0.2, "Yellow"),
    (1.0, (1.0, 0.82, 0.58, 1.0), 0.25, "Cream"),
)


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_015", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    pitch_experiment = load_previous_experiment()
    yaw_experiment = pitch_experiment.load_previous_experiment()
    radius_experiment = yaw_experiment.load_previous_experiment()
    transform_order_experiment = radius_experiment.load_previous_experiment()
    pre_rotation_arc = transform_order_experiment.load_pre_rotation_arc_experiment()
    pre_rotation_arc.COLOR_STOPS = COLOR_STOPS

    transform_order_experiment.load_pre_rotation_arc_experiment = lambda: pre_rotation_arc
    radius_experiment.load_previous_experiment = lambda: transform_order_experiment
    yaw_experiment.load_previous_experiment = lambda: radius_experiment
    pitch_experiment.load_previous_experiment = lambda: yaw_experiment
    pitch_experiment.BLEND_PATH = BLEND_PATH
    pitch_experiment.RENDER_PATH = RENDER_PATH
    pitch_experiment.main()


if __name__ == "__main__":
    main()
