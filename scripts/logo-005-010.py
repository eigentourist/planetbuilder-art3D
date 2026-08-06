"""Generate logo 005-010 with subtly relaxed left-hand guide curvature."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-009.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-010.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-010.png"
LEFT_RELAXATION = 0.08
RELAXATION_END_X = 1.0
LEFTMOST_CONTROL_X = -5.55


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_009", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def relax_coordinate(coordinate, right_anchor_y):
    x, y, z = coordinate
    progress = (RELAXATION_END_X - x) / (RELAXATION_END_X - LEFTMOST_CONTROL_X)
    influence = max(0.0, min(1.0, progress)) ** 2
    strength = LEFT_RELAXATION * influence
    return (x, right_anchor_y + (y - right_anchor_y) * (1.0 - strength), z)


def main():
    rim_size_experiment = load_previous_experiment()
    rim_position_experiment = rim_size_experiment.load_previous_experiment()
    key_experiment = rim_position_experiment.load_previous_experiment()
    guide_removal = key_experiment.load_previous_experiment()
    camera_experiment = guide_removal.load_previous_experiment()
    shape_experiment = camera_experiment.load_previous_experiment()
    lighting = shape_experiment.load_lighting_experiment()
    shape = lighting.load_shape_experiment()
    roll = shape.load_roll_experiment()
    orientation = roll.load_previous_experiment()
    spacing = orientation.load_spacing_experiment()
    layout = spacing.load_layout_helpers()
    base = layout.load_version_003_helpers()

    base.BASE_POINTS = tuple(
        tuple(relax_coordinate(coordinate, base.RIGHT_ANCHOR_Y) for coordinate in point)
        for point in base.BASE_POINTS
    )

    layout.load_version_003_helpers = lambda: base
    spacing.load_layout_helpers = lambda: layout
    orientation.load_spacing_experiment = lambda: spacing
    roll.load_previous_experiment = lambda: orientation
    shape.load_roll_experiment = lambda: roll
    lighting.load_shape_experiment = lambda: shape
    shape_experiment.load_lighting_experiment = lambda: lighting
    camera_experiment.load_previous_experiment = lambda: shape_experiment
    guide_removal.load_previous_experiment = lambda: camera_experiment
    key_experiment.load_previous_experiment = lambda: guide_removal
    rim_position_experiment.load_previous_experiment = lambda: key_experiment
    rim_size_experiment.load_previous_experiment = lambda: rim_position_experiment
    rim_size_experiment.BLEND_PATH = BLEND_PATH
    rim_size_experiment.RENDER_PATH = RENDER_PATH
    rim_size_experiment.main()


if __name__ == "__main__":
    main()
