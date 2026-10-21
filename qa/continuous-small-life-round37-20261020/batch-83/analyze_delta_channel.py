import sys,json,hashlib,datetime,collections,math
from pathlib import Path
sys.dont_write_bytecode=True;r=Path('/workspace/shared/lowpoly-batch83-20261020');o=Path(__file__).parent;sys.path.insert(0,str(r/'scripts'));from qa_glb import read_glb,accessor_values
p=r/'production/small-life-batch83/assets/wave-dominated-delta/r002/model.glb';d,b,_=read_glb(p);tris=[]
for m in d['meshes']:
 for pr in m['primitives']:
  if d['materials'][pr['material']]['name']!='water':continue
  pos=accessor_values(d,b,pr['attributes']['POSITION']);idx=[i[0] for i in accessor_values(d,b,pr['indices'])]
  for k in range(0,len(idx),3):tris.append([tuple(round(x,5) for x in pos[j]) for j in idx[k:k+3]])
edges=collections.defaultdict(list)
for i,t in enumerate(tris):
 for j in range(3):edges[tuple(sorted((t[j],t[(j+1)%3])))].append(i)
adj=collections.defaultdict(set)
for ts in edges.values():
 for a in ts:adj[a].update(ts)
remaining=set(range(len(tris)));components=[]
while remaining:
 seed=remaining.pop();todo=[seed];seen={seed}
 while todo:
  for b in adj[todo.pop()]:
   if b in remaining:remaining.remove(b);seen.add(b);todo.append(b)
 vs=[(x,-z,y) for j in seen for x,y,z in tris[j]]
 components.append({'triangle_count':len(seen),'bounds_blender_xyz':{'min':[min(v[i] for v in vs) for i in range(3)],'max':[max(v[i] for v in vs) for i in range(3)]},'triangles':sorted(seen)})
components.sort(key=lambda c:-c['triangle_count']);report={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'glb_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'Triangle adjacency by exact rounded position edge in the water material. This checks rendered water-region connectivity; it is not itself proof of geological process or overall closed mesh topology. Positions converted glTF XYZ to Blender X,-Z,Y.','water_triangles':len(tris),'edge_connected_components':len(components),'components':components};(o/'wave-dominated-delta/water-connectivity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps([{k:v for k,v in c.items() if k!='triangles'} for c in components],indent=2))
