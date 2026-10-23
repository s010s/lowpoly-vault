#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exact-export four-view launcher; canonical camera, light and color helper.
Hero direction is explicitly (1,-1,1), matching the v2 brief. This wrapper does
not edit the copied canonical renderer, exported mesh, or saved Blender source.
"""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.asin(1/math.sqrt(3))))
if __name__=='__main__': renderer.main()
