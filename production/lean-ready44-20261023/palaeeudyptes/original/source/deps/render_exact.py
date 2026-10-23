# SPDX-License-Identifier: MIT
"""Minimal canonical renderer adapter for the declared cardinal and diagonal views."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
if '--gray' in sys.argv:
    sys.argv.remove('--gray')
    renderer.DIRECTIONS['clay']=(0,0)
    renderer.DIRECTIONS['clayalt']=(90,0)
    renderer.DIRECTIONS['clay-alt']=(0,90)
    renderer.DIRECTIONS['wire']=(45,35.264389682754654)
else:
    renderer.DIRECTIONS['hero']=(45,35.264389682754654)
renderer.main()
