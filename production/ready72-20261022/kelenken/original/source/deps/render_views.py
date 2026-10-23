# SPDX-License-Identifier: MIT
"""Exact-GLB canonical renderer adapter; declares the template octant camera."""
import math, pathlib, sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import render_candidate_views
render_candidate_views.DIRECTIONS['hero']=(45,math.degrees(math.atan(1/math.sqrt(2))))
if __name__=='__main__':render_candidate_views.main()
