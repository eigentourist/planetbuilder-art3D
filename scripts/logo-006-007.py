"""Generate logo 006-007 over the final forty degrees of the circle's upper-left quarter."""

from importlib.util import module_from_spec, spec_from_file_location
from math import atan2, cos, pi, sin
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-006.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-007.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-007.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_006", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    centered_experiment = experiment.load_previous_experiment()
    arc_experiment = centered_experiment.load_arc_experiment()

    def place_characters_ending_at_circle_top(characters):
        source_centers = []
        local_centers = []
        for obj in characters:
            x_values = [vertex.co.x for vertex in obj.data.vertices]
            local_center = (min(x_values) + max(x_values)) / 2.0
            local_centers.append(local_center)
            source_centers.append(obj.location.x + local_center)

        first_center = source_centers[0]
        total_arc_length = source_centers[-1] - first_center
        for obj, source_center, local_center in zip(characters, source_centers, local_centers):
            arc_length = source_center - first_center
            remaining_arc = total_arc_length - arc_length
            theta = pi / 2.0 + remaining_arc / arc_experiment.BASELINE_RADIUS
            tangent_x = sin(theta)
            tangent_y = -cos(theta)

            for vertex in obj.data.vertices:
                vertex.co.x -= local_center
            obj.data.update()
            obj.location = (
                arc_experiment.BASELINE_RADIUS * cos(theta),
                arc_experiment.BASELINE_RADIUS * sin(theta),
                0.0,
            )
            obj.rotation_euler.z = atan2(tangent_y, tangent_x)
            obj["baseline_radius"] = arc_experiment.BASELINE_RADIUS
            obj["baseline_arc_length"] = arc_length / arc_experiment.BASELINE_RADIUS
            obj["baseline_angle_radians"] = theta
            obj["baseline_orientation"] = "Local tangent, clockwise toward circle top"

    arc_experiment.place_characters_on_arc = place_characters_ending_at_circle_top
    centered_experiment.load_arc_experiment = lambda: arc_experiment
    experiment.load_previous_experiment = lambda: centered_experiment
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
