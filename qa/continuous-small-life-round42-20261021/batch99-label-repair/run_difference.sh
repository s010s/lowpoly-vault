#!/bin/bash
set -euo pipefail
Q=/workspace/shared/lowpoly-batch99-label-independent-qa-20261021
for a in monetianthus proterocladus; do
 PYTHONDONTWRITEBYTECODE=1 flock /tmp/lowpoly-production-blender.lock blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$Q/independent_difference.py" -- "$a" > "$Q/$a-independent-difference.log" 2>&1
 tail -6 "$Q/$a-independent-difference.log"
done
