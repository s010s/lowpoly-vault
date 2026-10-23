# SPDX-License-Identifier: MIT
"""Exact-GLB four-view flight specimen rig, using canonical helper utilities."""
import bpy,json,math,hashlib,shutil
from pathlib import Path
from mathutils import Vector
from asset_common import _look_at,_vertices_world,_bounds,make_material,srgb_to_linear

def render(collection,out,glb_sha,gray=False,resolution=896,samples=32):
    out=Path(out);scene=bpy.context.scene;pts=_vertices_world(collection);low,high=_bounds(pts);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
    stage=bpy.data.collections.new('_PREVIEW_ONLY');scene.collection.children.link(stage)
    world=bpy.data.worlds.new('Neutral_Studio');world.use_nodes=True
    bg=world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    cam_bg=world.node_tree.nodes.new('ShaderNodeBackground');cam_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,)
    lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(bg.outputs[0],mix.inputs[1]);world.node_tree.links.new(cam_bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes.get('World Output').inputs[0]);scene.world=world
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=samples;scene.cycles.use_denoising=False;scene.cycles.use_adaptive_sampling=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=resolution;scene.render.resolution_y=resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2;ob=bpy.data.objects.new(name,data);stage.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
    camd=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camd);stage.objects.link(cam);scene.camera=cam;camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=100
    if gray: bpy.context.view_layer.material_override=make_material('_Gray','#96958E',roughness=.86)
    output=out/'gray' if gray else out/'views';output.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();projected=[inv@p for p in pts]
        lo=[min(p[i] for p in projected) for i in range(2)];hi=[max(p[i] for p in projected) for i in range(2)];shift=Vector(((lo[0]+hi[0])/2,(lo[1]+hi[1])/2,0));cam.location+=cam.matrix_world.to_3x3()@shift
        camd.ortho_scale=max(hi[i]-lo[i] for i in range(2))*1.16
        file=output/(name+'.png');scene.render.filepath=str(file);bpy.ops.render.render(write_still=True)
        manifest.append({'view':name,'file':str(file.relative_to(out)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'camera_direction_blender':direction,'camera_location_blender':list(cam.location),'ortho_scale_m':camd.ortho_scale,'resolution':[resolution,resolution]})
    if not gray:shutil.copyfile(output/'perspective.png',out/'preview.png')
    evidence={'source':'clean import of exact emitted model.glb','glb_sha256':glb_sha,'engine':'Cycles CPU','threads':2,'samples':samples,'gray_override':gray,'color':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'world_camera_background':'#E8E4DC'},'lights':'canonical helper key/fill, no floor for airborne specimen','views':manifest}
    path=out/'qa/evidence'/('gray-render.json' if gray else 'renders.json');path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(evidence,indent=2)+'\n')
