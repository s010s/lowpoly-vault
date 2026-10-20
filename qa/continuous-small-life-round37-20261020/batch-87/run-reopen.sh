set -euo pipefail
D=/workspace/shared/lowpoly-batch87-independent-qa-20261020
for spec in 'pleuromeia r002' 'glacier-crevasse-field r002' 'spatter-cone r004' 'travertine-terrace-pools r002'; do
 set -- $spec; mkdir -p "$D/$1"
 flock /tmp/lowpoly-production-blender.lock blender --background --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$D/reopen_measure.py" -- "$1" "$2" > "$D/$1/reopen-process.log" 2>&1
done
