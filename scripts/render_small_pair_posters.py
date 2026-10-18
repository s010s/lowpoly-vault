# SPDX-License-Identifier: MIT
"""Render the exact shipped GLB as a transparent poster with shared lighting helpers."""
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
import asset_common as C
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output-dir',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
c=C.setup_scene('poster-import'); root=bpy.data.objects[c['asset_root']]; before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
obs=[o for o in bpy.data.objects if o not in before]
for o in obs:C.link_object(o,c,parent=False)
for o in obs:
 if o.parent not in obs:
  w=o.matrix_world.copy();o.parent=root;o.matrix_world=w
C.render_previews(c,a.output_dir,views=('hero',),resolution=768,samples=24,transparent=True)
(a.output_dir/'poster-evidence.json').write_text(json.dumps({'source_glb_sha256':hashlib.sha256(a.glb.read_bytes()).hexdigest(),'poster_sha256':hashlib.sha256((a.output_dir/'preview-hero.png').read_bytes()).hexdigest(),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','view_transform':'Standard','look':'None','resolution':768,'samples':24,'transparent':True,'source_is_exact_export':True,'helper':'scripts/asset_common.py'},indent=2)+'\n')
