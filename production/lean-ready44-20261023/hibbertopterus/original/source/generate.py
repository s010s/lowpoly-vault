# SPDX-License-Identifier: MIT
"""Original Hibbertopterus scouleri reconstruction; Blender 4.3.2.
Run: blender -b --threads 2 --python source/generate.py -- --output .
Rebuild without views: append --no-render. Grey study: append --grey.
"""
import sys, json, math, hashlib, argparse
from pathlib import Path
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE / 'deps'))
import bpy, bmesh
from mathutils import Vector
import asset_common as common
from qa_glb import audit_glb

P = json.loads((SOURCE / 'params.json').read_text())
ARGS = argparse.ArgumentParser()
ARGS.add_argument('--output', default='.')
ARGS.add_argument('--no-render', action='store_true')
ARGS.add_argument('--grey', action='store_true')
args = ARGS.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT = Path(args.output).resolve(); OUT.mkdir(parents=True, exist_ok=True)
E = OUT / 'qa' / 'evidence'; E.mkdir(parents=True, exist_ok=True)
C = common.setup_scene(P['asset_id'], P['seed'])
root = bpy.data.objects[C['asset_root']]
root['representation'] = 'living-reconstruction'
root['scientific_scope'] = 'Same-species composite; restored dimensions and coloration are illustrative.'
root['anatomy'] = 'I chelicerae; II and III sweep feeding; IV mixed support; V and VI walking; twelve opisthosomal segments; keeled pointed telson.'
M = [common.make_material(n, c, r) for n,c,r in [
    ('dorsal_umber', '#75604B', .84), ('cuticle_ridge', '#9B805C', .83),
    ('joint_membrane', '#4C4035', .94), ('ventral_tan', '#AA916C', .90),
    ('eyes_obsidian', '#252620', .44), ('distal_cuticle', '#63513D', .88)]]
PARTS = []

def mesh(name, v, f, material=0, face_mats=None):
    ob = common.mesh_object(name, v, f, M if face_mats is not None else M[material], C)
    if face_mats is not None:
        for poly, mi in zip(ob.data.polygons, face_mats): poly.material_index = mi
    ob['semantic_part'] = name
    PARTS.append(ob)
    return ob

def pod(name, a, b, ra, rb, material=0, sides=10, flatten=1.0):
    """Deliberately tapered, closed four-ring podomere, no object-scale transform."""
    a,b = Vector(a),Vector(b); axis=(b-a).normalized()
    ref=Vector((0,0,1)) if abs(axis.z)<.9 else Vector((1,0,0))
    u=axis.cross(ref).normalized(); v=axis.cross(u).normalized()
    vs=[]
    rings=[(0,ra*.77),(.14,ra),(.83,rb*1.07),(1,rb*.72)]
    for t,r in rings:
        p=a.lerp(b,t)
        for k in range(sides):
            th=2*math.pi*k/sides
            vs.append(tuple(p + r*math.cos(th)*u + r*math.sin(th)*v*flatten))
    fs=[tuple(range(sides-1,-1,-1))]
    for j in range(3):
        for k in range(sides): fs.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    fs.append(tuple(3*sides+k for k in range(sides)))
    return mesh(name,vs,fs,material)

def oval(name, center, radii, material=0, longitude=20, latitude=9):
    # Closed profile loft with single poles. Used for small eyes, sockets, metastoma.
    cx,cy,cz=center; rx,ry,rz=radii
    vs=[(cx,cy,cz-rz)]
    for j in range(1,latitude):
        ph=-math.pi/2+math.pi*j/latitude
        for k in range(longitude):
            th=2*math.pi*k/longitude
            vs.append((cx+rx*math.cos(ph)*math.cos(th),cy+ry*math.cos(ph)*math.sin(th),cz+rz*math.sin(ph)))
    vs.append((cx,cy,cz+rz)); top=len(vs)-1
    fs=[]
    for k in range(longitude): fs.append((0,1+(k+1)%longitude,1+k))
    for j in range(latitude-2):
        for k in range(longitude):
            a=1+j*longitude+k; b=1+j*longitude+(k+1)%longitude
            fs.append((a,b,b+longitude,a+longitude))
    first=1+(latitude-2)*longitude
    for k in range(longitude): fs.append((first+k, first+(k+1)%longitude,top))
    return mesh(name,vs,fs,material)

# Prosoma: hand-authored shield perimeter, posterior lobes and domed radial loft.
N=48; cy=-.080; base=.035; height=P['head_depth_inferred']; rx=P['head_width_estimated']/2; ry=P['head_length_inferred']/2
outline=[]
for k in range(N):
    t=2*math.pi*k/N
    # Rounded anterior border; slightly squared posterior and modest posterolateral lobes.
    x=rx*math.sin(t)
    y=cy-ry*math.cos(t)
    if math.cos(t)<0:
        y-=.002*(-math.cos(t))*(abs(math.sin(t))**2)
        x*=1+.035*math.exp(-((abs(math.sin(t))-.78)/.18)**2)
    outline.append((x,y))
# Maintain exact estimated width (the posterior-lobe expression may widen the contour).
w=max(abs(x) for x,y in outline); outline=[(x*rx/w,y) for x,y in outline]
vs=[(0,cy,base+height)]; fs=[]; mats=[]
for j,r in enumerate((.18,.38,.58,.76,.90,1.0)):
    z=base+height*(max(0,1-r*r)**.67)
    for k,(x,y) in enumerate(outline):
        bump=.00065*math.cos(2*math.pi*k/N*3)*math.sin(math.pi*r)
        yy=cy+(y-cy)*r
        posterior_lift=.024*max(0,(yy-cy)/ry)**3
        vs.append((x*r,yy,z+bump+posterior_lift))
for k in range(N): fs.append((0,1+k,1+(k+1)%N)); mats.append(0)
for j in range(5):
    for k in range(N):
        a=1+j*N+k; b=1+j*N+(k+1)%N
        fs.append((a,a+N,b+N,b)); mats.append(1 if j==4 else 0)
# Thickened ventral lip, bottom disk; not an open two-sided sheet.
start=len(vs)
for x,y in outline: vs.append((x*.97,cy+(y-cy)*.97,base-.003+.024*max(0,(y-cy)/ry)**3))
for k in range(N): fs.append((1+5*N+k,start+k,start+(k+1)%N,1+5*N+(k+1)%N)); mats.append(5)
vs.append((0,cy,base-.004)); pole=len(vs)-1
for k in range(N): fs.append((pole,start+(k+1)%N,start+k)); mats.append(3)
mesh('prosoma_domed_shield',vs,fs,face_mats=mats)

# Eyes are modest sessile lenses, not elevated stalks.
def shield_z(x,y):
    r2=(x/rx)**2+((y-cy)/ry)**2
    return base+height*(max(0,1-r2)**.67)+.024*max(0,(y-cy)/ry)**3
for s in (-1,1):
    x=s*.034; y=-.085; z=shield_z(x,y)
    oval('lateral_eye_socket_'+str(s),(x,y,z-.0004),(.006,.008,.0023),5,20,7)
    oval('lateral_eye_'+str(s),(x,y-.0001,z+.0011),(.0038,.0053,.0018),4,20,7)
    x=s*.0024; y=-.088; z=shield_z(x,y)
    oval('median_ocellus_'+str(s),(x,y,z+.0005),(.00125,.0015,.0008),4,12,6)
# Subtle sparse lunulate cuticle ridges, an artistic readable abstraction, not hairs.
for row,(yy,xxs) in enumerate([(-.105,[-.018,0,.018]),(-.070,[-.024,0,.024]),(-.052,[-.022,0,.022])]):
    for q,xx in enumerate(xxs):
        pts=[]
        for k in range(7):
            th=math.pi*.15+math.pi*.7*k/6
            x=xx+.004*math.cos(th); y=yy+.002*math.sin(th)
            pts.append((x,y,shield_z(x,y)+.00045))
        for k in range(len(pts)-1): pod('lunule_%d_%d_%d'%(row,q,k),pts[k],pts[k+1],.00038,.00034,1,6)

# Opisthosoma: twelve overlapping, broad-to-narrow closed tergites.
widths=[.051,.053,.052,.050,.047,.043,.038,.032,.026,.021,.0168,.0125]
centers=[-.033+.013*i for i in range(12)]
for i,(y,w) in enumerate(zip(centers,widths)):
    z=.043-.014*(i/11)**1.4; hh=.022-.010*(i/11)
    length=.0148 if i<7 else .0140
    vs=[]; fs=[]; mats=[]; ns=32
    # Relative cross-section: gently arched dorsal, compressed sternum.
    for j,(dy,factor) in enumerate([(-length*.5,.95),(-length*.23,1.02),(length*.28,1.00),(length*.5,.91)]):
        for k in range(ns):
            th=2*math.pi*k/ns
            x=w*factor*math.cos(th)
            zz=z+hh*math.sin(th)*(1 if math.sin(th)>0 else .64)
            # modest pointed lateral shoulder, not trilobite spines
            zz+=.0011*math.cos(th)**8
            vs.append((x,y+dy,zz))
    fs.append(tuple(range(ns-1,-1,-1))); mats.append(2)
    for j in range(3):
        for k in range(ns):
            fs.append((j*ns+k,j*ns+(k+1)%ns,(j+1)*ns+(k+1)%ns,(j+1)*ns+k))
            upper=math.sin(2*math.pi*(k+.5)/ns)>0
            mats.append((1 if j==2 else 0) if upper else 3)
    fs.append(tuple(3*ns+k for k in range(ns))); mats.append(2)
    mesh('opisthosomal_tergite_%02d'%(i+1),vs,fs,face_mats=mats)
    # Dark recessed intersegmental membranes, fully beneath outer plates.
    if i<11: pod('segment_membrane_%02d'%i,(0,y+.005,z),(0,y+.010,z),w*.87,widths[i+1]*.87,2,20,.33)

# Telson: broadened shoulder, pointed planform, twin dorsal ridges and pronounced ventral keel.
# Cross section: middle upper groove lower than two lateral ridges; not a raised scorpion sting.
ys=[.114,.123,.134,.151,.169,.175]
ws=[.011,.016,.0128,.0081,.0026,.00022]
zs=[.029,.026,.022,.018,.014,.013]
vs=[]; fs=[]; mats=[]
for y,w,z in zip(ys,ws,zs):
    for xf,zf in [(-1,0),(-.55,.004),(0,.002),(.55,.004),(1,0),(.55,-.002),(0,-.008),(-.55,-.002)]:
        vs.append((xf*w,y,z+zf*min(1,w/.009)))
fs.append(tuple(range(7,-1,-1))); mats.append(2)
for j in range(len(ys)-1):
    for k in range(8):
        fs.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k)); mats.append(1 if k in (0,3) else 5 if k in (1,2) else 3)
fs.append(tuple((len(ys)-1)*8+k for k in range(8))); mats.append(5)
mesh('telson_shoulders_dorsal_groove_ventral_keel',vs,fs,face_mats=mats)

# Ventral mouth complex and small chelicerae (appendage I).
oval('metastoma_ventral_plate',(0,-.086,.029),(.012,.016,.004),3,20,8)
for s in (-1,1):
    pts=[(s*.009,-.095,.031),(s*.012,-.111,.026),(s*.009,-.120,.023)]
    for j in range(2): pod('appendage_I_%s_%s'%(s,j),pts[j],pts[j+1],.0038-j*.001,.0028-j*.0006,5,10,.8)
    pod('cheliceral_finger_outer_'+str(s),pts[-1],(s*.004,-.126,.024),.0018,.0006,5,8)
    pod('cheliceral_finger_inner_'+str(s),(s*.009,-.115,.024),(s*.0045,-.121,.024),.0014,.00055,5,8)

# Five postcheliceral limb pairs. II-III gather; IV support + sensory tibia; V-VI walk.
limb_records=[]
for s in (-1,1):
    for roman,points,radii in [
        ('II',[(.022,-.089,.032),(.037,-.103,.026),(.043,-.118,.022),(.036,-.135,.018),(.026,-.144,.017)],[.0052,.005,.004,.003,.0018]),
        ('III',[(.030,-.074,.032),(.048,-.088,.026),(.059,-.103,.021),(.062,-.119,.017),(.053,-.132,.013)],[.006,.0058,.0046,.0036,.0019]),
        ('IV',[(.038,-.065,.034),(.060,-.063,.038),(.076,-.067,.028),(.084,-.074,.014),(.086,-.071,.0027)],[.007,.007,.0052,.0038,.0026]),
        ('V',[(.040,-.055,.036),(.054,-.042,.041),(.082,-.031,.038),(.097,-.016,.024),(.103,.001,.011),(.106,.012,.0027)],[.009,.0085,.0078,.0056,.0042,.0028]),
        ('VI',[(.040,-.041,.035),(.052,-.022,.038),(.085,.002,.036),(.102,.027,.024),(.111,.052,.011),(.114,.071,.0027)],[.010,.0095,.009,.0067,.0048,.0028])
    ]:
        points=[(s*x,y,z) for x,y,z in points]
        for j in range(len(points)-1):
            a=Vector(points[j]); b=Vector(points[j+1]); d=b-a
            pod('appendage_%s_%s_podomere_%d'%(roman,s,j+1),a+d*.04,b-d*.035,radii[j],radii[j+1],0 if j<2 else 5,10,.82)
            if j: oval('appendage_%s_%s_joint_%d'%(roman,s,j),tuple(a),(radii[j]*.76,radii[j]*.76,radii[j]*.76),2,12,6)
        if roman in ('II','III'):
            # Three separated broad sensory flanges on inner/anterior face; no dense filtering comb.
            for j in (1,2,3):
                p=Vector(points[j]); tip=p+Vector((-s*(.0075 if j<3 else .006),-.010,0))
                pod('sensory_flange_%s_%s_%d'%(roman,s,j),p,tip,.0022,.00065,1,8,.34)
        elif roman=='IV':
            p=Vector(points[2]); pod('IV_sensory_tibial_spine_'+str(s),p,p+Vector((-s*.007,-.011,-.001)),.002,.0007,1,8,.42)
            p=Vector(points[3]); pod('IV_articulated_tarsal_spur_'+str(s),p,p+Vector((s*.004,-.006,-.004)),.0014,.0006,5,8)
            pod('IV_terminal_tarsus_'+str(s),points[-1],(s*.094,-.071,.0012),.0024,.0005,5,10,.55)
        else:
            p=Vector(points[-1]); pod('terminal_walking_tarsus_%s_%s'%(roman,s),p,p+Vector((s*.009,0,-.0015)),.0027,.00065,5,10,.55)
        limb_records.append({'pair':roman,'side':s,'articulations_m':points})

# Foot contact center and exact origin. Translate geometry only, retaining identity root.
common.ground_asset(C, center_xy=False)
source_qa=common.audit_source(C,max_triangles=40000)
if source_qa['errors']: raise RuntimeError(source_qa['errors'])
# Save original semantic parts and their vertex positions, not temporary export or lighting.
bpy.context.scene['reconstruction_notes']='Approximate 115 mm head, restored 300 mm shield-to-telson body. Limb reach is excluded from that total. No swimming paddles; no dense filtering hairs.'
bpy.context.preferences.filepaths.save_version=0
# Remove default workstation directories from editable-file UI state before its first save.
bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params is not None:
                space.params.directory=b' '*1023
                space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),compress=False)

# One export mesh with six material primitives, while model.blend retains all semantic parts.
vs=[]; fs=[]; mis=[]
for ob in PARTS:
    off=len(vs); vs.extend(tuple(ob.matrix_world@v.co) for v in ob.data.vertices)
    for poly in ob.data.polygons:
        fs.append(tuple(off+i for i in poly.vertices)); mis.append(M.index(ob.data.materials[poly.material_index]))
export_mesh=mesh('hibbertopterus_export_surface',vs,fs,face_mats=mis)
for ob in PARTS[:-1]: ob.hide_render=True; ob.hide_set(True)
bpy.ops.object.select_all(action='DESELECT'); root.select_set(True); export_mesh.select_set(True)
bpy.context.view_layer.objects.active=export_mesh
opts=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available: raise RuntimeError('Unsupported pinned exporter options: '+str(set(opts)-available))
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**opts)
audit=audit_glb(OUT/'model.glb',40000,6,8)
if audit['errors']: raise RuntimeError(audit['errors'])
# Audit reports contain relative model filename, never ambient working directories.
for key in ('path','file','filename'):
    if key in audit: audit[key]='model.glb'
expected_min=[source_qa['bounds_blender_m']['min'][0],source_qa['bounds_blender_m']['min'][2],-source_qa['bounds_blender_m']['max'][1]]
expected_max=[source_qa['bounds_blender_m']['max'][0],source_qa['bounds_blender_m']['max'][2],-source_qa['bounds_blender_m']['min'][1]]
bounds_delta=max(abs(audit['bounds_m'][edge][i]-expected[i]) for edge,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
assert bounds_delta<1e-6 and audit['scene_triangles']==source_qa['triangles']
report={'status':'PASS','scope':'Source geometry and static uncompressed GLB audit; not Khronos or runtime rendering.','blender_version':bpy.app.version_string,'source':source_qa,'glb':audit,'source_to_export_bounds_max_error_m':bounds_delta,'export_options':opts,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((SOURCE/'params.json').read_bytes()).hexdigest(),'seed':P['seed'],'body_shield_front_to_telson_m':.3,'head_width_m':P['head_width_estimated'],'scale_interpretation':'Restored length, not measured fossil total. Limb reach increases full model bounds.','palette':[{'name':m.name,'srgb':m['palette_srgb']} for m in M], 'appendage_pairs':limb_records,'femur_lengths_m':{'V':math.dist((.054,-.042,.041),(.082,-.031,.038)),'VI':math.dist((.052,-.022,.038),(.085,.002,.036))},'threejs_target_version':'0.180.0','gpu':'UNKNOWN','scene':'UNKNOWN'}
(E/'technical.json').write_text(json.dumps(report,indent=2)+'\n')

if not args.no_render:
    # Discard source, clean-import the exact exported bytes before every evidence set.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    imported=list(bpy.context.scene.objects)
    coll=bpy.data.collections.new('EXACT_GLB'); bpy.context.scene.collection.children.link(coll)
    for ob in imported:
        for old in list(ob.users_collection): old.objects.unlink(ob)
        coll.objects.link(ob)
    import render_exact
    render_exact.render(coll,OUT/'views',grey=args.grey)
    import shutil
    shutil.copyfile(OUT/'views'/'perspective.png',OUT/'preview.png')
    evidence={'scope':'Four Cycles CPU views from clean import of exact model.glb, not browser/GPU proof.','glb_sha256':audit['sha256'],'renderer':'Blender Cycles CPU 4.3.2','samples':8 if args.grey else 32,'resolution':[320,320] if args.grey else [640,640],'views':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[1,-1,1]},'projection':'orthographic','color_management':'Standard, None, exposure 0, gamma 1','preview_reuses_perspective':True,'view_hashes':{n:hashlib.sha256((OUT/'views'/f'{n}.png').read_bytes()).hexdigest() for n in ['front','side','top','perspective']}}
    (E/'views.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('HIBBERTOPTERUS_BUILD_COMPLETE',audit['scene_triangles'],audit['sha256'])
