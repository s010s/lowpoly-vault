# Independent Linux conifer A publication-preview review

Fixed review input: `e20d59e4e6871903d23fcec958ebc2ba7d9030ba`, branch `integrate/conifer-doc1-20261017`. Author/committer: Leon Made This <8357465+s010s@users.noreply.github.com>. This is a continuation of the independent preview task with a new immutable Linux-image approval; original approvals and source images are preserved.

**Exact Linux preview visual verdict: PASS. Strict candidate approval/integrity gate: PASS. Current candidate release status: still blocked by the existing25-file Linux reproduction failure until the integrator updates the selected images/pins and reruns complete Linux publication CI.** This review does not declare the current failing candidate publishable or identify the unresolved environment root cause.

## Pixels inspected and findings

Each of all24 new Linux WebPs was opened at its full decoded768×768 resolution beside the corresponding approved Mac frame, alternating actual light `#e8e4dc` and dark `#20251b` alpha composition. This is24 individual full-frame pairs, not a montage-only review. Poster was opened separately and also inspected on both backgrounds. Four complete comparison pairs are retained (0,7,17,23). All24 exact image hashes and observations are in `artifact-audit.json` and the candidate evidence.

The airy A branch/spray arrangement, fine separated needles, tan wood and subdued greens remain visually consistent. All24 Linux alpha bounds exactly equal their Mac counterparts. Tips/roots are complete with the same generous margins, no side clipping, no opaque rectangle or broad fringe. Frame0 is azimuth42°, elevation23.3°; every next frame advances15°, including the last-to-first wrap. No reordered/mirrored frame, independent zoom, object-position jump, or broad color/lighting shift was observed.

Differences are real decoded RGB **and alpha** changes, not solely WebP encoding changes. Correctly composited full-frame RGB mean absolute errors are approximately0.077–0.106 on the0–255 scale, with local maxima up to52 light/40 dark. These averages are supporting measurements, not the verdict. To avoid hiding local errors in the empty background average, opened4× nearest-neighbor crops at actual local difference maxima in frames0/6/11/22. Visible changes are small localized needle/branch edge coverage and intensity differences; no missing branch/spray, coherent geometry displacement, severe halo or altered A-style density. Both variants retain normal thin-needle sampling limits.

New Linux poster and frame0 are byte-identical: `fb46be69de3e6dd664150c9bddeae58353d293e2eebff536cf44d5f014dab975`;34692 bytes. Sequence824778 bytes. Generated manifest SHA256 is recorded in `artifact-audit.json` and exact-copied into the sealed candidate. Old Mac poster629628… remains separately approved and unchanged.

## Exact GLB and continuity

GLB remains715500 bytes,19052 triangles,3 materials,0 textures, SHA256 `c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40`. Source/brief/reference identity is unchanged. Site/scripts are unchanged from the original reviewed browser checkpoint through e20d59. The retained Linux capture report pins the current viewer source and shared ModelStage v2 preset: FOV38, fit_padding1.08,42°/23.3°,sRGB/ACESFilmic,exposure1.2, same lights. Chromium141.0.7390.37 canonical capture uses the actual built viewer and verifies exact source GLB bytes.

Opened the actual Linux canvas PNG `../conifer-doc1-linux-preview-recheck/linux-reference.png`. Its alpha equals the new frame0/poster exactly; lossless-PNG versus lossy-WebP mean composited RGB difference is0.158–0.159/255, with consistent structural appearance. The PNG and new poster depict the same frame0 camera, crop, color and model. This is actual captured runtime evidence, not a new browser execution by this reviewer.

Rechecked saved desktop/mobile real GLB detail captures against new Linux frame7 using an independent offline centered-square320px comparison with Pillow BILINEAR. RGB error is0.00195/0.00258 on normalized0–1 scale; bounds differ0/2px and centroids0.263/0.156px. Opened both parity pairs. Static angle, placement, scale and color agree. This offline method approximates the existing browser parity method; it is explicitly not a rerun of animated browser handoff. Previously approved exact-code reverse/reopen/interruption tests remain historical evidence. A new-image browser regression is still required after integrator activation, as later browser steps did not run in failed CI39038352273.

## New approval, validation and handoff

New record:
`experiments/structural-refinement-2026-10-17/accepted/conifer-tree/qa/doc1-linux-publication-preview-independent/candidate.reviewed.json`

Candidate SHA256: `4ecdcbc679099789ab917f72e0cc6ffbb959a9b870e16698f325a2283c41ef27`.

Its new visual report and approval seal bind all24 Linux frame hashes, poster and actual lossless frame0 PNG. Prior model visual/reference judgments and original Mac preview approval are inherited with their original reviewer/report attribution. Other six stage decisions and all artifacts/textures remain byte-for-byte identical in record content. No original approval is rewritten. Both old and Linux image sets are preserved as separate evidence.

Ran the unmodified strict validator with `--require-approved --previous qa/doc1-publication-preview-independent/candidate.reviewed.json`. Result: valid=true,approved_for_brief=true,no errors/blockers; new poster hash appears in approved_visual_image_sha256. See `strict-candidate-gate.json`. Source evidence SHA256SUMS and all reviewed new image hashes were independently rechecked. No source test or publication assertion was modified.

For integration, select this new candidate and its pin, copy the approved Linux frame/poster bytes and generated manifest into the intended proposal image routes, update corresponding image/release metadata/index/descriptor hashes, and rerun the complete strict Linux publication workflow with zero mismatches and actual new-image handoff tests. This task deliberately does not update active release metadata or image files. Existing failure logs and original renderer reports remain untouched. Current e20d59 failure is not waived by visual approval.

## Limits and remaining blockers

Capture-environment root cause remains unresolved: available comparisons do not isolate OS, browser package, backend, antialiasing or encoding implementation. Canonical capture success39038627111 and25-file mismatch39038352273 are retained as distinct facts. No claim that the new conifer is live.

**KHR_mesh_quantization remains required**, tested loader Three.js0.180.0. Performance acceptance remains only the recorded M5 Pro/ANGLE Metal profile; SwiftShader misses16.7ms including single tree. Other hardware/loaders unverified; fine-needle subpixel aliasing persists. No performance reapproval or zero-shimmer claim.

Preview visual defects: none found. Release blockers: integrate exact Linux-image approval/pins, then complete a fresh zero-mismatch Linux publication/browser run. No browser controlled, no processes launched in background, no push or publication, and no branch switch.
