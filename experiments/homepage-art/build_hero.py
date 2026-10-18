# SPDX-License-Identifier: MIT
"""Original editorial asset display. Cloud Blender 4.3.2; GPT-6 Astra, xhigh.

Reuses the repository's immutable production meshes without modifying sources.
This is an art-directed object display, not an ecological reconstruction.

blender -b --threads 8 --python-exit-code 1 --python experiments/homepage-art/build_hero.py -- --preview
blender -b --threads 8 --python-exit-code 1 --python experiments/homepage-art/build_hero.py
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
from datetime import datetime, timezone
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'site/public/home'
SOURCE = ROOT / 'experiments/homepage-art'
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
p = argparse.ArgumentParser(); p.add_argument('--preview', action='store_true')
a = p.parse_args(args)
OUT.mkdir(parents=True, exist_ok=True)
SOURCE.mkdir(parents=True, exist_ok=True)
sys.path.insert(0,str(ROOT / 'scripts'))
from asset_common import make_material, srgb_to_linear
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene['title'] = 'Forms for worlds'
scene['description'] = 'Editorial tabletop display of four original Lowpoly Vault models; not a coexisting prehistoric ecosystem.'
scene['license'] = 'CC-BY-4.0'
scene['author'] = 'Leon Made This / s010s'
scene['art_direction'] = 'GPT-6 Astra, xhigh; Blender 4.3.2; cloud only'

stage = bpy.data.collections.new('EDITORIAL_STAGING_ONLY')
scene.collection.children.link(stage)
references = []

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def asset(category, slug, position, scale=1, rotation=0):
    path = ROOT / f'assets/prehistoric/{category}/{slug}/{slug}.blend'
    digest = sha(path)
    with bpy.data.libraries.load(str(path), link=False) as (src, dst):
        dst.collections = ['EXPORT']
    collection = dst.collections[0]
    collection.name = 'ASSET_' + slug
    scene.collection.children.link(collection)
    objects = set(collection.all_objects)
    holder = bpy.data.objects.new('DISPLAY_TRANSFORM_' + slug, None)
    stage.objects.link(holder)
    for obj in objects:
        obj.hide_render = False
        obj.hide_set(False)
        if obj.parent not in objects:
            matrix = obj.matrix_world.copy()
            obj.parent = holder
            obj.matrix_world = matrix
    holder.location = position
    holder.scale = (scale,) * 3
    holder.rotation_euler.z = math.radians(rotation)
    references.append({'id':slug, 'source_blend':str(path.relative_to(ROOT)),
                       'source_sha256':digest,
                       'source_url':f'https://github.com/s010s/lowpoly-vault/tree/main/assets/prehistoric/{category}/{slug}',
                       'display_transform':{'translation':position,'uniform_scale':scale,'rotation_z_degrees':rotation},
                       'geometry_changes':'None; display transforms only', 'license':'CC-BY-4.0', 'author':'Leon Made This / s010s'})
    return holder

def move_to_stage(obj):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    stage.objects.link(obj)

def slab(name, location, dimensions, color, angle=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    obj=bpy.context.object; obj.name=name
    obj.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    obj.rotation_euler.z=math.radians(angle)
    obj.data.materials.append(make_material(name+' material', color, 0.8))
    bevel=obj.modifiers.new('Delicate physical edge', 'BEVEL'); bevel.width=.055; bevel.segments=2
    bevel.affect='EDGES'
    obj.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    move_to_stage(obj)
    return obj

def cylinder(name, xy, radius, height, color, vertices=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=height,location=(*xy,height/2))
    obj=bpy.context.object;obj.name=name
    obj.data.materials.append(make_material(name+' material',color,.82))
    bevel=obj.modifiers.new('Soft machined edge','BEVEL');bevel.width=.028;bevel.segments=2
    obj.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    move_to_stage(obj)
    return obj

# Each riser is editorial staging, never claimed as an additional catalog asset.
slab('Ivory arch display slab', (3.1,.0,.20), (6.1,2.75,.4), '#DDD3BF', 14)
cylinder('Ochre conifer display cylinder',(6.1,1.5),1.15,.82,'#CB9273')
cylinder('Pale cycad display cylinder',(.55,-1.8),1.10,.25,'#E0D6C5')
asset('geology','natural-arch',(3.1,.0,.4),1.02,14)
asset('plants','conifer-tree',(6.1,1.5,.82),.69,-24)
asset('plants','cycad',(.55,-1.8,.25),.91,35)
asset('plants','fern-cluster',(5.5,-2.0,0),1.18,-20)

# Large studio floor and unified physical lighting.
bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,-.015))
floor=bpy.context.object;floor.name='Warm paper infinity floor';move_to_stage(floor)
floor.data.materials.append(make_material('Warm paper','#EEEAE2',1.0))
floor.is_shadow_catcher=True
world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(.78,.82,.9,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
scene.world=world

def aim(obj, target): obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
def light(name, location, power, size, color):
    data=bpy.data.lights.new(name,'AREA');data.energy=power;data.shape='DISK';data.size=size;data.color=color
    obj=bpy.data.objects.new(name,data);stage.objects.link(obj);obj.location=location;aim(obj,(3,0,1.5));return obj
light('Broad upper left softbox',(-4,-6,11),1350,7,(1.0,.93,.84))
light('Cool frontal fill',(9,-4,8),420,6,(.86,.92,1.0))
light('Soft top rim',(5,6,10),900,5,(1.0,.97,.90))

cam_data=bpy.data.cameras.new('Editorial camera')
cam=bpy.data.objects.new('Editorial camera',cam_data);stage.objects.link(cam)
cam.location=(0,-20,12.8);aim(cam,(0,0,2.3))
cam_data.type='ORTHO';cam_data.ortho_scale=16.8;cam_data.lens=50;scene.camera=cam
cam_data.clip_start=.1;cam_data.clip_end=300
scene.render.engine='CYCLES';scene.cycles.device='CPU'
scene.cycles.samples=12 if a.preview else 64
scene.cycles.use_denoising=False
scene.cycles.use_adaptive_sampling=True
scene.cycles.adaptive_threshold=.05 if a.preview else .015
scene.cycles.max_bounces=6
scene.cycles.diffuse_bounces=3
scene.cycles.glossy_bounces=3
scene.render.resolution_x=1000 if a.preview else 1600
scene.render.resolution_y=625 if a.preview else 1000
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
scene.render.image_settings.color_depth='8'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.view_settings.exposure=0;scene.view_settings.gamma=1
# Composite physically rendered shadows onto exact paper color for a seamless UI.
scene.render.film_transparent=True
scene.use_nodes=True
nodes=scene.node_tree.nodes;nodes.clear()
rl=nodes.new('CompositorNodeRLayers')
over=nodes.new('CompositorNodeAlphaOver');over.inputs[0].default_value=1
bg_hex='#F2EFE7'
over.inputs[1].default_value=tuple(srgb_to_linear(int(bg_hex[i:i+2],16)/255) for i in (1,3,5))+(1,)
scene.node_tree.links.new(rl.outputs['Image'],over.inputs[2])
composite=nodes.new('CompositorNodeComposite')
scene.node_tree.links.new(over.outputs[0],composite.inputs[0])
scene.render.filepath=str(SOURCE/'preview.png' if a.preview else OUT/'editorial-hero.png')
# Keep the editable final project configured for the full-resolution deliverable.
if not a.preview: bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/'hero.blend'))
bpy.ops.render.render(write_still=True)
for ref in references:
    if sha(ROOT/ref['source_blend']) != ref['source_sha256']:
        raise RuntimeError('Unexpected change to source: '+ref['source_blend'])
report={'title':'Forms for worlds', 'kind':'original editorial homepage composition',
        'scientific_scope':'A curated display of independent stylized models, not a taxonomic or coexisting-ecosystem reconstruction.',
        'author':'Leon Made This / s010s','license':'CC-BY-4.0',
        'license_url':'https://creativecommons.org/licenses/by/4.0/',
        'software_license':'MIT', 'third_party_assets':[], 'sources_unchanged':True,
        'models':references, 'staging':'Original studio risers and floor, used only in this editorial render.',
        'render':{'engine':'Blender 4.3.2 Cycles CPU','resolution':[scene.render.resolution_x,scene.render.resolution_y],
                  'samples':scene.cycles.samples,'denoising':False,'view_transform':'Standard','background_srgb':'#F2EFE7',
                  'timestamp_utc':datetime.now(timezone.utc).isoformat(), 'png_sha256':sha(Path(scene.render.filepath))},
        'composition':{'headline_safe_area':'Left 36% of the full image',
                       'preferred_object_position':'72% 50%',
                       'motion':'Animate page frame or labels, never imply a rotating 3D render from this flat image.'}}
report_path=SOURCE/'preview.report.json' if a.preview else OUT/'editorial-hero.json'
report_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('HOMEPAGE_ART_COMPLETE '+str(scene.render.filepath),flush=True)
