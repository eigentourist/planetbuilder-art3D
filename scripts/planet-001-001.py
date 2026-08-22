"""Create the first textured forest-planet design experiment."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MOON_HELPERS = ROOT / "scripts" / "moon-001-001.py"
BLEND_PATH = ROOT / "blendfiles" / "planet-001-001.blend"
RENDER_PATH = ROOT / "renders" / "planet-001-001.png"
BASE_COLOR_PATH = ROOT / "textures" / "forest-planet.png"
NORMAL_PATH = ROOT / "textures" / "forest-planet" / "forest-planet_normal.png"
ORM_PATH = ROOT / "textures" / "forest-planet" / "forest-planet_orm.png"
HEIGHT_PATH = ROOT / "textures" / "forest-planet" / "forest-planet_height.png"
CAMERA_DISTANCE = 45.0


def load_geometry_and_material_helpers():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("moon_001_001_helpers", MOON_HELPERS)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_geometry_and_material_helpers()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.RENDER_PATH = RENDER_PATH
    experiment.BASE_COLOR_PATH = BASE_COLOR_PATH
    experiment.NORMAL_PATH = NORMAL_PATH
    experiment.ORM_PATH = ORM_PATH
    experiment.HEIGHT_PATH = HEIGHT_PATH
    experiment.CAMERA_DISTANCE = CAMERA_DISTANCE

    original_make_material = experiment.make_material
    original_make_moon = experiment.make_moon
    original_make_camera = experiment.make_camera

    def make_planet_material():
        material = original_make_material()
        material.name = "Forest Planet Material"
        material["asset"] = "Forest Planet"
        for node in material.node_tree.nodes:
            if "desert-moon" in node.label:
                node.label = node.label.replace("desert-moon", "forest-planet")
        for image in (
            experiment.bpy.data.images.get("Desert Moon Base Color"),
            experiment.bpy.data.images.get("Desert Moon ORM"),
            experiment.bpy.data.images.get("Desert Moon Normal"),
            experiment.bpy.data.images.get("Desert Moon Height"),
        ):
            if image is not None:
                image.name = image.name.replace("Desert Moon", "Forest Planet")
        return material

    def make_planet(material):
        planet = original_make_moon(material)
        planet.name = "Forest Planet"
        planet.data.name = "Forest Planet Mesh"
        planet["asset_type"] = "Forest Planet"
        return planet

    def make_planet_camera():
        camera = original_make_camera()
        camera.name = "Planet Camera"
        camera.data.name = "Planet Camera"
        camera["framing_goal"] = "Centered; planet approximately one third of frame height"
        return camera

    def make_planet_lighting():
        experiment.make_area_light(
            "Key Light",
            (8.0, -12.0, 8.0),
            1000.0,
            1.5,
            "Above, camera-right, and slightly in front of the camera-facing planet",
        )
        experiment.make_area_light(
            "Fill Light",
            (0.0, -10.0, 8.0),
            600.0,
            1.5,
            "Slightly above the camera axis",
        )
        experiment.make_area_light(
            "Rim Light",
            (0.0, 8.0, 8.0),
            400.0,
            1.5,
            "Behind the planet, above, and centered",
        )

    experiment.make_material = make_planet_material
    experiment.make_moon = make_planet
    experiment.make_camera = make_planet_camera
    experiment.make_lighting = make_planet_lighting
    experiment.main()


if __name__ == "__main__":
    main()
