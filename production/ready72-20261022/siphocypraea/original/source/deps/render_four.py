# SPDX-License-Identifier: MIT
"""Four-view adapter: canonical hero set exactly to (+X,-Y,+Z)."""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.atan(1/math.sqrt(2))))
renderer.main()
