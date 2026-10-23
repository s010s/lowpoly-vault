# SPDX-License-Identifier: MIT
"""Task-local four-view exact-GLB renderer. Independent of the editable scene."""
import hashlib,json,shutil
from pathlib import Path
import bpy
from mathutils import Vector
import asset_common as ac

def render_glb(out,gray=False):
 out=Path(out);glb=out/'model.glb';sha=hashlib.sha256(glb.read_bytes()).hexdigest()
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb));scene=bpy.context.scene
 scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=10 if gray else 40;scene.cycles.use_denoising=False
 scene.render.resolution_x=512 if gray else 1024;scene.render.resolution_y=scene.render.resolution_x;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
 scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 bpy.context.view_layer.update();pts=[o.matrix_world@v.co for o in scene.objects if o.type=='MESH' for v in o.data.vertices];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(lo+hi)/2;span=max(hi-lo)
 def aim(o,t):o.rotation_euler=(Vector(t)-o.location).to_track_quat('-Z','Y').to_euler()
 world=bpy.data.worlds.new('Neutral studio');world.use_nodes=True;scene.world=world;nodes=world.node_tree.nodes;links=world.node_tree.links
 nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);nodes['Background'].inputs['Strength'].default_value=.3
 bg=nodes.new('ShaderNodeBackground');bg.inputs['Color'].default_value=tuple(ac.srgb_to_linear(v/255) for v in (232,228,220))+(1,);bg.inputs['Strength'].default_value=1
 ray=nodes.new('ShaderNodeLightPath');mix=nodes.new('ShaderNodeMixShader');links.new(ray.outputs['Is Camera Ray'],mix.inputs[0]);links.new(nodes['Background'].outputs[0],mix.inputs[1]);links.new(bg.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes['World Output'].inputs['Surface'])
 lights=[]
 for name,direction,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
  d=bpy.data.lights.new(name,'AREA');d.energy=power*span*span/4;d.size=size*span/2;d.shape='DISK';o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;aim(o,center);lights.append({'name':name,'direction':direction,'energy':d.energy,'size':d.size})
 mesh=bpy.data.meshes.new('Diagnostic floor');ext=span*20;mesh.from_pydata([(-ext,-ext,-.002),(ext,-ext,-.002),(ext,ext,-.002),(-ext,ext,-.002)],[],[(0,1,2,3)]);floor=bpy.data.objects.new('Diagnostic floor outside export',mesh);scene.collection.objects.link(floor);mesh.materials.append(ac.make_material('Studio floor','#E8E4DC',1))
 if gray:scene.view_layers[0].material_override=ac.make_material('Gray check','#939393',.9)
 data=bpy.data.cameras.new('Diagnostic camera');cam=bpy.data.objects.new('Diagnostic camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO';data.clip_start=.001;data.clip_end=100
 dest=out/'private/gray' if gray else out/'views';dest.mkdir(parents=True,exist_ok=True)
 proof={'glb_sha256':sha,'source':'Clean import of delivered model.glb; never source-scene proof','blender_version':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'resolution':[scene.render.resolution_x,scene.render.resolution_y],'samples':scene.cycles.samples,'gray':gray,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background_srgb':'#E8E4DC','lights':lights,'world_strength':.3,'framing':'Each canonical view fitted to whole asset with 18% margin; no turntable or cross-revision comparison claim','views':{}}
 for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
  cam.location=center+Vector(direction).normalized()*span*4;aim(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();q=[inv@p for p in pts];x0=min(v.x for v in q);x1=max(v.x for v in q);y0=min(v.y for v in q);y1=max(v.y for v in q);cam.location+=cam.matrix_world.to_3x3()@Vector(((x0+x1)/2,(y0+y1)/2,0));data.ortho_scale=max(x1-x0,y1-y0)*1.18
  file=dest/(name+'.png');scene.render.filepath=str(file);bpy.ops.render.render(write_still=True);proof['views'][name]={'path':str(file.relative_to(out)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'camera_direction':direction,'camera_location':list(cam.location),'ortho_scale':data.ortho_scale}
 if not gray:shutil.copyfile(dest/'perspective.png',out/'preview.png')
 target=out/'private/gray/evidence.json' if gray else out/'qa/evidence/exact-glb-views.json';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(proof,indent=2)+'\n')
