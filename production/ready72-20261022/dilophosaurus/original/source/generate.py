# SPDX-License-Identifier: MIT
"""Original Dilophosaurus reconstruction. Blender 4.3.2, deterministic, metres.
Usage: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out DIR
Only source/params.json and the declared source/deps helpers are runtime inputs.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,audit_source,render_previews,link_object
from qa_glb import audit_glb

S=Path(__file__).resolve().parent
P=json.loads((S/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,default=S.parent); p.add_argument('--gray',action='store_true'); p.add_argument('--render',action='store_true')
a=p.parse_args(argv); O=a.out.resolve(); O.mkdir(parents=True,exist_ok=True); (O/'qa/evidence').mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,d): (O/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
C=setup_scene('dilophosaurus',seed=P['seed'])
M=[make_material(k,v,roughness=.84) for k,v in P['palette_hex'].items()]
parts=[]

def loft(name,stations,n=12,palette=True,material=0):
    """Closed articulated ring loft with tangent-aligned transverse planes.
    Station is x,y,z, lateral radius, dorsoventral radius. No default primitives.
    """
    vs=[]; fs=[]; ids=[]
    for i,s in enumerate(stations):
        c=Vector(s[:3]); d=Vector(stations[min(i+1,len(stations)-1)][:3])-Vector(stations[max(0,i-1)][:3])
        d.normalize(); u=Vector((1,0,0))
        if abs(d.dot(u))>.92: u=Vector((0,1,0))
        u=(u-d*u.dot(d)).normalized(); v=u.cross(d).normalized()
        for k in range(n):
            t=2*math.pi*k/n; q=c+u*(s[3]*math.cos(t))+v*(s[4]*math.sin(t)); vs.append(tuple(q))
    fs.append(tuple(reversed(range(n)))); ids.append(material)
    for i in range(len(stations)-1):
        for k in range(n):
            j=(k+1)%n; face=(i*n+k,i*n+j,(i+1)*n+j,(i+1)*n+k)
            theta=2*math.pi*(k+.5)/n
            mi=(2 if math.sin(theta)<-.6 else 1 if math.sin(theta)>.60 else 0) if palette else material
            # Chosen diagonals make larger silhouette areas read as intentional facets.
            if (i+k)%2: fs.extend([(face[0],face[1],face[3]),(face[1],face[2],face[3])])
            else: fs.extend([(face[0],face[1],face[2]),(face[0],face[2],face[3])])
            ids.extend([mi,mi])
    fs.append(tuple((len(stations)-1)*n+k for k in range(n))); ids.append(material)
    ob=mesh_object(name,vs,fs,M,C)
    for f,mi in zip(ob.data.polygons,ids): f.material_index=mi
    ob['anatomical_part']=name; parts.append(ob); return ob

def tube(name,points,radii,n=8,mat=0,palette=False):
    return loft(name,[(*p,r,r) for p,r in zip(points,radii)],n,palette,mat)

# One continuous original ring loft from nape through S-neck, trunk and balancing tail.
body=[(0,-1.63,2.51,.135,.16),(0,-1.50,2.38,.14,.19),(0,-1.39,2.20,.15,.21),
(0,-1.30,2.01,.17,.23),(0,-1.12,1.84,.22,.28),(0,-.87,1.72,.29,.36),
(0,-.58,1.67,.37,.44),(0,-.25,1.68,.40,.47),(0,.09,1.72,.38,.44),
(0,.40,1.74,.34,.36),(0,.68,1.75,.28,.29),(0,.97,1.74,.21,.23),
(.02,1.28,1.73,.17,.19),(.045,1.59,1.71,.135,.15),(.06,1.91,1.68,.11,.12),
(.07,2.22,1.66,.085,.095),(.07,2.51,1.64,.065,.075),(.055,2.79,1.62,.046,.054),
(.025,3.03,1.61,.03,.037),(0,3.27,1.61,.017,.022),(-.02,3.50,1.63,.003,.004)]
loft('01_Continuous_Neck_Trunk_Tail',body,14)
# Strong narrow upper skull, gentle premaxillary tip and conservative subnarial dip.
head=[(0,-2.50,2.48,.055,.055),(0,-2.43,2.51,.094,.095),(0,-2.30,2.52,.105,.100),
(0,-2.17,2.51,.107,.095),(0,-2.02,2.55,.130,.145),(0,-1.84,2.59,.163,.190),
(0,-1.67,2.58,.151,.185),(0,-1.55,2.53,.105,.145)]
loft('02_Upper_Skull',head,12)
jaw=[(0,-2.47,2.407,.056,.022),(0,-2.36,2.394,.087,.039),(0,-2.15,2.381,.099,.047),
(0,-1.94,2.376,.116,.054),(0,-1.75,2.400,.141,.080),(0,-1.61,2.452,.118,.074)]
loft('03_Lower_Jaw',jaw,10,False,0)
# Narrow dark lip line sits flush along the shut jaw rather than a gaping movie mouth.
for sign,label in ((1,'R'),(-1,'L')):
    tube('04_Lip_'+label,[(sign*.057,-2.46,2.433),(sign*.094,-2.34,2.430),(sign*.110,-2.14,2.420),(sign*.139,-1.91,2.426),(sign*.148,-1.76,2.463)],[.006,.007,.008,.008,.005],6,4)

# Paired low thin longitudinal crests. Soft tissue outer edge is artistic inference.
crest_profile=[(-2.31,2.595),(-2.23,2.70),(-2.10,2.835),(-1.94,2.98),(-1.79,3.025),(-1.64,2.97),(-1.57,2.83),(-1.64,2.745),(-1.83,2.735),(-2.03,2.675),(-2.22,2.61)]
for sign,label in ((1,'R'),(-1,'L')):
    verts=[]
    for side in (-1,1):
        for y,z in crest_profile:
            # 0.17 m central gap; plates lean very slightly outward at high points.
            x=sign*(.100+max(0,z-2.70)*.035)+side*.015
            verts.append((x,y,z))
    n=len(crest_profile); faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]
    faces.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
    ob=mesh_object('05_Separate_Nasolacrimal_Crest_'+label,verts,faces,M,C)
    for f in ob.data.polygons: f.material_index=3
    parts.append(ob)

# Ellipsoidal low-ring eye shells are authored as short transverse lofts, not spheres.
for sign,label in ((1,'R'),(-1,'L')):
    x=sign*.151
    # explicit lateral bulge at orbital region
    eye=loft('06_Orbit_'+label,[(x,-1.865,2.66,.024,.045),(x+sign*.015,-1.835,2.663,.025,.049),(x,-1.805,2.66,.017,.034)],8,False,4)
    # iris and pupil shells face laterally; hand-authored octagonal discs with volume
    for name,rx,ry,rz,mat,cx in [('Iris',.009,.027,.028,5,sign*.177),('Pupil',.005,.012,.019,4,sign*.185)]:
        vs=[(cx-sign*rx,-1.835,2.666),(cx+sign*rx,-1.835,2.666)]
        for k in range(8):
            t=k*math.pi/4; vs.append((cx,-1.835+ry*math.cos(t),2.666+rz*math.sin(t)))
        fs=[]
        for k in range(8): fs.extend([(0,2+k,2+(k+1)%8),(1,2+(k+1)%8,2+k)])
        ob=mesh_object('07_'+name+'_'+label,vs,fs,M,C)
        for f in ob.data.polygons: f.material_index=mat
        parts.append(ob)
    tube('08_Nostril_'+label,[(sign*.096,-2.39,2.535),(sign*.101,-2.36,2.539)],[.014,.011],6,4)

# Hindlimbs: full muscular thigh, angled shank, high ankle and long metatarsus.
for sign,label in ((1,'R'),(-1,'L')):
    shift=-.075 if sign==1 else .075
    leg=[(sign*.25,.20,1.69,.22,.25),(sign*.33,.14,1.48,.235,.26),
    (sign*.40,-.05+shift,1.23,.21,.23),(sign*.43,-.26+shift,1.04,.145,.15),
    (sign*.43,-.20+shift,.88,.10,.12),(sign*.43,-.01+shift,.66,.079,.091),
    (sign*.43,.14+shift,.46,.066,.075),(sign*.43,.13+shift,.34,.060,.064),
    (sign*.43,.025+shift,.16,.060,.060),(sign*.43,-.03+shift,.10,.080,.059)]
    loft('09_Hind_Limb_'+label,leg,12)
    for digit,(dx,length) in enumerate([(-.102,.40),(0,.49),(.105,.38)],1):
        xb=sign*.43; yb=-.035+shift
        pts=[(xb+dx*.35,yb,.105),(xb+dx*.78,yb-length*.40,.067),(xb+dx,yb-length*.82,.049)]
        tube('10_Pes_'+label+'_Digit_'+str(digit),pts,[.044,.037,.024],8,0)
        tube('11_Pes_'+label+'_Claw_'+str(digit),[pts[-1],(xb+dx*1.07,yb-length,.038),(xb+dx*1.10,yb-length-.044,.022)],[.026,.018,.0025],7,4)
    # Small raised hallux, not a fourth main forward toe.
    tube('12_Hallux_'+label,[(sign*.38,.07+shift,.25),(sign*.34,.16+shift,.19),(sign*.33,.21+shift,.17)],[.028,.017,.004],7,4)
    # Arms are held with palms facing medially, not pronated down.
    arm=[(sign*.285,-.75,1.75,.105,.12),(sign*.35,-.77,1.57,.094,.10),
    (sign*.405,-.89,1.35,.070,.08),(sign*.43,-1.01,1.29,.054,.063),
    (sign*.425,-1.17,1.37,.049,.060),(sign*.420,-1.26,1.37,.043,.063)]
    loft('13_Forelimb_'+label,arm,10)
    for digit,(yz,leng) in enumerate([(.036,.18),(0,.25),(-.045,.21)],1):
        y=-1.26; z=1.37+yz; x=sign*(.418+(digit-2)*.023)
        pts=[(x,y,z),(x-sign*.016,y-leng*.55,z-.035),(x-sign*.037,y-leng,z-.09)]
        tube('14_Manus_'+label+'_Major_Digit_'+str(digit),pts,[.025,.021,.014],7,0)
        tube('15_Manus_'+label+'_Claw_'+str(digit),[pts[-1],(pts[-1][0]-sign*.014,pts[-1][1]-.035,pts[-1][2]-.035),(pts[-1][0]-sign*.018,pts[-1][1]-.022,pts[-1][2]-.064)],[.016,.012,.0018],7,4)
    tube('16_Manus_'+label+'_Reduced_Digit_IV_Nub',[(sign*.471,-1.235,1.339),(sign*.477,-1.27,1.312),(sign*.469,-1.291,1.302)],[.023,.017,.008],7,0)

# Exact artistic adult total length and ground-centered bilateral footprint.
yvals=[v.co.y for ob in parts for v in ob.data.vertices]
scale_factor=P['length_target']/(max(yvals)-min(yvals))
for ob in parts:
    for v in ob.data.vertices: v.co*=scale_factor
low=min(v.co.z for ob in parts for v in ob.data.vertices)
foot_y=[v.co.y for ob in parts if ob.name.startswith(('10_','11_')) for v in ob.data.vertices]
foot_center_y=(min(foot_y)+max(foot_y))/2
for ob in parts:
    for v in ob.data.vertices: v.co.z-=low; v.co.y-=foot_center_y
source=audit_source(C,P['budgets']['max_triangles'])
if source['errors']: raise RuntimeError(source['errors'])
# Save semantic editable parts before export batching; they are independently selectable.
bpy.context.scene['reconstruction_notes']='Composite living reconstruction; approximate 6 m adult artistic scale. Crest soft tissue contour, colours and pose inferred. No frill or venom. Three main manual digits and reduced IV.'
bpy.context.scene['asset_author']='Leon Made This / s010s'; bpy.context.scene['asset_license']='CC-BY-4.0'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(O/'model.blend'))
# Batch only the temporary export representation. Semantic source stays untouched on disk.
bpy.ops.object.select_all(action='DESELECT')
for ob in parts: ob.select_set(True)
bpy.context.view_layer.objects.active=parts[0]; bpy.ops.object.join()
joined=bpy.context.view_layer.objects.active; joined.name='Dilophosaurus_Export_SixPaletteGroups'
options=dict(filepath=str(O/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
root=bpy.data.objects[C['asset_root']]; root.select_set(True)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
missing=set(options)-available
if missing: raise RuntimeError('Exporter unsupported flags '+repr(missing))
bpy.ops.export_scene.gltf(**options)
g=audit_glb(O/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
g['file']='model.glb'
if g['errors']: raise RuntimeError(g['errors'])
if g['bytes']>P['budgets']['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(g['bounds_m'][s][i]-expected[s][i]) for s in ('min','max') for i in range(3))
if delta>1e-4 or source['triangles']!=g['scene_triangles']: raise RuntimeError('Roundtrip metrics mismatch')
save('qa/evidence/source-geometry.json',source)
save('qa/evidence/glb-audit.json',g)
save('qa/evidence/build.json',{'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(S/'params.json'),'glb_sha256':sha(O/'model.glb'),'blend_sha256':sha(O/'model.blend'),'seed':P['seed'],'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_to_export_bound_max_error_m':delta,'source_semantic_parts':len(source['parts']),'export_primitives':g.get('scene_primitives_estimated_base_draw_calls'),'three_version_target':'0.180.0','anatomy':{'manual_main_digits_each_side':3,'manual_reduced_digit_IV_each_side':1,'major_forward_toes_each_side':3,'paired_crests':2,'crest_plate_thickness_m':.03*scale_factor,'crest_min_center_gap_m':.17*scale_factor,'ground_adjustment_m':-low,'uniform_scale_factor':scale_factor,'footprint_center_y_adjustment_m':-foot_center_y,'tail_minimum_surface_height_m':min(v.co.z for v in joined.data.vertices if v.co.y>.75)},'limits':'Bounds, original source topology and selected anatomy parameters only; no claim of union watertightness or independent anatomical acceptance.'})
if a.gray or a.render:
    # Clean import proves final previews depict exported geometry, not hidden source data.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(O/'model.glb'))
    c=bpy.data.collections.new('EXACT_GLB'); bpy.context.scene.collection.children.link(c)
    for ob in list(bpy.context.scene.objects):
        for old in list(ob.users_collection): old.objects.unlink(ob)
        c.objects.link(ob)
    if a.gray:
        clay=make_material('_Gray_Shape_Check','#929292',roughness=.9)
        bpy.context.view_layer.material_override=clay
        path=O/'private/gray'; path.mkdir(parents=True,exist_ok=True)
        rendered=render_previews(c,path,('front','side','top','hero'),resolution=480,samples=8)
        save('private/gray/evidence.json',{'status':'RENDERED_PENDING_MAKER_INSPECTION','glb_sha256':sha(O/'model.glb'),'views':{Path(x).name:sha(x) for x in rendered},'engine':'Cycles CPU','samples':8,'resolution':480,'threads':2})
    if a.render:
        path=O/'private/final-render'; path.mkdir(parents=True,exist_ok=True)
        rendered=render_previews(c,path,('front','side','top','hero'),resolution=1024,samples=80)
        (O/'views').mkdir(exist_ok=True)
        import shutil
        dest={v:('preview.png' if v=='hero' else 'views/'+v+'.png') for v in ('front','side','top','hero')}
        for v,rel in dest.items(): shutil.copyfile(path/f'preview-{v}.png',O/rel)
        shutil.copyfile(O/'preview.png',O/'views/perspective.png')
        save('qa/evidence/exact-glb-views.json',{'status':'RENDERED_PENDING_MAKER_INSPECTION','glb_sha256':sha(O/'model.glb'),'source_unchanged':True,'frames':{rel:sha(O/rel) for rel in list(dest.values())+['views/perspective.png']},'engine':'Cycles CPU','resolution':1024,'samples':80,'threads':2,'view_transform':'Standard','look':'None','camera_directions':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'camera_note':'Orthographic diagnostic views and oblique front-right hero; perspective name is standard layout role, not perspective projection. Hero reused byte-identically.'})
print(json.dumps({'status':'MADE_NOT_INDEPENDENTLY_ACCEPTED','output':str(O),'triangles':g['scene_triangles'],'glb_sha256':sha(O/'model.glb')}))
