#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exact delivered GLB four-view wrapper. REPENOMAMUS_CLAY=1 for prechecks."""
import sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
r.DIRECTIONS['perspective']=(45,35.264389682754654)
if os.environ.get('REPENOMAMUS_CLAY')=='1':
    import bpy
    original=r._look_at
    def look(o,t):
        original(o,t)
        for m in bpy.data.materials:
            if not m.name.startswith('_') and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type=='BSDF_PRINCIPLED':n.inputs['Base Color'].default_value=(.3,.3,.3,1)
    r._look_at=look
r.main()
