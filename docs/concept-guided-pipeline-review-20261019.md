# Concept-guided pipeline review, 19 October 2026

Status: provisional, tested on three representative low-poly assets; no batch expansion or publication approval.

## Additive implementation

The entry point is `skills/concept-guided-lowpoly/SKILL.md`. It links to the existing art-direction and Blender pipeline skills and adds genuine ImageGen-first interpretation, contradictory-view resolution, real volumetric construction, exact exported-GLB review, matched revision comparison and honest evidence boundaries.

Included reusable files:
- English brief/prompt template with optional bilingual names
- Evidence sidecar template
- Practical workflow recipe using existing project helpers
- Three-case R1/R2 lesson with actual measurements and limitations
- `scripts/validate_concept_evidence.py`, a read-only integrity checker
- `scripts/test_concept_evidence.py`, 20 focused integrity/rejection tests

The existing skills each gain only a short link. The schema index gains a supplemental-study explanation. `npm run test:pipeline` adds the new test suite. Existing approval profiles, release manifests, asset catalog and site files are unchanged.

## Executed validation

- Full `npm run test:pipeline`: 174 tests passed, including 20 new tests. The sparse worktree initially omitted the existing legacy-natural-arch fixture; restoring that existing fixture allowed the aggregate suite to run successfully. No test was bypassed or weakened.
- Skill-creator validation, Python compilation and `git diff --check`: passed.
- Integration: a copy of the R1 rock was rendered through the existing exact-GLB renderer, producing four new hash-bound frames. The supplemental checker accepted integrity and correctly left missing original concept receipt/chronology as incomplete. This new compatibility run does not repair historical provenance.
- Independent consumer run on all three R1 assets: all sidecars valid but incomplete; default exit 0, strict exit 1. Five historical blockers remain: original ImageGen receipt, generation/inspection/model-start timestamps, and original hash-bound render manifest.
- All 48 files in the R1 delivery manifest still matched. Fresh Khronos checks on copies returned zero errors/warnings. Static QA separately flagged all materials as double-sided.

## Lessons incorporated

Historical missing evidence can be represented with explicit nulls rather than fabricated receipts. Reserved canonical camera labels must not be applied to oblique images. The original fish is X-aligned, so its +X camera is an end view. The Khronos command requires the declared official dependency in the module search path; a missing dependency is a tooling failure, not an asset failure. Absolute signed-volume magnitude is not independent proof of outward orientation.

The checker tests evidence consistency, not tool authenticity, visual quality, truth, browser performance or user approval. The three examples support a useful provisional method, not a universal quality guarantee. Target-runtime acceptance and independently executed rebuild/source parity remain outside this completed study.

## User comparison decision

The 15:20 UTC feedback preferred R1 coral and saw little difference in the other
two assets. None of R2 is promoted. R1 remains the design-direction baseline,
without production release approval. The method now explicitly captures rejecting
a revision when its visible benefit is insufficient; complexity is not progress.
No further modeling iteration was requested or performed.

## Delivery boundary

Prepared on an isolated branch from base `56b8b86a80721d8eeb120f0414b87c479c3eb237`. Git author identity uses the verified project no-reply address. Normal remote push is blocked by absent GitHub CLI/HTTPS authentication; a public read-only fetch does not establish write access. A local commit and portable review package preserve the work for review and later integration. No remote commit, merge, batch run or site deployment is implied.

Original prose and art: CC BY 4.0, Leon Made This / s010s. Executable code: MIT. Third-party provenance remains separately recorded.
