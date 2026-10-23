# SPDX-License-Identifier: MIT
"""Thin adapter around the pinned canonical actual-GLB renderer.
Adds only the brief's exact (+X,-Y,+Z) perspective and required underside.
Use --clay-all to obtain preflight gray geometry images; never considered final.
"""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
r.DIRECTIONS['perspective']=(45,math.degrees(math.atan(1/math.sqrt(2))))
r.DIRECTIONS['ventral']=(0,-90)
if '--clay-all' in sys.argv:
    sys.argv.remove('--clay-all')
    # Canonical shader-override modes, repointed to three useful preflight axes.
    r.DIRECTIONS['clay']=(45,math.degrees(math.atan(1/math.sqrt(2))))
    r.DIRECTIONS['clayalt']=(0,90)
    r.DIRECTIONS['clay-alt']=(90,0)
    if '--views' in sys.argv: sys.argv[sys.argv.index('--views')+1]='clay,clayalt,clay-alt'
r.main()
