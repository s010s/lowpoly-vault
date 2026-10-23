# SPDX-License-Identifier: MIT
"""Original Ichthyosaurus somersetensis reconstruction, not a fossil scan.
Blender --background --python source/generate.py -- --output DIR
All runtime dependencies are bundled. See brief.json for scientific limits.
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
# Dedicated whole-animal X-axis profile: total 2.68 m, skull region 0.47 m.
# X, half-width, dorsal height, ventral height, Z center. Flesh is inferred.
BODY=[(-1.340,.0015,.003,.003,-.300),(-1.305,.006,.013,.010,-.272),(-1.264,.011,.024,.018,-.235),(-1.215,.017,.033,.026,-.191),(-1.160,.022,.037,.031,-.145),(-1.100,.027,.039,.035,-.098),(-1.035,.032,.041,.038,-.055),(-.970,.036,.043,.041,-.021),(-.900,.039,.046,.043,-.003),(-.800,.044,.055,.051,.002),(-.690,.055,.069,.063,.004),(-.570,.069,.088,.079,.005),(-.440,.087,.111,.099,.007),(-.310,.108,.140,.124,.008),(-.170,.134,.172,.153,.007),(-.020,.156,.198,.179,.004),(.140,.173,.222,.202,.001),(.300,.181,.232,.215,.000),(.450,.176,.223,.216,.000),(.580,.160,.202,.196,.004),(.680,.137,.170,.163,.009),(.770,.111,.134,.121,.015),(.840,.087,.102,.088,.019),(.900,.073,.084,.068,.022),(.960,.061,.067,.052,.024),(1.020,.049,.048,.034,.026),(1.080,.038,.035,.024,.028),(1.140,.028,.026,.019,.030),(1.200,.021,.020,.015,.031),(1.260,.014,.014,.012,.032),(1.310,.007,.008,.008,.032),(1.340,.0015,.003,.003,.032)]
def interp(st,x):
 for a,b in zip(st,st[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);return [a[k]+(b[k]-a[k])*t for k in range(1,len(a))]
 raise ValueError(x)
def body_y(x,z,s):
 w,u,d,c=interp(BODY,x);return s*w*math.sqrt(max(.001,1-((z-c)/(u if z>=c else d))**2))
def body(c,m):
 n=P['radial_segments'];v=[];f=[];mi=[]
 for x,w,u,d,z in BODY:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append((x,w*math.cos(a),z+(u if s>=0 else d)*s))
 for k in range(len(BODY)-1):
  for j in range(n):
   f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));s=math.sin(2*math.pi*(j+.5)/n);mi.append(0 if s>.44 else 2 if s<-.55 else 1)
 f.extend([tuple(reversed(range(n))),tuple((len(BODY)-1)*n+j for j in range(n))]);mi.extend([0,1])
 return surface('Compact_body_upper_skull_and_downturned_tail_axis',v,f,m,c,mi)
def loft(name,st,c,m,axis='z',n=20):
 v=[];f=[]
 for pos,x,ch,th,*z in st:
  for j in range(n):
   a=2*math.pi*j/n;v.append((x+ch/2*math.cos(a),th/2*math.sin(a),pos) if axis=='z' else (x+ch/2*math.cos(a),pos,(z[0] if z else 0)+th/2*math.sin(a)))
 for k in range(len(st)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 f.extend([tuple(reversed(range(n))),tuple((len(st)-1)*n+j for j in range(n))]);return surface(name,v,f,m,c)
def join(parts,name):
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();parts[0].name=name;return parts[0]
def rotate_jaw(p):
 x,y,z=p;a=math.radians(P['jaw_open_degrees']);px,pz=.810,-.058
 return (px+(x-px)*math.cos(a)+(z-pz)*math.sin(a),y,pz-(x-px)*math.sin(a)+(z-pz)*math.cos(a))
JAW=[(.810,.058,.009,.022,-.058),(.860,.066,.010,.026,-.049),(.920,.061,.010,.026,-.038),(.980,.051,.009,.022,-.022),(1.040,.040,.008,.018,-.008),(1.100,.031,.007,.015,.002),(1.160,.024,.006,.012,.009),(1.220,.017,.005,.010,.015),(1.280,.010,.004,.007,.020),(1.325,.004,.0025,.004,.025),(1.33385,.001,.001,.002,.027)]
def jaw(c,m):
 n=24;v=[];f=[];mi=[]
 for x,w,u,d,z in JAW:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append(rotate_jaw((x,w*math.cos(a),z+(u if s>=0 else d)*s)))
 for k in range(len(JAW)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)>.15 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(JAW)-1)*n+j for j in range(n))]);mi.extend([0,0]);return surface('Narrow_lower_jaw_six_degree_opening',v,f,m,c,mi)
def eyes(c,m):
 parts=[]
 for sign,label in [(-1,'near'),(1,'far')]:
  # 55 mm visible eye is smaller than the inferred 105 mm skeletal orbit.
  cx,cz=.970,.045;rx,rz=.0275,.026;n=24;rings=4;v=[];f=[]
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
 return join(parts,'Paired_small_living_eye_apertures')
def teeth(c,m):
 v=[];f=[];n=6;count=P['simplified_teeth_per_jaw_side']
 for lower in [False,True]:
  for side in [-1,1]:
   for k in range(count):
    t=k/(count-1);x=1.002+.309*t+(.002 if lower else 0);w,u,d,z=interp(JAW if lower else BODY,x);y=side*w*.70
    zroot=z+(u*math.sqrt(1-.70**2)-.001 if lower else -d*math.sqrt(1-.70**2)+.001)
    h=.007+.0035*math.sin(math.pi*t);bw=.004+.0012*math.sin(math.pi*t);off=len(v)
    for frac,r in [(0,1),(.57,.61)]:
     for j in range(n):
      a=2*math.pi*j/n;p=(x+bw/2*r*math.cos(a)-.0005*frac,y+bw*.38*r*math.sin(a),zroot+(1 if lower else -1)*h*frac);v.append(rotate_jaw(p) if lower else p)
    p=(x-.0005,y,zroot+(1 if lower else -1)*h);v.append(rotate_jaw(p) if lower else p)
    f.append(tuple(off+j for j in reversed(range(n))))
    for j in range(n):f.append((off+j,off+(j+1)%n,off+n+(j+1)%n,off+n+j));f.append((off+n+j,off+n+(j+1)%n,off+2*n))
 return surface('120_simplified_small_regular_tooth_crowns',v,f,m,c)
def build():
 c=setup_scene(P['asset_id'],P['seed']);r=bpy.data.objects[P['asset_id']];r['authoring_forward']='+X';r['mount']='Swimming axial centre';r['taxon']='Ichthyosaurus somersetensis';r['scale_basis']='2.68 m OR2013 cast; skull 0.47 m; preorbital 0.305 m; not a scan';r['soft_tissues']='Skin, volume, dorsal fin, upper tail lobe, paddle margins and color inferred';r['excluded']='NLMH106234 composite tail and plaster fin restorations not copied'
 m={k:make_material(k,color,.80 if k not in ['detail','tooth'] else .50) for k,color in P['palette'].items()}
 body(c,[m['dorsum'],m['flank'],m['belly']]);jaw(c,[m['belly'],m['oral']])
 loft('Modest_inferred_swept_dorsal_fin',[(.193,.080,.360,.042),(.244,.055,.300,.035),(.300,.010,.218,.027),(.355,-.038,.136,.019),(.400,-.080,.064,.011),(.425,-.105,.009,.003)],c,m['dorsum'])
 for s,label in [(-1,'near'),(1,'far')]:
  loft('Broad_forepaddle_'+label,[(s*.103,.718,.111,.044,-.091),(s*.151,.705,.142,.037,-.108),(s*.211,.681,.150,.030,-.128),(s*.281,.647,.139,.023,-.147),(s*.350,.612,.116,.018,-.161),(s*.414,.580,.079,.012,-.171),(s*.465,.556,.040,.007,-.177),(s*.485,.546,.008,.002,-.179)],c,m['dorsum'],'y')
  loft('Smaller_hindpaddle_'+label,[(s*.077,-.370,.067,.030,-.076),(s*.116,-.389,.083,.026,-.089),(s*.165,-.415,.085,.021,-.103),(s*.215,-.444,.076,.016,-.116),(s*.260,-.471,.059,.011,-.125),(s*.299,-.495,.033,.006,-.132),(s*.314,-.505,.006,.002,-.135)],c,m['dorsum'],'y')
 loft('Inferred_vertical_upper_caudal_lobe',[(.000,-.923,.160,.050),(.063,-.972,.155,.041),(.135,-1.040,.137,.032),(.206,-1.112,.106,.023),(.269,-1.179,.070,.015),(.317,-1.232,.035,.008),(.340,-1.260,.006,.002)],c,m['dorsum'])
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
    record={'status':'PASS','source':qa,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'python_version':sys.version,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'warning_review':{'mount':'Negative Z is intended for a swimming reconstruction with an axial mount.','smooth_normals':'Only the small eye surfaces are smooth; the body and fins are deliberate low-poly facets.','attachments':'Solid closed fin bases and eye/seam details intentionally overlap the body at anatomical roots.'},'claim_scope':'Source geometry and static GLB inspection only; not independent factual review or GPU rendering.'}
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
elif A.mode=='gray':render(build(),OUT/'private/gray',True)
else:render(import_exact(),OUT/'views')
