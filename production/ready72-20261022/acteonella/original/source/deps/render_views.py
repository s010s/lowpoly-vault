# SPDX-License-Identifier: MIT
"""Small view adapter over the copied canonical renderer. No hidden assets."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as r
r.DIRECTIONS['hero']=(45,35.264389682754654)
if '--clay-all' in sys.argv:
    sys.argv.remove('--clay-all')
    original=r.make_material
    def gray_material(*args,**kwargs): return original(*args,**kwargs)
    # Material override in the render operator is applied to every diagnostic direction.
    import bpy
    @bpy.app.handlers.persistent
    def before_render(scene):
        clay=bpy.data.materials.get('_candidate_clay')
        if clay: bpy.context.view_layer.material_override=clay
    bpy.app.handlers.render_pre.append(before_render)
r.main()
