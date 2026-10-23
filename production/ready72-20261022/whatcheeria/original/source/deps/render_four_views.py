# SPDX-License-Identifier: MIT
"""Four-view configuration wrapper; canonical renderer stays unchanged."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_candidate_views
render_candidate_views.DIRECTIONS['hero']=(45,math.degrees(math.asin(1/math.sqrt(3))))
render_candidate_views.main()
