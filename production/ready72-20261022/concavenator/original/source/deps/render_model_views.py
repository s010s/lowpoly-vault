# SPDX-License-Identifier: MIT
"""Pinned canonical exact-GLB renderer with the v2 four-view camera contract.
Use normal renderer arguments and optionally --clay-all.
"""
import sys, math, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.atan(1/math.sqrt(2))))
clay_all='--clay-all' in sys.argv
original_save=renderer.save_json
def save_with_adapter(path,value):
    if path.name=='render-config.json':
        value['adapter_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        value['clay_all']=clay_all
        value['adapter']='source/deps/render_model_views.py'
    return original_save(path,value)
renderer.save_json=save_with_adapter
if clay_all:
    sys.argv.remove('--clay-all')
    original_link=renderer.link_object
    def gray_link(obj,*args,**kwargs):
        result=original_link(obj,*args,**kwargs)
        for material in (obj.data.materials if obj.type=='MESH' else []):
            if not material.use_nodes: continue
            for node in material.node_tree.nodes:
                if node.type=='BSDF_PRINCIPLED': node.inputs['Base Color'].default_value=(.32,.32,.32,1)
        return result
    renderer.link_object=gray_link
renderer.main()
