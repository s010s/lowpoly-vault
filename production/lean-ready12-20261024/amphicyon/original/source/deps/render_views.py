# SPDX-License-Identifier: MIT
"""Four clean exact-export views. No source scene is used or modified."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,srgb_to_linear,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--resolution',type=int,default=768);p.add_argument('--samples',type=int,default=64)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=a.model.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
g=audit_glb(src,12000,8,48);assert not g['errors'];before_hash=sha(src)
c=setup_scene('exact-export-render');r=bpy.data.objects[c['asset_root']];before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(src));obs=[o for o in bpy.data.objects if o not in before]
for o in obs:link_object(o,c,parent=False)
for o in obs:
 if o.parent not in obs:world=o.matrix_world.copy();o.parent=r;o.matrix_world=world
bpy.context.view_layer.update();pts=_vertices_world(c);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
tri=0
for o in obs:
 if o.type=='MESH':o.data.calc_loop_triangles();tri+=len(o.data.loop_triangles)
assert tri==g['scene_triangles'];expected_lo=[g['bounds_m']['min'][0],-g['bounds_m']['max'][2],g['bounds_m']['min'][1]];expected_hi=[g['bounds_m']['max'][0],-g['bounds_m']['min'][2],g['bounds_m']['max'][1]]
delta=max(abs(cur[i]-exp[i]) for cur,exp in [(lo,expected_lo),(hi,expected_hi)] for i in range(3));assert delta<.0001
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral-illumination');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
lights=[]
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center);lights.append({'name':name,'direction':list(direction),'energy':d.energy,'size':d.size})
d=bpy.data.cameras.new('qa-camera');cam=bpy.data.objects.new('qa-camera',d);scene.collection.objects.link(cam);d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30;scene.camera=cam
views={};directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
for name,direction in directions.items():
 cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@q for q in pts]
 minx=min(q.x for q in proj);maxx=max(q.x for q in proj);miny=min(q.y for q in proj);maxy=max(q.y for q in proj)
 cam.location+=cam.matrix_world.to_3x3()@Vector(((minx+maxx)/2,(miny+maxy)/2,0));d.ortho_scale=max(maxx-minx,maxy-miny)*1.20
 scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
 views[name]={'path':'views/'+name+'.png','sha256':sha(out/(name+'.png')),'camera_direction':list(direction),'camera_location':list(cam.location),'ortho_scale_m':d.ortho_scale,'resolution':[a.resolution,a.resolution]}
assert sha(src)==before_hash
report={'scope':'Clean Blender import and Cycles CPU views of exact GLB. Not Three.js GPU or populated-scene evidence.','glb_sha256':before_hash,'renderer_source_sha256':sha(Path(__file__).resolve()),'blender_version':bpy.app.version_string,'renderer':'Cycles CPU','threads':2,'samples':a.samples,'denoising':False,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'transparent':True,'lights':lights,'imported_triangles':tri,'imported_bounds_blender_m':{'min':lo,'max':hi},'roundtrip_bounds_max_error_m':delta,'views':views}
(out/'render-evidence.json').write_text(json.dumps(report,indent=2)+'\n')
