# SPDX-License-Identifier: MIT
"""Thin canonical renderer wrapper: four required v2 cameras, no turntable."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as R
R.DIRECTIONS['perspective']=(45,35.264389682754654)
if __name__=='__main__':R.main()
