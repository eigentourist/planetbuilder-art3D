"""Generate logo experiment 001-001: the baseline trajectory study."""

from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
BLEND_PATH = ROOT / "blendfiles" / "logo-001-001.blend"
RENDER_PATH = ROOT / "renders" / "logo-001-001.png"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    for datablocks in (bpy.data.curves, bpy.data.materials, bpy.data.cameras):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def make_cream_material():
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


def make_baseline(material):
    curve = bpy.data.curves.new("Rocket Trajectory Baseline", type="CURVE")
    curve.dimensions = "2D"
    curve.resolution_u = 48
    curve.render_resolution_u = 64
    curve.bevel_depth = 0.105
    curve.bevel_resolution = 8
    curve.resolution_u = 64
    curve.use_fill_caps = True

    spline = curve.splines.new("BEZIER")
    spline.bezier_points.add(3)

    # A steep launch at left eases continuously toward near-horizontal flight.
    points = (
        ((-5.2, -1.65, 0.0), (-5.55, -2.08, 0.0), (-4.72, -0.98, 0.0)),
        ((-3.35, 0.05, 0.0), (-4.05, -0.55, 0.0), (-2.63, 0.61, 0.0)),
        ((-0.75, 1.26, 0.0), (-1.72, 1.02, 0.0), (0.24, 1.49, 0.0)),
        ((5.2, 1.72, 0.0), (3.35, 1.65, 0.0), (5.65, 1.74, 0.0)),
    )
    for bezier_point, (co, handle_left, handle_right) in zip(spline.bezier_points, points):
        bezier_point.co = co
        bezier_point.handle_left_type = "FREE"
        bezier_point.handle_right_type = "FREE"
        bezier_point.handle_left = handle_left
        bezier_point.handle_right = handle_right

    baseline = bpy.data.objects.new("Baseline", curve)
    baseline.data.materials.append(material)
    bpy.context.collection.objects.link(baseline)


def make_camera():
    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (0.0, 0.0, 10.0)
    camera.rotation_euler = (0.0, 0.0, 0.0)
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 7.2
    bpy.context.scene.camera = camera


def configure_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 675
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.render.filepath = str(RENDER_PATH)
    scene.render.image_settings.color_depth = "8"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.world.color = (0.0, 0.0, 0.0)
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
    background.inputs["Strength"].default_value = 0.0


def main():
    clear_scene()
    material = make_cream_material()
    make_baseline(material)
    make_camera()
    configure_render()
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
