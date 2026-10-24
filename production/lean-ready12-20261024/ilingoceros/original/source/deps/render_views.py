# SPDX-License-Identifier: MIT
"""Exact-GLB four-view evidence renderer. Uses copied canonical scene helpers."""
from pathlib import Path
import argparse, hashlib, json, math, sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene, link_object, make_material, _vertices_world, _bounds, _look_at

p=argparse.ArgumentParser();p.add_argument('--glb',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=64);p.add_argument('--clay',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=a.glb.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
collection=setup_scene('ilingoceros-view-evidence');before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(source))
imported=[o for o in bpy.data.objects if o not in before]
for o in imported:link_object(o,collection,parent=False)
points=_vertices_world(collection);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=not a.clay
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('EvidenceWorld');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.35;scene.world=world
if a.clay:
    bpy.context.view_layer.material_override=make_material('Clay','#A4A4A4',roughness=.88)
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.8,.8,.8,1)
for name,direction,energy,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-1,3),150,5)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj);obj.location=center+Vector(direction)*span/2;_look_at(obj,center)
cd=bpy.data.cameras.new('EvidenceCamera');camera=bpy.data.objects.new('EvidenceCamera',cd);scene.collection.objects.link(camera);scene.camera=camera
cd.type='ORTHO';cd.clip_start=.001;cd.clip_end=30
manifest={'source':'model.glb','glb_sha256':sha(source),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU',
 'render_script_sha256':sha(Path(__file__).resolve()),'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,
 'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'transparent':not a.clay,'clay_override':a.clay,
 'coordinate_convention':'Blender +Z up, -Y animal forward; cameras front -Y, side +X, top +Z, perspective (+X,-Y,+Z).',
 'lighting':[{'direction':[-3,-4,6],'energy':450*span*span/4,'size':4*span/2},{'direction':[4,-1,3],'energy':150*span*span/4,'size':5*span/2}],
 'clean_import':True,'views':[],'scope':'Exact-export image evidence only; no Three.js GPU claim.'}
for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
    camera.location=center+Vector(direction).normalized()*span*4;_look_at(camera,center);bpy.context.view_layer.update()
    projected=[camera.matrix_world.inverted()@v for v in points]
    x0,x1=min(v.x for v in projected),max(v.x for v in projected);y0,y1=min(v.y for v in projected),max(v.y for v in projected)
    camera.location+=camera.matrix_world.to_3x3()@Vector(((x0+x1)/2,(y0+y1)/2,0));cd.ortho_scale=max(x1-x0,y1-y0)*1.18
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    manifest['views'].append({'view':name,'path':name+'.png','sha256':sha(out/(name+'.png')),'direction':list(direction),
      'camera_position':list(camera.location),'camera_rotation_xyz':list(camera.rotation_euler),'orthographic_scale':cd.ortho_scale})
(out/'render-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('RENDER_COMPLETE',manifest['glb_sha256'])
