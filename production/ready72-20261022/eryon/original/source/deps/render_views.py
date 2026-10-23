# SPDX-License-Identifier: MIT
"""Thin v2 view adapter around unmodified canonical exact-GLB renderer."""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['perspective']=(45,math.degrees(math.asin(1/math.sqrt(3))))
if __name__=='__main__': renderer.main()
