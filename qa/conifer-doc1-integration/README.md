# Conifer doc1 integration candidate — publication preview review pending

Base: main `e6af7a7a07a600bec0a3ffa907de0e4841ff31a4`. Exact final model acceptance: `8e618be80a2624a58023cadcd508fdaf7494287c`, revision `structure-r20-a-normal16-doc1`, GLB `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`. Editable Blend/generators/config are exact accepted bytes, copied into the immutable revision folder. Current main manifest and turntable index are unchanged; no main publication performed.

The159-file accepted root contains every file actually read by the strict validator (including --previous), plus the complete current final independent QA directory. Strict model acceptance passes. Old models and failure histories remain in their original branches/recovery history; no failed model is promoted.

## Required independent preview action

The final QA README explicitly leaves the complete24alpha publication sequence and selected poster for publication-stage review. Its existing approved visual list does not contain the proposed SwiftShader poster `6296286130490b04dba1f1b4b1a7c00149cfecbc43bfeab82dd0c7b18eb0cfd4`. The integration maker therefore does not rewrite or reseal that independent record. Proposed release gate correctly refuses: `published preview is absent from approved visual evidence`.

`preview-review-request.json` identifies all24 exact768px alpha WebPs, poster and their hashes, source runtime commit/profile and unchanged doc1 GLB/brief/reference subject. Original source previews are fixed in runtime branch `b3107dc`; this proposal only changes storage namespaces, not pixels. The independent reviewer should inspect/approve the selected full sequence and poster, then issue a new independently sealed candidate record preserving model acceptance and explicit new visual bindings. This is a missing QA artifact, not a request to relax a gate or re-approve the same user permission.

`assets/releases/conifer-doc1-20261017.json` proposes the three-replacement mixed release, retaining exact arch/fern entries and all other original entries. The proposed turntable index is stored here rather than overwriting the active source index. After independent preview approval, use that reviewed record and pin to activate the descriptor/index and run full production workflow. Do not treat current active-release CI as proof that this unapproved preview proposal is released.

## Actual integrated-site review

`prepare-review.mjs` builds an explicitly REVIEW ONLY isolated tree using existing review delivery support, current compiled site/viewer, the exact accepted new conifer and candidate images/download. Other9 checked published entries/ZIPs remain unchanged in that tree. It writes neither production manifest nor active turntable index, grants no preview approval and emits no production Pages artifact. Run with `SITE_BASE=/lowpoly-vault/ SITE_ORIGIN=https://s010s.github.io node qa/conifer-doc1-integration/prepare-review.mjs`.

The conifer-targeted handoff test is an exact copy of the existing full suite with only asset/name literals changed, recorded by `handoff-test-provenance.json`; assertions are unchanged. It exercises frame7 → real GLB continuity, retained image ownership, reverse and interrupted navigation for this new asset rather than relying on the old arch test.

## Scope and compatibility

Metadata, About text and revision README retain KHR_mesh_quantization, tested Three.js0.180.0, physical M5 Pro/Metal acceptance conditions, SwiftShader frame-budget failure (including single tree) and fine-needle subpixel aliasing. Neither generic device performance nor arbitrary-loader compatibility is claimed. Existing gate and frontend behavior are unchanged. Author: Leon Made This, no-reply Git email. Final model/preview integration approval and main publication remain separate.
