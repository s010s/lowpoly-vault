import bpy,sys,json,pathlib,datetime,hashlib,os,collections,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch102-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch102-independent-qa-20261021');a=sys.argv[sys.argv.index('--')+1];rev={'arborea':'r003','swartpuntia':'r002','coronacollina':'r001','echmatocrinus':'r002'}[a];B=W/'production/small-life-batch102'/a/rev;D=O/a;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();start=now();src=B/'artifacts'/f'{a}.blend';sha=H(src)
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(objects)==1;o=objects[0];me=o.data;me.calc_loop_triangles();vs=[o.matrix_world@v.co for v in me.vertices];tris=[tuple(t.vertices)for t in me.loop_triangles]
def bounds(pts):
 lo=[min(p[k]for p in pts)for k in range(3)];hi=[max(p[k]for p in pts)for k in range(3)];return {'min':lo,'max':hi,'size':[hi[k]-lo[k]for k in range(3)]}
span=max(bounds(vs)['size']);eps=span*1e-8;groups={};records=[]
for g in o.vertex_groups:
 ids=[v.index for v in me.vertices if any(z.group==g.index and z.weight>0 for z in v.groups)];ss=set(ids);tt=[t for t in tris if set(t)<=ss];pts=[vs[i]for i in ids];tree=BVHTree.FromPolygons(vs,tt,all_triangles=True);ed=collections.defaultdict(list);vol=0;adj=collections.defaultdict(set)
 for t in tt:
  x,y,z=[vs[i]for i in t];vol+=x.dot(y.cross(z))/6
  for x,y in zip(t,t[1:]+t[:1]):ed[tuple(sorted((x,y)))].append((x,y));adj[x].add(y);adj[y].add(x)
 remaining=set(ids);islands=0
 while remaining:
  todo=[remaining.pop()];islands+=1
  while todo:
   for j in adj[todo.pop()]:
    if j in remaining:remaining.remove(j);todo.append(j)
 samples=[(i,vs[i])for i in ids]+[(len(vs)+i,sum((vs[j]for j in t),Vector())/3)for i,t in enumerate(tt)]
 groups[g.name]={'ids':ids,'set':ss,'faces':tt,'tree':tree,'samples':samples};records.append({'tag':g.name,'vertices':len(ids),'triangles':len(tt),'bounds_blender_m':bounds(pts),'islands':islands,'signed_volume_m3':vol,'boundary_edges':sum(len(e)==1 for e in ed.values()),'nonmanifold_edges':sum(len(e)>2 for e in ed.values()),'same_winding_edges':sum(len(e)==2 and e[0]==e[1]for e in ed.values())})
drs=[Vector(d).normalized()for d in [(1,.173,.293),(.139,1,.347),(.257,.419,1)]]
def inside(tree,p):
 near,n,idx,dist=tree.find_nearest(p)
 if near is None or dist<=eps:return False,{'nearest_surface_m':dist,'strict_interior':False}
 votes=[]
 for dr in drs:
  count=0;origin=p.copy()
  for _ in range(200):
   hit,n,i,d=tree.ray_cast(origin,dr,span*3)
   if hit is None:break
   count+=1;origin=hit+dr*eps*4
  votes.append(count%2)
 return sum(votes)>=2,{'nearest_surface_m':dist,'parity_votes':votes}
contacts=[]
for rel in json.loads(o['contact_design']):
 child,parent=rel['child'],rel['parent'];witness=None
 for x,y in [(child,parent),(parent,child)]:
  for ix,p in groups[x]['samples']:
   ok,details=inside(groups[y]['tree'],p)
   if ok:witness={'sample_component':x,'inside_component':y,'sample_index':ix,'position':list(p),**details};break
  if witness:break
 contacts.append({'child':child,'parent':parent,'true_solid_intersection':witness is not None,'strict_interior_witness':witness,'triangle_overlap_pairs':len(groups[child]['tree'].overlap(groups[parent]['tree']))})
dirs=[Vector(d).normalized()for d in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1),(1,1,1),(-1,1,1),(1,-1,1),(-1,-1,1),(1,1,-1),(-1,1,-1),(1,-1,-1),(-1,-1,-1)]];exposure=[]
for name,g in groups.items():
 rest=[t for t in tris if not set(t)<=g['set']];tree=BVHTree.FromPolygons(vs,rest,all_triangles=True);seen=total=0;by=[0]*len(dirs);witness=[];ring_seen=collections.Counter()
 for fi,t in enumerate(g['faces']):
  x,y,z=[vs[i]for i in t]
  for i in range(5):
   for j in range(5-i):
    p=(x*i+y*j+z*(4-i-j))/4;vis=False;total+=1
    for di,dr in enumerate(dirs):
     if tree.ray_cast(p+dr*eps,dr,span*3)[0] is None:by[di]+=1;vis=True
    if vis:
     seen+=1
     if len(witness)<2:witness.append({'triangle':fi,'position':list(p)})
 exposure.append({'tag':name,'sample_count':total,'exposed_count':seen,'diagnostic_fraction':seen/total,'exposed_by_direction':by,'witnesses':witness})
extras={}
if a=='arborea':
 pods=[(n,g)for n,g in groups.items()if n.startswith('pod_')];extras['pods']=len(pods);extras['unit_cues']=[]
 for n,g in pods:
  rings=[g['ids'][i:i+6]for i in range(0,len(g['ids']),6)];depths=[max(vs[i].y for i in ring)-min(vs[i].y for i in ring)for ring in rings];peaks=[i for i in range(1,len(depths)-1)if depths[i]>depths[i-1]and depths[i]>depths[i+1]]
  extras['unit_cues'].append({'pod':n,'actual_ring_depths_m':depths,'local_depth_peaks':peaks,'count':len(peaks)})
if a=='swartpuntia':
 extras['vane_count']=sum(n.startswith('vane_')for n in groups);extras['module_count_by_vane']={str(i):sum(n.startswith('module_'+str(i)+'_')for n in groups)for i in range(3)};extras['axis_nodes']=sum(n.startswith('axis_node_')for n in groups);extras['vane_radial_directions']=[];extras['module_depths_local']=[]
 for i in range(3):
  pts=[vs[j]for j in groups['vane_'+str(i)]['ids']];center=sum(pts,Vector())/len(pts);extras['vane_radial_directions'].append(math.degrees(math.atan2(center.y,center.x)))
 for n,g in groups.items():
  if n.startswith('module_'):
   sector=int(n.split('_')[1]);normal=Vector((-math.sin(2*math.pi*sector/3),math.cos(2*math.pi*sector/3),0));dots=[vs[j].dot(normal)for j in g['ids']];extras['module_depths_local'].append({'tag':n,'normal_min_m':min(dots),'normal_max_m':max(dots),'vane_halfthickness_m':.0009})
if a=='coronacollina':
 cone=next(r for r in records if r['tag']=='rimmed_cone');extras['cone']=cone['bounds_blender_m'];extras['spicules']=[]
 for n,g in groups.items():
  if n.startswith('spicule_'):
   pts=[vs[i]for i in g['ids']];p=sum(pts[:6],Vector())/6;q=sum(pts[6:],Vector())/6;diam=max((x-y).length for x in pts[:6]for y in pts[:6]);extras['spicules'].append({'tag':n,'axis_length_m':(q-p).length,'diameter_m':diam,'actual_endpoints':[list(p),list(q)],'downward':q.z<p.z})
 coneids=groups['rimmed_cone']['ids'];rim=[vs[i]for i in coneids[49:73]];zs=[p.z for p in rim];extras['rim_peak_count']=sum(zs[i]>zs[i-1]+eps and zs[i]>zs[(i+1)%24]+eps for i in range(24));extras['recess_depth_m']=min(zs)-vs[coneids[-1]].z
if a=='echmatocrinus':
 extras['arm_count']=sum(n.startswith('arm_')for n in groups);extras['soft_processes_by_arm']={str(i):sum(n.startswith('soft_process_'+str(i)+'_')for n in groups)for i in range(8)};extras['integral_plate_cells']=132;ids=groups['integral_plated_body']['ids'];extras['actual_plate_center_relief_m']=[]
 for k in range(12):
  for j in range(11):
   cell=[k*11+j,k*11+(j+1)%11,(k+1)*11+(j+1)%11,(k+1)*11+j];center=sum((vs[ids[i]]for i in cell),Vector())/4;real=vs[ids[143+k*11+j]];extras['actual_plate_center_relief_m'].append((real-center).length)
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();em.calc_loop_triangles();counts={'authored_vertices':len(vs),'authored_polygons':len(me.polygons),'authored_triangles':len(tris),'evaluated_vertices':len(em.vertices),'evaluated_polygons':len(em.polygons),'evaluated_triangles':len(em.loop_triangles)};ev.to_mesh_clear();bpy.ops.object.select_all(action='DESELECT');o.select_set(True);opts=json.loads((B/'artifacts/metadata.json').read_text())['export_options'];bpy.ops.export_scene.gltf(filepath=str(D/'reexport.glb'),**opts)
r={'asset_id':a,'revision':rev,'started_at':start,'finished_at':now(),'pid':os.getpid(),'source_sha256':sha,'source_unchanged':H(src)==sha,'glb_sha256':H(B/'artifacts'/f'{a}.glb'),'reexport_sha256':H(D/'reexport.glb'),'reexport_identical':H(D/'reexport.glb')==H(B/'artifacts'/f'{a}.glb'),'object':o.name,'objects':[{'name':q.name,'type':q.type}for q in bpy.context.scene.objects],'transform':[list(x)for x in o.matrix_world],'counts':counts,'bounds_blender_m':bounds(vs),'components':records,'contacts':contacts,'global_exposure':exposure,'actual_feature_checks':extras,'method':'Fresh source open; original exact vertex groups and transformed geometry. Strict interior witnesses use nearest-surface exclusion plus three-ray parity, not AABB/tangency. Dense barycentric samples (15 per triangle) test all other original triangles in fourteen directions. No repair/resave or threshold gate. Original GLB separately audited.','gpu':'unknown','scene':'unknown'};(D/'source-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(a,'reexport',r['reexport_identical'],'contact failures',[c['child']for c in contacts if not c['true_solid_intersection']],'zero_exposed',[e['tag']for e in exposure if e['exposed_count']==0])
