# SPDX-License-Identifier: MIT
"""Local thin entry point selecting the v2 declared (+X,-Y,+Z) hero pose.
The copied canonical renderer is unchanged. All flags remain its CLI contract.
"""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45, math.degrees(math.atan(1/math.sqrt(2))))
renderer.main()
