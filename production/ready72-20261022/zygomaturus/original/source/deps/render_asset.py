# SPDX-License-Identifier: MIT
"""Exact-GLB four-view driver. Clay branch is private authoring evidence only."""
from pathlib import Path
import sys, json, hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from asset_common import setup_scene,link_object,render_previews,make_material
import render_candidate_views as canonical
if '--clay-quick' in sys.argv:
    argv=sys.argv[sys.argv.index('--clay-quick')+1:]
    src=Path(argv[0]); out=Path(argv[1]); col=setup_scene('clay-check')
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=str(src))
    imported=[o for o in bpy.data.objects if o not in before]
    clay=make_material('clay-neutral','#929292')
    for obj in imported:
        link_object(obj,col,parent=False)
        if obj.type=='MESH':
            obj.data.materials.clear(); obj.data.materials.append(clay)
            for poly in obj.data.polygons: poly.material_index=0
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    files=render_previews(col,out,views=('front','side','top','hero'),resolution=480,samples=12)
    report={'kind':'low-cost-gray-self-check','source_glb_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
       'files':{Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in files},
       'resolution':480,'samples':12,'engine':'Blender Cycles CPU','threads':2,
       'material_override':'neutral gray on clean import; original GLB unchanged','visual_review':'pending'}
    (out/'clay-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
else:
    canonical.DIRECTIONS['perspective']=(45,35.264389682754654)
    canonical.main()
