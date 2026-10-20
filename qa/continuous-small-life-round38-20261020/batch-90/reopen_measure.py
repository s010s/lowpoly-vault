import bpy,sys,json,hashlib,os,datetime,math,collections,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('/workspace/shared/lowpoly-batch90-20261020');sys.path.insert(0,str(R/'scripts'))
from asset_common import audit_source
from qa_glb import audit_glb
from check_source_export import compare_source_audit
id,rev,out=sys.argv[sys.argv.index('--')+1:];O=Path(out);O.mkdir(parents=True,exist_ok=True);B=R/'production/batch90/assets'/id/rev
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();start=now();src=B/'source.blend';glb=B/'model.glb';before={str(p):h(p) for p in [src,glb]}
bpy.context.preferences.filepaths.use_scripts_auto_execute=False;bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();col=bpy.data.collections['EXPORT'];objs=[o for o in col.all_objects if o.type=='MESH'];sa=audit_source(col,14000);ga=audit_glb(glb,14000,6,30);parts=[];cs=[];pointsets=[];dg=bpy.context.evaluated_depsgraph_get()
for o in objs:
 m=o.data;m.calc_loop_triangles();ev=o.evaluated_get(dg);em=ev.to_mesh();em.calc_loop_triangles();parts.append(dict(name=o.name,vertices=len(m.vertices),triangles=len(m.loop_triangles),evaluated_vertices=len(em.vertices),evaluated_triangles=len(em.loop_triangles),modifiers=len(o.modifiers)));ev.to_mesh_clear()
 adj=[set() for v in m.vertices]
 for e in m.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 unseen=set(range(len(adj)))
 while unseen:
  q=min(unseen);ids={q};unseen.remove(q);stack=[q]
  while stack:
   for k in adj[stack.pop()]:
    if k in unseen:unseen.remove(k);ids.add(k);stack.append(k)
  ids=sorted(ids);v=np.array([tuple(o.matrix_world@m.vertices[i].co) for i in ids]);polys=[f for f in m.polygons if f.vertices[0] in ids];edges=collections.Counter(e for f in polys for e in f.edge_keys);rec=dict(object=o.name,vertices=len(ids),polygons=len(polys),material_names=sorted({m.materials[f.material_index].name for f in polys}),bounds_min=v.min(0).tolist(),bounds_max=v.max(0).tolist(),boundary_edges=sum(n==1 for n in edges.values()),nonmanifold_edges=sum(n!=2 for n in edges.values()),vertex_indices=ids);cs.append(rec);pointsets.append(v)
features={};verts=np.array([tuple(o.matrix_world@v.co) for o in objs for v in o.data.vertices]);features['actual_bounds_m']={'min':verts.min(0).tolist(),'max':verts.max(0).tolist(),'size':np.ptp(verts,axis=0).tolist()}
if id=='pertica':
 o=next(o for o in objs if 'sixteen' in o.name);buds=[(c,v) for c,v in zip(cs,pointsets) if c['material_names']==['sporangia']];lengths=[];radii=[]
 for c,v in buds:
  a=v-v.mean(0);w,U=np.linalg.eigh(a.T@a);u=U[:,-1];t=a@u;lengths.append(float(np.ptp(t)));radii.append(float(np.linalg.norm(a-np.outer(t,u),axis=1).max()))
 groups=[]
 for vg in sorted(o.vertex_groups,key=lambda x:x.name):
  ids=sorted(v.index for v in o.data.vertices if any(g.group==vg.index for g in v.groups));s=set(ids);v=np.array([tuple(o.matrix_world@o.data.vertices[i].co) for i in ids[:12]]);a=v[:6].mean(0);d=v[6:12].mean(0)-a;groups.append(dict(name=vg.name,z=float(a[2]),azimuth=math.degrees(math.atan2(d[1],d[0])),buds=sum(set(c['vertex_indices'])<=s for c,v in buds)))
 steps=[abs((b['azimuth']-a['azimuth']+180)%360-180) for a,b in zip(groups,groups[1:])];main=next(o for o in objs if o.name=='dominant-upright-axis');ring=np.array([tuple(main.matrix_world@v.co) for v in main.data.vertices[:8]])
 features.update(bud_count=len(buds),bud_lengths_minmax=[min(lengths),max(lengths)],bud_radii_minmax=[min(radii),max(radii)],lateral_groups=groups,rank_step_minmax=[min(steps),max(steps)],fertile_laterals=sum(x['buds']==16 for x in groups),sterile_laterals=sum(x['buds']==0 for x in groups),main_base_radius=float(np.linalg.norm(ring-ring.mean(0),axis=1).max()),closed_components=len(cs))
elif id.startswith('zoophycos'):
 o=next(o for o in objs if o.name.startswith('broad'));v=np.array([tuple(o.matrix_world@x.co) for x in o.data.vertices]);half=len(v)//2;bottom=v[:half];top=v[half:];row=13;edge=bottom[row-1::row];ang=np.unwrap(np.arctan2(edge[:,1],edge[:,0]));signals={}
 for j in [3,6,9,12]:
  s=top[j::row,2]-bottom[j::row,2];peaks=[i for i in range(1,len(s)-1) if s[i]>s[i-1]+1e-8 and s[i]>s[i+1]+1e-8];signals[str(j)]={'complete_interior_peak_count':len(peaks),'peak_indices':peaks,'end_half_peaks':int(s[0]>s[1]+1e-8)+int(s[-1]>s[-2]+1e-8),'relief_peak_to_trough_m':float(np.ptp(s))}
 shaft=next(o for o in objs if 'shaft' in o.name);sv=np.array([tuple(shaft.matrix_world@x.co) for x in shaft.data.vertices]);features.update(sheet_outer_radius_max=float(np.linalg.norm(v[:,:2],axis=1).max()),sheet_inner_radius_min=float(np.linalg.norm(v[:,:2],axis=1).min()),sheet_turns=float(abs(ang[-1]-ang[0])/math.tau),sheet_rise=float(edge[-1,2]-edge[0,2]),sheet_min_thickness=float((top[:,2]-bottom[:,2]).min()),lamella_signals=signals,shaft_radius_max=float(np.linalg.norm(sv[:,:2],axis=1).max()),shaft_top=float(sv[:,2].max()),shaft_bottom=float(sv[:,2].min()))
else:
 o=objs[0];T=.009 if id.startswith('rosary') else .012
 def z(x,y):
  hit,p,n,fi=o.ray_cast(Vector((x,y,1)),Vector((0,0,-1)));return p.z if hit else None
 features.update(full_volume_components=len(cs),max_relief_m=float(verts[:,2].max()-T),bottom_z=float(verts[:,2].min()),relief_vertex_bbox=(np.ptp(verts[verts[:,2]>T+.0004],axis=0)).tolist())
 if id.startswith('rosary'):
  ts=np.linspace(0,1,2401);profile=[z(-.04+.08*t,.009*math.sin(math.tau*t-.4))-T for t in ts];peaks=[i for i in range(1,len(profile)-1) if profile[i]>profile[i-1]+1e-9 and profile[i]>profile[i+1]+1e-9 and profile[i]>.002];widths=[]
  for t in [6/12,5.5/12]:
   x=-.04+.08*t;y=.009*math.sin(math.tau*t-.4);n=np.array([-.009*math.tau*math.cos(math.tau*t-.4),.08]);n/=np.linalg.norm(n);dist=np.linspace(-.005,.005,2001);positive=[d for d in dist if z(x+n[0]*d,y+n[1]*d)>T+.00008];widths.append(float(max(positive)-min(positive)))
  # Base footprint for all individual lobes at the original frozen centers. This is geometry, not material color.
  center_peaks=[z(-.04+.08*t,.009*math.sin(math.tau*t-.4))-T for t in np.linspace(0,1,13)]
  features.update(interior_chamber_peaks=len(peaks),terminal_chamber_peaks=int(profile[0]>.002)+int(profile[-1]>.002),total_chamber_peaks=len(peaks)+int(profile[0]>.002)+int(profile[-1]>.002),center_reliefs=center_peaks,minimum_centerline_relief=min(profile),width_sample_threshold_m=.00008,chamber_neck_widths_m=widths,chamber_neck_ratio=widths[0]/widths[1])
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']];opts=json.loads((B/'metrics.json').read_text())['export_options'];opts['filepath']=str(O/'source-reexport.glb');bpy.ops.export_scene.gltf(**opts);ra=audit_glb(O/'source-reexport.glb',14000,6,30)
report=dict(asset_id=id,revision=rev,started_at=start,finished_at=now(),pid=os.getpid(),blender=bpy.app.version_string,source_sha256=h(src),glb_sha256=h(glb),source_unchanged=all(h(p)==v for p,v in before.items()),source_saved=False,autoexec=False,parts=parts,components=cs,actual_features=features,source_audit=sa,glb_audit=ga,source_export_comparison=compare_source_audit(sa,ga,h(src),h(glb)),reexport_sha256=h(O/'source-reexport.glb'),reexport_semantic_match=ga['semantic_sha256']==ra['semantic_sha256'],reexport_byte_match=h(glb)==h(O/'source-reexport.glb'))
(O/'own-source-reopen-reexport.json').write_text(json.dumps(report,indent=2)+'\n');print(id,json.dumps(features),report['reexport_semantic_match'])
