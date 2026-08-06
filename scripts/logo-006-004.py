"""Generate logo 006-004 with the radius-one character arrangement centered for inspection."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-006-003.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-004.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-004.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_006_003", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arrangement_center(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    minimum = Vector(tuple(min(point[axis] for point in points) for axis in range(3)))
    maximum = Vector(tuple(max(point[axis] for point in points) for axis in range(3)))
    return (minimum + maximum) / 2.0


def main():
    experiment = load_previous_experiment()
    original_place_characters_on_arc = experiment.place_characters_on_arc

    def place_and_center_characters(characters):
        original_place_characters_on_arc(characters)
        center = arrangement_center(characters)
        for character in characters:
            character.location -= center
            character["arc_arrangement_center_offset"] = tuple(center)

    experiment.place_characters_on_arc = place_and_center_characters
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
