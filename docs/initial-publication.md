# Initial collection publication

The owner requested publication of the redesigned Pages site and the ten existing originals on 2026-10-17. Further artistic and scientific refinement remains ongoing. This is permission to publish the initial collection, not final-quality approval.

- Source snapshot: `550ac6b1d4477d1fbd85ea9f8eb69502b20a42a7`. Original geometry, authored scale, GLB and Blender bytes are unchanged.
- `assets/initial-publication.json` seals exactly ten IDs and the paths and SHA-256 of every GLB, Blender source and preview. Additional models need a new explicit publication decision.
- `assets/manifest.json` is generated explicitly by `node site/initial-release.mjs`. Build and CI only verify it; they do not generate approval.
- `npm run publication:check` requires the committed manifest to equal the current authorized source. Source/GLB/Khronos checks must pass. The strict `npm run manifest:check` gate is unchanged and remains distinct. Historical `threejs_runtime: not_run` records are not rewritten.
- Technical browser verification runs on the actual build. Strict software-WebGL and deliberately unavailable-WebGL profiles are separate; neither is physical-phone or hardware-GPU evidence.
- Deployment uses `/lowpoly-vault/` and `https://s010s.github.io`. Twenty localized detail pages plus six localized home/list/about pages are real HTML.
- Full-output allowlist auditing excludes QA, research, experimental sources and private archives from Pages. Public files include ten original GLBs, ten Blender files, ten previews and ten deterministic ZIPs with byte-checked originals and credits.
- Models and previews: CC BY 4.0. Original website code: MIT. Credit Leon Made This / s010s.

The historical redesign acceptance report describes the pre-publication checkpoint. This document records the later initial-publication decision.
