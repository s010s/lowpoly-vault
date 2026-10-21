import json,math,struct,collections,datetime,hashlib,pathlib,itertools
import numpy as np
O=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-independent-qa-20261021');S=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-20261020');A=S/'production/batch91-archaeopteris-repair/archaeopteris/r002';data=json.loads((O/'source-geometry.json').read_text());new=data['new']['parts'][0];old=data['old']['parts'][0]
assert len(data['new']['parts'])==len(data['old']['parts'])==1
assert old['edges']==new['edges'] and old['polygons']==new['polygons'] and old['material_indices']==new['material_indices']
v=np.array(new['vertices'],dtype=float);ov=np.array(old['vertices'],dtype=float)
adj=[set() for _ in v]
for a,b in new['edges']:adj[a].add(b);adj[b].add(a)
unseen=set(range(len(v)));comps=[]
while unseen:
 a=min(unseen);q=[a];ids={a};unseen.remove(a)
 while q:
  for b in adj[q.pop()]:
   if b in unseen:unseen.remove(b);ids.add(b);q.append(b)
 ids=sorted(ids);comps.append({'first':ids[0],'ids':ids,'count':len(ids)})
counts=collections.Counter(c['count'] for c in comps);assert counts=={120:1,24:6,18:12,15:48,8:576,16:3},counts
# Independently decode actual GLB float32 positions and indexed triangles; no maker measurement helper.
glb=(A/'artifacts/archaeopteris.glb').read_bytes();assert glb[:4]==b'glTF';jlen,jtype=struct.unpack_from('<II',glb,12);assert jtype==0x4e4f534a;doc=json.loads(glb[20:20+jlen]);blen,btype=struct.unpack_from('<II',glb,20+jlen);assert btype==0x004e4942;binary=glb[28+jlen:28+jlen+blen]
assert len(doc['meshes'])==1 and len(doc['nodes'])==2 and doc['scenes'][doc.get('scene',0)]['nodes']==[1]
assert doc['nodes'][1]['children']==[0] and doc['nodes'][0]['mesh']==0
assert all(not any(k in n for k in ['matrix','rotation','translation','scale']) for n in doc['nodes'])

def accessor(i):
 a=doc['accessors'][i];assert 'sparse' not in a;bv=doc['bufferViews'][a['bufferView']];fmt,size={5126:('f',4),5123:('H',2),5125:('I',4)}[a['componentType']];n={'SCALAR':1,'VEC3':3}[a['type']];off=bv.get('byteOffset',0)+a.get('byteOffset',0);stride=bv.get('byteStride',n*size)
 return [struct.unpack_from('<'+fmt*n,binary,off+i*stride) for i in range(a['count'])]
pts=[];keymap={};faces=[]
for primitive in doc['meshes'][0]['primitives']:
 assert primitive.get('mode',4)==4;pos=accessor(primitive['attributes']['POSITION']);idx=[a[0] for a in accessor(primitive['indices'])];local=[]
 for x,z,ny in pos:
  key=(primitive['material'],(x,-ny,z))
  if key not in keymap:keymap[key]=len(pts);pts.append(key)
  local.append(keymap[key])
 faces.extend(tuple(local[k] for k in idx[i:i+3]) for i in range(0,len(idx),3))
gadj=[set() for _ in pts]
for a,b,c in faces:
 gadj[a].update([b,c]);gadj[b].update([a,c]);gadj[c].update([a,b])
unseen=set(range(len(pts)));gcomps=[]
while unseen:
 a=min(unseen);q=[a];ids={a};unseen.remove(a)
 while q:
  for b in gadj[q.pop()]:
   if b in unseen:unseen.remove(b);ids.add(b);q.append(b)
 gcomps.append(ids)
assert collections.Counter(len(c) for c in gcomps)==counts
coords={p for mat,p in pts};assert all(tuple(p) in coords for p in v)
# For every source component, identify the matching exact GLB connected component, not just a nearby point.
gsets={frozenset(pts[i][1] for i in c) for c in gcomps};assert all(frozenset(tuple(v[i]) for i in c['ids']) in gsets for c in comps)

def point_bounds(p):
 low=[];high=[]
 for x in p:
  f=np.float32(x);below=float(np.nextafter(f,np.float32(-np.inf)));above=float(np.nextafter(f,np.float32(np.inf)));low.append((below+x)/2);high.append((above+x)/2)
 return np.array(low),np.array(high)
def dist_bounds(a,b):
 al,ah=point_bounds(a);bl,bh=point_bounds(b);lo=al-bh;hi=ah-bl;mn=np.where(lo>0,lo,np.where(hi<0,-hi,0));mx=np.maximum(abs(lo),abs(hi));return [float(np.linalg.norm(mn)),float(np.linalg.norm(mx))]
def length(a,b):return math.dist(a,b)
def closest_centerline(p,cs):
 best=(float('inf'),None,None)
 for i in range(len(cs)-1):
  a,b=cs[i],cs[i+1];t=float(np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1));d=float(np.linalg.norm(p-(a+t*(b-a))))
  if d<best[0]:best=(d,i,t)
 return best
sprays=[c for c in comps if c['count']==15];spray_centers=[v[c['ids']].reshape(3,5,3).mean(axis=1) for c in sprays]
leaves=[]
for c in [c for c in comps if c['count']==8]:
 pp=v[c['ids']];op=ov[c['ids']];L=length(pp[0],pp[3]);maxL=max(length(x,y) for x,y in itertools.combinations(pp,2));width=length(pp[2],pp[4]);thick=length(pp[6],pp[7]);li=len(leaves);pair=(li//2)%6;nom=.23-(.23-.15)*pair/5
 nearest=min((closest_centerline(pp[0],cs)[0],j,closest_centerline(pp[0],cs)[1],closest_centerline(pp[0],cs)[2]) for j,cs in enumerate(spray_centers))
 interval=dist_bounds(pp[0],pp[3]);wi=dist_bounds(pp[2],pp[4]);ti=dist_bounds(pp[6],pp[7]);ratio_interval=[wi[0]/interval[1],wi[1]/interval[0]]
 oldL=length(op[0],op[3]);direction_delta=float(np.linalg.norm((pp[3]-pp[0])/L-(op[3]-op[0])/oldL))
 leaves.append({'source_first_vertex':c['first'],'nominal_length_m':nom,'final_glb_base_tip_m':L,'final_glb_max_chord_m':maxL,'final_width_m':width,'width_ratio':width/L,'final_thickness_m':thick,'single_float32_storage_length_interval_m':interval,'nominal_within_single_storage_interval':interval[0]<=nom<=interval[1],'width_ratio_storage_interval':ratio_interval,'thickness_storage_interval_m':ti,'nearest_spray':nearest[1],'base_axis_distance_m':nearest[0],'closest_segment':nearest[2],'closest_fraction':nearest[3],'old_base_tip_m':oldL,'direction_unit_vector_delta':direction_delta})
leafids={i for c in comps if c['count']==8 for i in c['ids']};nonleaf=[i for i in range(len(v)) if i not in leafids];ratio=float(np.sum(v[nonleaf]*ov[nonleaf])/np.sum(ov[nonleaf]**2));res=np.linalg.norm(v[nonleaf]-ratio*ov[nonleaf],axis=1);deltas=np.linalg.norm(v[nonleaf]-ov[nonleaf],axis=1)
# Actual attachment containment: robust solid-angle winding test at tube centers/bases, on source points proven GLB-identical.
triangles={}
for c in comps:
 if c['count']==8:continue
 idset=set(c['ids']);fs=[p for p in new['polygons'] if p[0] in idset];ts=[]
 for p in fs:
  for j in range(1,len(p)-1):ts.append([v[p[0]],v[p[j]],v[p[j+1]]])
 triangles[c['first']]=np.array(ts)
def winding(point,component):
 t=triangles[component['first']]-point;aa,bb,cc=t[:,0],t[:,1],t[:,2];la=np.linalg.norm(aa,axis=1);lb=np.linalg.norm(bb,axis=1);lc=np.linalg.norm(cc,axis=1);numer=np.einsum('ij,ij->i',aa,np.cross(bb,cc));den=la*lb*lc+np.einsum('ij,ij->i',aa,bb)*lc+np.einsum('ij,ij->i',bb,cc)*la+np.einsum('ij,ij->i',cc,aa)*lb;return float(abs(np.sum(2*np.arctan2(numer,den))/(4*math.pi)))
trunk=next(c for c in comps if c['count']==120);limbs=[c for c in comps if c['count']==18];roots=[c for c in comps if c['count']==24];scars=[c for c in comps if c['count']==16]
attachments=[]
for c,l in zip([c for c in comps if c['count']==8],leaves):
 w=winding(v[c['ids'][0]],sprays[l['nearest_spray']]);attachments.append({'kind':'leaf_to_spray','first':c['first'],'host_first':sprays[l['nearest_spray']]['first'],'winding':w})
for c in sprays:
 center=v[c['ids'][:5]].mean(axis=0);ws=[winding(center,h) for h in limbs];j=int(np.argmax(ws));attachments.append({'kind':'spray_to_limb','first':c['first'],'host_first':limbs[j]['first'],'winding':ws[j]})
for kind,cc in [('root_to_trunk',roots),('limb_to_trunk',limbs)]:
 for c in cc:
  center=v[c['ids'][:6]].mean(axis=0);attachments.append({'kind':kind,'first':c['first'],'host_first':trunk['first'],'winding':winding(center,trunk)})
for c in scars:
 center=v[c['ids']].mean(axis=0);attachments.append({'kind':'scar_to_trunk','first':c['first'],'host_first':trunk['first'],'winding':winding(center,trunk)})
# Winding number one certifies those component bases lie inside the actual closed host volume, not merely touching an axis.
attachment_fails=[x for x in attachments if not abs(x['winding']-1)<1e-5]
summary={k:[min(x[k] for x in leaves),max(x[k] for x in leaves)] for k in ['final_glb_base_tip_m','final_glb_max_chord_m','final_width_m','width_ratio','final_thickness_m','base_axis_distance_m','old_base_tip_m','direction_unit_vector_delta']}
summary.update({'leaves':len(leaves),'raw_strict_length_outside_count':sum(not .15<=x['final_glb_base_tip_m']<=.23 for x in leaves),'nominal_not_in_single_storage_interval':sum(not x['nominal_within_single_storage_interval'] for x in leaves),'width_062_not_in_storage_interval':sum(not x['width_ratio_storage_interval'][0]<=.62<=x['width_ratio_storage_interval'][1] for x in leaves),'thickness_009_not_in_storage_interval':sum(not x['thickness_storage_interval_m'][0]<=.009<=x['thickness_storage_interval_m'][1] for x in leaves),'old_true_overlength_count':sum(x['old_base_tip_m']>.230001 for x in leaves),'max_nominal_length_deviation_m':max(abs(x['final_glb_base_tip_m']-x['nominal_length_m']) for x in leaves),'skeleton_scale_ratio_best_fit':ratio,'skeleton_nonleaf_max_displacement_m':float(max(deltas)),'uniform_skeleton_scale_fit_max_residual_m':float(max(res)),'bounds_blender_m':{'min':v.min(axis=0).tolist(),'max':v.max(axis=0).tolist(),'size':np.ptp(v,axis=0).tolist()},'actual_attachment_checks':len(attachments),'attachment_failures':attachment_fails})
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'final_glb_sha256':hashlib.sha256(glb).hexdigest(),'source_sha256':data['new']['sha256'],'method':'Independent binary GLB FLOAT accessor decoding with identity-node verification; exact material-position welding and triangle connected-component recovery; all source topological components map one-to-one to actual GLB point sets. Double-precision distances measured on final exported coordinates. All 28 pairwise chords checked per blade. Numeric intervals are derived from each actual coordinate adjacent float32 midpoint, not an arbitrary global epsilon. Host containment uses signed solid angle winding of real closed triangulated component geometry.','nodes':doc['nodes'],'source_and_glb_component_counts':dict(counts),'source_and_glb_points_identical':True,'old_new_topology_and_material_indices_identical':True,'exported_triangle_count':len(faces),'summary':summary,'leaves':leaves,'attachments':attachments}
(O/'geometry.report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(summary,indent=2))
