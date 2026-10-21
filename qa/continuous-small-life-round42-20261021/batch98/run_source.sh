#!/bin/bash
set -euo pipefail
O=/workspace/shared/lowpoly-batch98-independent-qa-20261021
for a in voltzia sciadopitys agathis archaefructus; do
 flock /tmp/lowpoly-production-blender.lock blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$O/inspect_source.py" -- "$a" > "$O/$a/source-independent.log" 2>&1
 echo "source done $a"
done
