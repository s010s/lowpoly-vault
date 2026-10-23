#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Sylviornis r001. Original profile/swept-ring geometry, meters, -Y forward.
Usage: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Only source/params.json and declared source/deps helpers are runtime inputs.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(args)
OUT=a.out.resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('sylviornis',seed=P['seed'])
scene=bpy.context.scene
scene.render.threads_mode='FIXED'; scene.render.threads=2
M={k:make_material('sylviornis-'+k,v,roughness=.29 if k=='eye' else .88 if k in ('body','wing','under') else .76) for k,v in P['palette_srgb'].items()}

# A loft is a closed sequence of authored cross sections, with pointed end caps.
# The two section axes allow long lateral-compressed skull/bill profiles as well
# as S-curved neck tubes. Faces are explicitly triangulated and consistently wound.
def loft(name, sections, n, material, *, axis='y', underside=False, stagger=False):
    # sections: (x,y,z,halfwidth,halfheight) with axes x and sagittal perpendicular.
    vs=[]; fs=[]
    for i,s in enumerate(sections):
        x,y,z,rx,rz=s
        if axis=='y': u=Vector((1,0,0)); v=Vector((0,0,1))
        elif axis=='x': u=Vector((0,1,0)); v=Vector((0,0,1))
        else:
            prev=Vector(sections[max(0,i-1)][:3]); nex=Vector(sections[min(len(sections)-1,i+1)][:3])
            tangent=(nex-prev).normalized(); u=Vector((1,0,0)); v=tangent.cross(u).normalized()
        phase=.045*math.sin(i*1.8) if stagger else 0
        for j in range(n):
            ang=2*math.pi*j/n+phase
            q=Vector((x,y,z))+u*(rx*math.cos(ang))+v*(rz*math.sin(ang))
            vs.append(tuple(q))
    for i in range(len(sections)-1):
        for j in range(n):
            k=(j+1)%n; p=i*n+j; q=i*n+k; r=(i+1)*n+k; s=(i+1)*n+j
            if (i+j)%2: fs.extend(((p,q,s),(q,r,s)))
            else: fs.extend(((p,q,r),(p,r,s)))
    for i,rev in ((0,True),(len(sections)-1,False)):
        center=len(vs);vs.append(tuple(sections[i][:3])); start=i*n
        for j in range(n):
            f=(center,start+j,start+(j+1)%n); fs.append(f[::-1] if rev else f)
    obj=mesh_object(name,vs,fs,material,C)
    if underside:
        for poly in obj.data.polygons:
            # Large quiet color regions, not per-face random noise.
            xyz=sum((obj.data.vertices[k].co for k in poly.vertices),Vector())/len(poly.vertices)
            nearest=min(sections,key=lambda s:abs(s[1]-xyz.y))
            if xyz.z<nearest[2]-.40*nearest[4]: poly.material_index=1
    return obj

def tube(name,pts,radii,n,mat):
    return loft(name,[(*p,*r) for p,r in zip(pts,radii)],n,mat,axis='path')

def ellipsoid_x(name,c,r,mat,n=16):
    cx,cy,cz=c;rx,ry,rz=r
    sections=[]
    for t in [-.98,-.85,-.5,0,.5,.85,.98]:
        f=math.sqrt(1-t*t); sections.append((cx+rx*t,cy,cz,ry*f,rz*f))
    return loft(name,sections,n,mat,axis='x')

# One continuous feathered trunk-to-neck surface, not a stack of primitives.
# Authored cross sections rotate along the centerline into the thick S neck.
body=loft('continuous-feathered-trunk-and-neck',[
(0,.348,.400,.018,.037),(0,.333,.414,.055,.072),(0,.295,.425,.108,.113),
(0,.235,.431,.153,.142),(0,.155,.435,.187,.165),(0,.070,.435,.200,.183),
(0,-.025,.435,.198,.188),(0,-.110,.446,.184,.177),(0,-.185,.480,.147,.132),
(0,-.240,.528,.105,.099),(0,-.283,.582,.079,.081),(0,-.311,.640,.067,.071),
(0,-.327,.696,.065,.070),(0,-.350,.729,.067,.061),(0,-.390,.750,.062,.044)],
24,[M['body'],M['under']],axis='path',stagger=True)
for poly in body.data.polygons:
    xyz=sum((body.data.vertices[k].co for k in poly.vertices),Vector())/len(poly.vertices)
    if xyz.z<.350 and xyz.y>-.18:poly.material_index=1
# Broad posterior skull, no bony holes represented as skin wounds.
head=loft('broad-posterior-head',[(0,-.518,.753,.028,.044),(0,-.480,.758,.050,.049),
(0,-.451,.760,.066,.052),(0,-.415,.760,.075,.053),(0,-.378,.755,.069,.049),
(0,-.348,.749,.048,.039),(0,-.332,.744,.016,.022)],20,M['body'],stagger=True)
# Adult NCP242-like deep rostrum: 148 mm hinge-to-tip, narrow front, hooked tip.
# This is a living contour with only a thin keratin addition, not a fossil cast.
bill=loft('deep-compressed-upper-bill',[(0,-.510,.750,.030,.044),(0,-.531,.750,.027,.045),
(0,-.555,.749,.024,.041),(0,-.580,.744,.021,.035),
(0,-.604,.735,.016,.026),(0,-.627,.722,.010,.020),
(0,-.647,.706,.005,.014),(0,-.658,.689,.0016,.003)],16,M['bill'])
# QA-01: extend the posterior jaw under the skull, with its cap buried inside
# the posterior head rather than exposed midway under the rostrum.
lower=loft('restrained-lower-mandible',[(0,-.355,.746,.025,.015),
(0,-.385,.731,.039,.020),(0,-.425,.719,.044,.021),(0,-.465,.713,.035,.020),
(0,-.501,.710,.028,.019),
(0,-.530,.706,.025,.015),(0,-.562,.704,.020,.012),(0,-.595,.703,.015,.009),
(0,-.625,.700,.007,.006),(0,-.645,.697,.002,.002)],14,M['bill'])
# Broad-based fixed bony rostral ornament. Full solid dome, no thin comb or horn.
orn=tube('dorsal-bony-rostral-ornament',[(0,-.532,.779),(0,-.532,.796),(0,-.535,.815),
(0,-.538,.832),(0,-.539,.843),(0,-.539,.850)],
[(.0206,.026),(.022,.029),(.026,.034),(.027,.034),(.024,.029),(.014,.019)],18,M['bill'])
# Reduced paired folded wings. Distinct low-profile shape, no fan of flight quills.
for sign,label in ((-1,'left'),(1,'right')):
    loft(label+'-reduced-folded-wing',[(sign*.151,-.142,.492,.006,.027),
    (sign*.181,-.100,.484,.020,.057),(sign*.199,-.040,.463,.022,.064),
    (sign*.199,.030,.443,.022,.056),(sign*.186,.095,.421,.019,.040),
    (sign*.162,.154,.399,.014,.024),(sign*.140,.180,.385,.004,.009)],14,M['wing'])
    # Three short narrow covert lobes form an original folded-edge rhythm.
    for j in range(3):
        x=sign*(.190-j*.010)
        loft(label+'-covert-'+str(j+1),[(x,-.023+j*.028,.454-j*.011,.004,.018),
            (x+sign*.019,.024+j*.024,.436-j*.012,.010,.024),
            (x+sign*.010,.097+j*.024,.411-j*.014,.008,.014),
            (x-sign*.009,.153+j*.009,.389-j*.010,.002,.004)],8,M['wing'])
    # Feathered tibia narrows toward the intertarsal joint. Femur is inside trunk.
    tube(label+'-feathered-tibia',[(sign*.106,-.036,.368),(sign*.108,.020,.299),
        (sign*.111,.065,.240),(sign*.110,.097,.168)],
        [(.055,.056),(.043,.043),(.033,.030),(.024,.024)],14,M['body'])
    # Tarsometatarsus is approximately 158 mm long, supported on toes.
    tube(label+'-stout-tarsometatarsus',[(sign*.110,.100,.194),(sign*.110,.095,.164),
        (sign*.108,.078,.092),(sign*.106,.059,.033),(sign*.106,.052,.023)],
        [(.019,.021),(.017,.019),(.016,.017),(.019,.019),(.022,.018)],12,M['foot'])
    # Three separated forward toes; the central toe is longest.
    starts=[]
    for j,(dx,dy) in enumerate(((-.050,-.075),(0,-.108),(.050,-.075))):
        base=(sign*.106,.052,.023);end=(sign*.106+dx,.052+dy,.010)
        pts=[base,(base[0]+dx*.40,base[1]+dy*.35,.018),
            (base[0]+dx*.78,base[1]+dy*.75,.012),end]
        toe=tube(label+'-forward-toe-'+str(j+1),pts,[(.011,.010),(.010,.009),(.008,.007),(.006,.005)],10,M['foot'])
        direction=Vector((dx,dy,0)).normalized(); tip=Vector(end)+direction*.017;tip.z=.004
        tube(label+'-toe-claw-'+str(j+1),[end,tuple(Vector(end)+direction*.009+Vector((0,0,.001))),tuple(tip)],
            [(.0062,.0058),(.0045,.0045),(.0015,.0015)],8,M['bill'])
    # One short backward hallux, separate from forward toe triplet.
    rear=[(sign*.105,.062,.029),(sign*.104,.095,.021),(sign*.102,.128,.012)]
    tube(label+'-rear-hallux',rear,[(.010,.009),(.008,.007),(.006,.005)],10,M['foot'])
    tube(label+'-hallux-claw',[rear[-1],(sign*.102,.138,.010),(sign*.101,.145,.005)],
        [(.006,.005),(.004,.004),(.0013,.0013)],8,M['bill'])
    # Eyes are restrained dark lateral eyes, with muted keratin-colored narrow rim.
    ellipsoid_x(label+'-eye-rim',(sign*.065,-.454,.777),(.0065,.0124,.0108),M['bill'],16)
    ellipsoid_x(label+'-eye',(sign*.070,-.454,.778),(.0047,.0087,.0078),M['eye'],16)
    ellipsoid_x(label+'-nostril',(sign*.026,-.534,.764),(.0019,.0055,.0034),M['eye'],12)
# Very short restrained tail, three tucked lobes, not a display fan.
for j,x in enumerate((-.047,0,.047)):
    loft('short-tail-feather-'+str(j+1),[(x,.285,.408,.032,.038),
        (x,.338,.399,.030,.032),(x,.389,.382,.024,.022),
        (x,.416-abs(x)*.3,.359,.012,.009)],12,M['wing'])

# Group selected anatomically tiny feather lobes into editable semantic wing meshes
# to keep draw work low without joining distinct limbs, bill, eyes, or trunk.
for sign,label in ((-1,'left'),(1,'right')):
    names=[label+'-reduced-folded-wing']+[label+'-covert-'+str(j+1) for j in range(3)]
    objs=[bpy.data.objects[n] for n in names]
    verts=[];faces=[]
    for obj in objs:
        off=len(verts);verts += [tuple(v.co) for v in obj.data.vertices]
        faces += [tuple(off+i for i in p.vertices) for p in obj.data.polygons]
    for obj in objs: bpy.data.objects.remove(obj,do_unlink=True)
    verts=[(x,.020+(y-.020)*.76,z) for x,y,z in verts]
    loftwing=mesh_object(label+'-folded-wing-with-coverts',verts,faces,M['wing'],C)
# The origin is the midpoint of the two weight-bearing feet, not body bbox center.
# Shift all geometry so its lowest toe-claw point touches floor; preserve root identity.
bpy.context.view_layer.update()
low=min(v.co.z for o in C.objects if o.type=='MESH' for v in o.data.vertices)
# Fit the exactly frozen reconstructed resting envelope, preserving all proportions.
high=max(v.co.z for o in C.objects if o.type=='MESH' for v in o.data.vertices)
scale=P['rest_height_m']/(high-low)
for o in C.objects:
    if o.type=='MESH':
        for v in o.data.vertices:
            v.co.x*=scale; v.co.y=(v.co.y-.044)*scale;v.co.z=(v.co.z-low)*scale
        o.data.update()
root=bpy.data.objects['sylviornis'];root['representation']='living reconstruction; composite osteology'
root['resting_height_m']=P['rest_height_m']; root['soft_tissue_and_colors']='inferred'
root['rostrum_reference']='NCP242, cf. neocaledoniae in 2005; separate from 2016 limb sample means'
root['bill_reconstruction']='deep lateral rostrum and fixed bony ornament; conservative keratin contour'
scene['asset_author']='Leon Made This / s010s';scene['asset_license']='CC-BY-4.0'
source=audit_source(C,P['budgets']['max_triangles'])
if source['errors']: raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,
 export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,
 export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,
 export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
 export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(opts)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing: raise RuntimeError('Unsupported exporter options '+str(missing))
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if glb['errors']: raise RuntimeError(glb['errors'])
if glb['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m'];delta=max(abs(glb['bounds_m'][side][i]-exp[i]) for side,exp in [('min',[b['min'][0],b['min'][2],-b['max'][1]]),('max',[b['max'][0],b['max'][2],-b['min'][1]])] for i in range(3))
if delta>1e-4 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Source/GLB metrics disagree')
record={'status':'PASS','claim_scope':'Source/static GLB geometry and bounds only; not independent visual, GPU or scene approval',
 'asset_id':'sylviornis','revision':'r001','blender_version':bpy.app.version_string,'threads':scene.render.threads,
 'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),
 'source':source,'glb':glb,'source_export_bounds_max_delta_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},
 'profile':'palette-only static flat-shaded profile with original mesh geometry',
 'scale_fit_factor':scale,'axis_convention':{'blender_up':'+Z','blender_forward':'-Y','glb_up':'+Y','glb_forward':'+Z'},
 'reconstruction_notes':['Rostrum 148 mm before uniform 0.85 m envelope fit; not a fossil measurement of whole animal.',
 'Limb sample means and NCP242 rostrum are different fossils, not an articulated specimen.',
 'Body/neck feathers, palette, keratin sheath and wing covert contours are artistic inference.',
 'Anatomical part overlaps are intentional, with closed manifold semantic meshes; no claim of printable union.']}
(OUT/'technical.json').write_text(json.dumps(record,indent=2)+'\n')
print('SYLVIORNIS_BUILD_OK',glb['sha256'],glb['scene_triangles'],glb['scene_primitives_estimated_base_draw_calls'])
