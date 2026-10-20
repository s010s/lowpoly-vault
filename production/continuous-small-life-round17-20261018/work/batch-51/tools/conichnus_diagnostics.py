# SPDX-License-Identifier: MIT
"""Gray top/oblique plus explicitly modified diagnostic section of exact input GLB."""
import sys,json,math,hashlib,time
from pathlib import Path
from datetime import datetime,timezone
import bpy,bmesh
from mathutils import Vector
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').is_file());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,link_object,make_material,_vertices_world,_bounds,_look_at
args=sys.argv[sys.argv.index('--')+1:];src=Path(args[0]).resolve();out=Path(args[1]).resolve();out.mkdir(parents=True,exist_ok=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_hash=sha(src);col=setup_scene('conichnus-diagnostics');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(src));objs=[o for o in bpy.data.objects if o not in before]
for o in objs:
 if o.type=='MESH':link_object(o,col)
clay=make_material('diagnostic-neutral-gray','#929292')
for o in col.all_objects:
 if o.type=='MESH':o.data.materials.clear();o.data.materials.append(clay)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False;scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
world=bpy.data.worlds.new('diagnostic-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5;scene.world=world
pts=_vertices_world(col);lo,hi=_bounds(pts);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);radius=max((p-center).length for p in pts);scale=2*radius*1.12
for name,loc,power,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=power*(2*radius)**2/4;data.size=size*radius;o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=center+Vector(loc)*radius;_look_at(o,center)
cam=bpy.data.objects.new('diagnostic-camera',bpy.data.cameras.new('diagnostic-camera'));scene.collection.objects.link(cam);cam.data.type='ORTHO';cam.data.ortho_scale=scale;cam.data.clip_start=.00001;cam.data.clip_end=10;scene.camera=cam
frames=[]
for name,dir in [('gray-top',(0,0,1)),('gray-oblique',(.574,-.819,.6)),('gray-section',(0,-1,.03))]:
 if name=='gray-section':
  for o in col.all_objects:
   if o.type!='MESH':continue
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-8,plane_co=(0,0,0),plane_no=(0,1,0),clear_inner=True,clear_outer=False);boundary=[e for e in bm.edges if e.is_boundary];bmesh.ops.holes_fill(bm,edges=boundary,sides=0);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
 cam.location=center+Vector(dir).normalized()*radius*6;_look_at(cam,center);bpy.context.view_layer.update();path=out/(name+'.png');scene.render.filepath=str(path);t=time.monotonic();bpy.ops.render.render(write_still=True)
 frames.append({'id':name,'path':path.name,'sha256':sha(path),'bytes':path.stat().st_size,'width':512,'height':512,'camera_matrix_world':[list(row) for row in cam.matrix_world],'orthographic_scale':scale,'source_glb_sha256':source_hash,'geometry_modified':name=='gray-section','modification':'Bisect at Blender Y=0, retain back half Y>=0, cap cut boundary. Explanatory section only; original delivered GLB untouched.' if name=='gray-section' else 'Material override only; geometry unchanged','wall_seconds':time.monotonic()-t})
assert sha(src)==source_hash
j={'kind':'targeted-diagnostic-manifest','source_glb':str(src.relative_to(R)),'source_glb_sha256':source_hash,'source_unchanged':True,'script_sha256':sha(Path(__file__)),'engine':'Blender 4.3.2 Cycles CPU','samples':16,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'frames':frames,'created_at':datetime.now(timezone.utc).isoformat(),'acceptance':'maker diagnostic only; independent review pending'};(out/'diagnostic-manifest.json').write_text(json.dumps(j,indent=2)+'\n')
