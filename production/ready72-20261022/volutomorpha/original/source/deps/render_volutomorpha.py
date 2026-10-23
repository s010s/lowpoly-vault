#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Canonical renderer wrapper: front/side/top and exact (+X,-Y,+Z) perspective.
All other renderer behavior is the pinned canonical implementation.
Use --views front,side,top,hero --turntable-frames 0.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,35.264389682754654)
if __name__=='__main__': renderer.main()
