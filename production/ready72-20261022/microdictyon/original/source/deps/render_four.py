#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Thin adapter: canonical exact-GLB renderer, four approved camera directions."""
import sys, math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['perspective']=(45,math.degrees(math.atan(1/math.sqrt(2))))
renderer.main()
