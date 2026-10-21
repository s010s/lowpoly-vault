# SPDX-License-Identifier: MIT
"""Read-only independent saved-source reopen, topology and exact exporter check."""
import bpy,sys,json,hashlib,datetime,os
from pathlib import Path
from mathutils.bvhtree import BVHTree
root,src,out=map(Path,sys.argv[sys.argv.index('--')+1:]); aid=src.parent.parent.name;sys.path.insert(0,str(root/'scripts'));sys.dont_write_bytecode=True
from asset_common import audit_source
from qa_glb import audit_glb
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
start=datetime.datetime.now(datetime.timezone.utc).isoformat();source_hash=sha(src/(aid+'.blend'));glb_hash=sha(src/(aid+'.glb'))
assert not out.exists(),out
out.mkdir()
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(src/(aid+'.blend')),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
col=bpy.data.collections['EXPORT'];sa=audit_source(col,max_triangles=14000);parts=[]
for o in col.all_objects:
 if o.type!='MESH':continue
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();vs=[o.matrix_world@v.co for v in me.vertices];ts=[tuple(t.vertices) for t in me.loop_triangles];edges={};dupes={};volume=0.0
 for tri in ts:
  for k in range(3):
   e=tuple(sorted((tri[k],tri[(k+1)%3])));edges[e]=edges.get(e,0)+1
  key=tuple(sorted(tri));dupes[key]=dupes.get(key,0)+1
  a,b,c=[vs[k] for k in tri];volume+=a.dot(b.cross(c))/6
 tree=BVHTree.FromPolygons(vs,ts,all_triangles=True,epsilon=0.0)
 pairs=[(a,b) for a,b in tree.overlap(tree) if a<b and not set(ts[a])&set(ts[b])]
 parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'evaluated_vertices':len(me.vertices),'authored_polygons':len(o.data.polygons),'evaluated_polygons':len(me.polygons),'triangles':len(ts),'boundary_or_nonmanifold_triangle_edges':sum(n!=2 for n in edges.values()),'duplicate_triangles':sum(n-1 for n in dupes.values()),'nonadjacent_intersection_pairs':len(pairs),'intersection_examples':pairs[:20],'signed_volume_m3':volume,'bounds_blender_m':{'min':[min(v[k] for v in vs) for k in range(3)],'max':[max(v[k] for v in vs) for k in range(3)]},'euler_characteristic':len(vs)-len(edges)+len(ts),'object_transform':list(map(list,o.matrix_world))});ev.to_mesh_clear()
opts=json.load(open(src/'metadata.json'))['export_options'];opts['filepath']=str(out/'saved-source-reexport.glb')
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
bpy.ops.export_scene.gltf(**opts)
orig=audit_glb(src/(aid+'.glb'),14000,6,30);fresh=audit_glb(out/'saved-source-reexport.glb',14000,6,30)
errors=list(sa['errors'])+orig['errors']+fresh['errors']
if orig['semantic_sha256']!=fresh['semantic_sha256']:errors.append('Saved-source export semantic mismatch')
if any(p['boundary_or_nonmanifold_triangle_edges'] or p['duplicate_triangles'] for p in parts):errors.append('Topology issue requires review')
# Nonadjacent intersections are reported diagnostically, not a universal failure.
report={'schema_version':1,'kind':'independent_saved_source_reopen_reexport','started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_pid':os.getpid(),'blender_version':bpy.app.version_string,'thread_count':bpy.context.scene.render.threads,'source_sha256':source_hash,'glb_sha256':glb_hash,'source_saved':False,'source_unchanged':sha(src/(aid+'.blend'))==source_hash,'glb_unchanged':sha(src/(aid+'.glb'))==glb_hash,'source_audit':sa,'parts':parts,'original_glb_audit':orig,'reexport_glb_audit':fresh,'semantic_match':orig['semantic_sha256']==fresh['semantic_sha256'],'byte_identical':glb_hash==fresh['sha256'],'errors':errors,'status':'pass' if not errors else 'fail','intentional_contact_policy':'Terrain/substrate embedded volumes are allowed; coplanar exposed faces require visual assessment, not blanket zero-intersection rule.', 'limitations':'BVH excludes shared-vertex adjacent triangles; not exhaustive surface artifact proof. Source reopen/export and CPU topology are not GPU or scene verification.'}
(out/'source-reexport.report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'semantic_match':report['semantic_match'],'byte_identical':report['byte_identical'],'parts':parts}));assert not errors,errors
