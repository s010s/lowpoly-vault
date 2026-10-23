# SPDX-License-Identifier: MIT
"""Original Temnodontosaurus platyodon living reconstruction.
Run using Blender --background --python source/generate.py -- --output DIR.
All model dependencies are bundled. Scientific uncertainty is in brief.json.
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
A=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--'in sys.argv else [])
OUT=Path(A.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2)+'\n')
def surface(name,v,f,m,c,indices=None):
 o=mesh_object(name,v,f,m,c)
 if indices:
  for p,i in zip(o.data.polygons,indices):p.material_index=i
 return o
# X, half-width, upper height, lower height, axial Z. New taxon-specific loft.
BODY=[(-3.415,.002,.004,.004,-.72),(-3.34,.014,.028,.027,-.66),(-3.23,.028,.054,.050,-.57),(-3.10,.039,.068,.060,-.45),(-2.94,.049,.077,.070,-.31),(-2.77,.062,.081,.073,-.18),(-2.60,.077,.092,.082,-.075),(-2.42,.092,.104,.095,-.015),(-2.22,.119,.135,.125,.005),(-1.98,.155,.180,.158,.016),(-1.72,.202,.235,.207,.027),(-1.43,.260,.310,.270,.028),(-1.12,.314,.390,.343,.025),(-.79,.365,.456,.414,.018),(-.44,.409,.511,.469,.010),(-.08,.438,.548,.503,.002),(.29,.449,.561,.519,.000),(.65,.439,.550,.522,.002),(.99,.405,.513,.497,.009),(1.27,.355,.453,.438,.018),(1.50,.310,.395,.345,.030),(1.70,.284,.350,.267,.042),(1.87,.263,.308,.205,.053),(2.02,.242,.268,.165,.065),(2.17,.218,.230,.140,.072),(2.33,.187,.192,.127,.077),(2.52,.153,.158,.119,.082),(2.72,.119,.125,.109,.086),(2.92,.086,.094,.097,.089),(3.10,.058,.067,.083,.092),(3.26,.035,.046,.064,.094),(3.36,.017,.026,.040,.096),(3.415,.002,.005,.006,.097)]
def interp(x):
 for a,b in zip(BODY,BODY[1:]):
  if a[0]<=x<=b[0]:
   t=(x-a[0])/(b[0]-a[0]);return [a[k]+(b[k]-a[k])*t for k in range(1,5)]
 raise ValueError(x)
def body_y(x,z,s):
 w,u,d,c=interp(x);return s*w*math.sqrt(max(.001,1-((z-c)/(u if z>=c else d))**2))
def body(c,m):
 n=P['radial_segments'];v=[];f=[];mi=[]
 for x,w,u,d,z in BODY:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append((x,w*math.cos(a),z+(u if s>=0 else d)*s))
 for k in range(len(BODY)-1):
  for j in range(n):
   f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));s=math.sin(2*math.pi*(j+.5)/n);mi.append(0 if s>.43 else 2 if s<-.57 else 1)
 f.extend([tuple(reversed(range(n))),tuple((len(BODY)-1)*n+j for j in range(n))]);mi.extend([0,1])
 return surface('Deep_body_upper_skull_and_downturned_tail_axis',v,f,m,c,mi)
def loft(name,st,c,m,axis='z',n=16):
 v=[];f=[]
 for pos,x,ch,th,*z in st:
  for j in range(n):
   a=2*math.pi*j/n
   v.append((x+ch/2*math.cos(a),th/2*math.sin(a),pos) if axis=='z' else (x+ch/2*math.cos(a),pos,(z[0] if z else 0)+th/2*math.sin(a)))
 for k in range(len(st)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 f.extend([tuple(reversed(range(n))),tuple((len(st)-1)*n+j for j in range(n))]);return surface(name,v,f,m,c)
def join(parts,name):
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();parts[0].name=name;return parts[0]
def rotate_jaw(p):
 x,y,z=p;a=math.radians(P['jaw_open_degrees']);px,pz=1.82,-.125
 return (px+(x-px)*math.cos(a)+(z-pz)*math.sin(a),y,pz-(x-px)*math.sin(a)+(z-pz)*math.cos(a))
JAW=[(1.72,.173,.035,.070,-.140),(1.86,.202,.030,.104,-.140),(2.04,.213,.027,.111,-.133),(2.23,.195,.025,.102,-.113),(2.45,.160,.023,.086,-.096),(2.68,.121,.021,.069,-.078),(2.91,.084,.019,.053,-.059),(3.12,.052,.016,.037,-.039),(3.29,.026,.011,.022,-.018),(3.40,.003,.003,.005,.002)]
def jaw(c,m):
 v=[];f=[];mi=[];n=24
 st=JAW
 for x,w,u,d,z in st:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append(rotate_jaw((x,w*math.cos(a),z+(u if s>=0 else d)*s)))
 for k in range(len(st)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)>.25 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(st)-1)*n+j for j in range(n))]);mi.extend([0,0]);return surface('Robust_lower_jaw_open_twelve_degrees',v,f,m,c,mi)
def ellipsoid(name,center,radii,c,m,n=16,rings=8):
 v=[(center[0],center[1],center[2]+radii[2])];f=[]
 for k in range(1,rings):
  a=math.pi*k/rings
  for j in range(n):
   b=2*math.pi*j/n;v.append((center[0]+radii[0]*math.sin(a)*math.cos(b),center[1]+radii[1]*math.sin(a)*math.sin(b),center[2]+radii[2]*math.cos(a)))
 v.append((center[0],center[1],center[2]-radii[2]));end=len(v)-1
 for j in range(n):f.append((0,1+j,1+(j+1)%n))
 for k in range(rings-2):
  for j in range(n):f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):f.append((end,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
 return surface(name,v,f,m,c)
def eyes(c,m):
 parts=[]
 for sign,label in [(-1,'near'),(1,'far')]:
  cx,cz=2.045,.196;rx,rz=.073,.067;n=24;rings=4;v=[];f=[]
  for level in [0,1]:
   v.append((cx,body_y(cx,cz,sign)+sign*(.006 if level==0 else -.010),cz))
   for k in range(1,rings+1):
    r=k/rings
    for j in range(n):
     a=2*math.pi*j/n;x=cx+rx*r*math.cos(a);z=cz+rz*r*math.sin(a);y=body_y(x,z,sign)+sign*((.0015+.0045*(1-r*r)) if level==0 else -.010);v.append((x,y,z))
  step=1+rings*n
  for off in [0,step]:
   for j in range(n):f.append((off,off+1+j,off+1+(j+1)%n))
   for k in range(rings-1):
    for j in range(n):f.append((off+1+k*n+j,off+1+(k+1)*n+j,off+1+(k+1)*n+(j+1)%n,off+1+k*n+(j+1)%n))
  for j in range(n):f.append((1+(rings-1)*n+j,1+(rings-1)*n+(j+1)%n,step+1+(rings-1)*n+(j+1)%n,step+1+(rings-1)*n+j))
  o=surface('Seated_eye_'+label,v,f,m,c)
  for p in o.data.polygons:p.use_smooth=True
  parts.append(o)
  x,z=2.44,.145;parts.append(ellipsoid('Nostril_'+label,(x,body_y(x,z,sign)+sign*.001,z),(.023,.004,.009),c,m))
 return join(parts,'Paired_flesh_seated_eyes_and_nostrils')
def teeth(c,m):
 v=[];f=[];n=8;count=P['simplified_teeth_per_jaw_side']
 for lower in [False,True]:
  for side in [-1,1]:
   for k in range(count):
    t=k/(count-1);x=2.055+1.26*t+(0.008 if lower else 0);w,u,d,z=interp(x);y=side*w*.68
    zroot=z-d*math.sqrt(1-.68**2)+.009
    if lower:
     for ja,jb in zip(JAW,JAW[1:]):
      if ja[0]<=x<=jb[0]:
       t0=(x-ja[0])/(jb[0]-ja[0]);jw,ju,jd,jz=[ja[ii]+(jb[ii]-ja[ii])*t0 for ii in range(1,5)];y=side*jw*.68;zroot=jz+ju*math.sqrt(1-.68**2)-.006;break
    h=.035+.020*math.sin(math.pi*t)**.7
    bw=.022+.014*math.sin(math.pi*t);depth=bw*.58
    off=len(v)
    for fraction,r in [(0,1),(.50,.78),(.82,.40)]:
     for j in range(n):
      a=2*math.pi*j/n;p=(x+bw/2*r*math.cos(a)-.005*fraction,y+depth/2*r*math.sin(a)-side*.002*fraction,zroot+(1 if lower else -1)*h*fraction)
      v.append(rotate_jaw(p) if lower else p)
    p=(x-.005,y-side*.003,zroot+(1 if lower else -1)*h);v.append(rotate_jaw(p) if lower else p)
    f.append(tuple(off+j for j in reversed(range(n))))
    for ring in range(2):
     for j in range(n):f.append((off+ring*n+j,off+ring*n+(j+1)%n,off+(ring+1)*n+(j+1)%n,off+(ring+1)*n+j))
    for j in range(n):f.append((off+2*n+j,off+2*n+(j+1)%n,off+3*n))
 return surface('112_simplified_broad_based_cutting_crowns',v,f,m,c)
def build():
 c=setup_scene(P['asset_id'],P['seed']);r=bpy.data.objects[P['asset_id']];r['authoring_forward']='+X';r['mount']='Swimming axial centre';r['taxon']='Temnodontosaurus platyodon';r['scale_basis']='6.83 m OR2003 skeletal length; living body thickness and all subordinate proportions inferred';r['comparative_teeth']='IRSNB R122 separate individual; 28 per jaw side is simplified, not a fossil tooth count';r['soft_tissues']='Dorsal fin, tail upper membrane, fleshed eyes and color inferred'
 m={k:make_material(k,color,.78 if k not in ['detail','tooth'] else .48)for k,color in P['palette'].items()}
 body(c,[m['dorsum'],m['flank'],m['belly']]);jaw(c,[m['belly'],m['oral']])
 loft('Modest_inferred_swept_dorsal_fin',[(.460,-.10,1.04,.095),(.560,-.15,.88,.077),(.700,-.24,.62,.059),(.840,-.36,.37,.039),(.960,-.46,.15,.022),(1.025,-.50,.018,.004)],c,m['dorsum'])
 for s,label in [(-1,'near'),(1,'far')]:
  loft('Long_forepaddle_'+label,[(s*.255,1.25,.290,.105,-.263),(s*.390,1.24,.300,.091,-.300),(s*.560,1.20,.292,.073,-.347),(s*.740,1.14,.261,.058,-.393),(s*.910,1.07,.211,.042,-.432),(s*1.070,1.00,.144,.027,-.465),(s*1.200,.95,.065,.014,-.486),(s*1.247,.93,.012,.004,-.490)],c,m['dorsum'],'y')
  loft('Substantial_hindpaddle_'+label,[(s*.207,-1.04,.245,.088,-.237),(s*.330,-1.07,.260,.073,-.275),(s*.480,-1.12,.248,.059,-.314),(s*.640,-1.19,.219,.045,-.353),(s*.790,-1.26,.176,.033,-.388),(s*.920,-1.33,.118,.022,-.414),(s*1.020,-1.38,.052,.011,-.431),(s*1.059,-1.40,.011,.004,-.435)],c,m['dorsum'],'y')
 loft('Inferred_upper_caudal_membrane',[(.005,-2.505,.380,.105),(.135,-2.580,.349,.088),(.295,-2.705,.296,.066),(.455,-2.844,.225,.048),(.600,-2.976,.149,.029),(.715,-3.082,.069,.014),(.755,-3.123,.012,.004)],c,m['dorsum'])
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
    record={'status':'PASS','source':qa,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'export_options':EXPORT_OPTIONS,'warning_review':{'mount':'Negative Z is intended for a swimming reconstruction with an axial mount.','smooth_normals':'Only the small eye surfaces are smooth; the body and fins are deliberate low-poly facets.','attachments':'Solid closed fin bases and eye/seam details intentionally overlap the body at anatomical roots.'},'claim_scope':'Source geometry and static GLB inspection only; not independent factual review or GPU rendering.'}
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
