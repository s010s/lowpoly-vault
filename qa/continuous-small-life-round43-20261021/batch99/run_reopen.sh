#!/bin/bash
set -euo pipefail
Q=/workspace/shared/lowpoly-batch99-independent-qa-20261021
for a in monetianthus quereuxia palaeocarpinus proterocladus; do
 /usr/bin/flock /tmp/lowpoly-production-blender.lock /usr/bin/blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$Q/reopen_geometry.py" -- "$a" > "$Q/$a-reopen.log" 2>&1
 tail -5 "$Q/$a-reopen.log"
done
