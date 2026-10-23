# SPDX-License-Identifier: MIT
"""Thin local adapter for pinned canonical exact-GLB renderer.
--gray applies neutral structural material. All views use the fixed reviewed framing
stored in render_framing.json; hero is prescribed (+X,-Y,+Z).
"""
import sys,math,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from bpy.app.handlers import persistent
import render_candidate_views as renderer
renderer.DIRECTIONS['hero']=(45,math.degrees(math.asin(1/math.sqrt(3))))
FRAMING=Path(__file__).with_name('render_framing.json')
frame=json.loads(FRAMING.read_text()) if FRAMING.is_file() else None
gray='--gray' in sys.argv
if gray:sys.argv.remove('--gray')
@persistent
def apply_presentation(scene,*_):
    if gray:bpy.context.view_layer.material_override=bpy.data.materials.get('_candidate_clay')
    if frame:
        cam=scene.camera
        direction=cam.rotation_euler.to_quaternion()@Vector((0,0,1))
        center=Vector(frame['target_blender_m']);radius=frame['radius']
        cam.location=center+direction*radius*6
        renderer._look_at(cam,center)
        cam.data.ortho_scale=frame['orthographic_scale']
        for light in frame['lights']:
            ob=bpy.data.objects['_candidate_'+light['name']]
            ob.location=center+Vector(light['direction'])*radius
            renderer._look_at(ob,center)
            ob.data.energy=light['energy'];ob.data.size=light['size']
bpy.app.handlers.render_pre.append(apply_presentation)
renderer.main()
# Canonical config is written before render_pre. Record actual fixed settings afterwards
# and renew manifest/config hashes without changing the already-rendered image bytes.
if frame:
    out=Path(sys.argv[sys.argv.index('--output-dir')+1])
    config_path=out/'render-config.json';conf=json.loads(config_path.read_text())
    conf['camera'].update(orthographic_scale=frame['orthographic_scale'],target_blender_m=frame['target_blender_m'])
    conf.update(orthographic_scale=frame['orthographic_scale'],target_blender_m=frame['target_blender_m'],lights=frame['lights'])
    conf['lighting']['lights']=frame['lights']
    conf['fixed_review_framing']={'baseline_glb_sha256':frame['source_glb_sha256'],'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'framing_sha256':hashlib.sha256(FRAMING.read_bytes()).hexdigest(),'note':'Actual render_pre camera and area-light settings; source_bounds_blender_m remains the current imported GLB bounds.'}
    conf['material_override']='uniform gray' if gray else None
    config_path.write_text(json.dumps(conf,indent=2,sort_keys=True)+'\n')
    digest=hashlib.sha256(config_path.read_bytes()).hexdigest()
    manifest_path=out/'render-manifest.json';m=json.loads(manifest_path.read_text());m['render_config']['sha256']=digest;m['config_sha256']=digest
    manifest_path.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    turn=out/'turntable.json';t=json.loads(turn.read_text());t['config_sha256']=digest;turn.write_text(json.dumps(t,indent=2,sort_keys=True)+'\n')
