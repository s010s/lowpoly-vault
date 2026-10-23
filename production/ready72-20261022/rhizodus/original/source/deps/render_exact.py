# SPDX-License-Identifier: MIT
"""Use the unchanged canonical renderer with the frozen (+X,-Y,+Z) view."""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as render
render.DIRECTIONS['perspective']=(45,math.degrees(math.asin(1/math.sqrt(3))))
render.main()
