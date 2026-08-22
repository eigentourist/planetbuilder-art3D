"""Render the desert moon with a tenfold increase in light power."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "moon-001-001.py"
BLEND_PATH = ROOT / "blendfiles" / "moon-001-002.blend"
RENDER_PATH = ROOT / "renders" / "moon-001-002.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("moon_001_001", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH

    def make_brighter_lighting():
        experiment.make_area_light(
            "Key Light",
            (8.0, -12.0, 8.0),
            1000.0,
            1.5,
            "Above, camera-right, and slightly in front of the camera-facing moon",
        )
        experiment.make_area_light(
            "Fill Light",
            (0.0, -10.0, 8.0),
            600.0,
            1.5,
            "Slightly above the camera axis",
        )
        experiment.make_area_light(
            "Rim Light",
            (0.0, 8.0, 8.0),
            400.0,
            1.5,
            "Behind the moon, above, and centered",
        )

    experiment.make_lighting = make_brighter_lighting
    experiment.main()


if __name__ == "__main__":
    main()
