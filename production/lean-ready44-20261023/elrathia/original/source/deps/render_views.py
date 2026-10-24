# SPDX-License-Identifier: MIT
"""Four-view exact-GLB adapter; --gray-all uses the renderer material override."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.asin(1/math.sqrt(3))))
renderer.main()
