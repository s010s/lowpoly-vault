# SPDX-License-Identifier: MIT
"""Necessary source geometry checks, not independent anatomical approval."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
root=Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(root/'model.blend'))
def shells(obj):
 mesh=obj.data;neighbors={v.index:set() for v in mesh.vertices}
 for edge in mesh.edges:
  a,b=edge.vertices;neighbors[a].add(b);neighbors[b].add(a)
 remaining=set(neighbors);trees=[]
 while remaining:
  pending=[remaining.pop()];component=set(pending)
  while pending:
   for nxt in neighbors[pending.pop()]:
    if nxt not in component:component.add(nxt);remaining.discard(nxt);pending.append(nxt)
  ids=sorted(component);remap={v:i for i,v in enumerate(ids)}
  polys=[tuple(remap[v] for v in poly.vertices) for poly in mesh.polygons if poly.vertices[0] in component]
  trees.append(BVHTree.FromPolygons([obj.matrix_world@mesh.vertices[i].co for i in ids],polys,all_triangles=False))
 return trees
def contains(tree,point):
 direction=Vector((.791,.413,.451)).normalized();p=point.copy();hits=0
 for n in range(200):
  hit,normal,idx,dist=tree.ray_cast(p,direction,10)
  if hit is None:return hits%2==1
  hits+=1;p=hit+direction*1e-7
 raise RuntimeError('Unbounded ray intersections')
upper=shells(bpy.data.objects['upper-hammerjaw']);lower=shells(bpy.data.objects['lower-hammerjaw-and-rami'])
teeth=bpy.data.objects['front-chisels-and-posterior-filter-mesh'];verts=teeth.data.vertices;failed=[];records=[]
for n in range(len(verts)//8):
 center=sum((verts[n*8+i].co for i in range(4)),Vector())/4
 trees=upper if n%2==0 else lower
 inside=any(contains(tree,center) for tree in trees)
 records.append({'tooth_index':n,'jaw':'upper' if n%2==0 else 'lower','root_center_m':list(center),'embedded':inside})
 if not inside:failed.append(n)
limbs=[o.name for o in bpy.data.objects if 'forelimb' in o.name or 'hindlimb' in o.name]
source_clean=not any(o.type in {'CAMERA','LIGHT'} for o in bpy.data.objects)
report={'kind':'maker-necessary-geometry-check','source_blend_sha256':hashlib.sha256((root/'model.blend').read_bytes()).hexdigest(),'source_glb_sha256':hashlib.sha256((root/'model.glb').read_bytes()).hexdigest(),'method':'Ray parity against each closed source jaw component, at each tooth base centroid; union-of-components containment. This proves centroid embedding, not a print-ready union or full visual acceptance.','teeth_count':len(records),'unembedded_tooth_root_centroids':failed,'teeth':records,'exactly_four_limbs':len(limbs)==4,'limb_names':limbs,'source_without_camera_or_lights':source_clean,'status':'PASS' if not failed and len(limbs)==4 and source_clean else 'FAIL'}
(root/'qa/evidence/anatomy-geometry.json').write_text(json.dumps(report,indent=2)+'\n');print('ANATOMY',report['status'],'unembedded roots',failed)
if report['status']!='PASS':raise RuntimeError('Necessary anatomy geometry failed')
