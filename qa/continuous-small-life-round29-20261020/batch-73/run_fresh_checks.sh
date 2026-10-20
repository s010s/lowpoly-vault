#!/usr/bin/env bash
set -euo pipefail
OUT=/workspace/shared/lowpoly-round29-qa73
REPO=/workspace/shared/lowpoly-batch73-20261020
BASE="$REPO/production/continuous-small-life-round29-20261020/work/batch-73"
python "$OUT/static_source_audit.py" > "$OUT/static_source_audit.stdout.log" 2> "$OUT/static_source_audit.stderr.log"
node "$OUT/check_exact_glbs.cjs" > "$OUT/khronos.stdout.log" 2> "$OUT/khronos.stderr.log"
for pair in 'fractofusus r002' 'striated-bedrock r003' 'fumarole-vent r003' 'banded-iron-formation r003'; do
  read -r id rev <<< "$pair"
  src="$BASE/assets/$id/$rev/source.blend"
  glb="$BASE/assets/$id/$rev/model.glb"
  dest="$OUT/source_exports/$id-$rev.glb"
  mkdir -p "$OUT/source_exports"
  flock -x /tmp/lowpoly-production-blender.lock /usr/bin/blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python "$OUT/reopen_export.py" -- --asset "$id" --source "$src" --shipped-glb "$glb" --output "$dest" > "$OUT/source_exports/$id-$rev.blender.log" 2>&1
 done
# Copy only the exact four immutable GLBs into the isolated dirs expected by the pinned Node parser.
python - <<'PY'
import pathlib,shutil
r=pathlib.Path('/workspace/shared/lowpoly-batch73-20261020/production/continuous-small-life-round29-20261020/work/batch-73/assets')
out=pathlib.Path('/workspace/shared/lowpoly-round29-qa73/node-three-inputs')
for ident,rev in [('fractofusus','r002'),('striated-bedrock','r003'),('fumarole-vent','r003'),('banded-iron-formation','r003')]:
 d=out/f'{ident}-{rev}';d.mkdir(parents=True,exist_ok=True);shutil.copyfile(r/ident/rev/'model.glb',d/'model.glb')
PY
node "$REPO/production/continuous-small-life-round29-20261020/work/batch-73/runtime-parse.mjs" "$OUT"/node-three-inputs/* > "$OUT/three-parse.stdout.log" 2> "$OUT/three-parse.stderr.log"
