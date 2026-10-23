# SPDX-License-Identifier: MIT
"""Original Coelacanthus granulatus reconstruction. Blender 4.3.2, meters.
Rebuild: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
No research image or mesh is loaded. All geometric dimensions are explicit below.
"""
import sys, json, math, hashlib, argparse
from pathlib import Path
from mathutils import Vector
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

P=json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=HERE.parent)
a=ap.parse_args(argv); OUT=a.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
C=setup_scene('coelacanthus',P['seed'])
root=bpy.data.objects[C['asset_root']]
root['authoring_forward']='-X'; root['glTF_forward']='-X'; root['mount']='Axial swim center at origin; no seabed contact'
root['taxon']='Coelacanthus granulatus'; root['soft_tissues']='Conservative inferred living reconstruction'
M=[make_material('Dorsal slate','#596B71',.72),make_material('Flank pewter','#84918D',.66),make_material('Ventral warm gray','#B0ACA0',.74),make_material('Fin rays and membrane','#7B8985',.73),make_material('Seams and pupil','#283336',.42),make_material('Muted bronze iris','#8C8460',.47)]
verts=[]; faces=[]; mats=[]; groups={}; smooth=[]
def add(name,vs,fs,mi,smooth_faces=False):
    o=len(verts); verts.extend(tuple(x) for x in vs); faces.extend(tuple(o+i for i in f) for f in fs)
    mats.extend(mi if isinstance(mi,list) else [mi]*len(fs)); smooth.extend([smooth_faces]*len(fs)); groups.setdefault(name,[]).extend(range(o,len(verts)))

def ellipsoid(name,center,scale,mi,segments=16,rings=8,smooth_faces=True):
    c=Vector(center); vs=[tuple(c+Vector((0,0,scale[2])))]; fs=[]
    for j in range(1,rings):
        t=math.pi*j/rings
        for k in range(segments):
            p=2*math.pi*k/segments; vs.append(tuple(c+Vector((scale[0]*math.sin(t)*math.cos(p),scale[1]*math.sin(t)*math.sin(p),scale[2]*math.cos(t)))))
    bottom=len(vs); vs.append(tuple(c-Vector((0,0,scale[2]))))
    for k in range(segments): fs.append((0,1+k,1+(k+1)%segments))
    for j in range(rings-2):
        for k in range(segments):
            u=1+j*segments+k; v=1+j*segments+(k+1)%segments; fs.append((u,u+segments,v+segments,v))
    for k in range(segments): fs.append((bottom,1+(rings-2)*segments+(k+1)%segments,1+(rings-2)*segments+k))
    add(name,vs,fs,mi,smooth_faces)

def tube(name,points,radii,mi,n=7):
    vs=[]; fs=[]
    for j,p in enumerate(points):
        p=Vector(p); tangent=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(0,j-1)])
        tangent.normalize(); temp=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0)); u=tangent.cross(temp).normalized(); v=tangent.cross(u).normalized()
        for k in range(n): vs.append(tuple(p+radii[j]*(math.cos(k*2*math.pi/n)*u+math.sin(k*2*math.pi/n)*v)))
    fs.append(tuple(reversed(range(n))))
    for j in range(len(points)-1):
        for k in range(n): fs.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    fs.append(tuple((len(points)-1)*n+k for k in range(n))); add(name,vs,fs,mi,True)

# Axial silhouette knots: x, half-width, dorsal elevation, ventral elevation.
knots=[(-.300,.003,.007,-.009),(-.293,.012,.018,-.019),(-.279,.020,.030,-.029),(-.257,.026,.042,-.038),(-.231,.030,.051,-.045),(-.205,.034,.057,-.052),(-.177,.038,.063,-.059),(-.145,.041,.066,-.064),(-.106,.0425,.0675,-.0675),(-.06,.041,.065,-.065),(-.012,.037,.060,-.058),(.04,.031,.051,-.048),(.085,.025,.041,-.037),(.127,.019,.032,-.027),(.165,.012,.022,-.019),(.196,.008,.014,-.012),(.234,.0045,.008,-.007),(.270,.0018,.0035,-.0035)]
def section(x):
    for k in range(len(knots)-1):
        if knots[k][0]<=x<=knots[k+1][0]:
            t=(x-knots[k][0])/(knots[k+1][0]-knots[k][0]); return tuple(knots[k][i]*(1-t)+knots[k+1][i]*t for i in (1,2,3))
    return tuple(knots[-1][i] for i in (1,2,3))
def surface(x,t,offset=0):
    w,d,v=section(x); zc=(d+v)/2; h=(d-v)/2
    return Vector((x,(w+offset)*math.cos(t),zc+(h+offset)*math.sin(t)))
xs=[]
for q in range(len(knots)-1):
    count=max(1,math.ceil((knots[q+1][0]-knots[q][0])/.014))
    xs += [knots[q][0]+(knots[q+1][0]-knots[q][0])*j/count for j in range(count)]
xs.append(knots[-1][0]); N=28; vs=[];fs=[];mi=[]
for x in xs:
    for j in range(N): vs.append(surface(x,2*math.pi*j/N))
fs.append(tuple(reversed(range(N))));mi.append(1)
for i in range(len(xs)-1):
    for j in range(N):
        fs.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j)); s=math.sin((j+.5)*2*math.pi/N)
        mi.append(0 if s>.53 else 2 if s<-.59 else 1)
fs.append(tuple((len(xs)-1)*N+j for j in range(N))); mi.append(1)
add('Axial_body_and_elongated_head',vs,fs,mi,True)

# Low-relief scales use original geometric relief, never image textures.
for row in range(16):
    x=-.135+row*.018
    for k in range(14):
        t=2*math.pi*k/14+(row%2)*math.pi/14; xx=x+.003*math.cos(t)
        # Small closed lenticular shield; maximum relief 0.35 mm.
        ring=[surface(xx-.007,t,0.00005),surface(xx-.001,t+.09,0.00005),surface(xx+.008,t,0.00005),surface(xx-.001,t-.09,0.00005)]
        top=surface(xx+.001,t,.00040); back=surface(xx,t,-.0004)
        v=ring+[top,back]; f=[(i,(i+1)%4,4) for i in range(4)]+[((i+1)%4,i,5) for i in range(4)]
        s=math.sin(t); add('Subtle_dermal_scale_relief',v,f,0 if s>.53 else 2 if s<-.59 else 1,False)

# Solid fan membranes with ridged rays. Boundary points are the distal arc,
# the final arc ends at the trailing root. No zero-thickness sheets.
def fan(name,rootp,arc,normal,halfthick=.0009,mi=3,rays=True):
    r=Vector(rootp); n=Vector(normal).normalized(); arc=[Vector(x) for x in arc]; vs=[];fs=[]; steps=[0,.30,.68,1]
    # Separate positive/negative sheets use a root vertex then radial rings.
    for side in (1,-1):
        vs.append(tuple(r+n*side*halfthick))
        for t in steps[1:]:
            for i,p in enumerate(arc):
                bump=(1+.3*(i%2==0)*(1-t))*(1-.70*t)
                vs.append(tuple(r.lerp(p,t)+n*side*halfthick*bump))
    A=len(arc); S=1+3*A
    for off in (0,S):
        for j in range(A-1): fs.append((off,off+1+j,off+1+j+1))
        for k in range(2):
            for j in range(A-1): fs.append((off+1+k*A+j,off+1+(k+1)*A+j,off+1+(k+1)*A+j+1,off+1+k*A+j+1))
    # Close perimeter along leading, trailing and distal edges.
    perimeter=[0,1,1+A,1+2*A]+[1+2*A+j for j in range(1,A)]+[1+A+A-1,1+A-1]
    for j,u in enumerate(perimeter): v=perimeter[(j+1)%len(perimeter)];fs.append((u,v,S+v,S+u))
    add(name+'_membrane',vs,fs,mi,False)
    if rays:
        for j,p in enumerate(arc):
            if j==len(arc)-1: continue
            pts=[r.lerp(p,t) for t in (.13,.45,.73,.97)]
            tube(name+'_rays',pts,[.0014,.0011,.00075,.00035],mi,6)

# Anterior dorsal is a direct ray sail without a fleshy basal lobe.
fan('Anterior_dorsal_unlobed',(-.079,0,.057),[(-.087,0,.073),(-.079,0,.089),(-.066,0,.104),(-.050,0,.109),(-.032,0,.105),(-.016,0,.095),(-.003,0,.082),(.007,0,.064),(.004,0,.052)],(0,1,0),.0011)
# Posterior dorsal has a separate fleshy basal lobe, visibly smaller than first.
tube('Posterior_dorsal_fleshy_lobe',[(.085,0,.034),(.099,0,.044),(.109,0,.052)],[.008,.007,.005],0,10)
fan('Posterior_dorsal_lobed',(.107,0,.050),[(.091,0,.066),(.105,0,.084),(.121,0,.098),(.139,0,.101),(.154,0,.093),(.164,0,.079),(.163,0,.067),(.148,0,.056),(.121,0,.046)],(0,1,0),.001)
# Pectoral and pelvic pairs are truly paired, low-lobed and splayed modestly.
for s in (-1,1):
    name='Left' if s<0 else 'Right'
    tube(name+'_pectoral_fleshy_lobe',[(-.136,s*.031,-.036),(-.125,s*.038,-.043),(-.116,s*.043,-.049)],[.009,.010,.0065],1,10)
    fan(name+'_pectoral',(-.116,s*.043,-.049),[(-.116,s*.052,-.055),(-.107,s*.063,-.064),(-.093,s*.071,-.073),(-.073,s*.076,-.077),(-.053,s*.074,-.071),(-.049,s*.062,-.061),(-.063,s*.049,-.051),(-.086,s*.042,-.046)],(0,s*.63,-.78),.0012)
    tube(name+'_pelvic_fleshy_lobe',[(.006,s*.018,-.047),(.017,s*.025,-.061),(.027,s*.031,-.067)],[.008,.008,.0055],1,10)
    fan(name+'_pelvic',(.023,s*.030,-.063),[(.020,s*.035,-.072),(.029,s*.043,-.084),(.044,s*.050,-.093),(.060,s*.050,-.096),(.073,s*.042,-.087),(.073,s*.034,-.077),(.058,s*.028,-.065),(.039,s*.026,-.058)],(0,s*.76,-.65),.001)
ellipsoid('Anal_fleshy_lobe',(.112,0,-.035),(.019,.006,.010),1,14,6)
fan('Anal_lobed',(.118,0,-.043),[(.119,0,-.055),(.135,0,-.070),(.151,0,-.080),(.168,0,-.081),(.180,0,-.072),(.182,0,-.058),(.164,0,-.044),(.139,0,-.033)],(0,1,0),.001)
# Three lobes, broad upper/lower rounded fans and a short central axial tip.
fan('Caudal_upper',(.163,0,.010),[(.160,0,.025),(.194,0,.043),(.215,0,.058),(.239,0,.067),(.258,0,.066),(.273,0,.057),(.281,0,.043),(.282,0,.028),(.273,0,.014),(.250,0,.006)],(0,1,0),.00115)
fan('Caudal_lower',(.163,0,-.008),[(.160,0,-.021),(.195,0,-.040),(.217,0,-.056),(.239,0,-.064),(.259,0,-.063),(.274,0,-.054),(.282,0,-.040),(.283,0,-.025),(.273,0,-.012),(.250,0,-.005)],(0,1,0),.00115)
fan('Caudal_axial_terminal',(.257,0,0),[(.278,0,.006),(.287,0,.013),(.296,0,.010),(.300,0,0),(.296,0,-.010),(.287,0,-.012),(.278,0,-.005)],(0,1,0),.0012)

# Lateral eyes, a restrained mouth crease and opercular joint. No teeth.
for s in (-1,1):
    name='Left' if s<0 else 'Right'; x=-.249; z=.018; yy=s*.0254
    ellipsoid(name+'_orbital_rim',(x,yy,z),(.014,.005,.0138),0,20,10)
    ellipsoid(name+'_eye_iris',(x,yy+s*.0034,z),(.0114,.0034,.0112),5,20,10)
    ellipsoid(name+'_eye_pupil',(x-.001,yy+s*.0062,z+.0005),(.0077,.0017,.0077),4,20,10)
    tube(name+'_closed_mouth',[(-.297,s*.007,-.009),(-.285,s*.017,-.015),(-.267,s*.023,-.020),(-.245,s*.026,-.023),(-.220,s*.030,-.021)],[.00065,.0008,.00085,.00085,.0004],4,6)
    # Opercular boundary follows the curved head rather than a straight dark slash.
    ps=[]
    for x,t in [(-.147,.91),(-.138,.59),(-.132,.23),(-.131,-.15),(-.136,-.54),(-.147,-.86)]:
        p=surface(x,t,.0007);p.y*=s;ps.append(p)
    tube(name+'_opercular_seam',ps,[.00055]*len(ps),4,6)
    ellipsoid(name+'_naris',(-.282,s*.017,.008),(.0015,.0006,.0012),4,10,6)

ob=mesh_object('Coelacanthus_editable_semantic_mesh',verts,faces,M,C)
for i,p in enumerate(ob.data.polygons): p.material_index=mats[i];p.use_smooth=smooth[i]
for name,inds in groups.items(): ob.vertex_groups.new(name=name).add(inds,1,'REPLACE')
ob['construction']='Profile loft, closed fin fans, paired lobes, subtle original scale relief; vertex groups retain editable semantic parts'
source=audit_source(C,40000)
if source['errors']: save(OUT/'source-failed.json',source); raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(opts)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Missing exporter options '+repr(missing))
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(OUT/'model.glb',40000,6,8)
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in ('min','max') for i in range(3))
if glb['errors'] or delta>1e-5 or glb['scene_triangles']!=source['triangles']:raise RuntimeError('Export QA failed')
report={'status':'PASS','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'semantic_parts':list(groups),'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(OUT/'model.blend'),'export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_scene_free_of_cameras_and_lights':not any(o.type in ('CAMERA','LIGHT') for o in bpy.context.scene.objects),'runtime_scope':'CPU build and static GLB audit only; not GPU or populated scene','reviewed_warnings':['Smooth body, orbital surfaces and slender rays intentional; faceted membranes and scale relief intentional.','Swim mount is axial center; negative Z is correct, not failed floor contact.','Anatomical attachments deliberately overlap. Not a printable boolean union.'],'materials':[{'name':m.name,'srgb':m['palette_srgb']} for m in M]}
save(OUT/'build-report.json',report)
print('BUILD_COMPLETE '+json.dumps({'glb_sha256':glb['sha256'],'semantic_sha256':glb['semantic_sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes']}))
