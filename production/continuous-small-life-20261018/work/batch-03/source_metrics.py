# SPDX-License-Identifier: MIT
"""Measure editable and evaluated source geometry after fresh reopen; never save."""
from pathlib import Path
import json,hashlib
import bpy
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
for s in ['cephalaspis','saccocoma','archaeocidaris','onoclea']:
 rev='r002' if s=='onoclea' else 'r001';f=ROOT/'assets/candidates/continuous-small-life-20261018/batch-03'/s/rev/s/(s+'.blend');h=hashlib.sha256(f.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(f),load_ui=False,use_scripts=False);c=bpy.data.collections['EXPORT'];root=bpy.data.objects[c['asset_root']];parts=[];deps=bpy.context.evaluated_depsgraph_get()
 for o in c.all_objects:
  if o.type!='MESH':continue
  ev=o.evaluated_get(deps);mesh=ev.to_mesh();mesh.calc_loop_triangles();parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'evaluated_vertices':len(mesh.vertices),'evaluated_triangles':len(mesh.loop_triangles),'modifiers':len(o.modifiers)});ev.to_mesh_clear()
 report={'asset_id':s,'revision':rev,'source_sha256':h,'source_reopened':True,'source_saved':False,'authored_vertices':sum(p['authored_vertices'] for p in parts),'evaluated_vertices':sum(p['evaluated_vertices'] for p in parts),'evaluated_triangles':sum(p['evaluated_triangles'] for p in parts),'parts':parts,'root_identity':all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-8 for i in range(4) for j in range(4)),'scene_cameras':len([o for o in bpy.data.objects if o.type=='CAMERA']),'scene_lights':len([o for o in bpy.data.objects if o.type=='LIGHT']),'preview_objects':[o.name for o in bpy.data.objects if o.name.startswith('_preview')],'meters_per_blender_unit':bpy.context.scene.unit_settings.scale_length}
 assert report['root_identity'] and report['scene_cameras']==report['scene_lights']==0 and not report['preview_objects'];assert hashlib.sha256(f.read_bytes()).hexdigest()==h
 out=ROOT/'qa/continuous-small-life-20261018/batch-03'/s/'verification/source-metrics.json';out.write_text(json.dumps(report,indent=2)+'\n')
