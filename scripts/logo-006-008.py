"""Generate logo 006-008 with camera-left key and right-rear rim lighting."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-007.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-008.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-008.png"


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

    def make_reversed_lighting(lighting, base, camera):
        key, fill, rim = lighting.make_three_light_rig(base, camera)
        key.location.x = -abs(key.location.x)
        key["placement_description"] = "Above, left, and slightly in front of the camera"
        base.point_camera_at(key, (0.0, 0.0, 0.0))
        rim.location.x = 5.5
        rim.data.size = 8.0
        rim["placement_description"] = "Behind the logo, above, and toward the right side"
        rim["size_description"] = "Large"
        base.point_camera_at(rim, (0.0, 0.0, 0.0))
        return key, fill, rim

    arc_experiment.make_current_lighting = make_reversed_lighting
    centered_experiment.load_arc_experiment = lambda: arc_experiment
    radius_experiment.load_previous_experiment = lambda: centered_experiment
    experiment.load_previous_experiment = lambda: radius_experiment
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
