# SPDX-License-Identifier: MIT
"""Read-only targeted exact-GLB near-parallel triangle overlap detector, not general collision QA."""
import sys,json,math,hashlib,pathlib,datetime
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/qa_glb.py').exists());sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,IDENTITY
sub=lambda a,b:tuple(x-y for x,y in zip(a,b));dot=lambda a,b:sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def area(p):return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2) if len(p)>2 else 0

def clip(subject,clipper):
 q=list(subject);sign=1 if sum(clipper[i][0]*clipper[(i+1)%len(clipper)][1]-clipper[(i+1)%len(clipper)][0]*clipper[i][1] for i in range(len(clipper)))>0 else -1
 for i,a in enumerate(clipper):
  b=clipper[(i+1)%len(clipper)];out=[]
  if not q:break
  def signed(p):return sign*((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))
  for j,p in enumerate(q):
   z=q[(j+1)%len(q)];dp=signed(p);dz=signed(z);insidep=dp>=-1e-12;insidez=dz>=-1e-12
   if insidep:out.append(p)
   if insidep!=insidez:
    t=dp/(dp-dz);out.append((p[0]+t*(z[0]-p[0]),p[1]+t*(z[1]-p[1])))
  q=out
 return q
path=pathlib.Path(sys.argv[1]);doc,bin,raw=read_glb(path);ts=[]
mesh_world={}
def visit(ni,parent):
 node=doc['nodes'][ni];world=matmul(parent,node_matrix(node))
 if 'mesh' in node:
  assert node['mesh'] not in mesh_world,'Instanced meshes require per-instance analysis'
  mesh_world[node['mesh']]=world
 for ch in node.get('children',[]):visit(ch,world)
for ni in doc['scenes'][doc.get('scene',0)]['nodes']:visit(ni,IDENTITY)
for mi,mesh in enumerate(doc['meshes']):
 for pi,p in enumerate(mesh['primitives']):
  pos=[transform(mesh_world[mi],v) for v in accessor_values(doc,bin,p['attributes']['POSITION'])];ix=[v[0] for v in accessor_values(doc,bin,p['indices'])] if 'indices' in p else list(range(len(pos)));mat=doc['materials'][p['material']]['name']
  parents=list(range(len(pos)));same={}
  def root(i):
   while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
   return i
  def join(a,b):parents[root(a)]=root(b)
  for vi,v in enumerate(pos):
   key=tuple(round(q,6) for q in v)
   if key in same:join(vi,same[key])
   else:same[key]=vi
  for k in range(0,len(ix),3):join(ix[k],ix[k+1]);join(ix[k+1],ix[k+2])
  compids={v:i for i,v in enumerate(sorted({root(q) for q in range(len(pos))}))}
  for k in range(0,len(ix),3):
   ps=[pos[j] for j in ix[k:k+3]];n=cross(sub(ps[1],ps[0]),sub(ps[2],ps[0]));norm=math.sqrt(dot(n,n))
   if norm<1e-12:continue
   n=tuple(v/norm for v in n);lo=tuple(min(p[a] for p in ps) for a in range(3));hi=tuple(max(p[a] for p in ps) for a in range(3));ts.append({'ps':ps,'n':n,'lo':lo,'hi':hi,'mesh':mi,'primitive':pi,'triangle':k//3,'material':mat,'component':compids[root(ix[k])],'center':tuple(sum(p[a] for p in ps)/3 for a in range(3))})
found=[];tol=1e-3;area_tol=1e-6
for i,a in enumerate(ts):
 for b in ts[i+1:]:
  if any(a['hi'][k]<b['lo'][k]-1e-4 or b['hi'][k]<a['lo'][k]-1e-4 for k in range(3)):continue
  if abs(dot(a['n'],b['n']))<1-1e-6:continue
  sep=max(abs(dot(a['n'],sub(p,a['ps'][0]))) for p in b['ps'])
  if sep>tol:continue
  drop=max(range(3),key=lambda k:abs(a['n'][k]));axes=[k for k in range(3) if k!=drop];ap=[tuple(p[k] for k in axes) for p in a['ps']];bp=[tuple(p[k] for k in axes) for p in b['ps']];overlap=area(clip(ap,bp))/abs(a['n'][drop])
  if overlap>area_tol:found.append({'a':{k:a[k] for k in ['mesh','primitive','triangle','material','component','center']},'b':{k:b[k] for k in ['mesh','primitive','triangle','material','component','center']},'overlap_area_m2':overlap,'plane_separation_m':sep})
report={'kind':'targeted_exact_glb_near_parallel_overlap','glb_sha256':hashlib.sha256(raw).hexdigest(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'triangles_checked':len(ts),'plane_tolerance_m':tol,'normal_dot_tolerance':1e-6,'area_tolerance_m2':area_tol,'coplanar_overlap_triangle_pairs':len(found),'maximum_overlap_area_m2':max((x['overlap_area_m2'] for x in found),default=0),'pairs':found,'limitations':'Near-parallel positive-projected-area witness only, including internal caps; not pixel root-cause proof, general intersection QA or visual approval. Scene hierarchy and mesh transforms applied; no instanced meshes permitted.'};pathlib.Path(sys.argv[2]).write_text(json.dumps(report,indent=2)+'\n');print(len(found),report['maximum_overlap_area_m2'])
