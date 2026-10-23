# SPDX-License-Identifier: MIT
"""Thin asset view adapter; canonical helper remains byte-for-byte unchanged.
Adds exact (+X,-Y,+Z) perspective. Optional --gray uses a pre-render gray override.
"""
import math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
import render_candidate_views as renderer
renderer.DIRECTIONS['perspective']=(45,math.degrees(math.asin(1/math.sqrt(3))))
if '--gray' in sys.argv:
 sys.argv.remove('--gray')
 original_vertices=renderer._vertices_world
 def gray_vertices(collection):
  for obj in collection.all_objects:
   if obj.type!='MESH':continue
   for mat in obj.data.materials:
    for node in mat.node_tree.nodes if mat.use_nodes else []:
     if node.type=='BSDF_PRINCIPLED':node.inputs['Base Color'].default_value=(.285,.285,.285,1)
  bpy.context.view_layer.update()
  return original_vertices(collection)
 renderer._vertices_world=gray_vertices
renderer.main()
