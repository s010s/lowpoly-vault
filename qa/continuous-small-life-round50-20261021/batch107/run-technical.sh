set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
R=/workspace/shared/lowpoly-batch107-20261021
B=$R/production/small-life-batch107
O=/workspace/shared/lowpoly-batch107-independent-qa-20261021
for id in dendrocystites trochocystites helicoplacus stromatocystites; do
 mkdir -p "$O/$id"
 flock /tmp/lowpoly-production-blender.lock blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$O/source-audit.py" -- "$B/$id/r001/artifacts/$id.blend" "$O/$id" > "$O/$id/source-reopen.log" 2>&1
 flock /tmp/lowpoly-production-blender.lock blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$B/tools/measure-components.py" -- --source "$B/$id/r001/artifacts/$id.blend" --brief "$B/$id/r001/original-brief.json" --output "$O/$id/recomputed-components.json" > "$O/$id/components.log" 2>&1
 python "$B/tools/check-original-winding.py" "$B/$id/r001/artifacts/$id.glb" "$O/$id/unmodified-glb-winding.json" > "$O/$id/winding.log" 2>&1
 cp "$B/$id/r001/artifacts/$id.glb" "$O/$id/$id.glb"
 python "$R/scripts/qa_glb.py" "$B/$id/r001/artifacts/$id.glb" --report "$O/$id/project-glb.json" --max-triangles 14000 --max-materials 6 --max-primitives 30 > "$O/$id/project-glb.log" 2>&1
 node "$R/scripts/validate_gltf.cjs" "$O/$id/$id.glb" > "$O/$id/khronos.log" 2>&1
 node "$B/tools/parse.cjs" "$O/$id/$id.glb" > "$O/$id/three.log" 2>&1
 echo "$id technical jobs complete"
done
