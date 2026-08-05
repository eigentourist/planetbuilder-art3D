"""Generate logo 005-003 with an additional positive yaw on P, L, and A."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys

from mathutils import Matrix, Vector


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-001.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-005-003.blend"
RENDER_PATH = ROOT / "renders" / "logo-005-003.png"
INDIVIDUAL_YAW_DEGREES = 2.0
INDIVIDUAL_YAW_CHARACTERS = {"P", "L", "A"}


def load_lighting_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_001", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def object_bounds_center(obj):
    points = [Vector(corner) for corner in obj.bound_box]
    minimum = Vector(tuple(min(point[axis] for point in points) for axis in range(3)))
    maximum = Vector(tuple(max(point[axis] for point in points) for axis in range(3)))
    return (minimum + maximum) / 2.0


def main():
    lighting = load_lighting_experiment()
    shape = lighting.load_shape_experiment()

    def apply_shared_orientation_with_selected_yaw(objects):
        shared_center = shape.bounds_center(objects)
        pitch = Matrix.Rotation(radians(shape.PITCH_DEGREES), 4, "X")
        yaw = Matrix.Rotation(radians(shape.YAW_DEGREES), 4, "Y")
        shared = Matrix.Translation(shared_center) @ yaw @ pitch @ Matrix.Translation(-shared_center)

        for obj in objects:
            obj.data.transform(shared @ obj.matrix_world)
            obj.matrix_world = Matrix.Identity(4)
            individual_yaw_degrees = 0.0
            if obj["character"] in INDIVIDUAL_YAW_CHARACTERS:
                individual_yaw_degrees = INDIVIDUAL_YAW_DEGREES
                character_center = object_bounds_center(obj)
                individual_yaw = (
                    Matrix.Translation(character_center)
                    @ Matrix.Rotation(radians(individual_yaw_degrees), 4, "Y")
                    @ Matrix.Translation(-character_center)
                )
                obj.data.transform(individual_yaw)
            obj.data.update()
            obj["pitch_degrees"] = shape.PITCH_DEGREES
            obj["shared_yaw_degrees"] = shape.YAW_DEGREES
            obj["individual_yaw_degrees"] = individual_yaw_degrees
            obj["yaw_method"] = "Shared-pivot yaw plus selected per-character center yaw"

    shape.apply_shared_orientation = apply_shared_orientation_with_selected_yaw
    lighting.load_shape_experiment = lambda: shape
    lighting.BLEND_PATH = BLEND_PATH
    lighting.RENDER_PATH = RENDER_PATH
    lighting.main()


if __name__ == "__main__":
    main()
