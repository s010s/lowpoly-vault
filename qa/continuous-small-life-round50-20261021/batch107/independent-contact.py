import bpy,sys,json,pathlib,hashlib,datetime,math,collections,itertools,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
src=pathlib.Path(sys.argv[sys.argv.index('--')+1]);out=pathlib.Path(sys.argv[sys.argv.index('--')+2]);bpy.ops.wm.open_mainfile(filepath=str(src));ct=json.loads(bpy.data.texts['BATCH107_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];bpy.context.view_layer.update();v=[o.matrix_world@x.co for x in o.data.vertices];o.data.calc_loop_triangles();tri=[tuple(x.vertices) for x in o.data.loop_triangles];C={c['tag']:c for c in ct['components']};faces={k:[t for t in tri if set(t)<=set(c['vertices'])] for k,c in C.items()};trees={k:BVHTree.FromPolygons(v,ts,all_triangles=True) for k,ts in faces.items()};whole=BVHTree.FromPolygons(v,tri,all_triangles=True);extent=max(max(x[k] for x in v)-min(x[k] for x in v) for k in range(3));eps=extent*1e-8;dirs=[Vector(a).normalized() for a in itertools.product([-1,0,1],repeat=3) if a!=(0,0,0)];expo=[];contacts=[];plate_contact=[];apertures=[]
for k,c in C.items():
 own=faces[k];rest=[t for t in tri if not set(t)<=set(c['vertices'])];allother=BVHTree.FromPolygons(v,rest,all_triangles=True);counts=[0]*len(dirs);n=0
 for t in own:
  p=sum((v[i] for i in t),Vector())/3;n+=1
  for z,d in enumerate(dirs):
   if allother.ray_cast(p+d*eps,d,extent*3)[0] is None:counts[z]+=1
 expo.append({'component':k,'samples':n,'visible_by_26_directions':counts,'any_exposed':max(counts)>0})
 if c.get('parent'):
  target=trees[c['parent']];pairs=trees[k].overlap(target);ds=[]
  for i in c['base_vertices']:
   p,n,_,dist=target.find_nearest(v[i]);ds.append((v[i]-p).dot(n))
  contacts.append({'component':k,'parent':c['parent'],'triangle_intersections':len(pairs),'minimum_base_signed_distance_m':min(ds),'contact':bool(pairs) or min(ds)<=0})
for f in ct['integrated_features']:
 if f['kind']!='geometric_plate':continue
 c=C[f['component']];parent=c.get('parent');ids=f['vertices'];fs=[t for t in faces[f['component']] if set(t)<=set(ids)];local=BVHTree.FromPolygons(v,fs,all_triangles=True)
 if parent:
  pairs=local.overlap(trees[parent]);ds=[]
  for i in ids[:len(ids)//2]:
   p,n,_,dist=trees[parent].find_nearest(v[i]);ds.append((v[i]-p).dot(n))
  upper=[v[i] for i in ids[len(ids)//2:]];mid=sum(upper,Vector())/len(upper);normal=(upper[1]-upper[0]).cross(upper[2]-upper[0]).normalized();hit=whole.ray_cast(mid+normal*eps,normal,extent*3)
  plate_contact.append({'tag':f['tag'],'parent':parent,'intersections':len(pairs),'minimum_base_signed_distance_m':min(ds),'contact':bool(pairs) or min(ds)<=0,'upper_center_outward_unobstructed':hit[0] is None,'upper_center_occluder_distance_m':hit[3]})
# Cup aperture center and seven floor samples. Direction derives from actual nested ring centroids, not world Z.
for k in ['mouth','periproct']:
 if k not in C:continue
 ids=C[k]['vertices'];assert len(ids)==48
 rim=[v[i] for i in ids[24:36]];floor=[v[i] for i in ids[36:48]];rm=sum(rim,Vector())/12;fm=sum(floor,Vector())/12;n=(rm-fm).normalized();points=[fm]+[fm+(p-fm)*.6 for p in floor[::2]];hits=[]
 for p in points:
  loc,normal,idx,distance=whole.ray_cast(p+n*eps,n,extent*3);occluding=None
  if idx is not None:
   t=set(tri[idx]);occluding=[name for name,c in C.items() if t<=set(c['vertices'])]
  hits.append({'ray_start_m':list(p),'unobstructed':loc is None,'distance_m':distance,'occluding_component':occluding})
 apertures.append({'component':k,'local_normal':list(n),'recess_depth_m':(rm-fm).length,'samples':hits,'qualification':'Opaque recessed low-poly opening, not an anatomical internal cavity claim. A hidden floor can reveal host intersection; visible recess judged with exact final pixels.'})
report={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'pid':os.getpid(),'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'directions':[list(d) for d in dirs],'origin_epsilon_m':eps,'contacts':contacts,'physical_plate_contacts':plate_contact,'global_exposure':expo,'aperture_floor_rays':apertures,'uncontacted_plates':[p['tag'] for p in plate_contact if not p['contact']],'completely_hidden_components':[p['component'] for p in expo if not p['any_exposed']],'source_modified':False,'limitations':'Ray samples cannot certify all continuous surfaces or GPU rendering. Nearest signed distances are diagnostic; triangle intersection independently supports contact. Hidden plate centers under overlay features are not by themselves defects.'};out.write_text(json.dumps(report,indent=2)+'\n');print(src.stem,'detached plates',report['uncontacted_plates'],'hidden components',report['completely_hidden_components'],'apertures',[(x['component'],[y['unobstructed'] for y in x['samples']]) for x in apertures])
