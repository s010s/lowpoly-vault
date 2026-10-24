# SPDX-License-Identifier: MIT
"""Exact-export four-view evidence. Canonical helper lighting, public paths only.
Derived lighting convention: Leon Made This / s010s, asset_common.py (MIT).
"""
from pathlib import Path
import sys,json,hashlib,math,argparse,time
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,j):Path(p).write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
av=sys.argv[sys.argv.index('--')+1:];p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=48);a=p.parse_args(av)
r=a.root.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
c=setup_scene('exact-export-review');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(r/'model.glb'));new=set(bpy.data.objects)-before
for o in new:link_object(o,c,parent=False)
root=bpy.data.objects[c['asset_root']]
for o in new:
    if o.parent not in new:
        w=o.matrix_world.copy();o.parent=root;o.matrix_world=w
bpy.context.view_layer.update();pts=_vertices_world(c);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2
s.render.resolution_x=s.render.resolution_y=a.resolution;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=False
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
w=bpy.data.worlds.new('evidence-world');w.use_nodes=True;bg=w.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
bg2=w.node_tree.nodes.new('ShaderNodeBackground');bg2.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg2.inputs['Strength'].default_value=1
lightpath=w.node_tree.nodes.new('ShaderNodeLightPath');mix=w.node_tree.nodes.new('ShaderNodeMixShader');w.node_tree.links.new(lightpath.outputs['Is Camera Ray'],mix.inputs[0]);w.node_tree.links.new(bg.outputs[0],mix.inputs[1]);w.node_tree.links.new(bg2.outputs[0],mix.inputs[2]);w.node_tree.links.new(mix.outputs[0],w.node_tree.nodes['World Output'].inputs['Surface']);s.world=w
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center);lights.append({'name':name,'direction':direction,'energy':d.energy,'size':d.size})
camd=bpy.data.cameras.new('evidence-camera');cam=bpy.data.objects.new('evidence-camera',camd);s.collection.objects.link(cam);s.camera=cam;camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=span*30
if a.gray:bpy.context.view_layer.material_override=make_material('gray-check','#929292',.85)
directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
config={'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'render_script_sha256':sha(__file__),'helper_sha256':sha(Path(__file__).with_name('asset_common.py')),'resolution':[a.resolution,a.resolution],'samples':a.samples,'threads':2,'gray_override':a.gray,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background_srgb':'#E8E4DC','lights':lights,'views':{},'framing':'Orthographic per-view fit at 1.18 padding; fixed asset pose, no per-view deformation.','website_image_contract':False}
frames=[]
for label,direction in directions.items():
    cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();pr=[inv@pt for pt in pts]
    width=max(v.x for v in pr)-min(v.x for v in pr);height=max(v.y for v in pr)-min(v.y for v in pr)
    shift=Vector(((max(v.x for v in pr)+min(v.x for v in pr))/2,(max(v.y for v in pr)+min(v.y for v in pr))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift;camd.ortho_scale=max(width,height)*1.18
    config['views'][label]={'camera_direction_blender':direction,'position_blender_m':list(cam.location),'rotation_euler_radians':list(cam.rotation_euler),'orthographic_scale':camd.ortho_scale}
    s.render.filepath=str(out/(label+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True)
    frames.append({'path':('private/gray/' if a.gray else 'views/')+label+'.png','sha256':sha(out/(label+'.png')),'view':label,'wall_seconds':round(time.monotonic()-start,4)})
write(out/'render-config.json',config)
write(out/'render-manifest.json',{'status':'RENDERED_NOT_INDEPENDENTLY_ACCEPTED','input':'model.glb','source_glb_sha256':sha(r/'model.glb'),'brief_sha256':sha(r/'brief.json'),'references_sha256':sha(r/'references.json'),'renderer_config_sha256':sha(out/'render-config.json'),'input_origin':'Clean import of the actual exported GLB into a factory-reset scene.','frames':frames,'gpu':'UNKNOWN','scene':'UNKNOWN'})
print('RENDERED',sha(r/'model.glb'))
