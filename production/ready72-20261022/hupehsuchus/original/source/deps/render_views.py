# SPDX-License-Identifier: MIT
"""Exact-GLB rendering adapter. Canonical helpers supply sRGB conversion/materials.
Draft is a three-view 384px clay check. Final is four 768px views with perspective
reused byte-for-byte as preview.png. Import the GLB fresh, never the source blend.
"""
from pathlib import Path
import sys,json,math,hashlib,argparse,shutil
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import make_material, srgb_to_linear, _look_at
p=argparse.ArgumentParser(); p.add_argument('--root',required=True); p.add_argument('--draft',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); R=Path(a.root).resolve()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
glbhash=sha(R/'model.glb')
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(R/'model.glb'),import_pack_images=True)
models=[o for o in bpy.context.scene.objects if o.type=='MESH']
points=[o.matrix_world@v.co for o in models for v in o.data.vertices]
lo=Vector([min(p[k] for p in points) for k in range(3)]); hi=Vector([max(p[k] for p in points) for k in range(3)])
center=(lo+hi)/2; span=max(hi-lo)
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=12 if a.draft else 48; scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED'; scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=384 if a.draft else 768
scene.render.resolution_percentage=100; scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.render.film_transparent=False
scene.view_settings.view_transform='Standard'; scene.view_settings.look='None'; scene.view_settings.exposure=0; scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral_studio'); world.use_nodes=True; scene.world=world
nodes=world.node_tree.nodes; bg=nodes.get('Background'); bg.inputs['Color'].default_value=(.75,.75,.75,1); bg.inputs['Strength'].default_value=.3
camera_bg=nodes.new('ShaderNodeBackground'); camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,); camera_bg.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath'); mix=nodes.new('ShaderNodeMixShader'); world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]); world.node_tree.links.new(bg.outputs[0],mix.inputs[1]); world.node_tree.links.new(camera_bg.outputs[0],mix.inputs[2]); world.node_tree.links.new(mix.outputs[0],nodes.get('World Output').inputs['Surface'])
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    d=bpy.data.lights.new(name,'AREA'); d.energy=energy*span*span/4; d.shape='DISK'; d.size=size*span/2; o=bpy.data.objects.new(name,d); scene.collection.objects.link(o); o.location=center+Vector(direction)*span/2; _look_at(o,center)
camdata=bpy.data.cameras.new('Exact_GLB_camera'); cam=bpy.data.objects.new('Exact_GLB_camera',camdata); scene.collection.objects.link(cam); scene.camera=cam; camdata.type='ORTHO'; camdata.clip_start=.001; camdata.clip_end=30
if a.draft: bpy.context.view_layer.material_override=make_material('Gray_diagnostic','#929292',roughness=.85)
directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
labels=['side','top','perspective'] if a.draft else list(directions)
out=R/'private/gray' if a.draft else R/'views'; out.mkdir(exist_ok=True,parents=True)
report={'status':'RENDERED_NOT_VISUALLY_REVIEWED','glb_sha256':glbhash,'import_source':'model.glb','source_blend_used':False,'blender':bpy.app.version_string,'engine':'Cycles CPU','samples':scene.cycles.samples,'resolution':[scene.render.resolution_x,scene.render.resolution_y],'colorspace':'Standard / None / exposure 0 / gamma 1','background':'#E8E4DC','lights':'Canonical key (-3,-4,6), 450*span²/4; fill (4,-1,3),150*span²/4; world strength .3','floor':'None, suspended swimmer','view_coordinates':'Authoring Blender axes restored by glTF importer','views':{}}
for label in labels:
    direction=Vector(directions[label]).normalized(); cam.location=center+direction*span*4; _look_at(cam,center); bpy.context.view_layer.update()
    projected=[cam.matrix_world.inverted()@p for p in points]
    xmin,xmax=min(p.x for p in projected),max(p.x for p in projected); ymin,ymax=min(p.y for p in projected),max(p.y for p in projected)
    cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0)); camdata.ortho_scale=max(xmax-xmin,ymax-ymin)*1.22
    path=out/(label+'.png'); scene.render.filepath=str(path); bpy.ops.render.render(write_still=True)
    report['views'][label]={'path':str(path.relative_to(R)),'sha256':sha(path),'camera_direction':directions[label],'camera_location_m':list(cam.location),'orthographic_scale_m':camdata.ortho_scale}
if not a.draft:
    shutil.copyfile(out/'perspective.png',R/'preview.png'); report['preview_sha256']=sha(R/'preview.png'); report['preview_is_perspective_copy']=True
    path=R/'qa/evidence/render.json'
else: path=R/'private/gray/render.json'
path.write_text(json.dumps(report,indent=2)+'\n')
assert sha(R/'model.glb')==glbhash
print('RENDER_COMPLETE',str(path))
