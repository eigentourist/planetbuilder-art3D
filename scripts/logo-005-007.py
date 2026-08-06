"""Generate logo 005-007 with the key light on the camera's right side."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-006.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-007.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-007.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_006", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    previous = load_previous_experiment()
    camera_experiment = previous.load_previous_experiment()
    shape_experiment = camera_experiment.load_previous_experiment()
    lighting = shape_experiment.load_lighting_experiment()
    original_make_three_light_rig = lighting.make_three_light_rig

    def make_right_key_light_rig(base, camera):
        key, fill, rim = original_make_three_light_rig(base, camera)
        key.location.x = abs(key.location.x)
        key["placement_description"] = "Above, right, and slightly in front of the camera"
        base.point_camera_at(key, (0.0, 0.0, 0.0))
        return key, fill, rim

    lighting.make_three_light_rig = make_right_key_light_rig
    shape_experiment.load_lighting_experiment = lambda: lighting
    camera_experiment.load_previous_experiment = lambda: shape_experiment
    previous.load_previous_experiment = lambda: camera_experiment
    previous.BLEND_PATH = BLEND_PATH
    previous.RENDER_PATH = RENDER_PATH
    previous.main()


if __name__ == "__main__":
    main()
