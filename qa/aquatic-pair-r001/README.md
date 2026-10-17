# Aquatic pair r001 evidence

The two original editable sources, GLBs, frozen v002 plan briefs, execution briefs, compact six-view clean-import evidence, contact sheets and technical reports are under `assets/prehistoric/fauna/{bothriolepis,waptia}/`.

Both official glTF validator runs have zero errors and warnings. Source/export count and bounds match; clean Blender reimports pass with only the documented suspended-mount warning. Each separately executed bounded queue rebuild produces a byte-identical GLB. Three.js 0.180.0 GLTFLoader parsing passes, which is not GPU rendering.

Queue records and exact rebuilt GLBs are retained here. Secondary rebuild .blend files are local scratch and not duplicated in this evidence package; canonical editable source .blend files are delivered in the asset directories. The immutable result logs still report the hashes of all generated build outputs.

Candidate integrity was checked using the explicit environment-prop tier introduced by planner commit `f269a40abb43901a38f681f816d0c1627a2a58b1`; combine that independently committed standards change before rerunning `scripts/validate_candidate.py`. Both pending candidate records are valid and unapproved. No independent visual/factual/specification stage or GPU/scene stage is represented as passed.

All production ran on the authorized cloud Blender 4.3.2 computer, with one two-thread process at a time in this worktree. No user Mac, museum repository, live site or existing release asset was modified.
