#!/bin/bash
set -euo pipefail
OUT=/workspace/shared/lowpoly-batch89-independent-qa-20261020
for pair in psilophyton:r001 rosselia-concentrically-filled-burrow:r002 skolithos-pipe-field:r001 teichichnus-spreite-wall:r003; do
 id=${pair%:*}; rev=${pair#*:}; mkdir -p "$OUT/$id"
 flock /tmp/lowpoly-production-blender.lock blender --background --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$OUT/reopen_measure_reexport.py" -- "$id" "$rev" "$OUT/$id" > "$OUT/$id/own-source-reopen-reexport.log" 2>&1
 tail -3 "$OUT/$id/own-source-reopen-reexport.log"
done
