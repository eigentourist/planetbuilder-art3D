"""Combine historical organic masks with restrained procedural detail."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "nebula-001-002.py"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-004.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-004.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-004-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-004-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-004-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)
HISTORICAL_MASK_PATHS = tuple(
    ROOT / "textures" / f"example-noise{index}.png"
    for index in range(1, 4)
)


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("nebula_001_002", SOURCE_SCRIPT)
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

    settings = tuple(dict(item) for item in experiment.LAYER_SETTINGS)
    for item, mask_path in zip(settings, HISTORICAL_MASK_PATHS):
        item["historical_mask_path"] = mask_path
    settings[0].update(mapping_scale=(0.92, 1.08, 1.0), noise_scale=3.2, value=0.59)
    settings[1].update(mapping_scale=(1.08, 0.92, 1.0), noise_scale=3.6, value=0.55)
    settings[2].update(mapping_scale=(0.82, 1.18, 1.0), noise_scale=4.2, value=0.66)
    experiment.LAYER_SETTINGS = settings

    original_make_material = experiment.make_masked_color_material

    def make_hybrid_material(experiment_helpers, layer_settings):
        material = original_make_material(experiment_helpers, layer_settings)
        nodes = material.node_tree.nodes
        links = material.node_tree.links

        procedural_ramp = next(node for node in nodes if node.type == "VALTORGB")
        procedural_ramp.color_ramp.interpolation = "EASE"
        elements = sorted(procedural_ramp.color_ramp.elements, key=lambda element: element.position)
        for element, position, alpha in zip(
            elements,
            (0.43, 0.53, 0.66, 0.82),
            (0.0, 0.10, 0.52, 0.80),
        ):
            element.position = position
            color = element.color
            element.color = (color[0], color[1], color[2], alpha)

        texcoord = next(node for node in nodes if node.type == "TEX_COORD")
        mix_shader = next(node for node in nodes if node.type == "MIX_SHADER")
        old_alpha_link = next(
            link for link in links
            if link.to_node == mix_shader and link.to_socket == mix_shader.inputs[0]
        )
        links.remove(old_alpha_link)

        mask_crop = nodes.new("ShaderNodeVectorMath")
        mask_crop.name = "Center Crop Historical 4:3 Mask"
        mask_crop.operation = "MULTIPLY_ADD"
        mask_crop.location = (-760, -500)
        mask_crop.inputs[1].default_value = (0.75, 1.0, 1.0)
        mask_crop.inputs[2].default_value = (0.125, 0.0, 0.0)

        historical_image = nodes.new("ShaderNodeTexImage")
        historical_image.name = "Historical Organic Mask"
        historical_image.image = bpy.data.images.load(
            str(layer_settings["historical_mask_path"]), check_existing=True
        )
        historical_image.image.colorspace_settings.name = "Non-Color"
        historical_image.extension = "EXTEND"
        historical_image.location = (-500, -500)

        historical_ramp = nodes.new("ShaderNodeValToRGB")
        historical_ramp.name = "Historical Mask Soft Contrast"
        historical_ramp.location = (-180, -480)
        historical_ramp.color_ramp.interpolation = "EASE"
        first = historical_ramp.color_ramp.elements[0]
        first.position = 0.16
        first.color = (0.12, 0.12, 0.12, 1.0)
        middle_low = historical_ramp.color_ramp.elements.new(0.42)
        middle_low.color = (0.38, 0.38, 0.38, 1.0)
        middle_high = historical_ramp.color_ramp.elements.new(0.68)
        middle_high.color = (0.82, 0.82, 0.82, 1.0)
        last = historical_ramp.color_ramp.elements[1]
        last.position = 0.90
        last.color = (1.0, 1.0, 1.0, 1.0)

        alpha_product = nodes.new("ShaderNodeMath")
        alpha_product.name = "Organic Structure x Procedural Detail"
        alpha_product.operation = "MULTIPLY"
        alpha_product.location = (170, -220)

        links.new(texcoord.outputs["Generated"], mask_crop.inputs[0])
        links.new(mask_crop.outputs["Vector"], historical_image.inputs["Vector"])
        links.new(historical_image.outputs["Color"], historical_ramp.inputs["Fac"])
        links.new(procedural_ramp.outputs["Alpha"], alpha_product.inputs[0])
        links.new(historical_ramp.outputs["Color"], alpha_product.inputs[1])
        links.new(alpha_product.outputs[0], mix_shader.inputs[0])

        material["mask_style"] = "Historical organic structure multiplied by procedural detail"
        material["historical_mask"] = str(
            layer_settings["historical_mask_path"].relative_to(ROOT)
        )
        return material

    experiment.make_masked_color_material = make_hybrid_material
    experiment.main()


if __name__ == "__main__":
    main()
