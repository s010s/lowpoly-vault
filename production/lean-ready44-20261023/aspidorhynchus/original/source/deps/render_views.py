# SPDX-License-Identifier: MIT
"""Four views from a clean import of the exact GLB; no source-scene substitution."""
import argparse,hashlib,json,math,sys,time
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,_vertices_world,_bounds,_look_at,make_material,srgb_to_linear
from qa_glb import audit_glb

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48);p.add_argument('--clay',action='store_true')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=False)
glb_hash=digest(a.glb);audit=audit_glb(a.glb,24000,6,16);assert not audit['errors']
col=setup_scene('exact-glb-view');root=bpy.data.objects[col['asset_root']];before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
imported=[o for o in bpy.data.objects if o not in before]
for o in imported:link_object(o,col,parent=False)
for o in imported:
 if o.parent not in imported:
  matrix=o.matrix_world.copy();o.parent=root;o.matrix_world=matrix
bpy.context.view_layer.update();points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);radius=max((pt-center).length for pt in points)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=a.samples;sc.cycles.use_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=2
sc.render.resolution_x=sc.render.resolution_y=a.resolution;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False
sc.view_settings.view_transform='Standard';sc.view_settings.look='None';sc.view_settings.exposure=0;sc.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral-world');world.use_nodes=True;nt=world.node_tree
nt.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);nt.nodes['Background'].inputs['Strength'].default_value=.3
bg=nt.nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(c/255) for c in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
lp=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(nt.nodes['Background'].outputs[0],mix.inputs[1]);nt.links.new(bg.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes['World Output'].inputs['Surface']);sc.world=world
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy*(2*radius)**2/4;data.shape='DISK';data.size=size*radius;o=bpy.data.objects.new(name,data);sc.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center);lights.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
camd=bpy.data.cameras.new('Evidence-camera');cam=bpy.data.objects.new('Evidence-camera',camd);sc.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.0001;camd.clip_end=20;sc.camera=cam
if a.clay:bpy.context.view_layer.material_override=make_material('Diagnostic-clay','#929292',roughness=.85)
config={'schema_version':1,'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'samples':a.samples,'resolution':[a.resolution,a.resolution],'threads':2,'denoising':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'lights':lights,'background':'#E8E4DC','clay':a.clay,'exact_import_glb_sha256':glb_hash,'renderer_sha256':digest(__file__),'asset_common_sha256':digest(Path(__file__).with_name('asset_common.py')),'views':{}}
frames={}
for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
 direction=Vector(direction).normalized();cam.location=center+direction*radius*6;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.rotation_euler.to_matrix().transposed();projected=[inv@(pt-center) for pt in points]
 extent=max(max(pt[k] for pt in projected)-min(pt[k] for pt in projected) for k in (0,1));camd.ortho_scale=extent*1.15
 config['views'][name]={'direction_blender':list(direction),'target_blender_m':list(center),'orthographic_scale_m':camd.ortho_scale,'purpose':{'front':'Lateral complete fish and jaw inequality','side':'Head-on inferred body thickness','top':'Dorsal planform','perspective':'Whole fish oblique'}[name]}
 sc.render.filepath=str(a.output/(name+'.png'));started=time.monotonic();bpy.ops.render.render(write_still=True);frames[name]={'sha256':digest(a.output/(name+'.png')),'render_seconds':time.monotonic()-started}
assert digest(a.glb)==glb_hash
(a.output/'render-config.json').write_text(json.dumps(config,indent=2)+'\n');(a.output/'render-receipt.json').write_text(json.dumps({'glb_sha256':glb_hash,'render_config_sha256':digest(a.output/'render-config.json'),'views':frames,'scope':'Actual GLB import rendered in Blender; not GPU browser, independent visual review or publication approval'},indent=2)+'\n')
