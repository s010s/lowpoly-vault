import bpy,json,sys,os,pathlib,hashlib,datetime,math,collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch101-20261021'); O=pathlib.Path('/workspace/shared/lowpoly-batch101-independent-qa-20261021'); aid=sys.argv[sys.argv.index('--')+1];rev='r002' if aid=='protospongia' else 'r001';B=W/'production/small-life-batch101'/aid/rev;D=O/aid;D.mkdir(exist_ok=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();started=now();src=B/'artifacts'/f'{aid}.blend';sha=H(src)
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ct=json.loads(bpy.data.texts['BATCH101_COMPONENT_CONTRACT.json'].as_string());ob=bpy.data.objects[ct['object_name']];me=ob.data;me.calc_loop_triangles();v=[ob.matrix_world@q.co for q in me.vertices];tri=[tuple(t.vertices)for t in me.loop_triangles]
def bounds(pts):
 lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)];return {'min':lo,'max':hi,'size':[hi[k]-lo[k]for k in range(3)]}
span=max(bounds(v)['size']);eps=span*1e-9;comps={c['tag']:c for c in ct['components']};groups={};records=[]
for name,c in comps.items():
 ids=set(c['vertices']);fs=[t for t in tri if set(t)<=ids];pts=[v[i]for i in c['vertices']];vs=set(q.index for q in me.vertices for g in q.groups if g.group==ob.vertex_groups[name].index and g.weight>0);assert vs==ids
 ax=[(ob.matrix_world.to_3x3()@Vector(a)).normalized()for a in c['axes']];dims=[max(p.dot(a)for p in pts)-min(p.dot(a)for p in pts)for a in ax];tree=BVHTree.FromPolygons(v,fs,all_triangles=True);groups[name]={'ids':ids,'faces':fs,'tree':tree,'bounds':bounds(pts)}
 records.append({'tag':name,'kind':c['kind'],'vertices':len(ids),'triangles':len(fs),'bounds_blender_m':bounds(pts),'axes_world':[list(a)for a in ax],'length_m':dims[0],'width_m':dims[1],'thickness_m':dims[2],'vertex_group_matches_contract':True})
# Contact witnesses derive from exact triangle intersections or actual vertices inside closed parent, never signed nearest-face estimates.
drs=[Vector(d).normalized()for d in [(1,.173,.293),(.139,1,.347),(.257,.419,1)]]
def inside(tree,p):
 q,n,i,d=tree.find_nearest(p)
 if q is not None and d<=eps:return True,{'surface_distance_m':d}
 votes=[]
 for dr in drs:
  count=0;origin=p.copy()
  for _ in range(400):
   hit,n,i,d=tree.ray_cast(origin,dr,span*3)
   if hit is None:break
   count+=1;origin=hit+dr*eps*4
  votes.append(count%2)
 return sum(votes)>=2,{'parity_votes':votes}
contacts=[]
for name,c in comps.items():
 if not c.get('parent'):continue
 parent=c['parent'];g=groups[name];pg=groups[parent]
 if c.get('shared_topology'):
  shared=g['ids']&pg['ids'];rec={'child':name,'parent':parent,'shared_vertex_count':len(shared),'contact':bool(shared),'method':'Original common topology vertex indices, child is a tissue region, not a separate solid.'}
 else:
  pairs=g['tree'].overlap(pg['tree']);witness=None
  if not pairs:
   for ix in c['vertices']:
    ok,detail=inside(pg['tree'],v[ix])
    if ok:witness={'source_vertex':ix,'position':list(v[ix]),**detail};break
  rec={'child':name,'parent':parent,'triangle_overlap_pairs':len(pairs),'containment_witness':witness,'contact':bool(pairs)or witness is not None,'method':'Exact transformed triangle BVH intersections; fallback three-direction solid ray parity on actual source vertices.'}
 contacts.append(rec)
# Dense all-scene visibility, no pass percentage. All original other triangles including non-parent occluders are tested.
directions=[Vector(x).normalized()for x in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,1),(-1,1,1),(1,-1,1),(-1,-1,1),(1,1,-1),(-1,1,-1),(1,-1,-1),(-1,-1,-1)]]
expo=[]
for name,c in comps.items():
 g=groups[name];rest=[t for t in tri if not set(t)<=g['ids']];tree=BVHTree.FromPolygons(v,rest,all_triangles=True)if rest else None;seen=0;total=0;by=[0]*len(directions);exposed_witnesses=[]
 for fi,t in enumerate(g['faces']):
  a,b,cc=[v[i]for i in t]
  for i in range(5):
   for j in range(5-i):
    p=(a*i+b*j+cc*(4-i-j))/4;visible=False;total+=1
    for di,dr in enumerate(directions):
     if tree is None or tree.ray_cast(p+dr*eps,dr,span*3)[0] is None:by[di]+=1;visible=True
    if visible:
     seen+=1
     if len(exposed_witnesses)<2:exposed_witnesses.append({'triangle':fi,'position':list(p)})
 expo.append({'tag':name,'kind':c['kind'],'sample_count':total,'exposed_count':seen,'diagnostic_fraction':seen/total if total else None,'exposed_by_direction':by,'witnesses':exposed_witnesses})
brief=json.loads((B/'original-brief.json').read_text());rules=[]
for rule in brief['hard_organ_ranges']:
 field={'oriented_length_m':'length_m','oriented_width_m':'width_m','oriented_thickness_m':'thickness_m'}[rule['measure']];rr=[r for r in records if r['kind']==rule['kind']];lo,hi=rule['range'];rules.append({'original_rule':rule,'count':len(rr),'observed_min_m':min(r[field]for r in rr),'observed_max_m':max(r[field]for r in rr),'violations':[r['tag']for r in rr if not lo-1e-8<=r[field]<=hi+1e-8]})
extras={}
if aid=='winfrenatia':
 extras['mat_thickness_m']=next(r['thickness_m']for r in records if r['kind']=='layered_mat');extras['pit_open_rim_depth_m']=[r['thickness_m']for r in records if r['kind']=='pit'];extras['actual_depth_from_top_surface_m']=[max(v[i].z for i in comps['mat_body']['vertices'])-min(v[i].z for i in comps[r['tag']]['vertices'])for r in records if r['kind']=='pit']
if aid=='marchantites':
 paths={}
 for name,c in comps.items():
  if c['kind']=='costa':
   pts=[v[i]for i in c['vertices']];paths[name]=[sum(pts[i:i+6],Vector())/6 for i in range(0,len(pts)-2,6)]
 lens={n:sum((b-a).length for a,b in zip(pp,pp[1:]))for n,pp in paths.items()};extras['max_path_m']=max(lens['costa_0']+lens['costa_1'],lens['costa_0']+lens['costa_2']+max(lens['costa_3'],lens['costa_4']));extras['branch_angles_deg']=[math.degrees((paths[a][1]-paths[a][0]).angle(paths[b][1]-paths[b][0]))for a,b in [('costa_1','costa_2'),('costa_3','costa_4')]]
 ids=comps['thallus']['vertices'];outline=[v[i]for i in ids[:len(ids)//2]];sections=[]
 for n in ['costa_0','costa_1','costa_3','costa_4']:
  a,b=paths[n][-2:];d=(b-a).normalized();perp=Vector((-d.y,d.x,0));mid=(a+b)/2;cuts=[]
  for q,r in zip(outline,outline[1:]+outline[:1]):
   delta=r-q;den=delta.dot(d)
   if abs(den)<1e-14:continue
   u=-(q-mid).dot(d)/den
   if 0<=u<=1:cuts.append((q+u*delta-mid).dot(perp))
  width=min(x for x in cuts if x>=0)-max(x for x in cuts if x<=0);sections.append({'costa':n,'body_cross_section_m':width})
 extras['strap_sections']=sections
 # Check actual scale pairs in each named row. Projection overlap is a prerequisite for imbrication; disjoint AABBs can conclusively disprove overlap but are never contact proof.
 scales=[r for r in records if r['kind']=='ventral_scale'];pairs=[]
 for i,a in enumerate(scales):
  for b in scales[i+1:]:
   if a['tag'].split('_')[-1]!=b['tag'].split('_')[-1]:continue
   ba=a['bounds_blender_m'];bb=b['bounds_blender_m'];proj=all(max(ba['min'][k],bb['min'][k])<=min(ba['max'][k],bb['max'][k])for k in [0,1]);gap=math.sqrt(sum(max(0,ba['min'][k]-bb['max'][k],bb['min'][k]-ba['max'][k])**2 for k in [0,1]));pairs.append({'a':a['tag'],'b':b['tag'],'xy_bounds_overlap':proj,'xy_lower_bound_gap_m':gap,'exact_triangle_intersections':len(groups[a['tag']]['tree'].overlap(groups[b['tag']]['tree']))})
 extras['same_row_scale_pairs']=pairs;extras['same_row_xy_overlap_count']=sum(x['xy_bounds_overlap']for x in pairs);extras['nearest_same_row_gap_m']=min(x['xy_lower_bound_gap_m']for x in pairs)
if aid=='protospongia':
 extras['orders']={str(i):{'count':sum(r['kind']=='spicule_order_'+str(i)for r in records),'actual_full_vertical_extents_m':[r['length_m']for r in records if r['kind']=='spicule_order_'+str(i)],'actual_full_horizontal_extents_m':[r['width_m']for r in records if r['kind']=='spicule_order_'+str(i)]}for i in range(1,7)}
# Authored/evaluated count parity; original source unmodified; independent reexport uses explicit pinned export options.
ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();em.calc_loop_triangles();evaldata={'vertices':len(em.vertices),'triangles':len(em.loop_triangles),'bounds':bounds([ev.matrix_world@x.co for x in em.vertices])};ev.to_mesh_clear()
bpy.ops.object.select_all(action='DESELECT');col=next(c for c in bpy.data.collections if c.get('asset_root'))
for o in col.all_objects:o.select_set(True)
opts=json.loads((B/'artifacts/metadata.json').read_text())['export_options'];bpy.ops.export_scene.gltf(filepath=str(D/'reexport.glb'),**opts)
r={'asset_id':aid,'revision':rev,'started_at':started,'finished_at':now(),'pid':os.getpid(),'source_sha256':sha,'source_unchanged':H(src)==sha,'glb_sha256':H(B/'artifacts'/f'{aid}.glb'),'reexport_sha256':H(D/'reexport.glb'),'reexport_identical':H(D/'reexport.glb')==H(B/'artifacts'/f'{aid}.glb'),'objects':[{'name':o.name,'type':o.type}for o in bpy.context.scene.objects],'matrix_world':[list(x)for x in ob.matrix_world],'authored_vertices':len(v),'authored_triangles':len(tri),'evaluated':evaldata,'bounds_blender_m':bounds(v),'component_kind_counts':dict(collections.Counter(c['kind']for c in comps.values())),'components':records,'contacts':contacts,'global_exposure':expo,'original_range_checks':rules,'extra_source_checks':extras,'limits':'Visibility samples are diagnostics only, no new numerical percentage gate. Original meshes never repaired or resaved. GPU and composed scene not run.'}
(D/'source-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(aid,'reexport identical',r['reexport_identical'],'contacts',len(contacts),'fail',[c['child']for c in contacts if not c['contact']],'rangefails',[x for x in rules if x['violations']])
