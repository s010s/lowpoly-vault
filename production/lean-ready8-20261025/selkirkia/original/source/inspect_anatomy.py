# SPDX-License-Identifier: MIT
"""Focused exact-GLB topology and attachment evidence, not a scientific or visual verdict."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:];glb=Path(args[0]);out=Path(args[1]);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb.resolve()))
objs={o.name:o for o in bpy.context.scene.objects if o.type=='MESH'}
def geom(o):
 o.data.calc_loop_triangles();return [o.matrix_world@v.co for v in o.data.vertices],[tuple(t.vertices) for t in o.data.loop_triangles]
def bv(o):v,f=geom(o);return BVHTree.FromPolygons(v,f,all_triangles=True)
def comps(o):
 vs,fs=geom(o);adj=[set() for _ in vs]
 for f in fs:
  for a in f:
   adj[a].update(f)
 remaining=set(range(len(vs)));cc=[]
 while remaining:
  start=next(iter(remaining));seen={start};stack=[start];remaining.remove(start)
  while stack:
   for k in adj[stack.pop()]:
    if k in remaining:remaining.remove(k);seen.add(k);stack.append(k)
  cc.append(seen)
 return vs,fs,cc
def count_components(o):return len(comps(o)[2])
tube=objs['organic-annulated-tube-open-at-both-ends'];body=objs['continuous-trunk-and-extended-introvert'];tv,tf=geom(tube);bb=bv(body);tb=bv(tube)
# Welding exact-position normals/material splits restores topological vertices without geometric modification.
def topology(o):
 vs,fs=geom(o);unique={};mp=[]
 for v in vs:
  key=tuple(round(x,10) for x in v)
  if key not in unique:unique[key]=len(unique)
  mp.append(unique[key])
 edges={};adj=[set() for _ in unique]
 for f in fs:
  f=[mp[x] for x in f]
  for i in range(3):
   a,b=f[i],f[(i+1)%3];e=tuple(sorted((a,b)));edges[e]=edges.get(e,0)+1;adj[a].add(b);adj[b].add(a)
 rem=set(range(len(unique)));ncomp=0
 while rem:
  ncomp+=1;stack=[rem.pop()]
  while stack:
   for j in adj[stack.pop()]:
    if j in rem:rem.remove(j);stack.append(j)
 return {'welded_vertices':len(unique),'edges':len(edges),'triangles':len(fs),'euler_characteristic':len(unique)-len(edges)+len(fs),'boundary_edges':sum(n==1 for n in edges.values()),'nonmanifold_edges':sum(n!=2 for n in edges.values()),'connected_components':ncomp}
# The axis is within both apertures even across the gentle 0.5 mm bend. Tube-only ray must pass entirely through.
ymin=min(v.y for v in tv);ymax=max(v.y for v in tv);zmid=(min(v.z for v in tv)+max(v.z for v in tv))/2
rays=[]
for x,zoff in [(0,0),(.00030,0),(-.00030,0),(0,.00030),(0,-.00030)]:
 for side in [-1,1]:
  p=Vector((x,ymin-.001 if side==1 else ymax+.001,zmid+zoff));d=Vector((0,side,0));hit=tb.ray_cast(p,d,ymax-ymin+.002)
  rays.append({'origin_m':list(p),'direction':list(d),'tube_surface_hit':hit[0] is not None})
# Weld disconnected flat-normal vertices for scalid components before triangle overlap testing.
def attachment(name):
 o=objs[name];vs,fs=geom(o);unique={};mp=[];verts=[]
 for v in vs:
  key=tuple(round(x,10) for x in v)
  if key not in unique:unique[key]=len(verts);verts.append(v)
  mp.append(unique[key])
 faces=[tuple(mp[x] for x in f) for f in fs];adj=[set() for _ in verts]
 for f in faces:
  for k in f:adj[k].update(f)
 remaining=set(range(len(verts)));result=[]
 while remaining:
  comp={remaining.pop()};stack=list(comp)
  while stack:
   for j in adj[stack.pop()]:
    if j in remaining:remaining.remove(j);comp.add(j);stack.append(j)
  ff=[f for f in faces if f[0] in comp];ob=BVHTree.FromPolygons(verts,ff,all_triangles=True);pairs=ob.overlap(bb);result.append(len(pairs))
 return {'components':len(result),'components_intersecting_body':sum(n>0 for n in result),'minimum_triangle_overlap_pairs':min(result),'all_attached_by_intersection':all(n>0 for n in result)}
tt=topology(tube);bt=topology(body);sc=attachment('introvert-short-radial-scalids');pa=attachment('small-anterior-trunk-papillae');clash=len(tb.overlap(bb))
checks={'tube_single_closed_wall_component':tt['connected_components']==1 and tt['boundary_edges']==0 and tt['nonmanifold_edges']==0,'tube_through_lumen_topology':tt['euler_characteristic']==0,'both_apertures_unblocked_by_tube_mesh':not any(r['tube_surface_hit'] for r in rays),'trunk_introvert_one_continuous_surface':bt['connected_components']==1,'scalids_all_rooted':sc['all_attached_by_intersection'],'papillae_all_rooted':pa['all_attached_by_intersection'],'tube_does_not_intersect_soft_body':clash==0}
d={'status':'PASS' if all(checks.values()) else 'FAIL','glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'source':'Fresh import of exact GLB','blender_version':bpy.app.version_string,'checks':checks,'tube':tt,'body':bt,'tube_only_axial_rays':rays,'scalids':sc,'papillae':pa,'tube_body_triangle_overlap_pairs':clash,'scope':'Topological and geometric evidence only. Tube-only rays intentionally ignore the resident trunk. Euler characteristic 0 plus no boundary edges is consistent with one open-ended hollow wall. Does not establish species accuracy, visual quality or GPU/world acceptance.'}
out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d));assert all(checks.values()),checks
