# SPDX-License-Identifier: MIT
"""Render only a clean import of the delivered GLB, never the authoring scene."""
from pathlib import Path
import argparse, hashlib, json, math, sys, shutil
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene, link_object, make_material, _vertices_world, _bounds, _look_at, srgb_to_linear
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--glb',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args(argv)
out=args.output;out.mkdir(parents=True,exist_ok=True)
C=setup_scene('exact-export-evidence');root=bpy.data.objects[C['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(args.glb.resolve()))
imported=[o for o in bpy.data.objects if o not in before]
for ob in imported:link_object(ob,C,parent=False)
for ob in imported:
    if ob.parent not in imported:
        world=ob.matrix_world.copy();ob.parent=root;ob.matrix_world=world
points=_vertices_world(C);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;scene.world=world
bg=world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
camera_bg=world.node_tree.nodes.new('ShaderNodeBackground');camera_bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);camera_bg.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader')
world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(bg.outputs[0],mix.inputs[1]);world.node_tree.links.new(camera_bg.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],world.node_tree.nodes['World Output'].inputs['Surface'])
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
    ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
floor_mesh=bpy.data.meshes.new('studio-floor');e=span*20;z=lo[2]-.002
floor_mesh.from_pydata([(-e,-e,z),(e,-e,z),(e,e,z),(-e,e,z)],[],[(0,1,2,3)]);floor=bpy.data.objects.new('studio-floor',floor_mesh);scene.collection.objects.link(floor);floor_mesh.materials.append(make_material('studio-floor','#E8E4DC',roughness=1))
data=bpy.data.cameras.new('evidence-camera');cam=bpy.data.objects.new('evidence-camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO';data.clip_start=.001;data.clip_end=span*30
views={};directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
for name,d in directions.items():
    cam.location=center+Vector(d).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inverse=cam.matrix_world.inverted();proj=[inverse@v for v in points]
    width=max(v.x for v in proj)-min(v.x for v in proj);height=max(v.y for v in proj)-min(v.y for v in proj)
    shift=Vector(((max(v.x for v in proj)+min(v.x for v in proj))/2,(max(v.y for v in proj)+min(v.y for v in proj))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift;data.ortho_scale=max(width,height)*1.2
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    views[name]={'direction_blender':list(d),'orthographic_scale_m':data.ortho_scale,'sha256':hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest()}
report={'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','subject_glb_sha256':hashlib.sha256(args.glb.read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source':'clean import of exact model.glb','engine':'Cycles CPU','blender':bpy.app.version_string,'resolution':[640,640],'samples':32,'threads':2,'background_srgb':'#E8E4DC','view_transform':'Standard','look':'None','exposure':0,'gamma':1,'views':views,'scope':'Export evidence images only; not browser GPU or combined scene performance.'}
(out/'render-report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
