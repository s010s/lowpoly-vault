# SPDX-License-Identifier: MIT
"""Original whole Dolichorhynchops osborni living reconstruction.
Blender --background --python source/generate.py -- --output DIR
Uses only bundled helpers. KUVP 1300 mount has a plaster skull and exaggerated cervical gaps.
Separate original skull evidence constrains the rostrum, but is crushed and repaired.
Nominal 5.2 m is Paul's uncertain author estimate, not a measured digital twin.
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
# X, half-width, dorsal radius, ventral radius, Z centre in metres.
# Tail -2.20..-1.15, trunk -1.15..1.15, neck 1.15..2.15, head 2.15..3.00.
# The short neck and 0.52 m slender rostrum are inferred flesh targets, not specimen measurements.
# Rounded torso, conservative tapering tail; no unsupported tail crescent or dorsal fin.
BODY=[
(-2.200,.002,.003,.002,-.085),(-2.165,.009,.011,.009,-.086),(-2.100,.022,.026,.021,-.088),(-2.020,.036,.043,.035,-.086),(-1.920,.055,.064,.051,-.080),(-1.800,.079,.092,.074,-.070),(-1.670,.104,.123,.100,-.055),(-1.530,.132,.157,.129,-.037),(-1.390,.156,.193,.162,-.020),(-1.260,.176,.224,.190,-.007),(-1.150,.200,.248,.217,.000),
(-1.000,.315,.315,.281,.001),(-.830,.430,.371,.327,.004),(-.640,.521,.418,.367,.006),(-.430,.578,.447,.393,.007),(-.200,.600,.455,.395,.008),(.030,.597,.446,.392,.010),(.260,.559,.418,.372,.015),(.480,.491,.376,.334,.023),(.670,.403,.319,.287,.034),(.840,.314,.256,.231,.048),(1.000,.255,.217,.195,.059),(1.150,.225,.196,.177,.066),
(1.280,.213,.184,.166,.071),(1.410,.198,.173,.153,.079),(1.540,.181,.164,.141,.091),(1.670,.164,.155,.128,.108),(1.800,.151,.148,.116,.125),(1.930,.142,.143,.106,.140),(2.050,.138,.144,.095,.151),(2.150,.137,.151,.070,.157),
(2.205,.144,.171,.054,.164),(2.270,.145,.184,.047,.169),(2.335,.137,.165,.041,.172),(2.400,.117,.128,.035,.171),(2.470,.092,.083,.030,.166),(2.545,.075,.057,.026,.160),(2.620,.065,.047,.023,.156),(2.695,.057,.041,.022,.153),(2.770,.048,.035,.020,.151),(2.845,.038,.029,.018,.149),(2.910,.029,.025,.016,.148),(2.960,.021,.022,.014,.147),(2.990,.012,.017,.011,.146),(3.000,.003,.010,.007,.145)]
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
 return surface('Continuous_round_trunk_short_neck_long_narrow_rostrum_and_tail',v,f,m,c,mi)
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
 x,y,z=p;a=math.radians(P['jaw_open_degrees']);px,pz=2.155,.091
 return (px+(x-px)*math.cos(a)+(z-pz)*math.sin(a),y,pz-(x-px)*math.sin(a)+(z-pz)*math.cos(a))
JAW=[(2.145,.111,.018,.041,.090),(2.205,.133,.018,.047,.100),(2.270,.137,.016,.046,.111),(2.335,.129,.014,.041,.120),(2.400,.111,.012,.035,.126),(2.470,.088,.011,.028,.127),(2.545,.072,.009,.023,.127),(2.620,.062,.008,.020,.128),(2.695,.054,.007,.018,.128),(2.770,.045,.007,.016,.128),(2.845,.035,.006,.014,.128),(2.910,.026,.005,.012,.129),(2.960,.018,.004,.010,.130),(2.990,.009,.003,.007,.131),(2.998,.002,.002,.003,.132)]
def jaw(c,m):
 n=24;v=[];f=[];mi=[]
 for x,w,u,d,z in JAW:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append(rotate_jaw((x,w*math.cos(a),z+(u if s>=0 else d)*s)))
 for k in range(len(JAW)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)>.20 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(JAW)-1)*n+j for j in range(n))]);mi.extend([0,0]);return surface('Narrow_rostral_lower_jaw_eight_degree_opening',v,f,m,c,mi)
def eyes(c,m):
 # Fleshed aperture is inferred, not the diameter of the crushed skeletal orbit.
 parts=[]
 for sign,label in [(-1,'near'),(1,'far')]:
  cx,cz=2.365,.239;rx,rz=.030,.025;n=20;rings=4;v=[];f=[]
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
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();parts[0].name='Paired_flesh_seated_eye_apertures';return parts[0]
def teeth(c,m):
 # Simplified tiny slender crowns, not an exact species dental count.
 v=[];f=[];n=6;count=P['simplified_teeth_per_jaw_side']
 for lower in [False,True]:
  for side in [-1,1]:
   for k in range(count):
    t=k/(count-1);x=2.389+.580*t+(.002 if lower else 0);w,u,d,z=interp(JAW if lower else BODY,x);y=side*w*.72
    zroot=z+(u*math.sqrt(1-.72**2)-.0008 if lower else -d*math.sqrt(1-.72**2)+.0007)
    h=.019+.012*math.sin(math.pi*t);bw=.0058+.0018*math.sin(math.pi*t);off=len(v)
    for frac,r in [(0,1),(.57,.58)]:
     for j in range(n):
      a=2*math.pi*j/n;p=(x+bw/2*r*math.cos(a)-.0004*frac,y+bw*.42*r*math.sin(a),zroot+(1 if lower else -1)*h*frac);v.append(rotate_jaw(p) if lower else p)
    p=(x-.0004,y,zroot+(1 if lower else -1)*h);v.append(rotate_jaw(p) if lower else p)
    f.append(tuple(off+j for j in reversed(range(n))))
    for j in range(n):f.append((off+j,off+(j+1)%n,off+n+(j+1)%n,off+n+j));f.append((off+n+j,off+n+(j+1)%n,off+2*n))
 return surface('Eighty_eight_simplified_slender_tooth_crowns',v,f,m,c)
def build():
 c=setup_scene(P['asset_id'],P['seed']);r=bpy.data.objects[P['asset_id']]
 r['authoring_forward']='+X';r['mount']='Swimming trunk axial centre';r['taxon']='Dolichorhynchops osborni'
 r['scale_basis']='Nominal 5.2 m is Paul author estimate for KUVP 1300; older 10-foot description differs; actual size unresolved, not a measured digital twin'
 r['soft_tissues']='Flesh, flipper margins and thickness, eye apertures, tooth simplification and color inferred'
 r['reference_limits']='Historical KUVP 1300 mount has plaster head and exaggerated cervical gaps. Separate original skull is laterally crushed and repaired. Other former Dolichorhynchops species are not mixed in.'
 m={k:make_material(k,color,.80 if k not in ['detail','tooth'] else .52) for k,color in P['palette'].items()}
 axial(c,[m['dorsum'],m['flank'],m['belly']]);jaw(c,[m['belly'],m['oral']])
 for s,label in [(-1,'near'),(1,'far')]:
  foil('Strongly_tapering_fore_hydrofoil_'+label,[(.180,.800,.210,.140,-.030),(.320,.790,.290,.165,-.038),(.450,.765,.345,.158,-.055),(.580,.725,.385,.140,-.079),(.720,.670,.400,.117,-.107),(.870,.605,.385,.092,-.139),(1.010,.540,.347,.070,-.168),(1.145,.473,.300,.051,-.194),(1.270,.410,.247,.037,-.216),(1.380,.355,.192,.026,-.231),(1.475,.308,.139,.017,-.240),(1.545,.274,.086,.010,-.244),(1.585,.254,.041,.005,-.244),(1.600,.247,.004,.002,-.242)],s,c,[m['dorsum'],m['belly']])
  # Hind pair in a modest raised stroke phase; four separate hydrofoils remain readable head-on.
  # Pose and fleshed cross sections are artistic inference, not a copy of mounting supports.
  foil('Strongly_tapering_hind_hydrofoil_'+label,[(.220,-.830,.240,.150,-.046),(.350,-.860,.301,.155,-.039),(.480,-.905,.354,.137,-.025),(.620,-.955,.389,.115,-.007),(.765,-1.010,.400,.091,.012),(.910,-1.065,.382,.070,.029),(1.050,-1.120,.342,.052,.043),(1.180,-1.172,.292,.038,.052),(1.295,-1.218,.237,.027,.056),(1.395,-1.259,.182,.018,.054),(1.475,-1.292,.129,.012,.048),(1.535,-1.317,.077,.007,.041),(1.570,-1.332,.036,.004,.035),(1.582,-1.337,.004,.002,.032)],s,c,[m['dorsum'],m['belly']])
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
    record={'status':'PASS','source':qa,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'warning_review':{'mount':'Negative Z is intended for a swimming reconstruction with the trunk axial mounting point.','smooth_normals':'Only the eye surfaces are smooth; the body and fins are deliberate low-poly facets.','attachments':'Solid closed fin bases and eye/seam details intentionally overlap the body at anatomical roots.'},'claim_scope':'Source geometry and static GLB inspection only; not independent factual review or GPU rendering.'}
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
