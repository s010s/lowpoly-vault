# SPDX-License-Identifier: MIT
"""Deterministic original Trigonotarbus johnsoni; Blender 4.3.2.
Run from any directory: blender -b --factory-startup -t 2 --python generate.py -- --output OUTPUT.
Published body dimensions refer only to scanned NHMUK I.15860. Pose, thickness,
color and missing limb completion are interpretations, not preserved anatomy.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb, read_glb, semantic_digest
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output',default='.'); A=ap.parse_args(args)
OUT=Path(A.output).resolve(); OUT.mkdir(parents=True,exist_ok=True)
E=OUT/'qa'/'evidence'; E.mkdir(parents=True,exist_ok=True)
C=setup_scene(P['asset_id'],P['seed']); root=bpy.data.objects[C['asset_root']]
M={k:make_material(k,c,roughness=.84 if k!='median_eyes' else .42) for k,c in P['palette'].items()}
parts=[]

def write_json(path,data): path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def mesh(name,vs,fs,material,kind):
    o=mesh_object(name,[(x*.001,y*.001,z*.001) for x,y,z in vs],fs,M[material],C)
    o['anatomy']=kind; o['reconstruction']='original procedural interpretation'; parts.append(o)
    return o

def interp(table,y,col=1):
    if y<=table[0][0]: return table[0][col]
    for a,b in zip(table,table[1:]):
        if y<=b[0]: return a[col]+(b[col]-a[col])*(y-a[0])/(b[0]-a[0])
    return table[-1][col]

# Curved axial lofts, not stock sphere assemblies. Each is a closed solid.
def loft(name,rows,n,material,kind):
    vs=[]
    for y,w,zc,h in rows:
        for i in range(n):
            a=2*math.pi*i/n; vs.append((w*math.cos(a),y,zc+h*math.sin(a)))
    fs=[]
    for r in range(len(rows)-1):
        for i in range(n): fs.append((r*n+i,r*n+(i+1)%n,(r+1)*n+(i+1)%n,(r+1)*n+i))
    fs.extend([tuple(reversed(range(n))),tuple((len(rows)-1)*n+i for i in range(n))])
    return mesh(name,vs,fs,material,kind)

# A thin plate spanning two parameter intervals over a curved surface.
def patch(name,y0,y1,u0,u1,surface,material,kind,ny=3,nu=6,thick=.065):
    vs=[]
    for bottom in [False,True]:
        for j in range(ny+1):
            y=y0+(y1-y0)*j/ny
            for i in range(nu+1):
                u=u0+(u1-u0)*i/nu; x,z=surface(y,u)
                vs.append((x,y,z-(thick if bottom else 0)))
    N=(ny+1)*(nu+1); fs=[]
    for j in range(ny):
        for i in range(nu):
            a=j*(nu+1)+i; fs.append((a,a+1,a+nu+2,a+nu+1)); fs.append((a+N,a+nu+1+N,a+nu+2+N,a+1+N))
    boundary=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,ny+1)]+[ny*(nu+1)+i for i in reversed(range(nu))]+[j*(nu+1) for j in reversed(range(1,ny))]
    for a,b in zip(boundary,boundary[1:]+boundary[:1]): fs.append((a,b,b+N,a+N))
    return mesh(name,vs,fs,material,kind)

abd=[(-.35,1.43,1.28,.57),(.10,1.66,1.32,.68),(.75,1.80,1.35,.74),(1.25,1.77,1.34,.73),(1.75,1.62,1.29,.70),(2.20,1.37,1.23,.63),(2.55,1.08,1.15,.52),(2.85,.72,1.06,.38),(3.10,.30,.98,.20),(3.15,.12,.98,.13)]
loft('opisthosoma_substrate',abd,20,'ventral_cuticle','entire rounded abdomen without pedicel or tail')
def dorsal(y,u):
    w=interp(abd,y,1); z=interp(abd,y,2)+interp(abd,y,3)*math.sqrt(max(0,1-u*u))+.045
    return w*u,z
bands=[(1,-.45,-.22),(2,-.20,.20),(3,.24,.66),(4,.70,1.10),(5,1.14,1.54),(6,1.58,1.97),(7,2.01,2.36),(8,2.40,2.75),(9,2.79,3.15)]
for n,a,b in bands:
    if n in (1,9):
        patch(f'tergite_{n:02}_undivided',a,b,-.98,.98,(lambda y,u:(dorsal(y,u)[0],dorsal(y,u)[1]-.10)) if n==1 else dorsal,'dorsal_plates',f'T{n}: '+('ridge partly tucked beneath carapace' if n==1 else 'narrow undivided terminal tergite'),ny=2,nu=14)
    else:
        patch(f'tergite_{n:02}_central',a,b,-.66,.66,dorsal,'dorsal_plates',f'T{n} central plate; T2 and T3 not fused',ny=3,nu=8)
        for s in (-1,1):
            patch(f'tergite_{n:02}_lateral_{"L" if s<0 else "R"}',a,b,(-.98 if s<0 else .685),(-.685 if s<0 else .98),dorsal,'lateral_plates',f'T{n} lateral plate',ny=3,nu=3)

# Broad triangular carapace; the small rounded clypeus belongs to its outline.
car=[(-3.15,.09,1.62,.20),(-3.00,.22,1.56,.35),(-2.70,.32,1.53,.40),(-2.35,.57,1.42,.47),(-1.90,.86,1.32,.54),(-1.40,1.12,1.25,.61),(-.90,1.35,1.20,.67),(-.45,1.44,1.19,.70),(-.35,1.42,1.18,.69)]
shield=loft('triangular_carapace',car,20,'carapace','smooth unlobed triangular carapace with raised median region')
# Recess the dorsal centerline behind the eyes and the posterior transverse row.
for v in shield.data.vertices:
    x,y,z=(c*1000 for c in v.co)
    if y>=-2.36 and z>1.5 and abs(x)<.01: v.co.z-=.000065
    if abs(y+.45)<.001 and z>1.20: v.co.z-=.000045
# Median ridge is expressed in profile and a narrow recessed inverted-T sulcus.
def car_top(y,x):
    w=interp(car,y,1); return interp(car,y,2)+interp(car,y,3)*math.sqrt(max(0,1-(x/w)**2))

def tube(name,points,radii,material,kind,sides=8):
    vs=[]
    for k,pt in enumerate(points):
        t=Vector(points[min(k+1,len(points)-1)])-Vector(points[max(0,k-1)])
        t.normalize(); guide=Vector((0,0,1)) if abs(t.z)<.92 else Vector((0,1,0)); a=t.cross(guide).normalized(); b=t.cross(a).normalized()
        for i in range(sides):
            ang=2*math.pi*i/sides; v=Vector(pt)+radii[k]*(math.cos(ang)*a+math.sin(ang)*b); vs.append(tuple(v))
    fs=[]
    for k in range(len(points)-1):
        for i in range(sides): fs.append((k*sides+i,k*sides+(i+1)%sides,(k+1)*sides+(i+1)%sides,(k+1)*sides+i))
    fs.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+i for i in range(sides))])
    return mesh(name,vs,fs,material,kind)

# Surface tracing of the sulcus is deliberately shallow, not a fictitious appendage.
tube('median_inverted_T_sulcus',[(0,y,car_top(y,0)-.055) for y in [-2.22,-1.85,-1.4,-.75,-.47]],[.022]*5,'ventral_cuticle','shallow inverted-T depression surface trace',sides=6)
tube('posterior_transverse_sulcus',[(x,-.46,car_top(-.46,x)-.044) for x in [-1.30,-.95,-.55,0,.55,.95,1.30]],[.022]*7,'ventral_cuticle','rear transverse groove',sides=6)

# Small close-set median eyes. No extra spider-like eye array.
for s in [-1,1]:
    x=s*.115; y=-2.55; z=car_top(y,x)
    vs=[(x,y,z+.080)]
    for j,rr,zz in [(0,.070,z+.035),(1,.060,z-.018)]:
        for i in range(8):
            a=2*math.pi*i/8; vs.append((x+rr*math.cos(a),y+rr*math.sin(a),zz))
    fs=[(0,1+i,1+(i+1)%8) for i in range(8)]+[(1+i,9+i,9+(i+1)%8,1+(i+1)%8) for i in range(8)]+[tuple(9+i for i in range(8))]
    mesh('median_eye_'+('L' if s<0 else 'R'),vs,fs,'median_eyes','closely spaced median eye')

# Four walking pairs. The six distal podomeres of leg IV retain published centerline lengths.
legdata=[]
angles=[[-65,-53,-57,-61,-64,-67],[-23,-24,-28,-31,-34,-36],[17,19,24,29,33,36],[49,60,67,73,78,82]]
roots=[(.48,-2.20,1.19),(.85,-1.68,1.15),(1.18,-1.10,1.10),(1.35,-.52,1.06)]
lengths4=[.8,1.1,.8,.9,.3,.8]
podomeres=['trochanter','femur','patella','tibia','metatarsus','tarsus']
for n,(r,aa) in enumerate(zip(roots,angles),1):
    lengths=[v*([.93,.97,1.0,1.0][n-1]) for v in lengths4]
    dzbase=[.24,.06,-.10,-.46,-.49,-.35]
    correction=(.065-r[2]-sum(l*z for l,z in zip(lengths,dzbase)))/sum(lengths)
    for s in [-1,1]:
        start=Vector((s*r[0],r[1],r[2])); pts=[tuple(start)]
        for l,deg,dz in zip(lengths,aa,dzbase):
            z=dz+correction; xy=math.sqrt(1-z*z); a=math.radians(deg)
            start+=Vector((s*math.cos(a)*xy,math.sin(a)*xy,z))*l; pts.append(tuple(start))
        for j,(a,b) in enumerate(zip(pts,pts[1:])):
            a,b=Vector(a),Vector(b); d=b-a
            r0=[.205,.205,.172,.149,.108,.095][j]
            rr=[r0*.78,r0,r0*.86,r0*(.32 if j==5 else .66)]
            pp=[a,a+d*.15,a+d*.77,b]
            obj=tube(f'walking_leg_{n}_{"L" if s<0 else "R"}_{podomeres[j]}',[tuple(p) for p in pp],rr,'limbs',f'walking pair {n}, {podomeres[j]}')
            obj['centerline_length_m']=float(lengths[j]*.001)
        legdata.append({'pair':n,'side':'L' if s<0 else 'R','points_mm':pts,'podomeres_mm':lengths,'last_ring_center_z_mm':pts[-1][2]})

# Slender, non-load-bearing pedipalps point forward between walking legs I.
for s in [-1,1]:
    pts=[(s*.30,-2.63,1.28),(s*.47,-3.20,1.23),(s*.59,-3.80,1.08),(s*.62,-4.35,.95),(s*.68,-4.72,.82)]
    for j,(a,b) in enumerate(zip(pts,pts[1:])):
        a,b=Vector(a),Vector(b); d=b-a; r=[.110,.100,.085,.068][j]
        tube(f'pedipalp_{"L" if s<0 else "R"}_{j+1}',[tuple(a),tuple(a+d*.20),tuple(b)],[r*.82,r,r*.60],'limbs','slender pedipalp, not a fifth walking leg',sides=8)
    tube('chelicera_'+('L' if s<0 else 'R'),[(s*.14,-3.00,1.52),(s*.16,-3.05,1.22),(s*.145,-3.07,.88),(s*.08,-3.11,.76)],[.105,.110,.080,.046],'ventral_cuticle','small downward-hanging chelicera under clypeus',sides=8)

# Coxal wedges converge on a diamond-shaped sternum.
for n,(x,y,z) in enumerate(roots,1):
    for s in [-1,1]:
        vs=[(s*.18,y-.12,.64),(s*.18,y+.20,.64),(s*(x+.10),y+.18,.86),(s*(x+.10),y-.17,.94),(s*.18,y-.12,.78),(s*.18,y+.20,.78)]
        fs=[(0,1,2,3),(4,3,2,5),(0,3,4),(1,5,2),(0,4,5,1)]
        mesh(f'coxa_{n}_{"L" if s<0 else "R"}',vs,fs,'limbs',f'triangular coxa for walking leg {n}')
# Small diamond sternum forms a shallow attached underside plate, not a floating leaf.
def carapace_underside(y,x):
    w=interp(car,y,1); return interp(car,y,2)-interp(car,y,3)*math.sqrt(max(0,1-(x/w)**2))
stern_outline=[(0,-2.25),(.23,-1.65),(0,-.84),(-.23,-1.65)]
stern_vs=[(x,y,carapace_underside(y,x)-.060) for x,y in stern_outline]
stern_vs += [(0,-1.65,carapace_underside(-1.65,0)-.080)]
stern_vs += [(x,y,carapace_underside(y,x)+.075) for x,y in stern_outline]
stern_fs=[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(5,8,7,6)]
stern_fs += [(i,(i+1)%4,5+(i+1)%4,5+i) for i in range(4)]
mesh('diamond_sternum',stern_vs,stern_fs,'ventral_cuticle','small diamond sternum attached to ventral prosoma and medial coxae')
# Backward-curving sternites; these remain editable under the abdomen.
def ventral(y,u):
    w=interp(abd,y,1); z=interp(abd,y,2)-interp(abd,y,3)*math.sqrt(max(0,1-u*u))-.025
    return w*u,z
for n,(a,b) in enumerate([(-.31,.19),(.24,.74),(.79,1.29),(1.34,1.86),(1.91,2.40),(2.45,3.10)],4):
    # V-shaped-to-rounded posterior sweep made in the coordinate map, not extra rings.
    def curve(y,u,a=a,b=b):
        yp=y+.17*(1-u*u)*(1 if a>.6 else .45)
        yp=min(3.13,yp); return ventral(yp,u)
    # Explicit grid with y curvature and uniform thickness.
    ny,nu=2,12; vs=[]
    for layer in [0,1]:
        for j in range(ny+1):
            y=a+(b-a)*j/ny
            for i in range(nu+1):
                u=-.93+1.86*i/nu; yp=min(3.13,y+.17*(1-u*u)*(1 if a>.6 else .45)); x,z=ventral(yp,u); vs.append((x,yp,z+layer*.055))
    N=(ny+1)*(nu+1); fs=[]
    for j in range(ny):
        for i in range(nu):
            q=j*(nu+1)+i; fs += [(q,q+1,q+nu+2,q+nu+1),(q+N,q+nu+1+N,q+nu+2+N,q+1+N)]
    boundary=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,ny+1)]+[ny*(nu+1)+i for i in reversed(range(nu))]+[j*(nu+1) for j in reversed(range(1,ny))]
    fs += [(q,r,r+N,q+N) for q,r in zip(boundary,boundary[1:]+boundary[:1])]
    mesh('sternite_'+('09_10_fused' if n==9 else f'{n:02}'),vs,fs,'lateral_plates','posteriorly curved ventral sternite; terminal 9+10 interpreted fused' if n==9 else 'recurved ventral sternite')
# Ventral pygidium, a small flush patch, expressly not an external tail.
pygidium_rows=[(y,w,interp(abd,y,2)-interp(abd,y,3)-.005,h) for y,w,h in [(2.32,.055,.035),(2.42,.11,.045),(2.52,.055,.035)]]
loft('ventral_pygidium',pygidium_rows,8,'ventral_cuticle','small attached ventral pygidium near anterior fused sternite margin')

# Keep source root at footprint center; minimum intended walking-contact surface is floor.
bpy.context.view_layer.update()
lowest=min((o.matrix_world@v.co).z for o in parts for v in o.data.vertices)
for o in parts:
    for v in o.data.vertices: v.co.z-=lowest
bpy.context.view_layer.update()
source=audit_source(C,max_triangles=40000)
write_json(E/'source-audit.json',source)
if source['errors']: raise RuntimeError('Source audit failed: '+'; '.join(source['errors']))
# Measured semantic anatomy, independent of the declared dimensions above.
def object_bounds(name):
    obj=bpy.data.objects[name]; pts=[obj.matrix_world@v.co for v in obj.data.vertices]
    lo=[min(p[i] for p in pts) for i in range(3)]; hi=[max(p[i] for p in pts) for i in range(3)]
    return {'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]}
cb=object_bounds('triangular_carapace'); ab=object_bounds('opisthosoma_substrate')
measured={'carapace_length_m':cb['size'][1],'abdomen_length_m':ab['size'][1],'abdomen_width_m':ab['size'][0],'combined_body_length_m':ab['max'][1]-cb['min'][1]}
for key,target in [('carapace_length_m',.0028),('abdomen_length_m',.0035),('abdomen_width_m',.0036),('combined_body_length_m',.0063)]: assert abs(measured[key]-target)<1e-8
names=[o.name for o in parts]
checks={'four_walking_pairs_with_six_podomeres_each':sum(n.startswith('walking_leg_') for n in names)==48,'separate_palps':sum(n.startswith('pedipalp_') for n in names)==8,'separate_chelicerae':sum(n.startswith('chelicera_') for n in names)==2,'seven_tripartite_tergites_2_to_8':sum(n.startswith('tergite_') and '_lateral_' in n for n in names)==14,'single_undivided_T9':'tergite_09_undivided' in names and not any(n.startswith('tergite_09_lateral') for n in names),'T2_and_T3_separate':all('tergite_'+n+'_central' in names for n in ['02','03']),'T1_overlaps_posterior_carapace':object_bounds('tergite_01_undivided')['min'][1]<cb['max'][1],'fused_terminal_ventral_sternite':'sternite_09_10_fused' in names and 'sternite_09' not in names,'small_ventral_pygidium':'ventral_pygidium' in names}
assert all(checks.values())
write_json(E/'measured-anatomy.json',{'status':'PASS_GEOMETRY_CHECKS_ONLY','checks':checks,'measured_dimensions_m':measured,'carapace_bounds_m':cb,'abdomen_bounds_m':ab,'source_python_version':sys.version,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'inference':'Symmetry, absent distal limbs, depth, pose and muted palette are reconstructed; dimensions are the scanned specimen, never the holotype.','limitations':'These checks inspect source semantic geometry; species identity and visual craft remain for independent review.'})
for o in parts:
    o['source_semantic_part']=o.name
bpy.context.scene['scientific_anchor']='NHMUK I.15860, body 6.3 mm; holotype measurements excluded'
bpy.context.scene['artist_inference']='Living depth, symmetric completion, pose and color'
bpy.context.preferences.filepaths.save_version=0
# Keep saved presentation defaults portable and free of machine directories.
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if hasattr(space,'params') and space.params and hasattr(space.params,'directory'): space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
# Export six material batches. Editable semantic objects remain separate in .blend.
batches=[]
for name,mat in M.items():
    group=[o for o in C.all_objects if o.type=='MESH' and o.data.materials[0]==mat]
    if not group: continue
    bpy.ops.object.select_all(action='DESELECT')
    for o in group: o.select_set(True)
    bpy.context.view_layer.objects.active=group[0]
    if len(group)>1: bpy.ops.object.join()
    o=bpy.context.view_layer.objects.active; o.name='export_'+name
    o['semantic_parts']=[p for p in source['parts'] if any(p['name']==g.name for g in [])] if False else 'See editable source and anatomy evidence'
    batches.append(o)
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects: o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing: raise RuntimeError('Missing required export options: '+repr(missing))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',40000,6,8,ground_tolerance=1e-7); glb['file']='model.glb'
write_json(E/'glb-audit.json',glb)
if glb['errors']: raise RuntimeError('GLB audit failed: '+'; '.join(glb['errors']))
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
assert delta<1e-8 and source['triangles']==glb['scene_triangles']
assert glb['bytes']<=8388608
write_json(E/'anatomy-and-build.json',{'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'seed':P['seed'],'body_dimensions_mm':{'length':6.3,'carapace_length':2.8,'opisthosoma_length':3.5,'opisthosoma_width':3.6},'source_specimen':'NHMUK I.15860','excluded_measurement':'4.8 mm holotype NHMUK In31239','walking_leg_pairs':4,'pedipalp_pairs':1,'chelicera_pairs':1,'tergites':{'1':'ridge partly covered by carapace','2_to_8':'each central plus left/right lateral plate, T2 and T3 distinct','9':'single undivided narrow plate'},'leg_centerlines':legdata,'floor_shift_m':-lowest,'source_export_bounds_max_error_m':delta,'source_editable_objects':len(source['parts']),'export_options':{k:v for k,v in options.items() if k!='filepath'},'semantic_digest':glb['semantic_sha256'] if 'semantic_sha256' in glb else semantic_digest(*read_glb(OUT/'model.glb')[:2]),'scope':'Source/format/semantic anatomy checks, not independent visual, GPU, scene, user or deployment approval.'})
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
