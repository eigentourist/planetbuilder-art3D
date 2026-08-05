"""Generate logo experiment 004-012: widen the left-side letters within the guide corridor."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-009.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-012.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-012.png"

PITCH_DEGREES = 20.0
YAW_DEGREES = 15.0
ROLL_DEGREES = 4.0
CAMERA_DISTANCE = 21.0
LEFT_LETTER_WIDTH_SCALE = 1.18
RIGHT_LETTER_WIDTH_SCALE = 1.0


def load_roll_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_009", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def connected_vertex_groups(mesh):
    neighbors = [set() for _vertex in mesh.vertices]
    for edge in mesh.edges:
        first, second = edge.vertices
        neighbors[first].add(second)
        neighbors[second].add(first)

    remaining = set(range(len(mesh.vertices)))
    groups = []
    while remaining:
        seed = remaining.pop()
        group = {seed}
        stack = [seed]
        while stack:
            current = stack.pop()
            additions = neighbors[current] & remaining
            remaining.difference_update(additions)
            group.update(additions)
            stack.extend(additions)
        groups.append(group)
    return groups


def widen_letters_from_right_to_left(text):
    groups = connected_vertex_groups(text.data)
    bounds = []
    for group in groups:
        x_values = [text.data.vertices[index].co.x for index in group]
        bounds.append((min(x_values), max(x_values), group))
    bounds.sort(key=lambda item: item[0])

    logo_left = min(item[0] for item in bounds)
    logo_right = max(item[1] for item in bounds)
    logo_width = logo_right - logo_left
    for minimum, maximum, group in bounds:
        center = (minimum + maximum) / 2.0
        rightward_progress = (center - logo_left) / logo_width
        scale = LEFT_LETTER_WIDTH_SCALE + rightward_progress * (
            RIGHT_LETTER_WIDTH_SCALE - LEFT_LETTER_WIDTH_SCALE
        )
        for index in group:
            vertex = text.data.vertices[index]
            vertex.co.x = center + (vertex.co.x - center) * scale

    text.data.validate(verbose=False)
    text.data.update()
    text["left_letter_width_scale"] = LEFT_LETTER_WIDTH_SCALE
    text["right_letter_width_scale"] = RIGHT_LETTER_WIDTH_SCALE
    text["horizontal_occupancy_method"] = "Per-letter widening about fixed centers, tapered left to right"
    print(f"Horizontally widened {len(groups)} connected letter meshes")


def main():
    roll_experiment = load_roll_experiment()
    orientation_experiment = roll_experiment.load_previous_experiment()
    spacing_experiment = orientation_experiment.load_spacing_experiment()
    original_fit = spacing_experiment.fit_mesh_to_guides

    def fit_and_widen(text, upper_path, lower_path):
        original_fit(text, upper_path, lower_path)
        widen_letters_from_right_to_left(text)

    spacing_experiment.fit_mesh_to_guides = fit_and_widen
    orientation_experiment.load_spacing_experiment = lambda: spacing_experiment
    roll_experiment.load_previous_experiment = lambda: orientation_experiment

    roll_experiment.BLEND_PATH = BLEND_PATH
    roll_experiment.RENDER_PATH = RENDER_PATH
    roll_experiment.PITCH_DEGREES = PITCH_DEGREES
    roll_experiment.YAW_DEGREES = YAW_DEGREES
    roll_experiment.ROLL_DEGREES = ROLL_DEGREES
    roll_experiment.CAMERA_DISTANCE = CAMERA_DISTANCE
    roll_experiment.main()


if __name__ == "__main__":
    main()
