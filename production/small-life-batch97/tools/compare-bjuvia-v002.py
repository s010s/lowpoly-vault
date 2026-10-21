#!/usr/bin/env python3
"""New equal-length neutral comparison, actual exact candidate meshes; no source mutation."""
import bpy,bmesh,sys,json,hashlib,datetime,os,math,argparse
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'));from asset_common import make_material,_look_at,srgb_to_linear
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=argparse.ArgumentParser();a.add_argument('--bjuvia',required=True);a.add_argument('--glossopteris',required=True);a.add_argument('--output',required=True);args=a.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(args.output);out.mkdir(parents=True,exist_ok=True);assert not list(out.iterdir());start=datetime.datetime.now(datetime.timezone.utc).isoformat();entries=[]
for name,path,rotation in [('glossopteris',args.glossopteris,90),('bjuvia',args.bjuvia,0)]:
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=path);meshes=[o for o in bpy.data.objects if o.type=='MESH']
 if name=='glossopteris':
  # Explicit diagnostic-only isolation of leaf+vein materials, excluding matrix support.
  # The original exact GLB remains unchanged and is still the comparison identity.
  for o in meshes:
   bm=bmesh.new();bm.from_mesh(o.data);drop=[f for f in bm.faces if o.data.materials[f.material_index].name=='matrix'];bmesh.ops.delete(bm,geom=drop,context='FACES');loose=[v for v in bm.verts if not v.link_faces]
   if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
   bm.to_mesh(o.data);bm.free()
 rot=Matrix.Rotation(math.radians(rotation),4,'X');stored={o.name:[rot@(o.matrix_world@v.co) for v in o.data.vertices] for o in meshes};pts=sum(stored.values(),[]);lo=Vector([min(v[k] for v in pts) for k in range(3)]);hi=Vector([max(v[k] for v in pts) for k in range(3)]);center=(lo+hi)/2;factor=.5/(hi.z-lo.z);neutral=make_material('shared-neutral','#929292',roughness=.85)
 for o in meshes:
  o.parent=None;o.matrix_world=Matrix.Identity(4)
  for v,xyz in zip(o.data.vertices,stored[o.name]):v.co=(xyz-center)*factor
  o.data.materials.clear();o.data.materials.append(neutral)
  for p in o.data.polygons:p.material_index=0
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 world=bpy.data.worlds.new('neutral-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.65,.65,.65,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4;scene.world=world
 for label,pos,energy,size in [('key',(-1,-1.5,2),80,1.2),('fill',(1,-.7,1),25,1.4)]:
  dat=bpy.data.lights.new(label,'AREA');dat.energy=energy;dat.size=size;ob=bpy.data.objects.new(label,dat);scene.collection.objects.link(ob);ob.location=pos;_look_at(ob,Vector((0,0,0)))
 camd=bpy.data.cameras.new('same-camera');cam=bpy.data.objects.new('same-camera',camd);scene.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.0001;camd.clip_end=20;scene.camera=cam;views=[]
 for view,az,el,scale in [('front',0,0,.58),('oblique',35,30,.58),('detail',0,0,.16)]:
  az=math.radians(az);el=math.radians(el);cam.location=Vector((math.sin(az)*math.cos(el),-math.cos(az)*math.cos(el),math.sin(el)))*2;_look_at(cam,Vector((0,0,0)));camd.ortho_scale=scale;f=out/(name+'-'+view+'.png');scene.render.filepath=str(f);bpy.ops.render.render(write_still=True);views.append({'view':view,'path':f.name,'sha256':h(f),'ortho_scale_m':scale,'camera_position':list(cam.location)})
 entries.append({'name':name,'input_path':path,'input_sha256':h(path),'diagnostic_subset':'leaf and vein only; matrix excluded' if name=='glossopteris' else 'entire candidate','original_axis_conversion_degrees_x':rotation,'display_uniform_scale':factor,'same_display_length_m':.5,'actual_unscaled_oriented_bounds_size_m':list(hi-lo),'material':'same-neutral929292','frames':views})
(out/'comparison-manifest.json').write_text(json.dumps({'schema_version':1,'purpose':'Fresh97 Bjuvia versus exact prior Glossopteris, same actual lamina displayed0.5m length and neutral material/light/camera; no prior pixels reused. Comparison transforms are display-only, not delivered model edits.','pid':os.getpid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'renderer':'Blender Cycles CPU','blender_version':bpy.app.version_string,'script_sha256':h(__file__),'items':entries,'status':'generated-awaiting-personal-inspection','gpu_scene_claim':False},indent=2)+'\n')
