# Independent engineering review checkpoint

17 October 2026. A fresh review read the Skills, exercised the actual producer/consumer contract, and tested failure paths before the final checkpoint. This review does not certify asset aesthetics, science, target GPU behavior or production throughput.

Six concrete issues were reproduced, fixed and independently retested:

1. JSON numeric overflow (`1e309`) could bypass camera coverage checks. The JSON decoder and numeric consumers now reject nonfinite values.
2. A resume record containing a valid JSON list could crash the scheduler. Malformed result/request/identity/output shapes are now ineligible for reuse and start a fresh attempt.
3. A raw static report could omit a warning found by the current computed audit. Current warning/error/status data must match before explicit warning reviews count.
4. Rehashed replacement pixels could retain an old visual decision. Passing reports now seal reviewed evidence digests; final approval seals the complete review snapshot.
5. New technical report fields initially lacked executable producers. Source/export and semantic rebuild adapters now measure actual files. Rebuild without a successful hash-bound execution record remains unknown.
6. Missing rebuilt-output hashes could compare equal as null. Provenance now requires correctly shaped digests and nested records.

Forward tests included an actual 34-frame Blender arch pack, deliberately incomplete coverage rejection, actual editable-source/export comparison (672 triangles, 0.0 m bounds delta), and an actual bounded deterministic-generator run. The same semantic outputs without run provenance return unknown/exit 2. Pending templates fail; the real Triceratops negative study and repository pending arch cannot pass `--require-approved`.

Latest complete v1 suites include 14 static-GLB, 75 candidate, 14 queue, 1 real-asset integration and 21 technical-producer tests. Formal manifest integration and all 46 exact-ten initial-release checks pass. No unresolved blocker remained within this bounded engineering review.

Limits remain explicit: reviewer identity/inspection and run records are not cryptographically authenticated; image-header validation does not decode every pixel; source count/bounds do not alone prove material fidelity; process-group cleanup is not hard-host-failure containment. Record integrity is necessary but not sufficient for asset acceptance.
