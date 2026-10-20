# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,subprocess,datetime,time
R=Path.cwd();W=R/'production/small-life-batch80';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
# This checker deliberately makes no raster inspection assertion.
p=W/'check-physical-surfaces.py';t=p.read_text().replace('Actual original32 final views separately inspected for raster artifacts.','Actual raster inspection is separately recorded; this report checks geometry only.');p.write_text(t)
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];args=['flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','-b','--factory-startup','--disable-autoexec','--threads','2','--python-exit-code','1','--python',str(p),'--',str(b)]
 start=now();begin=time.monotonic()
 with (b/'physical-surfaces.log').open('w') as log:subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=300)
 print('PHYSICAL',x['asset_id'],time.monotonic()-begin,flush=True)
 d=dict(created_at=now(),files={str(q.relative_to(R)):H(q) for q in [b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py',R/'scripts/check_source_export.py',R/'scripts/check_reproducibility.py',R/'scripts/rebuild_frozen_blender.py',R/'scripts/run_asset_queue.py',W/'render-fixed8.py',W/'runtime-parse.mjs',p]},blender={'version':'4.3.2','executable':'/usr/bin/blender','sha256':H(Path('/usr/bin/blender'))},runtime_dependency={'source':'Existing read-only /workspace/shared/lowpoly-landair-web-integration/node_modules','three_version':'0.180.0','three_package_sha256':H(R/'node_modules/three/package.json'),'gltf_validator_package_sha256':H(R/'node_modules/gltf-validator/package.json')},seed=80,external_source_media_incorporated=False)
 (b/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
