#!/bin/bash
set -euo pipefail
OUT=/workspace/shared/lowpoly-batch93-independent-qa-20261020
for pair in 'omphalophloios r004' 'chaloneria r001' 'nathorstiana r002' 'diplopora r002'; do
 read -r aid rev <<< "$pair"
 mkdir -p "$OUT/$aid"
 date -u +%FT%TZ > "$OUT/$aid/queued-at.txt"
 flock /tmp/lowpoly-production-blender.lock blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python "$OUT/audit_source.py" -- "$aid" "$rev" > "$OUT/$aid/reopen-reexport.log" 2>&1
 tail -5 "$OUT/$aid/reopen-reexport.log"
done
