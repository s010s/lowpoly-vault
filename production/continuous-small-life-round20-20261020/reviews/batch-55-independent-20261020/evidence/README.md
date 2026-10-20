# Reproducing batch-55 independent QA evidence

Run from a clean checkout of `candidate/small-life-batch55-concept-20261020` at pinned commit `b2341debdb31f73e0719d4aadbe832321db6008a`. The QA evidence directory is `production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020`; set `QA` to that path and `ROOT` to the checkout root. All source models and GLBs remain in the candidate commit and are hash-pinned in `evidence/asset-binding.json`.

Requirements used for this review: Blender 4.3.2, Node.js with the candidate commit's lockfile (`three` 0.180.0, `gltf-validator` 2.0.0-dev.3.10, `playwright` 1.56.1), and headless Chromium at `/usr/bin/chromium`. The browser harness launches Chromium with ANGLE/SwiftShader flags and confirms the unmasked renderer string. This is software rendering.

```bash
ROOT=$(git rev-parse --show-toplevel)
QA=production/continuous-small-life-round20-20261020/reviews/batch-55-independent-20261020
TMP=/tmp/batch55-reproduce
mkdir -p "$TMP"
python3 "$QA/evidence/build-binding.py" --repo "$ROOT"
python3 "$QA/evidence/reproduce-static-audit.py" --repo "$ROOT" --output "$TMP/static-audit.json"
```

For each final subject, use its bundle path from `production/continuous-small-life-round20-20261020/batch-55-QA-SCOPE.json` and run:

```bash
blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 \
  --python scripts/check_source_export.py -- \
  --source "$BUNDLE/$ASSET.blend" --glb "$BUNDLE/$ASSET.glb" \
  --output "$TMP/$ASSET-source-export.json"

blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 \
  --python production/continuous-small-life-round20-20261020/work/batch-55/source-metrics.py -- \
  --source "$BUNDLE/$ASSET.blend" --out "$TMP/$ASSET-source-metrics.json"

blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 \
  --python "$QA/evidence/blender-import-glb.py" -- \
  "$BUNDLE/$ASSET.glb" "$TMP/$ASSET-glb-reopen.json"
```

The first command freshly opens the editable `.blend`, compares the export collection to the pinned GLB, checks triangles and Blender-Z-up to GLB-Y-up bounds, and never saves either file. The second reports evaluated source-mesh topology. The third imports the exact GLB into a clean Blender scene and independently measures imported geometry, materials and bounds.

To reproduce Khronos validation without writing reports into candidate bundles, install the locked dependencies, copy the four pinned GLBs into a temporary directory, and validate those copies:

```bash
npm ci --ignore-scripts --no-audit --no-fund
for ASSET in vermicularia weichselia ventifact pentichnus-deep-dwelling-trace; do
  case "$ASSET" in
    pentichnus-deep-dwelling-trace) REV=r002 ;;
    *) REV=r001 ;;
  esac
  BUNDLE="$ROOT/assets/candidates/continuous-small-life-round20-20261020/batch-55/$ASSET/$REV"
  mkdir -p "$TMP/validator/$ASSET"
  cp "$BUNDLE/$ASSET.glb" "$TMP/validator/$ASSET/$ASSET.glb"
  node scripts/validate_gltf.cjs "$TMP/validator/$ASSET/$ASSET.glb"
done
```

The formal evidence-only checkers can be rerun as follows. Their results do not approve candidate records:

```bash
for ASSET in vermicularia weichselia ventifact pentichnus-deep-dwelling-trace; do
  case "$ASSET" in
    pentichnus-deep-dwelling-trace) REV=r002 ;;
    *) REV=r001 ;;
  esac
  BUNDLE="$ROOT/assets/candidates/continuous-small-life-round20-20261020/batch-55/$ASSET/$REV"
  python3 scripts/validate_candidate.py "$BUNDLE/candidate.json" --root "$ROOT" \
    --profile static-stylized-v1 --profile-contract "$BUNDLE/profile-contract.json" --json
  (cd "$BUNDLE" && python3 "$ROOT/scripts/validate_concept_evidence.py" concept-evidence.json --root "$BUNDLE")
done
```

To repeat Three.js loading and software WebGL rendering:

```bash
node "$QA/evidence/reproduce-webgl.cjs" "$ROOT" "$TMP/webgl"
```

It writes four individual renders, a synthetic four-asset smoke-scene render and `software-webgl-report.json`. The smoke scene is not a target production scene. Neither it nor SwiftShader can establish physical-GPU performance or a production scene pass.

`evidence/asset-binding.json`, `evidence/static-audit.json`, the per-stage outputs in `../independent-qa.json`, the captured source/export, Khronos and browser reports, and PNG hashes preserve the recorded results. The Pentichnus-specific `pentichnus-generator-r001-r002.diff` and `pentichnus-r002-repair-note.md` accompany the old/new topology metrics. The ImageGen provider timestamp/model/seed and exact generator-authoring start remain unknown and are intentionally not reconstructed from filesystem times.
