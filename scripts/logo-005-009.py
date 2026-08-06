"""Generate logo 005-009 with a large left-rear rim light."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-008.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-009.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-009.png"
RIM_LIGHT_SIZE = 8.0


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_008", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    key_experiment = experiment.load_previous_experiment()
    guide_removal = key_experiment.load_previous_experiment()
    camera_experiment = guide_removal.load_previous_experiment()
    shape_experiment = camera_experiment.load_previous_experiment()
    lighting = shape_experiment.load_lighting_experiment()
    original_make_three_light_rig = lighting.make_three_light_rig

    def make_large_rim_light_rig(base, camera):
        key, fill, rim = original_make_three_light_rig(base, camera)
        rim.data.size = RIM_LIGHT_SIZE
        rim["size_description"] = "Large"
        return key, fill, rim

    lighting.make_three_light_rig = make_large_rim_light_rig
    shape_experiment.load_lighting_experiment = lambda: lighting
    camera_experiment.load_previous_experiment = lambda: shape_experiment
    guide_removal.load_previous_experiment = lambda: camera_experiment
    key_experiment.load_previous_experiment = lambda: guide_removal
    experiment.load_previous_experiment = lambda: key_experiment
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
