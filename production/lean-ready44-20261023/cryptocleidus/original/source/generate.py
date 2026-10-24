# SPDX-License-Identifier: MIT
"""Original low-poly Cryptoclidus eurymerus living reconstruction.
Blender --background --python source/generate.py -- --output DIR
Uses only bundled helpers. Paris mount includes restored/cast material. It constrains gross form, not exact soft tissue.
The 5.5 m estimate refers to separate NHM R8575, not the Paris mount.
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
# The 5.5 m silhouette is a published large-individual estimate for NHM R8575.
# Paris photographic anatomy is separate material, not a measured digital twin.
# Neck 2.0 m and skull 0.5 m follow the genus head/neck ratio, with inferred flesh.
# Tail -2.05..-0.95, trunk -0.95..0.95, neck 0.95..2.95, head 2.95..3.45.
BODY=[
(-2.050,.002,.003,.002,-.090),(-2.010,.009,.012,.009,-.091),(-1.950,.021,.027,.021,-.093),(-1.870,.036,.045,.034,-.094),(-1.770,.056,.065,.052,-.092),(-1.650,.080,.093,.075,-.084),(-1.520,.108,.125,.100,-.070),(-1.380,.134,.158,.132,-.051),(-1.240,.154,.193,.163,-.030),(-1.100,.172,.224,.193,-.013),(-.950,.200,.250,.220,.000),
(-.830,.327,.322,.289,.002),(-.680,.456,.390,.342,.006),(-.500,.551,.445,.385,.009),(-.300,.609,.475,.412,.010),(-.080,.625,.480,.420,.009),(.140,.602,.461,.408,.012),(.350,.535,.413,.367,.019),(.530,.426,.337,.302,.031),(.690,.307,.257,.231,.046),(.830,.214,.193,.171,.061),(.950,.160,.155,.143,.072),
(1.080,.149,.145,.132,.076),(1.220,.136,.132,.122,.071),(1.370,.124,.123,.114,.062),(1.520,.114,.117,.107,.055),(1.670,.105,.112,.100,.054),(1.820,.097,.106,.094,.061),(1.970,.091,.099,.089,.075),(2.120,.086,.093,.084,.094),(2.270,.082,.089,.081,.115),(2.420,.079,.086,.078,.135),(2.570,.077,.083,.075,.151),(2.720,.075,.081,.073,.160),(2.850,.075,.079,.070,.165),(2.950,.077,.083,.065,.167),
(2.985,.108,.128,.048,.170),(3.035,.125,.155,.044,.173),(3.095,.122,.144,.039,.175),(3.155,.110,.117,.033,.173),(3.220,.093,.082,.029,.169),(3.280,.076,.058,.026,.165),(3.340,.057,.043,.023,.161),(3.392,.039,.033,.021,.158),(3.430,.023,.025,.018,.156),(3.450,.003,.009,.008,.154)]
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
 return surface('Continuous_round_trunk_neck_triangular_head_and_tail',v,f,m,c,mi)
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
 x,y,z=p;a=math.radians(P['jaw_open_degrees']);px,pz=2.955,.105
 return (px+(x-px)*math.cos(a)+(z-pz)*math.sin(a),y,pz-(x-px)*math.sin(a)+(z-pz)*math.cos(a))
JAW=[(2.945,.073,.015,.038,.104),(2.985,.101,.017,.044,.110),(3.035,.119,.016,.042,.116),(3.095,.115,.014,.037,.120),(3.155,.104,.012,.032,.122),(3.220,.088,.011,.026,.124),(3.280,.071,.009,.021,.125),(3.340,.053,.008,.018,.127),(3.392,.035,.007,.015,.129),(3.430,.019,.005,.011,.131),(3.448,.002,.003,.004,.133)]
def jaw(c,m):
 n=24;v=[];f=[];mi=[]
 for x,w,u,d,z in JAW:
  for j in range(n):
   a=2*math.pi*j/n;s=math.sin(a);v.append(rotate_jaw((x,w*math.cos(a),z+(u if s>=0 else d)*s)))
 for k in range(len(JAW)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(1 if math.sin(2*math.pi*(j+.5)/n)>.20 else 0)
 f.extend([tuple(reversed(range(n))),tuple((len(JAW)-1)*n+j for j in range(n))]);mi.extend([0,0]);return surface('Broad_posterior_tapered_lower_jaw_eight_degree_opening',v,f,m,c,mi)
def eyes(c,m):
 # Fleshed aperture diameter 55 mm; this is not skeletal orbit diameter.
 parts=[]
 for sign,label in [(-1,'near'),(1,'far')]:
  cx,cz=3.105,.228;rx,rz=.0275,.023;n=20;rings=4;v=[];f=[]
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
    t=k/(count-1);x=3.058+.354*t+(.003 if lower else 0);w,u,d,z=interp(JAW if lower else BODY,x);y=side*w*.72
    zroot=z+(u*math.sqrt(1-.72**2)-.0008 if lower else -d*math.sqrt(1-.72**2)+.0007)
    h=.011+.0060*math.sin(math.pi*t);bw=.0037+.0011*math.sin(math.pi*t);off=len(v)
    for frac,r in [(0,1),(.57,.58)]:
     for j in range(n):
      a=2*math.pi*j/n;p=(x+bw/2*r*math.cos(a)-.0004*frac,y+bw*.42*r*math.sin(a),zroot+(1 if lower else -1)*h*frac);v.append(rotate_jaw(p) if lower else p)
    p=(x-.0004,y,zroot+(1 if lower else -1)*h);v.append(rotate_jaw(p) if lower else p)
    f.append(tuple(off+j for j in reversed(range(n))))
    for j in range(n):f.append((off+j,off+(j+1)%n,off+n+(j+1)%n,off+n+j));f.append((off+n+j,off+n+(j+1)%n,off+2*n))
 return surface('Eighty_simplified_slender_tooth_crowns',v,f,m,c)
def build():
 c=setup_scene(P['asset_id'],P['seed']);r=bpy.data.objects[P['asset_id']];r['authoring_forward']='+X';r['mount']='Swimming trunk axial centre';r['taxon']='Cryptoclidus eurymerus';r['scale_basis']='5.5 m author estimate by Paul for NHM R8575, separate from Paris mount and neotype R2860, not a direct measurement';r['soft_tissues']='Flesh, flipper margins, eyes, small teeth and color are inferred';r['pose_basis']='Conservative near-straight neck; Noe et al. 2017 genus head/neck ratio approximately 1:4, ontogenetic variation applies';r['reference_limits']='Paris MNHN fossil-based assembly includes restoration/cast elements, accession and restored fraction unverified; Fig. 4 of Noe 2017 is Muraenosaurus and is not copied'
 m={k:make_material(k,color,.80 if k not in ['detail','tooth'] else .52) for k,color in P['palette'].items()}
 axial(c,[m['dorsum'],m['flank'],m['belly']]);jaw(c,[m['belly'],m['oral']])
 for s,label in [(-1,'near'),(1,'far')]:
  foil('Broad_hydrofoil_foreflipper_'+label,[(.100,.660,.180,.120,-.035),(.250,.660,.300,.170,-.040),(.370,.635,.355,.165,-.055),(.500,.590,.420,.145,-.080),(.640,.545,.456,.122,-.110),(.790,.490,.460,.095,-.144),(.940,.430,.440,.071,-.176),(1.080,.360,.410,.052,-.203),(1.210,.290,.360,.038,-.222),(1.330,.230,.295,.027,-.233),(1.420,.190,.225,.018,-.236),(1.480,.160,.145,.011,-.234),(1.515,.145,.070,.006,-.230),(1.525,.140,.004,.002,-.228)],s,c,[m['dorsum'],m['belly']])
  # A modest raised phase of the hind pair keeps all four hydrofoils legible head-on.
  # This pose is artistic inference, not copied from museum mounting rods.
  foil('Broad_hydrofoil_hindflipper_'+label,[(.230,-.660,.290,.165,-.045),(.350,-.700,.349,.158,-.035),(.480,-.760,.412,.138,-.024),(.620,-.810,.454,.114,-.005),(.770,-.870,.460,.088,.013),(.920,-.930,.439,.066,.026),(1.060,-.995,.400,.049,.033),(1.185,-1.055,.349,.036,.035),(1.295,-1.105,.285,.026,.034),(1.380,-1.140,.215,.018,.030),(1.440,-1.165,.140,.011,.025),(1.476,-1.176,.067,.006,.021),(1.486,-1.180,.004,.002,.019)],s,c,[m['dorsum'],m['belly']])
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
