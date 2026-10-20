#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
qa_root="qa/batch52-independent-20261020"
run_root="${QA_RUN_DIR:-$qa_root}"
mkdir -p "$run_root/technical"

while IFS=: read -r id revision stem; do
  candidate="assets/candidates/continuous-small-life-round18-20261020/batch-52/$id/$revision"
  blender --background --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 \
    --python scripts/check_source_export.py -- \
    --source "$candidate/$stem.blend" \
    --glb "$candidate/$stem.glb" \
    --output "$run_root/technical/$id-source-export.json"
  blender --background --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 \
    --python "$qa_root/blender-import-audit.py" -- \
    --source "$candidate/$stem.blend" \
    --glb "$candidate/$stem.glb" \
    --output "$run_root/technical/$id-blender-import.json"
done <<'EOF'
aturia:r002:aturia
phoenicopsis:r001:phoenicopsis
cave-popcorn:r003:cave-popcorn
curvolithus-trilobed-trail:r001:curvolithus-trilobed-trail
EOF

python3 scripts/validate_candidate.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002/candidate.json \
  --root . --profile static-stylized-v1 \
  --profile-contract assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002/profile-contract.json \
  --json > "$run_root/technical/aturia-candidate-validation.json"
python3 scripts/validate_candidate.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/candidate.json \
  --root . --profile static-stylized-v1 \
  --profile-contract assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/profile-contract.json \
  --json > "$run_root/technical/phoenicopsis-candidate-validation.json"
python3 scripts/validate_candidate.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/candidate.json \
  --root . --profile static-stylized-v1 \
  --profile-contract assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/profile-contract.json \
  --json > "$run_root/technical/cave-popcorn-candidate-validation.json"
python3 scripts/validate_candidate.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/candidate.json \
  --root . --profile static-stylized-v1 \
  --profile-contract assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/profile-contract.json \
  --json > "$run_root/technical/curvolithus-trilobed-trail-candidate-validation.json"

python3 scripts/validate_concept_evidence.py \
  concept-evidence.json \
  --root assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002 > "$run_root/technical/aturia-concept-evidence.json"
python3 scripts/validate_concept_evidence.py \
  assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/concept-evidence.json \
  --root . > "$run_root/technical/phoenicopsis-concept-evidence.json"
python3 scripts/validate_concept_evidence.py \
  concept-evidence.json \
  --root assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003 > "$run_root/technical/cave-popcorn-concept-evidence.json"
python3 scripts/validate_concept_evidence.py \
  production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concept-evidence.json \
  --root . > "$run_root/technical/curvolithus-trilobed-trail-concept-evidence.json"

for entry in \
  "aturia:assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002/concept-evidence.json" \
  "phoenicopsis:assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/concept-evidence.json" \
  "cave-popcorn:assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/concept-evidence.json" \
  "curvolithus-trilobed-trail:production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concept-evidence.json"; do
  id="$(printf '%s' "$entry" | cut -d: -f1)"
  path="$(printf '%s' "$entry" | cut -d: -f2-)"
  set +e
  if [[ "$id" == aturia || "$id" == cave-popcorn ]]; then
    asset_root="assets/candidates/continuous-small-life-round18-20261020/batch-52/$id/$([[ "$id" == aturia ]] && echo r002 || echo r003)"
    record="concept-evidence.json"
  else
    asset_root="."
    record="$path"
  fi
  python3 scripts/validate_concept_evidence.py "$record" --root "$asset_root" --require-complete \
    > "$run_root/technical/$id-concept-evidence-require-complete.json" 2>&1
  rc=$?
  set -e
  printf '%s\n' "$rc" > "$run_root/technical/$id-concept-evidence-require-complete.exit"
done
