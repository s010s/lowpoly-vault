# SPDX-License-Identifier: MIT
"""Original Pliosaurus carpenteri BRSMG Cd6172 whole living reconstruction.
Run with Blender --background --factory-startup --python source/generate.py -- --output DIR.
Fossil-based skull length is 1.8 m. Whole length 8 m and all flesh dimensions are
reconstruction estimates. Missing postcranium is not represented as original bone.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(HERE.parent));ap.add_argument('--mode',choices=['build','gray','views'],default='build')
A=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(A.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def surf(name,v,f,m,c,mi=None):
 o=mesh_object(name,v,f,m,c)
 if mi is not None:
  for face,i in zip(o.data.polygons,mi):face.material_index=i
 return o
# X, halfwidth, dorsal radius, ventral radius, centre Z in metres.
# Tail -4..-2.4, trunk -2.4..1.2, neck 1.2..2.2, skull 2.2..4.
# Full neck and large triangular jaw frame intentionally differ from slender polycotylids.
BODY=[
(-4.00,.003,.004,.003,-.08),(-3.94,.018,.025,.019,-.08),(-3.84,.041,.055,.041,-.08),(-3.69,.067,.086,.065,-.075),(-3.51,.103,.127,.097,-.065),(-3.31,.144,.170,.132,-.052),(-3.10,.189,.219,.171,-.036),(-2.88,.238,.274,.216,-.018),(-2.64,.293,.332,.269,-.004),(-2.40,.363,.402,.330,.000),
(-2.18,.460,.463,.388,.000),(-1.94,.574,.515,.448,.000),(-1.68,.675,.563,.492,.000),(-1.40,.755,.594,.525,.000),(-1.10,.807,.613,.542,.000),(-.78,.825,.620,.550,.000),(-.46,.816,.614,.548,.000),(-.14,.784,.596,.534,.004),(.18,.731,.566,.507,.012),(.46,.662,.521,.464,.022),(.72,.584,.469,.411,.034),(.96,.519,.425,.366,.046),(1.20,.475,.414,.386,.055),
(1.40,.453,.386,.351,.065),(1.60,.437,.352,.310,.077),(1.80,.427,.317,.268,.087),(2.00,.425,.280,.220,.096),(2.20,.425,.257,.160,.105),
(2.34,.423,.268,.092,.106),(2.48,.405,.275,.069,.101),(2.62,.376,.260,.059,.090),(2.76,.343,.227,.053,.077),(2.90,.308,.184,.050,.061),(3.04,.273,.145,.047,.044),(3.18,.239,.113,.044,.028),(3.32,.205,.089,.041,.014),(3.46,.171,.074,.038,.004),(3.60,.139,.065,.035,-.003),(3.70,.120,.064,.034,-.005),(3.78,.124,.069,.035,-.004),(3.85,.138,.075,.037,-.001),(3.91,.140,.075,.039,.000),(3.96,.104,.065,.038,.000),(3.99,.056,.046,.030,-.001),(4.00,.004,.014,.012,-.002)]
# Closed lower jaw, rotated at the robust posterior joint. Broad oral roof is
# a flesh membrane, not a solid bony palate claim. Healthy restoration is inferred.
JAW=[(2.18,.300,.022,.095,-.047),(2.28,.390,.025,.126,-.051),(2.40,.399,.025,.127,-.054),(2.54,.382,.023,.117,-.058),(2.68,.351,.021,.108,-.062),(2.82,.317,.020,.099,-.066),(2.96,.283,.019,.090,-.069),(3.10,.249,.018,.082,-.072),(3.24,.215,.017,.073,-.074),(3.38,.181,.016,.065,-.075),(3.52,.148,.015,.058,-.075),(3.66,.119,.014,.052,-.075),(3.78,.122,.014,.050,-.074),(3.87,.137,.014,.050,-.072),(3.94,.111,.013,.045,-.071),(3.985,.057,.011,.033,-.069),(3.996,.004,.005,.009,-.066)]
def interp(st,x):
 for a,b in zip(st,st[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);return [a[k]+(b[k]-a[k])*t for k in range(1,len(a))]
 raise ValueError(x)
def rotate_jaw(p):
 x,y,z=p;px,pz=2.23,-.047;a=math.radians(P['jaw_open_degrees'])
 return (px+(x-px)*math.cos(a)+(z-pz)*math.sin(a),y,pz-(x-px)*math.sin(a)+(z-pz)*math.cos(a))
def axial(name,st,c,m,jaw=False):
 n=P['radial_segments'];v=[];f=[];mi=[]
 for x,w,u,d,z in st:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);p=(x,w*math.cos(a),z+(u if s>=0 else d)*s);v.append(rotate_jaw(p) if jaw else p)
 for k in range(len(st)-1):
  for j in range(n):
   f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));s=math.sin(2*math.pi*(j+.5)/n)
   mi.append((1 if s>.15 else 0) if jaw else (0 if s>.42 else 2 if s<-.58 else 1))
 f.extend([tuple(reversed(range(n))),tuple((len(st)-1)*n+j for j in range(n))]);mi.extend([0,0])
 return surf(name,v,f,m,c,mi)
def foil(name,st,sgn,c,m):
 # Along lateral span, elliptical chord sections form thick roots and tapered paddles.
 n=20;v=[];f=[];mi=[]
 for y,x,ch,th,z in st:
  for j in range(n):
   a=2*math.pi*j/n;v.append((x+ch*.5*math.cos(a),sgn*y,z+th*.5*math.sin(a)))
 for k in range(len(st)-1):
  for j in range(n):
   f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)<-.25 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(st)-1)*n+j for j in range(n))]);mi.extend([0,0])
 return surf(name,v,f,m,c,mi)
def body_surface(x,z,s):
 w,u,d,c=interp(BODY,x);return s*w*math.sqrt(max(.0001,1-((z-c)/(u if z>=c else d))**2))
def details(c,m):
 v=[];f=[];n=16;rings=3
 for sign in [-1,1]:
  for name,cx,cz,rx,rz in [('eye',2.76,.176,.045,.033),('naris',3.025,.159,.025,.009)]:
   off=len(v)
   # Two nested surfaces ensure closed outward-facing geometry seated into flesh.
   for layer in [0,1]:
    v.append((cx,body_surface(cx,cz,sign)+sign*(.004 if not layer else -.007),cz))
    for k in range(1,rings+1):
     r=k/rings
     for j in range(n):
      a=2*math.pi*j/n;x=cx+rx*r*math.cos(a);z=cz+rz*r*math.sin(a);y=body_surface(x,z,sign)+sign*((.001+.003*(1-r*r)) if not layer else -.007);v.append((x,y,z))
   step=1+rings*n
   for start in [off,off+step]:
    for j in range(n):f.append((start,start+1+j,start+1+(j+1)%n))
    for k in range(rings-1):
     for j in range(n):f.append((start+1+k*n+j,start+1+(k+1)*n+j,start+1+(k+1)*n+(j+1)%n,start+1+k*n+(j+1)%n))
   for j in range(n):
    k=off+1+(rings-1)*n;f.append((k+j,k+(j+1)%n,k+step+(j+1)%n,k+step+j))
 o=surf('Flesh_seated_eyes_and_nostrils',v,f,m,c)
 for p in o.data.polygons:p.use_smooth=True
 return o

def teeth(c,m):
 v=[];f=[];n=3;count=P['simplified_teeth_per_jaw_side']
 for lower in [False,True]:
  for sign in [-1,1]:
   for i in range(count):
    t=i/(count-1);x=2.60+1.327*t+(0.018 if lower else 0)
    w,u,d,z=interp(JAW if lower else BODY,x);y=sign*w*.87
    zroot=z+(u*math.sqrt(1-.87**2)-.005 if lower else -d*math.sqrt(1-.87**2)+.006)
    # Posterior small crowns, strong maxillary caniniforms, smaller rosette crowns.
    h=.042+.100*math.exp(-((t-.57)/.20)**2)+.025*math.exp(-((t-.94)/.10)**2)
    if lower:h*=.90
    rad=.014+.012*math.exp(-((t-.57)/.23)**2);base=len(v)
    for frac,rf in [(0,1),(.56,.59)]:
     for j in range(n):
      a=2*math.pi*j/n+math.pi/6;pt=(x+rad*rf*math.cos(a)-.010*frac,y+rad*rf*math.sin(a),zroot+(1 if lower else -1)*h*frac);v.append(rotate_jaw(pt) if lower else pt)
    pt=(x-.017,y,zroot+(1 if lower else -1)*h);v.append(rotate_jaw(pt) if lower else pt)
    f.append(tuple(base+j for j in reversed(range(n))))
    for j in range(n):f.append((base+j,base+(j+1)%n,base+n+(j+1)%n,base+n+j));f.append((base+n+j,base+n+(j+1)%n,base+2*n))
 return surf('Simplified_trihedral_heterodont_crowns',v,f,m,c)

def build():
 c=setup_scene(P['asset_id'],P['seed']);root=bpy.data.objects[P['asset_id']]
 root['authoring_forward']='+X';root['mount']='Swimming trunk axial centre';root['taxon']='Pliosaurus carpenteri';root['specimen']='BRSMG Cd6172'
 root['scale_basis']='1.8 m published skull length; about 8 m whole is reconstructed estimate, not complete preserved skeleton measurement.'
 root['fossil_limits']='Only one fairly complete limb, about half vertebrae and fewer than half ribs survive. Skull is crushed and partly restored. No other species supplies the head.'
 root['inference']='Healthy soft tissues, neck muscles, opposite forelimb, hindflippers, missing axial skeleton, tail, skin and palette are reconstructed.'
 m={k:make_material(k,color,.8 if k not in ['detail','tooth'] else .55) for k,color in P['palette'].items()}
 axial('Continuous_broad_trunk_thick_neck_triangular_head_and_tail',BODY,c,[m['dorsum'],m['flank'],m['belly']])
 axial('Robust_broad_lower_jaw_open_12_degrees',JAW,c,[m['belly'],m['oral']],True)
 for s,label in [(-1,'near'),(1,'far')]:
  foil('Foreflipper_'+label,[(.35,.74,.33,.24,-.11),(.51,.74,.42,.25,-.13),(.68,.72,.50,.23,-.155),(.85,.68,.55,.20,-.19),(1.03,.62,.55,.17,-.23),(1.21,.55,.52,.14,-.27),(1.39,.47,.47,.111,-.31),(1.56,.39,.41,.086,-.34),(1.72,.31,.34,.064,-.36),(1.86,.24,.27,.045,-.37),(1.98,.18,.20,.029,-.37),(2.07,.135,.132,.018,-.365),(2.13,.105,.069,.010,-.355),(2.15,.094,.008,.003,-.35)],s,c,[m['dorsum'],m['belly']])
  foil('Reconstructed_hindflipper_'+label,[(.34,-1.94,.34,.23,-.14),(.50,-1.97,.43,.23,-.11),(.66,-2.02,.51,.21,-.075),(.83,-2.08,.55,.18,-.035),(1.01,-2.15,.55,.15,.003),(1.18,-2.22,.51,.12,.037),(1.35,-2.30,.45,.094,.065),(1.51,-2.38,.38,.071,.085),(1.66,-2.45,.31,.052,.095),(1.79,-2.51,.24,.036,.098),(1.90,-2.56,.17,.023,.092),(1.98,-2.60,.105,.014,.080),(2.03,-2.625,.048,.007,.065),(2.05,-2.635,.008,.003,.055)],s,c,[m['dorsum'],m['belly']])
 details(c,m['detail']);teeth(c,m['tooth']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
 return c
EXPORT_OPTIONS=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
def emit(col):
 qa=audit_source(col,P['max_triangles'])
 if qa['errors']:raise RuntimeError(str(qa['errors']))
 bpy.context.scene['asset_author']='Leon Made This / s010s';bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.preferences.filepaths.save_version=0
 for screen in bpy.data.screens:
  for area in screen.areas:
   for space in area.spaces:
    if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'//'
 bpy.context.scene.render.filepath='//';bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
 bpy.ops.object.select_all(action='DESELECT')
 for o in col.all_objects:o.select_set(True)
 bpy.context.view_layer.objects.active=bpy.data.objects[P['asset_id']]
 if set(EXPORT_OPTIONS)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}:raise RuntimeError('Exporter flags unavailable')
 bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**EXPORT_OPTIONS)
 glb=audit_glb(OUT/'model.glb',P['max_triangles'],P['max_materials'],P['max_primitives']);glb['file']='model.glb'
 if glb['errors'] or glb['bytes']>P['max_glb_bytes']:raise RuntimeError(str(glb['errors']))
 b=qa['bounds_blender_m'];expected_min=[b['min'][0],b['min'][2],-b['max'][1]];expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
 delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
 assert delta<.0001 and qa['triangles']==glb['scene_triangles']
 measured=[]
 for o in col.all_objects:
  if o.type!='MESH':continue
  verts=[o.matrix_world@v.co for v in o.data.vertices];lo,hi=_bounds(verts);bm=bmesh.new();bm.from_mesh(o.data);vol=bm.calc_volume(signed=True);bm.free()
  measured.append({'name':o.name,'bounds_blender_m':{'min':list(lo),'max':list(hi),'size':[hi[i]-lo[i] for i in range(3)]},'signed_volume_m3':vol,'positive_transform_determinant':o.matrix_world.determinant()>0})
 write(OUT/'qa/evidence/source-glb.json',{'status':'PASS','source':qa,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'parts_measured':measured,'palette_srgb_hex':P['palette'],'origin':P['origin'],'warning_review':{'mount':'Negative Z is intended around swimming trunk axial mount; no floor contact.','smooth_normals':'Only flesh-seated eye and nostril detail surfaces use smooth normals. Body and four hydrofoils have deliberate facets.','attachments':'Closed flipper roots, lower jaw, teeth and eye/nostril detail meshes overlap at intended anatomical roots; not a boolean printable union.'},'claim_scope':'Source geometry and static GLB integrity only; no independent factual, visual or GPU verdict.'})
 return col

def import_exact():
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
 col=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(col)
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH':
   for c in list(o.users_collection):c.objects.unlink(o)
   col.objects.link(o)
 return col

def render(col,destination,gray=False):
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8 if gray else P['preview']['samples'];scene.cycles.use_denoising=False;scene.cycles.seed=P['seed'];scene.render.threads_mode='FIXED';scene.render.threads=2
 size=448 if gray else P['preview']['resolution'];scene.render.resolution_x=size;scene.render.resolution_y=size;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=not gray
 scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 world=bpy.data.worlds.new('Neutral_studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4;scene.world=world
 if gray:scene.view_layers[0].material_override=make_material('Clay','#A6A6A6')
 points=_vertices_world(col);lo,hi=_bounds(points);center=Vector([(lo[i]+hi[i])/2 for i in range(3)]);span=max(hi[i]-lo[i] for i in range(3))
 for name,direction,energy,size_factor in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5)]:
  d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size_factor*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
 d=bpy.data.cameras.new('Evidence_camera');cam=bpy.data.objects.new('Evidence_camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30
 views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)};rows=[];destination.mkdir(parents=True,exist_ok=True)
 for name,direction in views.items():
  cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points];xmin,xmax=min(p.x for p in proj),max(p.x for p in proj);ymin,ymax=min(p.y for p in proj),max(p.y for p in proj);cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));d.ortho_scale=max(xmax-xmin,ymax-ymin)*1.16;scene.render.filepath=str(destination/(name+'.png'));bpy.ops.render.render(write_still=True)
  rows.append({'path':('private/gray/' if gray else 'views/')+name+'.png','sha256':sha(destination/(name+'.png')),'direction_blender':direction,'camera_position':list(cam.location),'orthographic_scale':d.ortho_scale,'width':size,'height':size})
 if not gray:
  shutil.copyfile(destination/'perspective.png',OUT/'preview.png')
  write(OUT/'qa/evidence/views.json',{'glb_sha256':sha(OUT/'model.glb'),'input':'Clean import of actual delivered GLB, not source scene','engine':'Cycles CPU','gpu_status':'UNKNOWN','samples':scene.cycles.samples,'transparent':True,'view_transform':'Standard','look':'None','views':rows,'preview_sha256':sha(OUT/'preview.png'),'preview_reuses':'views/perspective.png','render_source_sha256':sha(HERE/'generate.py')})
if A.mode=='build':emit(build())
elif A.mode=='gray':render(import_exact(),OUT/'private/gray',True)
else:render(import_exact(),OUT/'views')
