# Reproduction commands

Run in a clean checkout with Blender 4.3.2, Python 3, Node, Chromium, and Three.js r180 / Playwright available.

```sh
# Fetch the handoff commit and create the isolated QA worktree.
git fetch origin dc58b12e0aa3dce39fbef23754dafa3408276235
git worktree add -b qa/s010s/small-life-batch07-20261018 /tmp/batch07-qa FETCH_HEAD
cd /tmp/batch07-qa

# Fetch the four exact candidate branches recorded by final-handoff.jsonl.
git fetch origin \
  refs/heads/candidate/batch07-syringopora-20261018:refs/remotes/origin/candidate/batch07-syringopora-20261018 \
  refs/heads/candidate/batch07-vauxia-20261018:refs/remotes/origin/candidate/batch07-vauxia-20261018 \
  refs/heads/candidate/batch07-halimeda-20261018:refs/remotes/origin/candidate/batch07-halimeda-20261018 \
  refs/heads/candidate/batch07-isoxys-20261018:refs/remotes/origin/candidate/batch07-isoxys-20261018

# Extract each frozen bundle from its exact commit. Run from /tmp/batch07-qa.
mkdir -p /tmp/batch07-candidates
for spec in \
  'syringopora d0894b30b0fbeedb4d946d0d976a4e98abeb5aff' \
  'vauxia fd443ffd5eb8342a11956a574ab11bf73bd5a0ea' \
  'halimeda 5ea23624b9e56ccfc4b6700ef9b54774bc5acd6c' \
  'isoxys c017f7acec8027555cadf5a754fa982478bab9f8'; do
  set -- $spec
  id=$1
  commit=$2
  out=/tmp/batch07-candidates/$id
  mkdir -p "$out"
  git archive "$commit" "assets/candidates/continuous-small-life-round03-20261018/batch-07/$id/r001" | tar -x -C "$out"
done

report=production/continuous-small-life-round03-20261018/reviews/batch-07/independent-gpt6-luna-xhigh
for id in syringopora vauxia halimeda isoxys; do
  cand=/tmp/batch07-candidates/$id/assets/candidates/continuous-small-life-round03-20261018/batch-07/$id/r001
  mkdir -p "$report/checks/$id"
  python scripts/qa_glb.py "$cand/$id.glb" --report "$report/checks/$id/qa-glb.json"
  python scripts/validate_candidate.py "$cand/candidate.json" --root "/tmp/batch07-candidates/$id" --json \
    > "$report/checks/$id/candidate-integrity.json" 2> "$report/checks/$id/candidate-integrity.stderr" || true
  blender --background --factory-startup --python-exit-code 1 \
    --python scripts/check_glb_roundtrip.py -- "$cand/$id.glb" \
    --output-dir "/tmp/batch07-roundtrip/$id" --samples 32 --resolution 512 \
    > "$report/checks/$id/blender-roundtrip.log" 2>&1
  blender --background "$cand/$id.blend" --python-exit-code 1 \
    --python "$report/audit_source_blend.py" -- "$report/checks/$id/source-blend-audit.json" \
    > "$report/checks/$id/source-blend-audit.log" 2>&1
  (cd "$cand" && sha256sum -c checksums.sha256) > "$report/checks/$id/bundle-checksums.log" 2>&1
  BATCH07_NODE_MODULES=/tmp/batch02-deps/node_modules node \
    "$report/checks/runtime-medium.mjs" "$cand/$id.glb" \
    "$report/checks/$id/runtime-medium" > "$report/checks/$id/runtime-medium.log" 2>&1
done
```

`validate_candidate.py` exits nonzero for the four source metadata records because the required `license`/`reference-only` property is absent. Its JSON output is preserved under `checks/<id>/candidate-integrity.json`. The other commands and their outputs are preserved under `checks/<id>/`.

The `runtime-medium.mjs` runner is a one-view copy of the submitted Three.js runtime setup with a 512 × 512 viewport and orthographic fit scale 2.0, giving roughly 210 px of projected maximum extent. The handoff runtime's 9-copy view uses fit scale 4.7, roughly 89 px per copy. The screenshots use ANGLE SwiftShader and are functional rendering evidence, not physical-device performance data. The source and runtime contact sheets were assembled from the hash-verified committed PNG evidence with Python 3.12 and Pillow 12.3.0.
