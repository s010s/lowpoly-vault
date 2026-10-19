# SPDX-License-Identifier: MIT
"""Targeted true-gray top image from the exact GLB; outside primary fixed8."""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,link_object,render_previews,make_material
args=sys.argv[sys.argv.index('--')+1:];glb=Path(args[0]);out=Path(args[1]);c=setup_scene('exact-glb-gray-top');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(glb))
for o in set(bpy.data.objects)-before:link_object(o,c,parent=False)
out.mkdir(parents=True,exist_ok=True);gray=make_material('_diagnostic-true-gray','#929292',roughness=.85);bpy.context.view_layer.material_override=gray
files=render_previews(c,out,('top',),resolution=512,samples=24,transparent=False);bpy.context.view_layer.material_override=None
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
(out/'manifest.json').write_text(json.dumps(dict(kind='targeted-diagnostic-outside-primary-fixed8',source_glb_sha256=sha(glb),view='top',material_override='original preview gray929292',engine='Blender4.3.2 CyclesCPU',samples=24,threads=2,images=[dict(path=Path(p).name,sha256=sha(p)) for p in files]),indent=2)+'\n')
