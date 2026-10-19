# Independent QA: batch-42

**Content QA: PASS for all four exact, pinned assets within their frozen stylized teaching scopes. No required model repairs.** The candidate records remain unapproved. Formal profile approval is not granted: the original candidate records remain unapproved, the factual stage is not a specimen-level certification, and the available Chromium WebGL2 renderer is ANGLE SwiftShader software rendering, leaving hardware-GPU evidence unknown. No hardware-GPU or device-performance claim is made.

## Scope and identity

- Candidate source: `candidate/small-life-batch42-20261018` at `658fc5bc4a6e1c7823655ef6388c4bfbe067b67e`.
- Frozen model-source commit: `a3d499cd7a91940c171c04f6ad0b9d05d5b9d2f0`; profile: `static-stylized-v1` / `2026-10-18.1`.
- Handoff file SHA-256: `6694c2c10ebcf174f4bcca523806965d828d55278282c643380053ef93cef5d3`; QA scope SHA-256: `03c6158cf911c7b0ce218bd94d70a6a6eda5d0b81581ccfed7fe735cc2ab41ce`.
- Exact scope is `conularia`, `shale-scree`, `boudinaged-rock-layer`, and `ophiomorpha-pellet-lined-burrow` only.
- The handoff requested GPT-6 Luna / xhigh. The execution environment did not expose model metadata, so actual model identity and effort are not independently attested. This is recorded as the single requested QA round; no repeat was dispatched based on generic identity.
- Reviewed the repository `lowpoly-art-direction`, `asset-factual-review`, and `blender-lowpoly-pipeline` skills, static profile rule, and `.agents/skills/emil-animation` guidance. The animation guidance does not apply to static meshes.

## Per-asset result

| Asset | Exact GLB SHA-256 | Dimensions (m) | Triangles | Independent content conclusion | Required model fix |
|---|---|---:|---:|---|---|
| `conularia` | `e0bed18c8384590706d2ed7afdfafe2d8e22e6266133cc14971b06791f1df6ae` | `0.056403 × 0.150000 × 0.056403` | 10,396 | PASS — The continuous tapered body, four-lobed open aperture, and restrained transverse ribs read clearly in hero, reverse, front, top, clay, and runtime pixels. The 0.15 m scale is preserved. The silhouette and simple teaching form stay within the frozen Conularia-inspired scope. | None |
| `shale-scree` | `5ddbfeb0cfba1d25e60ede7b25df97842277d06814a13ec17a646c34aa88d244` | `0.850000 × 0.347084 × 0.588925` | 2,454 | PASS — The source ledge and broken bedding feed a connected slope with unequal, angular, overlapping platy fragments and smaller chips. Top, side, hero, gray, and runtime views make the shale/scree relationship legible. The blocky teaching patch reads as designed geology without claiming a locality or exact fragment count as natural fact. | None |
| `boudinaged-rock-layer` | `aba041be653b5739c87289637c1262fef96df9a00d35f06ad82683b548c066fe` | `0.850000 × 0.290949 × 0.228000` | 4,064 | PASS — Four unequal elongated lenses are readable within a continuous enclosing matrix; the necked gaps and shallow continuous foliation remain visible in hero, front, clay, and runtime pixels. Neutral-gray structure is legible. This is a sectioned teaching illustration, not a measured strain/site reconstruction. | None |
| `ophiomorpha-pellet-lined-burrow` | `4767fee02cd3be71b2f7725dcf0c070d33920c2433880357f1663ff5a75e5e3b` | `0.250000 × 0.075137 × 0.063901` | 9,984 | PASS — The continuous sectioned wall, smooth lumen, cut opening, and bonded exterior pellets are easy to read across hero, reverse, side, top, clay, and runtime views. The repeated pellet rhythm is orderly but still fits the expressly stylized teaching brief; no floating pellets or broken wall are visible. | None |

The visual conclusions cover only the stated teaching-art claims. They do not certify exact taxa, locality, age, strain, producer, or excavated specimens where those claims are outside the frozen briefs.

## Evidence checks

- `verify_handoff.py` passed all **161** pinned handoff path/hash/byte checks; the exact four IDs, candidate source, GLB pins, branch-change boundary, and one-round review policy match. The final Blend and GLB SHA-256 values match both the handoff and the frozen model-source commit.
- Each image manifest binds the exact GLB and zero turntable frames. I verified the SHA-256, byte length, and dimensions of all **8 fixed source images + 12 exact-GLB runtime images per asset** and inspected all eight original-resolution fixed views for each asset. I also opened every source/runtime contact sheet and full-size GLB runtime hero, top, small/medium-size, and six-copy scene pixels for each asset.
- The Blender 4.3.2 source-reopen/export evidence has no errors. Source/GLB triangle counts and converted bounds match; the maximum listed bounds error is at most `9.4e-10 m`. `conularia` and `ophiomorpha-pellet-lined-burrow` have automated “smooth faces require intentional-style review” warnings; the corresponding actual pixels show clean, intentional smooth forms, so these are reviewed warnings, not required repairs.
- Each recorded pair of deterministic rebuilds byte-matches the delivered GLB. Pinned Khronos validator output is **0 errors / 0 warnings** for every GLB.
- Chromium/Three.js 0.180 WebGL2 loaded the exact GLBs. Each runtime has 10 single-item views and 2 six-instance scene views with no reported scene errors or failed captures. ANGLE SwiftShader is software rendering; these results show functional loading/rendering only.
- `profile-contract-status` is `pass` and the explicit profile record is `valid=true` for all four. Each still has `approved_for_brief=false`. The preserved legacy checker remains invalid solely for its missing nonempty consulted-reference license text; the explicit consulted-only static profile does not infer or fabricate licenses.
- Factual review remains narrow: the frozen ledger records consulted sources and limitations, including constrained direct access for the KU/Connecticut material. No specimen-level scientific PASS is asserted.

## Exact evidence paths

All paths below are relative to the repository root. Each selected artifact directory contains the `.blend`, `.glb`, eight `preview-*.png` fixed images, `view-manifest.json`, and both contact sheets.

### `conularia` — content PASS

- Required model fix: **None.** The visual review does not establish exact species, soft-tissue, attachment, or specimen reconstruction. Retain the brief’s stylized/inspired framing.
- Candidate record: `production/continuous-small-life-round14-20261018/work/batch-42/conularia/r001/candidate.json`; metadata: `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/metadata.json`.
- Blend: `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/conularia.blend` (SHA-256 `790c65c831f7b08b97b073ef5d5be33adbf1a667cffd9a28f86cd01c9fbdc197`).
- GLB: `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/conularia.glb` (SHA-256 `e0bed18c8384590706d2ed7afdfafe2d8e22e6266133cc14971b06791f1df6ae`).
- Fixed-view manifest/contact sheet: `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/view-manifest.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/source-contact-sheet.jpg`.
- Runtime contact sheet/reports: `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/runtime-contact-sheet.jpg`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/runtime/single.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/conularia/r001/attempt-01/conularia/runtime/scene.json`.
- Blender source/export and rebuild evidence: `production/continuous-small-life-round14-20261018/work/batch-42/conularia/r001/source-scene.json`; `production/continuous-small-life-round14-20261018/work/batch-42/conularia/r001/source-export.json`; `production/continuous-small-life-round14-20261018/work/batch-42/conularia/r001/reproducibility.json`; Khronos `production/continuous-small-life-round14-20261018/work/batch-42/conularia/r001/khronos.txt`.
- Profile records: `production/continuous-small-life-round14-20261018/work/batch-42/conularia/r001/profile-gate.json`; preserved legacy result `production/continuous-small-life-round14-20261018/work/batch-42/conularia/r001/legacy-gate.json`.

### `shale-scree` — content PASS

- Required model fix: **None.** Layer, fragment count, thickness, tilt, and palette remain artistic choices under the frozen brief; this is not a site-specific reconstruction.
- Candidate record: `production/continuous-small-life-round14-20261018/work/batch-42/shale-scree/r001/candidate.json`; metadata: `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/metadata.json`.
- Blend: `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/shale-scree.blend` (SHA-256 `570db8405364580d4ab1b2d86a45f304191dc3e43e50c2a6a7e8525170cfd59a`).
- GLB: `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/shale-scree.glb` (SHA-256 `5ddbfeb0cfba1d25e60ede7b25df97842277d06814a13ec17a646c34aa88d244`).
- Fixed-view manifest/contact sheet: `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/view-manifest.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/source-contact-sheet.jpg`.
- Runtime contact sheet/reports: `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/runtime-contact-sheet.jpg`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/runtime/single.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/shale-scree/r001/attempt-02/shale-scree/runtime/scene.json`.
- Blender source/export and rebuild evidence: `production/continuous-small-life-round14-20261018/work/batch-42/shale-scree/r001/source-scene.json`; `production/continuous-small-life-round14-20261018/work/batch-42/shale-scree/r001/source-export.json`; `production/continuous-small-life-round14-20261018/work/batch-42/shale-scree/r001/reproducibility.json`; Khronos `production/continuous-small-life-round14-20261018/work/batch-42/shale-scree/r001/khronos.txt`.
- Profile records: `production/continuous-small-life-round14-20261018/work/batch-42/shale-scree/r001/profile-gate.json`; preserved legacy result `production/continuous-small-life-round14-20261018/work/batch-42/shale-scree/r001/legacy-gate.json`.

### `boudinaged-rock-layer` — content PASS

- Required model fix: **None.** No exact strain, locality, age, or specimen claim is established by this review.
- Candidate record: `production/continuous-small-life-round14-20261018/work/batch-42/boudinaged-rock-layer/r001/candidate.json`; metadata: `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/metadata.json`.
- Blend: `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/boudinaged-rock-layer.blend` (SHA-256 `54aafee5af3e9d2646da60b385cc8b71937e2eb8498f7fc18ca250c96b5f4571`).
- GLB: `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/boudinaged-rock-layer.glb` (SHA-256 `aba041be653b5739c87289637c1262fef96df9a00d35f06ad82683b548c066fe`).
- Fixed-view manifest/contact sheet: `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/view-manifest.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/source-contact-sheet.jpg`.
- Runtime contact sheet/reports: `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/runtime-contact-sheet.jpg`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/runtime/single.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/boudinaged-rock-layer/r001/attempt-02/boudinaged-rock-layer/runtime/scene.json`.
- Blender source/export and rebuild evidence: `production/continuous-small-life-round14-20261018/work/batch-42/boudinaged-rock-layer/r001/source-scene.json`; `production/continuous-small-life-round14-20261018/work/batch-42/boudinaged-rock-layer/r001/source-export.json`; `production/continuous-small-life-round14-20261018/work/batch-42/boudinaged-rock-layer/r001/reproducibility.json`; Khronos `production/continuous-small-life-round14-20261018/work/batch-42/boudinaged-rock-layer/r001/khronos.txt`.
- Profile records: `production/continuous-small-life-round14-20261018/work/batch-42/boudinaged-rock-layer/r001/profile-gate.json`; preserved legacy result `production/continuous-small-life-round14-20261018/work/batch-42/boudinaged-rock-layer/r001/legacy-gate.json`.

### `ophiomorpha-pellet-lined-burrow` — content PASS

- Required model fix: **None.** The reviewed source scope supports only a general smooth-interior/nodose-exterior inspired form. This is not a named-producer or exact excavated-specimen reconstruction.
- Candidate record: `production/continuous-small-life-round14-20261018/work/batch-42/ophiomorpha-pellet-lined-burrow/r001/candidate.json`; metadata: `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/metadata.json`.
- Blend: `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/ophiomorpha-pellet-lined-burrow.blend` (SHA-256 `b5e91b2ff17aeb84bfea49cde477a7c757bedc665aa425cd5b65399a942dd4e9`).
- GLB: `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/ophiomorpha-pellet-lined-burrow.glb` (SHA-256 `4767fee02cd3be71b2f7725dcf0c070d33920c2433880357f1663ff5a75e5e3b`).
- Fixed-view manifest/contact sheet: `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/view-manifest.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/source-contact-sheet.jpg`.
- Runtime contact sheet/reports: `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/runtime-contact-sheet.jpg`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/runtime/single.json`; `assets/candidates/continuous-small-life-round14-20261018/batch-42/ophiomorpha-pellet-lined-burrow/r001/attempt-02/ophiomorpha-pellet-lined-burrow/runtime/scene.json`.
- Blender source/export and rebuild evidence: `production/continuous-small-life-round14-20261018/work/batch-42/ophiomorpha-pellet-lined-burrow/r001/source-scene.json`; `production/continuous-small-life-round14-20261018/work/batch-42/ophiomorpha-pellet-lined-burrow/r001/source-export.json`; `production/continuous-small-life-round14-20261018/work/batch-42/ophiomorpha-pellet-lined-burrow/r001/reproducibility.json`; Khronos `production/continuous-small-life-round14-20261018/work/batch-42/ophiomorpha-pellet-lined-burrow/r001/khronos.txt`.
- Profile records: `production/continuous-small-life-round14-20261018/work/batch-42/ophiomorpha-pellet-lined-burrow/r001/profile-gate.json`; preserved legacy result `production/continuous-small-life-round14-20261018/work/batch-42/ophiomorpha-pellet-lined-burrow/r001/legacy-gate.json`.

## Remaining formal gate

No candidate files, model geometry, thresholds, CI, permissions, release data, or handoff records were edited. No merge, Drive action, or publication was performed. The original `approved_for_brief=false` states remain. Hardware-GPU runtime remains unknown because the available renderer is software-only; scientific claims outside the frozen stylized scope also remain unverified. If strict formal profile closure is later required, any hardware capture must bind to these exact GLB hashes. Current SwiftShader captures must remain software-only claims.

Machine-readable detail: [`independent-qa.json`](independent-qa.json).
