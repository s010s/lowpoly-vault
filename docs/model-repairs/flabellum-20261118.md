# Flabellum outer-rib material repair

This exact Colab-derived live model already has a valid fan-wedge outline, dimensions and presentation pose. On the deployed material, the omitted metallic factor defaults to 1 and obscures the lower exterior ribs across multiple viewing angles. 0.65 recovers readable ribs without washing out the cup or natural lower shadows. No orientation, lighting, texture, authored scale or geometry edit; no reconstruction.

- Production comparison: GLB, editable Blend, preview, left poster and right poster matched the Git baseline byte for byte.
- Delivery: original and candidate had zero glTF validator errors/warnings; candidate differs only in metallicFactor; entire BIN matches. Candidate editable source freshly imported with packed images and reopened; geometry, UV, matrix and nonempty texture pixels match the original delivery and the exact candidate GLB.
- Render: regenerated both actual source-bound posters in the present PreviewRenderer path. For 1440 × 1000 and 390 × 844 touch simulation, independent pre-release/ready endpoint review saw no obvious subject shift, rescale, angle or material jump. Original captured 29/47 CDP frames with one timestamp reversal per viewport; candidate 37/47 with none. Eight lifecycle checks, four real GLB/Blend button downloads and both actual poster responses passed per variant.
- Scope: controlled delay and finite headless samples, not physical-phone or every-frame certification. Branch CI and unified production release are separate gates.

Structured evidence: `assets/candidates/flabellum/material-20261118/SUMMARY.json`.
