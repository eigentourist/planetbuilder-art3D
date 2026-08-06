"""Generate logo 006-009 with twenty-degree yaw and reduced material roughness."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-007.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-009.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-009.png"
YAW_DEGREES = 20.0

COLOR_STOPS = (
    (0.0, (0.65, 0.015, 0.008, 1.0), 0.3, "Red"),
    (1.0 / 3.0, (1.0, 0.16, 0.015, 1.0), 0.25, "Orange"),
    (2.0 / 3.0, (1.0, 0.62, 0.04, 1.0), 0.2, "Yellow"),
    (1.0, (1.0, 0.82, 0.58, 1.0), 0.1, "Cream"),
)


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_007", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    radius_experiment = experiment.load_previous_experiment()
    centered_experiment = radius_experiment.load_previous_experiment()
    arc_experiment = centered_experiment.load_arc_experiment()
    arc_experiment.YAW_DEGREES = YAW_DEGREES
    arc_experiment.COLOR_STOPS = COLOR_STOPS

    centered_experiment.load_arc_experiment = lambda: arc_experiment
    radius_experiment.load_previous_experiment = lambda: centered_experiment
    experiment.load_previous_experiment = lambda: radius_experiment
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
