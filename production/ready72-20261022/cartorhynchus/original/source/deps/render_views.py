# SPDX-License-Identifier: MIT
"""Four-view profile wrapper around the unchanged pinned canonical renderer."""
from pathlib import Path
import math,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['perspective']=(45,math.degrees(math.atan(1/math.sqrt(2))))
renderer.main()
