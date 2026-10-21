import sys,pathlib,json,hashlib,collections,datetime
R=pathlib.Path('/workspace/shared/lowpoly-batch108-20261021');O=pathlib.Path(__file__).parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb,accessor_values,IDENTITY,node_matrix,matmul,transform
for a in ['isorophus','eleutherocrinus','nucleocrinus','placocystites']:
 rev='r003' if a=='placocystites' else 'r002';p=R/'production/batch-108'/a/rev/'artifacts'/f'{a}.glb';doc,b,_=read_glb(p);T=[]
 def walk(n,m):
  o=doc['nodes'][n];m=matmul(m,node_matrix(o))
  if 'mesh' in o:
   for prim in doc['meshes'][o['mesh']]['primitives']:
    pos=accessor_values(doc,b,prim['attributes']['POSITION']);idx=[x[0] for x in accessor_values(doc,b,prim['indices'])];T.extend(tuple(transform(m,pos[j]) for j in idx[i:i+3]) for i in range(0,len(idx),3))
  for ch in o.get('children',[]):walk(ch,m)
 for n in doc['scenes'][doc.get('scene',0)]['nodes']:walk(n,IDENTITY)
 ed=collections.defaultdict(list);adj=collections.defaultdict(set)
 for i,t in enumerate(T):
  for x,y in zip(t,t[1:]+t[:1]):key=tuple(sorted((x,y)));ed[key].append((i,1 if (x,y)==key else -1))
 for refs in ed.values():
  for i,_ in refs:adj[i].update(j for j,_ in refs)
 seen=set();comps=[]
 def volume(t):
  x,y,z=t;return (x[0]*(y[1]*z[2]-y[2]*z[1])+x[1]*(y[2]*z[0]-y[0]*z[2])+x[2]*(y[0]*z[1]-y[1]*z[0]))/6
 for i in range(len(T)):
  if i in seen:continue
  todo=[i];seen.add(i);ids=[]
  while todo:
   j=todo.pop();ids.append(j)
   for k in adj[j]:
    if k not in seen:seen.add(k);todo.append(k)
  idsset=set(ids);edges=[v for v in ed.values() if v[0][0] in idsset];bad=sum(len(v)!=2 or v[0][1]==v[1][1] for v in edges);vol=sum(volume(T[j]) for j in ids);comps.append(dict(triangles=len(ids),bad_edges=bad,signed_volume=vol,pass_result=bad==0 and vol>0))
 r=dict(glb_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='pass' if all(x['pass_result'] for x in comps) else 'fail',triangles=len(T),components=comps,method='Original byte-decoded world triangle exact coordinate edge matching. No weld, tolerance, winding repair or normal recalculation.')
 (O/a/'fresh-original-glb-topology.json').write_text(json.dumps(r,indent=2)+'\n');print(a,r['status'],len(comps))
