# lowpoly-vault: asset and scene budget research

Research date: 2026-10-17. Baseline repository: `s010s/lowpoly-vault` at `e4019e28354f058cd11efaf5e4529af1e957855a` (Three.js 0.180.0).

This isolated research package does not change production defaults or approve any asset. Its purpose is a reusable, evidence-based budget policy for a 1,000–10,000-asset open library and mobile/desktop Web3D museums.

## Initial verified findings

- An asset needs separate transfer, decoded geometry, texture allocation, submission, animation and visual-quality budgets. File size alone does not predict frame rate or GPU memory.
- The glTF specification is an interoperability specification. It is not a universal triangle or megabyte performance standard.
- The August 2025 Khronos Asset Creation Guidelines 2.0 summary is published, while several linked full chapters, including publishing targets, remain marked work in progress. The often repeated 5 MB / 100,000-triangle recommendation comes from the 2020 commerce guideline and is not a whole-museum budget.
- Our controlled Triceratops surface study uses 14,432 triangles throughout. Three 2K PNG maps yield 7,695,292 B and an estimated 64 MiB RGBA8+mip texture allocation. A single 512 JPEG variant is 471,784 B and about 1.33 MiB; its visual review is tracked separately. A fair no-texture control with unused tangents removed is 428,496 B, with nine primitive submissions rather than one.
- Environment experiments show why material count is not draw-call count: one material may still be used by several meshes/primitives. Many copies also multiply visible triangles even when GPU instancing reduces submissions.

## Evidence currently included

- `data/local-sample-inventory.json`: independent structural inventory of exact local GLBs, with hashes and explicit measurement limits.
- `data/official-sample-metadata.json`: pinned Khronos sample metadata, including Fox, DamagedHelmet and both FlightHelmet texture variants. No third-party asset binaries are republished here.
- `scripts/inspect_glb_samples.py`: read-only research inventory utility. Requires Pillow. Not a validator, visual reviewer or GPU profiler.

The complete report, source ledger and proposed English policy/schema are being prepared. Numerical allocation bands will be explicitly labeled project hypotheses until target-device scene benchmarks establish them.

License: prose and research data CC-BY-4.0, attribution Leon Made This / s010s; original scripts MIT. Upstream assets retain their own licenses and are referenced only.
