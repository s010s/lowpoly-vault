# Independent QA — small land/air quartet

**Outcome:** limited-scope QA pass for the frozen asset files and observed software rendering, with formal candidate-gate and release blockers. This is not approval to publish or integrate. Source freeze: `68483aa3b8eed2d86f9e59a930128d99579b0838` (`candidate/small-land-air-quartet-main-20261019`). No model or original candidate metadata was changed.

## Verified checks

| Asset (r001) | GLB SHA-256 | Tris | Export materials / primitives | Bytes | GLB bounds X,Y,Z (m) | Khronos |
|---|---|---:|---:|---:|---|---|
| sapeornis | `7b0aef80ee8327ebc06a8372fc63fce63c393a62451820b4bd183ff868b2755b` | 5,744 | 6 / 78 | 340,260 | `0.943240941, 0.210977972, 0.449886322` | 0 errors, 0 warnings |
| longirostravis | `10668416201cf7ec57e48285019fcd0738e6bb69665fd8fb519559aabaa6bd83` | 2,428 | 7 / 35 | 160,264 | `0.0913477018, 0.136473651, 0.318628833` | 0 errors, 0 warnings |
| dunbaria | `2f584412b3318fa3969e6b008271df107f73fe9f00c8f304c04bfa47e134311e` | 1,582 | 7 / 31 | 113,700 | `0.0595000014, 0.00824796167, 0.0543434117` | 0 errors, 0 warnings |
| chimerarachne | `848328130f8874bc6c81b0636d8bfc78f76d04b46cfa0786fe7d978f28e3ad6c` | 1,418 | 5 / 26 | 98,176 | `0.00383354002, 0.00123318997, 0.00715652341` | 0 errors, 0 warnings |

Every artifact SHA-256 listed in `handoff.json` matches the frozen files (`metadata/freeze-bindings.json`). All four Khronos validations report 0 errors, 0 warnings, 0 infos and 0 hints. Fresh `.blend` → GLB checks matched triangle counts and bounds for all four. Sapeornis reports only the understood negative-Y floor check because it is mounted at the flight-body center. Each asset stays under its brief limits: 16,000 triangles, 8 materials, 160 primitives and 1,000,000 bytes.

The exact GLBs were imported into Blender for eleven 256px views each. I opened the actual generated concept sheet and exported-model views. Fresh visual evidence is in [`renders/`](renders/); SHA-bound notes are in [`visual-review.json`](visual-review.json). Provenance records ImageGen return at 20:52:40 UTC, concept inspection at 20:52:53, brief freeze at 20:53:57, then Blender construction.

### Visual and factual observations

- **Sapeornis:** r001 reads as a broad-winged flying bird with a fan tail. Its outer tips are visibly narrower and pointier than the concept, but that does not undermine child-style recognition or construction. The matched r002 comparison makes paddle-like tips without a clear craft improvement. Keep r001 and its stated limitation; no geometry change is warranted. Consulted sources describe broad-wing interpretations and fan-arranged rectrices ([Serrano et al., 2017](https://pmc.ncbi.nlm.nih.gov/articles/PMC5550970/); [Zheng et al., 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4183337/)).
- **Longirostravis:** the perched-bird shape, folded wings, paired feet and narrow curved rostrum are clear. The model deliberately reduces the generated concept's exaggerated beak; teeth and species-exact cranial anatomy are not claimed. The published description supports a long slender rostrum/mandible ([Hou et al., 2004](https://link.springer.com/article/10.1007/s00114-003-0489-1)).
- **Dunbaria:** four main wings, six walking legs, smaller front lobes and paired cerci remain distinguishable in the close views. Lobes and venation are simplified; no species/sex-exact claim is made. This aligns with the described prothoracic lobes and cerci ([Kukalová-Peck, 1971](https://onlinelibrary.wiley.com/doi/pdf/10.1155/1971/84672)).
- **Chimerarachne:** close views show eight walking legs, shorter pedipalps, a segmented abdomen and a long whip-like tail. Spinneret projections are simplified; no exact homology, eye count, sex-specific palp or phylogenetic placement is claimed ([Wang et al., 2018](https://www.nature.com/articles/s41559-017-0449-3)).

These are bounded observations of stylized props, not a fossil-accuracy certification.

## WebGL scene check

Three.js 180 loaded the four exact GLBs in Chromium 154/WebGL2 with ANGLE SwiftShader. SHA-256 was checked before loading; the browser console and page-error lists are empty and the context stayed live. This is software rendering, not hardware GPU certification.

| Scenario | Instances | Draw calls | Triangles | Median / max frame (ms) |
|---|---:|---:|---:|---:|
| one-each | 4 | 171 | 11,174 | 1.5 / 2.3 |
| normal-8-each | 32 | 1,361 | 89,378 | 2.2 / 2.5 |
| stress-32-each | 128 | 5,441 | 357,506 | 9.1 / 10.9 |

At native scales, Chimerarachne occupies only a tiny part of the shared scene frame. It renders, but a parent scene needs an intentional camera/card layout for it to be inspectable. Full machine results and screenshots are in [`runtime/`](runtime/).

## Formal blockers and release inputs

1. There is no `production/concept-small-land-air-20261019/candidate.json`. The repository validator was run against that exact path and failed closed with “candidate: missing file”; required-field/evidence validation and independent approvals in the candidate record are therefore pending. See [`metadata/candidate-record-validation.report.json`](metadata/candidate-record-validation.report.json).
2. All four `metadata.json` files have a preview field, but every target `preview-hero.png` is absent. Supply the reviewed poster bytes and bind the exact file hash before catalog/release packaging.
3. Sapeornis metadata says `generator.py`, while the frozen handoff pins `generator-r001.py` (different SHA-256). Reconcile this provenance pointer in packaging metadata.
4. Parent-owned hardware GPU and populated production-scene checks remain pending. Plan an intentional visible presentation for native-scale Chimerarachne.
5. Record independent visual, factual and specification evidence against each exact candidate hash; keep the Sapeornis outer-wing limitation and stylized taxonomic boundaries explicit. Publication approval remains separate.

Metadata values for GLB/Blend hashes, triangles, bytes and dimensions match the frozen handoff. Details and missing-file checks are in [`metadata/metadata-audit.json`](metadata/metadata-audit.json). The full machine-readable result is [`report.json`](report.json).
