# Rebuild and check

Blender 4.3.2, generator seed 0, bundled Python. Run from the package root:

blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output rebuilt

The copied source/deps helpers are portable, unchanged project build infrastructure. The
Callichimaera generator and anatomical parameters are original for this candidate. No earlier
animal geometry or facts were reused. Generation needs no external images, models or network.

For official format validation and Three.js CPU parsing, install pinned dependencies with
npm ci --ignore-scripts inside source, then run:

node source/check_glb.mjs model.glb qa/evidence

For canonical exact-export renders:

blender -b -t 2 --python-exit-code 1 --python source/render_views.py -- model.glb --output views --resolution 768 --samples 48

Run only one Blender process per model task, two threads; check at least 2 GiB available RAM
and 1.5 GiB free disk before each heavy job, with no more than four concurrent heavy jobs
across the authorized queue. The asset uses real meters, not a display-normalized bounding box.
Independent review, browser GPU rendering and populated-world performance are separate gates.
