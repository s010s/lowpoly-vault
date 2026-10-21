"""Independent read-only source measurements and full-collection reexport.
No producer QA report is consumed. The original source is not saved or repaired.
"""
import bpy,sys,json,pathlib,hashlib,os,collections,math,datetime
from mathutils import Vector
from mathutils.bvhtree import BVHTree
Q=pathlib.Path(__file__).resolve().parent
intake=json.loads((Q/'final-intake.json').read_text()); W=pathlib.Path(intake['worktree'])
a=sys.argv[sys.argv.index('--')+1];item=next(x for x in intake['assets'] if x['asset_id']==a);D=Q/a;D.mkdir(exist_ok=True)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
start=now();src=W/item['source'];glb=W/item['glb'];sha=H(src)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
cols=[c for c in bpy.data.collections if c.get('asset_root')];assert len(cols)==1
objects=[o for o in cols[0].all_objects if o.type=='MESH'];assert len(objects)==1,[(o.name,o.type)for o in objects]
o=objects[0];me=o.data;me.calc_loop_triangles();vs=[o.matrix_world@v.co for v in me.vertices];tris=[tuple(t.vertices)for t in me.loop_triangles]
def bounds(pts):
 lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)]
 return {'min':lo,'max':hi,'size':[hi[k]-lo[k]for k in range(3)]}
span=max(bounds(vs)['size']);eps=span*1e-8
fulltree=BVHTree.FromPolygons(vs,tris,all_triangles=True,epsilon=0)
vertex_members=collections.defaultdict(list)
for v in me.vertices:
 for z in v.groups:
  if z.weight>0:vertex_members[z.group].append(v.index)
groups={};records=[]
for vg in o.vertex_groups:
 ids=vertex_members[vg.index];ss=set(ids);tt=[t for t in tris if set(t)<=ss];pts=[vs[i]for i in ids]
 ed=collections.defaultdict(list);adj=collections.defaultdict(set)
 for t in tt:
  for x,y in zip(t,t[1:]+t[:1]):ed[tuple(sorted((x,y)))].append((x,y));adj[x].add(y);adj[y].add(x)
 remaining=set(ids);islands=[]
 while remaining:
  seed=remaining.pop();island={seed};todo=[seed]
  while todo:
   for j in adj[todo.pop()]:
    if j in remaining:remaining.remove(j);island.add(j);todo.append(j)
  islands.append(island)
 volume=sum((vs[t[0]]-pts[0]).dot((vs[t[1]]-pts[0]).cross(vs[t[2]]-pts[0]))/6 for t in tt)
 samples=[('vertex',i,vs[i],i)for i in ids]+[('triangle_centroid',k,sum((vs[j]for j in t),Vector())/3,t[0])for k,t in enumerate(tt)]
 tree=BVHTree.FromPolygons(vs,tt,all_triangles=True,epsilon=0)
 groups[vg.name]={'ids':ids,'set':ss,'faces':tt,'tree':tree,'samples':samples,'islands':islands}
 records.append({'tag':vg.name,'vertices':len(ids),'triangles':len(tt),'bounds_blender_m':bounds(pts),'centroid_blender_m':list(sum(pts,Vector())/len(pts)),'islands':len(islands),'signed_volume_m3':volume,'boundary_edges':sum(len(e)==1 for e in ed.values()),'nonmanifold_edges':sum(len(e)>2 for e in ed.values()),'same_winding_edges':sum(len(e)==2 and e[0]==e[1]for e in ed.values())})
drs=[Vector(d).normalized()for d in [(1,.173,.293),(.139,1,.347),(.257,.419,1)]]
def inside(tree,p):
 near,n,idx,dist=tree.find_nearest(p)
 if near is None or dist<=eps:return False,{'nearest_surface_m':dist}
 votes=[]
 for dr in drs:
  count=0;origin=p.copy()
  for _ in range(300):
   hit,n,i,d=tree.ray_cast(origin,dr,span*3)
   if hit is None:break
   count+=1;origin=hit+dr*eps*4
  votes.append(count%2)
 return sum(votes)>=2,{'nearest_surface_m':dist,'parity_votes':votes}
contacts=[]
for rel in json.loads(o.get('contact_design','[]')):
 child,parent=rel['child'],rel['parent'];cg=groups[child];pg=groups[parent];island_results=[]
 for island in cg['islands']:
  witness=None
  for kind,ix,p,vertex in cg['samples']:
   if vertex not in island:continue
   ok,details=inside(pg['tree'],p)
   if ok:witness={'sample_component':child,'inside_component':parent,'sample_kind':kind,'sample_index':ix,'position':list(p),**details};break
  if witness is None:
   island_faces=[t for t in cg['faces']if t[0] in island];itree=BVHTree.FromPolygons(vs,island_faces,all_triangles=True,epsilon=0)
   for kind,ix,p,_ in pg['samples']:
    ok,details=inside(itree,p)
    if ok:witness={'sample_component':parent,'inside_component':child,'sample_kind':kind,'sample_index':ix,'position':list(p),**details};break
  island_results.append({'child_island_first_vertex':min(island),'strict_interior_witness':witness})
 contacts.append({'child':child,'parent':parent,'all_child_islands_true_intersection':all(z['strict_interior_witness']for z in island_results),'islands':island_results})
# Full-scene BVH includes even other islands in the same named group and the
# sampled solid itself. Outgoing ray escape is a numerical diagnostic, not a
# minimum percentage criterion and not a substitute for image inspection.
dirs=[Vector(d).normalized()for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,1),(-1,1,1),(1,-1,1),(-1,-1,1),(1,1,-1),(-1,1,-1),(1,-1,-1),(-1,-1,-1)]]
exposure=[]
for name,g in groups.items():
 seen=total=0;by=[0]*len(dirs);witness=[];island_by_vertex={v:k for k,island in enumerate(g['islands'])for v in island};island_visible=[0]*len(g['islands'])
 for fi,t in enumerate(g['faces']):
  x,y,z=[vs[i]for i in t]
  for i in range(5):
   for j in range(5-i):
    p=(x*i+y*j+z*(4-i-j))/4;vis=False;total+=1
    for di,dr in enumerate(dirs):
     if fulltree.ray_cast(p+dr*eps,dr,span*3)[0] is None:by[di]+=1;vis=True
    if vis:
     seen+=1;island_visible[island_by_vertex[t[0]]]+=1
     if len(witness)<2:witness.append({'triangle':fi,'position':list(p)})
 exposure.append({'tag':name,'sample_count':total,'exposed_count':seen,'diagnostic_fraction':seen/total if total else None,'exposed_by_direction':by,'island_exposed_samples':island_visible,'witnesses':witness})
lookup={r['tag']:r for r in records}
extras={'component_counts':{n:r['islands']for n,r in lookup.items()},'ring_geometry':{},'notes':['Named groups and mesh strips alone are not proof of an anatomical segmentation; radii, placement, materials, and exact final pixels are reviewed together.']}
def rings(tag,sides):
 ids=groups[tag]['ids'];assert len(ids)%sides==0
 rings=[ids[j:j+sides]for j in range(0,len(ids),sides)]
 centers=[sum((vs[i]for i in ring),Vector())/len(ring)for ring in rings]
 radii=[sum((vs[i]-c).length for i in ring)/len(ring)for ring,c in zip(rings,centers)]
 return {'ring_count':len(rings),'centerline_length_m':sum((q-p).length for p,q in zip(centers,centers[1:])),'centers_blender_m':[list(x)for x in centers],'radii_m':radii,'actual_radius_local_peaks':[j for j in range(1,len(radii)-1)if radii[j]>radii[j-1]and radii[j]>radii[j+1]],'surface_material_indices':sorted({p.material_index for p in me.polygons if set(p.vertices)<=groups[tag]['set']})}
if a=='kerygmachela':
 extras['flap_sizes']=[lookup[n]for n in sorted(groups)if n.startswith('flap_')]
 extras['tubercle_centers']=[{'tag':n,'center':lookup[n]['centroid_blender_m']}for n in sorted(groups)if n.startswith('tubercle_')]
 extras['eyes']=[lookup[n]for n in sorted(groups)if n.startswith('eye_')]
 extras['single_tail']=[lookup[n]for n in groups if n.startswith('median_tail')]
if a=='pambdelurion':
 extras['body_length_m']=lookup['annulated_trunk']['bounds_blender_m']['size'][1]
 extras['oral_geometry']=[lookup[n]for n in groups if n.startswith('oral_')]
 extras['ring_geometry']['annulated_trunk']=rings('annulated_trunk',12)
if a=='aegirocassis':
 for n in sorted(groups):
  if n.startswith('frontal_support_'):extras['ring_geometry'][n]=rings(n,6)
 extras['filter_setae_islands']={n:len(g['islands'])for n,g in groups.items()if n.startswith('filter_setae_')}
 extras['carapace_and_trunk']={n:lookup[n]for n in ['central_carapace','box_trunk']}
if a=='arthropleura':
 for n in sorted(groups):
  if n.startswith('antenna_'):extras['ring_geometry'][n]=rings(n,6)
  if n.startswith('leg_'):extras['ring_geometry'][n]=rings(n,5)
 extras['dorsal_units']=[lookup[n]for n in sorted(groups)if n.startswith('dorsal_unit_')]
 extras['body_core_length_m']=lookup['ventral_core']['bounds_blender_m']['size'][1]
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();em.calc_loop_triangles();counts={'authored_vertices':len(vs),'authored_polygons':len(me.polygons),'authored_triangles':len(tris),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles)};ev.to_mesh_clear()
bpy.ops.object.select_all(action='DESELECT')
for ob in cols[0].all_objects:ob.select_set(True)
opts=json.loads((W/item['metadata']).read_text())['export_options'];export=D/'reexport-full.glb';assert not export.exists()
bpy.ops.export_scene.gltf(filepath=str(export),**opts)
r={'asset_id':a,'revision':item['revision'],'host_started_at':start,'host_finished_at':now(),'clock_note':'Host timestamps are recorded as observed and may be ahead of authoritative session UTC.','pid':os.getpid(),'source_sha256':sha,'source_unchanged':H(src)==sha,'glb_sha256':H(glb),'reexport_sha256':H(export),'reexport_byte_identical':H(export)==H(glb),'source_saved':False,'script_autoexec':False,'export_collection':cols[0].name,'selected_objects':[ob.name for ob in cols[0].all_objects],'transform':[list(x)for x in o.matrix_world],'counts':counts,'bounds_blender_m':bounds(vs),'components':records,'contacts':contacts,'global_exposure':exposure,'actual_feature_checks':extras,'numerical_ray_epsilon_m':eps,'method':'Independent fresh source open. World-transformed original vertex membership and triangle geometry. Strict interior witnesses use nearest-surface exclusion plus3-ray parity in both contact directions per child island.15 barycentric samples per triangle test14 escape directions against the entire original scene, including other islands in the same semantic group. No mesh repair or arbitrary exposure fraction/organ-size threshold. Reexport includes the full original asset_root collection and pinned original exporter options.','gpu':'UNKNOWN','scene':'UNKNOWN'}
with (D/'source-audit.json').open('x')as f:json.dump(r,f,indent=2);f.write('\n')
print(a,'reexport_byte_identical',r['reexport_byte_identical'],'contact_failures',[c['child']for c in contacts if not c['all_child_islands_true_intersection']],'zero_exposed',[e['tag']for e in exposure if e['exposed_count']==0])
