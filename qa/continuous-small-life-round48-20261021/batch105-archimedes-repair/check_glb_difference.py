import sys,pathlib,hashlib,json,collections
sys.dont_write_bytecode=True
R=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-repair-20261021');Q=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-independent-qa-20261021');D=R/'production/small-life-batch105-archimedes-repair/r002';O=R/'production/small-life-batch105/archimedes/r001';sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb,accessor_values,IDENTITY,node_matrix,matmul,transform,audit_glb
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def get(p):
 d,bin,_=read_glb(p);ts=[]
 def walk(i,m):
  n=d['nodes'][i];m=matmul(m,node_matrix(n))
  if 'mesh' in n:
   for prim in d['meshes'][n['mesh']]['primitives']:
    pos=accessor_values(d,bin,prim['attributes']['POSITION']);ix=[x[0] for x in accessor_values(d,bin,prim['indices'])]
    for j in range(0,len(ix),3):ts.append((prim.get('material'),tuple(transform(m,pos[k]) for k in ix[j:j+3])))
  for c in n.get('children',[]):walk(c,m)
 for n in d['scenes'][d.get('scene',0)]['nodes']:walk(n,IDENTITY)
 return d,ts
a,ta=get(O/'artifacts/archimedes.glb');b,tb=get(D/'artifacts/archimedes.glb');assert len(ta)==len(tb)==9396;changed=[i for i,(x,y) in enumerate(zip(ta,tb)) if x!=y];assert len(changed)==144;assert a['materials']==b['materials'];assert a['nodes']==b['nodes'];assert not b.get('textures') and all(not m.get('doubleSided',False) and m.get('alphaMode','OPAQUE')=='OPAQUE' for m in b['materials'])
for i in changed:
 x,y=ta[i],tb[i];ps=x[1]+y[1];assert x[0]==y[0];assert all(abs(p[0])<.0021 and abs(p[2])<.0021 for p in ps);assert all(p[1]<.0021 for p in ps) or all(.033<p[1]<.036 for p in ps)
# Original exact exported coordinate edges, no tolerance welding or normal repair.
ed=collections.defaultdict(list);adj=collections.defaultdict(set)
for i,(_,t) in enumerate(tb):
 for x,y in zip(t,t[1:]+t[:1]):ed[tuple(sorted((x,y)))].append((i,x,y))
for refs in ed.values():
 for i,_,_ in refs:adj[i].update(j for j,_,_ in refs if i!=j)
todo=set(range(len(tb)));comps=[]
while todo:
 seen={todo.pop()};stack=list(seen)
 while stack:
  n=stack.pop();ns=adj[n]&todo;todo-=ns;seen|=ns;stack+=list(ns)
 edges={e:v for e,v in ed.items() if v[0][0] in seen};bad=[e for e,v in edges.items() if len(v)!=2 or v[0][1:]!=v[1][1:][::-1]]
 def vol(t):
  x,y,z=t;return (x[0]*(y[1]*z[2]-y[2]*z[1])+x[1]*(y[2]*z[0]-y[0]*z[2])+x[2]*(y[0]*z[1]-y[1]*z[0]))/6
 volume=sum(vol(tb[i][1]) for i in seen);assert not bad and volume>0;comps.append({'triangles':len(seen),'exact_coordinate_edges':len(edges),'bad_edges':len(bad),'signed_volume_m3':volume})
assert sorted(c['triangles'] for c in comps)==[1936,7460]
aud=audit_glb(D/'artifacts/archimedes.glb',14000,6,30);assert aud['status']=='pass';orig=audit_glb(O/'artifacts/archimedes.glb',14000,6,30);assert orig['bounds_m']==aud['bounds_m']
report={'status':'pass','original_glb_sha256':sha(O/'artifacts/archimedes.glb'),'repaired_glb_sha256':sha(D/'artifacts/archimedes.glb'),'triangles':len(tb),'changed_triangle_count':len(changed),'unchanged_triangle_count':len(tb)-len(changed),'changed_triangle_indices':changed,'changed_triangles_only_at_axial_endpoints':True,'materials_and_node_transforms_unchanged':True,'no_textures_alpha_masks_or_double_sided_materials':True,'bounds_unchanged':True,'original_export_topology':comps,'static_audit':aud}
(Q/'glb-independent.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS GLB:144 endpoint triangles differ,9252 unchanged;2 original outward closed components')
