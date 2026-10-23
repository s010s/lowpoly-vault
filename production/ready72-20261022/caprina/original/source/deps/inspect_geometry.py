# SPDX-License-Identifier: MIT
"""Inspect closed-valve topology and nonadjacent self intersections in source."""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy, bmesh
from mathutils.bvhtree import BVHTree
ap=argparse.ArgumentParser(); ap.add_argument('blend',type=Path); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(a.blend))
parts=[]; trees=[]
for o in bpy.data.objects:
 if o.type!='MESH': continue
 m=o.data;m.calc_loop_triangles(); ts=[tuple(t.vertices) for t in m.loop_triangles]; vs=[o.matrix_world@v.co for v in m.vertices]
 bm=bmesh.new();bm.from_mesh(m)
 volume=bm.calc_volume(signed=True); boundary=sum(e.is_boundary for e in bm.edges); nonman=sum(not e.is_manifold for e in bm.edges)
 tree=BVHTree.FromPolygons(vs,ts,all_triangles=True,epsilon=0.0)
 pairs=sorted({tuple(sorted((i,j))) for i,j in tree.overlap(tree) if i!=j and not set(ts[i])&set(ts[j])})
 parts.append({'name':o.name,'closed_manifold':nonman==0,'boundary_edges':boundary,'nonmanifold_edges':nonman,'signed_volume_m3':volume,'nonadjacent_self_intersection_pairs':len(pairs),'self_intersection_first_pairs':pairs[:20],'vertices':len(vs),'triangles':len(ts)})
 trees.append((o.name,tree));bm.free()
contacts=[]
for i,(ni,ti) in enumerate(trees):
 for nj,tj in trees[i+1:]: contacts.append({'parts':[ni,nj],'intersecting_triangle_pairs':len(ti.overlap(tj)),'interpretation':'Bounded valve contact overlap is permitted, not a printable fused union.'})
r={'status':'PASS' if all(p['closed_manifold'] and p['signed_volume_m3']>0 and not p['nonadjacent_self_intersection_pairs'] for p in parts) else 'FAIL','claim_scope':'Topological closure, positive oriented signed volume and Blender BVH nonadjacent self-intersection screening. Inter-valve contact is separately reported. No factual identity or beauty claim.','blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),'parts':parts,'contacts':contacts,'non_asset_object_types':[o.type for o in bpy.data.objects if o.type not in ['MESH','EMPTY']]}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
