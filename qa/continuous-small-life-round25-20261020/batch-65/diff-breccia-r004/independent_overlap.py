"""Independent GLB triangle-level overlap filters, all hierarchy transforms applied."""
import json,struct,hashlib,pathlib,sys,math
import numpy as np
COMP={5120:('i1',1),5121:('u1',1),5122:('i2',2),5123:('u2',2),5125:('u4',4),5126:('f4',4)}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def glb(path):
 raw=pathlib.Path(path).read_bytes(); magic,ver,total=struct.unpack_from('<4sII',raw,0)
 if magic!=b'glTF' or ver!=2 or total!=len(raw):raise ValueError('invalid GLB')
 at=12;doc=binchunk=None
 while at<len(raw):
  n,k=struct.unpack_from('<II',raw,at);at+=8;chunk=raw[at:at+n];at+=n
  if k==0x4e4f534a:doc=json.loads(chunk.decode().rstrip('\0 \t\r\n'))
  elif k==0x004e4942:binchunk=chunk
 return raw,doc,binchunk
def access(doc,binary,i):
 a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];fmt,size=COMP[a['componentType']];n=NC[a['type']]
 return np.ndarray((a['count'],n),dtype=np.dtype('<'+fmt),buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',size*n),size)).copy()
def local(n):
 if 'matrix'in n:return np.array(n['matrix'],float).reshape((4,4),order='F')
 t=np.eye(4);t[:3,3]=n.get('translation',[0,0,0]);x,y,z,w=n.get('rotation',[0,0,0,1]);r=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]],float);m=np.eye(4);m[:3,:3]=r;return t@m@np.diag([*n.get('scale',[1,1,1]),1])
def intersect2(s,c):
 out=[np.array(x,float) for x in s];c=np.asarray(c,float);ori=np.sign(np.sum(c[:,0]*np.roll(c[:,1],-1)-np.roll(c[:,0],-1)*c[:,1]))
 if not ori:return []
 for i in range(3):
  a=c[i];b=c[(i+1)%3];e=b-a;inp=out;out=[]
  if not inp:break
  def side(p):return ori*(e[0]*(p[1]-a[1])-e[1]*(p[0]-a[0]))
  prev=inp[-1];sp=side(prev)
  for cur in inp:
   sc=side(cur);ic=sc>=-1e-12;ip=sp>=-1e-12
   if ic!=ip:
    den=sp-sc
    if den:out.append(prev+(sp/den)*(cur-prev))
   if ic:out.append(cur)
   prev,sp=cur,sc
 return out
def area(poly):
 if len(poly)<3:return 0.
 p=np.asarray(poly);return abs(float(np.sum(p[:,0]*np.roll(p[:,1],-1)-np.roll(p[:,0],-1)*p[:,1])))*.5
def triangles(doc,binary):
 worlds={}
 def walk(i,parent):
  n=doc['nodes'][i];m=parent@local(n)
  if 'mesh'in n:
   if n['mesh'] in worlds:raise ValueError('instanced mesh unsupported')
   worlds[n['mesh']]=m
  for j in n.get('children',[]):walk(j,m)
 for i in doc['scenes'][doc.get('scene',0)].get('nodes',[]):walk(i,np.eye(4))
 tris=[]
 for mi,mesh in enumerate(doc['meshes']):
  if mi not in worlds:continue
  for pi,pr in enumerate(mesh['primitives']):
   if pr.get('mode',4)!=4:continue
   pos=access(doc,binary,pr['attributes']['POSITION']).astype(float);pos=(worlds[mi]@np.column_stack([pos,np.ones(len(pos))]).T).T[:,:3]
   ix=access(doc,binary,pr['indices']).reshape(-1) if 'indices'in pr else np.arange(len(pos))
   mat=doc.get('materials',[])[pr['material']].get('name') if 'material'in pr else None
   for t in range(len(ix)//3):
    p=pos[ix[t*3:t*3+3].astype(int)];n=np.cross(p[1]-p[0],p[2]-p[0]);nn=np.linalg.norm(n)
    if nn<1e-12:continue
    tris.append({'p':p,'n':n/nn,'lo':p.min(0),'hi':p.max(0),'mesh':mi,'primitive':pi,'triangle':t,'material':mat})
 return tris
def detect(path,tol,area_tol):
 raw,doc,binary=glb(path);ts=triangles(doc,binary);low=np.array([t['lo'] for t in ts]);high=np.array([t['hi'] for t in ts]);norm=np.array([t['n'] for t in ts]);pts=np.array([t['p'] for t in ts]);found=[]
 for i,a in enumerate(ts):
  cand=np.flatnonzero(np.all(high[i+1:]>=low[i]-tol,axis=1)&np.all(low[i+1:]<=high[i]+tol,axis=1))+i+1
  if not len(cand):continue
  cand=cand[np.abs(norm[cand]@norm[i])>=1-1e-6]
  if not len(cand):continue
  sep=np.max(np.abs((pts[cand]-pts[i,0])@norm[i]),axis=1);keep=sep<=tol;cand=cand[keep];sep=sep[keep]
  if not len(cand):continue
  drop=int(np.argmax(np.abs(norm[i])));axes=[x for x in range(3) if x!=drop]
  for j,s in zip(cand,sep):
   projected=intersect2(pts[i][:,axes],pts[j][:,axes]);a3=area(projected)/abs(norm[i,drop])
   if a3>area_tol:
    b=ts[j];found.append({'a':[a['mesh'],a['primitive'],a['triangle'],a['material']],'b':[b['mesh'],b['primitive'],b['triangle'],b['material']],'area_m2':float(a3),'separation_m':float(s)})
 return {'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'triangle_count':len(ts),'normal_dot_tolerance':1e-6,'plane_tolerance_m':tol,'minimum_projected_area_m2':area_tol,'pair_count':len(found),'max_area_m2':max((x['area_m2'] for x in found),default=0.),'pairs':found}
paths=sys.argv[1:3];res=[]
for path in paths:
 res.append({'glb':path,'near_1mm':detect(path,1e-3,1e-6),'strict_10um':detect(path,1e-5,1e-8)})
out={'method':'Independent raw GLB parser, full node transform chain, triangle AABB broadphase, near-parallel normal dot test, maximum vertex-plane separation, Sutherland-Hodgman positive projected triangle intersection, projected area lifted to 3D. This is a narrow parallel/coplanar witness filter, not full 3D solid intersection test or proof of website pixels.','results':res,'comparison':{'near_1mm_before':res[0]['near_1mm']['pair_count'],'near_1mm_after':res[1]['near_1mm']['pair_count'],'strict_before':res[0]['strict_10um']['pair_count'],'strict_after':res[1]['strict_10um']['pair_count']}}
open('/workspace/shared/lowpoly-round25-qa65/diff-breccia-r004/independent-overlap.json','w').write(json.dumps(out,indent=2)+'\n')
print(json.dumps({'comparison':out['comparison'],'summaries':[{'sha256':r['glb'],'near_pairs':r['near_1mm']['pair_count'],'strict_pairs':r['strict_10um']['pair_count'],'near_max_area':r['near_1mm']['max_area_m2'],'triangles':r['near_1mm']['triangle_count']} for r in res]},indent=2))
