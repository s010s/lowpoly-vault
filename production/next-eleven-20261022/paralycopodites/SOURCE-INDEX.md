# paralycopodites final source

Seven source roles retain the original accepted subject hashes in the evidence index. The generator, config, native files and helper dependencies are unchanged. The public references and dependency annotation JSONs are explicitly derived: only nonexecuted private absolute locators are removed, and the affected reference-file integrity pin is updated. Original and public hashes are distinct; this is not claimed to be an exact copy of those two original annotation roles. Actual rebuild-relative paths are retained. No historical failed or superseded GLB is included.

Final GLB and Blend are the exact production-accepted bytes, never rerender exports. New gallery posters are freshly rendered from that unchanged GLB and need independent final-pixel review. Reference media and detailed QA process materials are excluded. Model license: CC-BY-4.0; source code: MIT. All scientific limits remain in the bilingual metadata and credits.

## Rebuild verification

One fresh execution from this relocated source projection produced a byte-identical GLB. The delivered Blend remains the original exact accepted Blend, not the fresh rebuild save. Run from the git-ready root with Blender 4.3.2, using an empty output directory:

/usr/bin/blender -b -t 2 --factory-startup --disable-autoexec --python-exit-code 1 --python-expr 'import sys;sys.dont_write_bytecode=True' --python production/next-eleven-20261022/paralycopodites/rebuild/assets/paralycopodites/recovery-r001/generator.py -- --config production/next-eleven-20261022/paralycopodites/rebuild/assets/paralycopodites/recovery-r001/build-config.json --output YOUR_EMPTY_OUTPUT_DIRECTORY
