#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Thin local adapter: exact-GLB perspective at declared (+X,-Y,+Z)."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,35.264389682754654)
renderer.main()
