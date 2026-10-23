# SPDX-License-Identifier: MIT
"""Deterministic, editable Mecochirus longimanatus restoration, r001.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Only params.json and declared source/deps are runtime inputs. Numeric units: meters.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=argparse.ArgumentParser(); args.add_argument('--out',type=Path,required=True)
a=args.parse_args(sys.argv[sys.argv.index('--')+1:])
out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
collection=setup_scene('mecochirus',P['seed'])
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
mats=[make_material('01_Carapace_russet','#965C3C',.84),make_material('02_Dorsal_umber','#644831',.88),make_material('03_Pleura_ochre','#C18C54',.9),make_material('04_Joint_shadow','#493A2C',.93),make_material('05_Eye_carbon','#262724',.48)]
parts=[];paths={}
def record(obj,name,role):
    obj['anatomy']=role;parts.append({'name':name,'role':role,'vertices':len(obj.data.vertices)});return obj

def tube(name,points,radii,mat=0,sides=10,role='appendage'):
    points=[Vector(v) for v in points];v=[];f=[]
    for i,p in enumerate(points):
        tangent=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
        ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((1,0,0))
        u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
        r=radii[i];r=(r,r) if isinstance(r,(int,float)) else r
        for j in range(sides):
            t=2*math.pi*j/sides;v.append(tuple(p+u*(math.cos(t)*r[0])+w*(math.sin(t)*r[1])))
    for i in range(len(points)-1):
        for j in range(sides):k=i*sides+j; n=i*sides+(j+1)%sides;f.append((k,n,n+sides,k+sides))
    f.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))])
    ob=mesh_object(name,v,f,mats[mat],collection);return record(ob,name,role)

def shell(name,rings,role='body',sides=20):
    # Rings: longitudinal center y,z; transverse half width; vertical half-depth.
    v=[];f=[]
    for y,z,rx,rz in rings:
        for j in range(sides):
            t=2*math.pi*j/sides;x=rx*math.sin(t);zz=rz*math.cos(t)
            # Broad convex roof, mildly flattened ventral surface.
            if zz<0:zz*=.84
            v.append((x,y,z+zz))
    for i in range(len(rings)-1):
        for j in range(sides):f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    f.extend([tuple(reversed(range(sides))),tuple((len(rings)-1)*sides+j for j in range(sides))])
    ob=mesh_object(name,v,f,mats[:4],collection)
    for poly in ob.data.polygons:
        if poly.center.z>sum(x[1] for x in rings)/len(rings)+.005:poly.material_index=1
        elif poly.center.z<sum(x[1] for x in rings)/len(rings)-.004:poly.material_index=2
        else:poly.material_index=0
    return record(ob,name,role)

def plate(name,outline,depth,mat=2,role='pleuron'):
    # Closed shallow plate from front outline, thickness along x.
    v=[(x-depth/2,y,z) for x,y,z in outline]+[(x+depth/2,y,z) for x,y,z in outline]
    n=len(outline);f=[tuple(reversed(range(n))),tuple(n+i for i in range(n))]
    f.extend((i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n))
    return record(mesh_object(name,v,f,mats[mat],collection),name,role)

# Main cephalothorax: length 35 mm, cross-section 18 x 20 mm at its fullest.
shell('Carapace_contoured_35mm',[(-.022,.024,.004,.005),(-.019,.0245,.0068,.0077),(-.014,.024,.0085,.010),(-.005,.024,.009,.0098),(.005,.0235,.0086,.0088),(.0115,.023,.0078,.0078),(.013,.0228,.0068,.0068)],'35 mm cephalothorax')
# The incised cervical groove is a fitted dark shallow band, not a spike or armor ridge.
shell('Cervical_groove_band',[(-.0105,.024,.00894,.01015),(-.0097,.024,.00903,.01013)],'conservative cervical surface groove')
groove=bpy.data.objects['Cervical_groove_band'];groove.data.materials.clear();groove.data.materials.append(mats[3]);[setattr(p,'material_index',0) for p in groove.data.polygons]
# Short downward rostrum and cheek shields.
tube('Rostrum_downturned',[(0,-.021,.029),(0,-.026,.028),(0,-.029,.026)],[(.002,.0015),(.0012,.0009),(.00022,.00022)],0,8,'short downward rostrum')
for s,side in [(-1,'L'),(1,'R')]:
    tube('Eye_stalk_'+side,[(s*.004,-.020,.027),(s*.0068,-.023,.029)], [.001,.00085],2,8,'modest stalked eye')
    tube('Eye_'+side,[(s*.0067,-.0226,.029),(s*.007,-.0238,.0292),(s*.0072,-.0246,.029)], [.00065,.00125,.0005],4,10,'eye; color inferred')
    tube('Antennal_peduncle_'+side,[(s*.0035,-.021,.0245),(s*.006,-.027,.025)], [.0012,.00065],0,8,'antennal base; inferred')
    tube('Antenna_'+side,[(s*.006,-.027,.025),(s*.011,-.040,.026),(s*.017,-.052,.024),(s*.024,-.062,.021)], [.00048,.00037,.00024,.00012],2,7,'conservative antenna; length inferred')
    tube('Antennule_'+side,[(s*.0019,-.022,.026),(s*.0024,-.033,.026),(s*.004,-.041,.024)], [.00045,.00027,.00012],0,7,'short antennule; inferred')
# Six abdominal somites with individually fitted, pointed ventral pleura.
for i in range(6):
    y=.015+i*.0059;z=.0220-i*.00125
    rx=.0075-i*.00055;rz=.0066-i*.00046
    shell('Abdominal_somite_%d'%(i+1),[(y-.0014,z,rx*.94,rz*.9),(y+.0001,z+.00015,rx,rz),(y+.0034,z-.00045,rx*.96,rz*.91),(y+.0044,z-.0008,rx*.87,rz*.82)],'abdominal segment %d of 6'%(i+1),16)
    for s,side in [(-1,'L'),(1,'R')]:
        x=s*rx*.83
        plate('Pointed_pleuron_%d_%s'%(i+1,side),[(x,y-.0007,z-.001),(x,y+.0038,z-.0019),(x,y+.0050,z-.0064),(x,y+.0010,z-.0048)],.0010,2,'pointed abdominal pleuron')
# Living abdomen has continuous flexible tissue under the overlapping shell somites.
# This under-shell core removes through-gaps without erasing articulation seams.
shell('Abdominal_flexible_core',[(.010,.0225,.0056,.0047),(.018,.0216,.0062,.0050),(.030,.0190,.0052,.0042),(.042,.0166,.0042,.0035),(.050,.0150,.0030,.0026)],'continuous inferred intersegment connective tissue',16)
core=bpy.data.objects['Abdominal_flexible_core'];core.data.materials.clear();core.data.materials.append(mats[3]);[setattr(p,'material_index',0) for p in core.data.polygons]
# Tail fan: central telson, bilateral exopod and endopod blades with visible taper.
def fan(name,outline,z):
    v=[(x,y,z+dz) for x,y,dz in outline]+[(x,y,z+dz-.00065) for x,y,dz in outline]
    n=len(outline);f=[tuple(range(n)),tuple(reversed([n+i for i in range(n)]))]
    f.extend((i,n+i,n+(i+1)%n,(i+1)%n) for i in range(n))
    record(mesh_object(name,v,f,mats[0:3],collection),name,'closed tail fan blade')
    ob=bpy.data.objects[name]
    for p in ob.data.polygons:p.material_index=2 if len(p.vertices)==n else 0
fan('Telson', [(-.0038,.049,0),(.0038,.049,0),(.0032,.0575,-.001),(.0015,.060,-.0015),(-.0015,.060,-.0015),(-.0032,.0575,-.001)],.0150)
for s,side in [(-1,'L'),(1,'R')]:
    fan('Uropod_inner_'+side,[(s*.002,.0477,0),(s*.006,.0487,0),(s*.010,.057,-.001),(s*.007,.059,-.0013),(s*.0039,.0565,-.001)],.0152)
    fan('Uropod_outer_'+side,[(s*.0045,.047,0),(s*.009,.0476,0),(s*.016,.054,-.001),(s*.015,.057,-.0014),(s*.010,.0565,-.0012)],.0150)
# P1: noninflated articulated limb, 155 mm path including one movable finger.
lengths=[.006,.011,.045,.016,.050,.027]
for s,side in [(-1,'L'),(1,'R')]:
    p=Vector((s*.006,-.018,.019));p1=[p.copy()]
    dirs=[(s*1,-.25,-.4),(s*.35,-1,-.15),(s*.20,-1,-.02),(s*.55,-1,-.08),(-s*.24,-1,-.035),(s*.42,.91,-.055)]
    # Right distal finger slightly more open: relaxed live pose, not compressed fossil layout.
    if s==1: dirs[-1]=(s*.65,.76,-.055)
    names=['coxa','ischium','merus','carpus','propodus','movable_dactylus']
    radii=[(.0014,.0016),(.0015,.00165),(.0018,.0020),(.0019,.0020),(.00205,.00155),(.00125,.00016)]
    for i,(L,d,n,rr) in enumerate(zip(lengths,dirs,names,radii)):
        q=p+Vector(d).normalized()*L
        mid=p+(q-p)*.52
        tube('P1_%s_%s'%(side,n),[tuple(p),tuple(mid),tuple(q)],[rr[0],max(rr)*1.04,rr[1]],0 if i!=5 else 2,10,'first walking leg %s: %s'%(side,n))
        # Articulation cuff stays small. Dactylus folds toward the propodal margin.
        if i<5:
            k=p+(q-p)*.96
            tube('P1_%s_joint_%d'%(side,i+1),[tuple(k),tuple(q)],[rr[1]*1.08,rr[1]*1.08],3,10,'P1 joint articulation')
        p=q;p1.append(q.copy())
    # Single short fixed distal stop, not a second long finger.
    q=p1[-2];back=(p1[-3]-q).normalized()
    tube('P1_%s_propodos_stop'%side,[tuple(q+Vector((0,0,-.0003))),tuple(q+back*.0033+Vector((-s*.0018,0,-.0002)))],[.0008,.00022],2,8,'minor fixed propodal stop; subchelate ending')
    paths[side]={'path_vertices_m':[list(x) for x in p1],'segment_lengths_m':lengths,'total_articulated_path_m':sum((p1[j+1]-p1[j]).length for j in range(len(lengths))),'propodus_length_m':lengths[-2],'movable_dactylus_length_m':lengths[-1]}
# P2-P5, four pairs; staggered, grounded, much shorter than P1.
for i in range(4):
    y=-.010+i*.0063
    for s,side in [(-1,'L'),(1,'R')]:
        root=Vector((s*.0065,y,.018-i*.00025))
        elbow=Vector((s*(.0148+i*.0008),y+(-.007+i*.003),.013))
        wrist=Vector((s*(.0215+i*.0012),y+(-.011+i*.006),.005))
        end=Vector((s*(.0240+i*.0012),y+(-.015+i*.007),.00032))
        points=[root,elbow,wrist,end]
        for j in range(3):
            tube('P%d_%s_segment_%d'%(i+2,side,j+1),[tuple(points[j]),tuple((points[j]+points[j+1])*.5),tuple(points[j+1])],[.0010-j*.0002,.00105-j*.00025,.0008-j*.00024],0 if j<2 else 2,8,'walking leg pair %d of 5'%(i+2))
        if i<2:
            # Family-level inference only; small terminal hook, no enlarged chela.
            tube('P%d_%s_minor_subchelate_tip'%(i+2,side),[tuple(end),tuple(end+Vector((-s*.0012,-.0018,.0001)))],[.00035,.00013],2,7,'inferred family-level P2/P3 terminal hook')
        paths['P%d_%s'%(i+2,side)]=[list(x) for x in points]
# Two short folded maxilliped pairs beneath the face, deliberately not ground walking legs.
for s,side in [(-1,'L'),(1,'R')]:
    tube('Folded_maxilliped_'+side,[(s*.002,-.020,.019),(s*.004,-.023,.016),(s*.0018,-.025,.017)],[.0008,.0007,.0004],3,8,'short mouthpart, not a walking-leg pair')
# Ground by a uniform translation, keep root identity and centered footprint in X/Y.
bpy.context.view_layer.update();minz=min((o.matrix_world@v.co).z for o in collection.all_objects if o.type=='MESH' for v in o.data.vertices)
for o in collection.all_objects:
    if o.type=='MESH':
        for v in o.data.vertices:v.co.z-=minz
# Source meshes are separate editable semantic parts; all have unit transforms.
source=audit_source(collection,max_triangles=40000)
if source['errors']:raise RuntimeError(json.dumps(source['errors']))
scene['representation']='Living reconstruction, Late Jurassic Mecochirus longimanatus; widths, colors and small terminals inferred.'
scene['model_dimensions_note']='CL 35 mm; body approximately 85 mm; P1 path 155 mm, not span.'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
# Join for static export only after saving the fully editable source. One mesh/5 primitives.
bpy.ops.object.select_all(action='DESELECT')
meshes=[o for o in collection.all_objects if o.type=='MESH']
for o in meshes:o.select_set(True)
bpy.context.view_layer.objects.active=meshes[0]
bpy.ops.object.join();joined=bpy.context.object;joined.name='Mecochirus_static_surface'
root=bpy.data.objects[collection['asset_root']];root.select_set(True)
options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Missing exporter options: '+repr(missing))
bpy.ops.export_scene.gltf(**options)
report=audit_glb(out/'model.glb',40000,6,8)
if report['errors']:raise RuntimeError(json.dumps(report['errors']))
b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(report['bounds_m'][k][i]-expected[k][i]) for k in ('min','max') for i in range(3))
if delta>1e-6 or source['triangles']!=report['scene_triangles']:raise RuntimeError('Source/export mismatch')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(out/n).write_text(json.dumps(d,indent=2)+'\n')
write('source-audit.json',source);write('glb-audit.json',report)
write('anatomy.json',{'asset_id':'mecochirus','revision':'r001','walking_leg_pairs':5,'abdominal_segments':6,'semantic_source_parts':parts,'articulation':paths,'ground_translation_m':-minz,'scale_notes':P['note'],'terminal_small_legs_inferred':True,'long_P1_not_opposed_giant_chela':True})
write('build.json',{'blender_version':bpy.app.version_string,'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'semantic_sha256':report['semantic_sha256'],'bounds_roundtrip_error_m':delta,'source_triangles':source['triangles'],'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_part_count':len(parts),'seed':P['seed'],'render_threads':2})
print('MECOCHIRUS_BUILD_OK',report['scene_triangles'],report['sha256'])
