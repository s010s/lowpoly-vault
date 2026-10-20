Batch 67 desert-pavement r002 independent differential QA

Scope and bounded disposition

Pinned producer tree: /workspace/shared/lowpoly-batch67-20261020, branch candidate/small-life-batch67-concept-20261020, commit f6e5b25a4054747ec76714051e60b3bf42514be1. Worktree was clean at start and remained clean; all new QA output is outside the producer tree.

Desert-pavement r002 targeted visual-repair disposition: ACCEPT BOUNDED. The original r001 visual finding, “near-uniform Voronoi tessellation reads as decorative paving,” is resolved for the frozen educational target. All eight exact final 512x512 views and the 2048x1060 lossless sheet were personally inspected against the original NPS pixels and original generated row-D concept. The new hero, reverse hero and clay views now show visibly multiscale chipped angular clasts, uneven sloping shoulders, off-center faceted crowns and real relief, while retaining the nearly continuous close-fitted surface armor, narrow irregular cracks, thin closed substrate and irregular organic boundary. They do not become a loose gravel/boulder pile or decorative repeating grid. The top view still visibly exposes a Voronoi-like polygon partition; the cells are not uniform, and their height/crown differences are apparent in the other views. This residual is noted, but it no longer dominates the overall reading as mechanical tilework. No additional geometry change is required for the stated frozen target. I do not add a new “zero Voronoi topology” rule beyond the frozen brief.

Overall candidate acceptance remains BLOCKED, not because of the r001 visual issue, but because specification evidence is not fully closed and required GPU/scene stages are unrun. Stage decisions are separate below. This bounded local result is not formal approval, user/release acceptance, or publication authority.

Exact artifact identities and integrity

- r002 source.blend SHA-256: 05b7f0dea65fe2922e2c5a621454d5f37a15929dcee80630ad81c8e887b70c6a.
- r002 model.glb SHA-256: 8ac4620cfec4bfaa6d14a0098144217383ea1623199fb52aa73348b1659a249e.
- r002 generator.py SHA-256: ec4f03fceb778ebf1131b8fbd97dfc9aaa706706e9565e457e01770bddd44d08.
- r002 build-config.json SHA-256: 17677f32f110d21da1393fc55397cedccbd7c053eef0553c11c35a26f1ccc58a.
- r002 frozen brief.json SHA-256: 45f45ecf09ba9733b6744d7a45ae1945ff410ea996f5b8514eff24251d8dead3.
- r002 references.json SHA-256: 621a0a83000b52c06ae2c7c181097913fbfc17d21d623aa6102c294337d69257.
- Original r001 QA.md remains unchanged: SHA-256 a86e90a24839331a0e0c42473857d369631f2f63f9d81f5f0248ec6833d41ac6.
- r002 source reference pixels were locally consulted only: NPS-PAVEMENT photo SHA-256 aa21ae7f5292c6876bc7335d19e8d93930d9b84eee0fb4cd2766063d1fd35052. The consulted pixels were not incorporated or redistributed. The rights ledger identifies the NPS source as third-party rights retained; the original generated concept is CC-BY-4.0 and generator/support code MIT.
- The r002 repair freeze is 2026-10-20T15:54:35.477003Z; authoring-start is 2026-10-20T15:55:12.632508Z. The seven design input file hashes in modeling-freeze.json all match their current bytes. The saved source and GLB match the handoff hashes. All 15 declared source/dependency closure hashes match, including the exact generator, helper, exporter/audit, queue runner, validator, package lock and render/runtime scripts. Generator records no referenced image/mesh/texture or network input.
- The candidate validation record is internally valid but approval_status remains pending and approved_for_brief=false.

Images and visual/reference comparison

Manifest subject binds r002 GLB 8ac4620cfec4bfaa6d14a0098144217383ea1623199fb52aa73348b1659a249e, brief b47d9a732174b88ec4e23d81f7e95474a6deac997c993713252cef2fcfe848fb and references 621a0a83000b52c06ae2c7c181097913fbfc17d21d623aa6102c294337d69257. Each final frame independently matches its manifest SHA, byte length and 512x512 dimensions:
- hero: 1597a07625650eaeb1d881ea4075cfd24f349fbe4cdb4b7ec3e5254724c076f4
- reversehero: 3b2c46a5cc10d6a800600f6d5ea75723234a10dafb4bdef7e154d3c0fc90701a
- front: 55c62bf1cd54c2184424395b518bb24c9eb3291167eb26fc31945b548a94956d
- side: 48ae938272adbda407e7ff99461f061e1297e6f3b9e6bbf12ec4be1f36a8324c
- rear: 68fc5f4e041d7bc0b755e3e6a28c30019bde3720f26ff7cb55cf22a428814f77
- top: f75e07cd41c62145704afd92bc0776881ae5f7008f9172e514ada5180c0c1567
- clay: 4471271a060e74fec769eb053546c66d790f54581e1aec96e52b9aaa1173e476
- silhouette: c5ae89e8d36919f335c319b7ae7775cd40f857353794b44bdd1605d1f7866623
Contact sheet: SHA-256 4fca9282b282ced95752fdcadfbf1b043ea1c1e9518ae288f90f5bce4838a9a8, 923199 bytes, 2048x1060.

The NPS source pixels show dense, irregularly fitted clasts with unequal spacing, shape and crown. r002 preserves a dense fitted mantle and narrow cracks, not bare sand patches or loose gravel. The exact silhouette/front/rear/side views retain the low thin form. The source makes no claim to reconstruct a named locality, exact scale/clast size, age, varnish chemistry, ecosystem or single formation process; the generic educational claim scope remains bounded.

Static technical, source, and runtime checks

- Static GLB audit: pass; 6,816 triangles, 4 materials, 4 primitives, 14,142 POSITION accessor vertices, 384,792 bytes, 0 textures; measured GLB bounds 4.7225704 x 0.3233644 x 4.0613174 m. Static audit report records no errors/warnings and matches the target hash. Khronos validator 2.0.0-dev.3.10 independently reports 0 errors, 0 warnings, 0 infos and 0 hints.
- Blender 4.3.2 read-only source reopen/export-collection check passes. A separate actual source reopen and Blender GLB re-export under blocking flock /tmp/lowpoly-production-blender.lock produced a byte-identical 384,792-byte GLB (same SHA-256), same semantic hash bb8dc52ca9f4b15ff1a11311cd4ce650b0af37191d8e96c3344e4e76932e7938, 6,816 triangles and identical bounds. The source was not saved or altered.
- Independent Node Three.js 0.180.0 GLTFLoader CPU parse passes on the exact shipped GLB: 6,816 triangles, 4 meshes/materials, expected bounds, zero parse errors. This is not GPU or scene evidence.
- The two existing rebuild-queue jobs were independently verified from separate request/result records. Rebuild 1: request SHA-256 c001628c7a49d0db18e2b0a8be608c21ee416f7d6c91610123b46f440e63592a, result SHA-256 22d3913b1ea6232a846f8a66d087edba3327341e230e96b26bd8fe30869c3cd0, fingerprint b459e610fc590a2fd622936f56f6287476487d651fbf0c970ddd61f162e6d23b, PID 92, 15:55:21.318728Z–15:55:24.967210Z. Rebuild 2: request SHA-256 7c0a803751822f754585d8c38073c6a1cac5a3337d8175c651c2e59803b4e6e0, result SHA-256 f7c66045e2f17d11707036f8f4b2b82b8ceb7c26e1e08f7de649381cfbd9d9c4, fingerprint 00478094cf04ce016dea463d1ea501b022fb40fbc6cedae28299856a1d708ca0, PID 115, 15:55:24.972678Z–15:55:28.424072Z. Both are distinct, returned zero, passed input and output hash checks, and independently regenerated the exact target GLB SHA and identical semantic hash. Their generated .blend file byte hashes differ (10121bdfcdeb21e1d0a0afa1968f5662d75a91ae63391adc42bcd7f234e9bce0 vs 5f9d55d2a670982f0af8d801f2e206bac6aeac60804d0db5a01c0a61154c53ea), consistent with Blender file metadata; the actual shipped source re-exported byte-for-byte to the target GLB. The queue used one worker, two threads, blocking global flock and no overlap/starvation.
- The target palette is exactly unchanged from r001: clast #69645B, clastlight #898172, clastdark #514F49, sand #AC9675. Renderer/engine, resolution 512, 16 samples, camera type/orbit/elevation/background/view transform, light directions and world strength are unchanged. The exact render-config bytes are not identical: derived orthographic scale shifts 5.33740957846423 to 5.337592857201926, target Z 0.15477566421031952 to 0.16168218851089478, and light energy/size shifts by less than 0.007% (calculated from the changed bound height 0.3095513 to 0.3233644m). These small bound-driven fit/lighting deltas do not conceal geometry, but the r002 concept-evidence note says “original palette and cameras unchanged.” That wording is inaccurate at the parameter level and should be corrected to describe the tiny auto-fit/bounds deltas; do not change geometry or scope to hide them.

Separate stage decisions

- technical: PASS (static audit, Khronos, source topology, budgets, dependency/provenance checks).
- visual: ACCEPT BOUNDED for the original repair finding. Top-view tessellation is a visible residual, not a concealed failure; overall irregular multiscale form now satisfies the frozen visual target.
- factual: PASS BOUNDED (generic illustrative dense clast armor only; claims do not exceed consulted source or claim site-specific reconstruction).
- specification: REVISE / OPEN. The r002 repair freeze is correctly pre-authoring and all listed hashes match. However, original concept integrity is valid while evidence completeness remains false because concept-generation.json has provider_generation_timestamp=null; the validation blocker explicitly says concept_generated_at is unknown and must not be inferred from filesystem times. This uncertainty persists from r001. Also correct the inaccurate “cameras unchanged” note described above. Do not fabricate timestamp or loosen the frozen scope.
- runtime_parse: PASS (Node CPU parser only).
- gpu: BLOCKED / NOT RUN.
- scene: BLOCKED / NOT RUN.

Full-candidate status: BLOCKED from formal/user/release acceptance until specification evidence is accurately bounded and the required GPU and composed-scene checks are actually performed by the proper target runtime. Neither CPU renders nor Node parsing stand in for those checks. No approval/ledger, producer, CI, release, website, GitHub, or remote state was changed by this QA.

Per-ID dispositions and immutable r001 references

- marpolia r001: ACCEPT BOUNDED in the original QA; source SHA-256 e830edf6bca1b29bca2cb44517e4bca91af7fffe03ed6d4e7647ef77b9a610d3; GLB SHA-256 5b65c0ee2a58b4a7c075c86fecb916c8e8892c611f7e67e39c5682c45e5a318e; original independent report SHA-256 3c71bcae85ac5585b47f8834f20cd8c1cd37ff381f0502de4df8cfac3f53c7d9.
- balanced-rock r001: ACCEPT BOUNDED in the original QA; source SHA-256 36b281edd9cc1d1796f97bbd7cde4e1247a91063823b31618ed6f8dc68d72332; GLB SHA-256 a312c02e56e77ac69a3a6332ab70b0f660c6b68c90c98dd40e5329a7a478132a; original independent report SHA-256 7534e647a8054cea2039fbe22d481c79f87b9d12595eec88bff1feb47b49416e.
- u-shaped-glacial-valley r001: ACCEPT BOUNDED in the original QA; source SHA-256 b18aaa05d9a3203c1e815e2f31a57bf423bcb9854c8816ada43943dc706f2a82; GLB SHA-256 9a287ebb7b43b08460c1923a3a1b2b945a403cdb2795112da9d1fb20666c8cc1; original independent report SHA-256 3d9095ac1268fdfd432af204084b4d27d961d46961e254c7cd0c66198e3e89cc.
- desert-pavement r001: REVISE in the original QA; source SHA-256 2573cd27d972c1ce1827b9175272dc44c43e4ab4ecb362e8fe2b6f10d3fab3e9; GLB SHA-256 9e2af794d7b257410101072e118915838b99d6d24fe83ad38e6d73ae13a37758; original independent report SHA-256 2d74d0edcb78e997c5c904e1b69cb7a90ad02783ae4629eb4be24f7d64d4528f.
- desert-pavement r002: targeted visual repair ACCEPT BOUNDED (hashes as above); full candidate BLOCKED for open specification and unrun GPU/scene.

The accepted three r001 asset directories still have 156/156 unchanged full-file SHA-256 hashes. All 180 original tracked r001 files across the four asset directories have identical Git blob IDs from base commit 0e61511ad96c905e16139a9489cfaac5b80b51f6 to pinned current commit f6e5b25a4054747ec76714051e60b3bf42514be1. Original QA.md hash is unchanged. The full original QA evidence file/hash inventory is in original-evidence-inventory.txt in this differential folder; original queue request/result/stdout/stderr are retained in the producer tree and were not copied. The original report and ledger remain untouched.

New raw evidence in this differential folder: asset-provenance-closure.json, unchanged-closure-independent.json, image-and-render-binding.json, static-glb-qa.json, khronos-independent.json, source-reopen-export.json/.log, source-reexport-verified.json/.log/.glb, three-independent.json, rebuild-queue-independent.json and original-evidence-inventory.txt. None of those files are approval records.
