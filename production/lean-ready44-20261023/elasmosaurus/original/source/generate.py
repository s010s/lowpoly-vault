# SPDX-License-Identifier: MIT
"""Original low-poly Elasmosaurus platyurus whole living reconstruction.
Blender --background --python source/generate.py -- --output DIR
Uses only bundled helpers. ANSP 10081 is incomplete: preserved jaws and neck
anchor the original extreme-neck gate. Rear skull, trunk breadth and all four
limbs are explicitly comparative inference, not a complete original skeleton.
Total 10.5 m and neck 7 m are nominal reconstructed scale choices.
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
# Axial stations (X, half-width, upper radius, lower radius, Z centre).
# Tail -2.025..-1.025; trunk -1.025..1.025; neck 1.025..8.025;
# head 8.025..8.475. 10.5 m total and 7 m neck are NOMINAL INFERENCE,
# not a measurement of a complete original specimen. All flesh is inferred.
BODY=[
(-2.025,.002,.003,.002,-.065),(-1.995,.009,.012,.009,-.066),
(-1.940,.021,.027,.021,-.066),(-1.865,.039,.047,.035,-.063),
(-1.770,.062,.073,.057,-.058),(-1.655,.089,.105,.084,-.050),
(-1.525,.121,.143,.116,-.041),(-1.390,.155,.185,.153,-.030),
(-1.255,.188,.226,.190,-.017),(-1.135,.220,.263,.224,-.008),
(-1.025,.245,.285,.244,.000),(-.905,.361,.362,.318,.005),
(-.755,.496,.435,.388,.009),(-.565,.615,.505,.446,.012),
(-.345,.694,.548,.487,.013),(-.105,.725,.557,.493,.015),
(.140,.704,.537,.480,.020),(.365,.642,.488,.440,.029),
(.560,.543,.419,.378,.041),(.720,.426,.339,.303,.056),
(.855,.322,.269,.239,.072),(.955,.264,.232,.208,.085),
(1.025,.240,.225,.205,.090)]
# Many low-curvature stations make a continuous fleshed tube rather than beads.
# The 72-vertebra revision informs scientific identity, not visible skin segments.
for i in range(1,51):
 t=i/50; x=1.025+7*t
 w=.075+.165*(1-t)**1.65
 z=.09-.16*math.sin(math.pi*t)+.105*t*t
 BODY.append((x,w,w*.98+.003,w*.89+.002,z))
BODY.extend([
(8.055,.096,.104,.047,.198),(8.100,.115,.140,.045,.202),
(8.155,.112,.133,.040,.204),(8.215,.100,.105,.034,.202),
(8.275,.084,.072,.029,.199),(8.335,.067,.051,.025,.195),
(8.390,.049,.038,.022,.191),(8.435,.032,.030,.020,.188),
(8.463,.017,.023,.017,.186),(8.475,.002,.008,.006,.185)])
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
 return surface('Extreme_neck_short_broad_trunk_and_conservative_tail',v,f,m,c,mi)
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
 x,y,z=p;a=math.radians(P['jaw_open_degrees']);px,pz=8.030,.138
 return (px+(x-px)*math.cos(a)+(z-pz)*math.sin(a),y,pz-(x-px)*math.sin(a)+(z-pz)*math.cos(a))
JAW=[(8.020,.073,.014,.035,.137),(8.055,.090,.016,.039,.141),
(8.100,.109,.016,.040,.148),(8.155,.106,.014,.035,.151),
(8.215,.094,.012,.030,.153),(8.275,.079,.010,.025,.155),
(8.335,.063,.009,.020,.157),(8.390,.045,.008,.017,.159),
(8.435,.028,.006,.014,.160),(8.463,.013,.004,.009,.161),
(8.473,.002,.003,.003,.163)]
def jaw(c,m):
 n=24;v=[];f=[];mi=[]
 for x,w,u,d,z in JAW:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append(rotate_jaw((x,w*math.cos(a),z+(u if s>=0 else d)*s)))
 for k in range(len(JAW)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)>.20 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(JAW)-1)*n+j for j in range(n))]);mi.extend([0,0]);return surface('Broad_posterior_tapered_lower_jaw_eight_degree_opening',v,f,m,c,mi)
def eyes(c,m):
 # Fleshed aperture diameter 38 mm; this is not skeletal orbit diameter.
 parts=[]
 for sign,label in [(-1,'near'),(1,'far')]:
  cx,cz=8.164,.253;rx,rz=.019,.017;n=20;rings=4;v=[];f=[]
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
 # Simplified 20 crowns per jaw side. The six anterior upper positions are
 # a premaxillary representation supported by the target fragment; posterior
 # completion and the full visible row are NOT a complete fossil tooth formula.
 v=[];f=[];n=6;count=P['simplified_teeth_per_jaw_side']
 for lower in [False,True]:
  for side in [-1,1]:
   for k in range(count):
    t=k/(count-1);x=((8.130+.200*k/13) if k<14 else (8.350+.095*(k-14)/5))+(.002 if lower else 0);w,u,d,z=interp(JAW if lower else BODY,x);y=side*w*.72
    zroot=z+(u*math.sqrt(1-.72**2)-.0008 if lower else -d*math.sqrt(1-.72**2)+.0007)
    h=.015+.010*math.sin(math.pi*t/2);bw=.0038+.0010*math.sin(math.pi*t);off=len(v)
    for frac,r in [(0,1),(.50,.64),(.82,.29)]:
     for j in range(n):
      a=2*math.pi*j/n;p=(x+bw/2*r*math.cos(a)-.0040*frac*frac,y+bw*.42*r*math.sin(a),zroot+(1 if lower else -1)*h*frac);v.append(rotate_jaw(p) if lower else p)
    p=(x-.0040,y,zroot+(1 if lower else -1)*h);v.append(rotate_jaw(p) if lower else p)
    f.append(tuple(off+j for j in reversed(range(n))))
    for ring in range(2):
     for j in range(n):f.append((off+ring*n+j,off+ring*n+(j+1)%n,off+(ring+1)*n+(j+1)%n,off+(ring+1)*n+j))
    for j in range(n):f.append((off+2*n+j,off+2*n+(j+1)%n,off+3*n))
 return surface('Eighty_simplified_slender_recurved_tooth_crowns',v,f,m,c)
def build():
 c=setup_scene(P['asset_id'],P['seed']);r=bpy.data.objects[P['asset_id']]
 r['authoring_forward']='+X';r['mount']='Swimming trunk axial centre'
 r['taxon']='Elasmosaurus platyurus'
 r['scale_basis']='10.5 m total and 7.0 m neck are nominal reconstructed targets, not complete-specimen measurements; ANSP 10081 centrum measurements and historical neck estimate anchor scale'
 r['neck_evidence']='72 cervicals follows Sachs, Kear and Everhart 2013 revision, superseding the 2005 count of 71; a continuous fleshed surface does not expose vertebral segments'
 r['preservation_limits']='Original jaw fragments and almost complete cervical series; incomplete trunk/tail and ribs; historically documented girdles now lost; limbs not preserved'
 r['posterior_skull']='Conservative same-family completion; not an original preserved Elasmosaurus rear skull'
 r['trunk_width']='Fleshed short broad ribcage width/depth inferred from comparative elasmosaurid anatomy; not measured original torso flesh'
 r['four_limbs']='All four hydrofoils inferred from same-family Thalassomedon; not claimed Elasmosaurus limb fossils'
 r['comparative_source_limits']='Thalassomedon 1940 restored original mount and modern replica are distinct; no entire comparator neck ratio or genus-specific rostral ridge copied'
 r['soft_tissues']='Flesh, eyes, jaw pose, simplified tooth completion and all color are inferred'
 m={k:make_material(k,color,.80 if k not in ['detail','tooth'] else .52) for k,color in P['palette'].items()}
 axial(c,[m['dorsum'],m['flank'],m['belly']]);jaw(c,[m['belly'],m['oral']])
 for s,label in [(-1,'near'),(1,'far')]:
  # Closed roots are deliberately buried in shoulder flesh, without visible limb bones.
  foil('Comparatively_inferred_fore_hydrofoil_'+label,[
   (.220,.720,.210,.145,-.030),(.360,.700,.300,.175,-.040),
   (.490,.670,.365,.162,-.059),(.640,.620,.420,.141,-.085),
   (.800,.555,.452,.118,-.116),(.970,.485,.460,.094,-.150),
   (1.140,.410,.435,.071,-.182),(1.300,.335,.393,.052,-.211),
   (1.445,.265,.339,.037,-.233),(1.570,.205,.275,.026,-.247),
   (1.670,.158,.207,.018,-.251),(1.740,.125,.137,.011,-.250),
   (1.783,.105,.067,.006,-.246),(1.798,.099,.004,.002,-.243)
  ],s,c,[m['dorsum'],m['belly']])
  # A small separate stroke phase makes both inferred pairs visible head-on.
  foil('Comparatively_inferred_hind_hydrofoil_'+label,[
   (.250,-.735,.270,.170,-.025),(.380,-.765,.335,.163,-.016),
   (.520,-.810,.398,.142,-.001),(.675,-.865,.441,.118,.018),
   (.840,-.930,.460,.094,.039),(1.005,-.995,.442,.071,.058),
   (1.160,-1.055,.404,.052,.071),(1.300,-1.110,.350,.037,.077),
   (1.425,-1.160,.287,.026,.076),(1.525,-1.201,.219,.018,.071),
   (1.599,-1.232,.145,.011,.063),(1.645,-1.251,.071,.006,.056),
   (1.660,-1.257,.004,.002,.051)
  ],s,c,[m['dorsum'],m['belly']])
 eyes(c,m['detail']);teeth(c,m['tooth'])
 bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
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
