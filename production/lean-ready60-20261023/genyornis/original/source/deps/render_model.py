# SPDX-License-Identifier: MIT
"""Render canonical views from a clean import of the exact exported GLB.
Uses the pinned project's material, scene, bound and camera helpers.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys, time
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--clay',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); a.output.mkdir(parents=True,exist_ok=True)
digest=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest()
glb_hash=digest(a.glb); collection=setup_scene('render-genyornis');before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
for o in set(bpy.data.objects)-before:link_object(o,collection,parent=False)
pts=_vertices_world(collection);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=False;scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('studio');world.use_nodes=True;scene.world=world
nodes=world.node_tree.nodes;links=world.node_tree.links;bg=nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
cb=nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(bg.outputs[0],mix.inputs[1]);links.new(cb.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface'])
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
    ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
floormesh=bpy.data.meshes.new('stage');extent=span*20;z=lo[2]-.002
floormesh.from_pydata([(-extent,-extent,z),(extent,-extent,z),(extent,extent,z),(-extent,extent,z)],[],[(0,1,2,3)]);floor=bpy.data.objects.new('stage',floormesh);scene.collection.objects.link(floor);floormesh.materials.append(make_material('stage','#E8E4DC',roughness=1))
if a.clay:
    clay=make_material('clay','#94918B',roughness=.88)
    for ob in collection.all_objects:
        if ob.type=='MESH':
            ob.data.materials.clear();ob.data.materials.append(clay)
            for poly in ob.data.polygons:poly.material_index=0
camdata=bpy.data.cameras.new('camera');camera=bpy.data.objects.new('camera',camdata);scene.collection.objects.link(camera);scene.camera=camera;camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=span*40
# All views use a fixed 2.38 m orthographic span, same center and scale.
camdata.ortho_scale=span*1.20
frames=[]
for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
    camera.location=center+Vector(direction).normalized()*span*5;_look_at(camera,center)
    path=a.output/(name+'.png');scene.render.filepath=str(path);start=time.monotonic();bpy.ops.render.render(write_still=True)
    frames.append({'path':name+'.png','sha256':digest(path),'camera_direction_blender':list(direction),'camera_location_blender':list(camera.location),'width':a.resolution,'height':a.resolution,'wall_seconds':round(time.monotonic()-start,3)})
assert digest(a.glb)==glb_hash
report={'source_glb_sha256':glb_hash,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'import':'factory state, exact GLB, no source blend used',
 'clay':a.clay,'samples':a.samples,'resolution':a.resolution,'color_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},
 'camera':{'type':'ORTHO','scale':camdata.ortho_scale,'target':list(center),'fixed_framing':True},'lights':'Project neutral key (-3,-4,6) / fill (4,-1,3), warm #E8E4DC stage',
 'source_unchanged':True,'render_script_sha256':digest(__file__),'frames':frames,'visual_review':'pending, renders alone do not constitute acceptance','threejs_gpu':'not_run'}
(a.output/'render-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'rendered':len(frames),'clay':a.clay,'glb_sha256':glb_hash}))
