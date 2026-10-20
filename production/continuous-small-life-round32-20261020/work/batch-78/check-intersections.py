# SPDX-License-Identifier: MIT
"""Actual saved-source nonadjacent triangle intersections + positive-area near-coplanar overlaps."""
import bpy,sys,pathlib,json,hashlib,datetime,math
from mathutils.bvhtree import BVHTree
from mathutils.geometry import intersect_ray_tri
b=pathlib.Path(sys.argv[-1]);bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'));scale=max(json.loads((b/'metrics.json').read_text())['measured_blender_xyz_m']);tol=max(1e-10,scale*2e-6);verts=[];tris=[];owners=[]
for o in bpy.data.collections['EXPORT'].all_objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();base=len(verts);verts.extend(o.matrix_world@v.co for v in m.vertices)
 for t in m.loop_triangles:tris.append(tuple(base+i for i in t.vertices));owners.append(o.name)
bvh=BVHTree.FromPolygons(verts,tris,all_triangles=True,epsilon=tol);pairs=bvh.overlap(bvh);hits=[];near=[];tested=0

def area_clip(A,B):
 def cross(a,c,p):return (c[0]-a[0])*(p[1]-a[1])-(c[1]-a[1])*(p[0]-a[0])
 if cross(*A)<0:A=A[::-1]
 if cross(*B)<0:B=B[::-1]
 poly=A
 for k in range(3):
  out=[];a=B[k];c=B[(k+1)%3]
  for j,p in enumerate(poly):
   q=poly[(j+1)%len(poly)];u=cross(a,c,p);v=cross(a,c,q)
   if u>=0:out.append(p)
   if (u>=0)!=(v>=0):
    t=u/(u-v);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  poly=out
  if not poly:return 0
 return abs(sum(poly[j][0]*poly[(j+1)%len(poly)][1]-poly[(j+1)%len(poly)][0]*poly[j][1] for j in range(len(poly))))/2
for ia,ib in pairs:
 if ia>=ib or set(tris[ia])&set(tris[ib]):continue
 A=[verts[i] for i in tris[ia]];B=[verts[i] for i in tris[ib]];na=(A[1]-A[0]).cross(A[2]-A[0]).normalized();nb=(B[1]-B[0]).cross(B[2]-B[0]).normalized();tested+=1
 if abs(na.dot(nb))>1-1e-7 and max(abs(na.dot(p-A[0])) for p in B)<tol:
  axis=max(range(3),key=lambda i:abs(na[i]));inds=[i for i in range(3) if i!=axis];area=area_clip([tuple(p[i] for i in inds) for p in A],[tuple(p[i] for i in inds) for p in B])
  if area>scale*scale*1e-11:near.append({'a':ia,'b':ib,'owners':[owners[ia],owners[ib]],'area_m2':area})
  continue
 found=False
 for P,Q in [(A,B),(B,A)]:
  for j,p in enumerate(P):
   v=P[(j+1)%3]-p;length=v.length
   if length<tol:continue
   hit=intersect_ray_tri(Q[0],Q[1],Q[2],v.normalized(),p,True)
   if hit is not None and tol<(hit-p).length<length-tol:found=True
 if found:hits.append({'a':ia,'b':ib,'owners':[owners[ia],owners[ib]]})
d={'kind':'saved-source-triangle-intersection-and-near-coplanar-positive-area','status':'pass' if not hits and not near else 'review','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),'triangles':len(tris),'bvh_candidate_pairs':len(pairs),'nonadjacent_pairs_tested':tested,'noncoplanar_intersections':len(hits),'near_coplanar_positive_area_overlaps':len(near),'linear_tolerance_m':tol,'hits':hits[:40],'near_coplanar_hits':near[:40],'limits':'Numerical saved-source geometry diagnostic; skips shared-vertex pairs and is not a GPU/composed-scene/website proof. Actual final individual pixels also inspected.'};(b/'intersection-diagnostic.report.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
