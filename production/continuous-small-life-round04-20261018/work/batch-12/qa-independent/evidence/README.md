# Evidence bundle

The JPEGs in `images/` are the source and exact-GLB runtime contact sheets from source commit `b7a0582edbaa4e6cdea0f04524c6c59166987e56`. They are copied byte-for-byte; their SHA-256 hashes are listed in `reports/image-copy-hashes.json` and match the source handoff.

The `reports/` directory contains independently rerun current-main GLB, Khronos, Blend reopen, source/export, and static-profile outputs. The `logs/` directory preserves the exact commands, console results, source-ref check, checksum verification, and the reproduced historical queue failure. `reports/hash-audit.json` binds each selected checkpoint, GLB, Blend, candidate, freeze, generator, config, view manifest, and image sheet to the source handoff.

These are review artifacts. They do not edit or replace the source candidate. The scripts and exact temporary paths used for the runs are shown in `logs/commands.log`.
