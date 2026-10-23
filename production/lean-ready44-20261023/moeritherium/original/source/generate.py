# SPDX-License-Identifier: MIT
"""Original Moeritherium reconstruction. Run with Blender 4.3.2.
Usage: blender -b -t 2 --python source/generate.py -- --output . --stage build
Stages: gray (authoring check), build (editable blend and GLB), views (exact GLB).
All model dependencies are adjacent in deps; no external content is loaded.
"""
from pathlib import Path
import argparse,hashlib,json,math,shutil,sys
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source,_vertices_world,_bounds,_look_at,srgb_to_linear
from qa_glb import audit_glb,read_glb,semantic_digest
P=json.loads((HERE/'params.json').read_text())

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

def sweep(name,stations,mat,col,sides=12,phase=0):
 """Closed path loft with elliptical cross sections and explicit tapering."""
 verts=[];faces=[]
 for i,(xyz,rx,ry) in enumerate(stations):
  p=Vector(xyz)
  tangent=Vector(stations[min(i+1,len(stations)-1)][0])-Vector(stations[max(0,i-1)][0]);tangent.normalize()
  ax=Vector((1,0,0));ax=ax-tangent*ax.dot(tangent)
  if ax.length<.1:ax=Vector((0,1,0))-tangent*tangent.y
  ax.normalize();ay=tangent.cross(ax).normalized()
  for k in range(sides):
   a=2*math.pi*k/sides+phase;v=p+ax*(math.cos(a)*rx)+ay*(math.sin(a)*ry);verts.append(tuple(v))
 for i in range(len(stations)-1):
  for k in range(sides):
   a=i*sides+k;b=i*sides+(k+1)%sides;c=(i+1)*sides+(k+1)%sides;d=(i+1)*sides+k
   if (i+k)%2:faces.extend([(a,b,d),(b,c,d)])
   else:faces.extend([(a,b,c),(a,c,d)])
 faces.extend([tuple(reversed(range(sides))),tuple((len(stations)-1)*sides+k for k in range(sides))])
 return mesh_object(name,verts,faces,mat,col)

def ellipsoid(name,c,r,mat,col,segments=12,rings=6):
 verts=[(c[0],c[1],c[2]+r[2])];faces=[]
 for j in range(1,rings):
  t=math.pi*j/rings
  for k in range(segments):
   a=2*math.pi*k/segments;verts.append((c[0]+r[0]*math.sin(t)*math.cos(a),c[1]+r[1]*math.sin(t)*math.sin(a),c[2]+r[2]*math.cos(t)))
 bottom=len(verts);verts.append((c[0],c[1],c[2]-r[2]))
 for k in range(segments):faces.append((0,1+k,1+(k+1)%segments))
 for j in range(rings-2):
  for k in range(segments):
   a=1+j*segments+k;b=1+j*segments+(k+1)%segments;c1=b+segments;d=a+segments
   faces.extend([(a,b,c1),(a,c1,d)])
 for k in range(segments):faces.append((bottom,1+(rings-2)*segments+(k+1)%segments,1+(rings-2)*segments+k))
 return mesh_object(name,verts,faces,mat,col)

def combine(name,objects,mat,col):
 verts=[];faces=[]
 for ob in objects:
  n=len(verts);verts.extend(tuple(v.co) for v in ob.data.vertices);faces.extend(tuple(n+i for i in f.vertices) for f in ob.data.polygons)
  bpy.data.objects.remove(ob,do_unlink=True)
 return mesh_object(name,verts,faces,mat,col)

def build():
 col=setup_scene(P['asset_id'],P['seed'])
 mats={n:make_material(n,c) for n,c in P['palette_srgb'].items()}
 # Integrated loft: low elongated skull, substantial neck and very long barrel trunk.
 # Profiles are original soft-tissue decisions around the frozen composite skeleton.
 sections=[(-1.30,.495,.045,.045),(-1.29,.505,.095,.067),(-1.235,.515,.112,.077),(-1.16,.535,.119,.085),(-1.07,.555,.130,.105),(-.98,.555,.151,.120),(-.89,.555,.155,.120),(-.80,.540,.166,.131),(-.70,.505,.192,.170),(-.59,.470,.225,.219),(-.46,.450,.258,.250),(-.27,.445,.278,.252),(0,.445,.280,.250),(.25,.445,.273,.245),(.47,.445,.252,.236),(.64,.435,.205,.211),(.76,.420,.122,.155),(.81,.412,.044,.075)]
 body=sweep('Integrated_low_head_neck_long_barrel',[((0,y,z),rx,rz) for y,z,rx,rz in sections],mats['skin'],col,24)
 body.data.materials.append(mats['underside']);body.data.materials.append(mats['muzzle'])
 for f in body.data.polygons:
  if f.center.y< -1.16:f.material_index=2
  elif f.center.z<.285 and -.65<f.center.y<.70:f.material_index=1
 # Lip contours remain on the muzzle, not a hanging proboscis or giant hippo jaw.
 sweep('Restrained_lower_lip',[((0,-1.285,.457),.062,.018),((0,-1.245,.446),.095,.030),((0,-1.14,.448),.097,.035),((0,-1.035,.466),.111,.041),((0,-.965,.489),.115,.042)],mats['muzzle'],col,16)
 for s,label in [(-1,'R'),(1,'L')]:
  # Small eye beneath a quiet orbital brow, not cartoon elevated hippo eyes.
  ellipsoid('Eye_'+label,(s*.143,-1.007,.588),(.013,.019,.013),mats['dark'],col,12,6)
  sweep('Orbital_brow_'+label,[((s*.132,-1.052,.602),.009,.012),((s*.151,-1.010,.611),.013,.011),((s*.148,-.974,.601),.010,.010)],mats['skin'],col,10)
  # Small rounded pinnae with substantial attachment to skull.
  ear=ellipsoid('Small_ear_'+label,(s*.157,-.855,.595),(.035,.052,.054),mats['skin'],col,12,8)
  ear.data.materials.append(mats['muzzle'])
  for f in ear.data.polygons:
   if s*f.center.x>.173 and f.center.y<-.850:f.material_index=1
  ellipsoid('Nostril_'+label,(s*.065,-1.287,.536),(.014,.006,.009),mats['dark'],col,10,6)
  # Incisors arise from the front jaw. Their small exposed portions are inferred.
  sweep('Small_upper_incisor_'+label,[((s*.070,-1.236,.463),.015,.016),((s*.074,-1.249,.425),.013,.013),((s*.074,-1.260,.405),.004,.005)],mats['incisors'],col,10)
  sweep('Modest_lower_incisor_'+label,[((s*.039,-1.262,.452),.009,.008),((s*.040,-1.287,.463),.006,.005),((s*.040,-1.294,.465),.002,.002)],mats['incisors'],col,9)
  # Mouth line is restrained and mostly lateral, never a deep open maw.
  sweep('Mouth_line_'+label,[((s*.099,-1.247,.459),.003,.003),((s*.112,-1.17,.458),.003,.003),((s*.126,-1.08,.477),.002,.002)],mats['dark'],col,7)
 contacts=[]
 for s,label in [(-1,'R'),(1,'L')]:
  delta=.055 if s==-1 else 0
  sweep('Forelimb_short_flexed_'+label,[((s*.180,-.460,.493),.106,.128),((s*.220,-.423,.345),.084,.103),((s*.225,-.468-delta*.4,.215),.063,.077),((s*.230,-.510-delta,.070),.067,.075)],mats['skin'],col,16)
  fy=-.540-delta
  foot=ellipsoid('Forefoot_support_'+label,(s*.232,fy,.045),(.087,.110,.045),mats['skin'],col,16,8);contacts.append(foot)
  # Three low-relief nail accents indicate broad feet, not a claimed fossil digit count.
  nails=[]
  for i in (-1,0,1):
   nails.append(ellipsoid('nail',(s*.232+i*.043,fy-.095+abs(i)*.012,.030),(.019,.013,.017),mats['nails'],col,10,6))
  combine('Inferred_forefoot_nail_accents_'+label,nails,mats['nails'],col)
  hy=.580+delta
  sweep('Hindlimb_short_flexed_'+label,[((s*.168,.570,.470),.123,.140),((s*.229,.535,.330),.107,.116),((s*.235,.645+delta*.5,.190),.071,.083),((s*.241,hy+.020,.070),.067,.074)],mats['skin'],col,16)
  foot=ellipsoid('Hindfoot_support_'+label,(s*.242,hy-.010,.043),(.088,.106,.043),mats['skin'],col,16,8);contacts.append(foot)
  nails=[]
  for i in (-1,0,1):nails.append(ellipsoid('nail',(s*.242+i*.043,hy-.101+abs(i)*.012,.028),(.019,.013,.016),mats['nails'],col,10,6))
  combine('Inferred_hindfoot_nail_accents_'+label,nails,mats['nails'],col)
 # Short, tapering and down-curving tail. No elephant-like tuft is asserted.
 sweep('Modest_tapering_tail',[((0,.755,.433),.043,.044),((0,.850,.378),.035,.035),((.012,.925,.292),.026,.026),((.018,.984,.213),.014,.014),((.019,1.000,.188),.003,.003)],mats['skin'],col,12)
 # Move contact-center to the root while preserving length, proportions and zero ground.
 cs=[v.co.copy() for ob in contacts for v in ob.data.vertices if v.co.z<.00001]
 cx=(min(v.x for v in cs)+max(v.x for v in cs))/2;cy=(min(v.y for v in cs)+max(v.y for v in cs))/2
 for ob in col.objects:
  if ob.type=='MESH':
   for v in ob.data.vertices:v.co.x-=cx;v.co.y-=cy
 points=[v.co for ob in col.objects if ob.type=='MESH' for v in ob.data.vertices]
 length=max(v.y for v in points)-min(v.y for v in points);height=max(v.z for v in points)
 for ob in col.objects:
  if ob.type=='MESH':
   for v in ob.data.vertices:v.co.y*=P['length_model_m']/length;v.co.z*=P['shoulder_height_model_m']/height
 bpy.context.view_layer.update();root=bpy.data.objects[col['asset_root']]
 root['representation']='living-reconstruction';root['scientific_scope']='Moeritherium lyonsi, complete living reconstruction around a composite skeletal restoration'
 root['scale_note']='2.30 m length, 0.70 m shoulder height and 235 kg are composite restoration estimates, not measurements of one individual'
 root['specimen_note']='Young skull C.7867 enlarged by 15 percent with postcranial bones of different adults; Paris skull image is a cast comparison without verified specimen identity or scale'
 root['inference_note']='Skin, width, ears, muzzle flesh, feet, nail accents, tail details and palette are inferred; no conventional proboscis added'
 bpy.context.scene.render.filepath='//render'
 return col


def render(col,out,gray=False):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8 if gray else 32;scene.cycles.use_denoising=False
 scene.render.threads_mode='FIXED';scene.render.threads=2
 scene.render.resolution_x=360 if gray else 512;scene.render.resolution_y=scene.render.resolution_x;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=not gray
 scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 world=bpy.data.worlds.new('Review_world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.7,.7,.7,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45;scene.world=world
 points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
 for name,direction,energy,size in [('key',(-3,-4,6),650,4),('fill',(4,-1,3),230,5)]:
  data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
  ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center)
 data=bpy.data.cameras.new('Review_camera');cam=bpy.data.objects.new('Review_camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO';data.clip_start=.001;data.clip_end=span*30
 if gray:bpy.context.view_layer.material_override=make_material('Gray_check','#949494')
 directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
 if gray:directions={k:directions[k] for k in ('front','side','top','perspective')}
 report={}
 for name,direction in directions.items():
  cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();pp=[inv@p for p in points]
  xmin,xmax=min(p.x for p in pp),max(p.x for p in pp);ymin,ymax=min(p.y for p in pp),max(p.y for p in pp)
  cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));data.ortho_scale=span*1.20
  path=out/(name+'.png');scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
  report[name]={'sha256':digest(path),'camera_direction':direction,'projection':'ORTHO','orthographic_scale_m':data.ortho_scale}
 return report

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',default='.');parser.add_argument('--stage',choices=['build','gray','views'],default='build');a=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 if a.stage=='views':
  glb=out/'model.glb';sha=digest(glb);bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(glb))
  col=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(col)
  for ob in list(bpy.context.scene.objects):
   for c in list(ob.users_collection):c.objects.unlink(ob)
   col.objects.link(ob)
  views=render(col,out/'views');shutil.copyfile(out/'views/perspective.png',out/'preview.png')
  write(out/'qa/evidence/exact-glb-views.json',{'status':'RENDERED_FOR_VISUAL_REVIEW','glb_sha256':sha,'renderer':'Blender 4.3.2 Cycles CPU','gpu_claim':False,'samples':32,'resolution':[512,512],'transparent':True,'view_transform':'Standard','look':'None','views':views,'preview_reuses':'views/perspective.png','generator_sha256':digest(HERE/'generate.py')});return
 col=build()
 if a.stage=='gray':
  views=render(col,out,gray=True);write(out/'gray-render.json',{'source_stage_only':True,'views':views});return
 source=audit_source(col,16000)
 if source['errors']:raise RuntimeError(source['errors'])
 # Clear inherited file-browser hints before saving the portable source.
 for screen in bpy.data.screens:
  for area in screen.areas:
   for space in area.spaces:
    if space.type=='FILE_BROWSER' and space.params:
     space.params.directory=b'.'*1023;space.params.directory=b'//';space.params.filename='model.blend'
 bpy.context.preferences.filepaths.save_version=0
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=False)
 bpy.ops.object.select_all(action='DESELECT')
 for ob in col.all_objects:ob.select_set(True)
 bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
 options={'export_format':'GLB','use_selection':True,'export_yup':True,'export_apply':True,'export_normals':True,'export_texcoords':False,'export_tangents':False,'export_materials':'EXPORT','export_vertex_color':'NONE','export_animations':False,'export_skins':False,'export_morph':False,'export_cameras':False,'export_lights':False,'export_extras':True,'export_gpu_instances':False,'export_gn_mesh':False,'export_draco_mesh_compression_enable':False,'export_use_gltfpack':False}
 available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties};missing=set(options)-available
 if missing:raise RuntimeError('Required exporter settings missing: '+str(missing))
 bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
 glb=audit_glb(out/'model.glb',16000,6,48)
 if glb['errors']:raise RuntimeError(glb['errors'])
 if glb['bytes']>2200000:raise RuntimeError('GLB byte budget exceeded')
 source['glb_sha256']=digest(out/'model.glb');glb['file']='model.glb'
 write(out/'qa/evidence/source-check.json',source);write(out/'qa/evidence/glb-check.json',glb)
 doc,binpart,data=read_glb(out/'model.glb')
 write(out/'qa/evidence/build.json',{'asset_id':P['asset_id'],'revision':P['revision'],'seed':P['seed'],'blender_version':bpy.app.version_string,'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'dependencies_sha256':digest(HERE/'dependencies.json'),'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),'semantic_digest':semantic_digest(doc,binpart),'export_options':options,'body_length_note':'2.30 m long and 0.70 m shoulder height are published composite restoration estimates, not a single measured animal. Young skull C.7867 enlarged 15 percent combined with different adult postcrania.','anatomy_note':'Long low barrel, short flexed limbs and modest integrated muzzle, no proboscis. Skin, ears, lip shape, feet and palette are inferred.'})
if __name__=='__main__':main()
