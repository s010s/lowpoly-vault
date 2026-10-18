# Bird pair runtime QA

Current result: **r2 PASS** for both exact corrected static props. [Full corrected review and evidence](actions-evidence-r2/README.md).

The first actual browser run exposed inconsistent triangle winding despite mechanical checks passing. [Original failure and screenshots](actions-evidence/README.md) are preserved unchanged. The producer corrected face winding without shape or palette changes. The same browser harness, with only input hashes and the source checkout pin changed, then passed mechanical checks and actual screenshot inspection.

No main merge, deployment, hardware-performance claim or animation-readiness claim is implied.
