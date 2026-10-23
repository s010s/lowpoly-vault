#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Macropoma lewesiensis reconstruction, meters.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
The source blend preserves anatomical objects. Export joins a temporary in-memory
copy after saving source, to retain six material primitives without losing editability.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
P=json.loads((Path(__file__).parent/'params.json').read_text())
a=argparse.ArgumentParser(); a.add_argument('--out',type=Path,required=True)
a=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
a.out.mkdir(parents=True,exist_ok=True)
C=setup_scene('macropoma',P['seed']); ROOT=bpy.data.objects[C['asset_root']]
ROOT['authoring_forward']='-X'; ROOT['mount']='Midline swimming mounting point at trunk center; no floor contact.'
M=[make_material(n,c,roughness=r) for n,c,r in [('Dorsal slate','#3C5456',.82),('Flank sage','#657874',.83),('Ventral pearl olive','#9B9D87',.88),('Fin membrane','#66776D',.88),('Fin ray ochre','#9B9A77',.79),('Eye and incision','#222E2B',.46)]]
PARTS=[]
def obj(name,v,f,mat=1,indices=None):
    ob=mesh_object(name,v,f,M if indices is not None else M[mat],C)
    if indices is not None:
        for po,mi in zip(ob.data.polygons,indices): po.material_index=mi
    PARTS.append(ob); return ob

def tube(name,pts,radii,mat=4,n=6):
    pts=[Vector(x) for x in pts]; v=[]; f=[]
    for i,p in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
        ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0))
        u=tangent.cross(ref).normalized(); w=tangent.cross(u).normalized()
        for j in range(n): v.append(p+radii[i]*(u*math.cos(j*math.tau/n)+w*math.sin(j*math.tau/n)))
    f.append(tuple(range(n-1,-1,-1)))
    for i in range(len(pts)-1):
        for j in range(n): f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.append(tuple((len(pts)-1)*n+j for j in range(n)))
    return obj(name,v,f,mat)

# The short cranial profile and deep opercular/trunk block are deliberately lofted.
# x, half-width, dorsal height, ventral height; all longitudinal scale is 0.600 m.
R=[(-.300,.008,.000,-.018),(-.292,.021,.009,-.030),(-.279,.031,.026,-.038),(-.259,.036,.040,-.043),(-.237,.040,.049,-.049),(-.213,.044,.057,-.057),(-.184,.047,.067,-.067),(-.150,.0475,.075,-.075),(-.115,.047,.075,-.075),(-.075,.0445,.072,-.072),(-.030,.041,.068,-.067),(.015,.0365,.062,-.060),(.060,.031,.054,-.051),(.100,.025,.043,-.040),(.135,.019,.030,-.029),(.170,.013,.020,-.020),(.205,.009,.013,-.013),(.240,.005,.008,-.008),(.274,.0024,.0045,-.0045),(.291,.0008,.002,-.002)]
N=32

def section(x):
    for j in range(len(R)-1):
        if R[j][0]<=x<=R[j+1][0]:
            t=(x-R[j][0])/(R[j+1][0]-R[j][0]);return [R[j][k]*(1-t)+R[j+1][k]*t for k in range(1,4)]
    raise ValueError(x)
def surf(x,t,raise_=0):
    w,up,lo=section(x);s=math.sin(t);c=math.cos(t)
    return Vector((x,(w+raise_)*c,((up if s>=0 else -lo)+raise_)*s))
V=[];F=[];MI=[]
for x,w,up,lo in R:
    for j in range(N):
        t=j*math.tau/N; s=math.sin(t); V.append((x,w*math.cos(t),(up if s>=0 else -lo)*s))
F.append(tuple(range(N-1,-1,-1)));MI.append(1)
for i in range(len(R)-1):
    for j in range(N):
        F.append((i*N+j,(i+1)*N+j,(i+1)*N+(j+1)%N,i*N+(j+1)%N))
        s=math.sin((j+.5)*math.tau/N);MI.append(0 if s>.55 else 2 if s<-.52 else 1)
F.append(tuple((len(R)-1)*N+j for j in range(N)));MI.append(1)
body=obj('01_Profile_loft_head_operculum_trunk_axial_tail',V,F,indices=MI)

# Very shallow imbricated scale relief. Closed lenticular tiles, no spikes.
sv=[];sf=[];sm=[]
for row in range(20):
    x=-.139+row*.016
    for j in range(24):
        t=(j+.5*(row%2))*math.tau/24
        if abs(math.sin(t))>.985: continue
        outline=[surf(x-.008,t,.00015),surf(x,t-.116,.00015),surf(x+.0088,t,.00015),surf(x,t+.116,.00015)]
        center=surf(x+.0018,t,.00075);bottom=surf(x,t,-.00025)
        k=len(sv);sv+=outline+[center,bottom]
        mi=0 if math.sin(t)>.55 else 2 if math.sin(t)<-.52 else 1
        for z in range(4): sf.extend([(k+z,k+(z+1)%4,k+4),(k+(z+1)%4,k+z,k+5)]);sm.extend([mi,mi])
obj('02_Subtle_imbricate_scale_relief',sv,sf,indices=sm)

# Skin-following seams: y is solved on the local elliptical cross-section.
def sidepoint(x,z,sign,bias=.0007):
    w,up,lo=section(x);h=up if z>=0 else -lo
    return (x,sign*(w*math.sqrt(max(0,1-(z/h)**2))+bias),z)

# Closed shallow opercular bosses and incisions, restoring skin rather than bone holes.
for sign,side in [(-1,'near'),(1,'far')]:
    pts=[sidepoint(x,z,sign) for x,z in [(-.196,.051),(-.178,.038),(-.166,.012),(-.162,-.019),(-.175,-.048)]]
    tube('03_Opercular_edge_'+side,pts,[.0014]*5,5,6)
    # Small closed mouth, with jawline terminating ahead of large operculum.
    pts=[sidepoint(x,z,sign) for x,z in [(-.298,-.012),(-.282,-.024),(-.257,-.026),(-.231,-.024),(-.213,-.020)]]
    tube('04_Closed_mouth_incised_seam_'+side,pts,[.0010,.0013,.0014,.0012,.0008],5,6)
    tube('05_Submandibular_ridge_'+side,[sidepoint(x,z,sign,.0003) for x,z in [(-.291,-.030),(-.270,-.037),(-.244,-.042),(-.218,-.041)]],[.0018,.0020,.0022,.0011],2,6)
    # Lenticular eye with convex pupil embedded in head, not oversized protruding globe.
    cx,cy,cz=sidepoint(-.254,.021,sign,.0004)
    def lens(name,r,depth,mat,cy0):
        v=[(cx,cy0+sign*depth,cz)];n=16
        for j in range(n):
            t=j*math.tau/n; v.append((cx+r*math.cos(t),cy0,cz+r*math.sin(t)))
        v.append((cx,cy0-sign*.001,cz));f=[]
        for j in range(n): f.extend([(0,j+1,(j+1)%n+1),(n+1,(j+1)%n+1,j+1)])
        obj(name,v,f,mat)
    lens('06_Eye_rim_'+side,.0081,.002,4,cy)
    lens('07_Eye_'+side,.0059,.0027,5,cy+sign*.0013)
    # Modest nares, no external reconstruction of skeletal fenestrae.
    tube('08_Naris_'+side,[sidepoint(-.285,.005,sign,.0002),sidepoint(-.282,.007,sign,.0002)],[.0012,.0012],5,6)

# Fin webs are thin closed solid surfaces. Radiating ribs are structural geometry.
def fin(name,base,edge,normal,ray_count=None,radius=.0010):
    base=Vector(base);edge=[Vector(p) for p in edge];normal=Vector(normal).normalized(); n=len(edge)
    # A band of attachment vertices gives fin rays separate origins, avoiding star-like convergence.
    V=[];F=[]
    for offset in [-.000175,.000175]:
        V.append(base+normal*offset)
        for p in edge: V.append(p+normal*offset)
    stride=n+1
    for i in range(n-1):
        F.extend([(0,i+1,i+2),(stride,stride+i+2,stride+i+1)])
    perimeter=[0]+list(range(1,n+1))
    for i,k in enumerate(perimeter):
        l=perimeter[(i+1)%len(perimeter)];F.append((k,l,stride+l,stride+k))
    obj(name+'_web',V,F,3)
    for i,p in enumerate(edge):
        origin=base.lerp(edge[0],.16*(1-i/max(1,n-1)))
        tip=base.lerp(p,.98)
        mid=origin.lerp(tip,.55)
        tube(name+'_ray_%02d'%(i+1),[origin,mid,tip],[radius,radius*.78,radius*.48],4,5)

# Unlobed first dorsal: EXACTLY eight primary rays, no fleshy stalk/base lobe.
d1base=(-.092,0,.070)
d1edge=[(-.132,0,.128),(-.119,0,.138),(-.103,0,.139),(-.087,0,.133),(-.070,0,.122),(-.054,0,.107),(-.038,0,.091),(-.026,0,.075)]
fin('09_First_dorsal_unlobed_8_primary_rays',d1base,d1edge,(0,1,0),8,.00125)
# Lobe bearing posterior median fins: distinct fleshy bases, unlike dorsal 1.
tube('10_Second_dorsal_fleshy_base',[(.058,0,.048),(.067,0,.061),(.079,0,.073)],[.013,.015,.011],1,10)
d2edge=[(.066,0,.109),(.078,0,.119),(.091,0,.125),(.106,0,.123),(.120,0,.116),(.132,0,.105),(.139,0,.094),(.141,0,.084)]
fin('11_Second_dorsal_fan',(.076,0,.068),d2edge,(0,1,0),radius=.0009)
tube('12_Anal_fleshy_base',[(.084,0,-.043),(.094,0,-.056),(.105,0,-.067)],[.012,.013,.009],2,10)
anal=[(.099,0,-.095),(.110,0,-.104),(.122,0,-.105),(.134,0,-.100),(.144,0,-.090),(.148,0,-.081),(.147,0,-.073)]
fin('13_Anal_fan',(.104,0,-.063),anal,(0,1,0),radius=.0008)

# Paired fleshy fins gently splayed. No fin becomes a leg or narrow stick.
for sign,side in [(-1,'near'),(1,'far')]:
    base=Vector((-.162,sign*.037,-.032));lobe=Vector((-.142,sign*.065,-.048))
    tube('14_Pectoral_lobe_'+side,[base,base.lerp(lobe,.52),lobe],[.013,.014,.009],1,10)
    edge=[(-.146,sign*.096,-.058),(-.138,sign*.105,-.061),(-.125,sign*.112,-.066),(-.111,sign*.112,-.069),(-.098,sign*.105,-.069),(-.090,sign*.094,-.064),(-.089,sign*.083,-.058),(-.095,sign*.073,-.053)]
    fin('15_Pectoral_fan_'+side,lobe,edge,(.25,sign*.4,-.85),radius=.00085)
    pb=Vector((-.018,sign*.026,-.053));pl=Vector((.004,sign*.042,-.075))
    tube('16_Pelvic_lobe_'+side,[pb,pb.lerp(pl,.55),pl],[.011,.011,.0065],2,10)
    edge=[(-.002,sign*.059,-.098),(.010,sign*.065,-.108),(.022,sign*.069,-.111),(.034,sign*.070,-.108),(.046,sign*.066,-.100),(.053,sign*.058,-.089),(.052,sign*.050,-.081)]
    fin('17_Pelvic_fan_'+side,pl,edge,(.1,sign*.8,-.5),radius=.00075)

# Nearly balanced caudal halves. The central continuation is only 5 mm beyond edge.
for sign,side in [(1,'upper'),(-1,'lower')]:
    caud=[(.171,0,sign*.038),(.188,0,sign*.060),(.208,0,sign*.076),(.229,0,sign*.084),(.248,0,sign*.082),(.266,0,sign*.071),(.279,0,sign*.055),(.288,0,sign*.036),(.295,0,sign*.017),(.295,0,sign*.004)]
    fin('18_Caudal_'+side,(.159,0,sign*.004),caud,(0,1,0),radius=.00085)
fin('19_Very_short_central_axial_tip',(.266,0,0),[(.296,0,.006),(.300,0,0),(.296,0,-.006)],(0,1,0),radius=.00055)

# Record semantic construction and validate source before export-only joining.
ROOT['taxon']='Macropoma lewesiensis (Mantell, 1822)'
ROOT['reconstruction']='Original conservative living restoration from NHM photograph and Woodward 1909 Fig.49. Width, color and fin pose inferred.'
ROOT['first_dorsal_primary_rays']=8
ROOT['length_m']=.6
ROOT['source_part_names']=json.dumps([o.name for o in PARTS])
source=audit_source(C,max_triangles=40000)
if source['errors']: save(a.out/'source-failure.json',source); raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.context.scene['artifact_profile']='palette-only static, no external assets'
bpy.context.scene['author']='Leon Made This / s010s'
bpy.ops.wm.save_as_mainfile(filepath=str(a.out/'model.blend'))
# Consolidate temporary export state only; saved source stays anatomically editable.
bpy.ops.object.select_all(action='DESELECT')
for o in PARTS: o.select_set(True)
bpy.context.view_layer.objects.active=body
bpy.ops.object.join();body.name='Macropoma_export_surface'
# Remove duplicate material slots introduced by semantic object join.
unique=[];mapping={}
for i,mat in enumerate(body.data.materials):
    if mat not in unique: unique.append(mat)
    mapping[i]=unique.index(mat)
indices=[mapping[p.material_index] for p in body.data.polygons]
body.data.materials.clear()
for mat in unique: body.data.materials.append(mat)
for p,i in zip(body.data.polygons,indices):p.material_index=i
ROOT.select_set(True)
options=dict(filepath=str(a.out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-available: raise RuntimeError('Unsupported exporter flags: '+str(set(options)-available))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(a.out/'model.glb',max_triangles=40000,max_materials=6,max_primitives=8)
if glb['errors']: raise RuntimeError(glb['errors'])
b=source['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][q][i]-vals[i]) for q,vals in [('min',lo),('max',hi)] for i in range(3))
assert delta<.0001 and glb['scene_triangles']==source['triangles'] and glb['bytes']<8000000
save(a.out/'build.json',{'asset_id':'macropoma','revision':'r001','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(Path(__file__).parent/'params.json'),'seed':P['seed'],'export_options':{k:v for k,v in options.items() if k!='filepath'},'semantic_parts':len(PARTS),'palette':[{ 'name':m.name,'srgb':m['palette_srgb']} for m in M],'notes':['All authored surfaces are closed. Anatomical parts intentionally overlap. Not a boolean printable union.','Swimming mount origin, negative minimum Z expected.','Six portable opaque palette materials, no textures.','Source contains editable named anatomical pieces; GLB merges them only for draw calls.','Body depth 0.150 m excludes submillimeter scale relief. Species representative length, not an individual photo measurement.']})
print('BUILD_OK',glb['sha256'],glb['scene_triangles'],glb['bytes'])
