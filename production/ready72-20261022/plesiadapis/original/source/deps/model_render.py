# SPDX-License-Identifier: MIT
"""Task-local exact-GLB four-view renderer. Cycles CPU, no source scene dependency."""
import hashlib,json,shutil
from pathlib import Path
import bpy
from mathutils import Vector
import asset_common as ac

def render_glb(out,gray=False):
    out=Path(out);glb=out/'model.glb';digest=hashlib.sha256(glb.read_bytes()).hexdigest()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb))
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=12 if gray else 40;scene.cycles.use_denoising=False
    scene.render.resolution_x=512 if gray else 1024;scene.render.resolution_y=scene.render.resolution_x;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    pts=[o.matrix_world@v.co for o in scene.objects if o.type=='MESH' for v in o.data.vertices]
    lo=Vector([min(v[i] for v in pts) for i in range(3)]);hi=Vector([max(v[i] for v in pts) for i in range(3)])
    center=(lo+hi)/2;span=max(hi-lo)
    world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True;scene.world=world
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35
    bg=world.node_tree.nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(ac.srgb_to_linear(c/255) for c in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
    path=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader')
    world.node_tree.links.new(path.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(world.node_tree.nodes['Background'].outputs[0],mix.inputs[1]);world.node_tree.links.new(bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs[0])
    def point(o,t):o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
    for name,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5),('rim',(-1,4,4),130,3)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=power*span*span/4;d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;point(o,center)
    mesh=bpy.data.meshes.new('Stage outside asset');extent=span*20
    mesh.from_pydata([(-extent,-extent,-.002),(extent,-extent,-.002),(extent,extent,-.002),(-extent,extent,-.002)],[],[(0,1,2,3)])
    floor=bpy.data.objects.new('Stage outside asset',mesh);scene.collection.objects.link(floor);mesh.materials.append(ac.make_material('Stage', '#E8E4DC',1))
    if gray:scene.view_layers[0].material_override=ac.make_material('Gray diagnostic','#939393',.9)
    data=bpy.data.cameras.new('Diagnostic camera');cam=bpy.data.objects.new('Diagnostic camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO';data.clip_start=.001;data.clip_end=100
    dest=out/'private/gray' if gray else out/'views';dest.mkdir(parents=True,exist_ok=True)
    evidence={'glb_sha256':digest,'source':'clean import of the exact model.glb, not source-scene render','blender':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'samples':scene.cycles.samples,'resolution':[scene.render.resolution_x,scene.render.resolution_y],'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'views':{},'gray':gray}
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4;point(cam,center);bpy.context.view_layer.update()
        inv=cam.matrix_world.inverted();ps=[inv@p for p in pts]
        x0=min(p.x for p in ps);x1=max(p.x for p in ps);y0=min(p.y for p in ps);y1=max(p.y for p in ps)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((x0+x1)/2,(y0+y1)/2,0));data.ortho_scale=max(x1-x0,y1-y0)*1.18
        target=dest/(name+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True)
        evidence['views'][name]={'camera_direction':list(direction),'camera_location':list(cam.location),'ortho_scale':data.ortho_scale,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
    if not gray:shutil.copyfile(dest/'perspective.png',out/'preview.png')
    target=out/'private/gray/evidence.json' if gray else out/'qa/evidence/exact-glb-views.json'
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(evidence,indent=2)+'\n')
