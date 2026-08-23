"""Soften, broaden, and modestly brighten the masked nebula layers."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "nebula-001-002.py"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-003.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-003.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-003-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-003-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-003-cloud{index:02d}-2k.png"
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
    settings[0]["mapping_scale"] = (0.72, 1.25, 1.0)
    settings[0]["value"] = 0.54
    settings[1]["mapping_scale"] = (1.30, 0.68, 1.0)
    settings[1]["value"] = 0.50
    settings[2]["mapping_scale"] = (0.55, 1.90, 1.0)
    settings[2]["value"] = 0.60
    experiment.LAYER_SETTINGS = settings

    original_make_material = experiment.make_masked_color_material

    def make_softened_material(experiment_helpers, layer_settings):
        material = original_make_material(experiment_helpers, layer_settings)
        ramp_node = next(node for node in material.node_tree.nodes if node.type == "VALTORGB")
        ramp_node.color_ramp.interpolation = "EASE"
        elements = sorted(ramp_node.color_ramp.elements, key=lambda element: element.position)
        positions = (0.46, 0.56, 0.68, 0.83)
        alphas = (0.0, 0.08, 0.48, 0.78)
        for element, position, alpha in zip(elements, positions, alphas):
            element.position = position
            color = element.color
            element.color = (color[0], color[1], color[2], alpha)
        material["mask_adjustment"] = "Broader EASE transition for diffuse cloud boundaries"
        return material

    experiment.make_masked_color_material = make_softened_material
    experiment.main()


if __name__ == "__main__":
    main()
