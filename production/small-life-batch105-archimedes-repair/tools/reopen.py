#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import bpy,sys,json,hashlib,datetime,os
from pathlib import Path
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
from check_source_export import compare_source_audit
D=R/'production/small-life-batch105-archimedes-repair/r002';A=Path(sys.argv[sys.argv.index('--')+1]);s=D/'artifacts/archimedes.blend';g=D/'artifacts/archimedes.glb';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sh=sha(s);gh=sha(g)
bpy.ops.wm.open_mainfile(filepath=str(s),load_ui=False,use_scripts=False);bpy.context.view_layer.update();cols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cols)==1;col=cols[0];audit=audit_source(col,14000);original=audit_glb(g,14000,6,30);r=compare_source_audit(audit,original,sh,gh);r.update(blender_pid=os.getpid(),blender_version=bpy.app.version_string,source_audit=audit,glb_audit=original,source_saved=False,full_collection_objects=[(o.name,o.type) for o in col.all_objects])
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col['asset_root']);out=A/'reopen-export.glb';assert not out.exists()
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
new=audit_glb(out,14000,6,30);r['full_collection_reexport']={'path':str(out),'sha256':sha(out),'semantic_sha256':new['semantic_sha256'],'original_semantic_sha256':original['semantic_sha256'],'semantic_match':new['semantic_sha256']==original['semantic_sha256'],'byte_identical':sha(out)==gh};assert r['status']=='pass' and r['full_collection_reexport']['semantic_match'];assert sha(s)==sh and sha(g)==gh;r['source_and_glb_unchanged']=True;(D/'qa/source-export.report.json').write_text(json.dumps(r,indent=2)+'\n');print('REOPEN_FULL_EXPORT_PASS',r['full_collection_reexport'])
