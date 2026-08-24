"""Soften the bubble-like contour in cloud03's lower-right quadrant."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "nebula-001-004.py"
COLOR_FIELD_PATH = ROOT / "textures" / "example-base-layer-blurred-4k.png"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-006.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-006.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-006-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-006-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-006-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)


def load_hybrid_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("nebula_001_004", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    hybrid = load_hybrid_experiment()
    hybrid.BLEND_PATH = BLEND_PATH
    hybrid.PREVIEW_PATH = PREVIEW_PATH
    hybrid.BACKGROUND_PATH = BACKGROUND_PATH
    hybrid.COMPOSITE_PATH = COMPOSITE_PATH
    hybrid.CLOUD_PATHS = CLOUD_PATHS

    original_loader = hybrid.load_previous_experiment

    def load_with_cloud03_smoothing():
        experiment = original_loader()
        experiment.COLOR_FIELD_PATH = COLOR_FIELD_PATH

        def render_cloud_layers(experiment_helpers):
            experiment_helpers.clear_scene()
            experiment_helpers.make_camera(aspect=1.0)
            for index, (settings, path) in enumerate(
                zip(experiment.LAYER_SETTINGS, experiment.CLOUD_PATHS),
                start=1,
            ):
                plane = experiment_helpers.make_plane(
                    f"Generator {settings['name']}", size=10.0
                )
                material = experiment.make_masked_color_material(
                    experiment_helpers, settings
                )
                if index == 3:
                    ramp = material.node_tree.nodes.get("Historical Mask Soft Contrast")
                    ramp.color_ramp.interpolation = "B_SPLINE"
                    elements = sorted(
                        ramp.color_ramp.elements, key=lambda element: element.position
                    )
                    for element, position, value in zip(
                        elements,
                        (0.12, 0.38, 0.72, 0.94),
                        (0.18, 0.42, 0.78, 0.96),
                    ):
                        element.position = position
                        element.color = (value, value, value, 1.0)
                    material["cloud03_adjustment"] = (
                        "Gentler B-spline historical-mask remap to soften rounded contours"
                    )
                plane.data.materials.append(material)
                experiment_helpers.configure_render(
                    *experiment_helpers.LAYER_SIZE, path, transparent=True
                )
                bpy.ops.render.render(write_still=True)
                bpy.data.objects.remove(plane, do_unlink=True)
                print(f"Baked masked color layer {index}: {path}")

        experiment.render_cloud_layers = render_cloud_layers
        return experiment

    hybrid.load_previous_experiment = load_with_cloud03_smoothing
    hybrid.main()


if __name__ == "__main__":
    main()
