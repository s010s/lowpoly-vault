# SPDX-License-Identifier: MIT
"""Small local adapter for v2's four fixed views, reusing canonical exact-GLB renderer."""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
# Required (+X,-Y,+Z) direction, rather than the older 35/20 hero preset.
r.DIRECTIONS['perspective']=(45,math.degrees(math.asin(1/math.sqrt(3))))
if '--gray' in sys.argv:
    sys.argv.remove('--gray')
    original=r.make_material
    # Gray model is produced by temporarily overriding all imported mesh materials.
    import bpy
    handler=[]
    def clay_before(scene):
        if not handler:
            m=original('gray-inspection','#929292',roughness=.9)
            for obj in list(scene.objects):
                if obj.type=='MESH':
                    obj.data.materials.clear(); obj.data.materials.append(m)
            handler.append(True)
    bpy.app.handlers.render_pre.append(clay_before)
r.main()
