# Skolithos r002 independent differential review

PASS_STATIC_ONLY for the single exact candidate. Technical, visual, factual, specification and runtime_parse pass. GPU and scene remain unknown / not run. No formal, user, website, publication or live approval is claimed.

## Exact identity

- Source commit: 4264dbafd0cc3142175c890644f2990dfaa0acf6
- GLB: 6e729192850db1f29bd886d2d5d07518ae4e8ff2b4d373d245cb8493eef3fbd3
- Brief: 96210f9dc574d69b2506c74d433149859370bfe5840b8c7942b74d3afde7a610
- References: 462acade525357722fbc24fd3391970e666b7550fc3baf026c4bf6d7159a60be
- Maker handoff: 6f68ba0cad6436aa477b51ee2ea9541b0a531b0f63d11b3edcc871d495a86713

## Finding

The original r001 defect was real: its smallest actual circumradius was 0.002597398883191733 m, below the immutable 0.0026 m minimum due to the 0.999 inset. That original failure remains unchanged. The new r002 has 168 actual top/bottom radial samples in [0.0026000098708658737, 0.004795201122760795] m. Every sample meets the original [0.0026, 0.0048] m range with zero acceptance tolerance. The approximately9.87 nm lower-bound margin is actual authored interior geometry, not a relaxed threshold.

Only the sixth shaft and its matching host bore each changed24 world vertices. The other six shafts, topology indices, transforms and materials are unchanged. Seven continuous12-sided shafts and three exposed front shafts remain. The corrected bore retains at least2.6019117584374918 micrometers of conservative radial clearance. Host-top triangles do not cover any shaft center; these are real negative openings, not coplanar surface overlays.

## Verification and recovery provenance

The preceding independent reviewer actually reopened and reexported the saved Blend at23:17:57–58 UTC, measured world-space geometry at23:19, and ran Khronos/Three.js/candidate checks at23:20. This continuation preserved and rehashed all12 existing files instead of rerunning successful Blender work. It independently replayed the lightweight binary decoder and obtained exactly the same old/new world geometry.

The continuation completed277 provenance checks and rehashed50 raw files (1,828,046 bytes). Separate maker rebuilds have actual Blender PIDs9 and32, wrappers8 and31, different request/output paths, real start/finish receipts and successful logs. Both raw GLBs are byte-identical to the candidate, with semantic SHA777983dd34d38541bb8cafb95b50ed4903a6b44c11a5299422fd21512f47d530. Source reexport is also byte- and semantic-identical.

The original freeze and all original brief fields except the derived brief_version label are unchanged. Repair freeze preceded the first actual geometry request. Final GLB/brief/reference identity was bound before final rendering. The pinned renderer hashes the triplet before import/render, rejects nonempty output, and verifies unchanged inputs afterward. The complete raw log records all eight new PNG saves. Exact render-process start time is unknown because the original helper did not record it; no filesystem timestamp is used to invent it.

## Visual and factual review

This continuation personally inspected printed page72 and Figure56A–B, all four concept panels, all eight new512px individual views and the lossless sheet. It verified each sheet crop is pixel-identical to its original frame. The concept's disconnected shafts are not factual evidence and are not copied. The final model maintains separate full-height cylinders, quiet sandstone and the intended front cutaway. No obvious coplanar striping or new overlap artifact appears in the inspected stills, including neutral clay.

The primary source describes vertical unbranched cylindrical filled burrows and shows their protruding bed-top ends. It explicitly lacks cross-sectional observations adequate for ichnospecies identification. This is therefore a genus-level illustrative trace cutaway, not a measured reconstruction of those specimens, a tracemaker model or a universal environmental claim.

## Technical limits

Editable source has334 vertices and652 evaluated/exported triangles. GLB has652 triangles,998 split position-accessor vertices,2 materials,2 primitives,0 textures and30,172 bytes. Khronos reports zero errors/warnings/info/hints. Three GLTFLoader r180 Node parsing passes. Camera/render/material configuration equals r001; no rendering trick hides the repair.

CPU Cycles evidence is not hardware GPU evidence. Node parsing is not composed-scene acceptance. The candidate-profile validator remains valid but unapproved; the unchanged static-stylized profile accepts eight fixed views and zero turntable frames, whereas the legacy profile's generic turntable diagnostic is not the chosen contract. Optional unavailable Draco compression did not affect this uncompressed exact reexport.

No Git push, PR, merge, deployment, installation, full build, source change, raw deletion or user-computer action was performed. This report covers only one r002 differential candidate, not a new full-batch acceptance.
