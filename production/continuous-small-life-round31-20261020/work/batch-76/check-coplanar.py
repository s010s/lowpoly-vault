# SPDX-License-Identifier: MIT
"""Read-only saved-source positive-area coplanar triangle overlap diagnostic, not full intersection/scene acceptance."""
import bpy,sys,pathlib,json,hashlib,datetime,math,collections
b=pathlib.Path(sys.argv[-1]);bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'))
groups=collections.defaultdict(list);count=0;scale=max(json.loads((b/'metrics.json').read_text())['measured_blender_xyz_m']);tol=max(1e-11,scale*1e-8);area_eps=max(1e-18,scale*scale*1e-12)
for o in bpy.data.collections['EXPORT'].all_objects:
 if o.type!='MESH':continue
 mesh=o.data;mesh.calc_loop_triangles()
 for ti,t in enumerate(mesh.loop_triangles):
  vs=[o.matrix_world@mesh.vertices[i].co for i in t.vertices];n=(vs[1]-vs[0]).cross(vs[2]-vs[0])
  if n.length<area_eps:continue
  n.normalize();axis=max(range(3),key=lambda k:abs(n[k]))
  if n[axis]<0:n=-n
  d=n.dot(vs[0]);key=tuple(round(v/1e-6) for v in n)+(round(d/tol),);inds=[k for k in range(3) if k!=axis];p=[(v[inds[0]],v[inds[1]]) for v in vs]
  cross=lambda a,c,e:(c[0]-a[0])*(e[1]-a[1])-(c[1]-a[1])*(e[0]-a[0])
  if cross(*p)<0:p.reverse()
  box=(min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p));groups[key].append((o.name,ti,set(t.vertices),p,box));count+=1

def clip(poly,edge):
 a,c=edge;res=[]
 def side(p):return (c[0]-a[0])*(p[1]-a[1])-(c[1]-a[1])*(p[0]-a[0])
 for i,p in enumerate(poly):
  q=poly[(i+1)%len(poly)];u=side(p);v=side(q)
  if u>=0:res.append(p)
  if (u>=0)!=(v>=0):
   t=u/(u-v);res.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
 return res
hits=[];tested=0
for group in groups.values():
 for i,a in enumerate(group):
  for c in group[i+1:]:
   if a[0]==c[0] and len(a[2]&c[2])>=2:continue
   A=a[4];B=c[4]
   if min(A[2],B[2])-max(A[0],B[0])<=tol or min(A[3],B[3])-max(A[1],B[1])<=tol:continue
   tested+=1;poly=a[3]
   for k in range(3):
    if not poly:break
    poly=clip(poly,(c[3][k],c[3][(k+1)%3]))
   area=abs(sum(poly[k][0]*poly[(k+1)%len(poly)][1]-poly[(k+1)%len(poly)][0]*poly[k][1] for k in range(len(poly))))/2 if len(poly)>=3 else 0
   if area>area_eps:hits.append({'a':[a[0],a[1]],'b':[c[0],c[1]],'projected_area_m2':area})
d={'kind':'physical-coplanar-positive-area-triangle-overlap-diagnostic','status':'pass' if not hits else 'review','source_sha256':hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'triangles':count,'coplanar_aabb_candidate_pairs':tested,'positive_area_overlaps':len(hits),'hits':hits[:30],'linear_tolerance_m':tol,'area_epsilon_m2':area_eps,'limits':'Saved-source numerical near-exact coplanar overlap diagnostic only; not general noncoplanar intersection detection, GPU or website/scene proof.'};(b/'coplanar-overlap.report.json').write_text(json.dumps(d,indent=2)+'\n');print('COPLANAR',b,len(hits))
