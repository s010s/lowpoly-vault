# Independent QA: lowpoly-vault batch 68

**Reviewer:** GPT-6 Luna xhigh  
**Review date:** 2026-10-20  
**Target:** `candidate/small-life-batch68-concept-20261020`  
**Pinned producer revision:** `5dee4300e53732cd137d87f9dfa1d761bf5b66b0`  
**Worktree:** `/workspace/shared/lowpoly-batch68-20261020` (clean at review)

## Disposition

Three candidates pass this bounded independent review. **lava-dome r001 is REVISE**: despite technical validity and improvement over the retained diagnostic, its exact final pixels still show a circumferential horizontal belt/ring of angular blocks around a relatively smooth, bare summit. This materially conflicts with the brief's explicit “no mechanical belt” requirement. Overall batch disposition is **REVISE**, not accept.

No formal user/release approval is granted or inferred. GPU rendering and application-scene integration were not run; no CPU render, Khronos validation, or Three.js parse is treated as GPU/scene evidence.

## Per-asset stages

| Asset / exact final GLB SHA-256 | Technical | Visual | Factual | Specification | Runtime parse | GPU | Scene |
|---|---|---|---|---|---|---|---|
| thaumaptilon / `5f4108c4b97377bd2df41273672c16e6e9d7295a5e7d6710b4bdf0ad2b22bf42` | PASS | PASS, bounded | PASS, morphology-only | PASS | PASS | NOT RUN | NOT RUN |
| sandstone-fin / `20d94267de302a60886dcfa05aaa4bb41450f42e5e60caa29203a451cf039905` | PASS | PASS, bounded | PASS, generic form | PASS | PASS | NOT RUN | NOT RUN |
| lava-dome / `ec4eee3edc6b6cfd676bc9cb75bff04611afd7ebcd63bf6c279a46d539a159f8` | PASS | **REVISE** | PASS, generic form | **REVISE** | PASS | NOT RUN | NOT RUN |
| ice-wedge-polygon-ground / `a5eaa19f0f0d4f1de495974fbed3d360ce5ebb0c97b973f95a224b01a30a1f7d` | PASS | PASS, bounded | PASS, landform-only | PASS | PASS | NOT RUN | NOT RUN |

## Review performed

- Read the round27 production addendum, prior QA process example, batch handoff and handoff evidence, final verification/binding records, all four frozen briefs/configurations/reference ledgers, repair freezes/observations, candidate manifests, lifecycle records, and reproducibility receipts.
- Verified the pinned clean branch and source inventory against base. The unmodified original inventory SHA-256 is `b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c`.
- Independently inspected all four original generated concepts and all **32 exact final images** (eight per candidate, each 512×512) at full resolution, plus four contact sheets. Checked each image's manifest hash and binding to the final GLB. The views are hero, reversehero, front, side, rear, top, clay, and silhouette. Exact per-image hashes are in `independent-static-checks.json`.
- Read the source descriptions and inspected actual source pixels, not only thumbnails or producer summaries. The consulted images are held outside the repository and are verified as absent from delivered/repository assets. The rights ledgers mark every consulted source as not incorporated and state that no third-party photograph, art, scan, mesh, or texture is redistributed.
- Independently reopened each exact `.blend` source in Blender 4.3.2 in read-only mode, under a separate blocking `flock /tmp/lowpoly-production-blender.lock` per job and `--threads 2`. Pre/post hashes match. Per-source reopen JSON and logs are in this directory.
- Independently parsed the exact delivered GLBs with Khronos glTF Validator 2.0.0-dev.3.10 and Three.js 0.180.0 GLTFLoader. All four had zero Khronos errors and warnings; Three.js parsed the expected meshes/geometry. See `independent-runtime-checks.json`.
- Validated two existing distinct successful producer rebuild receipts for each exact final asset. Each pair has different request/result hashes, PIDs, start/finish times and fingerprints, while the final GLB bytes and semantic fingerprints match. Both rebuilds reproduced the exact final bytes. The queued jobs specify locked Blender execution and two threads; the dome and polygon receipts correspond to their retained diagnostic-repair rebuilds. No redundant producer builds were run.
- Confirmed all assets are within budgets: each GLB is under 1 MB, each is below 14,000 triangles, each has four materials, at most six primitives, and no textures. Exact byte, triangle, primitive, vertex, bounds, and receipt data are in `independent-static-checks.json`.
- Prior failed dome and polygon attempts and their diagnostic evidence remain present. No attempt/history erasure was observed.

## Per-asset observations and disposition

### thaumaptilon — PASS, bounded

The model reads as one narrow, continuous whole-organism frond with central axial relief, shallow connected oblique lateral structures, and a small blunt basal attachment. It does not depict separate leaflets, modern sea-pen tentacles, or a large sea-pen bulb. Some relief is schematic and its flattened silhouette is somewhat feather/leaf-like, but the continuous sheet and common-base structure remain legible across front/rear/side views.

The complete USNM 468028 part and counterpart, rather than a thumbnail, and Hoyal Cuthill (2022) Figure 2 were independently inspected. ROM's older stem-group cnidarian interpretation and the 2022 Petalonamae interpretation differ; that disagreement remains explicit and unresolved. The asset is judged for cautious morphology, not an asserted phylogenetic placement, living color, or unpreserved anatomy.

Primary sources: [Royal Ontario Museum, Thaumaptilon walcotti](https://burgess-shale.rom.on.ca/fossils/thaumaptilon-walcotti/) and [Hoyal Cuthill 2022, DOI 10.1017/S0016756821001333](https://doi.org/10.1017/S0016756821001333). Consulted actual pixel hashes: ROM image `b43be1e6879d0f7f90b8e37ef00c4ca0d33642b3c715819b55272cf970ddc742`; 2022 Fig. 2 `a8a2c0e7c27baec536d0a15e8c162abeadec364d624fb25b5438ee315de3ce50`.

### sandstone-fin — PASS, bounded

The exact final views show a single thin, tall sedimentary wall/fin with visible layered banding, an irregular worn crest and modestly widened foot. It is not perforated into an arch and does not read as a hoodoo. It is a generic fin rather than a claim about a precise site or geological age.

Primary sources: [NPS geology and formations](https://www.nps.gov/arch/learn/nature/geologicformations.htm) and [NPS Wooden Shoe Arch](https://www.nps.gov/places/wooden-shoe-arch-overlook-wooden-shoe-arch.htm). The actual consulted photo pixels are outside the repo (SHA-256 `664e55958dd58746c9d801d93b3384ca9b6045975761acbb14db579b21c54864`).

### lava-dome — REVISE

The model is dome-like rather than a cone or crater and is technically valid. However, the eight final images consistently show a relatively smooth central dome, with a circumferential belt/ring of angular blocks: the top view reveals a comparatively bare summit inside the ring, while hero/front views expose a strongly horizontal band. Irregular blocks soften but do not remove the ring-like organization. The final is improved over the retained diagnostic attempt, yet the explicit no-mechanical-belt target remains materially unresolved. This is an independent pixel-based visual and specification failure, even though the maker's note says the belt has been removed.

The producer observation describes the final as no longer a regular mechanical belt; I disagree based on the visible ring/banding in the exact final pixels. The NPS volcanic-dome source and actual dome/rubble pixels support a rough, blocky extrusion target. This candidate is only judged as a generic dome; no exact volcano or current event is asserted.

Primary source: [NPS, Volcanic Domes](https://www.nps.gov/articles/000/domes.htm). Consulted actual pixel hashes (both outside repo): dome `8e19ea04a220fa708e013426a37c923c219320409d6b4ac23b88588db5445381`; rubble `a3b7cb47a45d26115500b1ee73f4cfe2e59a38f3c96c403f4c44c6d8a2298ba3`.

### ice-wedge-polygon-ground — PASS, bounded

The final is a single connected low-centered polygon terrain patch with connected shallow ridges and lower-looking centers, not a set of detached decorative tiles. Cell edges and relief are stylized and some cells look similar, but the terrain reads coherently in top, side and silhouette views. No exact site, recent climate trend, or unsupported temporal claim is attached.

Primary sources: [NPS, Ice Wedges (2022)](https://www.nps.gov/articles/000/ice-wedges-2022.htm) and [NPS, Ice-wedge polygons at Swanson River](https://www.nps.gov/articles/aps-v12-i2-c7.htm). Actual aerial/reference pixel hashes (outside repo): `5443cc40465f7f76410d16fa9295f35d1347b2d023c742f8dd70dfac755a0ab8` and `8e075ac2ce43e706011b5f90367cbf3ec0344d06889730359bd1ea49b0ecdd3e`.

## Exact artifact hashes

All paths below are within `assets/candidates/continuous-small-life-round27-20261020/batch-68/<asset>/r001/`.

| Asset | Final GLB SHA-256 | Source `.blend` SHA-256 | Candidate brief SHA-256 | Reference ledger SHA-256 | Generator SHA-256 | Config SHA-256 | Original concept SHA-256 |
|---|---|---|---|---|---|---|---|
| thaumaptilon | `5f4108c4b97377bd2df41273672c16e6e9d7295a5e7d6710b4bdf0ad2b22bf42` | `f335a397e3bc20502e9dfc864dc153227830706c4c3f15c2e6ec8f7be4c7a73b` | `08151d333a70e2be2d47fb8911988c652cc7ec96b9e615353b0964524bb9b35e` | `e62c9c29600598f08b8f482c4852283708d9f0f6811811c5fa2a52f2c4480f81` | `e11a9479ef1b06980407ea052e229973d9681484f1a9592a18de1e43a60e9df0` | `42ecbb4f17ffdc0aff58725108f99354b8a33dda46e8fc76d655d8aacf66ec9f` | `ad22a947913aa5ea452de3eef77b9b0e3990093487c02635eef278e05093ecef` |
| sandstone-fin | `20d94267de302a60886dcfa05aaa4bb41450f42e5e60caa29203a451cf039905` | `3951327fdb390cf568e28e1dc8862a1d0540ad1581451543eb2f06413bc56b97` | `07a01644d89ed8760972c80a947e86c741f147dc523d6e81612702fb5b0e4a85` | `48ab9a07a03c575cfb22d4fd0667ae6cf7200a188080c8d209544fba0efff6a6` | `e11a9479ef1b06980407ea052e229973d9681484f1a9592a18de1e43a60e9df0` | `9362f0251077e72c22790d012c9a78b075b0f397cc47d4b16e177071a6554023` | `cd1c4392341b7ab6679d76baf84cd27ab547a1746f45cd740e623e14e2c6db79` |
| lava-dome | `ec4eee3edc6b6cfd676bc9cb75bff04611afd7ebcd63bf6c279a46d539a159f8` | `04a73fc30756668f472625772af197a8a0b5c017265140945ed690eeccce7d15` | `505b922c136495e7a1c792dbca7a3aa6d82f7185e94e9925f779955fb1c31aab` | `1cd99cf0e05282e5b85c404ddb40e098a9050eb84b4d0ee0330d95f5e5a18a5b` | `39baae389027ca6ff4572555568506d0ef9bf5c6f99fcffa4746cc4a89c6e887` | `af229fc35803154fb23e992fea4b818aaadbc9f203ee21b48093c98856bf9793` | `79e1c6f1bcebda03c445649f0df026e68ce8a78bd921a9949e25c715cfb52005` |
| ice-wedge-polygon-ground | `a5eaa19f0f0d4f1de495974fbed3d360ce5ebb0c97b973f95a224b01a30a1f7d` | `69e8c80b2694f418ce102fa81d651ede226a5c959be77f3e27a9f1a743d1ecdb` | `5ecdb531cc167676936a4c682c3cad726edafd04af5bc245f06c012ce872a801` | `a5af95a4f2755b11ad3a3d161c3351c06a8ef05e62be7fde85fd460d80f7f569` | `6c80a2afea834a1b750aa219672a5664e6b21fc1f4a4dd2e58de3c27b23b94d2` | `a69361f5c899ecfc21e166dc582ee34359925c05b3ea5f80bf8ff5da14f81c56` | `de76243028d4ae42fd3d9a959a54447e6fd5dba1fa5b90bab469b00c3e71b399` |

## Unknowns and boundaries

The ImageGen tool output supplied an image and output hint, but no provider generation ID or provider-internal generation timestamp. Internal image-generation time and exact geometry-authoring start therefore remain **unknown**; no file-mtime inference was used. Consulted copyrighted source images remain outside the repository.

The final artifacts and evidence have not been approved, pushed, merged, released, or GPU/scene tested as part of this QA. The producer handoff's pending approval state remains unchanged. The appropriate next step for the batch is a targeted dome repair and fresh review of the revised exact candidate.
