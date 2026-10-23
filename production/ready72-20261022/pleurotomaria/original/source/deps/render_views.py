# SPDX-License-Identifier: MIT
"""Four-view v2 adapter. Exact GLB imported by the canonical renderer."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['perspective']=(45,35.264389682754654)
renderer.main()
