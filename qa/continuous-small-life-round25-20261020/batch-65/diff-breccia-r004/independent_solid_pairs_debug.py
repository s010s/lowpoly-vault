"""Independent convex-solid overlap test on exact GLB indexed connected components, SAT."""
import struct,json,pathlib,sys,hashlib
import numpy as np
from scipy.spatial import ConvexHull,QhullError
COMP={5120:('i1',1),5121:('u1',1),5122:('i2',2),5123:('u2',2),5125:('u4',4),5126:('f4',4)};NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def load(p):
 b=pathlib.Path(p).read_bytes();magic,ver,total=struct.unpack_from('<4sII',b,0);assert magic==b'glTF' and ver==2 and total==len(b);i=12;d=binchunk=None
 while i<len(b):
  n,k=struct.unpack_from('<II',b,i);i+=8;c=b[i:i+n];i+=n
  if k==0x4e4f534a:d=json.loads(c.decode().rstrip('\0 \t\r\n'))
  elif k==0x004e4942:binchunk=c
 return b,d,binchunk
def acc(d,blob,idx):
 a=d['accessors'][idx];v=d['bufferViews'][a['bufferView']];fmt,s=COMP[a['componentType']];n=NC[a['type']]
 return np.ndarray((a['count'],n),dtype=np.dtype('<'+fmt),buffer=blob,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',s*n),s)).copy()
def mat(n):
 if 'matrix'in n:return np.asarray(n['matrix'],float).reshape((4,4),order='F')
 T=np.eye(4);T[:3,3]=n.get('translation',[0,0,0]);x,y,z,w=n.get('rotation',[0,0,0,1]);R=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]],float);M=np.eye(4);M[:3,:3]=R;return T@M@np.diag([*n.get('scale',[1,1,1]),1])
def mesh_comps(d,blob):
 worlds={}
 def walk(i,p):
  n=d['nodes'][i];w=p@mat(n)
  if 'mesh'in n:
   if n['mesh'] in worlds: raise ValueError('instancing not supported')
   worlds[n['mesh']]=w
  for c in n.get('children',[]):walk(c,w)
 for i in d['scenes'][d.get('scene',0)].get('nodes',[]):walk(i,np.eye(4))
 pieces=[]
 for mi,m in enumerate(d['meshes']):
  if mi not in worlds:continue
  for pi,p in enumerate(m['primitives']):
   v=acc(d,blob,p['attributes']['POSITION']).astype(float);v=(worlds[mi]@np.column_stack((v,np.ones(len(v)))).T).T[:,:3];ind=acc(d,blob,p['indices']).reshape(-1).astype(int);tri=ind.reshape((-1,3));parent=list(range(len(v)))
   def root(x):
    while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
    return x
   for a,b,c in tri:
    x=root(a)
    for y in (b,c):z=root(y);parent[z]=x
   groups={}
   for t in tri:groups.setdefault(root(int(t[0])),[]).append(t)
   for gi,(rt,faces) in enumerate(groups.items()):
    vids=sorted({int(x) for f in faces for x in f});pts=v[vids];vol=0.
    for a,b,c in faces:vol+=float(np.dot(v[a],np.cross(v[b],v[c])))/6
    pieces.append({'mesh':mi,'primitive':pi,'component':gi,'vertex_ids':vids,'points':pts,'faces':faces,'mesh_volume':abs(vol),'aabb_min':pts.min(0),'aabb_max':pts.max(0)})
 return pieces

def hull(piece):
 p=piece['points'];
 try:h=ConvexHull(p)
 except Exception as e: raise RuntimeError({'mesh':piece['mesh'],'primitive':piece['primitive'],'component':piece['component'],'npoints':len(p),'nfaces':len(piece['faces']),'min':p.min(0).tolist(),'max':p.max(0).tolist(),'points':p.tolist(),'err':str(e)[:600]})
 hn=np.linalg.norm(h.equations[:,:3],axis=1);norm=h.equations[:,:3]/hn[:,None];edges=[]
 for f in h.simplices:
  for a,b in ((f[0],f[1]),(f[1],f[2]),(f[2],f[0])):
   e=p[b]-p[a];n=np.linalg.norm(e)
   if n<1e-10:continue
   e=e/n
   if next((q for q in edges if abs(np.dot(e,q))>1-1e-7),None) is None:edges.append(e)
 piece['hull_volume']=float(h.volume);piece['hull_vertices']=len(h.vertices);piece['hull_axes']=norm;piece['edge_dirs']=list(edges)
 return piece

def overlaps(a,b,tol=1e-8):
 axes=[*a['hull_axes'],*b['hull_axes']]
 for x in a['edge_dirs']:
  for y in b['edge_dirs']:
   z=np.cross(x,y);n=np.linalg.norm(z)
   if n>1e-8:axes.append(z/n)
 p=a['points'];q=b['points'];minimum=float('inf')
 for n in axes:
  pa=p@n;pb=q@n;ov=min(pa.max(),pb.max())-max(pa.min(),pb.min())
  if ov<=tol:return False,max(0.,ov)
  if ov<minimum:minimum=ov
 return True,minimum

def check(path):
 raw,d,blob=load(path);pcs=mesh_comps(d,blob);host=[p for p in pcs if p['mesh']==0];clasts=[hull(p) for p in pcs if p['mesh']!=0]
 if len(host)!=1 or len(clasts)!=120:raise ValueError(f'expected host+120 clasts, got {len(host)}+{len(clasts)}')
 for p in clasts:
  p['hull_mesh_volume_ratio']=p['mesh_volume']/p['hull_volume'] if p['hull_volume'] else 0
 overlaps_found=[];tests=0
 for i,a in enumerate(clasts):
  for j in range(i+1,len(clasts)):
   b=clasts[j]
   if np.any(a['aabb_max'] < b['aabb_min']-1e-8) or np.any(b['aabb_max'] < a['aabb_min']-1e-8):continue
   tests+=1;ov,depth=overlaps(a,b)
   if ov:overlaps_found.append({'a':[a['mesh'],a['primitive'],a['component']],'b':[b['mesh'],b['primitive'],b['component']],'minimum_SAT_axis_overlap_m':depth,'hull_volume_a':a['hull_volume'],'hull_volume_b':b['hull_volume']})
 report={'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'triangles':sum(len(p['faces']) for p in pcs),'component_count':len(pcs),'host_count':len(host),'clast_count':len(clasts),'narrow_phase_pairs':tests,'positive_volume_clast_pair_intersections':len(overlaps_found),'mesh_vs_convex_hull_volume_ratio_min':min(x['hull_mesh_volume_ratio'] for x in clasts),'mesh_vs_convex_hull_volume_ratio_max':max(x['hull_mesh_volume_ratio'] for x in clasts),'all_clast_meshes_convex_within_1e-5_rel':all(x['hull_mesh_volume_ratio']>=1-1e-5 for x in clasts),'clast_sum_mesh_volume_m3':sum(x['mesh_volume'] for x in clasts),'clast_sum_convex_hull_volume_m3':sum(x['hull_volume'] for x in clasts),'intersections':overlaps_found}
 return report
paths=sys.argv[1:3];res=[check(p) for p in paths];out={'method':'Independent exact-GLB indexed-topology connected-component extraction followed by 3D convex hull volume and separating-axis theorem (both hull facet normals plus all unique edge cross-products). Pairwise test is limited to clast-versus-clast solids, not intentional clast-host embedding. SAT is exact only where components match their convex hulls; the report records hull/mesh volume ratio to expose nonconvex components. Positive axis overlap required on every axis; 1e-8m contact tolerance.','results':res,'comparison':{'r003_r004_pair_overlap_counts':[x['positive_volume_clast_pair_intersections'] for x in res],'all_components_convex':all(x['all_clast_meshes_convex_within_1e-5_rel'] for x in res)}}
open('/workspace/shared/lowpoly-round25-qa65/diff-breccia-r004/independent-solid-pairs.json','w').write(json.dumps(out,indent=2)+'\n')
print(json.dumps({'comparison':out['comparison'],'summaries':[{k:r[k] for k in ('path','triangles','component_count','clast_count','narrow_phase_pairs','positive_volume_clast_pair_intersections','mesh_vs_convex_hull_volume_ratio_min','mesh_vs_convex_hull_volume_ratio_max','all_clast_meshes_convex_within_1e-5_rel','clast_sum_mesh_volume_m3','clast_sum_convex_hull_volume_m3')} for r in res]},indent=2))
