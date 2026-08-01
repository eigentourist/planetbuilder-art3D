"""Generate logo experiment 002-005: thin contours for negative-space study."""

from math import radians
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "blendfiles" / "logo-002-005.blend"
RENDER_PATH = ROOT / "renders" / "logo-002-005.png"

STROKE_RADIUS = 0.0525
REFERENCE_STROKE_THICKNESS = 0.21
INITIAL_EDGE_GAP = REFERENCE_STROKE_THICKNESS * 2.0
INITIAL_CENTER_SEPARATION = REFERENCE_STROKE_THICKNESS + INITIAL_EDGE_GAP
LOWER_DROP = REFERENCE_STROKE_THICKNESS * 2.0
ARC_WIDTH_FACTOR = 1.2
RIGHT_ANCHOR_Y = 1.74
UPPER_ROTATION_DEGREES = -5.0


BASE_POINTS = (
    ((-5.2, -1.65, 0.0), (-5.55, -2.08, 0.0), (-4.72, -0.98, 0.0)),
    ((-3.35, 0.05, 0.0), (-4.05, -0.55, 0.0), (-2.63, 0.61, 0.0)),
    ((-0.75, 1.26, 0.0), (-1.72, 1.02, 0.0), (0.02, 1.45, 0.0)),
    ((1.05, 1.58, 0.0), (0.35, 1.49, 0.0), (2.00, 1.69, 0.0)),
    ((4.16, 1.74, 0.0), (3.15, 1.74, 0.0), (4.52, 1.74, 0.0)),
    ((5.2, 1.74, 0.0), (4.80, 1.74, 0.0), (5.55, 1.74, 0.0)),
)


def make_material():
    material = bpy.data.materials.new("Orange Cream Soda Cream")
    material.diffuse_color = (1.0, 0.79, 0.48, 1.0)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (1.0, 0.79, 0.48, 1.0)
    emission.inputs["Strength"].default_value = 1.0
    material.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return material


def widen_upper_arc(coordinate):
    x, y, z = coordinate
    return (x, RIGHT_ANCHOR_Y + (y - RIGHT_ANCHOR_Y) / ARC_WIDTH_FACTOR, z)


def make_baseline(name, points, vertical_offset, material):
    curve = bpy.data.curves.new(name, type="CURVE")
    curve.dimensions = "2D"
    curve.resolution_u = 64
    curve.render_resolution_u = 64
    curve.bevel_depth = STROKE_RADIUS
    curve.bevel_resolution = 8
    curve.use_fill_caps = True
    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, (co, left, right) in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = "FREE"
        point.handle_right_type = "FREE"
        point.handle_left = left
        point.handle_right = right

    baseline = bpy.data.objects.new(name, curve)
    baseline.location.y = vertical_offset
    baseline.data.materials.append(material)
    bpy.context.collection.objects.link(baseline)
    return baseline


def main():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    material = make_material()

    half_separation = INITIAL_CENTER_SEPARATION / 2.0
    upper_points = tuple(
        tuple(widen_upper_arc(coordinate) for coordinate in point)
        for point in BASE_POINTS
    )
    upper = make_baseline("Upper Logo Edge", upper_points, half_separation, material)
    upper.rotation_euler.z = radians(UPPER_ROTATION_DEGREES)
    make_baseline(
        "Lower Logo Baseline",
        BASE_POINTS,
        -half_separation - LOWER_DROP,
        material,
    )

    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0.0, 0.0, 10.0)
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 11.5

    scene = bpy.context.scene
    scene.camera = camera
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 675
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = False
    scene.render.filepath = str(RENDER_PATH)
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    background.inputs["Strength"].default_value = 0.0

    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
