#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only original GLB face winding proof; no weld, normal recalculation or save."""
import collections,datetime,hashlib,json,pathlib,sys,math
R=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb,accessor_values,IDENTITY,node_matrix,matmul,transform
p=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);before=p.read_bytes();doc,binary,_=read_glb(p);tris=[];neg_normals=[]
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def walk(n,m):
 node=doc['nodes'][n];m=matmul(m,node_matrix(node))
 if 'mesh' in node:
  for prim in doc['meshes'][node['mesh']]['primitives']:
   assert prim.get('mode',4)==4
   pos=accessor_values(doc,binary,prim['attributes']['POSITION']);indices=[x[0] for x in accessor_values(doc,binary,prim['indices'])] if 'indices' in prim else list(range(len(pos)))
   # All delivery node transforms are rigid axis conversions. Geometric winding is checked in world space.
   for i in range(0,len(indices),3):tris.append(tuple(transform(m,pos[j]) for j in indices[i:i+3]))
 for c in node.get('children',[]):walk(c,m)
for n in doc['scenes'][doc.get('scene',0)]['nodes']:walk(n,IDENTITY)
edges=collections.defaultdict(list);adj=collections.defaultdict(set)
for i,t in enumerate(tris):
 for a,b in zip(t,t[1:]+t[:1]):
  key=tuple(sorted((a,b)));edges[key].append((i,1 if (a,b)==key else -1))
for e,refs in edges.items():
 for i,_ in refs:
  adj[i].update(j for j,_ in refs if j!=i)
seen=set();components=[]
for i in range(len(tris)):
 if i in seen:continue
 stack=[i];seen.add(i);ids=[]
 while stack:
  t=stack.pop();ids.append(t)
  for n in adj[t]:
   if n not in seen:seen.add(n);stack.append(n)
 local={k:v for k,v in edges.items() if any(t in set(ids) for t,_ in v)}
 boundary=sum(len(v)==1 for v in local.values());nonmanifold=sum(len(v)>2 for v in local.values());same=sum(len(v)==2 and v[0][1]==v[1][1] for v in local.values());volume=sum(dot(tris[t][0],cross(tris[t][1],tris[t][2]))/6 for t in ids)
 components.append(dict(triangle_count=len(ids),exact_position_boundary_edges=boundary,nonmanifold_edges=nonmanifold,same_direction_shared_edges=same,signed_volume_m3=volume,consistently_outward_closed=not(boundary or nonmanifold or same) and volume>0))
assert p.read_bytes()==before
report=dict(schema_version=1,status='pass' if all(c['consistently_outward_closed'] for c in components) else 'fail',glb_sha256=hashlib.sha256(before).hexdigest(),checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),triangle_count=len(tris),closed_component_count=len(components),components=components,source_or_glb_modified=False,weld_performed=False,normal_recalculation_performed=False,method='Decode exact original GLB indices/positions and world transforms. Match edges by bit-identical decoded coordinate tuples without tolerance or mesh edits, including material/flat-normal index seams. Each closed connected component must have exactly two oppositely directed incidents per edge and positive original signed volume. No repaired diagnostic copy is used as acceptance evidence.',limitations='Tests oriented original triangle topology, not inter-component intersections, biological reconstruction or screen-space readability.')
out.write_text(json.dumps(report,indent=2)+'\n');print(p.stem,report['status'],len(components),[(i,x) for i,x in enumerate(components) if not x['consistently_outward_closed']][:4])
