# SPDX-License-Identifier: MIT
"""Render the delivered GLB only; canonical axes, CPU Cycles, no GPU assertion."""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb
ap=argparse.ArgumentParser();ap.add_argument('glb',type=Path);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--resolution',type=int,default=512);ap.add_argument('--samples',type=int,default=40);ap.add_argument('--clay',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
OUT=a.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
if any(OUT.iterdir()):raise ValueError('Use empty output directory to preserve earlier evidence')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=audit_glb(a.glb,16000,6,48)
if report['errors']:raise ValueError(report['errors'])
col=setup_scene('astrapotherium-render');root=bpy.data.objects[col['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()));imported=[o for o in bpy.data.objects if o not in before]
for ob in imported:link_object(ob,col,parent=False)
for ob in imported:
    if ob.parent not in imported:
        mat=ob.matrix_world.copy();ob.parent=root;ob.matrix_world=mat
points=_vertices_world(col);low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral_illuminating_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
    ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center);lights.append({'name':name,'direction':list(direction),'energy':data.energy,'size':data.size})
camdata=bpy.data.cameras.new('Orthographic_inspection_camera');camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=span*30
cam=bpy.data.objects.new('Inspection_camera',camdata);scene.collection.objects.link(cam);scene.camera=cam
if a.clay:bpy.context.view_layer.material_override=make_material('Clay','#929292',roughness=.85)
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
result={'asset_id':'astrapotherium','glb_sha256':sha(a.glb),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','render_helper_sha256':sha(Path(__file__)),'resolution':[a.resolution,a.resolution],'samples':a.samples,'transparent':True,'clay':a.clay,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'lights':lights,'glb_imported':True,'gpu':'UNKNOWN','views':{}}
for name,direction in views.items():
    cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points]
    width=max(p.x for p in proj)-min(p.x for p in proj);height=max(p.y for p in proj)-min(p.y for p in proj)
    shift=Vector(((max(p.x for p in proj)+min(p.x for p in proj))/2,(max(p.y for p in proj)+min(p.y for p in proj))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift
    camdata.ortho_scale=max(width,height)*1.16;scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
    result['views'][name]={'file':name+'.png','sha256':sha(OUT/(name+'.png')),'camera_direction':list(direction),'camera_location':list(cam.location),'orthographic_scale':camdata.ortho_scale,'transparent':True}
(OUT/'views-report.json').write_text(json.dumps(result,indent=2)+'\n')
print('EXACT_GLB_VIEWS_COMPLETE',sha(a.glb))
