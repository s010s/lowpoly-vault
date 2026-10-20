# Batch 61 scale-metadata differential QA

Review date: 2026-10-20 UTC  
Scope: targeted metadata-only differential review of Daemonelix, mesa and drumlin. This is not a repeat of the original four-model QA.

## Result

The three corrected `scale_note` strings are suitable, and the original frozen records and geometry artifacts are preserved. However, all three new carry-forward render manifests change their top-level `subject.brief_sha256` to the corrected v002 delivery brief, even though the images were rendered with the old v001 brief. The original subject is recorded in a nested carry-forward field, and each manifest clearly discloses no rerender, but the top-level subject remains materially misleading and does not meet the handoff requirement to retain the exact old render subject. Keep all three geological candidates `BLOCKED` pending correction of that binding.

## Pins and source preservation

Reviewed clean local HEAD `c15ccbb5bc0fa0890fad5b68856eb653645e571d`, parent/baseline `faa9090270732d1c770a807607fe5e34db8908eb`; original model HEAD remains `f1737e4f00dfc5c1817084ecb31763320ec2a163`. The repair commit adds exactly 26 files and modifies/deletes zero prior files. Handoff SHA-256 is `0a25dc54235bcaa822ab534b58e3f7d5f039aa182b347fc7059f4efec5ffbe17`. The `preserved-original-files.json` inventory lists 273 prior files; independently compared every listed file against the baseline and current commit, all 273 hashes match. Archived original QA and machine results match the handoff hashes. Pseudopulex remains unchanged at its original exact GLB, Blend and delivery-brief pins; its earlier `ACCEPT_BOUNDED` finding is carried forward without re-review.

Each corrected geological delivery brief differs from the original delivery brief only at `/scale_note`. Correction records bind the exact original wrong value and brief hash, the original frozen brief and modeling-freeze hashes, and the corrected brief hash. The original design briefs, frozen claims, references, source Blends, generators, configs, GLBs and old manifests are unchanged. Nominal art-planning dimensions are distinguished from actual Blender/glTF mesh bounds. Corrected values are asset-specific: exposed burrow-cast envelope, broad capped geological-form envelope, and low rounded elongated glacial-landform envelope. No new geometry, ImageGen, rebuild, render or runtime test was performed.

The new candidate, profile-contract and validation records bind to the corrected brief and unchanged GLB/source/reference/generator/config pins. Each integrity check is valid and the profile contract passes, but approval remains pending, `approved_for_brief` is false, and all required stages remain `unknown`. GPU and scene stages remain unrun.

## Remaining blocker: render subject rebinding

The original render manifests correctly bind their old brief hash. The copied v002 manifests preserve frame pixels, frame dimensions/camera angles/timestamps, render config, original `created_at`, GLB and reference hashes. They also state `metadata-only-evidence-adapter-not-a-new-render`, retain the exact old subject under `evidence_carry_forward.original_render_subject`, and disclose that the original render did not test the correction. But their top-level `subject.brief_sha256` has been replaced with the corrected brief hash:

| Asset | Original rendered brief hash | Incorrect top-level v002 manifest subject | New manifest SHA-256 |
|---|---|---|---|
| Daemonelix r002 | `2fcfd328842918ca9e1bc75bbb542692960c9a1f0644eb678bd8cca5a5056896` | `721ad77bfd1600cadda06b178a571f439c957c00f19ba1263d307f9e40449ac4` | `560d1cd3a72374b62762cc1e556d5d3e48a18b55266a861fc369ba749782898d` |
| mesa r002 | `4bf4e45bce74a19ba20ef2d8f658d08358c702ad0bb449055732434489f346cf` | `63de5d1f262ba10b471dba0587139685a141ca2105c5efdf77c8eee5a69798cd` | `12a18c4cc6767911d99ebd15f1138c58eb5f7ada2e9a4fa884c840a21c532560` |
| drumlin r002 | `12ddf48322e3b644df06d7df62a15a4272ed1a7bd5df680fe6e8ed2ed169ad6a` | `106e2bbd77cd9e7c69be89311af1aebb4dad808b1e25a40da0a98e3fded3da43` | `46bfa4cde845784e07c497f3019806370b01d4f632503ac5e68109bf9a439ae0` |

Exact paths are `assets/candidates/continuous-small-life-round23-20261020/batch-61/<asset>/r002/proof-final/render-manifest-scale-v002.json` in the reviewed commit. Although nested provenance accurately records the old render subject, consumers commonly treat the top-level `subject` as authoritative. Binding it to v002 can make the carried images appear to be fresh renders against corrected metadata. The explicit no-rerender text helps, but does not resolve the contradictory subject field.

The current validator imposes a real dependency: `scripts/validate_candidate.py::check_subject` requires the render-manifest subject to exactly equal the current candidate revision, GLB, brief and reference hashes (`check_render_manifest` around line 403; evidence subject check around line 629). Therefore, simply restoring the original v001 subject while leaving the v002 candidate pointed at that manifest would fail strict candidate integrity as stale evidence. Do not bypass or weaken this validator.

### Valid repair paths

1. Preserve the v001 render manifest and candidate as historical evidence, and represent the scale-note correction with a separate, explicitly typed non-render specification/correction record bound to the v002 candidate. Do not list the old images as a new v002 render or claim they validate the corrected wording. Keep v002 visual stage unknown/pending unless valid current-subject visual evidence is produced. Re-run focused candidate validation to ensure the chosen evidence types and subjects meet the existing strict contract.
2. Or genuinely rerender the unchanged, exact GLB under the corrected v002 delivery metadata, recording real new render times and pixels. The new manifest may then truthfully bind its top-level subject to v002. Keep the old v001 manifest untouched.

Either path must preserve the old render subject/timestamps/pixel hashes in the historical v001 record. A focused differential check of only these metadata/evidence bindings is sufficient; no geometry rebuild or full batch review is indicated.

## Evidence files

- Machine-readable result: `results.json`
- Assertion log: `checks.log`
- The checked-in maker handoff and proofs are in `/tmp/lowpoly-batch61-20261020/production/continuous-small-life-round23-20261020/work/batch-61/metadata-scale-v002/`.

No repository file was modified by this review. Outputs are confined to `/tmp/lowpoly-round23-qa61-scale-v002`.
