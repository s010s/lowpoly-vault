Batch 67 independent local QA (round 26)

Pinned to commit b4322a6d83a863051f56b3caa58e4fa3a11dfea3 on candidate/small-life-batch67-concept-20261020. Producer worktree remained clean. This report covers only the four named r001 candidates.

Overall: three bounded local passes and one visual/specification REVISE. No formal/user/release approval, upload, push, merge, deployment, or candidate/ledger mutation occurred.

Independent technical evidence passes for all four: static GLB budgets, official Khronos validation (zero errors/warnings), Node Three.js 0.180.0 CPU parse, and Blender 4.3.2 read-only source reopen/topology checks. All eight exact 512×512 view PNGs per asset match their render manifest; each lossless 2048×1060 PNG contact sheet and all source pixels/concepts were personally inspected. Source pixel SHA values match the ledger. Two distinct queued rebuilds per asset have separate job IDs, request/result files, fingerprints, PIDs, timestamps and outputs; all eight GLBs are byte-identical to the pinned target and independently semantic-equal. The single queue run ID is shared by the batch as expected. Blocking global flock wrapper was verified, with Blender two threads; queue completed sequentially without failure or starvation.

Per-ID results:

- marpolia r001: ACCEPT BOUNDED
  Source SHA-256: e830edf6bca1b29bca2cb44517e4bca91af7fffe03ed6d4e7647ef77b9a610d3
  GLB SHA-256: 5b65c0ee2a58b4a7c075c86fecb916c8e8892c611f7e67e39c5682c45e5a318e
  Independent report SHA-256: 3c71bcae85ac5585b47f8834f20cd8c1cd37ff381f0502de4df8cfac3f53c7d9
  Stages: technical pass; visual pass_bounded; factual pass_bounded (consulted primary sources match bounded claims; no exact locality, age, size, attachment, or exclusive-process claims); specification pass_bounded; runtime_parse pass; gpu not_run / blocked unknown; scene not_run / blocked unknown.
  Visual/factual finding: the ROM 57841 specimen direction is followed; this is a shallow fan-shaped fossil specimen, not a complete plant. No M. aequalis retouched image was used for the comparison.

- balanced-rock r001: ACCEPT BOUNDED
  Source SHA-256: 36b281edd9cc1d1796f97bbd7cde4e1247a91063823b31618ed6f8dc68d72332
  GLB SHA-256: a312c02e56e77ac69a3a6332ab70b0f660c6b68c90c98dd40e5329a7a478132a
  Independent report SHA-256: 7534e647a8054cea2039fbe22d481c79f87b9d12595eec88bff1feb47b49416e
  Stages: technical pass; visual pass_bounded; factual pass_bounded (consulted primary sources match bounded claims; no exact locality, age, size, attachment, or exclusive-process claims); specification pass_bounded; runtime_parse pass; gpu not_run / blocked unknown; scene not_run / blocked unknown.

- u-shaped-glacial-valley r001: ACCEPT BOUNDED
  Source SHA-256: b18aaa05d9a3203c1e815e2f31a57bf423bcb9854c8816ada43943dc706f2a82
  GLB SHA-256: 9a287ebb7b43b08460c1923a3a1b2b945a403cdb2795112da9d1fb20666c8cc1
  Independent report SHA-256: 3d9095ac1268fdfd432af204084b4d27d961d46961e254c7cd0c66198e3e89cc
  Stages: technical pass; visual pass_bounded; factual pass_bounded (consulted primary sources match bounded claims; no exact locality, age, size, attachment, or exclusive-process claims); specification pass_bounded; runtime_parse pass; gpu not_run / blocked unknown; scene not_run / blocked unknown.

- desert-pavement r001: REVISE
  Source SHA-256: 2573cd27d972c1ce1827b9175272dc44c43e4ab4ecb362e8fe2b6f10d3fab3e9
  GLB SHA-256: 9e2af794d7b257410101072e118915838b99d6d24fe83ad38e6d73ae13a37758
  Independent report SHA-256: 2d74d0edcb78e997c5c904e1b69cb7a90ad02783ae4629eb4be24f7d64d4528f
  Stages: technical pass; visual revise; factual pass_bounded (consulted primary sources match bounded claims; no exact locality, age, size, attachment, or exclusive-process claims); specification revise; runtime_parse pass; gpu not_run / blocked unknown; scene not_run / blocked unknown.
  Visual finding: dense single-layer coverage is present, but the near-uniform Voronoi tessellation reads as decorative paving and does not sufficiently vary clast size/shape. Revise without opening large bare patches.

Shared limitations: the candidate records still show approval pending; CPU images are not GPU evidence, and Node parsing is not target-browser evidence. GPU and composed scene are unrun. The ImageGen provider-internal generation timestamp is unknown; observed request/result/pixel inspection and authoring-start timestamps remain distinct and are not inferred from filesystem mtimes. Concept evidence integrity is valid, but completeness remains false solely for the unavailable provider timestamp.

Full per-asset records and evidence logs are in this directory. Producer queue request/result/stdout/stderr records remain in the pinned producer tree; independent copies were not made. No consulted source images were copied to this QA directory.
