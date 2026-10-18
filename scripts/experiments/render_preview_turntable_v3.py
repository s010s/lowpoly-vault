# SPDX-License-Identifier: MIT
"""Read-only source preview experiment, Blender 4.3.2 / GPT-6 Astra xhigh.

blender -b -t 8 --python-exit-code 1 --python scripts/experiments/render_preview_turntable_v3.py -- --asset dinosaur-nest

Only writes experiments/preview-turntable-v3. Does not change source meshes,
transforms, materials, saved cameras, or files. Non-EXPORT source scene objects
are retained and hidden in the experimental copy, with an explicit inventory.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'experiments/preview-turntable-v3'
sys.path.insert(0, str(ROOT / 'scripts'))
from asset_common import make_material

ASSETS = {'dinosaur-nest': 'traces', 'lepidodendron': 'plants', 'natural-arch': 'geology'}
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--asset', required=True, choices=ASSETS)
p.add_argument('--frames', type=int, default=16)
p.add_argument('--resolution', type=int, default=256)
p.add_argument('--samples', type=int, default=24)
p.add_argument('--pilot', action='store_true', help='Render frame zero and the alpha/ground checks only')
p.add_argument('--clean-only', action='store_true', help='Add a full no-floor cutout sequence without overwriting shadow renders')
a = p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
source = ROOT / f'assets/prehistoric/{ASSETS[a.asset]}/{a.asset}/{a.asset}.blend'
glb = source.with_suffix('.glb')
out = OUT / a.asset
out.mkdir(parents=True, exist_ok=True)
(out / 'png-shadow').mkdir(exist_ok=True)
(out / 'png-clean').mkdir(exist_ok=True)
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
source_sha, glb_sha = sha(source), sha(glb)
bpy.ops.wm.open_mainfile(filepath=str(source))
scene = bpy.context.scene
collection = bpy.data.collections.get('EXPORT')
if collection is None:
    raise RuntimeError('Missing EXPORT collection; no source selection guessed.')
objects = set(collection.all_objects)
inventory = [{'name': o.name, 'type': o.type, 'in_export': o in objects,
              'original_hide_render': o.hide_render,
              'matrix_world': [list(row) for row in o.matrix_world]} for o in scene.objects]
for obj in scene.objects:
    if obj not in objects:
        obj.hide_render = True
# Preserve the authored visibility, transforms and materials of every asset object.
deps = bpy.context.evaluated_depsgraph_get()
points = []
for obj in objects:
    if obj.type != 'MESH' or obj.hide_render:
        continue
    evaluated = obj.evaluated_get(deps)
    mesh = evaluated.to_mesh()
    points.extend([evaluated.matrix_world @ v.co for v in mesh.vertices])
    evaluated.to_mesh_clear()
if not points:
    raise RuntimeError('Empty renderable EXPORT geometry')
low = Vector([min(v[i] for v in points) for i in range(3)])
high = Vector([max(v[i] for v in points) for i in range(3)])
center = (low+high)/2
span = max(high-low)
stage = bpy.data.collections.new('EXPERIMENT_PREVIEW_ONLY')
scene.collection.children.link(stage)

def aim(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat('-Z', 'Y').to_euler()

cam_data = bpy.data.cameras.new('Experiment orthographic camera')
camera = bpy.data.objects.new('Experiment orthographic camera', cam_data)
stage.objects.link(camera)
cam_data.type = 'ORTHO'
cam_data.lens = 50  # Documented nominal lens; orthographic projection ignores focal distance.
cam_data.clip_start = span/1000
cam_data.clip_end = span*40
scene.camera = camera
elevation = math.radians(35)
azimuths = [math.radians(-55 + i*360/a.frames) for i in range(a.frames)]

def camera_at(azimuth):
    direction = Vector((math.cos(azimuth)*math.cos(elevation),
                        math.sin(azimuth)*math.cos(elevation), math.sin(elevation)))
    camera.location = center+direction*span*5
    aim(camera, center)
    bpy.context.view_layer.update()
    return direction

# One scale per object, constant through the whole turntable. Actual projected
# vertices at every sampled view determine the fit, not a giant shared world box.
projected = []
maximum_radius = 0
for azimuth in azimuths:
    camera_at(azimuth)
    rotation = camera.rotation_euler.to_matrix().transposed()
    local = [rotation @ (v-center) for v in points]
    bounds = [[min(v[i] for v in local), max(v[i] for v in local)] for i in (0, 1)]
    projected.append(bounds)
    maximum_radius = max(maximum_radius, *(abs(x) for axis in bounds for x in axis))
occupancy_target = .82
cam_data.ortho_scale = 2*maximum_radius/occupancy_target

world = bpy.data.worlds.new('Experiment neutral studio world')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs['Color'].default_value = (.75, .75, .75, 1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value = .30
scene.world = world
lights = []
for name, watts, size in [('key', 70, 1.8), ('fill', 20, 2.2), ('rim', 25, 1.6)]:
    data = bpy.data.lights.new('Experiment '+name, 'AREA')
    data.energy = watts*span*span
    data.shape = 'DISK'
    data.size = size*span
    data.color = (1, 1, 1)
    light = bpy.data.objects.new('Experiment '+name, data)
    stage.objects.link(light)
    lights.append(light)

def set_view(i):
    direction = camera_at(azimuths[i])
    toward = Vector((direction.x, direction.y, 0)).normalized()
    right = Vector((-toward.y, toward.x, 0))
    # Stable camera-relative soft key/fill, rotated around stationary source.
    for light, (x, y, z) in zip(lights, [(-1.5, 1.8, 3.0), (2, 1, 1.8), (.2, -2, 2.8)]):
        light.location = center + span*(right*x+toward*y+Vector((0,0,z)))
        aim(light, center)

floor_mesh = bpy.data.meshes.new('Experiment floor mesh')
extent = span*20
floor_mesh.from_pydata([(-extent,-extent,low.z-span*.001),
                       (extent,-extent,low.z-span*.001),
                       (extent,extent,low.z-span*.001),
                       (-extent,extent,low.z-span*.001)], [], [(0,1,2,3)])
floor = bpy.data.objects.new('Experiment shadow catcher only', floor_mesh)
stage.objects.link(floor)
floor_mesh.materials.append(make_material('Experiment neutral floor', '#F2EFE7', 1))
floor.is_shadow_catcher = True
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = a.samples
scene.cycles.use_denoising = False
scene.cycles.use_adaptive_sampling = False
scene.cycles.use_persistent_data = True
scene.cycles.max_bounces = 4
scene.cycles.diffuse_bounces = 2
scene.cycles.glossy_bounces = 2
scene.cycles.transparent_max_bounces = 8
scene.cycles.seed = 42
scene.render.resolution_x = a.resolution
scene.render.resolution_y = a.resolution
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.color_depth = '8'
scene.render.image_settings.compression = 30
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'None'
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1
scene.use_nodes = False
timings = []

def render(path, label):
    scene.render.filepath = str(path)
    start = time.perf_counter()
    bpy.ops.render.render(write_still=True)
    timings.append({'label': label, 'seconds': time.perf_counter()-start})
    print('PREVIEW_DONE '+a.asset+' '+label+' '+str(path), flush=True)

set_view(0)
if not a.clean_only:
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'preview-scene.blend'), copy=True)
floor.hide_render = a.clean_only
for i in range(1 if a.pilot else a.frames):
    set_view(i)
    kind = 'clean' if a.clean_only else 'shadow'
    render(out/('png-'+kind)/f'{i:02d}.png', f'{kind}-{i:02d}')
# Isolate a clean original-object image for alpha-edge and shadow comparisons.
set_view(0)
if not a.clean_only:
    floor.hide_render = True
    render(out/'hero-clean.png', 'clean-hero')
    floor.hide_render = False
    floor.is_shadow_catcher = False
# Actual opaque-floor checks expose the difference between recoloring a baked
# shadow render and physically changing the surface / light bounce.
for name, color in ([] if a.clean_only else [('light', '#F2EFE7'), ('dark', '#24292A')]):
    floor.data.materials.clear()
    floor.data.materials.append(make_material('Experiment '+name+' check floor', color, 1))
    render(out/f'hero-physical-{name}.png', 'physical-'+name)

if sha(source) != source_sha or sha(glb) != glb_sha:
    raise RuntimeError('Unexpected source change')
report = {
    'asset': a.asset, 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'operator_model': 'GPT-6 Astra xhigh', 'environment': 'dot cloud computer',
    'source_blend': str(source.relative_to(ROOT)), 'source_glb': str(glb.relative_to(ROOT)),
    'source_blend_sha256': source_sha, 'source_glb_sha256': glb_sha,
    'source_files_unchanged': True, 'source_objects': inventory,
    'geometry_material_transform_changes': 'None. Non-EXPORT objects retained but hidden only in experiment.',
    'source_bounds_m': {'min': list(low), 'max': list(high), 'size': list(high-low)},
    'render': {'blender': bpy.app.version_string, 'engine': 'Cycles CPU',
               'resolution': [a.resolution]*2, 'samples': a.samples,
               'denoising': False, 'adaptive_sampling': False, 'seed': 42,
               'view_transform': 'Standard', 'look': 'None', 'exposure': 0,
               'film_transparent': True, 'format': 'RGBA8 PNG',
               'frame_count': 1 if a.pilot else a.frames, 'timings': timings},
    'camera': {'projection': 'orthographic', 'elevation_degrees': 35,
               'azimuth_degrees': [-55+i*360/a.frames for i in range(a.frames)],
               'target': list(center), 'ortho_scale_m': cam_data.ortho_scale,
               'fit': 'Per-asset maximum projected vertex radius over all 16 views; constant zoom per asset.',
               'maximum_centered_extent_fraction': occupancy_target,
               'projected_bounds_m': projected,
               'per_frame_width_height_occupancy': [[(v[1]-v[0])/cam_data.ortho_scale for v in b] for b in projected]},
    'lighting': {'rig': 'Neutral, camera-relative key/fill/rim; light positions, size and power normalized by source bounds, never source transforms.',
                 'world_strength': .30, 'shadow_catcher_surface_srgb': '#F2EFE7',
                 'power_watts_per_span_squared': [70,20,25]},
    'variants': {'png-shadow': '16 transparent object+Cycles shadow-catcher renders',
                 'png-clean': '16 clean original-object renders, no floor, generated with --clean-only',
                 'hero-clean.png': 'Frame zero, no floor, physically rerendered',
                 'hero-physical-light.png': 'Frame zero, actual lit #F2EFE7 floor',
                 'hero-physical-dark.png': 'Frame zero, actual lit #24292A floor'},
    'license': {'images_and_original_models': 'CC-BY-4.0', 'author': 'Leon Made This / s010s',
                'scripts': 'MIT', 'third_party_images': []},
    'limits': ['256 px decision prototype, not a full-resolution production render.',
               '24 non-denoised samples can leave grain in dark material and shadow edges.',
               'Shadow-catcher RGBA is tied to this lighting/floor and is not physically correct for every background.',
               'Source model design/scientific acceptance remains separate from preview presentation.']}
(out/('clean-render-report.json' if a.clean_only else 'render-report.json')).write_text(json.dumps(report, indent=2)+'\n')
print('PREVIEW_ASSET_COMPLETE '+a.asset, flush=True)
