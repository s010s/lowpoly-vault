Clarification 01 to the r002 differential QA

This append-only QA clarification supplements, but does not replace or alter, QA.md (SHA-256 aa95bcf5272a250fd90f93f143ba06b56df56d4443dba686cbcc430774d1d46b). No model, source, producer evidence, brief, approval record, or original report was changed; no image was rerendered.

Static-stage assessment

- Geometry/technical: PASS BOUNDED. The exact r002 GLB is technically within the frozen brief and budgets; independent static, Khronos, source reopen/re-export, and CPU parser checks pass.
- Visual: ACCEPT BOUNDED for the specific r001 uniform/mechanical-tiling concern. The r002 views show irregular multiscale chipped crowns and genuine relief while preserving dense fitted armor and narrow cracks. Top remains recognizably polygonal, but that is not a frozen-brief failure or a new reason to require geometry changes.
- Factual: PASS BOUNDED for the generic illustrative clast surface and expressly limited claims.
- Specification: bounded recommendation should be PASS BOUNDED after one truthful append-only correction to the r002 evidence note below. No change to model geometry, render, frozen brief, or scope is indicated.

Exact render-difference reconciliation

The r001 and r002 render helper scripts are byte-identical: production/continuous-small-life-round26-20261020/work/batch-67/render-fixed8.py and .../repair-pavement-r002/render-fixed8.py both SHA-256 33ed7fc4b39a41e67f79e51d41fd4457f2a3087085837e59c8981d87e7bb412d. The bounds/framing policy is unchanged. The shared helper measures source bounds, derives center/radius, computes orthographic scale as 2 * radius * 1.12, sets light energies proportional to radius squared, and light sizes proportional to radius. This explains the exact render-config deltas; they are automatic bounds-derived fit values, not a hand-tuned camera/light change to conceal geometry.

- Maximum Z / model height: 0.30955132842063904 m (r001) to 0.32336437702178955 m (r002), +0.013813048601150513 m / +4.4622805%.
- Camera target Z: 0.15477566421031952 m to 0.16168218851089478 m, +0.006906524300575256 m, exactly half the height delta.
- Orthographic scale: 5.33740957846423 to 5.337592857201926, +0.00018327873769585779 / +0.00343385%.
- Key energy: 2554.92138671875 to 2555.096923828125 (+0.175537109375 / +0.00687055%); key size: 9.531088829040527 to 9.531415939331055 (+0.00032711029052734375 / +0.00343203%).
- Fill energy: 851.6404418945312 to 851.698974609375 (+0.05853271484375 / +0.00687294%); fill size: 11.913860321044922 to 11.91426944732666 (+0.00040912628173828125 / +0.00343404%).
- The renderer remains Blender Cycles CPU, 512 px, 16 samples; orbit/elevation, directions, background, world strength, view transform and all four palette colors are unchanged. All other render-config differences are the cited bound-derived numeric values.

The r002 concept-evidence note “original palette and cameras unchanged” is not literally accurate at parameter level. A truthful producer-side append-only correction should say that the framing helper/policy and artistic camera setup are unchanged, while the listed target/scale/light values were automatically recalculated from changed source bounds. This correction is the sole current static specification-evidence issue for website-preparation recommendation. It is a documentation correction only; do not rerender or alter geometry.

Separate formal state, not a new static rejection rule

The ImageGen provider-internal generation timestamp remains unknown. Existing concept evidence validation is integrity-valid but evidence_complete=false on that timestamp; do not invent a value or infer it from mtimes. GPU and composed-scene stages remain not_run/blocked unknown; neither CPU imagery nor Node parsing proves them. Under the existing contract these are explicitly retained boundaries for the static QA and formal candidate is still unapproved. They are not newly added universal rejection criteria for bounded static website-preparation assessment. Candidate status must continue to distinguish valid=true, evidence_complete=false, approved_for_brief=false/approval pending. This clarification grants no formal/user/release approval and makes no GPU/scene claim.

Actionable conclusion

Before recommending entry to static website preparation, append a truthful correction to the producer evidence note about the automatic bounds-derived values. No geometry, technical, factual, or frozen-scope defect remains in the targeted r002 delta. After that correction, the bounded static specification recommendation can be PASS BOUNDED; formal candidate approval and unrun GPU/scene remain separate gates.
