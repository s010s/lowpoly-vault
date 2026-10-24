# SPDX-License-Identifier: MIT
"""Original low-poly Plesiosaurus dolichodeirus living reconstruction.
Blender --background --python source/generate.py -- --output DIR
Uses only bundled helpers. Photographic bones constrain proportions, not flesh.
"""
from pathlib import Path
import argparse,sys,json,math,hashlib,shutil
import bpy,bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source,_vertices_world,_bounds,_look_at
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(HERE.parent));ap.add_argument('--mode',choices=['build','gray','views'],default='build');ap.add_argument('--view-names',default='front,side,top,perspective')
A=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(A.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def surface(name,v,f,m,c,indices=None):
 o=mesh_object(name,v,f,m,c)
 if indices is not None:
  for p,i in zip(o.data.polygons,indices):p.material_index=i
 return o
# X, half-width, dorsal radius, ventral radius, Z centre.
# The 3.1 m silhouette is a published specimen reconstruction estimate.
# Components and all soft tissue are explicitly inferred, not measurements.
BODY=[
(-.975,.0015,.0025,.0025,-.045),(-.947,.006,.008,.007,-.046),(-.905,.013,.015,.014,-.048),(-.850,.022,.025,.022,-.048),(-.785,.034,.036,.032,-.043),(-.710,.047,.049,.043,-.035),(-.635,.060,.065,.056,-.023),(-.560,.077,.085,.073,-.010),(-.475,.105,.110,.097,.000),
(-.400,.170,.145,.139,.000),(-.300,.239,.180,.172,.002),(-.180,.287,.198,.190,.003),(-.050,.310,.205,.195,.003),(.080,.305,.200,.192,.004),(.200,.278,.180,.175,.009),(.300,.235,.155,.145,.016),(.385,.170,.123,.110,.028),(.475,.095,.090,.084,.040),
(.555,.084,.080,.073,.043),(.645,.075,.071,.064,.040),(.745,.067,.064,.058,.034),(.845,.060,.059,.054,.029),(.945,.056,.055,.051,.027),(1.045,.052,.052,.048,.029),(1.145,.049,.050,.045,.033),(1.245,.046,.048,.042,.039),(1.345,.044,.046,.040,.048),(1.445,.042,.045,.039,.058),(1.545,.040,.043,.038,.069),(1.645,.039,.041,.037,.079),(1.745,.038,.039,.037,.087),(1.825,.0375,.038,.037,.093),(1.895,.039,.040,.035,.097),
(1.925,.050,.045,.026,.101),(1.955,.055,.049,.022,.103),(1.990,.051,.046,.020,.102),(2.025,.045,.037,.017,.099),(2.060,.038,.026,.014,.096),(2.090,.030,.020,.013,.094),(2.112,.019,.014,.011,.092),(2.125,.003,.006,.006,.091)]
def interp(st,x):
 for a,b in zip(st,st[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);return [a[k]+(b[k]-a[k])*t for k in range(1,len(a))]
 raise ValueError(x)
def body_y(x,z,s):
 w,u,d,c=interp(BODY,x);return s*w*math.sqrt(max(.001,1-((z-c)/(u if z>=c else d))**2))
def axial(c,m):
 n=P['radial_segments'];v=[];f=[];mi=[]
 for x,w,u,d,z in BODY:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append((x,w*math.cos(a),z+(u if s>=0 else d)*s))
 for k in range(len(BODY)-1):
  for j in range(n):
   f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));s=math.sin(2*math.pi*(j+.5)/n);mi.append(0 if s>.40 else 2 if s<-.55 else 1)
 f.extend([tuple(reversed(range(n))),tuple((len(BODY)-1)*n+j for j in range(n))]);mi.extend([0,1])
 return surface('Continuous_short_tail_broad_trunk_long_neck_small_upper_skull',v,f,m,c,mi)
def foil(name,st,sign,c,m):
 # Elliptic foil sections: y-distance, x-centre, chord, thickness, z-centre.
 # Both pairs use tapered rounded tips, broad flesh roots and no separate digits.
 n=20;v=[];f=[];mi=[]
 for y,x,ch,th,z in st:
  for j in range(n):
   a=2*math.pi*j/n;v.append((x+ch/2*math.cos(a),sign*y,z+th/2*math.sin(a)))
 for k in range(len(st)-1):
  for j in range(n):
   f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)<-.30 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(st)-1)*n+j for j in range(n))]);mi.extend([0,0])
 return surface(name,v,f,m,c,mi)
def rotate_jaw(p):
 x,y,z=p;a=math.radians(P['jaw_open_degrees']);px,pz=1.900,.074
 return (px+(x-px)*math.cos(a)+(z-pz)*math.sin(a),y,pz-(x-px)*math.sin(a)+(z-pz)*math.cos(a))
JAW=[(1.895,.036,.008,.018,.071),(1.925,.046,.009,.021,.078),(1.955,.052,.008,.020,.082),(1.990,.048,.007,.019,.082),(2.025,.042,.006,.016,.081),(2.060,.035,.005,.013,.081),(2.090,.027,.004,.010,.081),(2.112,.016,.003,.007,.082),(2.123,.002,.002,.003,.083)]
def jaw(c,m):
 n=24;v=[];f=[];mi=[]
 for x,w,u,d,z in JAW:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append(rotate_jaw((x,w*math.cos(a),z+(u if s>=0 else d)*s)))
 for k in range(len(JAW)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)>.20 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(JAW)-1)*n+j for j in range(n))]);mi.extend([0,0]);return surface('Narrow_lower_jaw_eight_degree_opening',v,f,m,c,mi)
def eyes(c,m):
 # Fleshed aperture diameter 23 mm; this is not skeletal orbit diameter.
 parts=[]
 for sign,label in [(-1,'near'),(1,'far')]:
  cx,cz=1.963,.124;rx,rz=.0115,.010;n=20;rings=4;v=[];f=[]
  for level in [0,1]:
   v.append((cx,body_y(cx,cz,sign)+sign*(.002 if level==0 else -.004),cz))
   for k in range(1,rings+1):
    r=k/rings
    for j in range(n):
     a=2*math.pi*j/n;x=cx+rx*r*math.cos(a);z=cz+rz*r*math.sin(a);y=body_y(x,z,sign)+sign*((.0005+.0015*(1-r*r)) if level==0 else -.004);v.append((x,y,z))
  step=1+rings*n
  for off in [0,step]:
   for j in range(n):f.append((off,off+1+j,off+1+(j+1)%n))
   for k in range(rings-1):
    for j in range(n):f.append((off+1+k*n+j,off+1+(k+1)*n+j,off+1+(k+1)*n+(j+1)%n,off+1+k*n+(j+1)%n))
  for j in range(n):f.append((1+(rings-1)*n+j,1+(rings-1)*n+(j+1)%n,step+1+(rings-1)*n+(j+1)%n,step+1+(rings-1)*n+j))
  o=surface('Flesh_seated_eye_'+label,v,f,m,c)
  for p in o.data.polygons:p.use_smooth=True
  parts.append(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();parts[0].name='Paired_small_eye_apertures';return parts[0]
def teeth(c,m):
 # Simplified tiny slender crowns, not an exact species dental count.
 v=[];f=[];n=6;count=P['simplified_teeth_per_jaw_side']
 for lower in [False,True]:
  for side in [-1,1]:
   for k in range(count):
    t=k/(count-1);x=1.953+.153*t+(.0017 if lower else 0);w,u,d,z=interp(JAW if lower else BODY,x);y=side*w*.72
    zroot=z+(u*math.sqrt(1-.72**2)-.0008 if lower else -d*math.sqrt(1-.72**2)+.0007)
    h=.004+.0020*math.sin(math.pi*t);bw=.0017+.0008*math.sin(math.pi*t);off=len(v)
    for frac,r in [(0,1),(.57,.58)]:
     for j in range(n):
      a=2*math.pi*j/n;p=(x+bw/2*r*math.cos(a)-.0004*frac,y+bw*.42*r*math.sin(a),zroot+(1 if lower else -1)*h*frac);v.append(rotate_jaw(p) if lower else p)
    p=(x-.0004,y,zroot+(1 if lower else -1)*h);v.append(rotate_jaw(p) if lower else p)
    f.append(tuple(off+j for j in reversed(range(n))))
    for j in range(n):f.append((off+j,off+(j+1)%n,off+n+(j+1)%n,off+n+j));f.append((off+n+j,off+n+(j+1)%n,off+2*n))
 return surface('Eighty_simplified_slender_tooth_crowns',v,f,m,c)
def build():
 c=setup_scene(P['asset_id'],P['seed']);r=bpy.data.objects[P['asset_id']];r['authoring_forward']='+X';r['mount']='Swimming trunk axial centre';r['taxon']='Plesiosaurus dolichodeirus';r['scale_basis']='NHMUK PV OR22656: 3.1 m published estimate by Paul, not direct measurement';r['soft_tissues']='Flesh, flipper margins, eyes, small teeth and color are inferred';r['pose_basis']='Conservative near-straight neck; cross-genera neck research is not a motion test of this species'
 m={k:make_material(k,color,.80 if k not in ['detail','tooth'] else .52) for k,color in P['palette'].items()}
 axial(c,[m['dorsum'],m['flank'],m['belly']]);jaw(c,[m['belly'],m['oral']])
 for s,label in [(-1,'near'),(1,'far')]:
  foil('Substantial_foreflipper_'+label,[(.100,.300,.150,.090,-.040),(.180,.330,.176,.093,-.040),(.240,.322,.204,.075,-.055),(.310,.301,.214,.056,-.075),(.390,.270,.202,.040,-.098),(.470,.231,.179,.029,-.117),(.550,.187,.147,.021,-.130),(.620,.147,.112,.015,-.138),(.680,.112,.077,.011,-.142),(.730,.086,.042,.007,-.143),(.758,.075,.015,.0035,-.142),(.765,.073,.003,.0015,-.142)],s,c,[m['dorsum'],m['belly']])
  foil('Substantial_hindflipper_'+label,[(.080,-.300,.140,.080,-.050),(.160,-.330,.157,.084,-.050),(.220,-.347,.186,.067,-.064),(.290,-.372,.195,.050,-.083),(.365,-.404,.187,.037,-.102),(.440,-.442,.167,.027,-.118),(.510,-.482,.136,.020,-.129),(.570,-.519,.103,.014,-.134),(.625,-.552,.072,.010,-.135),(.671,-.579,.039,.0065,-.134),(.698,-.592,.014,.0032,-.131),(.705,-.594,.003,.0015,-.130)],s,c,[m['dorsum'],m['belly']])
 eyes(c,m['detail']);teeth(c,m['tooth']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
 return c
EXPORT_OPTIONS=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)

def emit(col):
    qa=audit_source(col,P['max_triangles'])
    if qa['errors']:raise RuntimeError(str(qa['errors']))
    bpy.context.scene['asset_author']='Leon Made This / s010s'; bpy.context.scene['asset_license']='CC-BY-4.0'
    bpy.context.preferences.filepaths.save_version=0
    # Remove inherited file-browser directory hints from the editable deliverable.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type == 'FILE_BROWSER' and space.params:
                    space.params.directory = b'//'
    bpy.context.scene.render.filepath = '//'
    bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[P['asset_id']]
    if set(EXPORT_OPTIONS)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}:raise RuntimeError('Exporter flags unavailable')
    bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**EXPORT_OPTIONS)
    glb=audit_glb(OUT/'model.glb',P['max_triangles'],P['max_materials'],P['max_primitives'])
    glb['file']='model.glb'
    if glb['errors'] or glb['bytes']>P['max_glb_bytes']:raise RuntimeError(str(glb['errors']))
    b=qa['bounds_blender_m']; expected_min=[b['min'][0],b['min'][2],-b['max'][1]]; expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
    assert delta<.0001 and qa['triangles']==glb['scene_triangles']
    record={'status':'PASS','source':qa,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'warning_review':{'mount':'Negative Z is intended for a swimming reconstruction with the trunk axial mounting point.','smooth_normals':'Only the small eye surfaces are smooth; the body and fins are deliberate low-poly facets.','attachments':'Solid closed fin bases and eye/seam details intentionally overlap the body at anatomical roots.'},'claim_scope':'Source geometry and static GLB inspection only; not independent factual review or GPU rendering.'}
    measured=[]
    for obj in col.all_objects:
        if obj.type!='MESH':continue
        verts=[obj.matrix_world@v.co for v in obj.data.vertices];lo,hi=_bounds(verts)
        bm=bmesh.new();bm.from_mesh(obj.data);volume=bm.calc_volume(signed=True);bm.free()
        measured.append({'name':obj.name,'bounds_blender_m':{'min':list(lo),'max':list(hi),'size':[hi[i]-lo[i] for i in range(3)]},'signed_volume_m3':volume,'positive_transform_determinant':obj.matrix_world.determinant()>0})
    record['parts_measured']=measured
    record['palette_srgb_hex']=P['palette']
    record['origin']=P['origin']
    write(OUT/'qa/evidence/source-glb.json',record)
    return col

def import_exact():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    col=bpy.data.collections.new('EXACT_GLB'); bpy.context.scene.collection.children.link(col)
    for o in list(bpy.context.scene.objects):
        if o.type=='MESH':
            for c in list(o.users_collection):c.objects.unlink(o)
            col.objects.link(o)
    return col

def render(col, destination, gray=False):
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=8 if gray else P['preview']['samples']; scene.cycles.use_denoising=False; scene.cycles.seed=P['seed']
    scene.render.threads_mode='FIXED';scene.render.threads=2
    size=448 if gray else P['preview']['resolution']; scene.render.resolution_x=size;scene.render.resolution_y=size;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=not gray
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral_studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4;scene.world=world
    if gray:scene.view_layers[0].material_override=make_material('Clay','#A6A6A6')
    points=_vertices_world(col); low,high=_bounds(points);center=Vector([(low[i]+high[i])/2 for i in range(3)]);span=max(high[i]-low[i] for i in range(3))
    for name,direction,energy,size_factor in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),180,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*span*span/4;d.shape='DISK';d.size=size_factor*span/2;o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*span/2;_look_at(o,center)
    d=bpy.data.cameras.new('Evidence_camera');cam=bpy.data.objects.new('Evidence_camera',d);scene.collection.objects.link(cam);scene.camera=cam;d.type='ORTHO';d.clip_start=.001;d.clip_end=span*30
    views={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':(1,-1,1)}
    rows=[];destination.mkdir(parents=True,exist_ok=True)
    for name,direction in views.items():
        if name not in A.view_names.split(','):continue
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points]
        width=max(p.x for p in proj)-min(p.x for p in proj);height=max(p.y for p in proj)-min(p.y for p in proj)
        shift=Vector(((max(p.x for p in proj)+min(p.x for p in proj))/2,(max(p.y for p in proj)+min(p.y for p in proj))/2,0));cam.location+=cam.matrix_world.to_3x3()@shift
        d.ortho_scale=max(width,height)*1.18;scene.render.filepath=str(destination/(name+'.png'));bpy.ops.render.render(write_still=True)
        rows.append({'path':('private/gray/' if gray else 'views/')+name+'.png','sha256':sha(destination/(name+'.png')),'direction_blender':direction,'camera_position':list(cam.location),'orthographic_scale':d.ortho_scale,'width':size,'height':size})
    if not gray:
        shutil.copyfile(destination/'perspective.png',OUT/'preview.png')
        write(OUT/'qa/evidence/views.json',{'glb_sha256':sha(OUT/'model.glb'),'input':'Clean import of the actual delivered GLB, not source geometry','engine':'Cycles CPU','gpu_status':'UNKNOWN','samples':scene.cycles.samples,'transparent':True,'view_transform':'Standard','look':'None','views':rows,'preview_sha256':sha(OUT/'preview.png'),'preview_reuses':'views/perspective.png','render_source_sha256':sha(HERE/'generate.py')})

if A.mode=='build':emit(build())
elif A.mode=='gray':render(import_exact(),OUT/'private/gray',True)
else:render(import_exact(),OUT/'views')
