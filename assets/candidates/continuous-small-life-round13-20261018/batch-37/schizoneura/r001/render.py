# SPDX-License-Identifier: MIT
"""Render exact GLB in fresh Blender; no turntable frames."""
import bpy,sys,json,hashlib,argparse
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,link_object,render_previews
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('output',type=Path);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);c=setup_scene('exact-glb-render');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb))
for o in set(bpy.data.objects)-before:link_object(o,c,parent=False)
views=('hero','reversehero','front','side','rear','top','clay','silhouette');a.output.mkdir(parents=True,exist_ok=True)
files=render_previews(c,a.output,views,resolution=512,samples=24,transparent=False)
cover=a.output/'transparent';cover.mkdir();files+=render_previews(c,cover,('hero',),resolution=512,samples=24,transparent=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
(a.output/'view-manifest.json').write_text(json.dumps({'source_glb_sha256':sha(a.glb),'engine':'Blender '+bpy.app.version_string+' Cycles CPU','threads':2,'samples':24,'resolution':[512,512],'views':list(views),'turntable_frames':0,'view_transform':'Standard','files':[{'path':str(Path(f).relative_to(a.output)),'bytes':Path(f).stat().st_size,'sha256':sha(f)} for f in files],'render_helper_sha256':sha(ROOT/'scripts/asset_common.py')},indent=2)+'\n')
