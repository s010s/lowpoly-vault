# SPDX-License-Identifier: MIT
"""Integrity and measured-contract check, never independent visual/factual approval."""
import sys,json,hashlib
from pathlib import Path
from PIL import Image
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'));from qa_glb import audit_glb,read_glb
s=sys.argv[1];b=Path(__file__).resolve().parent;w=b/s/'r001';r=json.loads((w/'candidate.json').read_text());errors=[]
def read(p):return json.loads(p.read_text())
def check(entry):
 p=ROOT/entry['path'];assert p.is_file(),p;assert p.stat().st_size==entry['bytes'],p;assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],p;return p
try:
 for e in list(r['artifacts'].values())+list(r['technical_evidence'].values()):check(e)
 glb=check(r['artifacts']['glb']);audit=audit_glb(glb,14000,6,30);assert not audit['errors'];assert audit['bytes']<=1000000
 gltf,binary,_raw=read_glb(glb);assert len(gltf.get('images',[]))<=1
 from io import BytesIO
 encoded=0;decoded=0
 for image in gltf.get('images',[]):
  view=gltf['bufferViews'][image['bufferView']];raw=binary[view.get('byteOffset',0):view.get('byteOffset',0)+view['byteLength']];pic=Image.open(BytesIO(raw));assert max(pic.size)<=256;encoded+=len(raw);decoded+=pic.width*pic.height*4
 assert encoded<=65536 and decoded<=524288
 manifest=read(check(r['technical_evidence']['views']));assert manifest['glb_sha256']==audit['sha256'] and manifest['turntable_frames']==0
 frames=manifest['frames'];assert len(frames)==20
 for e in frames:
  p=check(e);im=Image.open(p);assert im.size==(e['width'],e['height'])
 for e in manifest['sheets']:check(e)
 for key in ['runtime','scene']:
  q=read(check(r['technical_evidence'][key]));assert q['glb_sha256']==audit['sha256'] and q['status']=='pass' and not q['errors'] and not q['failed']
  assert q['three']=='180' and 'SwiftShader' in q['renderer']
  assert all(v['triangles']==audit['scene_triangles']*q['instances'] for v in q['views'])
  for v in q['views']:assert hashlib.sha256((glb.parent/'runtime'/v['path']).read_bytes()).hexdigest()==v['sha256']
 q=read(check(r['technical_evidence']['two_rebuilds']));assert q['delivered_glb_sha256']==audit['sha256'];assert len(q['runs'])==2
 for run in q['runs']:
  p=ROOT/run['result_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==run['result_sha256'];result=read(p);request=read(p.parent/'request.json');assert result['status']=='succeeded';assert request['identity']['inputs']['generator']['sha256']==r['artifacts']['generator']['sha256'];assert request['identity']['inputs']['config']['sha256']==r['artifacts']['config']['sha256'];assert run['semantic_match'];assert audit_glb(ROOT/run['glb_path'],14000,6,30)['semantic_sha256']==audit['semantic_sha256']
 q=read(check(r['technical_evidence']['source_export']));assert q['source_sha256']==r['artifacts']['source']['sha256'] and q['glb_sha256']==audit['sha256'] and q['triangles_match'] and q['bounds_match']
 q=read(check(r['technical_evidence']['source_scene']));assert q['source_sha256']==r['artifacts']['source']['sha256'] and q['status']=='pass'
 q=read(check(r['technical_evidence']['khronos']));assert q['issues']['numErrors']==q['issues']['numWarnings']==0
 assert r['approval']['status']=='pending';assert all(x['status']=='unknown' for x in r['stages'].values())
except Exception as exc:errors.append(str(exc))
report={'status':'pass' if not errors else 'fail','scope':'Frozen practical-contract file integrity and measured maker checks only; independent acceptance pending. Legacy candidate checker profile incompatibility is separately recorded.','asset_id':s,'candidate_sha256':hashlib.sha256((w/'candidate.json').read_bytes()).hexdigest(),'glb_sha256':r['artifacts']['glb']['sha256'],'errors':errors,'independent_qa':'pending parent GPT-6 Luna xhigh'}
(w/'practical-integrity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));sys.exit(bool(errors))
