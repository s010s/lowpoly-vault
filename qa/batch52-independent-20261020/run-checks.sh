#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
qa_root="qa/batch52-independent-20261020"
run_root="${QA_RUN_DIR:-$qa_root}"
mkdir -p "$run_root/technical"

python3 scripts/qa_glb.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002/aturia.glb \
  --report "$run_root/technical/aturia-static.json" --max-triangles 14000 --max-materials 6 --max-primitives 30
python3 scripts/qa_glb.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/phoenicopsis.glb \
  --report "$run_root/technical/phoenicopsis-static.json" --max-triangles 14000 --max-materials 6 --max-primitives 30
python3 scripts/qa_glb.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/cave-popcorn.glb \
  --report "$run_root/technical/cave-popcorn-static.json" --max-triangles 14000 --max-materials 6 --max-primitives 30
python3 scripts/qa_glb.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/curvolithus-trilobed-trail.glb \
  --report "$run_root/technical/curvolithus-trilobed-trail-static.json" --max-triangles 14000 --max-materials 6 --max-primitives 30

node "$qa_root/format-check.mjs"
node "$qa_root/runtime-scene.mjs"
