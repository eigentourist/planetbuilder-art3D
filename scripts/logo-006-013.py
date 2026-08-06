"""Generate logo 006-013 on a fifteen-unit-radius circular baseline."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-012.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-013.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-013.png"
BASELINE_RADIUS = 15.0


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_012", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    pre_rotation_arc = experiment.load_pre_rotation_arc_experiment()
    preferred_arc = pre_rotation_arc.load_previous_experiment()
    radius_experiment = preferred_arc.load_previous_experiment()
    radius_experiment.BASELINE_RADIUS = BASELINE_RADIUS

    preferred_arc.load_previous_experiment = lambda: radius_experiment
    pre_rotation_arc.load_previous_experiment = lambda: preferred_arc
    experiment.load_pre_rotation_arc_experiment = lambda: pre_rotation_arc
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
