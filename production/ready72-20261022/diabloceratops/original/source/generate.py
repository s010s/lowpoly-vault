#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Diabloceratops eatoni living reconstruction, r001.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output /path/out
All source dependencies vendored beside this file. Photos never loaded.
The whole body is a ceratopsid reconstruction, not a measured skeleton.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('diabloceratops',P['seed']);ROOT=bpy.data.objects[COL['asset_root']]
M={name:make_material(name,color,roughness=.91 if name!='dark' else .6) for name,color in P['palette'].items()}
MATS=list(M.values());MI={name:i for i,name in enumerate(M)}

def mesh(name,verts,faces,mat='skin',select=None):
    ob=mesh_object(name,verts,faces,MATS,COL)
    for p in ob.data.polygons:p.material_index=MI[select(p,verts) if select else mat]
    ob['anatomical_part']=name
    return ob

def tube(name,points,radii,mat='skin',n=10,select=None,lateral=None):
    """Closed tapered profile sweep; ends have actual nonzero cap rings."""
    pts=list(map(Vector,points));verts=[]
    for j,p in enumerate(pts):
        direction=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized()
        x=Vector(lateral or (1,0,0));x=(x-direction*x.dot(direction)).normalized()
        if x.length<.1:x=direction.cross(Vector((0,0,1))).normalized()
        z=direction.cross(x).normalized();radius=radii[j]
        a,b=radius if isinstance(radius,(tuple,list)) else (radius,radius)
        for k in range(n):
            angle=2*math.pi*k/n
            verts.append(tuple(p+x*(a*math.cos(angle))+z*(b*math.sin(angle))))
    faces=[tuple(reversed(range(n)))]
    for j in range(len(pts)-1):
        for k in range(n):
            a=j*n+k;b=j*n+(k+1)%n;c=(j+1)*n+(k+1)%n;d=(j+1)*n+k
            faces.extend([(a,b,c),(a,c,d)])
    faces.append(tuple((len(pts)-1)*n+k for k in range(n)))
    return mesh(name,verts,faces,mat,select)

def ellipsoid(name,center,scale,mat,n=12,rings=5):
    cx,cy,cz=center;sx,sy,sz=scale;verts=[(cx,cy,cz-sz)]
    for j in range(1,rings):
        phi=-math.pi/2+math.pi*j/rings
        for k in range(n):
            theta=2*math.pi*k/n
            verts.append((cx+sx*math.cos(phi)*math.cos(theta),cy+sy*math.cos(phi)*math.sin(theta),cz+sz*math.sin(phi)))
    top=len(verts);verts.append((cx,cy,cz+sz));faces=[]
    for k in range(n):faces.append((0,1+(k+1)%n,1+k))
    for j in range(rings-2):
        for k in range(n):
            a=1+j*n+k;b=1+j*n+(k+1)%n;faces.append((a,b,b+n,a+n))
    for k in range(n):faces.append((1+(rings-2)*n+k,1+(rings-2)*n+(k+1)%n,top))
    return mesh(name,verts,faces,mat)

def body_color(poly,verts):
    if poly.center.z<.79:return 'belly'
    if poly.center.z<1.15:return 'flank'
    return 'skin'

# Deep barrel, short stout neck, and muscular tapering tail.
tube('Barrel torso',[(0,-.86,1.10),(0,-.69,1.10),(0,-.40,1.08),(0,-.05,1.07),
     (0,.32,1.07),(0,.66,1.06),(0,.90,1.04),(0,1.06,1.02)],
     [(.25,.25),(.44,.33),(.54,.37),(.59,.39),(.57,.39),(.48,.36),(.33,.28),(.15,.20)],n=16,select=body_color)
tube('Short muscular neck',[(0,-.60,1.10),(0,-.88,1.12),(0,-1.02,1.13)],[(.33,.33),(.30,.29),(.27,.25)],n=12)
tube('Tapering muscular tail',[(0,.80,1.08),(.02,1.12,1.02),(.04,1.48,.88),(.08,1.86,.73),
     (.14,2.20,.65),(.22,2.51,.65),(.30,2.80,.70)],
     [(.25,.25),(.205,.20),(.145,.15),(.096,.10),(.060,.066),(.031,.037),(.004,.005)],n=10)

# Four distinct load-bearing limbs; roots intentionally overlap the barrel.
for s,label in [(-1,'Left'),(1,'Right')]:
    tube(label+' forelimb',[(s*.34,-.57,1.19),(s*.43,-.57,.91),(s*.46,-.51,.63),(s*.44,-.62,.35),(s*.44,-.66,.13)],
         [(.205,.23),(.185,.19),(.13,.14),(.107,.115),(.12,.13)],n=10)
    tube(label+' powerful hindlimb',[(s*.32,.63,1.15),(s*.42,.70,.93),(s*.49,.79,.66),(s*.46,.64,.42),(s*.46,.57,.14)],
         [(.26,.28),(.235,.27),(.17,.18),(.125,.135),(.12,.14)],n=12)
    for kind,y,x in [('fore',-.69,s*.44),('hind',.59,s*.46)]:
        verts=[];outline=[(-.135,-.17),(.135,-.17),(.17,-.06),(.15,.13),(-.15,.13),(-.17,-.06)]
        for z,factor in [(0,1),(.075,1.02),(.18,.69)]:verts.extend([(x+dx*factor,y+dy*factor,z) for dx,dy in outline])
        faces=[tuple(reversed(range(6)))]
        for j in range(2):
            for k in range(6):faces.append((j*6+k,j*6+(k+1)%6,(j+1)*6+(k+1)%6,(j+1)*6+k))
        faces.append(tuple(range(12,18)));mesh(label+' '+kind+' weight-bearing foot',verts,faces,'flank')
        for toe,dx in enumerate([-.09,0,.09]):
            ellipsoid(label+' '+kind+' hoof '+str(toe+1),(x+dx,y-.157,.052),(.043,.052,.047),'horn',n=8,rings=3)

# Short deep muzzle, deep lower jaw, hooked keratin beak.
tube('Short deep cranium',[(0,-.92,1.13),(0,-1.09,1.14),(0,-1.28,1.10),(0,-1.46,1.03),(0,-1.58,.98)],
     [(.27,.24),(.31,.28),(.245,.25),(.19,.21),(.135,.16)],n=12)
tube('Deep lower jaw',[(0,-.98,.88),(0,-1.17,.83),(0,-1.41,.80),(0,-1.58,.83)],
     [(.245,.13),(.225,.13),(.162,.10),(.092,.067)],mat='belly',n=10)
tube('Rostral keratin beak',[(0,-1.52,1.00),(0,-1.63,.95),(0,-1.70,.86)],[(.147,.155),(.113,.125),(.023,.043)],mat='horn',n=10)

# Tall solid living frill, narrowing distally. No exposed skeletal windows.
rows=[(1.10,.24,-.86),(1.27,.39,-.79),(1.45,.44,-.69),(1.63,.40,-.60),(1.79,.31,-.55)]
xs=[-1,-.75,-.5,-.25,0,.25,.5,.75,1];verts=[]
for side in [-1,1]:
    for r,(z,w,y) in enumerate(rows):
        for t in xs:
            dz=-.075*(1-abs(t)) if r==4 else 0
            verts.append((w*t,y+.095*t*t+side*.045,z+dz))
faces=[];face_mats=[];nr=len(rows);nx=len(xs);layer=nr*nx
for fs in range(2):
    for r in range(nr-1):
        for k in range(nx-1):
            a=fs*layer+r*nx+k;b=a+1;c=b+nx;d=a+nx
            faces.extend([(a,b,c),(a,c,d)])
            col='frill' if fs==0 and 0<k<nx-2 and r>0 else 'skin'
            face_mats.extend([col,col])
edge=list(range(nx))+[r*nx+nx-1 for r in range(1,nr)]+list(range((nr-1)*nx+nx-2,(nr-1)*nx-1,-1))+[r*nx for r in range(nr-2,0,-1)]
for i,a in enumerate(edge):
    b=edge[(i+1)%len(edge)];faces.append((a,b,b+layer,a+layer));face_mats.append('skin')
ob=mesh('Tall tapering living frill',verts,faces)
for p,c in zip(ob.data.polygons,face_mats):p.material_index=MI[c]

for s,label in [(-1,'Left'),(1,'Right')]:
    tube(label+' curved rear frill horn',[(s*.29,-.50,1.74),(s*.31,-.46,1.87),(s*.35,-.43,2.02),
         (s*.43,-.42,2.15),(s*.54,-.45,2.23),(s*.66,-.50,2.23)],
         [.071,.062,.048,.034,.020,.003],mat='horn',n=10)
    tube(label+' long brow horn',[(s*.205,-1.17,1.30),(s*.215,-1.19,1.40),(s*.23,-1.24,1.52),(s*.25,-1.30,1.58)],
         [.071,.053,.027,.003],mat='horn',n=10)
    tube(label+' projecting cheek blade',[(s*.245,-1.03,1.02),(s*.35,-1.00,.95),(s*.405,-1.02,.80)],
         [(.12,.07),(.09,.06),(.008,.008)],mat='skin',n=8)
    for j,(x,y,z) in enumerate([(.38,-.68,1.28),(.445,-.57,1.45),(.397,-.49,1.62)]):
        tube(label+' frill marginal node '+str(j+1),[(s*(x-.035),y,z),(s*(x+.040),y+.005,z+.015)],[.032,.003],mat='horn',n=8)
    ellipsoid(label+' orbital eyelid',(s*.285,-1.17,1.21),(.041,.080,.060),'skin',n=10,rings=4)
    ellipsoid(label+' eye',(s*.315,-1.184,1.215),(.020,.045,.033),'dark',n=10,rings=4)
    ellipsoid(label+' eye glint',(s*.330,-1.194,1.229),(.004,.009,.008),'horn',n=8,rings=3)
    ellipsoid(label+' nostril',(s*.148,-1.493,1.075),(.013,.029,.018),'dark',n=8,rings=3)
    tube(label+' narrow mouth crease',[(s*.131,-1.57,.866),(s*.189,-1.43,.855),(s*.244,-1.23,.902),(s*.259,-1.08,.947)],
         [.008,.008,.007,.005],mat='dark',n=6,lateral=(0,0,1))
# Low nasal boss: deliberately NOT the long hooked Einiosaurus horn.
tube('Low nasal ornament',[(0,-1.43,1.188),(0,-1.45,1.237),(0,-1.47,1.245)],[(.067,.074),(.044,.045),(.005,.006)],mat='horn',n=10)

# Center the actual four-foot contact envelope, not the head/tail bounds.
contact=[v.co for ob in COL.objects if ob.type=='MESH' for v in ob.data.vertices if abs(v.co.z)<1e-8]
contact_center_y=(min(v.y for v in contact)+max(v.y for v in contact))/2
for ob in COL.objects:
    if ob.type=='MESH':
        for v in ob.data.vertices:v.co.y-=contact_center_y
ROOT['origin']='center of four-foot floor-contact envelope'
ROOT['taxon']='Diabloceratops eatoni';ROOT['representation']='living reconstruction; postcranium inferred'
ROOT['revision']='r001';ROOT['body_length_target_m']=4.5
ROOT['scientific_uncertainty']='Skull based, inferred full body, skin and colour. No open living frill windows.'
bpy.context.view_layer.update();source=audit_source(COL,max_triangles=6500)
if source['errors']:raise RuntimeError(source['errors'])
bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
bpy.context.scene['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
bpy.context.scene['params_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))

# Keep source semantically editable. Combine only the temporary export by palette.
originals=[ob for ob in COL.objects if ob.type=='MESH'];verts=[];faces=[];mats=[]
for ob in originals:
    base=len(verts);verts.extend([tuple(ob.matrix_world@v.co) for v in ob.data.vertices])
    for p in ob.data.polygons:
        faces.append(tuple(base+i for i in p.vertices));mats.append(p.material_index)
combined=mesh('Diabloceratops export palette mesh',verts,faces)
for p,m in zip(combined.data.polygons,mats):p.material_index=m
for ob in originals:bpy.data.objects.remove(ob,do_unlink=True)
bpy.ops.object.select_all(action='DESELECT');ROOT.select_set(True);combined.select_set(True)
bpy.context.view_layer.objects.active=combined
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,
    export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',
    export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,
    export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,
    export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available:raise RuntimeError('Required exporter flags unavailable')
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',max_triangles=6500,max_materials=6,max_primitives=12)
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>2000000:raise RuntimeError('Frozen byte budget exceeded')
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(glb['bounds_m'][key][i]-expected[key][i]) for key in ('min','max') for i in range(3))
if delta>.0001 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source-export mismatch')
report={'asset_id':'diabloceratops','revision':'r001','blender_version':bpy.app.version_string,'source':source,'glb':glb,
        'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},
        'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),
        'source_editability':'Named anatomical parts retained in model.blend; only export combined.',
        'model_blend_sha256':hashlib.sha256((OUT/'model.blend').read_bytes()).hexdigest()}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('COMPLETE',glb['scene_triangles'],'triangles;',glb['bytes'],'GLB bytes;',glb['sha256'])
