# SPDX-License-Identifier: MIT
"""Darwinius masillae, PMO 214.214 plate A: interpretive volumetric fossil study.
Not a CT reconstruction, not a complete bone inventory, and not a living animal.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
Only source/params.json and the hash-listed source/deps helpers are runtime inputs.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
from mathutils import Vector
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
a=argparse.ArgumentParser(); a.add_argument('--output',type=Path,required=True)
args=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene(P['asset_id'],P['seed']); scene=bpy.context.scene
scene.render.threads_mode='FIXED'; scene.render.threads=2
S=P['reference_xy_scale_m_per_unit']; O=P['reference_xy_origin']
M={k:make_material(k,v,roughness=0.92) for k,v in P['palette_srgb'].items()}
GROUPS={}; anatomy=[]
def xyz(p,z): return ((O[0]-p[0])*S,(p[1]-O[1])*S,z)
def add(name,vs,fs,mat='bone',note=None):
    g=GROUPS.setdefault(name,{'v':[],'f':[],'mat':mat}); i=len(g['v']); g['v']+=vs;g['f'] += [tuple(i+k for k in f) for f in fs]
    if note and note not in anatomy: anatomy.append(note)
def tube(name,points,radii,z=0.008,depth=0.7,mat='bone',sides=6):
    vs=[];fs=[]; zs=[z]*len(points) if isinstance(z,(int,float)) else z
    rs=[radii]*len(points) if isinstance(radii,(int,float)) else radii
    for i,p in enumerate(points):
        t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        if t.length==0: raise ValueError('Zero-length centerline')
        t.normalize(); n=Vector((-t.y,t.x))
        for k in range(sides):
            ang=2*math.pi*k/sides; r=rs[i]*S
            # Fossil relief rests in its reconstructed matrix, rather than floating.
            if name.startswith('cranial_') or name=='zygomatic_arch':
                zz=zs[i]+r*depth*math.sin(ang)
            else:
                vr=max(r*depth*(zs[i]/.008),.00045)
                min_sin=min(math.sin(2*math.pi*j/sides) for j in range(sides))
                zz=.00315-vr*min_sin+vr*math.sin(ang)
            vs.append(((O[0]-p[0])*S-n.x*r*math.cos(ang),(p[1]-O[1])*S+n.y*r*math.cos(ang),zz))
    for i in range(len(points)-1):
        for k in range(sides): fs.append((i*sides+k,i*sides+(k+1)%sides,(i+1)*sides+(k+1)%sides,(i+1)*sides+k))
    fs+=[tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+k for k in range(sides))]
    add(name,vs,fs,mat)
def bone(name,p,q,r=7,z=0.008,mat='bone',depth=0.7):
    p,q=Vector(p),Vector(q); d=q-p; n=Vector((-d.y,d.x)).normalized()
    ts=[0,.13,.51,.87,1]; rr=[.68,1.1,.58,1.07,.66]
    pts=[tuple(p+d*t+n*(math.sin(t*math.pi)*r*.18)) for t in ts]
    tube(name,pts,[r*v for v in rr],z,depth,mat)
def solid(name,poly,z0,z1,mat='bone',bevel=0.86):
    n=len(poly);c=sum((Vector(p) for p in poly),Vector((0,0)))/n
    if mat!='matrix': z0=.00315
    vs=[xyz(p,z0) for p in poly]+[xyz(c+(Vector(p)-c)*bevel,z1) for p in poly]
    fs=[tuple(range(n-1,-1,-1)),tuple(n+i for i in range(n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    add(name,vs,fs,mat)
def resample(poly,n):
    lengths=[0]
    for p,q in zip(poly,poly[1:]):lengths.append(lengths[-1]+(Vector(q)-Vector(p)).length)
    def at(t):
        value=t*lengths[-1]
        for j in range(1,len(lengths)):
            if value<=lengths[j]:return Vector(poly[j-1]).lerp(Vector(poly[j]),(value-lengths[j-1])/(lengths[j]-lengths[j-1]))
        return Vector(poly[-1])
    return at,lengths[-1]
# Minimal chipped matrix silhouette, a presentation reconstruction rather than slab geometry.
solid('matrix_support',P['matrix_outline'],0,0.0034,'matrix',.988)
# Cranial ring is a genuine closed solid with an open orbital fenestra, not a painted disk.
N=20
outer=[(335,124),(338,143),(325,161),(304,173),(280,175),(258,167),(237,157),(223,141),(215,126),(217,110),(223,95),(235,80),(248,68),(266,65),(284,69),(302,78),(315,90),(321,105),(326,112),(332,118)]
# Angular matching of an eccentric orbit to the non-circular crushed cranial margin.
# Low, irregular ridged relief replaces a uniformly filled or circular skull disk.
inner=[]
for p in outer:
    t=math.atan2(p[1]-110,p[0]-283)
    inner.append((283+22*math.cos(t),110+20*math.sin(t)))
heights=[.0083,.0072,.008,.009,.0078,.0087,.0103,.0097,.011,.0115,.0125,.0112,.012,.0106,.0118,.0128,.012,.010,.0095,.009]
vs=[xyz(p,.00315) for p in outer]+[xyz(p,heights[i]) for i,p in enumerate(outer)]+[xyz(p,.0097+.001*math.sin(i*1.8)) for i,p in enumerate(inner)]+[xyz(p,.00315) for p in inner];fs=[]
for i in range(N):
    j=(i+1)%N
    for a0,b0 in [(0,N),(N,2*N),(2*N,3*N),(3*N,0)]:fs.append((a0+i,a0+j,b0+j,b0+i))
add('cranium_with_orbit',vs,fs,'bone_high')
solid('maxillary_region',[(318,115),(345,126),(368,144),(378,158),(363,169),(335,170),(308,154)],.0048,.010,'bone')
bone('zygomatic_arch',(260,145),(337,162),5,.0112,'bone_high')
tube('mandible',[(243,153),(263,174),(296,185),(334,187),(365,174)],[5,7,7,5,3.3],.0072,.7,'bone_high')
bone('mandible',(244,151),(245,130),6,.0076,'bone_high')
for i in range(7):
    x=315+i*7; y=173-i*.6
    solid('preserved_toothline',[(x-2,y-3),(x+2,y-3),(x+1.7,y+3),(x-1.7,y+3)],.008,.0105,'mineral')
# Fragmented cranial ridges convey compression without replacing the diagnostic outline.
for i,(p,q,r) in enumerate([((229,104),(247,85),3.4),((229,131),(252,143),3.7),((252,73),(273,77),3),((300,82),(316,98),3),((323,137),(347,148),3.2),((259,157),(281,162),3)]):
    bone('cranial_preserved_ridges',p,q,r,.012 if i<4 else .010,'bone')
# Axial chain is a simplified observed-region rhythm, not a claim of complete vertebral counts.
spine=P['axial_path']; at,L=resample(spine,24)
for i in range(24):
    t=(i+.5)/24; p=at((i+.12)/24);q=at((i+.88)/24);r=7.5+3*math.sin(math.pi*t)
    bone('axial_preserved_blocks',p,q,r,.0079,'bone_high',.85)
    tangent=(q-p).normalized(); normal=Vector((-tangent.y,tangent.x)); mid=(p+q)/2
    for sg in (-1,1):
        pp=mid+normal*r*.6*sg; qq=mid+normal*(r+5.5)*sg+tangent*2
        bone('axial_process_fragments',pp,qq,3.5,.007,'bone')
# Deliberately asymmetric rib arcs derived from the visible crushed thoracic field.
for i in range(12):
    y=226+i*10.4;x=209-i*3.4; end=(278-i*1.65,276+i*8.3)
    pts=[(x,y),(x+23,y+7),(x+43,y+23),(end[0],end[1]-10),(end[0]-9,end[1])]
    tube('thoracic_visible_ribs',pts,[3.7,3.6,3.2,2.8,2.1],.0065+(i%3)*.0005,.75,'bone_high',6)
for i in range(7):
    y=251+i*13;x=191-i*3
    tube('thoracic_partial_far_ribs',[(x,y),(x-18,y+8),(x-20,y+20),(x-12,y+28)],[3.4,3.2,2.6,2.0],.0057,.65,'bone',6)
# Scapular and pelvic patches are bounded solid shape interpretations of compressed regions.
solid('scapular_fragments',[(220,207),(248,217),(257,256),(229,244),(212,222)],.0043,.0074,'bone')
bone('clavicular_remnants',(213,204),(261,218),4,.0086,'bone_high')
solid('pelvic_fragments',[(140,469),(164,479),(176,512),(171,555),(152,542),(138,506)],.0042,.008,'bone')
solid('pelvic_fragments',[(171,505),(191,514),(208,551),(200,583),(181,576),(171,549)],.0042,.009,'bone_high')
tube('pelvic_fragments',[(145,512),(136,531),(148,553),(175,559)],[6,5,5,4],.007,.75,'bone')
# Two folded forelimbs: major axes taken from plate A, not the restored counterpart B.
for row in P['long_bones']:
    if row.get('preservation')=='proximal_fragment_only':
        start,end=Vector(row['a']),Vector(row['b'])
        tube(row['name'],[start,start.lerp(end,.24),end],[row['radius'],row['radius']*.88,row['radius']*.64],row['z'],.72,row.get('material','bone_high'))
    else:
        bone(row['name'],row['a'],row['b'],row['radius'],row['z'],row.get('material','bone_high'),.72)
# Hands and feet use articulated digit chains with blunt termini. No curled claws.
for hand in P['digits']:
    for j,chain in enumerate(hand['chains']):
        for k,(p,q) in enumerate(zip(chain,chain[1:])):
            bone(hand['name'],p,q,hand['radius']*(1-.19*k),hand['z']+(j%2)*.00035,hand.get('material','bone_high'),.75)
# Wrist preservation includes a small irregular callus-like relief from Fig.9, not a repaired healthy joint.
for name,x,y,r,z in [('wrist_near',414,306,12,.008),('wrist_far',411,212,11,.008),('ankle_right',373,793,13,.008)]:
    poly=[(x+math.cos(k*math.pi/4)*r*(1+.13*math.sin(k*2)),y+math.sin(k*math.pi/4)*r*.8) for k in range(8)]
    solid(name,poly,.0042,z,'bone')
solid('wrist_near',[(402,300),(413,290),(423,302),(415,316),(405,314)],.007,.011,'bone_high')
# 31 visible caudal units are reported for the preserved specimen. Stop at a blunt fragment.
# Gaps and tapered proportions are interpretive; the unknown original terminal 1-2 are NOT added.
tail=P['tail_path']; at,tail_L=resample(tail,31)
for i in range(31):
    t=(i+.5)/31; p=at((i+.09)/31);q=at((i+.88)/31);r=8.5*(1-t)**1.23+1.7
    bone('tail_31_preserved_units',p,q,r,.0066-0.0014*t,'bone_high',.74)
    # Franzen et al. 2009: strong processes on Ca1-Ca3, reduced caudal-end Ca4,
    # and none on Ca5 onward. Do not repeat proximal anatomy down the tail.
    if i<4:
        tangent=(q-p).normalized();normal=Vector((-tangent.y,tangent.x));mid=(p+q)/2
        if i==3:
            mid=p.lerp(q,.82)
            for sg in (-1,1):bone('caudal_process_remnants',mid+normal*r*.68*sg,mid+normal*r*1.13*sg,1.2,.0059,'bone',.6)
        else:
            for sg in (-1,1):bone('caudal_process_remnants',mid+normal*r*.6*sg,mid+normal*(r+4.2*(1-t))*sg,2.1,.0059,'bone',.6)
# The final disconnected broken end does not invent a finished tapering tail tip.
end=at(1); tang=(at(1)-at(.98)).normalized()
bone('terminal_fault_fragment',end-tang*3,end,1.8,.0051,'bone',.7)
for name,g in GROUPS.items():
    ob=mesh_object(name,g['v'],g['f'],M[g['mat']],COL)
    ob['interpretation']='Closed low-poly relief volume; depth/backside reconstructed, XY placement from genuine plate A.'
root=bpy.data.objects['darwinius'];root['specimen']='PMO 214.214, plate A';root['representation']='compressed fossil skeleton study';root['unknown_tail_tip']='not reconstructed';root['not_a_complete_bone_inventory']=True
scene['factual_scope']='Juvenile Eocene adapiform primate. Compressed visible skeletal arrangement; not a living animal or tomography.'
source=audit_source(COL,max_triangles=P['budgets']['max_triangles'])
if source['errors']: raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in COL.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=root
opt=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
RNA={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opt)-RNA:raise RuntimeError('Unsupported export options')
bpy.ops.export_scene.gltf(**opt)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
b=source['bounds_blender_m'];lo=[b['min'][0],b['min'][2],-b['max'][1]];hi=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-target[i]) for side,target in [('min',lo),('max',hi)] for i in range(3))
if glb['errors'] or delta>1e-5 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('Export audit failed '+str(glb))
report={'status':'PASS','claim_scope':'Source/static GLB/axis roundtrip only; not independent visual, GPU, scene or release approval','blender_version':bpy.app.version_string,'seed':P['seed'],'source':source,'glb':glb,'roundtrip_bounds_max_error_m':delta,'export_options':{k:v for k,v in opt.items() if k!='filepath'},'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest(),'measured_tail_centerline_m':tail_L*S,'anatomy_scope':{'tail_preserved_display_units':31,'other_segment_counts':'Stylized visible-region rhythm, not inventory of anatomical bones','bone_depth_m':'Approximately 0.001-0.011 above matrix, reconstructed; not measured anatomy','unknown_terminal_tail':'Not supplied','plate_B':'Excluded'}}
(OUT/'build-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','triangles':glb['scene_triangles'],'primitives':glb['scene_primitives_estimated_base_draw_calls'],'glb_bytes':glb['bytes'],'sha256':glb['sha256']}))
