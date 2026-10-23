# SPDX-License-Identifier: MIT
"""Four canonical exact-GLB views. Self-contained with asset_common and qa_glb."""
import bpy,sys,math,json,hashlib,argparse
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_look_at,_vertices_world,_bounds
from qa_glb import audit_glb
p=argparse.ArgumentParser();p.add_argument('glb',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--views',default='front,side,top,perspective');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=64);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_sha=sha(a.glb);audit=audit_glb(a.glb,16000,4,32);assert not audit['errors']
coll=setup_scene('gogonasus-preview');root=bpy.data.objects[coll['asset_root']]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb));objs=[o for o in bpy.data.objects if o not in before]
for o in objs:link_object(o,coll,parent=False)
for o in objs:
    if o.parent not in objs:
        w=o.matrix_world.copy();o.parent=root;o.matrix_world=w
points=_vertices_world(coll);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);r=max((p-center).length for p in points)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True;nodes=world.node_tree.nodes;links=world.node_tree.links
nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);nodes['Background'].inputs['Strength'].default_value=.3
bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
lp=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(nodes['Background'].outputs[0],mix.inputs[1]);links.new(bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface']);scene.world=world
lights=[]
for name,direction,energy,size in [('Key',(-3,-4,6),450,4),('Fill',(4,-1,3),150,5)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=energy*(2*r)**2/4;d.shape='DISK';d.size=size*r;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*r;_look_at(o,center);lights.append({'name':name,'direction':direction,'energy':d.energy,'size':d.size})
cd=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',cd);scene.collection.objects.link(cam);cd.type='ORTHO';cd.clip_start=.0001;cd.clip_end=r*40;scene.camera=cam
if a.gray:scene.view_layers[0].material_override=make_material('Gray diagnostic','#929292',roughness=.9)
frames=[]
for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
    if name not in a.views.split(','):continue
    cam.location=center+Vector(direction).normalized()*r*6;_look_at(cam,center);cd.ortho_scale=2*r*1.08
    scene.render.filepath=str(a.out/(name+'.png'));bpy.ops.render.render(write_still=True)
    frames.append({'path':name+'.png','sha256':sha(a.out/(name+'.png')),'direction_blender':direction,'camera_target_blender_m':list(center),'orthographic_scale':cd.ortho_scale,'camera_location_blender_m':list(cam.location)})
assert sha(a.glb)==source_sha
report={'asset_id':'gogonasus','revision':'r001','source_glb_sha256':source_sha,'source_unchanged':True,'origin':'Clean import of delivered GLB, not source-scene rendering','renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'threads':2,'resolution':a.resolution,'samples':a.samples,'denoising':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background_srgb':'#E8E4DC','lights':lights,'gray':a.gray,'frames':frames,'render_script_sha256':sha(Path(__file__)),'status':'Rendered, pending visual inspection; no GPU/runtime implication'}
(a.out/'render-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('GOGONASUS_VIEWS',source_sha)
