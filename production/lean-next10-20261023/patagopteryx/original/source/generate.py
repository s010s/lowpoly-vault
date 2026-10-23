# SPDX-License-Identifier: MIT
"""Deterministic Patagopteryx whole-organism reconstruction, metres, -Y forward.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out /path/to/build
The only non-standard runtime is Blender. All project imports are vendored.
"""
import sys, json, math, hashlib, argparse
from pathlib import Path
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

P=json.loads((SOURCE/'params.json').read_text())
A=argparse.ArgumentParser(); A.add_argument('--out',required=True,type=Path); A.add_argument('--gray',action='store_true')
args=A.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.out.resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('patagopteryx',P['seed'])
SC=bpy.context.scene; SC.render.threads_mode='FIXED'; SC.render.threads=2
M={k:make_material('Patagopteryx_'+k,'#929292' if args.gray else v,roughness=.87) for k,v in P['palette_srgb'].items()}

def sh(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value): (OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def loft(name,rings,n,materials,assign=None,phase=0):
    # Each ring: centre x/y/z and lateral/vertical radius, cross-sections normal to Y.
    v=[]
    for ri,(x,y,z,rx,rz) in enumerate(rings):
        for j in range(n):
            a=2*math.pi*j/n+phase
            v.append((x+rx*math.cos(a),y,z+rz*math.sin(a)))
    f=[tuple(reversed(range(n)))]
    for i in range(len(rings)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;c=(i+1)*n+(j+1)%n;d=(i+1)*n+j
            # Alternating diagonals give intentional large low-poly facets.
            if (i+j)%2: f.extend([(a,b,d),(b,c,d)])
            else: f.extend([(a,b,c),(a,c,d)])
    f.append(tuple((len(rings)-1)*n+j for j in range(n)))
    o=mesh_object(name,v,f,materials,C)
    if assign:
        for p in o.data.polygons: p.material_index=assign(p.center)
    return o

def tube_geometry(points,radii,n=10):
    pts=list(map(Vector,points)); verts=[]
    for i,c in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        ref=Vector((1,0,0)) if abs(tangent.x)<.9 else Vector((0,1,0))
        u=(ref-tangent*tangent.dot(ref)).normalized(); w=tangent.cross(u).normalized()
        rr=radii[i]; rx,ry=(rr,rr) if isinstance(rr,(float,int)) else rr
        for j in range(n):
            a=2*math.pi*j/n; verts.append(tuple(c+u*(rx*math.cos(a))+w*(ry*math.sin(a))))
    faces=[tuple(reversed(range(n)))]
    for i in range(len(pts)-1):
        for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.append(tuple((len(pts)-1)*n+j for j in range(n)))
    return verts,faces

def tube(name,points,radii,mat,n=10):
    v,f=tube_geometry(points,radii,n); return mesh_object(name,v,f,mat,C)

def merge_geometries(name,parts,mat):
    v=[];f=[]
    for vv,ff in parts:
        offset=len(v);v.extend(vv);f.extend(tuple(k+offset for k in face) for face in ff)
    return mesh_object(name,v,f,mat,C)

# A single designed oval trunk, not a stack of spheres.
body_rings=[(0,-.124,.254,.007,.012),(0,-.111,.254,.039,.045),(0,-.085,.251,.068,.074),
 (0,-.047,.248,.087,.088),(0,.002,.248,.095,.088),(0,.047,.251,.091,.081),
 (0,.088,.257,.073,.065),(0,.119,.266,.045,.040),(0,.139,.273,.011,.013)]
body=loft('feathered_oval_trunk',body_rings,20,[M['body'],M['under'],M['wing']],
 lambda c: 1 if c.z<.218 else 2 if c.z>.324 and c.y>.0 else 0)
body['anatomy']='Soft trunk volume inferred; compact flightless reconstruction.'
# Short rising S-neck. Feathered collar overlaps inside chest, no cut line.
neck=tube('short_curved_feathered_neck',[(0,-.088,.259),(0,-.108,.287),(0,-.130,.318),(0,-.136,.345),(0,-.139,.367)],
 [(.036,.040),(.033,.036),(.026,.029),(.021,.023),(.020,.021)],M['body'],16)
# Compact rounded skull posterior, shorter conservative face.
head=loft('small_rounded_head',[(0,-.113,.371,.006,.011),(0,-.120,.374,.023,.022),(0,-.136,.376,.029,.024),
 (0,-.155,.373,.027,.022),(0,-.170,.368,.020,.017),(0,-.177,.365,.012,.010)],16,[M['body'],M['under']],lambda c: 1 if c.z<.361 else 0)
head['uncertainty']='Anterior fossil skull missing. Soft head/bill outline conservative reconstruction, not measured intact skull.'
# Closed, subtly decurved beak; no claim of preserved dentition.
bill=loft('conservative_short_closed_bill',[(0,-.168,.365,.013,.010),(0,-.180,.363,.012,.009),(0,-.194,.359,.0075,.006),(0,-.204,.355,.0015,.0018)],12,M['bill'])
# Restrained short tail blended into rear trunk, no bony elongate tail.
loft('short_restrained_tail',[(0,.102,.271,.031,.023),(0,.132,.279,.034,.021),(0,.160,.282,.027,.013),(0,.177,.281,.010,.006)],14,M['wing'])

joints={};toe_targets={}; wing_guides={}
for side,s in [('left',-1),('right',1)]:
    # Small folded wings hug the body. Feather tips remain well short of rump.
    wing=loft(side+'_reduced_folded_wing',[(s*.076,-.055,.283,.007,.009),(s*.088,-.037,.278,.011,.023),
       (s*.094,-.006,.268,.012,.029),(s*.093,.025,.258,.011,.024),(s*.082,.054,.251,.009,.014),(s*.071,.072,.248,.003,.003)],12,M['wing'])
    wing['anatomy']='Reduced folded forelimb, humerus 59.8 mm measured; feather shape/extent inferred.'
    # Clean closed folded-wing mesh; no intersecting raised vane overlays.
    shoulder=Vector((s*.071,-.034,.283)); dv=Vector((s*.019,.052,-.020)).normalized()*.0598
    wing_guides[side]={'shoulder':list(shoulder),'elbow':list(shoulder+dv),'humerus_m':dv.length}
    # Internal skeletal centreline uses 101 / 138 / 50.8 mm, not false exact fossil lengths.
    hip=Vector((s*.046,.027,.232))
    femdir=Vector((s*.007,-.079,-.062)).normalized()
    knee=hip+femdir*P['femur_model_m']
    tibdir=Vector((s*-.001,.078,-.113)).normalized()
    hock=knee+tibdir*P['tibiotarsus_model_m']
    # ankle height fixed at 0.008 m with exact selected tarsal length
    dz=hock.z-.008; dy=-math.sqrt(P['tarsometatarsus_m']**2-dz**2)
    ankle=hock+Vector((0,dy,-dz))
    joints[side]={k:list(v) for k,v in [('hip',hip),('knee',knee),('hock',hock),('ankle',ankle)]}
    tube(side+'_robust_feathered_thigh',[hip+Vector((0,0,.018)),hip.lerp(knee,.45),knee,knee.lerp(hock,.24)],[(.032,.039),(.033,.037),(.024,.026),(.015,.017)],M['body'],14)
    tube(side+'_tibiotarsal_shank',[knee.lerp(hock,.12),knee.lerp(hock,.50),hock],[(.014,.015),(.010,.012),(.009,.010)],M['foot'],10)
    tube(side+'_short_tarsometatarsus',[hock, hock.lerp(ankle,.45),ankle],[(.009,.010),(.007,.007),(.008,.008)],M['foot'],10)
    # Four splayed forward-directed digits, medial I is short; NONE points back.
    # Coordinates are pose choices. I/II/III/IV = .5/.7/1/.65 relative forward extent.
    specs=[('I',-s*.022,.025),('II',-s*.016,.039),('III',s*.002,.055),('IV',s*.027,.036)]
    toes=[];claws=[];toe_targets[side]={}
    for digit,dx,forward in specs:
        start=Vector((ankle.x+(dx*.13),ankle.y, .007))
        end=Vector((ankle.x+dx,ankle.y-forward,.0042))
        middle=start.lerp(end,.55)+Vector((0,0,.001))
        r=.0032 if digit=='I' else .0042
        toes.append(tube_geometry([start,middle,end],[(r,r*.85),(r*.88,r*.66),(r*.61,r*.48)],8))
        direction=(end-start).normalized(); tip=end+direction*(.006 if digit=='I' else .009);tip.z=.0012
        claws.append(tube_geometry([end-direction*.001,end+direction*.003,tip],[(r*.62,r*.52),(r*.48,r*.40),(.0005,.00055)],8))
        toe_targets[side][digit]={'root':list(start),'tip':list(tip),'forward_minus_y':tip.y<start.y,'webbing':False}
    merge_geometries(side+'_four_forward_toes',toes,M['foot'])
    merge_geometries(side+'_four_terminal_claws',claws,M['bill'])
    # Small black eyes placed on lateral skull surfaces; no cartoon-sized or feather brow.
    eye=loft(side+'_eye',[(s*.027,-.142,.379,.0010,.0014),(s*.0295,-.147,.379,.0022,.0034),
       (s*.0290,-.151,.379,.0019,.0032),(s*.027,-.154,.379,.0008,.0013)],10,M['eye'])

# Foot pads are minimum-ground features. Preserve all metric bone dimensions by only translating.
from asset_common import ground_asset
shift=ground_asset(C,False)
# Root is the centre of the projected two-foot footprint, not the body bbox.
footpoints=[o.matrix_world@v.co for o in C.all_objects if o.type=='MESH' and ('four_forward_toes' in o.name or 'four_terminal_claws' in o.name) for v in o.data.vertices]
shift[1]=-(min(p.y for p in footpoints)+max(p.y for p in footpoints))/2
for obj in C.all_objects:
    if obj.type=='MESH':obj.location.y+=shift[1]
bpy.context.view_layer.update()
for group in (joints,):
    for side,vals in group.items():
        for key,vec in vals.items(): vals[key]=[vec[i]+shift[i] for i in range(3)]
for side,digits in toe_targets.items():
    for d,vals in digits.items():
        for k in ['root','tip']: vals[k]=[vals[k][i]+shift[i] for i in range(3)]

SC['reconstruction_scope']='Original whole-body Patagopteryx deferrariisi. Fossil proportions plus explicitly inferred feathers, skin, colours, anterior bill.'
SC['seed']=P['seed'];SC['soft_tissue_and_bill_are_inferred']=True
SC['measurement_note']='Femur >99.1 mm; tibiotarsus >136.2 mm, missing <3 mm. Selected 101 and 138 mm are reconstructed complete lengths.'
SC['source_generator_sha256']=sh(Path(__file__))
qa=audit_source(C,P['budgets']['max_triangles'])
if qa['errors']: raise RuntimeError(qa['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
 export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
 export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Missing required exporter options: '+str(set(options)-available))
bpy.ops.export_scene.gltf(**options)
audit=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if audit['errors']:raise RuntimeError(audit['errors'])
if audit['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
b=qa['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(audit['bounds_m'][which][i]-expected[which][i]) for which in ['min','max'] for i in range(3))
assert delta<1e-6 and qa['triangles']==audit['scene_triangles']
write('source-audit.json',qa);write('glb-audit.json',audit)
write('build.json',{'asset_id':'patagopteryx','revision':'r001','gray':args.gray,'seed':P['seed'],'blender':bpy.app.version_string,
 'python':sys.version,'generator_sha256':sh(Path(__file__)),'params_sha256':sh(SOURCE/'params.json'),
 'export_options':{k:v for k,v in options.items() if k!='filepath'},'bounds_delta_m':delta,'glb_sha256':sh(OUT/'model.glb'),
 'blend_sha256':sh(OUT/'model.blend'),'semantic_sha256':audit['semantic_sha256'],'joints_blender_m':joints,
 'wing_humerus_guides':wing_guides,'toe_targets_blender_m':toe_targets,'ground_shift_m':shift,
 'root_origin':'Identity root at projected two-foot footprint bounding-box centre; lowest intended contact is Z=0.',
 'anatomical_intersections':'Closed independently editable trunk/neck/head/limbs/wings join by intentional hidden overlap. No boolean union/printability claim.',
 'notes':'Compact whole organism. Four forward toes per foot. Palette-only inferred plumage. No animation, texture or external asset dependency.'})
print('BUILD_COMPLETE',json.dumps({'out':str(OUT),'glb':sh(OUT/'model.glb'),'triangles':audit['scene_triangles']}))
