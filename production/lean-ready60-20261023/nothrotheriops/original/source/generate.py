# SPDX-License-Identifier: MIT
"""Original Nothrotheriops reconstruction. Run with Blender 4.3.2.
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

def build():
 col=setup_scene(P['asset_id'],P['seed'])
 mats={n:make_material(n,c) for n,c in P['palette_srgb'].items()}
 # Custom dorsal silhouette, slender thorax relative to the powerful pelvis.
 torso=sweep('Torso_arched_ribcage',[((0,-.62,.94),.10,.13),((0,-.51,1.00),.22,.26),((0,-.30,1.035),.28,.305),((0,-.05,1.025),.32,.33),((0,.20,1.00),.335,.33),((0,.42,.95),.32,.32),((0,.62,.88),.285,.30),((0,.78,.80),.20,.23),((0,.86,.74),.09,.13)],mats['body'],col,20)
 torso.data.materials.append(mats['under'])
 for f in torso.data.polygons:
  if f.center.z<.75:f.material_index=1
 sweep('Neck_forward_narrow',[((0,-.50,1.055),.15,.19),((0,-.65,1.105),.135,.15),((0,-.76,1.105),.105,.12),((0,-.84,1.08),.082,.10)],mats['body'],col,16)
 # Small elongated cranium and narrow muzzle, not a bear-like block head.
 sweep('Head_elongated_closed_muzzle',[((0,-.80,1.08),.068,.09),((0,-.85,1.085),.089,.108),((0,-.92,1.06),.085,.09),((0,-1.00,1.025),.067,.067),((0,-1.08,.995),.050,.048),((0,-1.132,.988),.041,.036)],mats['body'],col,16)
 ellipsoid('Nose_soft_inferred',(0,-1.133,.994),(.043,.007,.027),mats['nose'],col,12,6)
 # No carved white face mask and no exposed teeth or tusks.
 for s,label in [(-1,'R'),(1,'L')]:
  ellipsoid('Eye_'+label,(s*.079,-.936,1.088),(.009,.012,.009),mats['eye'],col,10,5)
  ellipsoid('Ear_small_'+label,(s*.096,-.828,1.149),(.024,.019,.036),mats['body'],col,10,6)
 # Strong, long tail: gentle centerline bend and continuous section taper.
 sweep('Tail_muscular_taper',[((0,.72,.77),.165,.18),((0,.85,.65),.153,.16),((0,1.02,.48),.12,.125),((.015,1.18,.31),.09,.095),((.035,1.33,.20),.059,.067),((.045,1.47,.135),.033,.041),((.04,1.60,.115),.005,.006)],mats['body'],col,14)
 for s,label in [(-1,'R'),(1,'L')]:
  # Deliberately long and narrow, elbow back and wrist reaching forward.
  sweep('Forelimb_slender_'+label,[((s*.205,-.43,1.07),.112,.13),((s*.266,-.36,.91),.105,.11),((s*.29,-.30,.65),.081,.085),((s*.30,-.34,.565),.071,.075),((s*.305,-.53,.39),.06,.065),((s*.31,-.745,.205),.048,.056),((s*.31,-.82,.147),.052,.055)],mats['body'],col,12)
  sweep('Manus_curled_lateral_pad_'+label,[((s*.31,-.78,.19),.055,.067),((s*.32,-.85,.12),.088,.077),((s*.33,-.92,.09),.092,.066),((s*.33,-.95,.085),.070,.054)],mats['body'],col,12)
  # Digit V is a reduced fleshy lateral edge in the palm, never a fifth claw.
  # Each separately named claw is open to individual anatomical editing.
  for digit,offset,length,thick in [('I',-.074,.072,.018),('II',-.038,.178,.028),('III',.012,.157,.029),('IV',.059,.148,.025)]:
   x=s*(.33+offset);y=-.929+(abs(offset)*.14);z=.112+(0.012 if digit=='I' else 0)
   sweep('Manus_'+label+'_digit_'+digit+'_claw',[((x,y,z),thick,thick*.85),((x-s*.008,y-length*.35,z-.015),thick*.85,thick*.72),((x-s*.024,y-length*.72,z-.034),thick*.50,thick*.44),((x-s*.041,y-length*.88,z-.016),thick*.25,thick*.26),((x-s*.052,y-length*.83,z+.013),.0028,.0028)],mats['claw'],col,9)
  # Bent powerful thigh and smaller lower leg; hind limb not a column.
  sweep('Hindlimb_flexed_'+label,[((s*.215,.56,.91),.16,.20),((s*.29,.50,.79),.18,.205),((s*.335,.33,.58),.145,.155),((s*.35,.29,.43),.105,.12),((s*.35,.43,.285),.086,.095),((s*.35,.58,.16),.071,.083)],mats['body'],col,14)
  # Pedolateral support. The outer fifth-digit pad is part of the broad outer foot.
  sweep('Pes_lateral_support_'+label,[((s*.35,.58,.16),.083,.09),((s*.37,.52,.108),.118,.10),((s*.37,.40,.078),.123,.076),((s*.36,.32,.08),.105,.065)],mats['body'],col,14)
  # I absent externally. III biggest, II intermediate, IV smallest and incurved.
  for digit,offset,length,thick,inward in [('II',-.067,.122,.027,.037),('III',-.006,.176,.039,.032),('IV',.067,.095,.023,.055)]:
   x=s*(.36+offset);y=.331;z=.108
   sweep('Pes_'+label+'_digit_'+digit+'_claw',[((x,y,z),thick,thick*.8),((x-s*inward*.22,y-length*.40,z-.010),thick*.81,thick*.65),((x-s*inward*.62,y-length*.80,z-.035),thick*.49,thick*.43),((x-s*inward,y-length,z-.020),.003,.003)],mats['claw'],col,10)
 # Four supported contacts: adjust the wrist/palm ends, not the upper shoulders.
 front_pads=[o for o in col.objects if o.name.startswith('Manus_curled_lateral_pad')]
 hind_pads=[o for o in col.objects if o.name.startswith('Pes_lateral_support')]
 drop=min(v.co.z for o in front_pads for v in o.data.vertices)-min(v.co.z for o in hind_pads for v in o.data.vertices)
 for ob in col.objects:
  if ob.type!='MESH':continue
  if ob.name.startswith('Manus_'):
   for v in ob.data.vertices:v.co.z-=drop
  elif ob.name.startswith('Forelimb_'):
   for v in ob.data.vertices:v.co.z-=drop*min(1,max(0,(.90-v.co.z)/.66))
 # Exact foot contact grounding without moving the identity export root.
 points=_vertices_world(col);low,high=_bounds(points)
 for obj in col.objects:
  if obj.type=='MESH':
   for v in obj.data.vertices:v.co.z-=low[2]
 # Root is the center of the four contact patches, not of the tail bounding box.
 contacts=[v.co.copy() for ob in front_pads+hind_pads for v in ob.data.vertices if v.co.z<=.003]
 center_x=(min(v.x for v in contacts)+max(v.x for v in contacts))/2
 center_y=(min(v.y for v in contacts)+max(v.y for v in contacts))/2
 for ob in col.objects:
  if ob.type=='MESH':
   for v in ob.data.vertices:v.co.x-=center_x;v.co.y-=center_y
 bpy.context.view_layer.update()
 root=bpy.data.objects[col['asset_root']]
 root['representation']='living-reconstruction';root['scientific_scope']='Nothrotheriops shastensis, whole body, estimated soft tissues'
 root['digit_note']='Manus I-IV clawed, V reduced nonclawed; pes II-IV differentiated claws, I absent, V nonclawed lateral support'
 bpy.context.scene.render.filepath='//render'
 return col

def render(col,out,gray=False):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=12 if gray else 40;scene.cycles.use_denoising=False
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
 if gray:directions={k:directions[k] for k in ('front','side','perspective')}
 report={}
 for name,direction in directions.items():
  cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();pp=[inv@p for p in points]
  xmin,xmax=min(p.x for p in pp),max(p.x for p in pp);ymin,ymax=min(p.y for p in pp),max(p.y for p in pp)
  cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));data.ortho_scale=max(xmax-xmin,ymax-ymin)*1.20
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
  write(out/'qa/evidence/exact-glb-views.json',{'status':'RENDERED_FOR_VISUAL_REVIEW','glb_sha256':sha,'renderer':'Blender 4.3.2 Cycles CPU','gpu_claim':False,'samples':40,'resolution':[512,512],'transparent':True,'view_transform':'Standard','look':'None','views':views,'preview_reuses':'views/perspective.png','generator_sha256':digest(HERE/'generate.py')});return
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
 write(out/'qa/evidence/build.json',{'asset_id':P['asset_id'],'revision':P['revision'],'seed':P['seed'],'blender_version':bpy.app.version_string,'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'dependencies_sha256':digest(HERE/'dependencies.json'),'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),'semantic_digest':semantic_digest(doc,binpart),'export_options':options,'body_length_note':'2.74 m approximate posed nose-to-tail projection; species estimate, not specimen measurement','anatomy_note':'Explicitly differentiated hand and foot claws; soft tissues and padding are original estimates'})
if __name__=='__main__':main()
