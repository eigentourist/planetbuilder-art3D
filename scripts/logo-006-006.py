"""Generate logo 006-006 on a ten-unit-radius circular baseline."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-005.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-006.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-006.png"
BASELINE_RADIUS = 10.0


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_005", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    arc_experiment = experiment.load_arc_experiment()
    arc_experiment.BASELINE_RADIUS = BASELINE_RADIUS
    experiment.load_arc_experiment = lambda: arc_experiment
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
