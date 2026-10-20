"""Read-only independent exact-GLB coplanar overlap test; raw GLB parser + 3D/2D triangle geometry."""
import json,struct,hashlib,pathlib,sys,math
import numpy as np

COMP={5120:('i1',1),5121:('u1',1),5122:('i2',2),5123:('u2',2),5125:('u4',4),5126:('f4',4)}
NC={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}

def glb(path):
    raw=pathlib.Path(path).read_bytes()
    magic,ver,total=struct.unpack_from('<4sII',raw,0)
    if magic!=b'glTF' or ver!=2 or total!=len(raw): raise ValueError('invalid GLB header')
    at=12;doc=binchunk=None
    while at<len(raw):
        n,kind=struct.unpack_from('<II',raw,at);at+=8;chunk=raw[at:at+n];at+=n
        if kind==0x4e4f534a:doc=json.loads(chunk.decode('utf-8').rstrip('\0 \t\r\n'))
        elif kind==0x004e4942:binchunk=chunk
    if doc is None or binchunk is None:raise ValueError('missing JSON/BIN chunk')
    return raw,doc,binchunk

def accessor(doc,binary,index):
    a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
    fmt,size=COMP[a['componentType']];n=NC[a['type']];stride=v.get('byteStride',size*n);off=v.get('byteOffset',0)+a.get('byteOffset',0)
    arr=np.ndarray((a['count'],n),dtype=np.dtype('<'+fmt),buffer=binary,offset=off,strides=(stride,size)).copy()
    return arr

def node_local(n):
    if 'matrix' in n:return np.array(n['matrix'],dtype=float).reshape((4,4),order='F')
    t=np.eye(4);t[:3,3]=n.get('translation',[0,0,0])
    x,y,z,w=n.get('rotation',[0,0,0,1]);r=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]],dtype=float)
    s=np.diag([*n.get('scale',[1,1,1]),1]);m=np.eye(4);m[:3,:3]=r;return t@m@s

def polys_intersection(subject,clipper):
    out=[np.array(p,dtype=float) for p in subject]
    c=np.asarray(clipper,dtype=float); orientation=np.sign(np.sum(c[:,0]*np.roll(c[:,1],-1)-np.roll(c[:,0],-1)*c[:,1]))
    if orientation==0:return []
    for i in range(3):
        a=c[i];b=c[(i+1)%3];edge=b-a;inp=out;out=[]
        if not inp:break
        def side(p):return orientation*(edge[0]*(p[1]-a[1])-edge[1]*(p[0]-a[0]))
        prev=inp[-1];sp=side(prev)
        for cur in inp:
            sc=side(cur);inside_c=sc>=-1e-12;inside_p=sp>=-1e-12
            if inside_c!=inside_p:
                den=sp-sc
                if den!=0:out.append(prev+(sp/den)*(cur-prev))
            if inside_c:out.append(cur)
            prev,sp=cur,sc
    return out

def polygon_area(poly):
    if len(poly)<3:return 0.0
    p=np.asarray(poly);return abs(float(np.sum(p[:,0]*np.roll(p[:,1],-1)-np.roll(p[:,0],-1)*p[:,1])))*.5

def collect(doc,binary):
    worlds={}
    def walk(node_i,parent):
        n=doc['nodes'][node_i];w=parent@node_local(n)
        if 'mesh' in n:
            if n['mesh'] in worlds:raise ValueError('instanced mesh unsupported')
            worlds[n['mesh']]=w
        for child in n.get('children',[]):walk(child,w)
    scene=doc['scenes'][doc.get('scene',0)]
    for node in scene.get('nodes',[]):walk(node,np.eye(4))
    alltris=[]
    for mi,mesh in enumerate(doc['meshes']):
        if mi not in worlds: continue
        M=worlds[mi]
        for pi,pr in enumerate(mesh['primitives']):
            if pr.get('mode',4)!=4:continue
            pos=accessor(doc,binary,pr['attributes']['POSITION']).astype(np.float64)
            p4=np.column_stack([pos,np.ones(len(pos))]);pos=(M@p4.T).T[:,:3]
            ix=accessor(doc,binary,pr['indices']).reshape(-1) if 'indices' in pr else np.arange(len(pos))
            mat_i=pr.get('material');mat=doc.get('materials',[])[mat_i].get('name') if mat_i is not None else None
            for ti in range(len(ix)//3):
                ids=ix[3*ti:3*ti+3].astype(int);pts=pos[ids];n=np.cross(pts[1]-pts[0],pts[2]-pts[0]);norm=np.linalg.norm(n)
                if norm<1e-12:continue
                n=n/norm
                alltris.append({'points':pts,'normal':n,'lo':pts.min(axis=0),'hi':pts.max(axis=0),'mesh':mi,'primitive':pi,'triangle':ti,'material':mat})
    return alltris

def detect(path):
    raw,doc,binary=glb(path);tris=collect(doc,binary);tol=1e-5;area_tol=1e-8;found=[];n=len(tris)
    lows=np.array([t['lo'] for t in tris]); highs=np.array([t['hi'] for t in tris]); norms=np.array([t['normal'] for t in tris]); pts=np.array([t['points'] for t in tris])
    for i,a in enumerate(tris):
        candidates=np.flatnonzero(np.all(highs[i+1:]>=lows[i]-tol,axis=1)&np.all(lows[i+1:]<=highs[i]+tol,axis=1))+i+1
        if not len(candidates):continue
        parallel=np.abs(norms[candidates]@norms[i])>=1-1e-6;candidates=candidates[parallel]
        if not len(candidates):continue
        separations=np.max(np.abs((pts[candidates]-pts[i,0])@norms[i]),axis=1)
        candidates=candidates[separations<=tol];separations=separations[separations<=tol]
        if not len(candidates):continue
        drop=int(np.argmax(np.abs(norms[i])));axes=[k for k in range(3) if k!=drop];ap=pts[i][:,axes]
        for j,sep in zip(candidates,separations):
            projected=polys_intersection(ap,pts[j][:,axes]);area=polygon_area(projected)/abs(norms[i,drop])
            if area>area_tol:
                b=tris[j]
                found.append({'a':{k:a[k] for k in ('mesh','primitive','triangle','material')},'b':{k:b[k] for k in ('mesh','primitive','triangle','material')},'overlap_area_m2':float(area),'plane_separation_m':float(sep)})
    doc_json={'raw_sha256':hashlib.sha256(raw).hexdigest(),'triangle_count':len(tris),'all_material_pairs':len(found),'max_area_m2':max((x['overlap_area_m2'] for x in found),default=0.0),'plane_tolerance_m':tol,'normal_dot_tolerance':1e-6,'positive_area_threshold_m2':area_tol,'pairs':found,'website_subset':{'criterion':'mesh 6, primitive 0, material darkclast on both triangles','count':sum(x['a']['mesh']==6 and x['b']['mesh']==6 and x['a']['primitive']==0 and x['b']['primitive']==0 and x['a']['material']=='darkclast' and x['b']['material']=='darkclast' for x in found)}}
    return doc_json

if __name__=='__main__':
    paths=sys.argv[1:3]
    out=[]
    for p in paths:out.append({'path':p,**detect(p)})
    result={'method':'Independent raw GLB accessor reader; full scene-transformed triangle geometry; bounding-box broadphase; normalized plane parallel/separation tests; exact 2D convex triangle clipping; projected intersection area lifted to 3D. No producer overlap detector output used.','results':out}
    print(json.dumps([{k:r[k] for k in ('path','raw_sha256','triangle_count','all_material_pairs','max_area_m2','website_subset')} for r in out],indent=2))
    pathlib.Path('/workspace/shared/lowpoly-round25-qa65/diff-breccia-r003/independent-overlap.json').write_text(json.dumps(result,indent=2)+'\n')
