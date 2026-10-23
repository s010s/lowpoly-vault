# SPDX-License-Identifier: MIT
# Small asset-specific adapter, using canonical exact-GLB render implementation.
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['perspective']=(45,35.264389682754654)
renderer.main()
