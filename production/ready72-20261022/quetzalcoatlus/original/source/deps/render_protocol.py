#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Thin task-specific adapter around the pinned canonical exact-GLB renderer.
Adds the frozen (+X,-Y,+Z) perspective and a temporary gray-mode source copy.
Gray-mode GLB is private diagnostic-only; final images load the final GLB.
"""
import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import render_candidate_views as R
R.DIRECTIONS['perspective']=(45,math.degrees(math.asin(1/math.sqrt(3))))
if '--gray' in sys.argv:
 sys.argv.remove('--gray')
 # Canonical frame mode determines override by semantic view, so map four
 # temporary diagnostic IDs to clay while retaining the actual camera angles.
 R.DIRECTIONS.update({'clay-front':(0,0),'clay-side':(90,0),'clay-top':(0,90),'clay-perspective':R.DIRECTIONS['perspective']})
 # Instead use a fresh separate gray GLB. This never changes the delivered GLB.
 import bpy
 idx=sys.argv.index('--')+1;src=Path(sys.argv[idx]);out=src.parent/'gray-diagnostic.glb'
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(src))
 from asset_common import make_material
 gray=make_material('diagnostic-gray','#929292')
 for obj in bpy.data.objects:
  if obj.type=='MESH':
   obj.data.materials.clear();obj.data.materials.append(gray)
   for face in obj.data.polygons:face.material_index=0
 bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_animations=False,export_cameras=False,export_lights=False)
 sys.argv[idx]=str(out)
R.main()
