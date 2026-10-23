# SPDX-License-Identifier: MIT
"""Clean-import exact GLB four-view evidence using canonical studio recipe."""
import bpy,sys,math,json,hashlib,argparse
from pathlib import Path
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import make_material,srgb_to_linear,_look_at
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--gray',action='store_true');p.add_argument('--resolution',type=int,default=800);p.add_argument('--samples',type=int,default=32);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);r=Path(a.root)
glb=r/'model.glb';sha=hashlib.sha256(glb.read_bytes()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb))
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
meshes=[o for o in scene.objects if o.type=='MESH'];points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
lo=Vector([min(v[k] for v in points) for k in range(3)]);hi=Vector([max(v[k] for v in points) for k in range(3)]);center=(lo+hi)/2;span=max(hi-lo)
if a.gray:
    clay=make_material('_clay','#A5A5A5',roughness=.95)
    for o in meshes:
        o.data.materials.clear();o.data.materials.append(clay)
        for poly in o.data.polygons:poly.material_index=0
world=bpy.data.worlds.new('neutral-preview');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
bg=world.node_tree.nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
lp=world.node_tree.nodes.new('ShaderNodeLightPath');mix=world.node_tree.nodes.new('ShaderNodeMixShader');nodes=world.node_tree.nodes;links=world.node_tree.links;links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);links.new(nodes['Background'].outputs[0],mix.inputs[1]);links.new(bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface']);scene.world=world
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
# Neutral stage is preview-only and never written back to model.blend or GLB.
f=bpy.data.meshes.new('floor');ext=span*20;f.from_pydata([(-ext,-ext,lo.z-.0005),(ext,-ext,lo.z-.0005),(ext,ext,lo.z-.0005),(-ext,ext,lo.z-.0005)],[],[(0,1,2,3)]);o=bpy.data.objects.new('floor',f);scene.collection.objects.link(o);f.materials.append(make_material('neutral-floor','#E8E4DC',roughness=1))
cam=bpy.data.cameras.new('camera');co=bpy.data.objects.new('camera',cam);scene.collection.objects.link(co);scene.camera=co;cam.type='ORTHO';cam.ortho_scale=span*1.23;cam.clip_start=.0001;cam.clip_end=10
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False;scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
out=r/'private/gray' if a.gray else r/'views';out.mkdir(parents=True,exist_ok=True)
views={};dirs={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
for name,direction in dirs.items():
    co.location=center+Vector(direction).normalized()*span*4;_look_at(co,center);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
    views[name]={'path':str((out/(name+'.png')).relative_to(r)),'sha256':hashlib.sha256((out/(name+'.png')).read_bytes()).hexdigest(),'direction':direction,'camera':list(co.location),'target':list(center),'ortho_scale':cam.ortho_scale}
receipt={'glb_sha256':sha,'source':'clean import of exact model.glb; source scene not used','blender':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'resolution':[a.resolution,a.resolution],'samples':a.samples,'gray_override':a.gray,'background_srgb':'#E8E4DC','view_transform':'Standard','look':'None','exposure':0,'gamma':1,'views':views}
target=r/'private/gray/evidence.json' if a.gray else r/'qa/evidence/views.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(receipt,indent=2)+'\n')
if not a.gray:
    import shutil
    shutil.copy2(r/'views/perspective.png',r/'preview.png')
print('RENDERED_EXACT_GLB',sha)
