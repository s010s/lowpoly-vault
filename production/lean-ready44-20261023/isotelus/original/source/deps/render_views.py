# SPDX-License-Identifier: MIT
"""Exact-GLB four-view adapter; hero uses the frozen (1,-1,1) direction."""
from pathlib import Path
import sys, math
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.asin(1/math.sqrt(3))))
renderer.main()
