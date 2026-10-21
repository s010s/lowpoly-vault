import bpy,sys,json,pathlib,hashlib,collections,os,datetime
from mathutils import Vector
R=pathlib.Path('/workspace/shared/lowpoly-batch107-20261021');sys.path.insert(0,str(R/'scripts'));from qa_glb import audit_glb
src=pathlib.Path(sys.argv[sys.argv.index('--')+1]);out=pathlib.Path(sys.argv[sys.argv.index('--')+2]);out.mkdir(exist_ok=True);before=src.read_bytes();bpy.ops.wm.open_mainfile(filepath=str(src));bpy.context.view_layer.update();col=bpy.data.collections['EXPORT'];objects=[];allpts=[];ct=json.loads(bpy.data.texts['BATCH107_COMPONENT_CONTRACT.json'].as_string());components=ct['components'];coordinate_data={}
for o in col.all_objects:
 if o.type!='MESH':continue
 v=[o.matrix_world@x.co for x in o.data.vertices];o.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in o.data.loop_triangles];allpts+=v;edges=collections.defaultdict(list)
 for i,t in enumerate(tris):
  for a,b in zip(t,t[1:]+t[:1]):edges[tuple(sorted((a,b)))].append((i,a<b))
 adj=collections.defaultdict(set)
 for e,inc in edges.items():
  for a,_ in inc:adj[a].update(b for b,_ in inc if a!=b)
 seen=set();solids=[]
 for i in range(len(tris)):
  if i in seen:continue
  seen.add(i);todo=[i];ids=[]
  while todo:
   t=todo.pop();ids.append(t)
   for k in adj[t]:
    if k not in seen:seen.add(k);todo.append(k)
  tid=set(ids);local=[inc for inc in edges.values() if inc[0][0] in tid];bad=sum(len(z)!=2 or z[0][1]==z[1][1] for z in local);vol=sum(v[tris[z][0]].dot(v[tris[z][1]].cross(v[tris[z][2]]))/6 for z in ids);solids.append({'triangles':len(ids),'edge_defects':bad,'signed_volume_m3':vol,'pass':bad==0 and vol>0})
 objects.append({'object':o.name,'vertices':len(v),'triangles':len(tris),'solid_count':len(solids),'solids':solids,'all_closed_outward':all(x['pass'] for x in solids),'modifiers':[m.type for m in o.modifiers]})
 coordinate_data[o.name]={'vertices_world_m':[list(p) for p in v],'triangles':tris,'contract':ct}
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(col.get('asset_root',''))
metadata=json.loads((src.parent/'metadata.json').read_text());options=metadata['export_options'];p=out/'source-reexport.glb';bpy.ops.export_scene.gltf(filepath=str(p),**options);audit=audit_glb(p,14000,6,30);original=audit_glb(src.with_suffix('.glb'),14000,6,30)
report={'status':'pass' if all(x['all_closed_outward'] for x in objects) and audit['semantic_sha256']==original['semantic_sha256'] else 'fail','source_sha256':hashlib.sha256(before).hexdigest(),'source_unchanged':before==src.read_bytes(),'source_saved':False,'normal_recalculation':False,'weld':False,'objects':objects,'bounds_blender_m':{'min':[min(v[k] for v in allpts) for k in range(3)],'max':[max(v[k] for v in allpts) for k in range(3)]},'reexport_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'original_glb_sha256':original['sha256'],'byte_identical_export':p.read_bytes()==src.with_suffix('.glb').read_bytes(),'semantic_identical_export':audit['semantic_sha256']==original['semantic_sha256'],'export_options':options,'pid':os.getpid(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(out/'source-reopen-export.json').write_text(json.dumps(report,indent=2)+'\n');(out/'source-geometry.json').write_text(json.dumps(coordinate_data,separators=(',',':'))+'\n');print(report['status'],report['byte_identical_export'],report['semantic_identical_export'])
