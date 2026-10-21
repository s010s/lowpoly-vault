#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$HERE/../.." && pwd)
OUTPUT=${1:?Pass a new isolated output directory.}
python3 - "$ROOT" "$HERE" "$OUTPUT" <<'PY'
from pathlib import Path
import sys,json,hashlib
root,here,out=map(Path,sys.argv[1:]);select=json.loads((here/'final-selection.json').read_text());asset=root/select['path'];deps=json.loads((asset/'build-dependencies.json').read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not out.exists(),'Output already exists: preserve evidence and choose a new directory.'
for name,sha in deps['files'].items():assert h(root/name)==sha,name
pins=json.loads((asset/'candidate.json').read_text())['artifacts']
for key in ['generator','config']:assert h(root/pins[key]['path'])==pins[key]['sha256'],key
assert select['asset_id']=='ernietta'
print(asset)
PY
ASSET=$(python3 -c 'import json,sys;from pathlib import Path;root=Path(sys.argv[1]);d=json.loads(Path(sys.argv[2]).read_text());print(root/d["path"])' "$ROOT" "$HERE/final-selection.json")
flock /tmp/lowpoly-production-blender.lock /usr/bin/blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python "$ASSET/generator.py" -- --config "$ASSET/build-config.json" --output "$OUTPUT"
python3 "$ROOT/scripts/check_reproducibility.py" --glb "$ASSET/model.glb" --rebuilt-glb "$OUTPUT/model.glb" --generator "$ASSET/generator.py" --config "$ASSET/build-config.json" --root "$ROOT" --output "$OUTPUT/semantic-comparison.json"
