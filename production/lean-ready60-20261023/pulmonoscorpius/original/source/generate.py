# SPDX-License-Identifier: MIT
"""Deterministic Pulmonoscorpius living reconstruction in specimen-estimated meters.
Run with Blender 4.3.2: blender -b -t 2 --python generate.py -- --output MODEL_DIR
Only params.json and the explicitly inventoried local deps are required.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source, ground_asset
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
A=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args(A)
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True); (OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
COL=setup_scene(P['asset_id'],P['seed']); root=bpy.data.objects[COL['asset_root']]
root['interpretation']='NMS G.1987.7.136 photo-scale; genus-level restored limbs, thickness, pose and color.'
root['anatomy_counts']='4 walking pairs; 1 pedipalp pair; 1 cheliceral pair; 7 tergites; 5 metasomal segments; 1 telson'
M=[make_material(n,c,roughness=r) for n,c,r in P['palette']]
parts=[]
YOFF=P['body_y_offset_m']
def pos(p): return (p[0],p[1]+YOFF,p[2])
def make(name,vs,fs,mi):
    ob=mesh_object(name,[pos(p) for p in vs],fs,M[mi],COL); parts.append(ob); return ob

def axial(name,rings,mi=0,n=16,exponent=1):
    # Closed transverse section loft, consciously flattened ventral profile.
    vs=[]
    for y,w,z,d in rings:
        for j in range(n):
            a=2*math.pi*j/n; c=math.cos(a); s=math.sin(a)
            x=w*math.copysign(abs(c)**exponent,c)
            h=d*math.copysign(abs(s)**0.82,s)*(1 if s>=0 else .68)
            vs.append((x,y,z+h))
    fs=[]
    for i in range(len(rings)-1):
        for j in range(n): fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))])
    return make(name,vs,fs,mi)

def tube(name,points,radii,mi=0,n=8,flatten=1):
    pts=[Vector(p) for p in points]; vs=[]
    for i,p in enumerate(pts):
        t=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        u=t.cross(Vector((0,0,1)))
        if u.length<.1: u=Vector((1,0,0))
        u.normalize(); v=t.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n
            vs.append(tuple(p+u*math.cos(a)*radii[i]+v*math.sin(a)*radii[i]*flatten))
    fs=[]
    for i in range(len(pts)-1):
        for j in range(n): fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    fs.extend([tuple(reversed(range(n))),tuple((len(pts)-1)*n+j for j in range(n))])
    return make(name,vs,fs,mi)

def limb_segment(name,a,b,r,mi=0,n=10):
    a=Vector(a); b=Vector(b); vec=b-a
    return tube(name,[a,a+vec*.13,a+vec*.56,a+vec*.88,b],[r*.70,r,r*.97,r*.76,r*.57],mi,n,.83)

def ellipsoid(name,c,r,mi=2,n=12):
    # Profile-generated joint/eye, not an unedited primitive.
    c=Vector(c); pts=[]; rs=[]
    for t,s in [(-1,.13),(-.8,.65),(0,1),(.8,.65),(1,.13)]:
        pts.append(tuple(c+Vector((0,t*r[1],0)))); rs.append(r[0]*s)
    return tube(name,pts,rs,mi,n,r[2]/r[0])

# Prosoma: nearly rectangular dorsal shield and a restrained median eye prominence.
axial('carapace', [(-.050,.017,.031,.009),(-.048,.021,.033,.012),(-.040,.0225,.034,.013),(-.017,.023,.033,.013),(-.003,.023,.0315,.012),(.001,.0195,.030,.009)],0,20,.64)
axial('sternum-underbody',[(-.047,.012,.022,.004),(-.035,.015,.021,.004),(-.012,.014,.021,.004),(.001,.011,.023,.004)],2,12,.8)
ellipsoid('median-eye-prominence',(0,-.037,.0461),(.0033,.0037,.002),1,12)
for side in (-1,1): ellipsoid('median-eye-'+str(side),(side*.0017,-.038,.0478),(.0012,.00155,.00105),4,10)
# Broad mesosoma: seven independently editable dorsal tergites, with articulated seams.
widths=[.0245,.028,.030,.030,.0285,.0255,.019]
ys=[0,.013,.027,.042,.058,.073,.087,.100]
axial('ventral-mesosoma',[(.001,.018,.028,.009),(.03,.0265,.027,.009),(.063,.026,.027,.008),(.088,.017,.028,.007),(.101,.008,.029,.005)],2,16,.9)
for i in range(7):
    a,b=ys[i],ys[i+1]; w=widths[i]; dep=.0125 if i<5 else .011
    z=.0315+.0007*math.sin(i*.5)
    backw=widths[min(i+1,6)] if i<6 else .0085
    axial('mesosoma-tergite-%02d'%(i+1),[(a+.0003,w*.86,z,dep*.76),(a+.002,w,z+.001,dep),(b-.003,w*.96,z,dep*.98),(b-.0005,backw*.92,z-.0004,dep*.77)],0 if i%2==0 else 1,20,.82)
    # Subtle transverse posterior lip catches light without ornamental spikes.
    axial('tergite-rim-%02d'%(i+1),[(b-.0028,w*.955,z-.0001,dep*.98),(b-.0018,w*.96,z-.0001,dep*.995)],3,20,.82)
# Walking appendages: all originate around prosomal coxae, distal reach increases posteriorly.
legs=[(-.041,[(.034,-.043,.027),(.049,-.035,.032),(.071,-.043,.014),(.083,-.048,.002)]),
      (-.028,[(.035,-.019,.028),(.054,-.008,.031),(.079,-.004,.012),(.090,-.009,.002)]),
      (-.014,[(.037,.003,.027),(.056,.022,.030),(.083,.034,.011),(.096,.031,.002)]),
      (-.001,[(.033,.025,.027),(.048,.049,.028),(.079,.073,.010),(.096,.079,.002)])]
for si in (-1,1):
    label='L' if si<0 else 'R'
    for i,(y,chain) in enumerate(legs):
        points=[(.013,y,.022)]+chain
        points=[(si*x,yy,z) for x,yy,z in points]
        radii=[.0038,.0034,.0028,.0019]
        for j in range(4):
            limb_segment('walking-%s%d-segment-%d'%(label,i+1,j+1),points[j],points[j+1],radii[j],0 if j<3 else 3)
            if j<3: ellipsoid('walking-%s%d-joint-%d'%(label,i+1,j+1),points[j+1],(radii[j]*.65,radii[j]*.65,radii[j]*.65),2,8)
        tip=points[-1]; tube('walking-%s%d-tarsal-tip'%(label,i+1),[tip,(tip[0]+si*.004,tip[1]-.001,.0007)],[.0014,.00035],3,8,.7)
    # Long slender pedipalps. Small palm followed by long thin curved fingers.
    pts=[(si*.015,-.047,.026),(si*.032,-.052,.030),(si*.054,-.060,.033),(si*.063,-.080,.036)]
    for j in range(3):
        limb_segment('pedipalp-%s-segment-%d'%(label,j+1),pts[j],pts[j+1],[.0050,.0047,.0036][j],0,12)
        ellipsoid('pedipalp-%s-joint-%d'%(label,j+1),pts[j+1],(.0026,.0026,.0026),2,8)
    tube('chela-%s-palm'%label,[(si*.063,-.077,.036),(si*.064,-.083,.037),(si*.063,-.089,.038),(si*.062,-.094,.038)],[.0028,.0044,.0042,.0026],0,12,.84)
    # Open negative space remains between fingers; palms are never massive.
    tube('chela-%s-fixed-finger'%label,[(si*.066,-.089,.039),(si*.068,-.099,.041),(si*.0665,-.110,.044),(si*.0625,-.119,.045)],[.0021,.0017,.0011,.00035],3,8,.85)
    tube('chela-%s-movable-finger'%label,[(si*.060,-.091,.037),(si*.057,-.100,.039),(si*.058,-.110,.043),(si*.061,-.118,.045)],[.0020,.00165,.00105,.00035],0,8,.85)
    # Small anterior chelicerae; simple inferred chelate outline, not a second large pincer pair.
    tube('chelicera-%s-base'%label,[(si*.006,-.048,.028),(si*.0065,-.056,.030),(si*.006,-.062,.031)],[.0036,.0033,.0020],1,10,.85)
    tube('chelicera-%s-finger-a'%label,[(si*.0075,-.060,.032),(si*.0085,-.065,.033),(si*.0065,-.067,.033)],[.0013,.001,.00035],3,8)
    tube('chelicera-%s-finger-b'%label,[(si*.0045,-.059,.030),(si*.004,-.064,.031),(si*.0055,-.067,.032)],[.0013,.0009,.00035],0,8)
# Five tail units total .112 m centerline, then a .028 m telson/sting.
# Deliberate gentle upcurve instead of a forward-threatening modern pose.
angles=[4,14,27,43,58]
lengths=[.020,.021,.022,.023,.026]
tail=[Vector((0,.100,.031))]
for L,a in zip(lengths,angles): tail.append(tail[-1]+Vector((0,L*math.cos(math.radians(a)),L*math.sin(math.radians(a)))))
for i in range(5):
    a,b=tail[i],tail[i+1]; d=b-a; r=[.0067,.0065,.0061,.0058,.0054][i]
    tube('metasoma-%02d'%(i+1),[a-d.normalized()*.0003,a+d*.12,a+d*.52,a+d*.90,b+d.normalized()*.00025],[r*.74,r,r*.97,r*.79,r*.65],0 if i%2==0 else 1,12,.96)
    if i<4: ellipsoid('metasomal-joint-%02d'%(i+1),b,(r*.59,r*.59,r*.59),2,10)
    # Paired modest longitudinal dorsal carinae, no invented armature.
    for side in (-1,1):
        off=Vector((side*r*.53,0,r*.69))
        tube('metasomal-carina-%02d-%s'%(i+1,side),[a+d*.18+off,a+d*.80+off],[.00065,.00065],3,6)
base=tail[-1]; direction=Vector((0,math.cos(math.radians(63)),math.sin(math.radians(63))))
ves=base+direction*.007
ellipsoid('telson-vesicle',tuple(ves),(.0054,.0068,.0064),1,14)
sting=[base+direction*.011,base+Vector((0,.0085,.014)),base+Vector((0,.012,.019)),base+Vector((0,.016,.0205))]
tube('telson-curved-aculeus',sting,[.0026,.0020,.0012,.00035],3,10)
# Contact center is a footprint pivot, while posed bounds are not total body length.
shift=ground_asset(COL,center_xy=False)
source=audit_source(COL,P['budgets']['max_triangles'])
if source['errors']: raise RuntimeError(json.dumps(source['errors']))
source['intended_parts']={'walking_legs':8,'pedipalps':2,'chelicerae':2,'dorsal_tergites':7,'metasomal_segments':5,'telsons':1}
source['ground_shift_m']=shift
source['centerline_estimates_m']={'carapace':.05,'mesosoma':.10,'metasoma_plus_telson':.14,'whole_excluding_legs_and_pedipalps':.29}
source['actual_metasoma_polyline_length_m']=sum((tail[i+1]-tail[i]).length for i in range(5))
source['claim']='Geometric assembly and source checks only; inferred soft thickness and articulated pose.'
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER' and space.params:
                space.params.directory=b'//'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
# Preserve separate semantic editing parts in saved source; consolidate only temporary export.
verts=[]; faces=[]; material_indices=[]
for ob in parts:
    offset=len(verts); verts.extend(tuple(ob.matrix_world@v.co) for v in ob.data.vertices)
    mi=M.index(ob.data.materials[0]); faces.extend(tuple(offset+i for i in p.vertices) for p in ob.data.polygons); material_indices.extend([mi]*len(ob.data.polygons))
for ob in list(parts): bpy.data.objects.remove(ob,do_unlink=True)
merged=mesh_object('pulmonoscorpius-export',verts,faces,M,COL)
for face,mi in zip(merged.data.polygons,material_indices): face.material_index=mi
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects: ob.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing: raise RuntimeError('Missing exporter fields: '+repr(missing))
bpy.ops.export_scene.gltf(filepath=str(OUT/'model.glb'),**options)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
b=source['bounds_blender_m']; low=[b['min'][0],b['min'][2],-b['max'][1]]; high=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-val[i]) for side,val in [('min',low),('max',high)] for i in range(3))
assert not glb['errors'],glb['errors']; assert delta<1e-6; assert glb['scene_triangles']==source['triangles']; assert glb['bytes']<=P['budgets']['max_glb_bytes']
# audit helper may report a caller path: public evidence uses the package-relative filename only.
glb['file']='model.glb'
save(OUT/'qa/evidence/source.json',source); save(OUT/'qa/evidence/glb-audit.json',glb)
save(OUT/'qa/evidence/build.json',{'blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'exporter_version':'4.3.47','export_options':options,'source_export_bounds_max_error_m':delta,'source_geometry_triangles':source['triangles'],'rendering':'Not part of generation; exact export is imported separately.','anatomy':source['intended_parts']})
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'])
