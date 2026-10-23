# SPDX-License-Identifier: MIT
"""Exact delivered GLB view adapter around pinned asset_common lighting. No source-blend render."""
import argparse, hashlib, json, shutil, sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene, link_object, make_material, render_previews
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',type=Path,required=True)
p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=800);p.add_argument('--samples',type=int,default=48)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); a.output_dir.mkdir(parents=True,exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sha=h(a.glb); c=setup_scene('fruitafossor',665001); bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
for ob in list(bpy.context.scene.objects):
    if ob.type=='MESH': link_object(ob,c)
if a.clay:
    mat=make_material('gray-anatomy-check','#98948E')
    for ob in c.all_objects:
        if ob.type=='MESH':
            ob.data.materials.clear();ob.data.materials.append(mat)
            for face in ob.data.polygons: face.material_index=0
views=('front','side','top','hero') if not a.clay else ('front','side','hero')
paths=render_previews(c,a.output_dir,views=views,resolution=a.resolution,samples=a.samples)
files={}
for view in views:
    origin=a.output_dir/f'preview-{view}.png'; target=a.output_dir/('perspective.png' if view=='hero' else view+'.png')
    origin.rename(target); files[target.name]=h(target)
assert sha==h(a.glb)
(a.output_dir/'render-evidence.json').write_text(json.dumps({'status':'rendered_not_independently_reviewed','glb_sha256':sha,
    'origin':'Clean import of exact GLB, never source blend','clay_override':a.clay,'blender':bpy.app.version_string,
    'engine':'Cycles CPU','threads':2,'resolution':a.resolution,'samples':a.samples,
    'camera_directions':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},
    'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'files':files},indent=2)+'\n')
