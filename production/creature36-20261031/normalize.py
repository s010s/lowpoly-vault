"""Preserve frozen GLB buffers/materials; add only an authored-scale root transform.

Usage: python normalize.py private-selected-models.json [--install]
The private selection file is not a public deliverable. Existing authored maximum
dimension is the scale contract; it is not a life-size/specimen measurement.
"""
import json,struct,hashlib,pathlib,sys,copy
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[2]
RELEASE='creature36-20261031'
def digest(b):return hashlib.sha256(b).hexdigest()
def unpack(b):
    assert struct.unpack_from('<III',b)==(0x46546c67,2,len(b))
    n,t=struct.unpack_from('<II',b,12);assert t==0x4e4f534a
    g=json.loads(b[20:20+n]);tail=b[20+n:]
    assert not any(v.get('uri') for v in g.get('buffers',[])+g.get('images',[]))
    assert struct.unpack_from('<I',tail,4)[0]==0x004e4942
    return g,tail
def pack(g,tail):
    j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
    return struct.pack('<IIIII',0x46546c67,2,20+len(j)+len(tail),len(j),0x4e4f534a)+j+tail
def accessor(g,tail,i):
    a=g['accessors'][i];v=g['bufferViews'][a['bufferView']]
    dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']]
    k={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    return np.ndarray((a['count'],k),dtype=dtype,buffer=tail,offset=8+v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',np.dtype(dtype).itemsize*k),np.dtype(dtype).itemsize))
def matrix(n):
    if 'matrix' in n:return np.array(n['matrix']).reshape(4,4).T
    x,y,z,w=n.get('rotation',[0,0,0,1]);m=np.eye(4)
    m[:3,:3]=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]])@np.diag(n.get('scale',[1,1,1]))
    m[:3,3]=n.get('translation',[0,0,0]);return m
def audit(g,tail):
    points=[];triangles=0;primitives=0
    def walk(i,parent):
        nonlocal triangles,primitives
        n=g['nodes'][i];m=parent@matrix(n)
        if 'mesh' in n:
            for p in g['meshes'][n['mesh']]['primitives']:
                assert p.get('mode',4)==4
                v=accessor(g,tail,p['attributes']['POSITION']);assert np.isfinite(v).all()
                points.append(v@m[:3,:3].T+m[:3,3]);primitives+=1
                triangles+=(g['accessors'][p['indices']]['count'] if 'indices' in p else len(v))//3
        for c in n.get('children',[]):walk(c,m)
    for i in g['scenes'][g.get('scene',0)]['nodes']:walk(i,np.eye(4))
    v=np.concatenate(points);lo=v.min(axis=0);hi=v.max(axis=0)
    return dict(min=lo.tolist(),max=hi.tolist(),dimensions=(hi-lo).tolist(),triangles=triangles,primitives=primitives,material_count=len(g.get('materials',[])),embedded_images=len(g.get('images',[])))
def run(selection,install=False):
    manifest=json.loads((ROOT/'assets/manifest.json').read_text());old={a['id']:a for a in manifest['assets']};rows=[]
    for source in selection:
        id=source['id'];raw=pathlib.Path(source['path']).read_bytes();assert digest(raw)==source['sha256']
        g,tail=unpack(raw);before=audit(g,tail);s=max(old[id]['dimensions'])/max(before['dimensions'])
        # Retain the published principal horizontal axis, rotating only around Y.
        old_axis=0 if old[id]['dimensions'][0]>old[id]['dimensions'][2] else 2
        new_axis=0 if before['dimensions'][0]>before['dimensions'][2] else 2
        rotation=np.eye(4)
        if new_axis!=old_axis:rotation[:3,:3]=[[0,0,1],[0,1,0],[-1,0,0]]
        rotated=copy.deepcopy(g)
        for scene in rotated['scenes']:
            index=len(rotated['nodes']);rotated['nodes'].append(dict(name='Authored orientation',children=scene['nodes'],matrix=rotation.T.flatten().tolist()));scene['nodes']=[index]
        bounds=audit(rotated,tail);center=(np.array(bounds['min'])+np.array(bounds['max']))/2
        t=np.array([-center[0]*s,-bounds['min'][1]*s,-center[2]*s]);transform=np.eye(4);transform[:3,:3]*=s;transform[:3,3]=t
        for scene in rotated['scenes']:
            index=len(rotated['nodes']);rotated['nodes'].append(dict(name='Authored scale and ground',children=scene['nodes'],matrix=transform.T.flatten().tolist()));scene['nodes']=[index]
        result=pack(rotated,tail);after=audit(*unpack(result))
        assert abs(after['min'][1])<1e-6 and abs(after['min'][0]+after['max'][0])<1e-6 and abs(after['min'][2]+after['max'][2])<1e-6
        assert abs(max(after['dimensions'])-max(old[id]['dimensions']))<1e-5
        assert unpack(result)[1]==tail and rotated['meshes']==g['meshes'] and rotated['materials']==g['materials']
        path=f'assets/revisions/{RELEASE}/{id}/model.glb'
        row=dict(id=id,source_glb_sha256=digest(raw),source_glb_bytes=len(raw),source_bounds=before,glb=path,glb_sha256=digest(result),glb_bytes=len(result),binary_chunk_sha256=digest(tail),buffers_images_materials_unchanged=True,uniform_scale=s,rotate_y_90=new_axis!=old_axis,translation=t.tolist(),bounds=after,historical_status=source['historical_status'],adopted=source['adopted'],scale_scope='Existing authored maximum dimension retained; illustrative asset scale, not life size or specimen metrology.')
        rows.append(row)
        if install:
            dst=ROOT/path;dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists();dst.write_bytes(result)
        print(id,'before',np.round(before['dimensions'],3),'after',np.round(after['dimensions'],3),after['triangles'])
    if install:(ROOT/f'production/{RELEASE}/integration-ledger.json').write_text(json.dumps(dict(baseline='7bcf95269a7651c47fcb25413d089ee274083c92',models=rows),indent=2)+'\n')
if __name__=='__main__':run(json.loads(pathlib.Path(sys.argv[1]).read_text()),'--install' in sys.argv)
