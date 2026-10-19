# SPDX-License-Identifier: MIT
"""Reuse repository clean-GLB renderer with a retained approximate concept angle.
The generated illustration has no measured camera; 70deg azimuth/12deg elevation
is an authored visual approximation, not a recovered calibrated camera.
"""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/render_candidate_views.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
import render_candidate_views as renderer
renderer.DIRECTIONS['concept-match']=(70,12)
# Config's renderer hash identifies this exact wrapper. The underlying helper
# and renderer are separately pinned in the handoff dependency ledger.
renderer.__file__=__file__
_digest=renderer.digest
renderer.digest=lambda path: _digest(REPO/'scripts'/Path(path).name if Path(path).name in {'asset_common.py','qa_glb.py'} else path)
renderer.main()
