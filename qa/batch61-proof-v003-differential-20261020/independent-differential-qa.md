# Batch 61 fresh-render metadata differential QA

Date: 2026-10-20 UTC  
Scope: focused review of the corrected delivery-brief and genuine render-only repair for Daemonelix, mesa and drumlin. This is not a full batch review or formal approval.

## Outcome

`ACCEPT_BOUNDED` for the three corrected v003 delivery records, limited to the corrected specification binding and fresh fixed-view render evidence. The earlier independent geometry, visual, factual and technical findings carry forward because the exact original GLB and Blend hashes remain unchanged. Candidate acceptance flags were not changed: each current candidate gate is integrity-valid, but `approved_for_brief` is false, approval is pending, and all stage statuses remain unknown. GPU and composed-scene checks remain unrun.

## Exact reviewed commits and preservation

- Baseline containing the prior source and rejected v002 metadata: `896563bfcbc70f160edf29b84dacfc824536be6a`.
- Initial fresh-render work: `013e48e352a2eb4b34c5770862eec5bbbf7bea9a`.
- Completed render payload: `439ef387e3acd4e2413bcd2a9f001feed6165d1c`.
- Final local HEAD: `e2ed7b0b13a850f2663a6701fa28edc6ffef6951`, parent is the payload commit; branch is `candidate/small-life-batch61-concept-20261020`, worktree clean.
- Diff from baseline: exactly 65 additive paths, zero modified/deleted prior files.
- All 488 entries in `original-byte-preservation-v003.json` independently match their baseline and current-HEAD SHA-256. This includes prior model assets, old v001/v002 proof records, the rejected carry-forward manifests and archived QA. Pseudopulex is unchanged; its earlier `ACCEPT_BOUNDED` result is carried forward without an art or geometry re-review.

## Genuine fresh render verification

I cross-checked the run JSONs, exact argv, Blender binary and input files, stdout hashes and saved-frame log lines against each v003 render manifest. The runs invoked Blender 4.3.2 in clean background mode on the exact existing GLB, the corrected `candidate-brief-scale-v002.json`, and the pinned references; each wrote to its new `proof-scale-v003` directory using the fixed eight views, 512×512 resolution and zero turntable frames. The recorded Blender binary SHA-256 (`0dfe9af0f3e67643ecf15327fa5e14e7315f61d1a81afdcafe76a71b1918e2b4`) matched `/usr/bin/blender`; each run returned 0 and its stdout log hash matched the run record. Logs show GLB import, per-view `Saved:` output and completion. Three distinct Blender PIDs ran sequentially with no overlap.

| Asset | Blender PID | UTC run interval | Corrected brief SHA-256 | Unchanged GLB SHA-256 | New manifest SHA-256 |
|---|---:|---|---|---|---|
| Daemonelix r002 | 33 | 09:05:13.135633–09:05:31.047461 | `721ad77bfd1600cadda06b178a571f439c957c00f19ba1263d307f9e40449ac4` | `c415fbe405e75ac182bb39512ea33b43f81d574723263f04378422fb0221aa82` | `ffaf205a273244c7c6a7eae0e3c37a947829f22f3ce1e544df12ba0acb6a349e` |
| mesa r002 | 63 | 09:05:31.255396–09:05:55.294374 | `63de5d1f262ba10b471dba0587139685a141ca2105c5efdf77c8eee5a69798cd` | `399e9fb78b225cd808563598485888ea343b568e8bc2cac8b427939fc94f1cad` | `9ae6cf2a196a4ca4414c691ce0d0d12dd2c657a578a78819e903a4fc6dc1f10e` |
| drumlin r002 | 93 | 09:05:55.506986–09:06:07.863015 | `106e2bbd77cd9e7c69be89311af1aebb4dad808b1e25a40da0a98e3fded3da43` | `317dee38ec731d1939985a61fd431238a188b5be34dfcc717dafe23dc4bd7534` | `60e14ae97a99bf4d0d7499775016d4c2fa66061d77b84407d12b62bb09de69fe` |

For each new manifest, its top-level subject now matches the corrected v002 brief, exact existing GLB and references. Its `created_at` falls within the corresponding real run interval and differs from the old render timestamp. Every manifest contains eight 512×512 fixed views. All 24 new PNG hashes and byte lengths match their files, and each actual Blender stdout log confirms saving the named frames to the new v003 path.

I independently decoded all old and new PNGs to RGBA and compared their pixel buffers: all 24 pairs are exactly identical. All 24 newly encoded PNG byte hashes differ from their old counterparts. This is consistent with a real rerender of unchanged geometry and settings, not merely re-pointing the old manifest; the independent runner command, input hashes, timestamps and saved-output logs also support the fresh-run claim. The maker’s inspection ledger reports all three new 2048×1060 contact sheets opened and inspected; I did not repeat the full visual review because decoded pixels exactly match the previously inspected frames.

## Corrected candidate/profile bindings and limits

Each `candidate-proof-v003.json` binds the corrected delivery brief and new v003 render-manifest hash, while retaining exact original GLB/Blend/reference/generator/config pins and linking the rejected v002 record as predecessor. Each profile contract binds the exact candidate file hash and `static-stylized-v1` rule `2026-10-18.1`. The associated validation reports are `valid: true`, `profile_contract_status: pass`, `approved_for_brief: false`, and `approval_status: pending`. All stage statuses remain `unknown`, as before; the repair makes no formal reviewer, maker, release, GPU or scene claim.

The original specification-only problem is resolved by the already-verified asset-specific v002 `scale_note` corrections. New v003 render manifests refer to those exact corrected-brief hashes while old v001 manifests and the rejected v002 carry-forward records remain preserved unchanged. No geometry/source rebuild, new ImageGen, Pseudopulex render, validator/CI/site change, remote push or publication occurred. Full new proof output measured `6,989,165` bytes against a `20,000,000`-byte budget. The three new renders are Cycles CPU views only; target GPU hardware and composed-scene checks remain not run.

## QA artifacts

- Machine-readable findings: `results.json`
- Exact check log: `checks.log`
- Audit script: `audit.py`
- Source render handoff: `/tmp/lowpoly-batch61-20261020/production/continuous-small-life-round23-20261020/work/batch-61/render-proof-v003/HANDOFF-proof-v003.md`

All reviewer-generated outputs are confined to `/tmp/lowpoly-round23-qa61-proof-v003`; no source or approval record was modified.
