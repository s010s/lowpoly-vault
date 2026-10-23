#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Exact-GLB renderer wrapper; canonical helper unchanged. For gray precheck,
set VOLATICOTHERIUM_CLAY=1. All images are freshly imported delivered geometry."""
import sys, os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
r.DIRECTIONS['perspective']=(45,35.264389682754654)
if os.environ.get('VOLATICOTHERIUM_CLAY')=='1':
    import bpy
    original=r._look_at
    def look(obj,target):
        original(obj,target)
        # Called before each render after import; recolor model materials in-place.
        for m in bpy.data.materials:
            if not m.name.startswith('_') and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type=='BSDF_PRINCIPLED':n.inputs['Base Color'].default_value=(.3,.3,.3,1)
    r._look_at=look
r.main()
