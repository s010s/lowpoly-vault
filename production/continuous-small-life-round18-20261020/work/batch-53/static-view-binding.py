# SPDX-License-Identifier: MIT
"""Documented metadata adapter: actual +X camera is static profile's side view.
Retains raw renderer outputs; copies exact rendered images, never synthesizes pixels.
"""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parents[4];s=sys.argv[1];o=R/'assets/candidates/continuous-small-life-round18-20261020/batch-53'/s/'r001';v=o/'views';out=o/'views-static';out.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
raw=json.loads((v/'render-manifest.json').read_text());config=json.loads((v/'render-config.json').read_text());names=['hero','reversehero','front','side','rear','top','clay','silhouette'];frames=[]
for f in raw['frames']:
 if f['id'] not in names:continue
 q=dict(f)
 if q['id']=='side':
  assert q['view']=='right' and q['angle_degrees']==[90,0];q['view']='side'
 shutil.copy(v/q['path'],out/q['path']);assert sha(out/q['path'])==q['sha256'];frames.append(q)
assert len(frames)==8
cfg=dict(config);cfg['frames']=[{k:f[k] for k in ['id','view','angle_degrees']} for f in frames];cfg['metadata_adapter_note']='Derived static-profile view tags; side is actual +X camera azimuth90/elevation0. Raw renderer uses right. Extra claytop remains in raw views, outside exact-eight profile.';put(out/'render-config.json',cfg)
manifest=dict(raw);manifest.update(frames=frames,frame_count=8,render_config={'path':'render-config.json','sha256':sha(out/'render-config.json')},config_sha256=sha(out/'render-config.json'),total_encoded_bytes=sum(f['byte_length'] for f in frames),decoded_rgba_bytes_estimate=sum(f['width']*f['height']*4 for f in frames));put(out/'render-manifest.json',manifest)
put(out/'derivation.json',{'source_manifest':{'path':str((v/'render-manifest.json').relative_to(R)),'sha256':sha(v/'render-manifest.json')},'derived_manifest_sha256':sha(out/'render-manifest.json'),'transform':'Copy exact actual-render PNG bytes. Adapt geometric right tag to declared side for +X canonical camera. Select eight fixed views; no pose, framing, lighting, geometry or pixel changes. Optional gray-top remains separately available.','images_identical':True,'all_poses_preserved':True,'not_independent_approval':True})
print(s,'static-eight manifest derived from actual proof without pixel or pose changes')
