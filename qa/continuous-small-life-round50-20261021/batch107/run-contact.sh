set -euo pipefail
O=/workspace/shared/lowpoly-batch107-independent-qa-20261021
B=/workspace/shared/lowpoly-batch107-20261021/production/small-life-batch107
for id in dendrocystites trochocystites helicoplacus stromatocystites; do
 flock /tmp/lowpoly-production-blender.lock blender -b --threads 2 --factory-startup --disable-autoexec --python-exit-code 1 --python "$O/independent-contact.py" -- "$B/$id/r001/artifacts/$id.blend" "$O/$id/independent-contact-exposure.json" > "$O/$id/independent-contact.log" 2>&1
 tail -3 "$O/$id/independent-contact.log"
done
