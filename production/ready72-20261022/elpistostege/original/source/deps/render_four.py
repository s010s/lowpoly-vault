# SPDX-License-Identifier: MIT
"""Thin reproducible view-profile wrapper around the pinned canonical renderer.
--gray renders actual-GLB 4-angle structural evidence, with one gray material.
"""
from pathlib import Path
import sys, math
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as R
R.DIRECTIONS['hero']=(45,math.degrees(math.asin(1/math.sqrt(3))))
if '--gray' in sys.argv:
    sys.argv.remove('--gray')
    original_vertices=R._vertices_world
    def gray_vertices(collection):
        points=original_vertices(collection)
        gray=R.make_material('_diagnostic_gray','#969A9B',roughness=.9)
        for ob in collection.all_objects:
            if ob.type=='MESH':
                ob.data.materials.clear(); ob.data.materials.append(gray)
                for face in ob.data.polygons: face.material_index=0
        return points
    R._vertices_world=gray_vertices

R.main()
