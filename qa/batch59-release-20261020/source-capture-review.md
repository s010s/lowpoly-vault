# Independent seven-model source and capture-preparation review

Reviewed 2026-10-20 UTC, read-only against:
- Base: `f8a793082a2167cfc8fe5cbf1c9d7ebc742b70d1`
- Capture head: `34c4bcd7c74d0ff914f3fbe577901a42e392e037`
- Checkout: `/tmp/lowpoly-batches58-59-release-20261020`

## Outcome

PASS for exact seven-model source closure and capture-only preparation. No source-integrity, model-selection, metadata measurement, runtime mutation, or policy mutation blocker found. This is not pixel QA, final collector approval, publication acceptance, physical-GPU verification, or a live-release claim.

One concrete integration-documentation inconsistency was identified: the copied standalone package manifest is not an integrated-repository manifest. Running its `verify-package.py` in this checkout fails on `README.md`. The coordinator confirmed the manifest seals the original standalone payload, whose own README differs from the deliberately preserved main README. The correct resolution is to label the original manifest as sealed-input evidence and create a final-repository integrity record, not overwrite the main README. That final resolution is pending at the reviewed capture head.

Actual ModelStage images and the finalized collector have not been supplied, so both remain explicitly unreviewed. Remote push was outside this read-only scope and was not attempted or retried.

## Exact selection and identity

The preparation, derived release metadata, capture descriptor, candidate records and immutable independent reviews all agree on these exact revisions and GLB hashes:

| ID | Revision | GLB SHA-256 |
| --- | --- | --- |
| calamophyton | r001 | 005c21c5dfa735762fcfc65387075701ba3e24a915316e6e7c1a59a096362815 |
| perspicaris | r002 | ec95315cac17288508b02d7f3901e9a6a8e8ef464e46b44f460bba049488d35c |
| barchan-dune | r001 | 4b4580c6ed599b80865ebe9a4e506dc3d4a770077fa5f5be3ec099d3ab8a2543 |
| current-ripple-surface | r001 | 2bdae5b8730c661fe9817df41baa7e12ea5b0f91c78a245f4f13eedffcae640d |
| glacial-erratic | r002 | 94bdc5b0dddd8a3925d53ded4be6191d4769cc9414d8860d9664a8170010bfcd |
| gypsum-cave-flower | r002 | 8ddaf4c36f2fd0dbe7c3971c27c750e8c41760954a8fb25e9e40b679c24eac2b |
| stalactite-group | r002 | 6e2bf795d94dae162a65dd8cf0924d70e402e28dbb1c17917d622919d608fca7 |

Batch 58 model/QA pins: `9bb7eb242a2c7ee35868ca57789c93c06c4bcbb8` / `48f08fa3e2d6bb9a06526efd7142c4fc35184d86`.

Batch 59 model/QA pins: `330bc4aa669a1647c632a32622ce4318fd8d1b59` / `289cca9359cdd3595f7015f894a00675a004c422`.

Erbenochile is absent from additions, selected candidate directories, and capture staging. Its blocked review context is retained as evidence only. New revisions elsewhere would not alter this seven-ID decision.

## Checks executed independently

1. Verified all 629 original source-bundle files (65,026,937 bytes) against actual SHA-256, size, all listed source Git commits and their Git blob identities. No mismatch. Compared every file in each of the seven selected immutable revision directories against the bundle: none missing.
2. Checked all 677 sealed-input manifest entries against this checkout: 676 match; the sole mismatch is the standalone README explained above. All source-helper contracts themselves match.
3. Re-ran `validate_candidate.py --profile static-stylized-v1` for all seven in the integrated checkout with bytecode writes disabled: all records valid; all `approved_for_brief=false`. No formal acceptance was rewritten.
4. Independently measured all seven payload GLBs with `qa_glb.audit_glb`. All triangle/material/primitive counts and exported dimensions match release metadata. No errors. The only warning is the declared stalactite ceiling extent below origin.
5. Independently parsed the seven actual payload GLBs with Three.js `GLTFLoader.parseAsync`; all pass, have zero animations, and parsed bounds agree with release metadata within 1e-6 m.
6. Ran the capture staging script with `GALLERY_DIR` and `GITHUB_ENV` pointing solely into this report directory. It produced exactly seven checked GLBs and one capture-only manifest. All source hashes match; authority remains false; no preview image exists or is substituted.
7. The packaged verifier completed the source-bundle, seven-asset artifact/evidence, measured-GLB and 14 existing queue rebuild-record checks before reaching the README manifest mismatch. No new Blender rebuild was executed.
8. Compared 721 protected files to the supplied base: all tracked files under `site/`, `scripts/`, `schemas/`, `skills/`, and `production/policies/`, plus main manifest, image index, package/lock, Vite config and main README. All are byte-identical.
9. Worktree was clean at start and end. No worktree file was edited; report and staging outputs are outside it.

Evidence: `source-origins.json`, `source-bundle.json.audit.json`, `package-manifest.json.audit.json`, `candidate-audit-summary.json`, seven `*-candidate.json` records, `three-parser-summary.json`, `protected-scope-audit.json`, and `staging.log` / `staged/assets/manifest.json` in this directory.

## Capture workflow review

The only modified pre-existing file is `.github/workflows/publication-poster-capture.yml`; the other 649 changed paths are additions. The added files beneath `production/` are immutable source/rebuild evidence, not changed production policies or current runtime behavior.

The workflow:
- has read-only repository permissions and no commit/push/merge/deployment step;
- builds the unchanged site, then substitutes an isolated capture-only manifest, not the production manifest;
- checks the hard-coded capture-input digest, exact seven-ID set, review-report hashes, metadata hashes and GLB hashes before staging;
- rejects unsafe source paths and symlink substitutions;
- invokes the unchanged current ModelStage renderer and preset, with pinned Playwright Chromium, posters only, and PNG reference capture;
- validates pass status, renderer identity, exact seven report IDs and their source hashes;
- uploads an evidence artifact only and explicitly does not claim physical-GPU or populated-scene verification.

Dry staging passed. Actual rendering and image outputs have not been run or inspected by this reviewer. The renderer's report and index are not a replacement for independent pixel/hash/dimension checks on the final image artifact. It writes a copy of the existing image index plus new poster records, so the final integration should preserve all pre-existing index entries rather than import the whole artifact blindly.

The pull-request path filter still names previous capture payloads; this does not block the intended `capture/**` push trigger, but it is not a generic automatic trigger for future Batch58/59-only descriptor changes. Keep this capture-only workflow scoped appropriately when preparing final production integration.

## Metadata and mounting

Derived release metadata explicitly distinguishes measured exported file-space bounds from illustrative nominal dimensions and real specimen/site measurements. Labels and descriptions preserve the independent reviews' bounded stylized scopes; no locality, age or exact-specimen claim is introduced. Batch59 stale original export paths remain unchanged in original evidence and are not used as delivery authority; candidate artifact pins are authoritative.

GLB/Blend delivery bytes match original candidate exports exactly. The source helper code, licenses and CC BY attribution are retained. Preview paths are reservations with null preview hashes, and source proof/concept images have not been promoted to website posters.

Stalactite bounds are glTF Y = [-2.2894442975521088, 0]. Its derived metadata says the origin is the ceiling attachment and warns against ground-normalization. The unchanged ModelStage uses a display-only centering parent, not an edited GLTF source or flipped mount. Actual preview/detail orientation still requires pixel inspection.

## Remaining gates / limits

- Correctly label the standalone input-manifest evidence and verify the final integrated files with the promised new integration record. Do not rewrite the immutable source/policy or main README to make the standalone verifier pass.
- At this exact capture head the preserved base manifest has 194 unique assets; the package's historical expected 209 is not established. Verify the actual final integration base and additive ID/count delta rather than assuming 209.
- Review actual seven PNG/WebP image pairs, their digests/dimensions/alpha, source/preset/viewer/Chromium provenance, clipping/material/silhouette quality and stalactite orientation.
- Review the final collector/descriptor/manifest/allowlist changes and negative cases, preserving formal pending statuses and excluding Erbenochile.
- Run final gallery/detail/wheel/mobile/return/fallback and resource-count checks, exact-commit CI and eventual live/download verification under the coordinator's authority.
- This review did not inspect actual new website pixels, rerun Blender generation, execute a populated scene, verify physical GPU, or recheck remote branch/deployment state.

## Worktree coordination note

After the checks above completed, the coordinator moved this checkout to `8c15fdfc53a06b9f49e479293b3641487e82529a`. I inspected the delta to the reviewed capture head: the generic capture workflow is restored to the base bytes and the temporary `capture-only-stage.mjs` is absent. No other files differ between those two heads. The source findings therefore still apply, while the capture-workflow findings refer specifically to immutable head `34c4bcd7c74d0ff914f3fbe577901a42e392e037`, not to the now-restored source-only checkout. Both observed worktree states were clean.
