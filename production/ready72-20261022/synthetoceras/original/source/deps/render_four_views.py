# SPDX-License-Identifier: MIT
"""Thin fixed-four-view wrapper around the unmodified canonical renderer."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,35.264389682754654)
renderer.main()
