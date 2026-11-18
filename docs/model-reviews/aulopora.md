# Aulopora: material-only readability review

Baseline: `88766ab2027881e30d563a7b3ca36182fdb071b0`. Original GLB `b02129d717acfcf59368ebdcd302ac2f113c260a8a0fd8154a5ec6f31ccda3e9` (2,413,164 bytes); original imported editable Blend `94fad87eb8e1ac7b8cbd6070a070064a4c80d7312a14bb2ef152f94fce30645f` (2,784,994 bytes). Original tracked assets are retained.

This is an existing stylized educational trumpet-network coral. Its scientific scope, unknown physical units, artistic geometry and open network are unchanged. No geometry repair, physical reconstruction or specimen certification is claimed.

## Material diagnosis

In the actual source viewer, four desktop angles and four simulated-phone angles compare default metallicFactor 1 to 0, with explicit redraw after material changes. Additional four-angle desktop controls compare 0.75 and 0.5. MeshBasicMaterial unlit diagnostics retain the actual map, baseColor factor, vertex-colour setting, side and alpha semantics; no asset is edited by these controls. Scene display uses sRGB output, ACES filmic tone mapping and exposure 1.1, unchanged from the source renderer.

The underlying colour is pale brown, while the original lit trumpet necks are near black. Metal0 makes the neck and network surface more readable while retaining shaded interiors and colour variation; 0.75/0.5 controls remain darker. This is a target-view readability decision, not a claim that ancient living colours are known. No new painted texture is introduced.

Candidate GLB `9c486116d31b520089f98c139f849c75b90bb45c38dbd5815ee592e6cf080728` changes only metallicFactor default1→0. Every other parsed JSON field and BIN/chunk byte is identical. A new paired editable Blend is imported from this exact candidate, textures packed, saved and reopened with equal recorded mesh/UV/image/material state; it is not historical original authoring source. Matching wheel/detail images are captured from the actual candidate through the current source renderer. The temporary generation site with old poster bindings is not transition acceptance evidence.

## Tests and limits

Original site: exact three-asset SHA checks, 34 desktop + 6 phone finite entry frames, original GLB HTTP200 body hash and no recorded HTTP/JS errors. Phone frame1→2 timestamp reverses 6.816ms; finite samples do not establish uninterrupted every-frame stability. Original 8/8 shared repeated-flow tests pass (two viewports, reselection after ready, late response, retry, rotation/reset).

Candidate entry/regression, focused isolation/delivery, independent review, unified integration and exact CI are still pending. Not deployed.
