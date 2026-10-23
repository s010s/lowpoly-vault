# SPDX-License-Identifier: MIT
"""Exact-GLB neutral studio four-view rendering. Not a browser/GPU test."""
import hashlib,json,shutil
from pathlib import Path
import bpy
from mathutils import Vector
import asset_common as ac

def render_glb(out,gray=False):
    out=Path(out);glb=out/'model.glb';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb))
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8 if gray else 64;scene.cycles.use_denoising=False
    scene.render.resolution_x=256 if gray else 512;scene.render.resolution_y=scene.render.resolution_x;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    bpy.context.view_layer.update()
    pts=[o.matrix_world@v.co for o in scene.objects if o.type=='MESH' for v in o.data.vertices]
    lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(lo+hi)/2;span=max(hi-lo)
    world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True;scene.world=world
    nodes=world.node_tree.nodes;links=world.node_tree.links
    nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);nodes['Background'].inputs['Strength'].default_value=.35
    bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(ac.srgb_to_linear(c/255) for c in [232,228,220])+(1,);bg.inputs['Strength'].default_value=1
    lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(nodes['Background'].outputs[0],mix.inputs[1]);links.new(bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs[0])
    def point(o,t):o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
    lighting=[('key',[-3,-4,6],450,4),('fill',[4,-1,3],180,5),('rim',[-1,4,4],130,3)]
    for name,direction,power,size in lighting:
        d=bpy.data.lights.new(name,'AREA');d.energy=power*span*span/4;d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;point(o,center)
    extent=span*20;mesh=bpy.data.meshes.new('Studio floor');mesh.from_pydata([(-extent,-extent,-.002),(extent,-extent,-.002),(extent,extent,-.002),(-extent,extent,-.002)],[],[(0,1,2,3)]);floor=bpy.data.objects.new('Studio floor',mesh);scene.collection.objects.link(floor);mesh.materials.append(ac.make_material('Studio floor','#E8E4DC',1))
    if gray:scene.view_layers[0].material_override=ac.make_material('Diagnostic gray','#939393',.9)
    d=bpy.data.cameras.new('Canonical camera');cam=bpy.data.objects.new('Canonical camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=100
    dest=out/'private/gray' if gray else out/'views';dest.mkdir(parents=True,exist_ok=True)
    evidence={'glb_sha256':sha(glb),'renderer_sha256':sha(Path(__file__)),'source':'Clean import of exact model.glb, not source scene','blender':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'samples':scene.cycles.samples,'resolution':[scene.render.resolution_x,scene.render.resolution_y],'gray':gray,'background':'#E8E4DC neutral studio','lighting':lighting,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'views':{}}
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4;point(cam,center);bpy.context.view_layer.update();ps=[cam.matrix_world.inverted()@p for p in pts]
        x0=min(p.x for p in ps);x1=max(p.x for p in ps);y0=min(p.y for p in ps);y1=max(p.y for p in ps)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((x0+x1)/2,(y0+y1)/2,0));d.ortho_scale=max(x1-x0,y1-y0)*1.18
        target=dest/(name+'.png');scene.render.filepath=str(target);bpy.ops.render.render(write_still=True)
        evidence['views'][name]={'camera_direction':list(direction),'camera_location':list(cam.location),'ortho_scale':d.ortho_scale,'sha256':sha(target)}
    if not gray:shutil.copyfile(dest/'perspective.png',out/'preview.png')
    p=out/'private/gray/evidence.json' if gray else out/'qa/evidence/exact-glb-views.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(evidence,indent=2)+'\n')
