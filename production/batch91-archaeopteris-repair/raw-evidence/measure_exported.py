import json,pathlib,sys,math,collections,hashlib,datetime
W=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-20261020');P=W/'production/batch91-archaeopteris-repair';D=P/'archaeopteris/r002';sys.path.insert(0,str(W/'scripts'));from qa_glb import read_glb,accessor_values
f=D/'artifacts/archaeopteris.glb';d,b,_=read_glb(f);assert len(d['meshes'])==1
pts=[];by={};faces=[]
for prim in d['meshes'][0]['primitives']:
 vv=accessor_values(d,b,prim['attributes']['POSITION']);ii=[x[0] for x in accessor_values(d,b,prim['indices'])];local=[]
 for x,z,ny in vv:
  p=(x,-ny,z)
  if p not in by:by[p]=len(pts);pts.append(p)
  local.append(by[p])
 faces += [tuple(local[k] for k in ii[j:j+3]) for j in range(0,len(ii),3)]
adj=[set() for _ in pts]
for face in faces:
 for a,c in zip(face,face[1:]+face[:1]):adj[a].add(c);adj[c].add(a)
unseen=set(range(len(pts)));comps=[]
while unseen:
 i=min(unseen);todo=[i];seen={i};unseen.remove(i)
 while todo:
  for q in adj[todo.pop()]:
   if q in unseen:unseen.remove(q);seen.add(q);todo.append(q)
 pp=[pts[i] for i in seen];comp={'vertices':len(pp)}
 if len(pp)==8:
  L,a,c=max((math.dist(a,c),a,c) for a in pp for c in pp);axis=[(c[k]-a[k])/L for k in range(3)];proj=lambda v:sum((v[k]-a[k])*axis[k] for k in range(3));width=max(math.dist(x,y) for x in pp for y in pp if abs(proj(x)-proj(y))<1e-6);thickness=min(math.dist(x,y) for x in pp for y in pp if x!=y)
  comp.update(length_m=L,width_m=width,width_to_length=width/L,thickness_m=thickness)
 comps.append(comp)
leaves=[x for x in comps if 'length_m' in x];assert len(leaves)==576
ulp=lambda x: 2**(math.frexp(abs(x))[1]-24) if x else 2**-149
max_ulp=max(ulp(x) for p in pts for x in p)
r={'schema_version':1,'asset_id':'archaeopteris','revision':'r002','measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'glb_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'nodes':d['nodes'],'method':'Decode final FLOAT POSITION accessors, restore Blender axes (x,-glbZ,glbY), weld only exact identical positions and traverse triangle-edge connected components. Leaf8-vertex components: longest pair gives base-tip/max chord; widest equal-axis pair gives blade width, shortest distinct pair gives peak thickness. Distances accumulated using Python double precision, not metadata parameter labels.','components_by_vertex_count':dict(collections.Counter(c['vertices'] for c in comps)),'unique_vertices':len(pts),'leaves':leaves,'summary':{k:[min(x[k] for x in leaves),max(x[k] for x in leaves)] for k in ['length_m','width_m','width_to_length','thickness_m']},'bounds_blender_m':{'min':[min(p[k] for p in pts) for k in range(3)],'max':[max(p[k] for p in pts) for k in range(3)]},'numerical_precision':{'coordinate_storage':'IEEE754 float32 from final GLB accessors','max_coordinate_ulp_m':max_ulp,'worst_case_distance_quantization_bound_m':math.sqrt(3)*max_ulp,'length_max_relative_error_vs_frozen_upper':(max(x['length_m'] for x in leaves)-.23)/.23,'length_min_relative_error_vs_frozen_lower':(min(x['length_m'] for x in leaves)-.15)/.15,'no_hard_threshold_change':True,'note':'No relaxation of original0.15–0.23m limits. Disclosed endpoint error is tens of nanometers due float32 coordinate quantization, unlike original8.4mm normalization error. Fresh independent reviewer decides acceptance.'}}
assert all(.15-1e-6 <= x['length_m'] <= .23+1e-6 for x in leaves)
assert all(abs(x['width_to_length']-.62)<1e-5 and abs(x['thickness_m']-.009)<1e-6 for x in leaves)
(D/'qa').mkdir(exist_ok=True)
(D/'qa/exported-leaf-dimensions.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:r[k] for k in ['components_by_vertex_count','summary','numerical_precision']},indent=2))
