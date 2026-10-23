#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Local exact-export view entrypoint, using pinned canonical renderer.
Hero camera is (1,-1,1) in authoring coordinates, reused as preview/perspective.
"""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.atan(1/math.sqrt(2))))
if __name__=='__main__':renderer.main()
