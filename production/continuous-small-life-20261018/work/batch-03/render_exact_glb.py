# SPDX-License-Identifier: MIT
"""Import exact shipped GLB into factory state; render eight true fixed QA views."""
import sys,json,hashlib
from pathlib import Path
import bpy
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,link_object,render_previews,audit_source
slug=sys.argv[-1];glb=ROOT/'assets/candidates/continuous-small-life-20261018/batch-03'/slug/('r002' if slug=='onoclea' else 'r001')/slug/(slug+'.glb');out=ROOT/'qa/continuous-small-life-20261018/batch-03'/slug/'exact-glb';out.mkdir(parents=True,exist_ok=False)
c=setup_scene(slug);before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(glb));objects=[o for o in bpy.data.objects if o not in before];root=bpy.data.objects[c['asset_root']]
for o in objects:
 link_object(o,c,parent=False)
for o in objects:
 if o.parent not in objects:
  matrix=o.matrix_world.copy();o.parent=root;o.matrix_world=matrix
bpy.context.view_layer.update()
files=render_previews(c,out,('hero','reversehero','front','side','rear','top','clay','silhouette'),resolution=512,samples=8,transparent=True)
report={'glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'imported_from_glb':True,'engine':'Cycles CPU','resolution':512,'samples':8,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'transparent':True,'frames':[{'path':str(Path(f).relative_to(ROOT)),'sha256':hashlib.sha256(Path(f).read_bytes()).hexdigest(),'bytes':Path(f).stat().st_size} for f in files],'status':'rendered_pending_independent_review'}
(out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
