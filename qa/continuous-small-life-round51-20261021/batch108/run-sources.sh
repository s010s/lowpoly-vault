#!/bin/bash
set -u
O=/workspace/shared/lowpoly-batch108-independent-qa-20261021
for a in isorophus eleutherocrinus nucleocrinus placocystites; do
  date -u +%FT%TZ > "$O/$a/source-process-start.txt"
  flock /tmp/lowpoly-production-blender.lock blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$O/review-source.py" -- "$a" > "$O/$a/source-process.log" 2>&1
  echo $? > "$O/$a/source-process-exit.txt"
  date -u +%FT%TZ > "$O/$a/source-process-end.txt"
done
