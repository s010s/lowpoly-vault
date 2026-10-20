#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
run_id="$(date -u +%Y%m%dT%H%M%S%NZ)"
export QA_RUN_DIR="${QA_RUN_DIR:-qa/batch52-independent-20261020/replay-$run_id}"
mkdir -p "$QA_RUN_DIR"
sha256sum -c production/continuous-small-life-round18-20261020/work/batch-52/checksums.sha256 \
  > "$QA_RUN_DIR/production-checksum-verification.txt"
python3 qa/batch52-independent-20261020/record-inputs.py \
  --output "$QA_RUN_DIR/pinned-inputs.json"
bash qa/batch52-independent-20261020/run-checks.sh
bash qa/batch52-independent-20261020/run-source-audits.sh
printf 'Replay evidence: %s\n' "$QA_RUN_DIR"
