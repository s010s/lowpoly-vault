# Confuciusornis material candidate

Status: **in progress; not release-ready**. This commit preserves the actual reviewed candidate, not a production manifest replacement. The deployed model remains unchanged.

The material-only edit improves wing and belly readability. Geometry, UVs and the GLB binary payload are unchanged. `source.blend` is an editable import of this candidate with packed images, not the original modeling session. `wheel.png` and `detail.png` belong to this candidate only.

Independent scoped review confirmed asset pairing and material improvement. Transition residuals and complete repository integration remain unresolved. Limited local screenshot tests are not full production or real-device acceptance.

## Continue this same branch

1. Integrate candidate paths, checksums, size and provenance through the repository's existing same-ID successor contract. Do not relabel old golden poster approvals.
2. Integrate the shared transition fix as a separately reviewable source change. Do not copy diagnostic compiled bundles or cumulative model allowlists.
3. Generate/check final poster metadata and actual GLB/Blend download mapping against the integrated version.
4. Run targeted visual checks and full PR CI, obtain independent final review, then include in an authorized release batch.

The four final assets and a small machine-readable receipt live here. Bulk debugging logs and private operational records are deliberately excluded.
