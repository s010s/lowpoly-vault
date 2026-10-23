# SPDX-License-Identifier: MIT
"""Clean-import, exact-GLB CPU reference renderer with real micro-scale cameras."""
from pathlib import Path
import hashlib,json,math
import bpy
from mathutils import Vector
from asset_common import make_material

def render_exact_glb(glb, output, gray=False):
    glb=Path(glb);out=Path(output);sha=hashlib.sha256(glb.read_bytes()).hexdigest()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    scene=bpy.context.scene
    objs=[o for o in scene.objects if o.type=='MESH']
    bpy.context.view_layer.update()
    points=[o.matrix_world@v.co for o in objs for v in o.data.vertices]
    lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)])
    center=(lo+hi)/2;span=max(hi-lo)
    world=bpy.data.worlds.new('Reference-studio');world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.72,.74,.77,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;scene.world=world
    for name,vec,energy,size in [('key',(-3,-4,6),500,4),('fill',(4,-2,2),260,3),('rim',(1,4,5),420,3)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span;data.shape='DISK';data.size=size*span
        o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(vec)*span
        o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
    cd=bpy.data.cameras.new('Reference-camera');camera=bpy.data.objects.new('Reference-camera',cd);scene.collection.objects.link(camera)
    cd.type='ORTHO';cd.clip_start=span*.0001;cd.clip_end=span*100;scene.camera=camera
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8 if gray else 64
    scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=384 if gray else 768
    scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=not gray
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    if gray:scene.view_layers[0].material_override=make_material('Inspection-clay','#A8AAA8',.92)
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    target=out/('private/gray' if gray else 'views');target.mkdir(parents=True,exist_ok=True)
    frames=[]
    for name,direction in views.items():
        vec=Vector(direction).normalized();camera.location=center+vec*span*5
        camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
        inv=camera.matrix_world.inverted();ps=[inv@p for p in points];xs=[p.x for p in ps];ys=[p.y for p in ps]
        offset=Vector(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,0));camera.location+=camera.matrix_world.to_3x3()@offset
        cd.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*1.18
        scene.render.filepath=str(target/(name+'.png'));bpy.ops.render.render(write_still=True)
        frames.append({'path':('private/gray/' if gray else 'views/')+name+'.png','sha256':hashlib.sha256((target/(name+'.png')).read_bytes()).hexdigest(),'direction_blender':direction,'camera_location_m':list(camera.location),'ortho_scale_m':cd.ortho_scale})
    rec={'glb_sha256':sha,'rendered_from':'clean import of delivered model.glb','blender':bpy.app.version_string,'engine':'Cycles CPU','samples':scene.cycles.samples,'threads':2,'resolution':scene.render.resolution_x,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'transparent':not gray,'geometry_scale_applied':1,'frames':frames,'scope':'Reference CPU renders, not target GPU or populated scene acceptance.'}
    dest=out/('private/gray/receipt.json' if gray else 'qa/evidence/views.json');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(rec,indent=2)+'\n')
    if not gray:(out/'preview.png').write_bytes((target/'perspective.png').read_bytes())
