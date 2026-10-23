# SPDX-License-Identifier: MIT
"""Original Castorocauda reconstruction. Run with Blender 4.3.2.
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

def web_solid(name,points,mat,col):
 # Thin but closed connective membrane, never a solid oval flipper.
 n=len(points);verts=[(x,y,z+d) for d in [-.0006,.0006] for x,y,z in points]
 faces=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]
 faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
 return mesh_object(name,verts,faces,mat,col)

def build():
 col=setup_scene(P['asset_id'],P['seed'])
 mats={n:make_material(n,c) for n,c in P['palette_srgb'].items()}
 # Furred torso with deliberate changing thoracic and lumbar profile.
 torso=sweep('Furred_trunk',[((0,-.090,.044),.010,.012),((0,-.077,.046),.019,.021),((0,-.052,.048),.024,.023),((0,-.020,.047),.025,.023),((0,.015,.045),.0235,.021),((0,.045,.043),.0215,.020),((0,.070,.041),.020,.019),((0,.090,.037),.014,.014)],mats['fur'],col,20)
 torso.data.materials.append(mats['underfur'])
 for f in torso.data.polygons:
  if f.center.z<.032:f.material_index=1
 sweep('Neck_low_continuous',[((0,-.073,.047),.017,.019),((0,-.088,.048),.016,.017),((0,-.102,.049),.013,.014)],mats['fur'],col,16)
 head=sweep('Head_pointed_mammaliaform',[((0,-.093,.049),.010,.012),((0,-.105,.051),.016,.015),((0,-.119,.050),.014,.014),((0,-.132,.047),.010,.010),((0,-.148,.0425),.0065,.0065),((0,-.1575,.041),.004,.004)],mats['fur'],col,16)
 head.data.materials.append(mats['underfur'])
 for f in head.data.polygons:
  if f.center.z<.040:f.material_index=1
 ellipsoid('Small_dark_nose',(0,-.158,.041),(.0042,.002,.003),mats['nose'],col,12,6)
 for s,label in [(-1,'R'),(1,'L')]:
  ellipsoid('Eye_'+label,(s*.0136,-.119,.0555),(.0022,.0027,.002),mats['nose'],col,10,6)
  ellipsoid('Inferred_small_ear_'+label,(s*.014,-.098,.062),(.0037,.003,.0053),mats['fur'],col,10,6)
 # Long horizontally broad paddle, not a vertical disk or cylindrical otter tail.
 # First quarter stays furred; middle predominantly scaled, distal scale/hair mixed.
 tail_stations=[((0,.086,.034),.013,.010),((0,.105,.023),.020,.007),((0,.125,.015),.026,.005),((0,.145,.012),.030,.0045),((0,.170,.011),.032,.004),((0,.200,.0105),.0325,.0038),((0,.230,.010),.032,.0035),((0,.260,.009),.029,.003),((0,.285,.0085),.024,.0025),((0,.304,.008),.016,.002),((0,.315,.0078),.008,.0017),((0,.320,.0075),.001,.0008)]
 tail=sweep('Tail_broad_horizontal_paddle',tail_stations,mats['tail'],col,24)
 tail.data.materials.append(mats['fur'])
 for f in tail.data.polygons:
  y=f.center.y
  if y<.145 or (y>.2625 and abs(f.center.x)>.016):f.material_index=1
 # Fine tessellated relief reads as a low-contrast scale field, not armored plates.
 # Relief is confined to 0.12 mm and shares the tail material.
 scales=[]
 def tail_at(y):
  for i in range(len(tail_stations)-1):
   a,b=tail_stations[i],tail_stations[i+1]
   if a[0][1]<=y<=b[0][1]:
    t=(y-a[0][1])/(b[0][1]-a[0][1]);return (a[0][2]*(1-t)+b[0][2]*t,a[1]*(1-t)+b[1]*t,a[2]*(1-t)+b[2]*t)
 for row in range(26):
  y=.151+row*.0055;zc,rx,rz=tail_at(y)
  for k in range(-5,6):
   x=(k+(.5 if row%2 else 0))*.0053
   if abs(x)>rx*.82:continue
   z=zc+rz*math.sqrt(max(0,1-(x/rx)**2))
   verts=[(x-.0023,y,z-.00015),(x,y-.0023,z-.00015),(x+.0023,y,z-.00015),(x,y+.0023,z-.00015),(x,y,z+.00012),(x,y,z-.0005)]
   faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(1,0,5),(2,1,5),(3,2,5),(0,3,5)]
   scales.append(mesh_object('scale',verts,faces,mats['tail'],col))
 combine('Tail_fine_scale_field',scales,mats['tail'],col)
 # Compact limbs with lateral elbows/knees and individual splayed digits.
 contact_pads=[]
 for s,label in [(-1,'R'),(1,'L')]:
  sweep('Forelimb_robust_'+label,[((s*.017,-.064,.048),.0095,.011),((s*.030,-.052,.034),.010,.010),((s*.034,-.060,.021),.007,.008),((s*.035,-.077,.010),.0058,.0055)],mats['fur'],col,12)
  palm=ellipsoid('Manus_pad_'+label,(s*.035,-.080,.006),(.009,.010,.006),mats['fur'],col,12,6);contact_pads.append(palm)
  fingerobs=[];clawobs=[]
  for i in range(5):
   dx=(i-2)*.0044;angle=(i-2)*.23
   base=Vector((s*(.035+dx*.66),-.085,.005))
   end=Vector((s*(.035+dx+math.sin(angle)*.009),-.095-.003*(2-abs(i-2)),.0032))
   mid=base.lerp(end,.52);mid.z=.0042
   fingerobs.append(sweep('finger',[(base,.00225,.002), (mid,.0019,.0016),(end,.00125,.0012)],mats['fur'],col,8))
   clawend=end+Vector((s*math.sin(angle)*.003,-.0033,-.001))
   clawobs.append(sweep('claw',[(end,.0013,.0012),(clawend,.00025,.00025)],mats['claw'],col,7))
  combine('Manus_five_separate_digits_'+label,fingerobs,mats['fur'],col);combine('Manus_modest_claws_'+label,clawobs,mats['claw'],col)
  hindstations=[((s*.015,.064,.040),.012,.014),((s*.030,.050,.030),.013,.013),((s*.038,.055,.020),.009,.008),((s*.043,.072,.009),.006,.005)]
  if s==-1:hindstations=[((v[0]-.012*i/3,v[1]+.020*i/3,v[2]),rx,ry) for i,(v,rx,ry) in enumerate(hindstations)]
  sweep('Hindlimb_flexed_'+label,hindstations,mats['fur'],col,14)
  pad=ellipsoid('Pes_pad_'+label,(s*.046,.075,.006),(.009,.012,.006),mats['fur'],col,12,6);contact_pads.append(pad)
  toeobs=[];clawobs=[];starts=[];ends=[]
  # Hind toes fan laterally as in the source skeleton, not a seal flipper.
  for i in range(5):
   t=(i-2)/2;angle=-.80+t*.54
   base=Vector((s*(.048+.002*t),.076+.004*t,.005))
   length=.021-.003*abs(t)
   end=base+Vector((s*math.cos(angle)*length,math.sin(angle)*length,.003-base.z))
   mid=base.lerp(end,.56);mid.z=.004
   starts.append(base);ends.append(end)
   toeobs.append(sweep('toe',[(base,.0024,.002),(mid,.002,.0017),(end,.00125,.0012)],mats['fur'],col,8))
   delta=(end-base).normalized()*.0027;delta.z=-.001
   clawobs.append(sweep('claw',[(end,.0013,.0011),(end+delta,.00022,.00022)],mats['claw'],col,7))
  combine('Pes_five_splayed_digits_'+label,toeobs,mats['fur'],col);combine('Pes_small_claws_'+label,clawobs,mats['claw'],col)
  webs=[]
  for i in range(4):
   a=starts[i];b=starts[i+1];c=b.lerp(ends[i+1],.57);d=a.lerp(ends[i],.57)
   # Shallow concave outer edge leaves the distal 43% of each toe free.
   m=(c+d)*.5;m=m.lerp((a+b)*.5,.16)
   webs.append(web_solid('web',[tuple(a),tuple(b),tuple(c),tuple(m),tuple(d)],mats['tail'],col))
  combine('Pes_partial_interdigital_webbing_'+label,webs,mats['tail'],col)
 # A modest asymmetric hind step preserves section widths and all five toe rays.
 for ob in col.objects:
  if ob.type=='MESH' and ob.name.startswith('Pes_') and ob.name.endswith('_R'):
   for v in ob.data.vertices:v.co.x-=.012;v.co.y+=.020
 # Origin is at the center of the contact footprint. Pads begin on the floor.
 contacts=[v.co.copy() for ob in contact_pads for v in ob.data.vertices if v.co.z<=.00001]
 cx=(min(v.x for v in contacts)+max(v.x for v in contacts))/2
 cy=(min(v.y for v in contacts)+max(v.y for v in contacts))/2
 for ob in col.objects:
  if ob.type=='MESH':
   for v in ob.data.vertices:v.co.x-=cx;v.co.y-=cy
 bpy.context.view_layer.update()
 root=bpy.data.objects[col['asset_root']]
 root['representation']='living-reconstruction';root['scientific_scope']='Castorocauda lutrasimilis, whole living mammaliaform; inferred soft tissues'
 root['scale_note']='0.48 m estimated living length; preserved holotype 0.425 m and incomplete cranium 0.060 m are not living body dimensions'
 root['webbing_note']='Conservative proximal 57 percent web span; fossil suggests partial webbing, exact extent unknown'
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
 if gray:directions={k:directions[k] for k in ('front','side','top','perspective')}
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
 write(out/'qa/evidence/build.json',{'asset_id':P['asset_id'],'revision':P['revision'],'seed':P['seed'],'blender_version':bpy.app.version_string,'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'dependencies_sha256':digest(HERE/'dependencies.json'),'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),'semantic_digest':semantic_digest(doc,binpart),'export_options':options,'body_length_note':'0.48 m living reconstruction estimate; 0.425 m preserved rostrum-tail and 0.060 m incomplete cranium are distinct fossil measurements','anatomy_note':'Broad dorsoventrally flattened tail and conservative partial hindfoot webbing; soft-tissue volumes, ears and palette are inferred'})
if __name__=='__main__':main()
