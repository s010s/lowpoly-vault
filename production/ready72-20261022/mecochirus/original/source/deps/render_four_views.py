# SPDX-License-Identifier: MIT
"""Thin canonical-render wrapper for the v2 (+X,-Y,+Z) perspective camera.
Usage is identical to render_candidate_views.py, with --views front,side,top,perspective.
"""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['perspective']=(45.0,math.degrees(math.atan(1/math.sqrt(2))))
if __name__=='__main__':renderer.main()
