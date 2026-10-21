import bpy,sys,pathlib,json,hashlib,datetime,os,math
from mathutils import Vector
R=pathlib.Path('/workspace/shared/lowpoly-batch107-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch107-independent-qa-20261021');sys.path.insert(0,str(R/'scripts'));from asset_common import setup_scene,link_object,_look_at
id=sys.argv[sys.argv.index('--')+1];A=R/'production/small-life-batch107'/id/'r001';src=A/'artifacts'/f'{id}.glb';before=src.read_bytes();d=next(iter(json.loads((O/id/'source-geometry.json').read_text()).values()));C={c['tag']:c for c in d['contract']['components']};v=[Vector(x) for x in d['vertices_world_m']];col=setup_scene('independent-detail');bpy.ops.import_scene.gltf(filepath=str(src));sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=64;sc.cycles.use_denoising=False;sc.render.resolution_x=sc.render.resolution_y=512;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
world=bpy.data.worlds.new('detailworld');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.5,.5,.5,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6;sc.world=world
camd=bpy.data.cameras.new('auditcamera');cam=bpy.data.objects.new('auditcamera',camd);sc.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.000001;camd.clip_end=2;sc.camera=cam
if id=='stromatocystites':
 target=sum((v[i] for i in C['attachment_pad']['vertices']),Vector())/len(C['attachment_pad']['vertices']);views=[('aboral',(0,0,-1),.037)]
else:
 ids=C['mouth']['vertices'];rim=sum((v[i] for i in ids[24:36]),Vector())/12;floor=sum((v[i] for i in ids[36:48]),Vector())/12;n=(rim-floor).normalized();target=rim;views=[('mouth-normal',tuple(n),.0048),('mouth-oblique',tuple((n+Vector((.35,0,.4))).normalized()),.006)]
lights=[]
for name,direction,energy in [('key',(1,-2,3),.008),('fill',(-1,-1,-1),.003)]:
 l=bpy.data.lights.new(name,'AREA');l.energy=energy;l.size=.008;o=bpy.data.objects.new(name,l);sc.collection.objects.link(o);o.location=target+Vector(direction)*.008;_look_at(o,target);lights.append(o)
records=[]
for label,direction,scale in views:
 direction=Vector(direction);cam.location=target+direction*.05;_look_at(cam,target);camd.ortho_scale=scale;p=O/id/(label+'.png');sc.render.filepath=str(p);bpy.ops.render.render(write_still=True);records.append({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'target_blender_m':list(target),'direction':list(direction),'ortho_scale_m':scale,'resolution':[512,512]})
assert before==src.read_bytes();report={'glb_sha256':hashlib.sha256(before).hexdigest(),'brief_sha256':hashlib.sha256((A/'delivery-brief.json').read_bytes()).hexdigest(),'references_sha256':hashlib.sha256((A/'references.json').read_bytes()).hexdigest(),'frames':records,'geometry_or_materials_modified':False,'source_unchanged':True,'renderer':'Cycles CPU','pid':os.getpid(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()};(O/id/'supplementary-render-manifest.json').write_text(json.dumps(report,indent=2)+'\n')
