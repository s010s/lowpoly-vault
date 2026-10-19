# SPDX-License-Identifier: MIT
"""Clean-import exact-GLB evidence with an approximate concept perspective.
The illustration has no calibrated camera. 55deg azimuth /32deg elevation is an
explicit authored approximation shared by all four assets, not recovered truth.
"""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/render_candidate_views.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
import render_candidate_views as renderer
renderer.DIRECTIONS['concept-match']=(55,32)
renderer.__file__=__file__
_digest=renderer.digest
renderer.digest=lambda path:_digest(REPO/'scripts'/Path(path).name if Path(path).name in {'asset_common.py','qa_glb.py'} else path)
renderer.main()
