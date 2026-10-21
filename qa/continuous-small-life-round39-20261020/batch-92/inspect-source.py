import bpy, bmesh, sys, pathlib, json, hashlib, os, datetime, math
import numpy as np
sys.dont_write_bytecode = True
src, dst = map(pathlib.Path, sys.argv[sys.argv.index('--')+1:])
dst.mkdir(parents=True, exist_ok=True)
root = pathlib.Path('/workspace/shared/lowpoly-batch92-20261020')
sys.path.insert(0, str(root/'scripts'))
from qa_glb import audit_glb
from asset_common import audit_source
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
original={n:sha(src/n) for n in ['source.blend','model.glb','candidate-brief.json','references.json']}
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(src/'source.blend'),load_ui=False,use_scripts=False)
bpy.context.view_layer.update()
col=bpy.data.collections['EXPORT']; obs=[o for o in col.all_objects if o.type=='MESH']; dg=bpy.context.evaluated_depsgraph_get()
brief=json.loads((src.parent/'r001/brief.json').read_text()); sem=json.loads((src/'geometry-semantics.json').read_text())
def bounds(v):
 a=np.array(v); return dict(min=a.min(0).tolist(),max=a.max(0).tolist(),size=np.ptp(a,axis=0).tolist())
def group_indices(o,g): return [v.index for v in o.data.vertices if any(s.group==g.index and s.weight>.5 for s in v.groups)]
def worldv(o,idx): return np.array([tuple(o.matrix_world@o.data.vertices[i].co) for i in idx])
def connected_components(mesh,indices=None):
 indices=set(range(len(mesh.vertices))) if indices is None else set(indices)
 edges={i:set() for i in indices}
 for e in mesh.edges:
  a,b=e.vertices
  if a in edges and b in edges: edges[a].add(b);edges[b].add(a)
 seen=set(); sizes=[]
 for i in edges:
  if i in seen: continue
  todo=[i];comp=set()
  while todo:
   j=todo.pop()
   if j in seen:continue
   seen.add(j);comp.add(j);todo.extend(edges[j]-seen)
  sizes.append(len(comp))
 return sorted(sizes)
parts=[]; all_a=[]; all_e=[]; groups={}; failures=[]
def check(name,value,expected):
 ok=bool(expected(value)); checks[name]={'measured':value,'pass':ok}
 if not ok:failures.append(name)
checks={}
for o in obs:
 a=worldv(o,range(len(o.data.vertices)));all_a.extend(a.tolist())
 o.data.calc_loop_triangles(); eo=o.evaluated_get(dg);em=eo.to_mesh();em.calc_loop_triangles();ev=np.array([tuple(eo.matrix_world@v.co) for v in em.vertices]);all_e.extend(ev.tolist())
 bm=bmesh.new();bm.from_mesh(o.data);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
 groups[o.name]={g.name:{'indices_count':len(ix:=group_indices(o,g)),'connected_component_vertex_counts':connected_components(o.data,ix),'world_bounds':bounds(worldv(o,ix))} for g in o.vertex_groups if len(group_indices(o,g))}
 parts.append(dict(name=o.name,authored_vertices=len(o.data.vertices),authored_triangles=len(o.data.loop_triangles),evaluated_vertices=len(em.vertices),evaluated_triangles=len(em.loop_triangles),authored_world_bounds=bounds(a),evaluated_world_bounds=bounds(ev),local_bounds=bounds([tuple(v.co) for v in o.data.vertices]),matrix_world=[list(row) for row in o.matrix_world],modifiers=[m.type for m in o.modifiers],nonmanifold_edges=nonmanifold,connected_component_vertex_counts=connected_components(o.data)))
 check(o.name+' closed edge manifold',nonmanifold,lambda v:v==0)
 eo.to_mesh_clear()
world=bounds(all_a); evaluated=bounds(all_e)
for axis,(lo,hi) in enumerate(brief['scale']['hard_overall_bounds_blender_xyz_m']):
 check('world bound '+str(axis),world['size'][axis],lambda v,lo=lo,hi=hi:lo-1e-7<=v<=hi+1e-7)
 check('evaluated bound '+str(axis),evaluated['size'][axis],lambda v,lo=lo,hi=hi:lo-1e-7<=v<=hi+1e-7)
check('bottom contact',world['min'][2],lambda v:abs(v)<1e-7)
components={}; aid=src.parent.name
if aid=='eophyllophyton':
 leaf=next(o for o in obs if o.name.startswith('twenty-four'));axis=next(o for o in obs if o.name.startswith('slender'))
 check('leaf count',len(leaf.vertex_groups),lambda v:v==24)
 check('terminal shoot count',sum(g.name.startswith('terminal-shoot') for g in axis.vertex_groups),lambda v:v==12)
 for f in sem['leaf_frames']:
  ix=group_indices(leaf,leaf.vertex_groups[f['group']]);vv=worldv(leaf,ix);u=np.array(f['longitudinal']);v=np.array(f['transverse']);normal=np.cross(v,u);half=len(vv)//2
  length=float(np.ptp(vv@u));width=float(np.ptp(vv@v));thickness=((vv[half:]-vv[:half])@normal).tolist()
  components[f['group']]=dict(longitudinal_span_m=length,transverse_span_m=width,paired_lamina_thickness_m=[min(thickness),max(thickness)],folded_normal_bbox_m=float(np.ptp(vv@normal)),basis_norms=[float(np.linalg.norm(u)),float(np.linalg.norm(v))],basis_dot=float(u@v),world_bounds=bounds(vv),connected_components=connected_components(leaf.data,ix))
  check(f['group']+' length',length,lambda x:.0022-1e-7<=x<=.005+1e-7)
  check(f['group']+' width',width,lambda x:.0017-1e-7<=x<=.0048+1e-7)
  check(f['group']+' component',len(connected_components(leaf.data,ix)),lambda x:x==1)
elif aid=='oncoid-bed':
 o=obs[0];grain=[g for g in o.vertex_groups if g.name.startswith('grain-')];cuts=[g for g in o.vertex_groups if g.name.startswith('cut-grain-')]
 check('grain count',len(grain),lambda v:v==16);check('cut grain count',len(cuts),lambda v:v==3)
 check('disconnected source shells including bed',len(connected_components(o.data)),lambda v:v==17)
 components=groups[o.name]
elif aid=='thrombolite-mound':
 check('mound objects',len(obs),lambda v:v==1);check('connected mound shells',len(connected_components(obs[0].data)),lambda v:v==1)
 components=parts
elif aid=='caytonia':
 cup=next(o for o in obs if o.name.startswith('twelve'));axis=next(o for o in obs if o.name.startswith('slender'))
 check('cupule count',len(cup.vertex_groups),lambda v:v==12);check('pair count',len(set(g.name.split('-pair-')[1] for g in cup.vertex_groups)),lambda v:v==6)
 for f in sem['cupule_frames']:
  name=f['group'];ix=group_indices(cup,cup.vertex_groups[name]);vv=worldv(cup,ix);stalk=worldv(axis,group_indices(axis,axis.vertex_groups['stalk-'+name.split('-')[1]]));attach=stalk[:6].mean(0);mouth=vv[:f['opening_vertex_count']].mean(0);center=vv.mean(0);a=mouth-center;b=attach-center;cos=float(a@b/np.linalg.norm(a)/np.linalg.norm(b))
  components[name]=dict(actual_mouth_centroid_world_m=mouth.tolist(),actual_stalk_root_ring_centroid_world_m=attach.tolist(),actual_component_centroid_world_m=center.tolist(),mouth_proximal_cosine=cos,world_bounds=bounds(vv),connected_components=connected_components(cup.data,ix))
  check(name+' proximal opening',cos,lambda x:x>.9)
source_audit=audit_source(col,14000);original_audit=audit_glb(src/'model.glb',14000,6,30)
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=json.loads((src/'metrics.json').read_text())['export_options'];opts['filepath']=str(dst/'reexport.glb')
bpy.ops.export_scene.gltf(**opts)
fresh=audit_glb(dst/'reexport.glb',14000,6,30)
check('reexport byte identical',sha(dst/'reexport.glb'),lambda x:x==original['model.glb'])
check('source input unmodified',{n:sha(src/n) for n in original},lambda x:x==original)
check('source audit errors',source_audit['errors'],lambda x:not x);check('GLB audit errors',original_audit['errors'],lambda x:not x)
check('source exported triangle match',sum(x['evaluated_triangles'] for x in parts),lambda x:x==original_audit['scene_triangles'])
converted=[world['size'][0],world['size'][2],world['size'][1]];check('exported axis converted bounds maxdelta',max(abs(a-b) for a,b in zip(converted,original_audit['bounds_m']['size'])),lambda x:x<1e-7)
report=dict(kind='fresh-independent-source-reopen-measure-reexport',asset_id=aid,pid=os.getpid(),started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),blender=bpy.app.version_string,script_autoexec=False,source_saved=False,input_hashes=original,parts=parts,groups=groups,components=components,authored_world_bounds=world,evaluated_world_bounds=evaluated,checks=checks,source_audit=source_audit,project_audit=original_audit,reexport_project_audit=fresh,reexport_sha256=sha(dst/'reexport.glb'),status='pass' if not failures else 'fail',failures=failures,gpu='not_run',scene='not_run')
(dst/'source-inspection.json').write_text(json.dumps(report,indent=2)+'\n');print('INDEPENDENT_SOURCE_RESULT',aid,report['status'],failures)
