# Reproducible source index: spyroceras

Seven source roles and their exact byte hashes are in evidence.json. Generator and required helper bytes are unchanged. Relocation preserves relative import behavior; Lituites additionally has its exact required ../references/source-outline.json.

Rebuild with Blender 4.3.2 from repository root, writing to a new empty directory outside the source:

    blender -b -t 2 --factory-startup --disable-autoexec --python-exit-code 1 --python production/recovery-20261022/spyroceras/source/generator.py -- --config production/recovery-20261022/spyroceras/source/config.json --output-dir /path/to/empty-rebuild

No rebuild was claimed or run during this release preparation. Previously independent reproducibility evidence is bound through the original acceptance SHA. Source references/dependency lists intentionally retain historical process identity pins; those private inputs are not build runtime dependencies and are not copied into Git. Briefs retain exact specimen/scientific limitations.

The Blend and GLB are the original accepted final bytes. presentation/ contains final render configuration only, not modeling changes. The common presentation-source renderer imports a clean GLB and adds only display lighting/camera/shadow-catcher geometry; it never writes or re-exports the accepted source.

Original process backup is privately verified. This new release projection and any new final preview renders have not been uploaded or published.
