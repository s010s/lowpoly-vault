#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Call pinned canonical exact-GLB renderer with the frozen (+X,-Y,+Z) hero."""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.asin(1/math.sqrt(3))))
if __name__=='__main__':renderer.main()
