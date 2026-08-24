"""Rotate only cloud01's color-field sampling to disrupt an angular contour."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "nebula-001-007.py"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-008.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-008.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-008-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-008-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-008-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("nebula_001_007", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    experiment = load_previous_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.PREVIEW_PATH = PREVIEW_PATH
    experiment.BACKGROUND_PATH = BACKGROUND_PATH
    experiment.COMPOSITE_PATH = COMPOSITE_PATH
    experiment.CLOUD_PATHS = CLOUD_PATHS

    original_adjustment = experiment.add_contrast_then_blur

    def add_blur_and_cloud01_color_rotation(material, cloud_index):
        original_adjustment(material, cloud_index)
        if cloud_index != 1:
            return

        nodes = material.node_tree.nodes
        links = material.node_tree.links
        color_field = nodes.get("4K Color Field (sRGB)")
        color_link = next(
            link for link in links
            if link.to_node == color_field and link.to_socket == color_field.inputs["Vector"]
        )
        color_crop = color_link.from_node
        links.remove(color_link)

        rotate = nodes.new("ShaderNodeVectorRotate")
        rotate.name = "Cloud01 Color Field Rotation"
        rotate.rotation_type = "Z_AXIS"
        rotate.invert = False
        rotate.inputs["Center"].default_value = (0.5, 0.5, 0.0)
        rotate.inputs["Angle"].default_value = radians(4.0)
        links.new(color_crop.outputs["Vector"], rotate.inputs["Vector"])
        links.new(rotate.outputs["Vector"], color_field.inputs["Vector"])
        material["cloud01_color_sampling_adjustment"] = (
            "Rotate color coordinates +4 degrees around texture center; mask unchanged"
        )

    experiment.add_contrast_then_blur = add_blur_and_cloud01_color_rotation
    experiment.main()


if __name__ == "__main__":
    main()
