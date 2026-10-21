#!/bin/bash
set -euo pipefail
R=/workspace/shared/lowpoly-batch106-20261021/production/small-life-batch106
O=/workspace/shared/lowpoly-batch106-independent-qa-20261021
for spec in didymograptus:r004 monograptus:r004 diplograptus:r009 dictyonema:r005; do
 a=${spec%:*}; r=${spec#*:}; mkdir -p "$O/$a"
 flock /tmp/lowpoly-production-blender.lock blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python "$O/inspect_source.py" -- "$R/$a/$r/artifacts/$a.blend" "$O/$a" > "$O/$a/source-inspection.log" 2>&1
 echo "$a completed"; tail -3 "$O/$a/source-inspection.log"
done
