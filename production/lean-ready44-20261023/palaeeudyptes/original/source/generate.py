# SPDX-License-Identifier: MIT
"""Original bounded Palaeeudyptes whole-body reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
Body, bill, paddles, posture and plumage are an artistic reconstruction, not a fossil mesh.
Generation reads only adjacent params and declared relative helpers.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
S=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=S.parent);a=ap.parse_args(args)
O=a.output.resolve();O.mkdir(parents=True,exist_ok=True)
P=json.loads((S/'params.json').read_text())
assert bpy.app.version_string=='4.3.2', 'This source is pinned to Blender 4.3.2'
C=setup_scene(P['asset_id'],P['seed']);scene=bpy.context.scene
scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.filepath=''
M={key:make_material('palaeeudyptes-'+key,color,roughness=.84 if key!='eye' else .32) for key,color in P['palette_srgb'].items()}
root=bpy.data.objects[C['asset_root']]
root['representation']='living reconstruction'
root['factual_scope']='MLP12-I-20-289 postcranium; skull and whole external form not preserved.'
root['standing_height_status']='1.10 m original pose estimate; not published 1.332-1.432 m total-length estimate.'
root['bill_scope']='Long spear bill comparative inference only; no reliably associated genus skull.'

# Single continuous bilateral loft. The lower-body oval narrows into a long neck,
# then a small, lengthened head. Boundary-aware rings make a clean ventral field.
# z, half-width, half-depth, center y, pale-plumage half-angle.
sections=[(.09,.050,.065,.035,55),(.145,.086,.093,.035,68),(.22,.127,.127,.032,75),
(.31,.160,.152,.025,78),(.41,.178,.171,.014,80),(.51,.180,.176,.005,80),
(.61,.165,.164,-.008,77),(.70,.140,.141,-.025,73),(.77,.112,.116,-.041,67),
(.83,.086,.092,-.056,60),(.885,.063,.073,-.073,52),(.93,.049,.060,-.093,42),
(.965,.044,.055,-.112,31),(1.00,.043,.054,-.129,23),(1.028,.046,.059,-.143,15),
(1.050,.047,.061,-.147,0),(1.073,.042,.054,-.146,0),
(1.090,.030,.039,-.143,0),(1.098,.013,.019,-.140,0)]
N=32;V=[];F=[];material_indices=[]
for z,rx,ry,cy,pale in sections:
    edge=math.radians(max(pale,15))
    for j in range(N):
        q=min(j,N-j)
        angle=q/7*edge if q<=7 else edge+(math.pi-edge)*(q-7)/(N/2-7)
        if j>N/2: angle=-angle
        V.append((rx*math.sin(angle),cy-ry*math.cos(angle),z))
for k in range(len(sections)-1):
    for j in range(N):
        F.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
        material_indices.append(1 if k<=13 and (j<7 or j>=N-7) else 0)
V.extend([(0,.035,.079),(0,-.140,1.10)])
for j in range(N):
    F.append((len(V)-2,(j+1)%N,j));material_indices.append(0)
    F.append((len(V)-1,(len(sections)-1)*N+j,(len(sections)-1)*N+(j+1)%N));material_indices.append(0)
body=mesh_object('continuous-body-neck-head',V,F,[M['back'],M['belly']],C)
for poly,idx in zip(body.data.polygons,material_indices): poly.material_index=idx
body['anatomy_status']='Original soft-tissue loft, no digital tracing of published schematic.'

# Closed long, straight, narrow spear bill. Upper and lower sheaths converge;
# the small separation is a readable mouth seam, not an open mouth or tooth row.
def bill(lower):
    v=[];f=[]
    for y,w,z,h in [(-.186,.024,1.047,.015),(-.211,.021,1.050,.013),(-.258,.0165,1.056,.0105),(-.313,.0105,1.063,.0075),(-.369,.005,1.070,.0038),(-.406,.0011,1.074,.0010)]:
        if lower:
            ring=[(-w,y,z-.0003),(-w*.70,y,z-h*.65),(w*.70,y,z-h*.65),(w,y,z-.0003)]
        else:
            ring=[(-w,y,z+.0005),(-w*.48,y,z+h),(w*.48,y,z+h),(w,y,z+.0005)]
        v.extend(ring)
    for k in range(5):
        for j in range(4):f.append((k*4+j,k*4+(j+1)%4,(k+1)*4+(j+1)%4,(k+1)*4+j))
    f.extend([tuple(reversed(range(4))),tuple(20+j for j in range(4))])
    ob=mesh_object('lower-spear-mandible' if lower else 'upper-spear-bill',v,f,M['bill_feet'],C)
    ob['scientific_limit']='Length 0.22 m is an original estimate; comparative stem-penguin bill, not associated Palaeeudyptes fossil.'
bill(False);bill(True)

# Small deliberately faceted eyes. This utility is restricted to minor parts,
# rather than assembling the principal form from stock spheres.
def ellipsoid(name,c,r,mat,n=12,kmax=5):
    v=[(c[0],c[1],c[2]-r[2])];f=[]
    for k in range(1,kmax):
        a=-math.pi/2+math.pi*k/kmax
        for j in range(n):
            t=2*math.pi*j/n
            v.append((c[0]+r[0]*math.cos(a)*math.cos(t),c[1]+r[1]*math.cos(a)*math.sin(t),c[2]+r[2]*math.sin(a)))
    v.append((c[0],c[1],c[2]+r[2]))
    for j in range(n):
        f.append((0,1+(j+1)%n,1+j));f.append((len(v)-1,1+(kmax-2)*n+j,1+(kmax-2)*n+(j+1)%n))
    for k in range(kmax-2):
        for j in range(n):f.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
    return mesh_object(name,v,f,mat,C)

# Rolled, abducted paddle flippers: .39 m centerline, .13 m widest chord,
# .018 m maximum exposed blade thickness. No feather fingers or round rods.
chord=Vector((.42,-.84,.34)).normalized()
axis=Vector((.25,.045,-.30)).normalized()
normal=axis.cross(chord).normalized()
chord=normal.cross(axis).normalized()
for side,sign in [('left',1),('right',-1)]:
    ellipsoid(side+'-eye',(sign*.043,-.170,1.066),(.0063,.0078,.007),M['eye'])
    start=Vector((.133,-.006,.766))
    wing_sections=[(0,.025,.018),(.045,.050,.016),(.11,.065,.010),(.20,.062,.008),(.29,.043,.006),(.36,.020,.004),(.389,.0025,.0013)]
    v=[];f=[];n=12
    for d,w,t in wing_sections:
        center=start+axis*d+chord*(.013*(d/.389)**2)
        for j in range(n):
            a=2*math.pi*j/n;p=center+chord*(w*math.cos(a))+normal*(t*math.sin(a))
            v.append((sign*p.x,p.y,p.z))
    for k in range(len(wing_sections)-1):
        for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    f.extend([tuple(reversed(range(n))),tuple((len(wing_sections)-1)*n+j for j in range(n))])
    ob=mesh_object(side+'-broad-flat-paddle',v,f,M['flippers'],C)
    ob['shape_status']='Original reconstruction: complete wing not preserved in anchor specimen.'
    ob['length_model_m']=.39;ob['max_chord_model_m']=.13;ob['midblade_thickness_model_m']=.02
    ellipsoid(side+'-short-shank',(sign*.074,.022,.090),(.038,.045,.068),M['back'])
    # Closed three-lobed webbed support foot, flat underside exactly on z=0.
    outline=[(-.029,.072),(.028,.071),(.044,.020),(.058,-.050),(.053,-.079),(.039,-.088),(.024,-.066),(.014,-.099),(-.001,-.105),(-.018,-.069),(-.036,-.091),(-.050,-.083),(-.047,-.040),(-.033,.017)]
    v=[];f=[]
    for top in (False,True):
        for x,y in outline:v.append((sign*(.074+x),y,.0 if not top else .016+max(0,y)*.15))
    n=len(outline);v.extend([(sign*.074,-.009,0),(sign*.074,-.009,.021)])
    for j in range(n):
        f.append((2*n,j,(j+1)%n));f.append((2*n+1,n+(j+1)%n,n+j));f.append((j,n+j,n+(j+1)%n,(j+1)%n))
    mesh_object(side+'-webbed-foot',v,f,M['bill_feet'],C)

# Compact rear wedge tail, closed section loft.
v=[];f=[];n=10
for y,z,w,h in [(.115,.213,.062,.036),(.171,.171,.054,.029),(.223,.127,.033,.018),(.250,.105,.007,.004)]:
    for j in range(n):
        a=2*math.pi*j/n;v.append((w*math.cos(a),y,z+h*math.sin(a)))
for k in range(3):
    for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
f.extend([tuple(reversed(range(n))),tuple(3*n+j for j in range(n))])
mesh_object('short-wedge-tail',v,f,M['back'],C)

source=audit_source(C,P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
# Factory UI can retain a host home directory in an inactive file browser.
# Scrub its fixed-size directory buffer before saving a portable source file.
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'+b' '*1020
                space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(O/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in C.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(O/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Unsupported exporter flags: '+repr(missing))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(O/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if glb['errors']:raise RuntimeError(glb['errors'])
assert glb['bytes']<=P['budgets']['max_glb_bytes']
b=source['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][key][i]-value[i]) for key,value in [('min',lo),('max',hi)] for i in range(3))
assert delta<.0001 and source['triangles']==glb['scene_triangles']
glb['file']='model.glb'  # Public report paths are bundle-relative.
write(O/'qa/evidence/technical.json',{'status':'PASS','claim_scope':'Source geometry, static embedded GLB audit and source/export correspondence only','blender_version':bpy.app.version_string,'generator_sha256':sha(Path(__file__)),'params_sha256':sha(S/'params.json'),'glb_sha256':sha(O/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'gpu':'NOT_RUN','scene':'NOT_RUN'})
print('PALAE EUDYPTES BUILD OK '+glb['sha256'])
