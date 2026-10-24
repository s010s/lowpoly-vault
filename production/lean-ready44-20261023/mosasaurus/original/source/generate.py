# SPDX-License-Identifier: MIT
"""Original deterministic Mosasaurus missouriensis living reconstruction.
Run in Blender background with -- --output-dir DEST. All dependencies are local.
Coordinates: X forward, Z up. Anatomical inference is recorded in brief.json.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,default=HERE.parent); a=ap.parse_args(args)
out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True); (out/'qa/evidence').mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
C=setup_scene('mosasaurus',seed=P['seed']); root=bpy.data.objects[C['asset_root']]
root['authoring_forward']='+X'; root['mount_origin']=P['mount_origin']; root['taxon']=P['taxon']
M={k:make_material(k,v,roughness=.83 if k!='features' else .48) for k,v in P['palette'].items()}

def mesh(name,V,F,matkeys,indices=None):
    ob=mesh_object(name,V,F,[M[k] for k in matkeys],C)
    if indices:
        for p,i in zip(ob.data.polygons,indices): p.material_index=i
    return ob

def loft(name,stations,matkeys,selector,N=20,transform=None):
    # Stations are x, y center, z center, y radius, upper z radius, lower z radius.
    V=[]; F=[]; I=[]
    for x,y,z,w,up,dn in stations:
        for j in range(N):
            t=2*math.pi*j/N; s=math.sin(t)
            v=(x,y+w*math.cos(t),z+(up if s>=0 else dn)*s)
            V.append(tuple(transform(Vector(v))) if transform else v)
    for k in range(len(stations)-1):
        for j in range(N):
            jj=(j+1)%N; q=(k*N+j,k*N+jj,(k+1)*N+jj,(k+1)*N+j)
            # Deliberate cross-section faceting; alternate diagonals avoid long stripes.
            fs=[(q[0],q[1],q[2]),(q[0],q[2],q[3])] if (k+j)%2==0 else [(q[0],q[1],q[3]),(q[1],q[2],q[3])]
            F.extend(fs); I.extend([selector(k,j,N)]*2)
    F.append(tuple(range(N-1,-1,-1))); I.append(selector(0,0,N))
    F.append(tuple((len(stations)-1)*N+j for j in range(N))); I.append(selector(len(stations)-2,0,N))
    return mesh(name,V,F,matkeys,I)

def body_mat(k,j,n):
    s=math.sin(2*math.pi*(j+.5)/n)
    return 0 if s>.42 else 2 if s<-.48 else 1
# Continuous musculature from tail peduncle through torso and short neck.
body=[(-2.81,0,-.12,.047,.09,.11),(-2.63,0,-.07,.065,.115,.15),(-2.36,0,-.015,.085,.15,.18),(-2.02,0,.025,.105,.18,.20),(-1.64,0,.055,.13,.225,.22),(-1.23,0,.065,.165,.26,.25),(-.84,0,.06,.22,.31,.30),(-.47,0,.055,.275,.35,.34),(-.10,0,.05,.34,.405,.395),(.28,0,.055,.415,.46,.44),(.69,0,.065,.45,.475,.475),(1.08,0,.075,.43,.455,.445),(1.43,0,.08,.375,.385,.365),(1.73,0,.085,.30,.31,.285),(1.97,0,.085,.22,.225,.205),(2.17,0,.075,.164,.155,.15),(2.36,0,.065,.145,.13,.12),(2.43,0,.06,.13,.12,.11)]
loft('Axial-trunk-neck-and-laterally-compressed-tail',body,['dorsal','flank','ventral'],body_mat,24)
# Broad posterior cranium and deep jaw adductors, narrowed into the long tooth-bearing rostrum.
head=[(2.27,0,.068,.18,.175,.12),(2.39,0,.065,.225,.215,.125),(2.51,0,.056,.22,.195,.105),(2.62,0,.043,.181,.153,.073),(2.77,0,.025,.141,.125,.055),(2.94,0,.012,.103,.102,.042),(3.10,0,.005,.071,.08,.033),(3.20,0,0,.05,.057,.028),(3.25,0,-.002,.030,.035,.024)]
def headmat(k,j,n):
    s=math.sin(2*math.pi*(j+.5)/n)
    return 0 if s>.45 else 2 if s<-.70 else 1
loft('Robust-upper-cranium-and-toothed-rostrum',head,['dorsal','flank','mouth'],headmat,24)
# Lower jaw opened modestly about the posterior jaw joint, never a giant shark gape.
angle=math.radians(P['jaw_open_degrees']); pivot=Vector((2.38,0,-.055)); R=Matrix.Rotation(angle,3,'Y')
def jawrot(v):return pivot+R@(v-pivot)
jaw=[(2.33,0,-.078,.169,.045,.077),(2.44,0,-.076,.20,.042,.078),(2.57,0,-.072,.177,.034,.068),(2.75,0,-.065,.133,.026,.051),(2.94,0,-.058,.093,.022,.041),(3.10,0,-.05,.065,.019,.03),(3.22,0,-.046,.035,.015,.024)]
def jawmat(k,j,n):
    s=math.sin(2*math.pi*(j+.5)/n)
    return 2 if s>.45 else 1 if s<-.30 else 0
loft('Continuous-open-mandible',jaw,['flank','ventral','mouth'],jawmat,20,jawrot)
# Four thick hydrofoil paddles. Positive determinants; mirrored coordinates are wound by the helper.
def paddle(name,side,front):
    x=1.64 if front else -.18; y=.27 if front else .24
    length=.80 if front else .68; chord=.34 if front else .29
    st=[(0,0,.75,.070),(.19,-.045,1,.060),(.44,-.105,.92,.045),(.70,-.20,.71,.030),(.91,-.27,.39,.018),(1,-.28,.12,.008)]
    V=[]; F=[]; n=12
    for t,sweep,cf,h in st:
        for j in range(n):
            q=2*math.pi*j/n
            V.append((x+sweep+chord*.5*cf*math.cos(q),side*(y+length*t),-.14-.13*t+h*math.sin(q)))
    for k in range(len(st)-1):
        for j in range(n):
            q=(k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j);F.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3])])
    F.extend([tuple(range(n-1,-1,-1)),tuple((len(st)-1)*n+j for j in range(n))])
    return mesh(name,V,F,['flank'])
for side,label in [(-1,'right'),(1,'left')]:
    paddle('Fore-paddle-'+label,side,True);paddle('Hind-paddle-'+label,side,False)
# Vertically compressed in Y, not a horizontal cetacean fluke. Lower lobe longer.
# Perimeter + two gently inflated interior rings create a solid, closed soft-tissue tail fin.
outline=[(-2.54,.065),(-2.67,.235),(-2.80,.40),(-2.98,.55),(-3.13,.60),(-3.11,.42),(-3.04,.21),(-2.99,.015),(-3.08,-.22),(-3.25,-.50),(-3.24,-.78),(-3.10,-.69),(-2.96,-.47),(-2.83,-.30),(-2.65,-.20)]
center=Vector((-2.86,0,-.005)); V=[]; n=len(outline)
for x,z in outline:V.append((x,0,z))
for sign in (-1,1):
    for x,z in outline:
        V.append((center.x+.58*(x-center.x),sign*.055,center.z+.58*(z-center.z)))
    V.append((center.x,sign*.073,center.z))
F=[]
for si in range(2):
    base=n+si*(n+1); c=base+n
    for j in range(n):
        q=(j,(j+1)%n,base+(j+1)%n,base+j)
        F.extend([(q[0],q[1],q[2]),(q[0],q[2],q[3]),(base+j,base+(j+1)%n,c)])
mesh('Inferred-hypocercal-tail-fin',V,F,['dorsal'])
# Small faceted bilateral eyes and dorsolateral nares, grouped without extra draw calls.
FV=[];FF=[]
def ellipsoid(center,radii,longitude=12,latitude=6):
    b=len(FV); FV.append((center[0],center[1],center[2]+radii[2]))
    for k in range(1,latitude):
        p=math.pi*k/latitude
        for j in range(longitude):
            t=2*math.pi*j/longitude
            FV.append((center[0]+radii[0]*math.sin(p)*math.cos(t),center[1]+radii[1]*math.sin(p)*math.sin(t),center[2]+radii[2]*math.cos(p)))
    end=len(FV);FV.append((center[0],center[1],center[2]-radii[2]))
    for j in range(longitude):FF.append((b,b+1+j,b+1+(j+1)%longitude))
    for k in range(latitude-2):
        for j in range(longitude):
            v=b+1+k*longitude+j;w=b+1+k*longitude+(j+1)%longitude
            FF.extend([(v,w,w+longitude),(v,w+longitude,v+longitude)])
    last=b+1+(latitude-2)*longitude
    for j in range(longitude):FF.append((last+j,end,last+(j+1)%longitude))
for side in (-1,1):
    ellipsoid((2.59,side*.173,.120),(.055,.022,.039))
    ellipsoid((2.89,side*.063,.092),(.031,.014,.011),10,4)
mesh('Bilateral-eyes-and-nares',FV,FF,['features'])
# Recurved conical marginal dentition reaches the tip, with no Tylosaurus-style knob.
TV=[];TF=[]
def tooth(base,length,radius,direction):
    axis=Vector((-.18,0,direction)).normalized(); u=Vector((0,1,0)); v=axis.cross(u).normalized(); b=len(TV); base=Vector(base); n=7
    for t,r in [(0,radius),(.62,radius*.48)]:
        mid=base+axis*length*t+Vector((-.010*t*t,0,0))
        for j in range(n):
            q=2*math.pi*j/n;TV.append(tuple(mid+r*(u*math.cos(q)+v*math.sin(q))))
    tip=len(TV);TV.append(tuple(base+axis*length+Vector((-.013,0,0))))
    for j in range(n):
        k=(j+1)%n;TF.extend([(b+j,b+k,b+n+k),(b+j,b+n+k,b+n+j),(b+n+j,b+n+k,tip)])
    TF.append(tuple(b+j for j in range(n-1,-1,-1)))
def interp(st,x,col):
    for l,r in zip(st,st[1:]):
        if l[0]<=x<=r[0]:
            t=(x-l[0])/(r[0]-l[0]);return l[col]*(1-t)+r[col]*t
    return st[-1][col]
for side in (-1,1):
    for k in range(P['simplified_teeth_per_jaw_side']):
        t=k/(P['simplified_teeth_per_jaw_side']-1);x=2.53+t*.655
        width=interp(head,x,3); cz=interp(head,x,2);dn=interp(head,x,5)
        size=.036+.018*math.sin(math.pi*t)
        tooth((x,side*width*.83,cz-dn*.59),size,.012*(.7+.3*math.sin(math.pi*t)),-1)
        xj=2.55+t*.63;w=interp(jaw,xj,3);z=interp(jaw,xj,2)
        pos=jawrot(Vector((xj,side*w*.82,z+.012)))
        tooth(pos,size*.84,.0105*(.7+.3*math.sin(math.pi*t)),1)
mesh('Marginal-dentition-56-simplified-cones',TV,TF,['tooth'])
bpy.context.view_layer.update()
source=audit_source(C,max_triangles=24000)
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
# Save only relative output destinations; scrub startup file-browser storage.
bpy.context.scene.render.filepath='//render.png'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b' ' * 1023
                space.params.directory=b'//'
                space.params.filename=' ' * 255
                space.params.filename='model.blend'
bpy.context.scene['author']='Leon Made This / s010s';bpy.context.scene['license']='CC-BY-4.0'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in C.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Missing explicit exporter options')
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
glb=audit_glb(out/'model.glb',max_triangles=24000,max_materials=6,max_primitives=16)
glb['file']='model.glb'
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>2500000:raise RuntimeError('GLB bytes budget exceeded')
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))
if delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export mismatch')
save(out/'qa/evidence/technical.json',{'asset_id':'mosasaurus','revision':'r001','status':'PASS','scope':'Source and static GLB geometry only; no GPU, population or independent visual approval','glb_sha256':sha(out/'model.glb'),'source':source,'glb':glb,'bounds_max_error_m':delta,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'gltf_exporter_version':P['gltf_exporter_version'],'consumer_three_version':P['consumer_three_version'],'export_options':options,'axes':{'blender_forward':'+X','blender_up':'+Z','glb_forward':'+X','glb_up':'+Y'},'origin':P['mount_origin'],'topology_review':'Each solid semantic part closed and outward-wound by bmesh. Eyes, teeth, paddle roots, cranial neck and tail fin deliberately intersect as fleshed assembly; not a boolean-printable union.','reviewed_source_warnings':['Swimming mount, no floor contact; negative minimum Z is intentional.'],'reconstruction_limits':'Different same-species specimens combined; adult overall/head scale approximate conference abstract values; tail-fin skin and all color inferred.'})
print('MODEL_BUILD_COMPLETE',sha(out/'model.glb'),glb['scene_triangles'],glb['scene_primitives_estimated_base_draw_calls'])
