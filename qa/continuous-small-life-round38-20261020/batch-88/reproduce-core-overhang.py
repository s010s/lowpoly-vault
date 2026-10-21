# Read-only minimal independent reproduction of Phycosiphon cross-profile spill.
import json,math,numpy as np
from pathlib import Path
Q=Path('/workspace/shared/lowpoly-batch88-independent-qa-20261020');R=Path('/workspace/shared/lowpoly-batch88-20261020');d=R/'production/batch88/assets/phycosiphon-looping-trace/r002';obj=next(iter(json.load(open(Q/'phycosiphon-looping-trace/mesh-measure-input.json')).values()));V=np.array(obj['vertices']);paths=[np.array(p) for p in json.load(open(d/'geometry-semantics.json'))['centerline_paths']];segments=np.array([(p[i],p[i+1]) for p in paths for i in range(len(p)-1)])
def near(p):
 a=segments[:,0];v=segments[:,1]-a;t=np.clip(np.sum((p-a)*v,axis=1)/np.sum(v*v,axis=1),0,1);return float(np.min(np.linalg.norm(p-a-v*t[:,None],axis=1)))
def background(v):
 host=.0063+.00012*math.sin(v[0]/.08*7)*math.sin(v[1]/.065*5); mantle=.0006*math.sqrt(max(0,1-(near(v[:2])/.00145)**2));return host,mantle
p=paths[0];j=10;c=p[j];t=p[j+1]-p[j-1];t/=np.linalg.norm(t);n=np.array([-t[1],t[0]])
results=[]
for offset in [-.0007,-.0006,-.0005,.0006,.0007,.0008,.0009,.001,.0011,.0013]:
 xy=c+n*offset
 for fi,(face,mi) in enumerate(zip(obj['faces'],obj['material_indices'])):
  if obj['materials'][mi]=='cut':continue
  found=False
  for k in range(1,len(face)-1):
   ids=[face[0],face[k],face[k+1]];vv=V[ids];A=np.array([vv[1,:2]-vv[0,:2],vv[2,:2]-vv[0,:2]]).T
   if abs(np.linalg.det(A))<1e-16:continue
   weights=np.linalg.solve(A,xy-vv[0,:2]);a,b=weights
   if a>=-1e-7 and b>=-1e-7 and a+b<=1.0000001:
    weights=np.array([1-a-b,a,b]);host=np.array([background(v)[0] for v in vv]);mantle=np.array([background(v)[1] for v in vv]);core=vv[:,2]-host-mantle
    results.append({'offset_along_local_normal_m':offset,'sample_xy_m':xy.tolist(),'nearest_entire_centerline_distance_m':near(xy),'face_index':fi,'triangle_vertex_indices':ids,'triangle_material':obj['materials'][mi],'barycentric_weights':weights.tolist(),'actual_surface_z_m':float(weights@vv[:,2]),'interpolated_host_z_m':float(weights@host),'interpolated_mantle_contribution_m':float(weights@mantle),'interpolated_core_contribution_m':float(weights@core),'triangle_vertices':[{'vertex_index':int(idx),'xyz_m':v.tolist(),'nearest_centerline_m':near(v[:2]),'host_z_m':float(h),'mantle_contribution_m':float(m),'core_contribution_m':float(q)} for idx,v,h,m,q in zip(ids,vv,host,mantle,core)]});found=True;break
  if found:break
report={'asset_id':'phycosiphon-looping-trace','revision':'r002','glb_sha256':'2e8a66f5d7201bccc2cb43f37c2c5fccbdf60ed1f5f451d9b8798593cba9cc4a','path_zero_based':0,'sample_zero_based':10,'center_xy_m':c.tolist(),'unit_tangent_xy':t.tolist(),'unit_normal_xy':n.tolist(),'method':'Measure the exact authored triangulated surface, not nominal rc. Host and mantle contribution are evaluated at each actual triangle vertex using the retained profile, then linearly interpolated with those same triangle weights. The remaining positive height is the actual core contribution. Entire-polyline nearest-distance rules out a chord/projection shortcut. This is not a material assignment measurement.','samples':results}
(Q/'phycosiphon-looping-trace/core-overhang-minimal-repro.json').write_text(json.dumps(report,indent=2)+'\n');print('center',c,'normal',n);print([(x['offset_along_local_normal_m'],x['nearest_entire_centerline_distance_m'],x['interpolated_core_contribution_m'],x['face_index']) for x in results])
