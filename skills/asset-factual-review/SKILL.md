---
name: asset-factual-review
description: Independently check factual obligations of a modeled asset against its frozen brief and primary references, including animal anatomy, botanical structure, and jurisdiction-sensitive manufactured objects. Use before factual acceptance or when a named feature is disputed; visual appeal and publication are separate decisions.
---

# Review what the asset claims

An asset can be technically valid and attractive while depicting the wrong structure. Establish what must be true before reviewing whether it is. This Skill reduces unsupported claims; it does not guarantee complete scientific or real-world accuracy.

## Inputs and independence

Read the frozen brief, source/provenance ledger, exact GLB hash, full-angle evidence manifest and [candidate contract](../blender-lowpoly-pipeline/references/standardized-pipeline.md). Form the first verdict in a fresh review task without the maker's self-score or expected answer. Inspect actual image pixels and geometry/measurements where needed. Reference captions and metadata are claims to check, not proof.

For each critical feature, require a primary source with an exact section, figure, specimen or measurement. Record edition/date and applicability. A general museum homepage or an attractive third-party model is not a feature-specific authority. Check sources for contradictory restorations, historical mounts, composite specimens and outdated regional standards.

## Subject-specific checks

- **Animals:** lock taxon, life stage, pose and reconstruction scope. Check identifying proportions, skeleton/soft-tissue distinction, limb articulation, hands/feet, attachment points and diagnostic structures. Do not count visible nails as all digits. Mark missing/restored anatomy, color, integument, behavior and disputed pose as uncertain or artistic as appropriate.
- **Plants and traces:** check growth/branching structure, reproductive features, period/region and representation scale. Modern analogues do not establish ancient species identity. Nest/track internal geometry may matter more than the outer silhouette.
- **Manufactured objects:** lock jurisdiction, era, type/variant, functional arrangement and viewing orientation. Check component count, order, mounting and operational state against the applicable authority or original equipment reference. Read [traffic-signal example](references/traffic-signal-example.md) only for signal work.
- **Fantasy/alien concepts:** check consistency with the explicit invented design rules and honest labeling. Do not invent real-world scientific authority for fictional features.

## Decision and repair

Return criterion-level `pass`, `fail`, `unknown`, `not_applicable` or `stale`, with source IDs, actual evidence, confidence and limitations. Unsupported critical claims remain unknown; conflicting evidence requires reconciliation or a narrower claim. Aesthetic plausibility is not a factual pass. For museum-grade or disputed high-specificity claims, identify the need for qualified subject review instead of claiming expertise the evidence does not supply.

Defects name the feature, view/location, factual obligation, source, correction/evidence needed and retest. Recheck repaired exports by their new hash and inspect for regression. A user can choose a stylized concept, but its label must match that scope. Publication permission never changes the factual verdict.

## Reference use and licensing

For every incorporated component record creator, origin, license, attribution, modifications and allowed redistribution. Keep consulted-only references separate from copied material. Scientific facts, image rights and mesh/texture licenses are different. Do not bundle third-party reference images or scans as original assets. Use original geometry/maps unless reuse is both authorized and licensed.
