"""Generate logo experiment 004-003: fit one converted text mesh to the guides."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import bpy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCRIPT = ROOT / "scripts" / "logo-004-001.py"
BLEND_PATH = ROOT / "blendfiles" / "logo-004-003.blend"
RENDER_PATH = ROOT / "renders" / "logo-004-003.png"
FONT_PATH = ROOT / "fonts" / "Days_One" / "DaysOne-Regular.ttf"

LOGO_TEXT = "PLANETBUILDER"
TEXT_LEFT = -4.62
TEXT_RIGHT = 4.62
VERTICAL_MARGIN_FRACTION = 0.15


def load_layout_helpers():
    sys.dont_write_bytecode = True
    spec = spec_from_file_location("logo_004_001", SOURCE_SCRIPT)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def interpolate_path_at_x(path, x_coordinate):
    for index in range(len(path) - 1):
        left = path[index]
        right = path[index + 1]
        if left.x <= x_coordinate <= right.x:
            width = right.x - left.x
            factor = 0.0 if abs(width) < 1e-8 else (x_coordinate - left.x) / width
            return left.lerp(right, factor)
    return path[0].copy() if x_coordinate < path[0].x else path[-1].copy()


def create_and_convert_text(layout):
    font = bpy.data.fonts.load(str(FONT_PATH), check_existing=True)
    material = layout.make_logo_material()

    curve = bpy.data.curves.new("PLANETBUILDER Days One Source", type="FONT")
    curve.body = LOGO_TEXT
    curve.font = font
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = 1.0
    curve.space_character = 1.0
    curve.extrude = 0.0505
    curve.bevel_depth = 0.002
    curve.bevel_resolution = 3
    curve.fill_mode = "BOTH"
    curve.resolution_u = 12

    text = bpy.data.objects.new("PLANETBUILDER Days One Text", curve)
    text.data.materials.append(material)
    bpy.context.collection.objects.link(text)
    bpy.context.view_layer.objects.active = text
    text.select_set(True)
    bpy.ops.object.convert(target="MESH")
    text.name = "PLANETBUILDER Days One Fitted Mesh"
    text.data.name = "PLANETBUILDER Days One Fitted Mesh"
    text["font_choice"] = "Days One"
    text["construction"] = "Single text object converted to mesh before guide fitting"
    return text


def fit_mesh_to_guides(text, upper_path, lower_path):
    x_values = [vertex.co.x for vertex in text.data.vertices]
    y_values = [vertex.co.y for vertex in text.data.vertices]
    source_min_x = min(x_values)
    source_max_x = max(x_values)
    source_min_y = min(y_values)
    source_max_y = max(y_values)
    source_width = source_max_x - source_min_x
    source_height = source_max_y - source_min_y

    for vertex in text.data.vertices:
        horizontal = (vertex.co.x - source_min_x) / source_width
        vertical = (vertex.co.y - source_min_y) / source_height
        target_x = TEXT_LEFT + horizontal * (TEXT_RIGHT - TEXT_LEFT)
        lower = interpolate_path_at_x(lower_path, target_x)
        upper = interpolate_path_at_x(upper_path, target_x)
        gap = upper.y - lower.y
        fitted_lower = lower.y + gap * VERTICAL_MARGIN_FRACTION
        fitted_upper = upper.y - gap * VERTICAL_MARGIN_FRACTION
        vertex.co.x = target_x
        vertex.co.y = fitted_lower + vertical * (fitted_upper - fitted_lower)

    text.data.validate(verbose=False)
    text.data.update()
    bpy.context.view_layer.objects.active = text
    text.select_set(True)
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    text.select_set(False)

    approximate_triangles = sum(max(0, len(polygon.vertices) - 2) for polygon in text.data.polygons)
    print(
        f"Fitted text mesh: {len(text.data.vertices)} vertices, "
        f"{len(text.data.polygons)} polygons, approximately {approximate_triangles} triangles"
    )


def main():
    layout = load_layout_helpers()
    base = layout.load_version_003_helpers()
    base.clear_scene()
    guide_material = base.make_cream_material()
    half_separation = base.INITIAL_CENTER_SEPARATION / 2.0
    upper_points = tuple(
        tuple(base.widen_upper_arc(coordinate) for coordinate in point)
        for point in base.BASE_POINTS
    )

    upper_y = half_separation
    lower_y = -half_separation - base.LOWER_DROP
    base.make_centerline("Upper", upper_points, upper_y, base.UPPER_ROTATION_DEGREES)
    base.make_centerline("Lower", base.BASE_POINTS, lower_y, 0.0)
    upper_path = base.sample_centerline(upper_points, upper_y, base.UPPER_ROTATION_DEGREES)
    lower_path = base.sample_centerline(base.BASE_POINTS, lower_y, 0.0)
    base.make_ribbon_mesh("Upper 3D Ribbon Guide", upper_path, guide_material)
    base.make_ribbon_mesh("Lower 3D Ribbon Guide", lower_path, guide_material)

    text = create_and_convert_text(layout)
    fit_mesh_to_guides(text, upper_path, lower_path)

    camera = base.make_camera()
    base.make_skylight(camera)
    base.configure_render()
    bpy.context.scene.render.filepath = str(RENDER_PATH)
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND_PATH))
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
