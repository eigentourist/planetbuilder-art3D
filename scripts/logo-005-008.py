"""Generate logo 005-008 with the rim light behind, above, and left of the logo."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-007.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-008.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-008.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_007", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    guide_removal = experiment.load_previous_experiment()
    camera_experiment = guide_removal.load_previous_experiment()
    shape_experiment = camera_experiment.load_previous_experiment()
    lighting = shape_experiment.load_lighting_experiment()
    original_make_three_light_rig = lighting.make_three_light_rig

    def make_left_rim_light_rig(base, camera):
        key, fill, rim = original_make_three_light_rig(base, camera)
        rim.location.x = -5.5
        rim["placement_description"] = "Behind the logo, above, and toward the left side"
        base.point_camera_at(rim, (0.0, 0.0, 0.0))
        return key, fill, rim

    lighting.make_three_light_rig = make_left_rim_light_rig
    shape_experiment.load_lighting_experiment = lambda: lighting
    camera_experiment.load_previous_experiment = lambda: shape_experiment
    guide_removal.load_previous_experiment = lambda: camera_experiment
    experiment.load_previous_experiment = lambda: guide_removal
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
