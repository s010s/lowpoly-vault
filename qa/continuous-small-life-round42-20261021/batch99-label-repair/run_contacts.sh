#!/bin/bash
set -euo pipefail
Q=/workspace/shared/lowpoly-batch99-label-independent-qa-20261021
for a in monetianthus proterocladus; do
 PYTHONDONTWRITEBYTECODE=1 flock /tmp/lowpoly-production-blender.lock blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$Q/retained_contact_exposure_method.py" -- "$a" > "$Q/$a-contacts.log" 2>&1
 tail -5 "$Q/$a-contacts.log"
done
node "$Q/runtime.cjs" > "$Q/runtime.log" 2>&1
cat "$Q/runtime.log"
