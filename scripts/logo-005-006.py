"""Generate logo 005-006 with construction guides removed after fitting."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-005.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-006.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-006.png"


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_005", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    shape_experiment = experiment.load_previous_experiment()
    lighting = shape_experiment.load_lighting_experiment()
    shape = lighting.load_shape_experiment()
    roll = shape.load_roll_experiment()
    original_roll_as_group = roll.roll_as_group

    def remove_guides_then_roll(objects):
        guide_objects = tuple(objects[:4])
        character_objects = tuple(objects[4:])
        for guide in guide_objects:
            bpy.data.objects.remove(guide, do_unlink=True)
        print(f"Removed {len(guide_objects)} curved guide objects after character fitting")
        return original_roll_as_group(character_objects)

    roll.roll_as_group = remove_guides_then_roll
    shape.load_roll_experiment = lambda: roll
    lighting.load_shape_experiment = lambda: shape
    shape_experiment.load_lighting_experiment = lambda: lighting
    experiment.load_previous_experiment = lambda: shape_experiment
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.main()


if __name__ == "__main__":
    main()
