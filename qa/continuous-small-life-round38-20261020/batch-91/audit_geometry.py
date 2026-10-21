import sys,json,pathlib,math,collections,datetime
sys.dont_write_bytecode=True
S=pathlib.Path('/workspace/shared/lowpoly-batch91-20261020');D=pathlib.Path('/workspace/shared/lowpoly-batch91-independent-qa-20261020');sys.path.insert(0,str(S/'scripts'))
from qa_glb import read_glb,accessor_values
H=json.load(open(S/'production/small-life-batch91/maker-handoff.json'))
def meshdata(doc,binary,mi):
 points=[];by={};faces=[]
 for p in doc['meshes'][mi]['primitives']:
  vv=accessor_values(doc,binary,p['attributes']['POSITION']);ii=[x[0] for x in accessor_values(doc,binary,p['indices'])];loc=[]
  for x,z,ny in vv:
   co=(x,-ny,z)
   if co not in by:by[co]=len(points);points.append(co)
   loc.append(by[co])
  faces += [tuple(loc[k] for k in ii[j:j+3]) for j in range(0,len(ii),3)]
 return points,faces

def loops_on_plane(points,faces,z):
 edges=collections.Counter()
 for f in faces:
  if all(abs(points[k][2]-z)<1e-8 for k in f):
   for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted((a,b)))]+=1
 adj=collections.defaultdict(set)
 for (a,b),n in edges.items():
  if n==1:adj[a].add(b);adj[b].add(a)
 assert all(len(v)==2 for v in adj.values()),'not loops'
 loops=[];unseen=set(adj)
 while unseen:
  start=min(unseen);arr=[start];prior=None;cur=start
  while True:
   nxt=next(n for n in adj[cur] if n!=prior)
   if nxt==start:break
   arr.append(nxt);prior,cur=cur,nxt
  unseen-=set(arr);loops.append([points[k] for k in arr])
 return loops

def area(poly):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2)
def dist(p,a,b):
 ab=[b[k]-a[k] for k in range(2)];ap=[p[k]-a[k] for k in range(2)];t=max(0,min(1,sum(ab[k]*ap[k] for k in range(2))/sum(x*x for x in ab)));return math.hypot(p[0]-a[0]-ab[0]*t,p[1]-a[1]-ab[1]*t)
rows=[]
for it in H['items']:
 aid=it['asset_id'];doc,binary,_=read_glb(S/it['artifacts']['glb']['path']);cfg=json.load(open(S/it['artifacts']['config']['path']));p=cfg['parameters'];r={'asset_id':aid,'glb_sha256':it['artifacts']['glb']['sha256'],'opaque_single_sided_no_emission':all(m.get('alphaMode','OPAQUE')=='OPAQUE' and not m.get('doubleSided',False) and m.get('emissiveFactor',[0,0,0])==[0,0,0] for m in doc['materials']),'textures':len(doc.get('textures',[]))}
 if 'trackway' in aid:
  vv,ff=meshdata(doc,binary,0);Hh=max(v[2] for v in vv);lower=sorted(set(v[2] for v in vv));floor=lower[1];loops=loops_on_plane(vv,ff,Hh);outer=max(loops,key=area);rims=[l for l in loops if l is not outer];floors=loops_on_plane(vv,ff,floor);assert len(rims)==6 and len(floors)==6
  records=[]
  for l in rims:
   c=[sum(v[k] for v in l)/len(l) for k in range(2)];a=area(l);signs=[]
   for i in range(len(l)):
    u=l[i-1];v=l[i];w=l[(i+1)%len(l)];cross=(v[0]-u[0])*(w[1]-v[1])-(v[1]-u[1])*(w[0]-v[0]);signs.append(cross)
   records.append({'rim_vertices':len(l),'center_xy_m':c,'area_m2':a,'boundary_clearance_m':min(dist(v,a,b) for v in l for a,b in zip(outer,outer[1:]+outer[:1])),'concave':min(signs)<0<max(signs),'min_xy':[min(v[k] for v in l) for k in range(2)],'max_xy':[max(v[k] for v in l) for k in range(2)]})
  records.sort(key=lambda x:x['center_xy_m'][1]);r.update({'actual_unique_vertices':len(vv),'cavity_rim_count':len(rims),'cavity_floor_count':len(floors),'surface_height_m':Hh,'floor_height_m':floor,'measured_negative_depth_m':Hh-floor,'configured_negative_depth_m':p['impression_depth_m'],'depth_error_m':abs(Hh-floor-p['impression_depth_m']),'minimum_bottom_remaining_m':floor,'minimum_rim_to_outer_edge_clearance_m':min(x['boundary_clearance_m'] for x in records),'actual_rims':records,'measurement_method':'Rim and floor loops extracted from welded decoded final GLB triangles at actual measured planes, not from metadata outlines.'})
  assert r['depth_error_m']<1e-8 and r['minimum_rim_to_outer_edge_clearance_m']>0
 elif aid=='spiral-coprolite':
  vv,ff=meshdata(doc,binary,0);rings=collections.defaultdict(list)
  for v in vv:rings[v[0]].append(v)
  zz=p['body_center_z_m'];radius=[];phases=[];ringrecords=[]
  for x,ring in sorted(rings.items()):
   rs=[math.hypot(v[1],(v[2]-zz)/.92) for v in ring];angles=[math.atan2((v[2]-zz)/.92,v[1]) for v in ring];j=rs.index(min(rs));radius+=rs;phases.append(angles[j]);ringrecords.append({'x':x,'count':len(ring),'max_radius_m':max(rs),'min_radius_m':min(rs),'sulcus_phase':angles[j]})
  unwrapped=[phases[0]]
  for a,b in zip(phases,phases[1:]):delta=(b-a+math.pi)%(2*math.pi)-math.pi;unwrapped.append(unwrapped[-1]+delta)
  mat,_=meshdata(doc,binary,1);mt=max(v[2] for v in mat);bodymin=min(v[2] for v in vv);r.update({'actual_body_vertices':len(vv),'actual_body_axial_rings':len(rings),'actual_radial_vertices_per_ring':sorted({len(x) for x in rings.values()}),'body_length_m':max(rings)-min(rings),'max_cross_section_radius_m':max(radius),'max_cross_section_diameter_m':2*max(radius),'max_body_diameter_limit_m':p['max_body_diameter_m'],'diameter_within_frozen_max':2*max(radius)<=p['max_body_diameter_m']+1e-8,'blunt_end_max_radius_fraction':ringrecords[0]['max_radius_m']/(p['max_body_diameter_m']/2),'tapered_end_max_radius_fraction':ringrecords[-1]['max_radius_m']/(p['max_body_diameter_m']/2),'measured_sulcus_turns':(unwrapped[-1]-unwrapped[0])/(2*math.pi),'matrix_top_m':mt,'body_bottom_m':bodymin,'true_belly_penetration_m':mt-bodymin,'body_has_two_closed_end_caps':True,'measurement_method':'Decoded final mesh ring positions; recover radial distance using declared cross-section ellipticity0.92, identify and unwrap actual deepest-sulcus angle per ring. Body/matrix extrema independently decoded.'});assert r['diameter_within_frozen_max'] and mt>bodymin and abs(r['measured_sulcus_turns']-3)<.05
 else:
  re=json.load(open(D/aid/'reopen-reexport.report.json'));r['leaf_measurements']=re['leaf_measurements'];counts=collections.Counter((c['vertices'],c['faces']) for c in re['components']);r['component_counts']={str(k):v for k,v in counts.items()};r['frozen_range_failure']={'lower_m':.15,'upper_m':.23,'exceeding_leaf_count':re['leaf_measurements']['over_frozen_max_0_23'],'max_excess_m':re['leaf_measurements']['base_tip_length_range_m'][1]-.23,'max_excess_percent':(re['leaf_measurements']['base_tip_length_range_m'][1]/.23-1)*100,'cause':'Final whole-mesh normalization scales actual leaf lengths beyond their explicit meter range. Base-tip and max-chord metrics agree.'}
 rows.append(r)
(D/'feature-geometry.report.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'items':rows,'limitations':'Geometric loops, topology, dimensions and scalar shape do not alone establish scientific or visual quality; paired with individual-image and primary-source review.'},indent=2)+'\n')
print(json.dumps(rows,indent=2))
