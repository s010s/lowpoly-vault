# SPDX-License-Identifier: MIT
import bpy,sys,pathlib,json,hashlib,datetime,math,numpy as np,bmesh,os
b=pathlib.Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'));aid=b.parent.name;brief=json.loads((b/'brief.json').read_text());sem=json.loads((b/'geometry-semantics.json').read_text());objs=[o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH'];deps=bpy.context.evaluated_depsgraph_get();parts=[];checks={}
def check(n,v,lo,hi):checks[n]=dict(measured=v,allowed=[lo,hi],pass_=lo-1e-7<=v<=hi+1e-7);checks[n]['pass']=checks[n].pop('pass_')
def groupv(o,g):return np.array([tuple(o.matrix_world@v.co)for v in o.data.vertices if any(s.group==g.index and s.weight>.5 for s in v.groups)])
for o in objs:
 o.data.calc_loop_triangles();e=o.evaluated_get(deps);m=e.to_mesh();m.calc_loop_triangles();bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not edge.is_manifold for edge in bm.edges);bm.free();check(o.name+'-nonmanifold-edges',bad,0,0);parts.append(dict(name=o.name,authored_vertices=len(o.data.vertices),evaluated_vertices=len(m.vertices),authored_polygons=len(o.data.polygons),evaluated_polygons=len(m.polygons),authored_triangles=len(o.data.loop_triangles),evaluated_triangles=len(m.loop_triangles)));e.to_mesh_clear()
allv=np.array([tuple(o.matrix_world@v.co)for o in objs for v in o.data.vertices]);bounds=(allv.max(0)-allv.min(0)).tolist()
for axis,(v,range_)in enumerate(zip(bounds,brief['scale']['hard_overall_bounds_blender_xyz_m'])):check('whole-'+str(axis)+'-extent-including-caps-m',v,*range_)
check('bottom-ground-contact-m',float(allv[:,2].min()),-1e-7,1e-7)
if aid=='eophyllophyton':
 o=next(o for o in objs if o.name.startswith('twenty-four'));a=next(o for o in objs if o.name.startswith('slender-three'));check('leaf-count-actual-nonempty-vertex-groups',sum(len(groupv(o,g))>0 for g in o.vertex_groups),24,24);check('terminal-shoot-actual-nonempty-groups',sum(g.name.startswith('terminal-shoot')and len(groupv(a,g))>0 for g in a.vertex_groups),12,12);lengths=[];widths=[]
 for f in sem['leaf_frames']:
  vv=groupv(o,o.vertex_groups[f['group']]);L=vv@np.array(f['longitudinal']);W=vv@np.array(f['transverse']);lengths.append(float(np.ptp(L)));widths.append(float(np.ptp(W)))
 check('minimum-leaf-local-longitudinal-span-m',min(lengths),.0022,.005);check('maximum-leaf-local-longitudinal-span-m',max(lengths),.0022,.005);check('minimum-leaf-local-transverse-span-m',min(widths),.0017,.0048);check('maximum-leaf-local-transverse-span-m',max(widths),.0017,.0048);checks['per-leaf-dimensions']={'longitudinal_m':lengths,'transverse_m':widths,'method':'Actual vertices projected onto stored construction unit vectors; fold/cap included. Directions define measurement, no lengths echoed from config.'}
elif aid=='oncoid-bed':
 o=objs[0];check('actual-grain-groups',sum(g.name.startswith('grain-')and len(groupv(o,g))>0 for g in o.vertex_groups),16,16);check('actual-cut-grain-groups',sum(g.name.startswith('cut-grain-')and len(groupv(o,g))>0 for g in o.vertex_groups),3,3)
elif aid=='caytonia':
 o=next(o for o in objs if o.name.startswith('twelve'));a=next(o for o in objs if o.name.startswith('slender'));check('actual-cupule-groups',sum(len(groupv(o,g))>0 for g in o.vertex_groups),12,12);check('actual-stalk-groups',sum(g.name.startswith('stalk-')and len(groupv(a,g))>0 for g in a.vertex_groups),12,12);check('paired-level-groups',len(set(g.name.split('-pair-')[1]for g in o.vertex_groups)),6,6)
 cos=[]
 for f in sem['cupule_frames']:
  vv=groupv(o,o.vertex_groups[f['group']]);mouth=vv[:f['opening_vertex_count']].mean(0);center=vv.mean(0);axis=mouth-center;cos.append(float(axis@np.array(f['opening_axis'])/np.linalg.norm(axis)))
 check('actual-mouth-proximal-direction-cosine-min',min(cos),.90,1.00001);checks['mouth_note']={'method':'Actual first mouth-rim vertices minus actual component centroid compared to proximal attachment direction. Not render-only assurance.'}
else:
 check('actual-mound-mesh-count',len(objs),1,1)
 # Physical connectivity proof for continuous integrated mound.
 o=objs[0];adj={v.index:set()for v in o.data.vertices}
 for ed in o.data.edges:a,c=ed.vertices;adj[a].add(c);adj[c].add(a)
 seen=set();count=0
 for i in adj:
  if i in seen:continue
  count+=1;todo=[i]
  while todo:
   j=todo.pop()
   if j in seen:continue
   seen.add(j);todo.extend(adj[j]-seen)
 check('actual-connected-mound-components',count,1,1)
report=dict(kind='actual-source-geometric-freeze-diagnostics',source_sha256=hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),glb_sha256=hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),observed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),pid=os.getpid(),parts=parts,bounds_blender_xyz_m=bounds,checks=checks,all_numeric_checks_pass=all(x.get('pass',True)for x in checks.values()),limitations='Actual authored/evaluated vertices and connectivity, not config self-attestation; maker diagnostic, not independent approval.')
for k in ['authored_vertices','evaluated_vertices','authored_polygons','evaluated_polygons','authored_triangles','evaluated_triangles']:report[k]=sum(v[k]for v in parts)
(b/'source-vertex-counts.json').write_text(json.dumps(report,indent=2)+'\n');print(aid,report['all_numeric_checks_pass'],json.dumps({n:v for n,v in checks.items()if v.get('pass')is False}))
