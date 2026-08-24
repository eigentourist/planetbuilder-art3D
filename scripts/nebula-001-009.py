"""Gently distort cloud03 color coordinates to bend geometric contours."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "nebula-001-007.py"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-009.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-009.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-009-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-009-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-009-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("nebula_001_007", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def color_field_input(material):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    color_field = nodes.get("4K Color Field (sRGB)")
    color_link = next(
        link for link in links
        if link.to_node == color_field and link.to_socket == color_field.inputs["Vector"]
    )
    color_crop = color_link.from_node
    links.remove(color_link)
    return color_crop, color_field


def rotate_cloud01_color(material):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    color_crop, color_field = color_field_input(material)
    rotate = nodes.new("ShaderNodeVectorRotate")
    rotate.name = "Cloud01 Color Field Rotation"
    rotate.rotation_type = "Z_AXIS"
    rotate.inputs["Center"].default_value = (0.5, 0.5, 0.0)
    rotate.inputs["Angle"].default_value = radians(4.0)
    links.new(color_crop.outputs["Vector"], rotate.inputs["Vector"])
    links.new(rotate.outputs["Vector"], color_field.inputs["Vector"])
    material["cloud01_color_sampling_adjustment"] = (
        "Rotate color coordinates +4 degrees around texture center"
    )


def distort_cloud03_color(material):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    color_crop, color_field = color_field_input(material)

    distortion_noise = nodes.new("ShaderNodeTexNoise")
    distortion_noise.name = "Cloud03 Low Frequency Color Warp"
    distortion_noise.noise_dimensions = "4D"
    distortion_noise.inputs["Scale"].default_value = 1.6
    distortion_noise.inputs["Detail"].default_value = 2.0
    distortion_noise.inputs["Roughness"].default_value = 0.45
    distortion_noise.inputs["Distortion"].default_value = 0.10
    distortion_noise.inputs["W"].default_value = 23.7

    center_noise = nodes.new("ShaderNodeVectorMath")
    center_noise.name = "Center Cloud03 Warp Around Zero"
    center_noise.operation = "SUBTRACT"
    center_noise.inputs[1].default_value = (0.5, 0.5, 0.5)

    scale_noise = nodes.new("ShaderNodeVectorMath")
    scale_noise.name = "Cloud03 Warp Amplitude 0.018"
    scale_noise.operation = "SCALE"
    scale_noise.inputs[3].default_value = 0.018

    add_warp = nodes.new("ShaderNodeVectorMath")
    add_warp.name = "Warp Cloud03 Color Coordinates Only"
    add_warp.operation = "ADD"

    links.new(color_crop.outputs["Vector"], distortion_noise.inputs["Vector"])
    links.new(distortion_noise.outputs["Color"], center_noise.inputs[0])
    links.new(center_noise.outputs["Vector"], scale_noise.inputs[0])
    links.new(color_crop.outputs["Vector"], add_warp.inputs[0])
    links.new(scale_noise.outputs["Vector"], add_warp.inputs[1])
    links.new(add_warp.outputs["Vector"], color_field.inputs["Vector"])
    material["cloud03_color_sampling_adjustment"] = (
        "Low-frequency nonlinear color-coordinate warp at 0.018 amplitude"
    )


def main():
    experiment = load_previous_experiment()
    experiment.BLEND_PATH = BLEND_PATH
    experiment.PREVIEW_PATH = PREVIEW_PATH
    experiment.BACKGROUND_PATH = BACKGROUND_PATH
    experiment.COMPOSITE_PATH = COMPOSITE_PATH
    experiment.CLOUD_PATHS = CLOUD_PATHS
    original_adjustment = experiment.add_contrast_then_blur

    def add_blur_and_color_adjustments(material, cloud_index):
        original_adjustment(material, cloud_index)
        if cloud_index == 1:
            rotate_cloud01_color(material)
        elif cloud_index == 3:
            distort_cloud03_color(material)

    experiment.add_contrast_then_blur = add_blur_and_color_adjustments
    experiment.main()


if __name__ == "__main__":
    main()
