# SPDX-License-Identifier: MIT
"""Deterministic original Teleoceras proterum living reconstruction.
Run with Blender 4.3.2, two render threads, and -- --output OUTPUT.
Only the adjacent parameters and declared relative dependencies are required.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector, Matrix
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, render_previews
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())

def write(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n')

def loft(name, rings, n, mat, axis='Y', group=None):
    # Ring data: center x,y,z and the two perpendicular radii.
    verts=[]; faces=[]
    for j,(x,y,z,a,b) in enumerate(rings):
        for k in range(n):
            t=2*math.pi*k/n
            if axis=='Y': v=(x+a*math.cos(t),y,z+b*math.sin(t))
            else: v=(x+a*math.cos(t),y+b*math.sin(t),z)
            verts.append(v)
    for j in range(len(rings)-1):
        for k in range(n):
            a=j*n+k; b=j*n+(k+1)%n; c=(j+1)*n+(k+1)%n; d=(j+1)*n+k
            faces.append((a,b,c,d))
    faces.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+k for k in range(n))])
    if group is not None:
        off=len(group[0]);group[0].extend(verts);group[1].extend(tuple(i+off for i in f) for f in faces);return
    return mesh_object(name,verts,faces,mat,C)

def ellipsoid(name,center,scale,mat,n=12,r=6,group=None):
    # Explicit latitude mesh with polar fans, never an untouched primitive.
    x,y,z=center; ax,ay,az=scale; verts=[(x,y,z-az)];faces=[]
    for j in range(1,r):
        a=-math.pi/2+math.pi*j/r
        for k in range(n):
            t=2*math.pi*k/n
            verts.append((x+ax*math.cos(a)*math.cos(t),y+ay*math.cos(a)*math.sin(t),z+az*math.sin(a)))
    verts.append((x,y,z+az)); top=len(verts)-1
    for k in range(n): faces.append((0,1+(k+1)%n,1+k))
    for j in range(r-2):
        for k in range(n):
            a=1+j*n+k;b=1+j*n+(k+1)%n; faces.append((a,b,b+n,a+n))
    for k in range(n): faces.append((top,1+(r-2)*n+k,1+(r-2)*n+(k+1)%n))
    if group is not None:
        off=len(group[0]);group[0].extend(verts);group[1].extend(tuple(i+off for i in f) for f in faces);return
    return mesh_object(name,verts,faces,mat,C)

def tube(name,points,radii,mat,n=8):
    verts=[];faces=[]
    for j,p in enumerate(points):
        p=Vector(p); tangent=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(0,j-1)])
        tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0))
        u=tangent.cross(ref).normalized();v=tangent.cross(u).normalized()
        for k in range(n):
            a=2*math.pi*k/n; verts.append(tuple(p+radii[j]*(u*math.cos(a)+v*math.sin(a))))
    for j in range(len(points)-1):
        for k in range(n): faces.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    faces+=[tuple(reversed(range(n))),tuple((len(points)-1)*n+k for k in range(n))]
    return mesh_object(name,verts,faces,mat,C)

def ear(side):
    # Folded, pointed rhino pinna with outer shell and inset inner plane.
    outline=[(.17,-.91,1.05),(.27,-.92,1.14),(.34,-.83,1.28),(.32,-.73,1.31),(.23,-.71,1.23),(.15,-.79,1.11)]
    verts=[(side*x,y,z) for x,y,z in outline]+[(side*(x+.012),y+.035,z-.015) for x,y,z in outline]
    verts += [(side*.245,-.805,1.18),(side*.255,-.775,1.17)]
    faces=[]
    for k in range(6):faces.append((12,k,(k+1)%6))
    for k in range(6):faces.append((13,6+(k+1)%6,6+k))
    for k in range(6):faces.append((k,6+k,6+(k+1)%6,(k+1)%6))
    ob=mesh_object(('left' if side<0 else 'right')+'-folded-ear',verts,faces,[skin,inner],C)
    for poly in ob.data.polygons:
        if poly.index<6:poly.material_index=1 if poly.index in (1,2,3,4) else 0
    return ob

argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);a.add_argument('--gray',action='store_true');args=a.parse_args(argv)
out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
C=setup_scene('teleoceras',P['seed'])
materials={k:make_material(k,v,roughness=.87) for k,v in P['palette'].items()}
skin=materials['warm-gray-hide']; belly=materials['ventral-hide']; dark=materials['crease']; horn=materials['horn-and-hooves']; eye=materials['eye'];inner=materials['ear-inner']
# The chest/abdomen is very broad and deep, with a high shoulder and tapering haunch.
body=loft('barrel-trunk',[(0,-.88,.88,.23,.24),(0,-.76,.91,.37,.37),(0,-.55,.91,.48,.44),(0,-.30,.88,.55,.47),(0,0,.86,.58,.48),(0,.28,.86,.57,.47),(0,.53,.86,.50,.44),(0,.74,.88,.39,.37),(0,.90,.87,.25,.26),(0,.97,.86,.09,.12)],24,[skin,belly])
for f in body.data.polygons:
    if f.center.z<.65:f.material_index=1
# Short lowered neck narrows intentionally from the shoulder into the low skull.
neck=loft('short-thick-neck',[(0,-.69,.91,.30,.32),(0,-.86,.93,.28,.28),(0,-1.01,.91,.235,.23),(0,-1.13,.88,.21,.19)],20,skin)
head_parts=[]
skull=loft('long-low-rhino-head',[(0,-1.70,.68,.14,.105),(0,-1.64,.70,.205,.145),(0,-1.49,.735,.22,.17),(0,-1.32,.79,.195,.195),(0,-1.16,.86,.23,.225),(0,-1.00,.90,.215,.20),(0,-.91,.92,.15,.145)],20,skin); head_parts.append(skull)
jaw=loft('heavy-lower-jaw',[(0,-1.66,.625,.14,.055),(0,-1.52,.61,.19,.075),(0,-1.33,.625,.18,.09),(0,-1.13,.69,.20,.11),(0,-1.03,.78,.15,.095)],16,belly);head_parts.append(jaw)
head_parts.append(loft('small-inferred-nasal-horn',[(0,-1.48,.88,.075,.073),(0,-1.49,.94,.060,.060),(0,-1.52,1.01,.040,.045),(0,-1.56,1.085,.018,.022),(0,-1.58,1.12,.004,.005)],12,horn,axis='Z'))
head_parts.extend([ear(-1),ear(1)])
# Sculpted, short upper limbs meet distinct wrists/hocks; not slender tubes.
for side in (-1,1):
    for front in (True,False):
        tag=('left' if side<0 else 'right')+('-fore' if front else '-hind')
        y=-.59 if front else .63; x=.37*side; dy=.035 if side<0 else -.035
        if front:
            rings=[(side*.34,y,.95,.19,.22),(side*.40,y+.02,.75,.16,.18),(side*.415,y+.04,.52,.12,.135),(side*.40,y+.015,.33,.095,.105),(side*.40,y-.015+dy,.16,.11,.12)]
        else:
            rings=[(side*.33,y,.96,.22,.23),(side*.41,y-.035,.75,.19,.20),(side*.43,y-.06,.56,.14,.16),(side*.43,y+.05,.36,.10,.115),(side*.40,y+.02+dy,.16,.105,.115)]
        loft(tag+'-limb',rings,14,skin,axis='Z')
        fy=y-.04+dy
        loft(tag+'-foot',[(x,fy,.035,.135,.16),(x,fy,.09,.15,.175),(x,fy+.02,.16,.12,.13),(x,fy+.025,.205,.10,.105)],14,skin,axis='Z')
# Every foot has three separate blunt digits and pale keratin nail plates.
toes=([],[]);nails=([],[])
for side in (-1,1):
    for front in (True,False):
        y=-.59 if front else .63;dy=.035 if side<0 else -.035; x=.40*side; fy=y-.04+dy
        for k in (-1,0,1):
            xx=x+k*.089; yy=fy-.11-(.025 if k==0 else 0)
            loft('digit',[(xx,yy,.0,.042,.066),(xx,yy-.009,.035,.048,.073),(xx,yy,.08,.046,.065),(xx,yy+.035,.12,.034,.04)],10,skin,axis='Z',group=toes)
            ellipsoid('nail',(xx,yy-.058,.045),(.038,.027,.034),horn,n=10,r=4,group=nails)
mesh_object('twelve-blunt-toes',*toes,skin,C);mesh_object('twelve-nail-plates',*nails,horn,C)
# Small lateral eyes, skin brow, recessed nostrils, and a restrained closed lip seam.
eyes=([],[]);brows=([],[]);nostrils=([],[])
for side in (-1,1):
    ellipsoid('eye',(side*.221,-1.16,.927),(.020,.034,.023),eye,n=12,r=6,group=eyes)
    ellipsoid('brow',(side*.214,-1.155,.956),(.027,.055,.022),skin,n=12,r=4,group=brows)
    ellipsoid('nostril',(side*.196,-1.573,.754),(.017,.038,.021),dark,n=12,r=6,group=nostrils)
head_parts+=[mesh_object('small-dark-eyes',*eyes,eye,C),mesh_object('brow-ridges',*brows,skin,C),mesh_object('paired-nostrils',*nostrils,dark,C)]
head_parts.append(tube('closed-mouth-line',[(-.177,-1.47,.638),(-.19,-1.59,.632),(-.13,-1.699,.637),(0,-1.71,.637),(.13,-1.699,.637),(.19,-1.59,.632),(.177,-1.47,.638)],[.0055]*7,dark,8))
# Small head turn is an artistic pose only, not a claimed anatomical measurement.
turn=Matrix.Rotation(math.radians(P['head_turn_deg']),4,'Z');pivot=Vector((0,-.94,.9))
for ob in head_parts:
    for v in ob.data.vertices:v.co=pivot+turn.to_3x3()@(v.co-pivot)
# The narrow downward-curved tail contrasts with the barrel and broad haunch.
tube('tapered-tail',[(0,.86,1.02),(0,1.0,.96),(.01,1.10,.82),(.02,1.14,.63),(.025,1.14,.46)],[.055,.048,.035,.025,.016],skin,10)
ellipsoid('tail-brush',(.025,1.14,.43),(.03,.035,.065),dark,n=10,r=5)
bpy.context.view_layer.update()
source=audit_source(C,P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
# The editable source has no camera, light or floor.
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//renders/'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params is not None:
                space.params.directory=b'//'
bpy.context.scene['scientific_limits']='Color, skin, keratin horn, soft tissue and exact dimensions are artistic estimates.'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in C.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Required exporter flags unavailable')
bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
glb=audit_glb(out/'model.glb',**{k:P['budgets'][k] for k in ('max_triangles','max_materials','max_primitives')});glb['file']='model.glb'
if glb['errors']:raise RuntimeError(glb['errors'])
lo=source['bounds_blender_m']['min'];hi=source['bounds_blender_m']['max'];exp={'min':[lo[0],lo[2],-hi[1]],'max':[hi[0],hi[2],-lo[1]]}
delta=max(abs(glb['bounds_m'][k][i]-exp[k][i]) for k in ('min','max') for i in range(3))
assert delta<1e-4 and glb['scene_triangles']==source['triangles'] and glb['bytes']<=P['budgets']['max_glb_bytes']
write(out/'build-report.json',{'asset':'teleoceras','revision':'r001','source':source,'glb':glb,'source_export_bounds_max_error_m':delta,'source_export_triangle_match':True,'export_options':options,'runtime':{'blender':bpy.app.version_string,'python':sys.version.split()[0]},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'scope':'Source and static export technical checks only; no visual, GPU, scene, user or publication approval.'})
if args.gray:
    gray=make_material('gray-check','#929292');bpy.context.view_layer.material_override=gray
    render_previews(C,out/'gray',views=('front','side','hero'),resolution=384,samples=8)
print('TELEOCERAS_BUILD_OK',glb['sha256'],glb['scene_triangles'])
