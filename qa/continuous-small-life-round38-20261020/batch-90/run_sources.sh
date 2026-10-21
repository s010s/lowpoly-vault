set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
O=/workspace/shared/lowpoly-batch90-independent-qa-20261020
for pair in 'pertica r003' 'rosary-shaped-chambered-burrow-hormosiroidea-type r001' 'zoophycos-spiral-spreite r002' 'lumbricaria-thread-like-coprolite r001'; do
 set -- $pair; mkdir -p "$O/$1"
 flock /tmp/lowpoly-production-blender.lock /usr/bin/blender -b --factory-startup --disable-autoexec --threads 2 --python-exit-code 1 --python "$O/reopen_measure.py" -- "$1" "$2" "$O/$1" > "$O/$1/source-reopen.log" 2>&1
 echo "$1 done"
done
