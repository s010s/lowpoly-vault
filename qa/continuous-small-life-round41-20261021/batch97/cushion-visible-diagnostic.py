import pathlib,sys
P=pathlib.Path(__file__).parent;s=(P/'inspect_source.py').read_text();exec(compile(s.split('records=[];relations=')[0],str(P/'inspect_source.py'),'exec'))
from asset_common import _look_at
source_results=json.loads((out/'cushion-dense-exposure.json').read_text());R={r['tag']:r for r in source_results['items']};scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
for o in list(bpy.data.objects):
 if o.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(o,do_unlink=True)
w=bpy.data.worlds.new('low-energy-neutral-world');w.use_nodes=True;w.node_tree.nodes['Background'].inputs['Color'].default_value=(.6,.6,.6,1);w.node_tree.nodes['Background'].inputs['Strength'].default_value=.4;scene.world=w
camd=bpy.data.cameras.new('exact-visible-sample');cam=bpy.data.objects.new('exact-visible-sample',camd);scene.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.00001;camd.clip_end=2;scene.camera=cam
ld=bpy.data.lights.new('key','AREA');ld.energy=.08;ld.size=.08;light=bpy.data.objects.new('key',ld);scene.collection.objects.link(light);rows=[]
for idx in [0,9,10,17]:
 tag=f'cushion_{idx:02d}';w=R[tag]['first_visible_witness'];target=Vector(w['point']);direction=Vector(w['direction']).normalized();cam.location=target+direction*.15;_look_at(cam,target);light.location=target+direction*.12+Vector((-.02,-.02,.03));_look_at(light,target)
 for scale in [.025,.008]:
  camd.ortho_scale=scale;f=out/f'{tag}-witness-{scale:.3f}m.png';scene.render.filepath=str(f);bpy.ops.render.render(write_still=True);rows.append({'tag':tag,'path':str(f),'sha256':H(f),'camera_position':list(cam.location),'target':list(target),'outward_ray':w,'ortho_scale_m':scale,'entire_original_mesh':True})
(out/'cushion-witness-render.json').write_text(json.dumps({'pid':os.getpid(),'source_sha256':H(src),'glb_sha256':H(glb),'blender':bpy.app.version_string,'renderer':'Cycles CPU','samples':32,'items':rows,'limitations':'Aims at known clear surface witness while retaining every original mesh triangle. Closeups diagnose useful visible cushion relief, never confer GPU/composed-scene approval.'},indent=2)+'\n')
