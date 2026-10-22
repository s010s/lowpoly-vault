# fault-scarp final source

The seven source roles and original hashes are indexed in evidence.json. Rebuild contains only exact generator inputs and helper dependency bytes, with the original relative layout retained. Original dependency-list bytes retain archived paths and process-only ancestors as provenance, not required runtime inputs. No historic failed or superseded GLB is included.

Final GLB and Blend are the exact production-accepted bytes, never rerender exports. New gallery posters are freshly rendered from that unchanged GLB and need independent final-pixel review. Reference media and detailed QA process materials are excluded. Model license: CC-BY-4.0; source code: MIT. All scientific limits remain in the bilingual metadata and credits.

## Rebuild verification

One fresh execution from this relocated source projection produced a byte-identical GLB. The delivered Blend remains the original exact accepted Blend, not the fresh rebuild save. Run from the git-ready root with Blender 4.3.2, using an empty output directory:

/usr/bin/blender -b -t 2 --factory-startup --disable-autoexec --python-exit-code 1 --python-expr 'import sys;sys.dont_write_bytecode=True' --python production/next-eleven-20261022/fault-scarp/rebuild/source/build.py -- --output YOUR_EMPTY_OUTPUT_DIRECTORY
