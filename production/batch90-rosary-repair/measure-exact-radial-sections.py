from pathlib import Path
import sys,hashlib,json,math,numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values
B=Path(sys.argv[1]);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d,b,raw=read_glb(B/'model.glb');lookup={tuple(r['world_blender_xyz_m']):r['actual_chamber_increment_m'] for r in json.loads((B/'source-neck-baseline.json').read_text())['rows']};tri=[]
for mesh in d['meshes']:
 for pr in mesh['primitives']:
  v=np.array(accessor_values(d,b,pr['attributes']['POSITION']));v=v[:,[0,2,1]];v[:,1]*=-1;ii=np.array(accessor_values(d,b,pr['indices'])).ravel().reshape(-1,3);tri.extend(v[ii])
tri=np.array(tri);inc=np.array([[lookup[tuple(v)] for v in f] for f in tri]);tri=tri[inc.max(1)>0];a=tri[:,0,:2];u=tri[:,1,:2]-a;v=tri[:,2,:2]-a;den=u[:,0]*v[:,1]-u[:,1]*v[:,0];valid=abs(den)>1e-16;tri=tri[valid];a=a[valid];u=u[valid];v=v[valid];den=den[valid]
def weights(q):
 s=(q[:,0]*v[:,1]-q[:,1]*v[:,0])/den;t=(u[:,0]*q[:,1]-u[:,1]*q[:,0])/den;return np.stack((1-s-t,s,t),axis=1)
rows=[]
for i in range(13):
 t=i/12;c=np.array([-.04+.08*t,.009*math.sin(math.tau*t-.4)]);normal=np.array([-.009*math.tau*math.cos(math.tau*t-.4),.08]);normal/=np.linalg.norm(normal);w0=weights(c-a);rad=[]
 for sign in [-1,1]:
  w1=weights(c+normal*sign-a);dw=w1-w0;intervals=[]
  for j in range(len(tri)):
   # Ignore other chambers: their triangles cannot touch this base disk.
   if np.linalg.norm(tri[j,:,:2]-c,axis=1).min()>.0032:continue
   lo=0.;hi=float('inf');ok=True
   for x,y in zip(w0[j],dw[j]):
    if abs(y)<1e-15:
     if x<0:ok=False;break
    elif y>0:lo=max(lo,-x/y)
    else:hi=min(hi,-x/y)
   if ok and hi>lo and hi<.0033:intervals.append((lo,hi))
  assert intervals;rad.append(max(v[1] for v in intervals))
 rows.append({'chamber':i,'exact_normal_section_positive_contribution_support_radii_m':rad,'range_pass':all(.0027<=r<=.0032 for r in rad)})
report={'status':'pass' if all(r['range_pass'] for r in rows) else 'fail','glb_sha256':H(B/'model.glb'),'method':'Analytic ray intersections with actual exported positive-contribution triangles; support closure includes zero-height boundary vertices but no selected relief-height threshold. Both exact normals for13 chamber centers.','rows':rows,'minimum_m':min(x for r in rows for x in r['exact_normal_section_positive_contribution_support_radii_m']),'maximum_m':max(x for r in rows for x in r['exact_normal_section_positive_contribution_support_radii_m']),'frozen_range_m':[.0027,.0032]};(B/'exact-radial-sections.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['minimum_m'],report['maximum_m']);assert report['status']=='pass'
