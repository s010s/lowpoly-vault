# SPDX-License-Identifier: MIT
"""Thin exact-GLB canonical renderer adapter; private clay mode is not final QA."""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
r.DIRECTIONS['perspective']=(45,math.degrees(math.atan(1/math.sqrt(2))))
r.DIRECTIONS['ventral']=(0,-90)
if '--clay-all' in sys.argv:
    sys.argv.remove('--clay-all');r.DIRECTIONS['clay']=(45,math.degrees(math.atan(1/math.sqrt(2))));r.DIRECTIONS['clayalt']=(0,90);r.DIRECTIONS['clay-alt']=(90,0)
    if '--views' in sys.argv:sys.argv[sys.argv.index('--views')+1]='clay,clayalt,clay-alt'
r.main()
