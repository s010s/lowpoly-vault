import json,math,datetime
from pathlib import Path
import numpy as np
R=Path('/workspace/shared/lowpoly-batch88-20261020');Q=Path('/workspace/shared/lowpoly-batch88-independent-qa-20261020');J=lambda p:json.loads(p.read_text())
def nearest(p,segs):
 a,b=segs[:,0],segs[:,1];v=b-a;t=np.clip(np.sum((p-a)*v,axis=1)/np.sum(v*v,axis=1),0,1);return float(np.min(np.linalg.norm(p-(a+v*t[:,None]),axis=1)))
for aid,rev,w,h,base,outer in [('phycosiphon-looping-trace','r002',.08,.065,.0063,.00145)]:
 d=R/'production/batch88/assets'/aid/rev;obj=next(iter(J(Q/aid/'mesh-measure-input.json').values()));verts=np.array(obj['vertices']);mats=obj['materials'];sema=J(d/'geometry-semantics.json');paths=[np.array(x) for x in sema['centerline_paths']];segs=np.array([(p[i],p[i+1]) for p in paths for i in range(len(p)-1)])
 # Independent query of actual authored upper-surface triangle planes, using each source face, not a regenerated nominal primitive.
 tri=[];mi=[]
 for face,mat in zip(obj['faces'],obj['material_indices']):
  if mats[mat]=='cut':continue
  for j in range(1,len(face)-1):
   ix=[face[0],face[j],face[j+1]];v=verts[ix];det=np.linalg.det(np.array([v[1,:2]-v[0,:2],v[2,:2]-v[0,:2]]))
   if abs(det)>1e-16:tri.append(v);mi.append(mat)
 tri=np.array(tri);mi=np.array(mi);lo=tri[:,:,:2].min(axis=1);hi=tri[:,:,:2].max(axis=1);N=48;gr={};origin=np.array([-w/2,-h/2]);cell=np.array([w,h])/N
 for i in range(len(tri)):
  mn=np.floor((lo[i]-origin)/cell).astype(int);mx=np.floor((hi[i]-origin)/cell).astype(int)
  for x in range(mn[0],mx[0]+1):
   for y in range(mn[1],mx[1]+1):gr.setdefault((x,y),[]).append(i)
 def sample(p):
  c=tuple(np.floor((p-origin)/cell).astype(int));ids=gr.get(c,[])
  for i in ids:
   if (p<lo[i]-1e-10).any() or (p>hi[i]+1e-10).any():continue
   v=tri[i];u=v[1,:2]-v[0,:2];v2=v[2,:2]-v[0,:2];q=p-v[0,:2];det=u[0]*v2[1]-u[1]*v2[0];a=(q[0]*v2[1]-q[1]*v2[0])/det;b=(u[0]*q[1]-u[1]*q[0])/det
   if a>=-1e-7 and b>=-1e-7 and a+b<=1.0000001:return float(tri[i,0,2]+a*(tri[i,1,2]-tri[i,0,2])+b*(tri[i,2,2]-tri[i,0,2])),mats[mi[i]]
  return None,None
 metrics=[]
 for pi,p in enumerate(paths):
  for idx in range(len(p)):
   c=p[idx];t=p[min(idx+1,len(p)-1)]-p[max(0,idx-1)];t=t/np.linalg.norm(t);n=np.array([-t[1],t[0]])
   # Quantify main contiguous raised section about the actual center; nearest other paths can join only at branch junctions.
   step=.00001;ds=np.arange(-outer*2,outer*2+step/2,step);vals=[];materials=[]
   for off in ds:
    pp=c+n*off;z,mat=sample(pp);bh=base+.00012*math.sin(pp[0]/w*7)*math.sin(pp[1]/h*5);vals.append(z-bh if z is not None else float('nan'));materials.append(mat)
   vals=np.array(vals);ic=int(np.argmin(abs(ds)));l=r=ic
   while l>0 and vals[l-1]>.000005:l-=1
   while r<len(ds)-1 and vals[r+1]>.000005:r+=1
   rec={'path':pi,'sample':idx,'endpoint':idx in [0,len(p)-1],'relief_support_width_above_5um_m':float(ds[r]-ds[l]),'center_height_above_local_host_m':float(vals[ic])}
   for mat in ['fill','core','mantle']:
    inds=[i for i,x in enumerate(materials) if x==mat and l-2<=i<=r+2]
    if inds:rec[mat+'_material_span_m']=float(ds[max(inds)]-ds[min(inds)])
   # Cross-profile shoulders geometrically distinguish core and mantle, without relying on material.
   if aid.startswith('phyco'):
    rec['height_at_0_9mm_left_m']=float(vals[np.argmin(abs(ds+.0009))]);rec['height_at_0_9mm_right_m']=float(vals[np.argmin(abs(ds-.0009))])
   metrics.append(rec)
 # Actual complete boundary/support envelope, including end caps and all source triangle boundary vertices.
 envelope={}
 for mat in ['fill','core','mantle']:
  inds=set(i for f,m in zip(obj['faces'],obj['material_indices']) if mats[m]==mat for i in f)
  if inds:
   pts=verts[sorted(inds)];envelope[mat]={'vertex_count':len(inds),'bounds_min_m':pts.min(axis=0).tolist(),'bounds_max_m':pts.max(axis=0).tolist(),'max_distance_from_all_actual_centerline_segments_m':max(nearest(p[:2],segs) for p in pts)}
 summary={}
 for k in metrics[0]:
  if k in ['path','sample']:continue
  values=[m[k] for m in metrics if k in m];summary[k]={'min':min(values),'max':max(values)}
 report={'asset_id':aid,'method':'Exact authored triangle barycentric cross-sections, 10um step; known quiet-host sinusoid subtracted only to separate relief from host warp. 5um support threshold is measurement convention, not acceptance tolerance. Full material face-vertex envelopes include endcaps and polygon boundaries, not merely config radii.','cross_section_count':len(metrics),'summary':summary,'complete_material_envelopes':envelope,'profiles':metrics,'connected_surface_components':J(Q/aid/'source-inspection.json')['parts'][0]['connected_components']}
 (Q/aid/'dense-cap-measurements.json').write_text(json.dumps(report,indent=2)+'\n');print(aid,json.dumps(summary),json.dumps(envelope),flush=True)
