import pathlib,json,struct,hashlib,collections,datetime,sys,numpy as np
W=pathlib.Path('/workspace/shared/lowpoly-batch102-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch102-independent-qa-20261021')
def decode(path):
 raw=path.read_bytes();magic,ver,total=struct.unpack_from('<III',raw);assert magic==0x46546c67 and ver==2 and total==len(raw);n=12;doc=None;binary=None
 while n<len(raw):
  size,kind=struct.unpack_from('<II',raw,n);chunk=raw[n+8:n+8+size];n+=8+size
  if kind==0x4e4f534a:doc=json.loads(chunk)
  elif kind==0x004e4942:binary=chunk
 def acc(ix):
  a=doc['accessors'][ix];view=doc['bufferViews'][a['bufferView']];typ={5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']];num={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];size=np.dtype(typ).itemsize;off=view.get('byteOffset',0)+a.get('byteOffset',0);return np.ndarray((a['count'],num),dtype=typ,buffer=binary,offset=off,strides=(view.get('byteStride',size*num),size)).copy()
 def mat(node):
  if 'matrix'in node:return np.array(node['matrix']).reshape(4,4).T
  x,y,z,w=node.get('rotation',[0,0,0,1]);R=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]]);M=np.eye(4);M[:3,:3]=R@np.diag(node.get('scale',[1,1,1]));M[:3,3]=node.get('translation',[0,0,0]);return M
 triangles=[];prims=0
 def walk(i,parent):
  nonlocal prims
  node=doc['nodes'][i];m=parent@mat(node)
  if 'mesh'in node:
   for p in doc['meshes'][node['mesh']]['primitives']:
    assert p.get('mode',4)==4;prims+=1;v=acc(p['attributes']['POSITION']).astype(float);v=np.c_[v,np.ones(len(v))]@m.T;ix=acc(p['indices']).ravel()if'indices'in p else np.arange(len(v));triangles.extend([tuple(tuple(float(x)for x in v[j,:3])for j in t)for t in ix.reshape(-1,3)])
  for c in node.get('children',[]):walk(c,m)
 for root in doc['scenes'][doc.get('scene',0)]['nodes']:walk(root,np.eye(4))
 return raw,doc,triangles,prims
for aid in ['arborea','swartpuntia','coronacollina','echmatocrinus']:
 rev={'arborea':'r003','swartpuntia':'r002','coronacollina':'r001','echmatocrinus':'r002'}[aid];p=W/'production/small-life-batch102'/aid/rev/'artifacts'/f'{aid}.glb';raw,doc,tt,prims=decode(p);edge=collections.defaultdict(list);parent=list(range(len(tt)))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for i,t in enumerate(tt):
  for a,b in zip(t,t[1:]+t[:1]):
   key=tuple(sorted([a,b]));edge[key].append((i,1 if(a,b)==key else-1))
 for refs in edge.values():
  for j,_ in refs[1:]:parent[root(j)]=root(refs[0][0])
 cs=collections.defaultdict(list)
 for i in range(len(tt)):cs[root(i)].append(i)
 stats=[]
 for ids in cs.values():
  ids=set(ids);ee=[refs for refs in edge.values()if refs[0][0]in ids];arr=np.array([tt[i]for i in ids]);volume=float(np.einsum('ij,ij->i',arr[:,0],np.cross(arr[:,1],arr[:,2])).sum()/6);area=np.linalg.norm(np.cross(arr[:,1]-arr[:,0],arr[:,2]-arr[:,0]),axis=1)/2;bad=[e for e in ee if len(e)!=2 or sum(r[1]for r in e)!=0];stats.append({'triangles':len(ids),'edge_count':len(ee),'boundary':sum(len(e)==1 for e in ee),'nonmanifold':sum(len(e)>2 for e in ee),'same_direction':sum(len(e)==2 and e[0][1]==e[1][1]for e in ee),'bad_edges':len(bad),'zero_area_triangles':int(sum(area==0)),'signed_volume_m3':volume,'closed_outward':not bad and volume>0 and not any(area==0)})
 arr=np.array(tt).reshape(-1,3);h=hashlib.sha256(raw).hexdigest();r={'asset_id':aid,'revision':rev,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'glb_sha256':h,'triangle_count':len(tt),'primitives':prims,'materials':len(doc.get('materials',[])),'textures':len(doc.get('textures',[])),'glb_bytes':len(raw),'world_bounds_gltf_m':{'min':arr.min(axis=0).tolist(),'max':arr.max(axis=0).tolist(),'size':np.ptp(arr,axis=0).tolist()},'closed_connected_solids':len(stats),'solids':stats,'all_closed_consistently_outward':all(s['closed_outward']for s in stats),'no_bfont':not any('bfont'in n.get('name','').lower()for n in doc.get('nodes',[])),'material_flags':[{'alphaMode':m.get('alphaMode','OPAQUE'),'doubleSided':m.get('doubleSided',False)}for m in doc.get('materials',[])],'original_unchanged':raw==p.read_bytes(),'method':'Independent binary decoder reads original indices and transformed float positions. Bit-exact position edges reconstruct flat-normal/material seams without welding or editing. Two opposite incidents, positive signed volume and no zero-area triangles required per edge-connected solid; no virtual repair.'};(O/aid/'binary-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(aid,len(stats),r['all_closed_consistently_outward'])
