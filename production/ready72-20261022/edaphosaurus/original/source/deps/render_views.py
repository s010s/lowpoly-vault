# SPDX-License-Identifier: MIT
"""Use the pinned canonical renderer with the frozen v2 diagonal hero pose.
The hero is (+X,-Y,+Z), azimuth45/elevationatan(1/sqrt(2)).
All actual camera angles are retained in canonical render-config/manifest.
"""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.atan(1/math.sqrt(2))))
if __name__=='__main__':renderer.main()
