# SPDX-License-Identifier: MIT
"""Original Palaeotarbus jerami reconstruction anchored to K25850.
Run: blender -b --factory-startup -t 2 --python generate.py -- --output OUTPUT
SI-scale original geometry. Body length is a scale-bar estimate, not a published
measurement; missing appendages follow the same-taxon Dunlop 1996 restoration.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
ap=argparse.ArgumentParser();ap.add_argument('--output',default='.')
A=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=Path(A.output).resolve();OUT.mkdir(parents=True,exist_ok=True)
E=OUT/'qa/evidence';E.mkdir(parents=True,exist_ok=True)
C=setup_scene(P['asset_id'],P['seed']);root=bpy.data.objects[C['asset_root']]
M={k:make_material(k,c,roughness=.88 if k!='eyes' else .65) for k,c in P['palette'].items()}
parts=[]
def write(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mesh(name,vs,fs,mat,anatomy):
    o=mesh_object(name,[(x*.001,y*.001,z*.001) for x,y,z in vs],fs,M[mat],C)
    o['anatomy']=anatomy;o['reconstruction']='original procedural interpretation';parts.append(o);return o

def interp(rows,y,col):
    if y<=rows[0][0]:return rows[0][col]
    for a,b in zip(rows,rows[1:]):
        if y<=b[0]:return a[col]+(b[col]-a[col])*(y-a[0])/(b[0]-a[0])
    return rows[-1][col]

def loft(name,rows,n,mat,anatomy):
    vs=[]
    for y,w,c,h in rows:
        for i in range(n):
            t=2*math.pi*i/n;vs.append((w*math.cos(t),y,c+h*math.sin(t)))
    fs=[]
    for k in range(len(rows)-1):
        for i in range(n):fs.append((k*n+i,k*n+(i+1)%n,(k+1)*n+(i+1)%n,(k+1)*n+i))
    fs += [tuple(reversed(range(n))),tuple((len(rows)-1)*n+i for i in range(n))]
    return mesh(name,vs,fs,mat,anatomy)

def tube(name,points,radii,mat,anatomy,sides=8):
    vs=[]
    for k,p in enumerate(points):
        tangent=(Vector(points[min(k+1,len(points)-1)])-Vector(points[max(k-1,0)])).normalized()
        guide=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0))
        a=tangent.cross(guide).normalized();b=tangent.cross(a).normalized()
        for i in range(sides):
            t=i*2*math.pi/sides;vs.append(tuple(Vector(p)+radii[k]*(math.cos(t)*a+math.sin(t)*b)))
    fs=[]
    for k in range(len(points)-1):
        for i in range(sides):fs.append((k*sides+i,k*sides+(i+1)%sides,(k+1)*sides+(i+1)%sides,(k+1)*sides+i))
    fs += [tuple(reversed(range(sides))),tuple((len(points)-1)*sides+i for i in range(sides))]
    return mesh(name,vs,fs,mat,anatomy)

def patch(name,y0,y1,u0,u1,surface,mat,anatomy,ny=3,nu=6,thickness=.012,ventral=False):
    vs=[]
    for layer in [0,1]:
        for j in range(ny+1):
            y=y0+(y1-y0)*j/ny
            for i in range(nu+1):
                u=u0+(u1-u0)*i/nu;x,yy,z=surface(y,u)
                vs.append((x,yy,z+layer*thickness*(1 if ventral else -1)))
    N=(ny+1)*(nu+1);fs=[]
    for j in range(ny):
        for i in range(nu):
            a=j*(nu+1)+i;fs += [(a,a+1,a+nu+2,a+nu+1),(a+N,a+nu+1+N,a+nu+2+N,a+1+N)]
    edge=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,ny+1)]+[ny*(nu+1)+i for i in reversed(range(nu))]+[j*(nu+1) for j in reversed(range(1,ny))]
    fs += [(a,b,b+N,a+N) for a,b in zip(edge,edge[1:]+edge[:1])]
    return mesh(name,vs,fs,mat,anatomy)

# Approximately 0.75 mm long and wide, rounded rather than pear-pointed.
abd=[(-.15,.290,.266,.111),(-.08,.335,.266,.128),(.02,.370,.267,.137),(.12,.375,.266,.139),(.23,.365,.262,.135),(.34,.337,.254,.125),(.44,.292,.244,.110),(.52,.235,.233,.091),(.575,.151,.219,.066),(.60,.070,.210,.047)]
loft('rounded_opisthosoma',abd,24,'ventral_cuticle','rounded plated abdomen, broad prosomal union, no pedicel or external tail')
def dorsal(y,u):
    return interp(abd,y,1)*u,y,interp(abd,y,2)+interp(abd,y,3)*math.sqrt(max(0,1-u*u))+.006
# T1 is mostly concealed. The source explicitly labels one combined anterior T2-3.
patch('tergite_01_concealed_ridge',-.17,-.145,-.93,.93,lambda y,u:(dorsal(y,u)[0],y,dorsal(y,u)[2]-.018),'lateral_cuticle','narrow anterior ridge overlapped by rear shield',ny=1,nu=12)
bands=[('02_03',-.144,-.040),('04',-.032,.063),('05',.071,.165),('06',.173,.266),('07',.274,.367),('08',.375,.470)]
for n,a,b in bands:
    patch('tergite_'+n+'_central',a,b,-.62,.62,dorsal,'dorsal_cuticle','one combined T2-3 plate' if n=='02_03' else 'transverse median tergite '+n,ny=3,nu=8)
    for side,u0,u1 in [('L',-.985,-.653),('R',.653,.985)]:
        patch('tergite_'+n+'_lateral_'+side,a,b,u0,u1,dorsal,'lateral_cuticle','lateral tergal subdivision '+n,ny=3,nu=3)
patch('tergite_09_undivided',.478,.600,-.985,.985,dorsal,'dorsal_cuticle','broad unpartitioned terminal dorsal plate 9',ny=4,nu=14)
# A compact, subtriangular shield with a small pointed front and broad posterior.
car=[(-.60,.015,.286,.047),(-.575,.044,.280,.065),(-.53,.090,.269,.096),(-.47,.143,.258,.124),(-.40,.196,.253,.141),(-.32,.243,.251,.146),(-.24,.279,.249,.143),(-.175,.300,.247,.135),(-.15,.296,.247,.128)]
loft('subtriangular_carapace',car,24,'carapace','subtriangular headshield with pointed anterior apex, broad rear and no exaggerated lobes')
def car_top(y,x):return interp(car,y,2)+interp(car,y,3)*math.sqrt(max(0,1-(x/interp(car,y,1))**2))
# Low, conservative median eye relief near the front: neither a spider eye array nor horns.
for s in [-1,1]:
    x=s*.023;y=-.508;z=car_top(y,x)
    loft('median_eye_'+('L' if s<0 else 'R'),[(y-.010,.006,z+.001,.004),(y,.011,z+.003,.006),(y+.010,.006,z+.001,.004)],8,'eyes','subtle interpretive median eye relief')
    o=parts[-1]
    for v in o.data.vertices:v.co.x+=x*.001

# Six tapered distal podomeres per leg beyond each broad coxa.
# Centerlines follow the published full-animal fan: I/II anterior, III/IV posterior.
leg_centerlines=[
[(.133,-.450,.258),(.210,-.548,.300),(.305,-.680,.348),(.490,-.890,.338),(.630,-1.055,.245),(.710,-1.165,.133),(.752,-1.224,.013)],
[(.218,-.333,.245),(.340,-.368,.295),(.505,-.425,.330),(.750,-.523,.302),(.950,-.616,.219),(1.095,-.690,.119),(1.165,-.728,.013)],
[(.275,-.236,.227),(.405,-.184,.268),(.552,-.091,.295),(.749,.064,.260),(.896,.223,.181),(.988,.374,.095),(1.038,.474,.013)],
[(.291,-.159,.213),(.352,-.032,.243),(.429,.153,.274),(.525,.414,.254),(.589,.658,.176),(.627,.863,.092),(.650,1.015,.013)]
]
legdata=[]
podomeres=['trochanter','femur','patella','tibia','metatarsus','tarsus']
for n,pts in enumerate(leg_centerlines,1):
    for s in [-1,1]:
        side='L' if s<0 else 'R';points=[(s*x,y,z) for x,y,z in pts]
        for j,(a,b) in enumerate(zip(points,points[1:])):
            a,b=Vector(a),Vector(b);d=b-a;r=[.032,.033,.030,.025,.019,.016][j]
            tube('walking_leg_%d_%s_%s'%(n,side,podomeres[j]),[tuple(a),tuple(a+d*.16),tuple(a+d*.76),tuple(b)],[r*.76,r,r*.84,r*(.32 if j==5 else .66)],'legs','walking pair %d %s'%(n,podomeres[j]))
        # Small convergent coxal volume joins directly to shield underside.
        x,y,z=points[0]
        tube('coxa_%d_%s'%(n,side),[(s*.065,y+.035,.157),(s*abs(x)*.65,y+.016,.200),(x,y,z)],[.032,.041,.034],'legs','walking leg coxa %d under prosoma'%n)
        legdata.append({'pair':n,'side':side,'centerlines_mm':points,'podomere_lengths_mm':[(Vector(b)-Vector(a)).length for a,b in zip(points,points[1:])]})
# Same-taxon drawing has long forward palps, distinct from the four walking pairs.
for s in [-1,1]:
    side='L' if s<0 else 'R';points=[(s*.052,-.523,.249),(s*.082,-.666,.274),(s*.113,-.839,.285),(s*.131,-1.016,.277),(s*.128,-1.176,.248),(s*.123,-1.295,.213)]
    for j,(a,b) in enumerate(zip(points,points[1:])):
        a,b=Vector(a),Vector(b);d=b-a;r=[.021,.022,.020,.017,.013][j]
        tube('pedipalp_'+side+'_'+str(j+1),[tuple(a),tuple(a+d*.24),tuple(b)],[r*.78,r,r*(.42 if j==4 else .70)],'legs','slender forward pedipalp, not walking leg or antenna')
    tube('chelicera_'+side,[(s*.024,-.567,.260),(s*.026,-.579,.223),(s*.018,-.581,.186)],[.014,.017,.007],'ventral_cuticle','conservative small paired downward mouthpart, no scorpion pincer')
# Restrained ventral reconstruction: broad transverse sternites and flush pygidium.
def ventral(y,u):return interp(abd,y,1)*u,y,interp(abd,y,2)-interp(abd,y,3)*math.sqrt(max(0,1-u*u))-.004
for n,(a,b) in enumerate([(-.134,-.032),(-.024,.077),(.085,.187),(.195,.297),(.305,.407),(.415,.505),(.513,.590)],2):
    patch('sternite_'+str(n),a,b,-.92,.92,ventral,'lateral_cuticle','ventral transverse plate, conservative interpretive continuation',ny=2,nu=10,thickness=.010,ventral=True)
loft('ventral_pygidium',[(.532,.018,.150,.006),(.548,.026,.151,.008),(.563,.015,.153,.005)],8,'ventral_cuticle','small flush ventral terminal feature, not an external tail')
# Smooth attached sternum, no floating underside plane.
loft('sternum', [(-.47,.016,.161,.008),(-.36,.043,.130,.012),(-.24,.037,.127,.012),(-.18,.015,.140,.008)],8,'ventral_cuticle','small conservative sternum joining convergent coxae')

# Floor at true walking-tarsus surfaces. Relative threshold is in square meters.
bpy.context.view_layer.update();lowest=min(v.co.z for o in parts for v in o.data.vertices)
for o in parts:
    for v in o.data.vertices:v.co.z-=lowest
bpy.context.view_layer.update()
epsilon=P['body_length_estimate']**2 * P['degenerate_area_relative_factor']
source=audit_source(C,max_triangles=40000,triangle_area_epsilon=epsilon)
source['triangle_area_epsilon_m2']=epsilon;source['area_threshold_formula']='body_length_estimate_m ** 2 * 1e-12'
write(E/'source-audit.json',source)
if source['errors']:raise RuntimeError(str(source['errors']))
# Geometry-derived checks, not merely repeated declarations.
def bounds(o):
    pts=[o.matrix_world@v.co for v in o.data.vertices]
    lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
    return {'min':lo,'max':hi,'size':[hi[i]-lo[i] for i in range(3)]}
cb=bounds(bpy.data.objects['subtriangular_carapace']);ab=bounds(bpy.data.objects['rounded_opisthosoma']);names=[o.name for o in parts]
measured={'body_length_m':ab['max'][1]-cb['min'][1],'carapace_length_m':cb['size'][1],'abdomen_length_m':ab['size'][1],'abdomen_width_m':ab['size'][0]}
checks={'body_length_matches_estimated_1_2mm':abs(measured['body_length_m']-.0012)<1e-9,'carapace_0_45mm':abs(measured['carapace_length_m']-.00045)<1e-9,'abdomen_0_75mm':abs(measured['abdomen_length_m']-.00075)<1e-9,'four_walking_pairs_six_distal_podomeres':sum(n.startswith('walking_leg_') for n in names)==48,'separate_forward_palps':sum(n.startswith('pedipalp_') for n in names)==10,'combined_tergite_2_3':all(n in names for n in ['tergite_02_03_central','tergite_02_03_lateral_L','tergite_02_03_lateral_R']),'no_separate_T2_T3':not any(n in names for n in ['tergite_02_central','tergite_03_central']),'undivided_broad_T9':'tergite_09_undivided' in names and not any(n.startswith('tergite_09_lateral') for n in names),'no_external_tail':max(v.co.y for o in parts if 'pygidium' in o.name for v in o.data.vertices)<ab['max'][1]}
assert all(checks.values())
write(E/'measured-anatomy.json',{'status':'PASS_SOURCE_GEOMETRY_CHECKS_ONLY','checks':checks,'dimensions_m':measured,'source_specimen':'Ulster Museum K25850','measurement_scope':'Estimated from 0.5 mm published scale bar, approximate 15 percent tolerance. Not a published caliper measurement.','restored_appendages':'Following same taxon reconstruction, JNCC Fig2.44b after Dunlop1996; not fully fossil-preserved.','source_python_version':sys.version,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json')})
# Save semantic, editable scene before export batching or preview additions.
bpy.context.scene['scientific_anchor']='Palaeotarbus jerami K25850; JNCC Fig2.44 and Biology2022 Fig1D'
bpy.context.scene['artist_inference']='Depth, symmetry, pose, eyes and color; restored appendages from same-taxon drawing'
bpy.context.scene.render.filepath='//';bpy.context.preferences.filepaths.save_version=0
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if hasattr(space,'params') and space.params and hasattr(space.params,'directory'):space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
# Batch by six palette materials, without destroying editable semantic source.
for name,mat in M.items():
    group=[o for o in C.all_objects if o.type=='MESH' and o.data.materials[0]==mat]
    if not group:continue
    bpy.ops.object.select_all(action='DESELECT')
    for o in group:o.select_set(True)
    bpy.context.view_layer.objects.active=group[0]
    if len(group)>1:bpy.ops.object.join()
    bpy.context.view_layer.objects.active.name='export_'+name
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Missing exporter properties: '+str(missing))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',40000,6,8,ground_tolerance=1e-8,triangle_area_epsilon=epsilon);glb['file']='model.glb';glb['triangle_area_epsilon_m2']=epsilon
write(E/'glb-audit.json',glb)
if glb['errors']:raise RuntimeError(str(glb['errors']))
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))
assert delta<1e-9 and source['triangles']==glb['scene_triangles'] and glb['bytes']<8388608
write(E/'anatomy-and-build.json',{'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'seed':P['seed'],'source_editable_objects':len(source['parts']),'body_dimensions_m':measured,'appendages':{'walking_pairs':4,'pedipalp_pairs':1,'chelicera_pairs':1},'tergites':'Combined T2-3, then T4-T8 with median/lateral subdivisions; broad undivided T9','leg_centerlines':legdata,'floor_shift_m':-lowest,'source_export_bounds_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'semantic_digest':glb['semantic_sha256'],'area_threshold_formula':'body_length_estimate_m ** 2 * 1e-12','area_threshold_m2':epsilon,'limitations':'Technical checks cannot establish independent visual/factual acceptance, GPU, museum scene, user acceptance or deployment.'})
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],glb['bytes'])
