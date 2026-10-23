# SPDX-License-Identifier: MIT
"""Call the pinned canonical renderer with the frozen (1,-1,1) perspective."""
import math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
r.DIRECTIONS['hero']=(45,math.degrees(math.atan(1/math.sqrt(2))))
if __name__=='__main__': r.main()
