"""Generate logo version 006 experiment 001 with a logo-wide color and roughness gradient."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-005-012.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-006-001.blend"
RENDER_PATH = ROOT / "renders" / "logo-006-001.png"

COLOR_STOPS = (
    (0.0, (0.30, 0.012, 0.006, 1.0), 0.45, "Deep Red"),
    (1.0 / 3.0, (1.0, 0.16, 0.015, 1.0), 0.35, "Orange"),
    (2.0 / 3.0, (1.0, 0.62, 0.04, 1.0), 0.25, "Yellow"),
    (1.0, (1.0, 0.82, 0.58, 1.0), 0.15, "Cream"),
)


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_005_012", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def configure_ramp(ramp, values):
    first = ramp.elements[0]
    last = ramp.elements[1]
    first.position, first.color = values[0]
    last.position, last.color = values[-1]
    for position, color in values[1:-1]:
        element = ramp.elements.new(position)
        element.color = color
    ramp.interpolation = "LINEAR"


def make_gradient_material(layout):
    material = bpy.data.materials.new("PLANETBUILDER Four-Color Gradient")
    material.diffuse_color = (1.0, 0.28, 0.03, 1.0)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    principled = nodes.get("Principled BSDF")

    gradient_origin = bpy.data.objects.new("Logo Gradient Coordinate Origin", None)
    bpy.context.collection.objects.link(gradient_origin)
    gradient_origin["purpose"] = "Shared logo-wide left-to-right material coordinates"

    coordinates = nodes.new("ShaderNodeTexCoord")
    coordinates.name = "Logo-Wide Coordinates"
    coordinates.object = gradient_origin
    separate = nodes.new("ShaderNodeSeparateXYZ")
    separate.name = "Global Left-to-Right Axis"
    normalized_x = nodes.new("ShaderNodeMapRange")
    normalized_x.name = "Normalize Logo X"
    normalized_x.inputs["From Min"].default_value = -4.62
    normalized_x.inputs["From Max"].default_value = 4.62
    normalized_x.inputs["To Min"].default_value = 0.0
    normalized_x.inputs["To Max"].default_value = 1.0
    normalized_x.clamp = True

    color_ramp = nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Deep Red Orange Yellow Cream"
    configure_ramp(
        color_ramp.color_ramp,
        tuple((position, color) for position, color, _roughness, _name in COLOR_STOPS),
    )
    roughness_ramp = nodes.new("ShaderNodeValToRGB")
    roughness_ramp.name = "Roughness 0.45 to 0.15"
    configure_ramp(
        roughness_ramp.color_ramp,
        tuple(
            (position, (roughness, roughness, roughness, 1.0))
            for position, _color, roughness, _name in COLOR_STOPS
        ),
    )

    links.new(coordinates.outputs["Object"], separate.inputs["Vector"])
    links.new(separate.outputs["X"], normalized_x.inputs["Value"])
    links.new(normalized_x.outputs["Result"], color_ramp.inputs["Fac"])
    links.new(normalized_x.outputs["Result"], roughness_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], principled.inputs["Base Color"])
    links.new(roughness_ramp.outputs["Color"], principled.inputs["Roughness"])

    principled.inputs["Metallic"].default_value = 0.0
    if "Specular IOR Level" in principled.inputs:
        principled.inputs["Specular IOR Level"].default_value = 0.16
    if "Emission Strength" in principled.inputs:
        principled.inputs["Emission Strength"].default_value = 0.0

    material["gradient_basis"] = "Shared object coordinates, global left to right"
    material["color_sequence"] = "Deep red, orange, yellow, cream"
    material["roughness_sequence"] = "0.45, 0.35, 0.25, 0.15"
    return material


def main():
    yaw_experiment = load_previous_experiment()
    fitting_experiment = yaw_experiment.load_previous_experiment()
    curvature_experiment = fitting_experiment.load_previous_experiment()
    rim_size_experiment = curvature_experiment.load_previous_experiment()
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

    layout.make_logo_material = lambda: make_gradient_material(layout)
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
    curvature_experiment.load_previous_experiment = lambda: rim_size_experiment
    fitting_experiment.load_previous_experiment = lambda: curvature_experiment
    yaw_experiment.load_previous_experiment = lambda: fitting_experiment
    yaw_experiment.BLEND_PATH = BLEND_PATH
    yaw_experiment.RENDER_PATH = RENDER_PATH
    yaw_experiment.main()


if __name__ == "__main__":
    main()
