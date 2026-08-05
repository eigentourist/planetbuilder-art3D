"""Generate logo experiment 004-002: Days One font comparison."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-001.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-002.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-002.png"
FONT_PATH = ROOT / "fonts" / "Days_One" / "DaysOne-Regular.ttf"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_001", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.FONT_PATH = FONT_PATH

    previous_make_letter = experiment.make_letter

    def make_days_one_letter(*args, **kwargs):
        letter = previous_make_letter(*args, **kwargs)
        letter["font_choice"] = "Days One"
        return letter

    experiment.make_letter = make_days_one_letter
    experiment.main()


if __name__ == "__main__":
    main()
