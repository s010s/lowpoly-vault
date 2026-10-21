import os,sys,json,hashlib,struct,collections,datetime
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
O=Path(__file__).parent;W=Path('/workspace/shared/lowpoly-batch106-monograptus-repair-20261021');B=W/'production/small-life-batch106/monograptus';R=B/'r005';h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sys.path.insert(0,str(W/'scripts'))
from qa_glb import audit_glb
from validate_candidate import validate_candidate

def decode(path):
 raw=path.read_bytes();magic,version,total=struct.unpack_from('<III',raw);assert magic==0x46546c67 and version==2 and total==len(raw);at=12;chunks={}
 while at<len(raw):
  size,typ=struct.unpack_from('<II',raw,at);chunks[typ]=raw[at+8:at+8+size];at+=8+size
 doc=json.loads(chunks[0x4e4f534a]);binary=chunks[0x004e4942]
 def acc(i):
  a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];assert 'sparse' not in a;ctype={5120:'b',5121:'B',5122:'h',5123:'H',5125:'I',5126:'f'}[a['componentType']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];fmt='<'+ctype*n;size=struct.calcsize(fmt);stride=v.get('byteStride',size);start=v.get('byteOffset',0)+a.get('byteOffset',0);return [struct.unpack_from(fmt,binary,start+j*stride) for j in range(a['count'])]
 records=[];positions=[]
 def visit(i,parent):
  n=doc['nodes'][i]
  if 'matrix' in n:local=np.array(n['matrix']).reshape((4,4),order='F')
  else:
   q=n.get('rotation',[0,0,0,1]);x,y,z,w=q;rot=np.array([[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]]);local=np.eye(4);local[:3,:3]=rot@np.diag(n.get('scale',[1,1,1]));local[:3,3]=n.get('translation',[0,0,0])
  mat=parent@local;normalmat=np.linalg.inv(mat[:3,:3]).T
  if 'mesh' in n:
   for pr in doc['meshes'][n['mesh']]['primitives']:
    assert pr.get('mode',4)==4;vv=[tuple((mat@np.array([*v,1]))[:3]) for v in acc(pr['attributes']['POSITION'])];nn=[tuple(normalmat@np.array(v)) for v in acc(pr['attributes']['NORMAL'])];ii=[x[0] for x in acc(pr['indices'])]
    for off in range(0,len(ii),3):
     tri=tuple((vv[j],nn[j]) for j in ii[off:off+3]);records.append((pr['material'],min(tri,tri[1:]+tri[:1],tri[2:]+tri[:2])));positions.append(tuple(vv[j] for j in ii[off:off+3]))
  for child in n.get('children',[]):visit(child,mat)
 for i in doc['scenes'][doc.get('scene',0)]['nodes']:visit(i,np.eye(4))
 return doc,collections.Counter(records),positions
ad,at,ap=decode(B/'r004/artifacts/monograptus.glb');bd,bt,bp=decode(R/'artifacts/monograptus.glb');removed=list((at-bt).elements());added=list((bt-at).elements());plane=0.02516326867043972
# Decode exact coincident exported seams, without rounding or a geometric weld.
ed=collections.defaultdict(list);vol=[];deg=[]
for i,t in enumerate(bp):
 av,bv,cv=map(np.array,t);vol.append(float(np.dot(av,np.cross(bv,cv))/6));deg.append(float(np.linalg.norm(np.cross(bv-av,cv-av)))==0)
 for x,y in zip(t,t[1:]+t[:1]):ed[tuple(sorted((x,y)))].append((x,y,i))
adj=collections.defaultdict(set)
for es in ed.values():
 for e in es:
  for f in es:adj[e[2]].add(f[2])
left=set(range(len(bp)));islands=[]
while left:
 seed=left.pop();part={seed};todo=[seed]
 while todo:
  for j in adj[todo.pop()]&left:left.remove(j);part.add(j);todo.append(j)
 islands.append({'triangles':len(part),'signed_volume_m3':sum(vol[j] for j in part)})
top={'triangles':len(bp),'closed_islands':islands,'nonmanifold_edges':sum(len(x)!=2 for x in ed.values()),'same_direction_edges':sum(len(x)==2 and x[0][:2]==x[1][:2] for x in ed.values()),'degenerate_triangles':sum(deg)};top['pass']=not any(top[k] for k in ['nonmanifold_edges','same_direction_edges','degenerate_triangles']) and len(islands)==21 and all(x['signed_volume_m3']>0 for x in islands)
r={'status':'PASS','old_sha256':h(B/'r004/artifacts/monograptus.glb'),'new_sha256':h(R/'artifacts/monograptus.glb'),'old_triangles':sum(at.values()),'new_triangles':sum(bt.values()),'identical_oriented_position_normal_material_triangles':sum((at&bt).values()),'removed_triangles':removed,'added_triangles':added,'changed_triangles_all_on_or_below_old_plane':all(v[0][1]<=plane for _,tri in removed+added for v in tri),'materials_identical':ad['materials']==bd['materials'],'nodes_identical':ad['nodes']==bd['nodes'],'scene_identical':ad['scenes']==bd['scenes'],'original_glb_topology':top,'method':'Reviewer-owned GLB binary decoder; exact accessor positions, transformed normals, material IDs and cyclic oriented triangle multisets. No coordinate rounding, welding tolerance, renormalization, winding repair or altered geometry.'};assert r['identical_oriented_position_normal_material_triangles']==3084 and len(removed)==4 and len(added)==16 and all(r[k] for k in ['changed_triangles_all_on_or_below_old_plane','materials_identical','nodes_identical','scene_identical']) and top['pass'];(O/'decoded-glb-and-topology.json').write_text(json.dumps(r,indent=2)+'\n')
project=audit_glb(R/'artifacts/monograptus.glb',max_triangles=14000,max_materials=6,max_primitives=30);candidate=validate_candidate(str((R/'candidate.json').relative_to(W)),W,None,'static-stylized-v1',str((R/'profile-contract.json').relative_to(W)));(O/'project-validation.json').write_text(json.dumps({'audit':project,'candidate':candidate},indent=2)+'\n');assert not project['errors'] and candidate['valid'],candidate
chains=[]
for lab in ['a','b']:
 reqpath=R/f'qa/rebuild-{lab}-request.json';exepath=R/f'qa/rebuild-{lab}-execution.json';respath=R/f'qa/rebuild-{lab}-result.json';req=json.loads(reqpath.read_text());exe=json.loads(exepath.read_text());res=json.loads(respath.read_text());out=Path(exe['argv'][exe['argv'].index('--output')+1]);run=out.parent.parent;assert req['argv'][0]=='/usr/bin/flock' and req['argv'][1]=='/tmp/lowpoly-production-blender.lock';assert req['identity']['threads']==2;fp=hashlib.sha256(json.dumps(req['identity'],sort_keys=True,separators=(',',':')).encode()).hexdigest();assert req['fingerprint']==res['fingerprint']==fp;assert res['status']=='succeeded' and res['returncode']==0;assert req['created_at']<=res['started_at']<=exe['started_at']<=exe['finished_at']<=res['finished_at'];inputs=[];outputs=[]
 for name,r0 in req['identity']['inputs'].items():
  p=Path(r0['path']);assert h(p)==r0['sha256'] and p.stat().st_size==r0['bytes'];inputs.append({'name':name,**r0})
 for rel,r0 in res['outputs'].items():
  p=out.parent/rel;assert h(p)==r0['sha256'] and p.stat().st_size==r0['bytes'];outputs.append({'path':str(p),'inode':p.stat().st_ino,**r0})
 glb=out/'monograptus/monograptus.glb';assert glb.read_bytes()==(R/'artifacts/monograptus.glb').read_bytes();assert glb.stat().st_ino!=(R/'artifacts/monograptus.glb').stat().st_ino;logs=[]
 for p in run.glob('*.log'):
  logs.append({'path':str(p),'sha256':h(p),'bytes':p.stat().st_size,'contains_blender':('Blender' in p.read_text(errors='replace'))})
 assert logs,run
 chains.append({'job':lab,'request_sha256':h(reqpath),'execution_sha256':h(exepath),'result_sha256':h(respath),'actual_generator_pid':exe['pid'],'queue_pid':res['pid'],'started_at':exe['started_at'],'finished_at':exe['finished_at'],'separate_output_directory':str(out),'output_glb_sha256':h(glb),'inputs_verified':inputs,'all_retained_outputs_verified':outputs,'retained_logs':logs,'pass':True})
assert chains[0]['actual_generator_pid']!=chains[1]['actual_generator_pid'] and chains[0]['finished_at']<chains[1]['started_at'];assert chains[0]['separate_output_directory']!=chains[1]['separate_output_directory'];(O/'two-rebuild-chains.json').write_text(json.dumps({'status':'PASS','fresh_duplicate_generation_needed':False,'chains':chains,'scope':'Retained two actual distinct-process rebuild chains independently verified against raw separate outputs, request fingerprint, exact generator/config/input hashes, successful result and chronology; no new queue or rebuild jobs.'},indent=2)+'\n');print('PASS decoded',r['old_triangles'],r['new_triangles'],r['identical_oriented_position_normal_material_triangles'],'project valid',candidate['valid'],'chains',len(chains))
