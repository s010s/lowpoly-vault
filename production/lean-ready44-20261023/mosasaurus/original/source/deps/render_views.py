# SPDX-License-Identifier: MIT
"""Four exact-export orthographic evidence views; optional cheap clay checkpoint."""
import argparse,hashlib,json,sys,shutil
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at
ap=argparse.ArgumentParser();ap.add_argument('--glb',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--clay',action='store_true');ap.add_argument('--samples',type=int,default=48);ap.add_argument('--resolution',type=int,default=512)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output_dir.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=setup_scene('exact-export-evidence');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a.glb)); imported=[o for o in bpy.data.objects if o not in before]
for o in imported:link_object(o,C,parent=False)
pts=_vertices_world(C);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples;scene.cycles.use_denoising=False
scene.render.resolution_x=a.resolution;scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('neutral-reference');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3;scene.world=world
for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
if a.clay:bpy.context.view_layer.material_override=make_material('gray-check','#9A9A9A',.9)
camd=bpy.data.cameras.new('orthographic-reference');cam=bpy.data.objects.new('orthographic-reference',camd);scene.collection.objects.link(cam);scene.camera=cam;camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=span*50
views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
if a.clay:views={k:views[k] for k in ['front','top','perspective']}
rows=[]
for name,dr in views.items():
    cam.location=center+Vector(dr).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();p=[inv@v for v in pts]
    mn=[min(v[i] for v in p) for i in range(2)];mx=[max(v[i] for v in p) for i in range(2)]
    cam.location+=cam.matrix_world.to_3x3()@Vector(((mn[0]+mx[0])/2,(mn[1]+mx[1])/2,0));camd.ortho_scale=max(mx[0]-mn[0],mx[1]-mn[1]) * 1.16
    dst=a.output_dir/(name+'.png');scene.render.filepath=str(dst);bpy.ops.render.render(write_still=True)
    rows.append({'view':name,'camera_direction':list(dr),'camera_position_m':list(cam.location),'orthographic_scale_m':camd.ortho_scale,'path':name+'.png','sha256':sha(dst)})
rec={'status':'RENDERED_NOT_INDEPENDENTLY_APPROVED','glb_sha256':sha(a.glb),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','samples':a.samples,'resolution':[a.resolution,a.resolution],'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'clay':a.clay,'source':'Fresh factory scene import of delivered GLB only; no source blend rendered','imported_meshes':[o.name for o in imported if o.type=='MESH'],'bounds_blender_m':{'min':lo,'max':hi},'views':rows,'renderer_script_sha256':sha(Path(__file__)),'gpu':'UNKNOWN','scene':'UNKNOWN'}
(a.output_dir/'render-evidence.json').write_text(json.dumps(rec,indent=2)+'\n')
