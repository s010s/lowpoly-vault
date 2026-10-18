# Executed QA commands and pins

Working repository: `/tmp/lowpoly-batch11-qa`. Read-only candidate snapshot: `/tmp/batch11-candidate-review`. QA worktree was created at `0bd62cda92814af5ac781e1a706bba6310cecc35`; exact remote candidate ref was `7394fef092feb21ab9c084f331cfdf35a86979aa`.

## Pin and extract the source candidate

```sh
git fetch origin refs/heads/main:refs/remotes/origin/main refs/heads/candidate/small-life-batch11-20261018:refs/remotes/origin/candidate/small-life-batch11-20261018
git ls-remote origin refs/heads/candidate/small-life-batch11-20261018 refs/heads/main
git archive 7394fef092feb21ab9c084f331cfdf35a86979aa | tar -x -C /tmp/batch11-candidate-review
```

Each `candidate_checkpoint_sha` in `HANDOFF.json` was checked as an ancestor of the exact source SHA with `git merge-base --is-ancestor`.

## Recomputed frozen inputs and evidence frames

```sh
python3 production/continuous-small-life-round04-20261018/work/batch-11/qa-independent/verify_frozen.py \
  /tmp/batch11-candidate-review \
  production/continuous-small-life-round04-20261018/work/batch-11/qa-independent/evidence/frozen-input-audit.json
```

Result: all four assets pass; no missing, byte-count, hash, frame, runtime-pin, or freeze mismatch.

## Current static profile and project GLB audit

For each asset, the current validator was run with the explicit profile and exact frozen sidecar. Example (`micrabacia`; the same command ran for the other IDs and outputs are committed beside this file):

```sh
python3 scripts/validate_candidate.py \
  /tmp/batch11-candidate-review/production/continuous-small-life-round04-20261018/work/batch-11/micrabacia/r001/candidate.json \
  --root /tmp/batch11-candidate-review \
  --profile static-stylized-v1 \
  --profile-contract /tmp/batch11-candidate-review/production/continuous-small-life-round04-20261018/work/batch-11/micrabacia/r001/profile-contract.json \
  --json
```

The baseline audit ran with the brief's unchanged caps (`14000` triangles, `6` materials, `30` primitives):

```sh
python3 scripts/qa_glb.py /tmp/batch11-candidate-review/assets/candidates/continuous-small-life-round04-20261018/batch-11/micrabacia/r001/attempt-01/micrabacia/micrabacia.glb \
  --max-triangles 14000 --max-materials 6 --max-primitives 30 \
  --report /tmp/batch11-micrabacia-qa-glb.json
```

Equivalent paths were used for Sengelia `attempt-01`, Coquina `attempt-02`, and Naraoia `attempt-01`.

## Official Khronos validator

The validator package was installed outside the repository at its recorded pinned version; exact GLB copies under `/tmp/batch11-khronos` were validated so the input snapshot remained untouched.

```sh
npm install --prefix /tmp/batch11-validator-deps --cache /tmp/batch11-npm-cache \
  --ignore-scripts --no-audit --no-fund --no-save gltf-validator@2.0.0-dev.3.10
NODE_PATH=/tmp/batch11-validator-deps/node_modules \
  node scripts/validate_gltf.cjs /tmp/batch11-khronos
```

All four returned 0 errors and 0 warnings. Per-file validator and summary JSONs are in this evidence directory.

## Blend reopen and exact GLB import

The committed `reopen_compare_blend_glb.py` was run once per source/GLB pair using Blender 4.3.2, with auto-execution disabled and two threads. Example:

```sh
blender -b --disable-autoexec -t 2 --python-exit-code 1 \
  --python production/continuous-small-life-round04-20261018/work/batch-11/qa-independent/reopen_compare_blend_glb.py -- \
  micrabacia \
  /tmp/batch11-candidate-review/assets/candidates/continuous-small-life-round04-20261018/batch-11/micrabacia/r001/attempt-01/micrabacia/micrabacia.blend \
  /tmp/batch11-candidate-review/assets/candidates/continuous-small-life-round04-20261018/batch-11/micrabacia/r001/attempt-01/micrabacia/micrabacia.glb \
  production/continuous-small-life-round04-20261018/work/batch-11/qa-independent/evidence/micrabacia-blend-glb.json
```

Substitute the matching IDs and selected attempt directories for the other three. The reports include recomputed Blend/GLB hashes, source/imported counts, per-object bounds, source boundary/non-manifold/degenerate counts, and exact comparison results; console logs are stored as `*-blender.log`.
