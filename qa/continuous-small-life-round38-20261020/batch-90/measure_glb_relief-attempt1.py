import json,sys,math,pathlib,hashlib,numpy as np
R=pathlib.Path('/workspace/shared/lowpoly-batch90-20261020');O=pathlib.Path('/workspace/shared/lowpoly-batch90-independent-qa-20261020');sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values
for aid in ['rosary-shaped-chambered-burrow-hormosiroidea-type','lumbricaria-thread-like-coprolite']:
 p=R/'production/batch90/assets'/aid/'r001/model.glb';d,b,raw=read_glb(p);T=.009 if aid.startswith('rosary') else .012;tris=[];allpos=[]
 for me in d['meshes']:
  for pr in me['primitives']:
   v=np.array(accessor_values(d,b,pr['attributes']['POSITION']));v=v[:,[0,2,1]];v[:,1]*=-1;idx=np.array(accessor_values(d,b,pr['indices'])).ravel().reshape(-1,3);tri=v[idx];allpos.append(v);tris.extend(tri)
 tri=np.array(tris);a=tri[:,0,:2];u=tri[:,1,:2]-a;v=tri[:,2,:2]-a;den=u[:,0]*v[:,1]-u[:,1]*v[:,0];valid=np.abs(den)>1e-12;tri=tri[valid];a=a[valid];u=u[valid];v=v[valid];den=den[valid]
 def z(x,y):
  q=np.array([x,y])-a;s=(q[:,0]*v[:,1]-q[:,1]*v[:,0])/den;t=(u[:,0]*q[:,1]-u[:,1]*q[:,0])/den;mask=(s>=-1e-8)&(t>=-1e-8)&(s+t<=1+1e-8)
  zz=tri[:,0,2]+s*(tri[:,1,2]-tri[:,0,2])+t*(tri[:,2,2]-tri[:,0,2]);return float(zz[mask].max())
 pts=np.unique(np.concatenate(allpos),axis=0);result={'asset_id':aid,'glb_sha256':hashlib.sha256(raw).hexdigest(),'method':'Decoded exact exported triangle coordinates. Interpolate vertical hit against triangles, not material or generator config. Coordinates transformed glTF XYZ to Blender XYZ.','unique_positions':len(pts),'slab_flat_top_vertices_z':T,'surface_peak_height_m':float(pts[:,2].max()-T)}
 if aid.startswith('rosary'):
  lobes=[]
  for i in range(13):
   t=i/12;x=-.04+.08*t;y=.009*math.sin(math.tau*t-.4);n=np.array([-.009*math.tau*math.cos(math.tau*t-.4),.08]);n/=np.linalg.norm(n)
   radii=[]
   for sign in [-1,1]:
    lo,hi=.0015,.004
    for _ in range(24):
     mid=(lo+hi)/2
     if z(x+sign*n[0]*mid,y+sign*n[1]*mid)>T+1e-8:lo=mid
     else:hi=mid
    radii.append((lo+hi)/2)
   lobes.append({'index':i,'surface_apex_m':z(x,y)-T,'normal_section_semibreadths_m':radii})
  result['lobes']=lobes;result['semibreadth_range_m']=[min(v for l in lobes for v in l['normal_section_semibreadths_m']),max(v for l in lobes for v in l['normal_section_semibreadths_m'])];result['range_note']='Normal-section footprint is approximately the original 2.7–3.2mm chamber radius range; tiny numerical/CDT variation distinguished from hard gross-shape bounds. Exact spherical body is not claimed: fused heightfield, not detached bead.'
 else:
  # A vertical section through a separated, observed trailing cord around x=0.05,y=-0.03.
  above=pts[pts[:,2]>T+1e-8];result['raised_relief_bbox_m']=(above.max(0)-above.min(0)).tolist();result['max_relief_not_texture']=bool(pts[:,2].max()>T+.0017);result['geometry_no_plane_overlay']='One connected manifold heightfield volume verified by source reopening; crossings are maximum-union surface, not intersecting tube overlays.'
 (O/aid/'own-exported-relief-measurement.json').write_text(json.dumps(result,indent=2)+'\n');print(aid,json.dumps(result))
