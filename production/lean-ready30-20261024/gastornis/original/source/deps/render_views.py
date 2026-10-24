# SPDX-License-Identifier: MIT
"""Clean exact-GLB import with canonical helper lighting and explicit view axes."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
import asset_common as common
p=argparse.ArgumentParser();p.add_argument('--root',default='.');p.add_argument('--clay',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);root=Path(a.root).resolve()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.ops.import_scene.gltf(filepath=str(root/'model.glb'))
collection=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(collection)
for obj in list(bpy.context.scene.objects):
    for old in list(obj.users_collection):old.objects.unlink(obj)
    collection.objects.link(obj)
# Keep the canonical lighting and camera fitting code. Replace only the helper's
# historical oblique hero direction with the brief's exact +X,-Y,+Z diagonal.
original_look=common._look_at
def orient(obj,target):
    if obj.type=='CAMERA':
        d=obj.location-Vector(target)
        if all(abs(v)>1e-6 for v in d):obj.location=Vector(target)+Vector((1,-1,1)).normalized()*d.length
    original_look(obj,target)
common._look_at=orient
if a.clay:
    bpy.context.view_layer.material_override=common.make_material('authoring-clay','#929292',.85)
    out=root/'private'/'clay';views=('front','side','hero');res=320;samples=12
else:
    out=root/'private'/'exact-view-render';views=('front','side','top','hero');res=640;samples=64
paths=common.render_previews(collection,out,views,resolution=res,samples=samples,transparent=True)
if not a.clay:
    (root/'views').mkdir(exist_ok=True)
    for v in views:shutil.copyfile(out/('preview-'+v+'.png'),root/'views'/('perspective.png' if v=='hero' else v+'.png'))
    shutil.copyfile(root/'views'/'perspective.png',root/'preview.png')
receipt={'stage':'early_clay' if a.clay else 'exact_export_final_views',
         'model_glb_sha256':hashlib.sha256((root/'model.glb').read_bytes()).hexdigest(),
         'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','threads':2,'samples':samples,
         'resolution':[res,res],'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,
         'camera_projection':'ORTHOGRAPHIC','perspective_label_means_oblique_diagnostic':True,
         'directions':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[1,-1,1]},
         'lighting':'Pinned canonical helper soft key and fill; neutral illumination',
         'renderer_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'canonical_helper_sha256':hashlib.sha256((Path(__file__).parent/'asset_common.py').read_bytes()).hexdigest(),
         'website_contract_compliance':'NOT_CLAIMED','source':'clean import of exact model.glb; no source-scene geometry',
         'files':{}}
for view in views:
    dst=out/('preview-'+view+'.png') if a.clay else root/'views'/('perspective.png' if view=='hero' else view+'.png')
    receipt['files'][dst.relative_to(root).as_posix()]={'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'bytes':dst.stat().st_size}
path=root/'private'/'clay-receipt.json' if a.clay else root/'qa'/'evidence'/'exact-glb-views.json'
path.write_text(json.dumps(receipt,indent=2)+'\n')
print('RENDER_COMPLETE',path.name)
