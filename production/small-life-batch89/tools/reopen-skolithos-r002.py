# SPDX-License-Identifier: MIT
# Fresh maker source reopen; no independent approval claimed.
import bpy,sys,json,hashlib,os,datetime,math,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
from check_source_export import compare_source_audit
args=sys.argv[sys.argv.index('--')+1:];aid,rev,out=args;out=Path(out);out.mkdir(parents=True,exist_ok=True)
b=ROOT/'production/small-life-batch89'/aid/rev;src=b/'artifacts'/f'{aid}.blend';glb=b/'artifacts'/f'{aid}.glb'
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(); start=datetime.datetime.now(datetime.timezone.utc).isoformat();before={str(p):h(p) for p in [src,glb]}
bpy.context.preferences.filepaths.use_scripts_auto_execute=False;bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
cols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cols)==1;col=cols[0]
audit=audit_source(col,max_triangles=14000);ga=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
comparison=compare_source_audit(audit,ga,h(src),h(glb));parts=[];components=[];dg=bpy.context.evaluated_depsgraph_get();private_points=[]
for o in col.all_objects:
 if o.type!='MESH':continue
 me=o.data;me.calc_loop_triangles();ev=o.evaluated_get(dg);em=ev.to_mesh();em.calc_loop_triangles()
 parts.append({'name':o.name,'vertices':len(me.vertices),'polygons':len(me.polygons),'triangles':len(me.loop_triangles),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles),'modifiers':len(o.modifiers),'editable':True});ev.to_mesh_clear()
 adj=[set() for _ in me.vertices]
 for e in me.edges:
  ea,eb=e.vertices;adj[ea].add(eb);adj[eb].add(ea)
 unseen=set(range(len(adj)));local=0
 while unseen:
  root=min(unseen);stack=[root];idx={root};unseen.remove(root)
  while stack:
   for q in adj[stack.pop()]:
    if q in unseen:unseen.remove(q);idx.add(q);stack.append(q)
  points=[o.matrix_world@me.vertices[i].co for i in sorted(idx)];polys=[p for p in me.polygons if p.vertices[0] in idx];lo=[min(v[k] for v in points) for k in range(3)];hi=[max(v[k] for v in points) for k in range(3)];mats=sorted({me.materials[p.material_index].name for p in polys});edges=collections.Counter()
  for p in polys:
   for edge in p.edge_keys:edges[tuple(sorted(edge))]+=1
  center=[(hi[k]+lo[k])/2 for k in range(3)]
  r={'index':len(components),'object':o.name,'local_index':local,'vertex_indices':sorted(idx),'vertices':len(points),'polygons':len(polys),'materials':mats,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[k]-lo[k] for k in range(3)]},'boundary_edges':sum(n==1 for n in edges.values()),'nonmanifold_edges':sum(n!=2 for n in edges.values())}
  if aid=='skolithos-pipe-field' and len(points)==24:
   rr=[math.hypot(v.x-center[0],v.y-center[1]) for v in points];r.update(radius_min_m=min(rr),radius_max_m=max(rr),center_xy_m=center[:2],bottom_z_m=lo[2],top_z_m=hi[2],top_bottom_identical_xy=sorted((round(v.x,8),round(v.y,8)) for v in points[:12])==sorted((round(v.x,8),round(v.y,8)) for v in points[12:]))
  components.append(r);private_points.append([tuple(v) for v in points]);local+=1
features={}
# Export the already opened source without rerunning or invoking maker generator.
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
options=json.loads((b/'artifacts/metadata.json').read_text())['export_options'];options['filepath']=str(out/'source-reexport.glb');bpy.ops.export_scene.gltf(**options);ra=audit_glb(out/'source-reexport.glb',max_triangles=14000,max_materials=6,max_primitives=30)
r={'schema_version':1,'asset_id':aid,'revision':rev,'pid':os.getpid(),'parent_pid':os.getppid(),'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender':bpy.app.version_string,'source_path':str(src),'source_sha256':h(src),'glb_sha256':h(glb),'autoexec':False,'source_saved':False,'source_unchanged':all(h(p)==v for p,v in before.items()),'source_export_comparison':comparison,'source_audit':audit,'static_glb':ga,'parts':parts,'components':components,'actual_features':features,'reexport_sha256':h(out/'source-reexport.glb'),'reexport_semantic_sha256':ra.get('semantic_sha256'),'original_semantic_sha256':ga.get('semantic_sha256'),'reexport_semantic_match':ra.get('semantic_sha256')==ga.get('semantic_sha256'),'reexport_byte_match':h(out/'source-reexport.glb')==h(glb),'reexport_audit':ra}
(out/'maker-source-reopen-reexport.json').write_text(json.dumps(r,indent=2)+'\n');print(aid,'components',len(components),'reexport_semantic_match',r['reexport_semantic_match'],'features',json.dumps({k:v for k,v in features.items() if k!='capsules'}))
