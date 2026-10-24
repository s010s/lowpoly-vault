# SPDX-License-Identifier: MIT
"""Original deterministic Embolotherium andrewsi reconstruction.
Run inside Blender: --python source/generate.py -- --output-dir OUTPUT
Only source/params.json and pinned source/deps are required to rebuild.
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
A=argparse.ArgumentParser(); A.add_argument('--output-dir',type=Path,required=True)
args=A.parse_args(sys.argv[sys.argv.index('--')+1:])
OUT=args.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene(P['asset_id'],P['seed'])
MAT={k:make_material(k,c,roughness=0.88 if k!='eyes' else .32) for k,c in P['palette_srgb_hex'].items()}

def write(name,verts,faces,mat):
    return mesh_object(name,verts,faces,MAT[mat] if isinstance(mat,str) else mat,COL)

def closed_rings(name,rings,mat):
    n=len(rings[0]); verts=[v for r in rings for v in r]
    faces=[]
    for j in range(len(rings)-1):
        for i in range(n):
            faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
    for j in [0,len(rings)-1]:
        center=tuple(sum(v[k] for v in rings[j])/n for k in range(3)); c=len(verts);verts.append(center)
        for i in range(n): faces.append((c,j*n+i,j*n+(i+1)%n))
    return write(name,verts,faces,mat)

def along_y(name,sections,mat,n=32,head=False):
    rings=[]
    for y,w,lo,hi in sections:
        ring=[]
        for i in range(n):
            a=2*math.pi*i/n; s=math.sin(a); c=math.cos(a)
            if head:
                # Rounded broad nasal rim, a full fleshy side and deep jaw.
                exponent=.35 if y<-2.25 else .72
                xf=math.copysign(abs(s)**exponent,s)
                zf=math.copysign(abs(c)**(.35 if y<-2.25 else .82),c)
                x=w*xf*(1.0 if c>=0 else .91)
            else: x=w*s; zf=c
            ring.append((x,y,(lo+hi)/2+(hi-lo)*.5*zf))
        rings.append(ring)
    return closed_rings(name,rings,mat)

def tube(name,points,radii,mat,n=12):
    rings=[]
    for j,(p,r) in enumerate(zip(points,radii)):
        p=Vector(p); tangent=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(j-1,0)])
        tangent.normalize(); base=Vector((1,0,0)) if abs(tangent.x)<.8 else Vector((0,1,0)); u=tangent.cross(base).normalized();v=tangent.cross(u).normalized()
        if isinstance(r,(int,float)): r=(r,r)
        rings.append([tuple(p+u*(r[0]*math.cos(2*math.pi*i/n))+v*(r[1]*math.sin(2*math.pi*i/n))) for i in range(n)])
    return closed_rings(name,rings,mat)

def vertical(name,sections,mat,n=16):
    # Sections encode articulated center, width and front/back radius.
    rings=[]
    for x,y,z,rx,ry in sections:
        rings.append([(x+rx*math.cos(2*math.pi*i/n),y+ry*math.sin(2*math.pi*i/n),z) for i in range(n)])
    return closed_rings(name,rings,mat)

body=along_y('barrel-shoulder-and-rump',[
(-1.18,.29,1.36,2.10),(-1.06,.43,1.15,2.23),(-.88,.58,1.02,2.31),(-.66,.66,.93,2.32),(-.43,.72,.88,2.27),(-.13,.75,.85,2.20),(.20,.76,.84,2.15),(.53,.74,.85,2.12),(.83,.69,.89,2.10),(1.08,.60,1.00,2.04),(1.29,.46,1.17,1.94),(1.43,.27,1.37,1.78),(1.47,.08,1.51,1.65)],'body')
# A short deep rising neck, neither elephant neck nor disconnected head sphere.
along_y('strong-neck', [(-1.52,.25,1.42,2.30),(-1.36,.39,1.26,2.42),(-1.18,.48,1.15,2.46),(-.98,.53,1.09,2.41),(-.79,.51,1.16,2.29),(-.65,.35,1.35,2.15)],'body',24)
head=along_y('integrated-nasal-ram-snout-cheek',[
(-2.58,.18,1.48,2.48),(-2.53,.31,1.40,2.62),(-2.45,.44,1.36,2.68),(-2.33,.46,1.32,2.57),(-2.20,.42,1.29,2.39),(-2.04,.37,1.26,2.24),(-1.85,.34,1.25,2.17),(-1.66,.36,1.24,2.22),(-1.47,.41,1.28,2.36),(-1.28,.44,1.37,2.53),(-1.10,.40,1.52,2.60),(-.96,.28,1.72,2.51),(-.90,.15,1.91,2.34)],[MAT['body'],MAT['muzzle'],MAT['underside']],32,True)
# Face-level restrained soft-tissue regions, not a pale bare horn.
for face in head.data.polygons:
    pts=[head.data.vertices[i].co for i in face.vertices]; z=sum(v.z for v in pts)/len(pts);y=sum(v.y for v in pts)/len(pts)
    face.material_index=2 if z<1.43 else 1 if y<-2.13 else 0
# Deep lower lip and chin follow the anatomical mandibular profile.
along_y('lower-lip-chin', [(-2.48,.15,1.34,1.45),(-2.36,.29,1.25,1.46),(-2.16,.34,1.20,1.43),(-1.93,.34,1.19,1.40),(-1.71,.32,1.23,1.42),(-1.49,.29,1.31,1.51)],'muzzle',20,True)
for side,label in [(-1,'left'),(1,'right')]:
    for front in [True,False]:
        pos='fore' if front else 'hind'; x=side*(.51 if front else .50); y=-.73 if front else .99
        # Small stagger keeps all four load-bearing columns legible obliquely.
        shift=(.075 if side==-1 else -.025) if front else (-.05 if side==-1 else .04)
        if front:
            sections=[(x*.70,y+shift,2.12,.13,.20),(x*.94,y+shift,1.91,.265,.29),(x*1.05,y-.01+shift,1.66,.29,.29),(x*1.10,y-.04+shift,1.35,.26,.26),(x*1.12,y+.01+shift,1.04,.205,.215),(x*1.13,y+.01+shift,.77,.17,.19),(x*1.14,y-.055+shift,.46,.16,.18),(x*1.14,y-.11+shift,.23,.205,.235),(x*1.14,y-.12+shift,.10,.22,.26)]
        else:
            sections=[(x*.65,y+shift,1.99,.13,.18),(x*.93,y+shift,1.75,.27,.30),(x*1.07,y-.06+shift,1.51,.285,.31),(x*1.12,y-.16+shift,1.23,.24,.26),(x*1.15,y-.08+shift,.98,.19,.21),(x*1.16,y+.11+shift,.70,.155,.18),(x*1.17,y+.10+shift,.43,.145,.16),(x*1.17,y+.02+shift,.22,.19,.22),(x*1.17,y+shift,.10,.215,.25)]
        vertical(label+'-'+pos+'-limb',sections,'body')
        fx,fy=sections[-1][:2]
        vertical(label+'-'+pos+'-foot-pad',[(fx,fy,.01,.20,.235),(fx,fy,.10,.23,.26),(fx,fy,.20,.205,.23),(fx,fy+.025,.29,.16,.17)],'body',16)
        count=4 if front else 3
        for t in range(count):
            dx=(t-(count-1)/2)*(.108 if front else .135)
            scale=.85 if front and t in [0,3] else 1
            tx=fx+dx; ty=fy-.195+(abs(dx)*.18)
            vertical(label+'-'+pos+'-toe-'+str(t+1),[(tx,ty,0,.046*scale,.085*scale),(tx,ty-.012,.045,.052*scale,.092*scale),(tx,ty-.006,.12,.049*scale,.084*scale),(tx,ty+.025,.17,.033*scale,.055*scale)],'hooves',12)
    # Small lateral ears with an outer skin rim and a darker recessed center.
    tube(label+'-ear',[(side*.31,-1.04,2.40),(side*.48,-1.015,2.49),(side*.67,-.99,2.53),(side*.75,-.97,2.51)],[(.09,.105),(.13,.13),(.09,.095),(.018,.025)],'body',12)
    tube(label+'-ear-inner',[(side*.47,-1.115,2.485),(side*.60,-1.095,2.515),(side*.69,-1.07,2.513)],[(.04,.028),(.065,.035),(.022,.015)],'muzzle',10)
    # Tiny low-profile eyes, framed with fleshy rather than protruding sockets.
    tube(label+'-orbital-ridge',[(side*.335,-1.66,2.025),(side*.375,-1.62,2.065),(side*.403,-1.55,2.075),(side*.412,-1.49,2.055)], [.025,.035,.033,.02],'body',10)
    tube(label+'-eye',[(side*.355,-1.586,2.013),(side*.397,-1.586,2.013),(side*.414,-1.586,2.013)],[(.047,.033),(.049,.034),(.025,.019)],'eyes',12)
    # Opaque shallow nostril patches, not tubes or detached cavities.
    tube(label+'-nostril',[(side*.390,-2.31,1.72),(side*.424,-2.31,1.72),(side*.432,-2.31,1.72)],[(.060,.036),(.064,.034),(.035,.021)],'nostrils',12)
    tube(label+'-mouth-seam',[(side*.29,-2.44,1.445),(side*.35,-2.29,1.433),(side*.354,-2.12,1.414),(side*.348,-1.94,1.405),(side*.337,-1.77,1.423),(side*.325,-1.67,1.452)],[.008,.012,.013,.013,.012,.006],'nostrils',8)
# Curved, tapering tail with a modest darker terminal tuft.
tube('tapering-tail',[(0,1.33,1.74),(.025,1.57,1.60),(.055,1.81,1.45),(.08,2.02,1.27),(.11,2.21,1.13),(.13,2.33,1.17)],[.105,.09,.065,.048,.030,.010],'body',12)
tube('tail-tip',[(.105,2.15,1.15),(.12,2.25,1.115),(.135,2.36,1.16)],[.037,.052,.009],'hooves',12)
bpy.context.view_layer.update()
source=audit_source(COL,P['geometry_budget']['max_triangles'])
if source['errors']: raise RuntimeError(source['errors'])
root=bpy.data.objects[COL['asset_root']]
root['representation']='living-reconstruction';root['taxon']='Embolotherium andrewsi';root['revision']=P['revision']
# Use a runtime-resolved absolute output path, independent of caller working dir.
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//render'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params is not None:
                space.params.directory=b'//'
                space.params.filename=''

bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'),relative_remap=False)
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects: ob.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available: raise RuntimeError('Missing exporter flags: '+repr(set(opts)-available))
bpy.ops.export_scene.gltf(**opts)
budget=P['geometry_budget']; report=audit_glb(OUT/'model.glb',budget['max_triangles'],budget['max_materials'],budget['max_primitives']); report['file']='model.glb'
if report['bytes']>budget['max_glb_bytes']: report['errors'].append('GLB byte budget exceeded')
b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(report['bounds_m'][side][i]-expected[side][i]) for side in ['min','max'] for i in range(3))
if delta>1e-4 or source['triangles']!=report['scene_triangles']: raise RuntimeError('Source/export geometry mismatch')
if report['errors']: raise RuntimeError(report['errors'])
record={'asset_id':P['asset_id'],'revision':P['revision'],'blender_version':bpy.app.version_string,'exporter_version':list(__import__('io_scene_gltf2').bl_info['version']),'source':source,'glb':report,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'inputs':{'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()},'scope':'Source and static GLB checks only. Not independent QA, GPU, scene, or publication approval.'}
(OUT/'build-report.json').write_text(json.dumps(record,indent=2)+'\n')
print('BUILD_COMPLETE',report['scene_triangles'],report['scene_primitives_estimated_base_draw_calls'],report['bytes'],report['sha256'])
