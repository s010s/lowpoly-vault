# Batch54 bounded publication

This additive package contains didymoceras r003, spirematospermum r003,
cave-shield r002 and psammichnites-ribbon-trace r002. Its source is
54d5380ec3c63ae3e9ab4f36cb377db65ab16c75 and its independent review is
d5b0956916ab21d1ef0fef44a42358b3d9c2db95. The original 190 catalog records
remain unchanged; this package adds four exact GLB/Blend payload pairs.

The publication scope is `independent_qa_accepted_stylized_prop`, following
the existing bounded-release policy. It does not grant formal candidate
approval, imply user visual acceptance, verify physical GPU performance,
verify an authored target scene, or invent the missing provider generation
timestamp. Formal acceptance remains BLOCKED. Frozen candidates and QA are
preserved byte-for-byte. The old unready dispatch placeholder is preserved;
`qa/batch54-release-20261020/dispatch-binding.json` binds exact completed QA
additively instead of rewriting history.

Card WebP and reference PNG files come from the unchanged actual ModelStage
renderer, not concept art or diagnostic Blender previews. Capture run
39362925560 at 6d39ec68e803ef463560796b121a124ea59ecbd6 successfully rendered
four exact sources and uploaded artifact 12237998862. The overall job failed
in a subsequent legacy log-export assertion that compared the new IDs with
an old quartet. This failure is retained in capture-provenance.json and is
not reported as a successful workflow. The artifact digest, renderer report,
source hashes and output hashes are independently auditable.

Required release gates remain independent: bounded publication integrity and
negative tests; independent image review; distinct approved gallery renderer
detail/wheel PNG pairs; complete 194-asset delivery; trusted-baseline real
190-reused/4-fresh CI proof; final release review; coordinated merge; Pages
and live-site readback. A prepared commit or a successful renderer step is
not evidence that any later gate has completed.

Run `node site/concept-landair-release-test.mjs --batch54-only` for the four
new models' bounded tamper tests without repeating prior model QA. The normal
publication test invocation also retains all historical release gates.
