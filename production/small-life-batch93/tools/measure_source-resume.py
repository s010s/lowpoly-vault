#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only source reopen plus authored/evaluated counts; no source mutation."""
import sys,json,hashlib,datetime,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from check_source_export import main
main()
import bpy
args=sys.argv[sys.argv.index('--')+1:];source=Path(args[args.index('--source')+1]);out=Path(args[args.index('--output')+1]);parts=[];dg=bpy.context.evaluated_depsgraph_get()
for o in bpy.data.objects:
 if o.type!='MESH':continue
 o.data.calc_loop_triangles();ev=o.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles();parts.append({'name':o.name,'authored_vertices':len(o.data.vertices),'authored_polygons':len(o.data.polygons),'authored_triangles':len(o.data.loop_triangles),'evaluated_vertices':len(me.vertices),'evaluated_polygons':len(me.polygons),'evaluated_triangles':len(me.loop_triangles),'modifier_count':len(o.modifiers)});ev.to_mesh_clear()
r={'schema_version':1,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'blender':bpy.app.version_string,'parts':parts,'totals':{k:sum(x[k] for x in parts) for k in ['authored_vertices','authored_polygons','authored_triangles','evaluated_vertices','evaluated_polygons','evaluated_triangles']},'source_saved':False}
with (out.parent/'authored-evaluated-counts.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
# Mesh-connected-component measurements derive directly from freshly reopened vertex/face data.
components=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 adj=[set() for _ in o.data.vertices]
 for e in o.data.edges:
  a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 unseen=set(range(len(adj)));count=0
 while unseen:
  start=next(iter(unseen));stack=[start];seen={start};unseen.remove(start)
  while stack:
   for q in adj[stack.pop()]:
    if q in unseen:unseen.remove(q);seen.add(q);stack.append(q)
  points=[o.matrix_world@o.data.vertices[i].co for i in seen];lo=[min(v[k] for v in points) for k in range(3)];hi=[max(v[k] for v in points) for k in range(3)];polys=[p for p in o.data.polygons if p.vertices[0] in seen];mats=sorted({o.data.materials[p.material_index].name for p in polys});components.append({'object':o.name,'component':count,'vertices':len(seen),'polygons':len(polys),'materials':mats,'bounds_blender_m':{'min':lo,'max':hi,'size':[hi[k]-lo[k] for k in range(3)]}});count+=1
rr={'schema_version':1,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'method':'Actual freshly reopened source connected vertex-edge components, not config counts; intersecting branch junction components intentionally remain separate.','components':components}
with (out.parent/'frozen-feature-measurements.json').open('x') as f:json.dump(rr,f,indent=2);f.write('\n')

# Actual mesh topology and retained design metadata, separate from inferred biological counts.
import bmesh
topo=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data);topo.append({'object':o.name,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'euler_characteristic':len(bm.verts)-len(bm.edges)+len(bm.faces),'boundary_edges':sum(1 for e in bm.edges if len(e.link_faces)==1),'nonmanifold_edges':sum(1 for e in bm.edges if len(e.link_faces)!=2),'design_metadata_not_independent_measurements':{k:o[k] for k in o.keys() if k.startswith('design_')}});bm.free()
with (out.parent/'actual-mesh-topology.json').open('x') as f:json.dump({'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'objects':topo,'diplopora_interpretation':'Single connected closed shell with axial lumen has genus1;96 through-wall channels add96 handles, genus97, Euler characteristic-192. Confirm actual counts, do not infer solely from config.'},f,indent=2);f.write('\n')
# Attachment preflight on actual reopened world-space vertices, never inferred config endpoints.
from mathutils import Vector
from mathutils.bvhtree import BVHTree
records=[]
for o in bpy.data.objects:
 if o.type!='MESH':continue
 adj=[set() for _ in o.data.vertices]
 for e in o.data.edges:
  a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 unseen=set(range(len(adj)));cs=[]
 while unseen:
  first=min(unseen);stack=[first];seen={first};unseen.remove(first)
  while stack:
   for k in adj[stack.pop()]:
    if k in unseen:unseen.remove(k);seen.add(k);stack.append(k)
  ids=sorted(seen);v=[o.matrix_world@o.data.vertices[i].co for i in ids];imap={q:i for i,q in enumerate(ids)};fs=[tuple(imap[k] for k in p.vertices) for p in o.data.polygons if p.vertices[0] in seen];mats={p.material_index for p in o.data.polygons if p.vertices[0] in seen};cs.append({'first':first,'v':v,'f':fs,'mat':mats,'bvh':BVHTree.FromPolygons(v,fs)})
 def inside(c,p):
  # Three non-axis directions avoid edge coincidences. Majority parity is recorded.
  votes=[]
  for dr in [(1,.193,.311),(.217,1,.473),(.319,.181,1)]:
   dr=Vector(dr).normalized();q=p.copy();hits=0
   for _ in range(20):
    loc,normal,idx,dist=c['bvh'].ray_cast(q,dr,100)
    if loc is None:break
    hits+=1;q=loc+dr*1e-7
   votes.append(hits%2==1)
  return sum(votes)>=2
 if 'quill-crown' in o.name:
  stempart=next(c for c in cs if len(c['v'])==288);leaves=[c for c in cs if c['mat'] <= {2,3}];rows=[]
  for c in leaves:
   p=c['v'][0];rows.append({'first_vertex':c['first'],'base_world_m':list(p),'base_inside_stem':inside(stempart,p),'distance_to_stem_surface_m':stempart['bvh'].find_nearest(p)[3]})
  records.append({'kind':'all_actual_nathorstiana_leaf_bases','leaf_components':len(leaves),'stem_top_z_m':max(v.z for v in stempart['v']),'all_embedded':all(r['base_inside_stem'] for r in rows),'leaves':rows})
 if 'dichotomous-crown' in o.name:
  woody=[c for c in cs if c['mat']=={0} and len(c['v']) in [30,28,24]];rows=[]
  for c in woody:
   if len(c['v'])==30:continue
   n=len(c['v'])//4;joint=sum(c['v'][n:2*n],Vector())/n
   choices=[]
   for other in woody:
    if other is c:continue
    ns=10 if len(other['v'])==30 else len(other['v'])//4;tip=sum(other['v'][-ns:],Vector())/ns;choices.append(((tip-joint).length,other))
   distance,parent=min(choices,key=lambda x:x[0]);ninside=sum(inside(parent,v) for v in c['v'][:n]);rows.append({'child_first_vertex':c['first'],'parent_first_vertex':parent['first'],'joint_endpoint_distance_m':distance,'buried_base_ring_vertices':n,'vertices_inside_parent':ninside})
  records.append({'kind':'all_actual_omphalophloios_branch_bases','woody_components':len(woody),'branch_joints':len(rows),'all_joint_centres_match_parent_tips':all(r['joint_endpoint_distance_m']<1e-6 for r in rows),'all_buried_base_rings_inside_parent':all(r['vertices_inside_parent']==r['buried_base_ring_vertices'] for r in rows),'joints':rows})
with (out.parent/'attachment-measurements.json').open('x') as f:json.dump({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'method':'Actual freshly reopened world-space mesh components; three-direction ray parity for buried bases and Euclidean parent-tip/joint-centre distances. This does not replace final visual inspection.','records':records},f,indent=2);f.write('\n')
