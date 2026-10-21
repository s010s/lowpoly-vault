#!/usr/bin/env bash
set -euo pipefail
O=/workspace/shared/lowpoly-batch97-independent-qa-20261021
for a in ginkgo dicranophyllum noeggerathia bjuvia; do
 if test -f "$O/$a/source-independent.json"; then echo "Existing result $a; no rerun"; continue; fi
 /usr/bin/flock /tmp/lowpoly-production-blender.lock /usr/bin/blender --background --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$O/inspect_source.py" -- "$a" > "$O/$a/source-independent.log" 2>&1
 echo "Completed source reopen: $a"
done
