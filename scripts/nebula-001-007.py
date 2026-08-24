"""Increase mask contrast, then apply a conservative five-tap alpha blur."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "nebula-001-004.py"
COLOR_FIELD_PATH = ROOT / "textures" / "example-base-layer-blurred-4k.png"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-007.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-007.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-007-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-007-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-007-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)


def load_hybrid_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("nebula_001_004", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def configure_contrast_ramp(ramp, cloud_index):
    elements = sorted(ramp.color_ramp.elements, key=lambda element: element.position)
    if cloud_index == 3:
        ramp.color_ramp.interpolation = "B_SPLINE"
        positions = (0.12, 0.38, 0.72, 0.94)
        values = (0.0, 0.12, 0.90, 1.0)
    else:
        ramp.color_ramp.interpolation = "EASE"
        positions = (0.16, 0.42, 0.68, 0.90)
        values = (0.0, 0.10, 0.90, 1.0)
    for element, position, value in zip(elements, positions, values):
        element.position = position
        element.color = (value, value, value, 1.0)


def add_contrast_then_blur(material, cloud_index):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    crop = nodes.get("Center Crop Historical 4:3 Mask")
    center_image = nodes.get("Historical Organic Mask")
    center_ramp = nodes.get("Historical Mask Soft Contrast")
    alpha_product = nodes.get("Organic Structure x Procedural Detail")
    configure_contrast_ramp(center_ramp, cloud_index)

    old_link = next(
        link for link in links
        if link.to_node == alpha_product and link.to_socket == alpha_product.inputs[1]
    )
    links.remove(old_link)

    weighted_outputs = []
    samples = (
        ("Center", (0.0, 0.0, 0.0), 0.40),
        ("Left", (-0.006, 0.0, 0.0), 0.15),
        ("Right", (0.006, 0.0, 0.0), 0.15),
        ("Down", (0.0, -0.006, 0.0), 0.15),
        ("Up", (0.0, 0.006, 0.0), 0.15),
    )
    for sample_index, (label, offset, weight) in enumerate(samples):
        if sample_index == 0:
            sample_ramp = center_ramp
        else:
            vector_add = nodes.new("ShaderNodeVectorMath")
            vector_add.name = f"Blur Offset {label}"
            vector_add.operation = "ADD"
            vector_add.inputs[1].default_value = offset
            sample_image = nodes.new("ShaderNodeTexImage")
            sample_image.name = f"Historical Mask Sample {label}"
            sample_image.image = center_image.image
            sample_image.image.colorspace_settings.name = "Non-Color"
            sample_image.extension = "EXTEND"
            sample_ramp = nodes.new("ShaderNodeValToRGB")
            sample_ramp.name = f"Contrast Sample {label}"
            for extra in range(2):
                sample_ramp.color_ramp.elements.new((0.42, 0.68)[extra])
            configure_contrast_ramp(sample_ramp, cloud_index)
            links.new(crop.outputs["Vector"], vector_add.inputs[0])
            links.new(vector_add.outputs["Vector"], sample_image.inputs["Vector"])
            links.new(sample_image.outputs["Color"], sample_ramp.inputs["Fac"])

        weighted = nodes.new("ShaderNodeMath")
        weighted.name = f"Blur Weight {label}"
        weighted.operation = "MULTIPLY"
        weighted.inputs[1].default_value = weight
        links.new(sample_ramp.outputs["Color"], weighted.inputs[0])
        weighted_outputs.append(weighted.outputs[0])

    blurred_output = weighted_outputs[0]
    for add_index, sample_output in enumerate(weighted_outputs[1:], start=1):
        add = nodes.new("ShaderNodeMath")
        add.name = f"Five Tap Blur Sum {add_index}"
        add.operation = "ADD"
        links.new(blurred_output, add.inputs[0])
        links.new(sample_output, add.inputs[1])
        blurred_output = add.outputs[0]
    links.new(blurred_output, alpha_product.inputs[1])
    material["mask_adjustment"] = "Higher contrast followed by five-tap 12-pixel alpha blur"


def main():
    hybrid = load_hybrid_experiment()
    hybrid.BLEND_PATH = BLEND_PATH
    hybrid.PREVIEW_PATH = PREVIEW_PATH
    hybrid.BACKGROUND_PATH = BACKGROUND_PATH
    hybrid.COMPOSITE_PATH = COMPOSITE_PATH
    hybrid.CLOUD_PATHS = CLOUD_PATHS
    original_loader = hybrid.load_previous_experiment

    def load_with_contrast_blur():
        experiment = original_loader()
        experiment.COLOR_FIELD_PATH = COLOR_FIELD_PATH

        def render_cloud_layers(helpers):
            helpers.clear_scene()
            helpers.make_camera(aspect=1.0)
            for index, (settings, path) in enumerate(
                zip(experiment.LAYER_SETTINGS, experiment.CLOUD_PATHS), start=1
            ):
                plane = helpers.make_plane(f"Generator {settings['name']}", size=10.0)
                material = experiment.make_masked_color_material(helpers, settings)
                add_contrast_then_blur(material, index)
                plane.data.materials.append(material)
                helpers.configure_render(*helpers.LAYER_SIZE, path, transparent=True)
                bpy.ops.render.render(write_still=True)
                bpy.data.objects.remove(plane, do_unlink=True)
                print(f"Baked contrast-blurred layer {index}: {path}")

        experiment.render_cloud_layers = render_cloud_layers
        return experiment

    hybrid.load_previous_experiment = load_with_contrast_blur
    hybrid.main()


if __name__ == "__main__":
    main()
