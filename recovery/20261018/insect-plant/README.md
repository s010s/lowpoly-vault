# Source-only recovery: insect and plant pilot

This packet was reconstructed from retained conversation/tool-call content on 2026-10-18. It preserves the original authoring source and the recorded r2 foliage edit without running Blender or generating replacement models.

**Original GLB and .blend binaries have not been recovered in this packet. Current candidate QA is pending.** Historical export hashes are identifiers for a future byte comparison, not evidence that recovered binaries exist. The old generator hash was not printed in retained output, so byte identity to the old source is not certified.

- `scripts/models/build_small_insect_plant_pair_r1_history.py`: recovered initial generator text
- `scripts/models/build_small_insect_plant_pair.py`: that source with the exact five recorded r2 replacements
- `exact-r2-edits.json`: recorded replacement operations
- `config/`: the two recorded final build configs
- `RECOVERY.json`: provenance, known historical GLB hashes/counts, dependencies and current recovered-file hashes

Only Python AST syntax parsing was run for this recovery. No Blender build, rendering or new model acceptance was performed. Earlier observed technical results do not establish QA for a future reconstruction.

The generator depends on `scripts/asset_common.py` and `scripts/qa_glb.py` from s010s/lowpoly-vault baseline `01c60dd85322932a967c4f2aa50045f2da1a25bd`, plus the planner's frozen pilot-v002 briefs/references. Those dependencies are not copied into this packet.

Code: MIT. Any future generated asset or preview: CC BY 4.0, attribution Leon Made This / s010s. This packet contains no third-party artwork, mesh or texture. Do not treat it as a completed or published asset release.
