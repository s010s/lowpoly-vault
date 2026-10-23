#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Thin local wrapper: fixed canonical +X/-Y/+Z perspective, four views only.
The copied canonical renderer is unchanged. Every render is a clean GLB import.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as render
render.DIRECTIONS['hero']=(45,35.264389682754654)
render.DIRECTIONS['detail']=(10,15)
if __name__=='__main__': render.main()
