# SPDX-License-Identifier: MIT
"""Read-only saved-source connected solids and per-clast embed witness audit."""
import bpy,bmesh,json,sys,pathlib,hashlib,datetime
from mathutils import Vector
from mathutils.bvhtree import BVHTree
b=pathlib.Path(sys.argv[sys.argv.index('--')+1]);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sourcehash=H(b/'source.blend');bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'));metrics=json.load(open(b/'geometry-repair-report.json'))['component_metrics'];parts=[];host=None
for obj in bpy.data.collections['EXPORT'].all_objects:
 if obj.type!='MESH':continue
 me=obj.data;adj={i:set() for i in range(len(me.vertices))}
 for e in me.edges:a,c=e.vertices;adj[a].add(c);adj[c].add(a)
 unvisited=set(adj)
 while unvisited:
  stack=[next(iter(unvisited))];seen=set()
  while stack:
   i=stack.pop()
   if i in seen:continue
   seen.add(i);unvisited.discard(i);stack.extend(adj[i]-seen)
  indices=sorted(seen);remap={old:new for new,old in enumerate(indices)};vs=[me.vertices[i].co.copy() for i in indices];fs=[[remap[i] for i in p.vertices] for p in me.polygons if p.vertices[0] in seen];tree=BVHTree.FromPolygons(vs,fs,all_triangles=False);bm=bmesh.new();vv=[bm.verts.new(v) for v in vs]
  for f in fs:bm.faces.new([vv[i] for i in f])
  volume=abs(bm.calc_volume(signed=True));boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)];item={'object':obj.name,'tree':tree,'lo':lo,'hi':hi,'volume_m3':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'vertices':len(vs)}
  if 'coherent_angular_matrix' in obj.name:host=item
  else:parts.append(item)
assert host is not None

def inside(tree,p):
 direction=Vector((.833,.421,.356)).normalized();origin=p.copy();count=0
 for _ in range(200):
  hit,normal,face,distance=tree.ray_cast(origin,direction,100)
  if hit is None:break
  count+=1;origin=hit+direction*1e-5
 return bool(count%2)
witnesses=[]
for c in metrics:
 center=Vector(c['center']);normal=Vector(c['normal']);embed=center-normal*.060;matches=[]
 for i,p in enumerate(parts):
  if all(p['lo'][k]-1e-6<=center[k]<=p['hi'][k]+1e-6 for k in range(3)) and inside(p['tree'],center):matches.append(i)
 own=[i for i in matches if inside(parts[i]['tree'],embed)];hostinside=inside(host['tree'],embed)
 witnesses.append({'clast_id':c['id'],'original_center':c['center'],'inner_witness':list(embed),'witness_distance_inside_from_center_m':.060,'source_solid_matches':matches,'matching_solid_contains_inner_witness':own,'inner_witness_inside_host':hostinside,'attached_embed_witness_pass':len(own)>=1 and hostinside})
report={'kind':'read_only_source_embedding_and_solids','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':sourcehash,'glb_sha256':H(b/'model.glb'),'clast_solids':len(parts),'all_clast_solids_closed_nonzero':all(p['boundary_edges']==0 and p['nonmanifold_edges']==0 and p['volume_m3']>1e-10 for p in parts),'all_120_inner_embed_witnesses_pass':len(witnesses)==120 and all(x['attached_embed_witness_pass'] for x in witnesses),'clast_sum_source_volume_m3':sum(p['volume_m3'] for p in parts),'host_source_volume_m3':host['volume_m3'],'parts':[{k:v for k,v in p.items() if k!='tree'} for p in parts],'witnesses':witnesses,'limits':'Each inner point lies inside an actual source clast solid AND matrix host, proving an embedded connection rather than floating faces at those witnesses. Not general all-surface boolean union or website pixel clearance.'};assert H(b/'source.blend')==sourcehash;(b/'embedding-source-audit.json').write_text(json.dumps(report,indent=2)+'\n');print('Embedding',report['all_120_inner_embed_witnesses_pass'],'closed',report['all_clast_solids_closed_nonzero'],'solids',len(parts))
