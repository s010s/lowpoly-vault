# SPDX-License-Identifier: MIT
"""Exact-delivery GLB camera evidence, scale-aware for millimeter-size arthropods."""
import argparse, hashlib, json, sys, math
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene, link_object, make_material, srgb_to_linear, _vertices_world, _bounds, _look_at
ap=argparse.ArgumentParser(); ap.add_argument('glb',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--gray',action='store_true');ap.add_argument('--views',default='');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);args.out.mkdir(parents=True,exist_ok=True)
C=setup_scene('euproops-render'); before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=str(args.glb.resolve()))
for o in set(bpy.data.objects)-before: link_object(o,C,parent=False)
points=_vertices_world(C);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8 if args.gray else 40;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=384 if args.gray else 800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral_studio');world.use_nodes=True;scene.world=world;nodes=world.node_tree.nodes; bg=nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
cb=nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');world.node_tree.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);world.node_tree.links.new(bg.outputs[0],mix.inputs[1]);world.node_tree.links.new(cb.outputs[0],mix.inputs[2]);world.node_tree.links.new(mix.outputs[0],nodes['World Output'].inputs['Surface'])
camdata=bpy.data.cameras.new('evidence_camera');cam=bpy.data.objects.new('evidence_camera',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.type='ORTHO';camdata.clip_start=span/1000;camdata.clip_end=span*30
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5),('rim',(1,4,4),160,3)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);lights.append((o,direction))
if args.gray: bpy.context.view_layer.material_override=make_material('gray_diagnostic','#929292',roughness=.85)
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1),'ventral':(0,0,-1)}
if args.gray: views={k:views[k] for k in ['front','top','perspective','ventral']}
if args.views: views={k:views[k] for k in args.views.split(',')}
records={}
for name,direction in views.items():
 v=Vector(direction).normalized();cam.location=center+v*span*4;_look_at(cam,center);bpy.context.view_layer.update();rot=cam.rotation_euler.to_matrix();right=rot@Vector((1,0,0));up=rot@Vector((0,1,0));w=max(p.dot(right) for p in points)-min(p.dot(right) for p in points);h=max(p.dot(up) for p in points)-min(p.dot(up) for p in points);camdata.ortho_scale=max(w,h)*1.18
 target=center+right*((max(p.dot(right) for p in points)+min(p.dot(right) for p in points))/2-center.dot(right))+up*((max(p.dot(up) for p in points)+min(p.dot(up) for p in points))/2-center.dot(up));cam.location=target+v*span*4;_look_at(cam,target)
 for light,d in lights:
  xyz=Vector(d);xyz.z*=(-1 if name=='ventral' else 1);light.location=center+xyz*span/2;_look_at(light,center)
 path=args.out/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
 records[name]={'path':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'camera_direction_blender':direction,'camera_location_m':list(cam.location),'target_m':list(target),'orthographic_scale_m':camdata.ortho_scale,'lighting_hemisphere':'ventral mirrored Z' if name=='ventral' else 'dorsal standard'}
report={'status':'rendered_not_independently_reviewed','source':'fresh import of exact delivered GLB, never source scene','glb_sha256':hashlib.sha256(args.glb.read_bytes()).hexdigest(),'blender':bpy.app.version_string,'engine':'Cycles CPU','samples':scene.cycles.samples,'resolution':[scene.render.resolution_x,scene.render.resolution_y],'material_override':'gray' if args.gray else None,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background_srgb':'#E8E4DC','floor':'none; ventral line of sight unobstructed','views':records}
(args.out/'render-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
