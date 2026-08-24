"""Compare the hybrid nebula recipe using the blurred 4K color field."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "nebula-001-004.py"
COLOR_FIELD_PATH = ROOT / "textures" / "example-base-layer-blurred-4k.png"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-005.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-005.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-005-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-005-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-005-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)


def load_hybrid_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("nebula_001_004", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    hybrid = load_hybrid_experiment()
    hybrid.BLEND_PATH = BLEND_PATH
    hybrid.PREVIEW_PATH = PREVIEW_PATH
    hybrid.BACKGROUND_PATH = BACKGROUND_PATH
    hybrid.COMPOSITE_PATH = COMPOSITE_PATH
    hybrid.CLOUD_PATHS = CLOUD_PATHS

    original_loader = hybrid.load_previous_experiment

    def load_with_blurred_color_field():
        experiment = original_loader()
        experiment.COLOR_FIELD_PATH = COLOR_FIELD_PATH
        return experiment

    hybrid.load_previous_experiment = load_with_blurred_color_field
    hybrid.main()


if __name__ == "__main__":
    main()
