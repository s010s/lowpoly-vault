import bpy,json,sys,pathlib,hashlib,collections,math,datetime
from mathutils import Vector
from mathutils.bvhtree import BVHTree
O=pathlib.Path(__file__).parent;R=pathlib.Path('/workspace/shared/lowpoly-batch108-20261021');a=sys.argv[-1];src=R/'production/batch-108'/a/'r002/artifacts'/f'{a}.blend';bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);ct=json.loads(bpy.data.texts['BATCH108_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];o.data.calc_loop_triangles();V=[o.matrix_world@v.co for v in o.data.vertices];T=[tuple(t.vertices) for t in o.data.loop_triangles];D={c['tag']:c for c in ct['components']};F={}
for c in D.values():
 ids=set(c['vertices']);F[c['tag']]=[t for t in T if all(i in ids for i in t)]
tr={k:BVHTree.FromPolygons(V,f,all_triangles=True) for k,f in F.items()};extent=max(max(v[k] for v in V)-min(v[k] for v in V) for k in range(3));eps=extent*2**-21;dirs=[Vector(x).normalized() for x in [(1,.371,.217),(.163,1,.493),(.719,.283,1)]]
def inside(tree,p):
 q,n,f,d=tree.find_nearest(p)
 if d is None or d<=eps:return False
 for direction in dirs:
  cur=p.copy();n=0
  for _ in range(512):
   q=tree.ray_cast(cur,direction,extent*4)[0]
   if q is None:break
   n+=1;cur=q+direction*eps*8
  if not n%2:return False
 return True
prior=json.loads((O/a/'fresh-source-inspection.json').read_text());targets={c['tag']:[p['part'] for p in c['parts'] if p['contact_witness'] is None] for c in prior['components'] if D[c['tag']].get('parent')};out=[]
for tag,wanted in targets.items():
 if not wanted:continue
 fs=F[tag];adj=collections.defaultdict(set);byv=collections.defaultdict(list)
 for j,t in enumerate(fs):
  for v in t:byv[v].append(j)
 for refs in byv.values():
  for j in refs:adj[j].update(refs)
 seen=set();groups=[]
 for j in range(len(fs)):
  if j in seen:continue
  stack=[j];seen.add(j);g=[]
  while stack:
   k=stack.pop();g.append(k)
   for n in adj[k]:
    if n not in seen:seen.add(n);stack.append(n)
  groups.append(g)
 for part in wanted:
  fs2=[fs[j] for j in groups[part]];ids=set(i for t in fs2 for i in t);own=BVHTree.FromPolygons(V,fs2,all_triangles=True);parent=tr[D[tag]['parent']];cc=sum((V[i] for i in ids),Vector())/len(ids);points=[]
  for i in ids:
   for f in [.0001,.001,.005,.01,.05,.2,.5]:points.append(V[i]*(1-f)+cc*f)
  for t in fs2:
   x,y,z=[V[i] for i in t];n=(y-x).cross(z-x).normalized();step=min((x-y).length,(y-z).length,(x-z).length)
   for bary in [(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6)]:
    c=x*bary[0]+y*bary[1]+z*bary[2]
    for frac in [.0001,.0005,.001,.005,.01,.05,.2,.45]:points.append(c-n*step*frac)
  witness=next((q for q in points if inside(parent,q) and inside(own,q)),None);signed=[]
  for i in ids:
   q,n,_,dist=parent.find_nearest(V[i]);signed.append((V[i]-q).dot(n))
  peer=[]
  if witness is None:
   for other,tree in tr.items():
    if other in [tag,D[tag]['parent']]:continue
    pairs=own.overlap(tree)
    if pairs:peer.append({'tag':other,'intersecting_triangle_pairs':len(pairs)})
  out.append(dict(component=tag,part=part,parent=D[tag]['parent'],witness=list(witness) if witness is not None else None,parent_triangle_intersections=len(own.overlap(parent)),signed_vertices_min=min(signed),signed_vertices_max=max(signed),other_intersecting_components=peer,actual_vertices=list(ids)))
r=dict(asset=a,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=out,remaining_without_parent_witness=sum(x['witness'] is None for x in out),method='Denser inward barycentric and vertex-to-centroid samples preserve strict boundary exclusion. Diagnostic only. All original failed sampling reports retained.')
(O/a/'dense-contact-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(a,'remaining',r['remaining_without_parent_witness'],'of',len(out))
