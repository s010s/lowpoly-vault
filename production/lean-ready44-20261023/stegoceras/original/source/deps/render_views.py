# SPDX-License-Identifier: MIT
"""Exact-GLB v2 diagonal renderer. ASSET_CLAY=1 is a temporary gray diagnostic."""
import math, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.atan(1/math.sqrt(2))))
if os.environ.get('ASSET_CLAY')=='1':
    original=renderer.make_material
    def material(*args,**kwargs):
        result=original(*args,**kwargs)
        import bpy
        for mat in bpy.data.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type=='BSDF_PRINCIPLED':
                        node.inputs['Base Color'].default_value=(.287,.287,.287,1)
                        node.inputs['Roughness'].default_value=.85
        return result
    renderer.make_material=material
if __name__=='__main__':renderer.main()
