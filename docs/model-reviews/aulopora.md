# Aulopora: material-only readability review

Baseline: `88766ab2027881e30d563a7b3ca36182fdb071b0`. Original GLB `b02129d717acfcf59368ebdcd302ac2f113c260a8a0fd8154a5ec6f31ccda3e9` (2,413,164 bytes); original imported editable Blend `94fad87eb8e1ac7b8cbd6070a070064a4c80d7312a14bb2ef152f94fce30645f` (2,784,994 bytes). Original tracked assets are retained.

This is an existing stylized educational trumpet-network coral. Its scientific scope, unknown physical units, artistic geometry and open network are unchanged. No geometry repair, physical reconstruction or specimen certification is claimed.

## Material diagnosis

In the actual source viewer, four desktop angles and four simulated-phone angles compare default metallicFactor 1 to 0, with explicit redraw after material changes. Additional four-angle desktop controls compare 0.75 and 0.5. MeshBasicMaterial unlit diagnostics retain the actual map, baseColor factor, vertex-colour setting, side and alpha semantics; no asset is edited by these controls. Scene display uses sRGB output, ACES filmic tone mapping and exposure 1.1, unchanged from the source renderer.

The underlying colour is pale brown, while the original lit trumpet necks are near black. Metal0 makes the neck and network surface more readable while retaining shaded interiors and colour variation; 0.75/0.5 controls remain darker. This is a target-view readability decision, not a claim that ancient living colours are known. No new painted texture is introduced.

Candidate GLB `9c486116d31b520089f98c139f849c75b90bb45c38dbd5815ee592e6cf080728` changes only metallicFactor default1→0. Every other parsed JSON field and BIN/chunk byte is identical. A new paired editable Blend is imported from this exact candidate, textures packed, saved and reopened with equal recorded mesh/UV/image/material state; it is not historical original authoring source. Matching wheel/detail images are captured from the actual candidate through the current source renderer. The temporary generation site with old poster bindings is not transition acceptance evidence.

## Tests and limits

Original site: exact three-asset SHA checks, 34 desktop + 6 phone finite entry frames, original GLB HTTP200 body hash and no recorded HTTP/JS errors. Phone frame1→2 timestamp reverses 6.816ms; finite samples do not establish uninterrupted every-frame stability. Original 8/8 shared repeated-flow tests pass (two viewports, reselection after ready, late response, retry, rotation/reset).

Candidate source-built site: 34 desktop + 4 phone monotonic finite frames, correct new GLB response SHA/HTTP200 and no recorded HTTP/JS errors. Actual held/ready screenshots preserve primary position, scale, angle and material. No uninterrupted or all-pixel stability guarantee is claimed. Candidate 8/8 repeated-flow cases pass, retry requests each2, true transition-end reset with unchanged camera/target1e-4 and quaternion1e-7 thresholds. Phone dragging is simulated mouse, not physical all-touch hardware.

Focused isolation/delivery test passes: the sole metallicFactor edit, remaining JSON/BIN equality, 938 other entries unchanged at model introduction, paired source/poster hashes, and actual generated download ZIP/credits. Candidate build originated at baseline source with the now-committed candidate manifest/assets; its baseline SCOPE commit is not falsely represented as already containing those candidate edits. Independent review accepted the bounded material improvement and complete pairing.

## Unified completion

Remote introduction `f02547e03` + `242b907b32c14cc208049cd07f3d1958dec33619` equals the complete local tested tree `473eb008ecc0f469075aa9905a56bd6c0cf0a6d3` (tree `3e2d755d6c34c49bf4c712e44c1756aa8d6270fb`). Official shared scoped build, fresh dual-end held→ready screenshots and 30 + 6 monotonic finite frames verified main projection/material consistency, exact candidate GLB HTTP200 body hash and no recorded HTTP/JS errors. All 8 unified repeated-flow cases passed, retry each2, strict endpoint reset unchanged. Independent integrated visual recheck passed within those limits.

Final head `7efae6da1db12e2b5bf15c834f7b9b5d9222b5cb` adds only another model: Aulopora manifest entry/poster binding/assets and all `site/gallery` renderer code compare equal to 242b. Focused checks passed again on 7ef. Exact CI `44395354019` completed successfully, deployment skipped. Earlier 242b CI was cancelled, not counted as a pass.

Aulopora review is complete, awaiting shared release; not already deployed. Review-stage manifest flags are not production-release authorization. Original and candidate sampling/artistic limits remain applicable.
