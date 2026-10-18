# Batch 08 independent QA commands

- `git fetch origin refs/heads/handoff/batch08-20261018:refs/remotes/origin/handoff/batch08-20261018 <four exact candidate refs>` — acquired the handoff and four candidate branches.
- `git worktree add -b qa/independent-batch08-20261018 /tmp/lowpoly-batch08-qa 421ffc94a7fbe00664ddc5d78f7696e5e766831b` — isolated reviewer branch rooted at the handoff commit.
- For each frozen source snapshot, `(cd <bundle> && sha256sum -c checksums.sha256)` — all entries verified.
- `python scripts/validate_candidate.py <snapshot>/assets/candidates/continuous-small-life-round03-20261018/batch-08/<asset>/r001/candidate.json --root <snapshot> --json` — all four returned invalid because the listed reference source(s) have no required nonempty `license` field.
- `python scripts/qa_glb.py <snapshot>/.../<asset>.glb --max-triangles 14000 --max-materials 6 --max-primitives 30 --report /tmp/<asset>-qa-glb.json` — static-uncompressed profile; zero errors/warnings for all four at their unchanged brief budgets (14,000 triangles, 6 materials, 30 primitives).
- `npm install --prefix /tmp/batch08-validator-deps --cache /tmp/npm-cache-batch08 --ignore-scripts --no-audit --no-fund --no-save gltf-validator@2.0.0-dev.3.10` — installed the pinned official validator outside the repository.
- `NODE_PATH=/tmp/batch08-validator-deps/node_modules node scripts/validate_gltf.cjs /tmp/batch08-validator-input/<asset>/<asset>.glb` — official Khronos Validator 2.0.0-dev.3.10 returned 0 errors / 0 warnings for all exact GLB hashes; raw outputs are retained here.
- `blender -b --disable-autoexec -t 2 --python-exit-code 1 --python production/continuous-small-life-round03-20261018/work/batch-08/independent-evidence/reopen-blend-glb.py -- /tmp/batch08-blender-manifest.json /tmp/batch08-blender-roundtrip.json` — freshly reopened each Blend and imported each exact GLB in Blender 4.3.2; geometry counts and bounds agree.

All visual images in `images/` are byte-identical copies from the candidate commit paths recorded in `visual-evidence.json`. Review images were opened at original resolution; they were not altered. No model file, threshold, CI or permission setting was changed.
