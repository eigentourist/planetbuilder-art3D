"""Bake high-contrast anisotropic nebula layers from the 4K color field."""

from importlib.util import module_from_spec, spec_from_file_location
from math import radians
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_SCRIPT = ROOT / "scripts" / "nebula-001-001.py"
COLOR_FIELD_PATH = ROOT / "textures" / "example-base-layer-4k.png"
BLEND_PATH = ROOT / "blendfiles" / "nebula-001-002.blend"
PREVIEW_PATH = ROOT / "renders" / "nebula-001-002.png"
BACKGROUND_PATH = ROOT / "textures" / "nebula-001-002-background-4k.png"
COMPOSITE_PATH = ROOT / "textures" / "nebula-001-002-composite-4k.png"
CLOUD_PATHS = tuple(
    ROOT / "textures" / f"nebula-001-002-cloud{index:02d}-2k.png"
    for index in range(1, 4)
)

LAYER_SETTINGS = (
    {
        "name": "Cloud 01 Broad Horizontal",
        "seed": 2.3,
        "noise_scale": 2.0,
        "noise_detail": 4.5,
        "noise_roughness": 0.66,
        "noise_distortion": 0.30,
        "mapping_scale": (0.52, 1.55, 1.0),
        "mapping_rotation": radians(-12.0),
        "color_offset": (-0.08, 0.05, 0.0),
        "value": 0.38,
        "composite_rotation": radians(-8.0),
        "composite_offset": (-2.8, 1.7),
        "composite_scale": (1.20, 1.15),
        "speed": 0.16,
    },
    {
        "name": "Cloud 02 Diagonal",
        "seed": 9.1,
        "noise_scale": 2.35,
        "noise_detail": 5.2,
        "noise_roughness": 0.70,
        "noise_distortion": 0.42,
        "mapping_scale": (1.65, 0.48, 1.0),
        "mapping_rotation": radians(31.0),
        "color_offset": (0.12, -0.06, 0.0),
        "value": 0.34,
        "composite_rotation": radians(11.0),
        "composite_offset": (2.8, -1.8),
        "composite_scale": (1.24, 1.17),
        "speed": -0.12,
    },
    {
        "name": "Cloud 03 Diffuse Filaments",
        "seed": 16.7,
        "noise_scale": 3.8,
        "noise_detail": 3.0,
        "noise_roughness": 0.56,
        "noise_distortion": 0.78,
        "mapping_scale": (0.34, 2.65, 1.0),
        "mapping_rotation": radians(-38.0),
        "color_offset": (0.03, 0.13, 0.0),
        "value": 0.46,
        "composite_rotation": radians(-4.0),
        "composite_offset": (0.7, 0.3),
        "composite_scale": (1.13, 1.13),
        "speed": 0.07,
    },
)


def load_previous_experiment():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("nebula_001_001", PREVIOUS_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_masked_color_material(experiment, settings):
    material = bpy.data.materials.new(f"{settings['name']} Masked Color Field")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (900, 0)
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (660, 0)
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (420, -130)
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (420, 100)

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-1000, 40)

    crop = nodes.new("ShaderNodeVectorMath")
    crop.operation = "MULTIPLY_ADD"
    crop.location = (-760, 240)
    crop.inputs[1].default_value = (0.5625, 1.0, 1.0)
    crop.inputs[2].default_value = (0.21875 + settings["color_offset"][0], settings["color_offset"][1], 0.0)
    color_field = nodes.new("ShaderNodeTexImage")
    color_field.name = "4K Color Field (sRGB)"
    color_field.image = bpy.data.images.load(str(COLOR_FIELD_PATH), check_existing=True)
    color_field.image.colorspace_settings.name = "sRGB"
    color_field.extension = "EXTEND"
    color_field.location = (-500, 260)
    grade = nodes.new("ShaderNodeHueSaturation")
    grade.location = (-190, 240)
    grade.inputs["Saturation"].default_value = 1.08
    grade.inputs["Value"].default_value = settings["value"]

    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-760, -180)
    mapping.inputs["Scale"].default_value = settings["mapping_scale"]
    mapping.inputs["Rotation"].default_value[2] = settings["mapping_rotation"]
    noise = nodes.new("ShaderNodeTexNoise")
    noise.noise_dimensions = "4D"
    noise.location = (-500, -180)
    noise.inputs["Scale"].default_value = settings["noise_scale"]
    noise.inputs["Detail"].default_value = settings["noise_detail"]
    noise.inputs["Roughness"].default_value = settings["noise_roughness"]
    noise.inputs["Distortion"].default_value = settings["noise_distortion"]
    noise.inputs["W"].default_value = settings["seed"]
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-180, -150)
    first = ramp.color_ramp.elements[0]
    first.position = 0.54
    first.color = (0.0, 0.0, 0.0, 0.0)
    low = ramp.color_ramp.elements.new(0.62)
    low.color = (0.08, 0.08, 0.08, 0.025)
    high = ramp.color_ramp.elements.new(0.71)
    high.color = (0.55, 0.55, 0.55, 0.48)
    last = ramp.color_ramp.elements[1]
    last.position = 0.82
    last.color = (1.0, 1.0, 1.0, 0.84)

    links.new(texcoord.outputs["Generated"], crop.inputs[0])
    links.new(crop.outputs["Vector"], color_field.inputs["Vector"])
    links.new(color_field.outputs["Color"], grade.inputs["Color"])
    links.new(grade.outputs["Color"], emission.inputs["Color"])
    links.new(texcoord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Alpha"], mix.inputs[0])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])

    material["color_field"] = str(COLOR_FIELD_PATH.relative_to(ROOT))
    material["mask_style"] = "High contrast anisotropic procedural noise"
    return material


def render_cloud_layers(experiment):
    experiment.clear_scene()
    experiment.make_camera(aspect=1.0)
    for index, (settings, path) in enumerate(zip(LAYER_SETTINGS, CLOUD_PATHS), start=1):
        plane = experiment.make_plane(f"Generator {settings['name']}", size=10.0)
        plane.data.materials.append(make_masked_color_material(experiment, settings))
        experiment.configure_render(*experiment.LAYER_SIZE, path, transparent=True)
        bpy.ops.render.render(write_still=True)
        bpy.data.objects.remove(plane, do_unlink=True)
        print(f"Baked masked color layer {index}: {path}")


def make_opaque_color_field_material():
    material = bpy.data.materials.new("4K Color Field Material")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    image = nodes.new("ShaderNodeTexImage")
    image.image = bpy.data.images.load(str(COLOR_FIELD_PATH), check_existing=True)
    image.image.colorspace_settings.name = "sRGB"
    links.new(image.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material


def render_color_field(experiment):
    experiment.clear_scene()
    experiment.make_camera(aspect=16.0 / 9.0)
    plane = experiment.make_plane("4K Reference Color Field", size=2.0)
    plane.scale.x = 8.8888889
    plane.scale.y = 5.0
    plane.data.materials.append(make_opaque_color_field_material())
    experiment.configure_render(*experiment.PRODUCTION_SIZE, BACKGROUND_PATH, transparent=False)
    bpy.ops.render.render(write_still=True)


def build_composite_scene(experiment):
    experiment.clear_scene()
    camera = experiment.make_camera(aspect=16.0 / 9.0)
    camera.data.ortho_scale = 10.0
    for index, (settings, path) in enumerate(zip(LAYER_SETTINGS, CLOUD_PATHS), start=1):
        plane = experiment.make_plane(settings["name"], size=20.5, z=float(index) * 0.1)
        material = experiment.make_image_material(f"{settings['name']} Baked RGBA", path)
        if index == 3:
            emission = next((node for node in material.node_tree.nodes if node.type == "EMISSION"), None)
            if emission is not None:
                emission.inputs["Strength"].default_value = 1.22
            material["composite_role"] = "Restrained bright filament accent"
        else:
            material["composite_role"] = "Normal alpha cloud compositing"
        plane.data.materials.append(material)
        plane.location.x, plane.location.y = settings["composite_offset"]
        plane.rotation_euler.z = settings["composite_rotation"]
        plane.scale.x, plane.scale.y = settings["composite_scale"]
        plane["godot_layer_order"] = index
        plane["suggested_rotation_speed_degrees_per_second"] = settings["speed"]
        plane["runtime_technique"] = "Pre-baked RGBA; animate transform/modulation only"


def render_composite_and_preview(experiment):
    build_composite_scene(experiment)
    experiment.configure_render(*experiment.PRODUCTION_SIZE, COMPOSITE_PATH, transparent=False)
    bpy.ops.render.render(write_still=True)
    experiment.configure_render(*experiment.PREVIEW_SIZE, PREVIEW_PATH, transparent=False)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


def main():
    experiment = load_previous_experiment()
    render_cloud_layers(experiment)
    render_color_field(experiment)
    render_composite_and_preview(experiment)
    print(f"Saved nebula scene: {BLEND_PATH}")
    print(f"Saved preview: {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
