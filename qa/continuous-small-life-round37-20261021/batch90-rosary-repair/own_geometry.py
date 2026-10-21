from pathlib import Path
import struct,json,hashlib,math,collections,numpy as np
O=Path(__file__).parent;R=Path('/workspace/shared/lowpoly-batch90-rosary-repair-20261020');B=R/'production/batch90-rosary-repair/assets/rosary-shaped-chambered-burrow-hormosiroidea-type/r002';OLD=Path('/workspace/shared/lowpoly-batch90-20261020/production/batch90/assets/rosary-shaped-chambered-burrow-hormosiroidea-type/r001');H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def decode(path):
 raw=path.read_bytes();magic,version,length=struct.unpack_from('<III',raw);assert magic==0x46546c67 and version==2 and length==len(raw);offset=12;chunks={}
 while offset<len(raw):
  size,kind=struct.unpack_from('<II',raw,offset);offset+=8;chunks[kind]=raw[offset:offset+size];offset+=size
 d=json.loads(chunks[0x4e4f534a]);bin=chunks[0x004e4942]
 for n in d['nodes']:
  assert n.get('matrix',[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1])==[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1];assert n.get('translation',[0,0,0])==[0,0,0];assert n.get('scale',[1,1,1])==[1,1,1];assert n.get('rotation',[0,0,0,1])==[0,0,0,1]
 def acc(index):
  a=d['accessors'][index];v=d['bufferViews'][a['bufferView']];ty={5126:'f',5125:'I',5123:'H',5121:'B'}[a['componentType']];num={'VEC3':3,'SCALAR':1,'VEC2':2,'VEC4':4}[a['type']];fmt='<'+ty*num;sz=struct.calcsize(fmt);stride=v.get('byteStride',sz);off=v.get('byteOffset',0)+a.get('byteOffset',0);return np.array([struct.unpack_from(fmt,bin,off+j*stride) for j in range(a['count'])])
 tri=[]
 for mesh in d['meshes']:
  for pr in mesh['primitives']:
   assert pr.get('mode',4)==4;v=acc(pr['attributes']['POSITION'])[:,[0,2,1]];v[:,1]*=-1;tri.extend(v[acc(pr['indices']).ravel().astype(int).reshape(-1,3)])
 return d,np.array(tri)
d,tr=decode(B/'model.glb');od,otr=decode(OLD/'model.glb');lookup={tuple(x['xyz']):x['chamber_increment'] for x in json.loads((O/'own-source-vertices-baseline.json').read_text())['rows']};inc=np.array([[lookup[tuple(v)] for v in t] for t in tr]);assert inc.min()==0
centers=np.array([[-.04+.08*i/12,.009*math.sin(math.tau*i/12-.4)] for i in range(13)]);radii=np.array([.0027+.0005*(.5+.5*math.sin(i*1.3+.2)) for i in range(13)])
positive=inc.max(axis=1)>0;pt=tr[positive];distance=np.linalg.norm(pt[:,:,:2,None]-centers.T[None,None,:,:],axis=2);maxdistance=distance.max(axis=1);contained=maxdistance<=radii[None,:];assert contained.any(axis=1).all();assert (contained.sum(1)==1).all()
# Connected positive-contribution faces, using exact exported vertex identities, rather than maker semantic labels.
vfaces=collections.defaultdict(set)
for i,f in enumerate(pt):
 for v in f:vfaces[tuple(v)].add(i)
unseen=set(range(len(pt)));components=[]
while unseen:
 seed=unseen.pop();todo=[seed];group={seed}
 while todo:
  for v in pt[todo.pop()]:
   for k in vfaces[tuple(v)]:
    if k in unseen:unseen.remove(k);group.add(k);todo.append(k)
 g=sorted(group);ch=np.where(contained[g].any(0))[0].tolist();assert len(ch)==1;v=pt[g].reshape(-1,3);components.append(dict(chamber=ch[0],triangles=len(g),bounds_min_m=v.min(0).tolist(),bounds_max_m=v.max(0).tolist(),size_m=np.ptp(v,axis=0).tolist(),maximum_support_vertex_radius_m=float(maxdistance[g,ch[0]].max()),original_radius_m=float(radii[ch[0]])))
components.sort(key=lambda x:x['chamber']);assert len(components)==13
class Surface:
 def __init__(self,tri,contrib=None):
  a=tri[:,0,:2];u=tri[:,1,:2]-a;v=tri[:,2,:2]-a;det=u[:,0]*v[:,1]-u[:,1]*v[:,0];mask=det!=0;self.tr=tri[mask];self.a=a[mask];self.u=u[mask];self.v=v[mask];self.det=det[mask];self.inc=None if contrib is None else contrib[mask]
 def weights(self,q):
  q=np.asarray(q)-self.a;s=(q[:,0]*self.v[:,1]-q[:,1]*self.v[:,0])/self.det;t=(self.u[:,0]*q[:,1]-self.u[:,1]*q[:,0])/self.det;return np.column_stack((1-s-t,s,t))
 def hit(self,q):
  w=self.weights(q);mask=(w>=-1e-12).all(1);ids=np.where(mask)[0];assert len(ids);z=(w*self.tr[:,:,2]).sum(1);i=int(ids[np.argmax(z[ids])]);return dict(point_xy_m=list(q),z_m=float(z[i]),height_above_exported_host_m=float(z[i]-np.float32(.009)),triangle_xyz_m=self.tr[i].tolist(),barycentric=w[i].tolist(),chamber_contribution_m=None if self.inc is None else float(w[i]@self.inc[i]))
s=Surface(tr,inc);os=Surface(otr);ps=Surface(pt)
# Stable plane interpolation distinguishes exact constant planes from harmless summation roundoff.
def hit(q,s=s):
 r=s.hit(q);v=np.array(r['triangle_xyz_m']);w=np.array(r['barycentric']);r['z_m']=float(v[0,2]+w[1]*(v[1,2]-v[0,2])+w[2]*(v[2,2]-v[0,2]));r['height_above_exported_host_m']=r['z_m']-float(np.float32(.009));return r
old=json.loads(Path('/workspace/shared/lowpoly-batch90-independent-qa-20261020/rosary-shaped-chambered-burrow-hormosiroidea-type/chamber-tail-exact-triangle-evidence.json').read_text());regression=[]
for x in old['samples']:
 q=x['point_blender_xy'];before=hit(q,os);after=hit(q);assert after['height_above_exported_host_m']==0 and after['chamber_contribution_m']==0;regression.append(dict(radius_m=x['requested_normal_radius_m'],old=before,new=after))
normal_samples=[];normal_sections=[]
for i,c in enumerate(centers):
 t=i/12;n=np.array([-.009*math.tau*math.cos(math.tau*t-.4),.08]);n/=np.linalg.norm(n)
 for rad in [.0032,.0035,.0038]:
  for sign in [-1,1]:
   rec=dict(chamber=i,radius_m=rad,side=sign,**hit(c+rad*sign*n));normal_samples.append(rec);assert rec['chamber_contribution_m']==0
 row=[]
 for sign in [-1,1]:
  w0=ps.weights(c);dw=ps.weights(c+n*sign)-w0;lo=np.zeros(len(pt));hi=np.full(len(pt),np.inf);valid=np.ones(len(pt),dtype=bool)
  for k in range(3):
   a=w0[:,k];b=dw[:,k];nz=b!=0;pos=b>0;neg=b<0;cut=np.zeros(len(pt));cut[nz]=-a[nz]/b[nz];lo[pos]=np.maximum(lo[pos],cut[pos]);hi[neg]=np.minimum(hi[neg],cut[neg]);valid&=nz|(a>=0)
  valid&=(hi>lo)&(lo<radii[i])&(hi<.0033);intervals=sorted(zip(lo[valid],hi[valid]));assert intervals;maxr=max(x[1] for x in intervals);assert .0027<=maxr<=.0032;row.append(float(maxr))
 normal_sections.append(dict(chamber=i,support_semiradii_m=row,diameter_m=sum(row)))
# Actual exact-triangle centerline values at 2401 positions: count 11 internal maxima plus 2 terminal lobes.
profile=[hit([-.04+.08*t,.009*math.sin(math.tau*t-.4)])['height_above_exported_host_m'] for t in np.linspace(0,1,2401)];peaks=[i for i in range(1,len(profile)-1) if profile[i]>profile[i-1] and profile[i]>profile[i+1] and profile[i]>.002];assert len(peaks)==11
# Readability contour is stated explicitly, used only for chamber/neck breadth, never for the radius envelope.
widths=[]
for t in [6/12,5.5/12]:
 c=np.array([-.04+.08*t,.009*math.sin(math.tau*t-.4)]);n=np.array([-.009*math.tau*math.cos(math.tau*t-.4),.08]);n/=np.linalg.norm(n);ds=[x for x in np.linspace(-.005,.005,2001) if hit(c+x*n)['height_above_exported_host_m']>.00008];widths.append(max(ds)-min(ds))
assert widths[0]/widths[1]>=2.4
v=tr.reshape(-1,3);ov=otr.reshape(-1,3);assert d['materials']==od['materials'];assert np.array_equal(v.min(0),ov.min(0)) and np.array_equal(v.max(0),ov.max(0))
# Neck-only vertices at common exact XY positions must preserve their z exactly.
oldxy={tuple(x[:2]):float(x[2]) for x in ov if x[2]>=float(np.float32(.009))};neckrows=[x for x in json.loads((O/'own-source-vertices-baseline.json').read_text())['rows'] if x['chamber_increment']==0 and 0<x['neck_distance']<.001 and tuple(x['xyz'][:2]) in oldxy];diff=[x['xyz'][2]-oldxy[tuple(x['xyz'][:2])] for x in neckrows]
report=dict(status='pass',glb_sha256=H(B/'model.glb'),source_sha256=H(B/'source.blend'),baseline_sha256=H(O/'own-source-vertices-baseline.json'),method='Own struct-based GLB decoder; identity transforms verified; every actual exported coordinate mapped to freshly reopened source. Original neck field independently recomputed, no maker contribution labels used. Any strictly positive actual chamber increment selects its incident triangle; all three vertices are inside the same original convex chamber disk, hence the full triangle is inside. Zero means exactly zero, no height threshold. Normal support is analytic ray/triangle interval intersection.',triangles=len(tr),positive_chamber_triangles=int(positive.sum()),uncontained_positive_triangles=int((~contained.any(1)).sum()),positive_contribution_connected_components=len(components),chamber_components=components,old_failure_points=regression,external_normal_samples=normal_samples,all_78_zero=all(x['chamber_contribution_m']==0 for x in normal_samples),normal_sections=normal_sections,normal_semiradius_minmax_m=[min(x for r in normal_sections for x in r['support_semiradii_m']),max(x for r in normal_sections for x in r['support_semiradii_m'])],bounds_m={'min':v.min(0).tolist(),'max':v.max(0).tolist(),'size':np.ptp(v,axis=0).tolist()},chamber_count=13,centerline_internal_peaks=len(peaks),terminal_peaks=2,centerline_minimum_relief_m=min(profile),center_reliefs_m=[hit(c)['height_above_exported_host_m'] for c in centers],readability_contour_m=.00008,chamber_neck_widths_m=widths,chamber_neck_ratio=widths[0]/widths[1],same_exported_materials=True,same_overall_bounds=True,common_neck_vertices_checked=len(diff),common_neck_vertex_z_max_difference_m=max(abs(x) for x in diff),precision='Planar hit formula is z0+w1*(z1-z0)+w2*(z2-z0), so an exact exported host triangle remains exactly host. Barycentric membership epsilon1e-12 is dimensionless numerical edge membership only, not height/radius allowance. Positive contribution and convex-disk containment use strict zero and literal radius limits. The20nm guard is inside the new mesh, not an acceptance epsilon.',limitations='Neck analytical kernel and centers retained; retriangulation can change interpolation away from shared vertices. A contribution component is not a detached object. GPU/scene not run.')
(O/'own-exact-geometry.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['chamber_components','old_failure_points','external_normal_samples','normal_sections','method','precision','limitations']},indent=2))
