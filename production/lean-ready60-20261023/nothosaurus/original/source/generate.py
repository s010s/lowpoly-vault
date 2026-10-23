# SPDX-License-Identifier: MIT
"""Nothosaurus mirabilis, deterministic editable living reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
All model-specific geometry is original. Anatomical uncertainty is in brief.json.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=argparse.ArgumentParser();args.add_argument('--output',default='.')
args=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(args.output);OUT.mkdir(parents=True,exist_ok=True)
(OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
COL=setup_scene(P['asset_id'],P['seed'])
root=bpy.data.objects[COL['asset_root']]
root['authoring_forward']='+X';root['mounting_origin']='Swimming trunk center; no terrestrial ground-contact claim'
root['taxon']='Nothosaurus mirabilis';root['revision']=P['revision']
MAT=[make_material(k,v,roughness=.84 if k!='Eyes' else .35) for k,v in P['palette'].items()]
# Coordinates are metres. Elliptical axial lofts are continuous across tail/trunk/neck.
def loft(sections,n=16,transform=None):
    vs=[];fs=[];mi=[]
    for x,y,z,ry,rz in sections:
        for j in range(n):
            a=2*math.pi*j/n;p=(x,y+ry*math.cos(a),z+rz*math.sin(a))
            vs.append(tuple(transform(p)) if transform else p)
    for i in range(len(sections)-1):
        for j in range(n):
            fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
            s=math.sin(2*math.pi*(j+.5)/n);mi.append(0 if s>.38 else 2 if s<-.45 else 1)
    fs.append(tuple(reversed(range(n))));mi.append(1)
    fs.append(tuple((len(sections)-1)*n+j for j in range(n)));mi.append(1)
    return vs,fs,mi

def obj(name,data,mats=MAT[:3],indices=True):
    v,f,mi=data;o=mesh_object(name,v,f,mats,COL)
    if indices:
        for p,m in zip(o.data.polygons,mi):p.material_index=m
    return o

sections=[(-1.68,.035,-.015,.0025,.003),(-1.62,.029,-.01,.009,.012),(-1.52,.018,-.004,.017,.023),(-1.40,0,.005,.027,.036),(-1.26,-.016,.012,.041,.049),(-1.10,-.021,.018,.057,.065),(-.94,-.018,.02,.074,.082),(-.78,-.008,.018,.092,.105),(-.64,0,.013,.112,.125),(-.54,0,.009,.128,.143),(-.42,0,.004,.148,.16),(-.28,0,0,.162,.17),(-.12,0,0,.164,.17),(.05,0,0,.160,.166),(.20,0,.008,.149,.155),(.34,0,.018,.132,.138),(.46,0,.026,.107,.111),(.55,0,.033,.081,.081),(.63,.008,.038,.065,.066),(.71,.021,.043,.056,.057),(.79,.039,.047,.049,.051),(.87,.059,.05,.045,.046),(.95,.077,.053,.043,.043),(1.04,.092,.056,.045,.042)]
obj('Axial_body_neck_and_tail',loft(sections))
HEAD=Vector((1.04,.092,.056));ANG=math.radians(P['head_yaw_degrees'])
def headpoint(p):
    x,y,z=p;return HEAD+Vector((x*math.cos(ANG)-y*math.sin(ANG),x*math.sin(ANG)+y*math.cos(ANG),z))
# Long posterior skull, narrowed rostral waist and modest expanded premaxilla.
upper=[(-.03,0,.002,.036,.032),(0,0,.004,.044,.038),(.025,0,.01,.065,.043),(.06,0,.014,.075,.042),(.10,0,.012,.067,.037),(.14,0,.005,.049,.030),(.185,0,-.002,.033,.024),(.225,0,-.006,.0325,.020),(.26,0,-.005,.043,.021),(.29,0,-.005,.048,.021),(.315,0,-.006,.036,.017),(.32,0,-.006,.020,.010)]
obj('Elongate_constricted_upper_head',loft(upper,16,headpoint))
# Lower jaw rotates as a single continuous mandible around the posterior joint.
JAW=math.radians(P['jaw_open_degrees'])
def jawpoint(p):
    x,y,z=p;return headpoint((x*math.cos(JAW)+z*math.sin(JAW),y,-x*math.sin(JAW)+z*math.cos(JAW)-.024))
lower=[(.005,0,0,.04,.013),(.04,0,-.002,.062,.015),(.08,0,-.003,.062,.014),(.13,0,-.004,.048,.012),(.18,0,-.005,.032,.010),(.23,0,-.006,.033,.009),(.27,0,-.006,.043,.010),(.30,0,-.006,.039,.009),(.316,0,-.006,.022,.006)]
lo=loft(lower,12,jawpoint);lo=(lo[0],lo[1],[1 if x==0 else 2 for x in lo[2]])
obj('Opened_lower_mandible',lo)
# Shallow enclosed oral lining, visibly separate from the ivory grasping teeth.
oral=[(.025,0,-.011,.039,.006),(.09,0,-.014,.05,.005),(.16,0,-.016,.032,.0035),(.23,0,-.017,.029,.003),(.29,0,-.017,.032,.003),(.312,0,-.017,.015,.002)]
obj('Palatal_oral_lining',loft(oral,10,headpoint),[MAT[3]],False)

# Closed oriented swept tubes, assembled into each editable anatomical limb.
def tube(points,radii,n=10):
    vs=[];fs=[]
    for i,(p,rr) in enumerate(zip(points,radii)):
        p=Vector(p);direction=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
        direction.normalize();u=direction.cross(Vector((0,0,1))).normalized();v=direction.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n;vs.append(tuple(p+u*rr[0]*math.cos(a)+v*rr[1]*math.sin(a)))
    for i in range(len(points)-1):
        for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))])
    return vs,fs,[0]*len(fs)
def merge(a,b):
    av,af,am=a;bv,bf,bm=b;off=len(av)
    return av+bv,af+[tuple(off+i for i in f) for f in bf],am+bm

def webbed_foot(center,side,hind=False):
    # A solid fan with five rounded ray tips and four shallow clefts; inferred soft tissue.
    x,y,z=center;lengths=[.078,.108,.123,.115,.085] if not hind else [.066,.089,.105,.097,.073]
    angs=[-43,-23,0,23,43];rim=[(-.035,-.026),(-.048,.014)]
    for i,(ang,ln) in enumerate(zip(angs,lengths)):
        for da in [-5,5]:
            a=math.radians(ang+da);rim.append((math.sin(a)*ln,math.cos(a)*ln))
        if i<4:
            a=math.radians((ang+angs[i+1])/2);r=.073 if not hind else .064
            rim.append((math.sin(a)*r,math.cos(a)*r))
    rim.extend([(.047,.012),(.032,-.026)])
    vs=[];th=.009 if not hind else .0075
    for dz in [th,-th]:
        vs.extend((x+u,y+side*v,z+dz*(.6+.4*max(0,1-v/.13))) for u,v in rim)
    n=len(rim);vs.extend([(x,y+side*.034,z+th*1.15),(x,y+side*.034,z-th*1.15)])
    fs=[]
    for j in range(n):
        k=(j+1)%n;fs.extend([(2*n,j,k),(2*n+1,n+k,n+j),(j,n+j,n+k,k)])
    return vs,fs,[0]*len(fs)
for side,label in [(-1,'Right'),(1,'Left')]:
    for hind in [False,True]:
        if not hind:
            pp=[(.38,side*.095,.005),(.35,side*.17,-.035),(.29,side*.244,-.07),(.325,side*.29,-.085),(.34,side*.336,-.095)]
            rr=[(.062,.052),(.057,.044),(.043,.032),(.035,.023),(.032,.017)]
        else:
            pp=[(-.44,side*.10,-.01),(-.48,side*.17,-.044),(-.55,side*.228,-.073),(-.57,side*.27,-.09),(-.58,side*.305,-.101)]
            rr=[(.047,.042),(.040,.032),(.030,.025),(.026,.019),(.025,.014)]
        obj(label+('_hindlimb_and_webbed_foot' if hind else '_forelimb_and_webbed_foot'),merge(tube(pp,rr),webbed_foot(pp[-1],side,hind)),[MAT[1]],False)

# Teeth are conical slender grasping crowns, not crushing knobs or giant tusks.
def cone_between(base,tip,radius,n=7):
    b,t=Vector(base),Vector(tip);d=(t-b).normalized();u=d.cross(Vector((0,1,0)))
    if u.length<.01:u=d.cross(Vector((1,0,0)))
    u.normalize();v=d.cross(u).normalized();vs=[]
    for tt,rr in [(0,radius),(.40,radius*.70)]:
        p=b+(t-b)*tt
        for j in range(n):vs.append(tuple(p+(u*math.cos(2*math.pi*j/n)+v*math.sin(2*math.pi*j/n))*rr))
    vs.append(tuple(t));fs=[tuple(reversed(range(n)))]
    for j in range(n):k=(j+1)%n;fs.extend([(j,k,n+k,n+j),(n+j,n+k,2*n)])
    return vs,fs,[0]*len(fs)
teeth=([],[],[])
upper_teeth=[(.075,.061,.012),(.105,.053,.013),(.135,.043,.014),(.168,.032,.018),(.197,.031,.026),(.227,.031,.021),(.260,.040,.025),(.290,.042,.027),(.313,.023,.020)]
for s in [-1,1]:
    for x,y,l in upper_teeth:
        base=(x,s*y,-.022);tip=(x+.005,s*(y+.001),-.022-l)
        teeth=merge(teeth,cone_between(headpoint(base),headpoint(tip),.0024 if l<.02 else .0032))
    for x,y,l in [(.09,.054,.01),(.125,.045,.011),(.16,.034,.014),(.199,.030,.019),(.239,.035,.016),(.273,.041,.022),(.303,.029,.020)]:
        teeth=merge(teeth,cone_between(jawpoint((x,s*y,.002)),jawpoint((x+.003,s*y,.002+l)),.0023 if l<.018 else .0029))
obj('Pointed_grasping_teeth',teeth,[MAT[4]],False)
# Small dorsolateral eye solids, not exposed cranial windows.
eyes=([],[],[])
for s in [-1,1]:
    center=headpoint((.071,s*.064,.039));v=[];f=[];n=12;rows=5
    # Closed UV lens with nonzero terminal rings, then caps.
    for i in range(rows):
        lat=-math.pi/2+.09+i*(math.pi-.18)/(rows-1)
        for j in range(n):
            a=2*math.pi*j/n;v.append(tuple(center+Vector((.014*math.cos(lat)*math.cos(a),.008*math.cos(lat)*math.sin(a),.010*math.sin(lat)))))
    for i in range(rows-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.extend([tuple(reversed(range(n))),tuple((rows-1)*n+j for j in range(n))])
    eyes=merge(eyes,(v,f,[0]*len(f)))
obj('Paired_dorsolateral_eyes',eyes,[MAT[5]],False)
# Source QA and exact GLB export. Save an editable source without cameras/stage.
bpy.context.view_layer.update();source=audit_source(COL,max_triangles=P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
# Clear non-model UI file-browser history before saving a public editable source.
bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'_'*1023
                space.params.directory=b'//'
                space.params.filename=''
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in COL.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Missing required exporter options')
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**options)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))
assert delta<1e-4 and source['triangles']==glb['scene_triangles'] and not glb['errors']
assert glb['bytes']<=P['budgets']['max_glb_bytes']
# Public evidence names the portable artifact, not the invocation directory.
glb['file']='model.glb'
write(OUT/'qa/evidence/technical.json',{'status':'PASS','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','export_options':options,'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'blend_sha256':digest(OUT/'model.blend'),'axes':{'authoring_forward':'+X','authoring_up':'+Z','glb_forward':'+X','glb_up':'+Y'},'mounting':'Swimming trunk center at origin; lowest point is not ground contact','scope':'Source and static exported geometry only. Not independent QA, GPU rendering or publication.'})
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'])
