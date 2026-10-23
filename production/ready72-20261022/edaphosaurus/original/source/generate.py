# SPDX-License-Identifier: MIT
"""Original Edaphosaurus boanerges whole-animal reconstruction, revision r001.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUT
All geometry is authored in metres, X lateral / -Y forward / Z up.
Museum descriptions and skeleton inform form, not copied mesh or photo texture.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
argsv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,required=True); ap.add_argument('--clay',action='store_true')
args=ap.parse_args(argsv); OUT=args.output_dir.resolve(); OUT.mkdir(parents=True,exist_ok=True)
(OUT/'qa'/'evidence').mkdir(parents=True,exist_ok=True)
col=setup_scene('edaphosaurus',seed=P['seed'])
scene=bpy.context.scene; scene.render.threads_mode='FIXED'; scene.render.threads=2
mats={k:make_material(k, '#959187' if args.clay else v, roughness=.87) for k,v in P['palette_hex'].items()}
class Part:
    def __init__(self,name,matkeys): self.name=name; self.matkeys=matkeys; self.v=[]; self.f=[]; self.mi=[]
    def add(self,verts,faces,mi=0):
        n=len(self.v); self.v.extend(verts); self.f.extend([tuple(n+i for i in face) for face in faces]); self.mi.extend(mi if isinstance(mi,list) else [mi]*len(faces))
    def finish(self):
        obj=mesh_object(self.name,self.v,self.f,[mats[m] for m in self.matkeys],col)
        for p,i in zip(obj.data.polygons,self.mi): p.material_index=i
        obj['anatomy']=self.name; obj['surface_style']='deliberate flat profile lofts'
        return obj

def tube(part,coords,radii,sides=10,mat=0,flatten=1.0):
    """Closed tapered path loft. Radii are transverse, depth optionally flattened."""
    vv=[]; ff=[]; pts=[Vector(p) for p in coords]
    for i,p in enumerate(pts):
        tangent=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        axis=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((1,0,0))
        u=tangent.cross(axis).normalized(); w=tangent.cross(u).normalized()
        for k in range(sides):
            a=2*math.pi*k/sides
            vv.append(tuple(p+radii[i]*(math.cos(a)*u+flatten*math.sin(a)*w)))
    for i in range(len(pts)-1):
        for k in range(sides): ff.append((i*sides+k,i*sides+(k+1)%sides,(i+1)*sides+(k+1)%sides,(i+1)*sides+k))
    ff.extend([tuple(reversed(range(sides))),tuple((len(pts)-1)*sides+k for k in range(sides))]); part.add(vv,ff,mat)

def ellipsoid(part,center,scale,mat=0,sides=10,rings=5):
    x,y,z=center; rx,ry,rz=scale; vv=[(x,y,z+rz)]; ff=[]
    for j in range(1,rings):
        p=math.pi*j/rings
        for k in range(sides):
            a=2*math.pi*k/sides; vv.append((x+rx*math.sin(p)*math.cos(a),y+ry*math.sin(p)*math.sin(a),z+rz*math.cos(p)))
    bottom=len(vv); vv.append((x,y,z-rz))
    for k in range(sides): ff.append((0,1+k,1+(k+1)%sides))
    for j in range(rings-2):
        a=1+j*sides; b=a+sides
        for k in range(sides):ff.append((a+k,b+k,b+(k+1)%sides,a+(k+1)%sides))
    a=1+(rings-2)*sides
    for k in range(sides):ff.append((a+k,bottom,a+(k+1)%sides))
    part.add(vv,ff,mat)

# One uninterrupted skin loft: tiny blunt head, short neck, deep barrel and tapered tail.
axial=Part('axial-head-neck-barrel-tail',['body','belly'])
vv=[]; ff=[]; mm=[]; n=P['radial_segments']; profiles=P['axial_profiles']
for y,cx,cz,rx,rz in profiles:
    for k in range(n):
        a=2*math.pi*k/n; vv.append((cx+rx*math.cos(a),y,cz+rz*math.sin(a)))
for j in range(len(profiles)-1):
    for k in range(n):
        ff.append((j*n+k,(j+1)*n+k,(j+1)*n+(k+1)%n,j*n+(k+1)%n))
        # Restrained lower-flank/belly tone; no randomly scattered faces.
        mm.append(1 if math.sin(2*math.pi*(k+.5)/n)<-.48 else 0)
ff.extend([tuple(reversed(range(n))),tuple((len(profiles)-1)*n+k for k in range(n))]);mm.extend([0,0])
axial.add(vv,ff,mm); axial.finish()

# Closed continuous skin sail. Crossbar knobs are relief sculpted into both
# surfaces, not exposed bones or freestanding antler-like projections.
sail=Part('continuous-sail-with-transverse-bosses',['sail','rib'])
sp=P['sail_spines']; heights=P['sail_levels']; stations=[]
for j,p in enumerate(sp):
    stations.append((*p,True))
    if j<len(sp)-1: stations.append((*(.5*(p[k]+sp[j+1][k]) for k in range(3)),False))
nj=len(stations); nk=len(heights); vv=[];ff=[];mm=[]
for side in (-1,1):
    for j,(y,base,top,rib) in enumerate(stations):
        for k,f in enumerate(heights):
            taper=math.sin(math.pi*f)**.35
            thick=.007+.008*taper
            if rib and 1<j<nj-2:
                thick+=.006*taper
                if f in (.28,.52,.74): thick+=P['boss_relief_m']*(1-.22*f)
            # Broad root blends into trunk, narrow but closed dorsal edge.
            if f==0: thick=.038
            if f==1: thick=.0055
            vv.append((side*thick,y,base+f*(top-base)))
for side in range(2):
    offset=side*nj*nk
    for j in range(nj-1):
        for k in range(nk-1):
            a=offset+j*nk+k;b=a+nk
            ff.extend([(a,b,b+1),(a,b+1,a+1)])
            mm.extend([1 if j%2==0 else 0]*2)
# Close entire perimeter without internal duplicate side faces.
for j in range(nj-1):
    for k in (0,nk-1):
        a=j*nk+k;b=(j+1)*nk+k; ff.append((a,b,nj*nk+b,nj*nk+a));mm.append(0)
for j in (0,nj-1):
    for k in range(nk-1):
        a=j*nk+k;ff.append((a,a+1,nj*nk+a+1,nj*nk+a));mm.append(0)
sail.add(vv,ff,mm); sail.finish()

claws=Part('twenty-small-digit-tips',['claw'])
# Four stocky articulated limbs, with a palm and five splayed toe lofts each.
for side in (-1,1):
    for hind in (False,True):
        label=('left' if side<0 else 'right')+('-hindlimb' if hind else '-forelimb')
        leg=Part(label,['body'])
        if hind:
            path=[(.19,.37,.46),(.29,.36,.36),(.39,.31,.24),(.435,.40,.14),(.445,.455,.072)]
            radii=[.103,.105,.080,.054,.043]; palm_y=.445
        else:
            path=[(.18,-.43,.47),(.29,-.43,.36),(.38,-.405,.25),(.43,-.50,.14),(.445,-.565,.072)]
            radii=[.090,.088,.070,.049,.041]; palm_y=-.575
        tube(leg,[(side*x,y,z) for x,y,z in path],radii,12)
        ellipsoid(leg,(side*.445,palm_y,.047),(.068,.073,.045),sides=12,rings=5)
        for digit in range(5):
            d=digit-2; reach=.132-.023*abs(d); startx=.445+.023*d; endx=.445+.048*d
            starty=palm_y-.029; endy=palm_y-reach
            p=[(side*startx,starty,.041),(side*(startx*.4+endx*.6),starty-.046,.033),(side*endx,endy,.021),(side*(endx+.005*d),endy-.019,.014)]
            tube(leg,p,[.018,.016,.012,.007],8,flatten=.78)
            tip=(side*(endx+.008*d),endy-.043,.009)
            tube(claws,[p[-2],p[-1],tip],[.011,.008,.0018],7,flatten=.63)
        leg.finish()
claws.finish()
# Eyes and closed mouth line are small in scale, with no predatory canines.
dark=Part('eyes-nostrils-closed-mouth',['dark'])
for side in (-1,1):
    ellipsoid(dark,(side*.084,-.858,.535),(.016,.018,.017),sides=10,rings=5)
    ellipsoid(dark,(side*.050,-.963,.496),(.007,.009,.005),sides=8,rings=4)
    tube(dark,[(side*.051,-.986,.451),(side*.075,-.950,.445),(side*.085,-.895,.450),(side*.076,-.810,.462)],[.0025,.0032,.0031,.0018],6)
dark.finish()
# Move all mesh vertices up uniformly to exact lowest digital contact.
low=min(v.co.z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
for o in col.objects:
    if o.type=='MESH':
        for v in o.data.vertices:v.co.z-=low
bpy.context.view_layer.update()
root=bpy.data.objects[col['asset_root']];root['reconstruction_uncertainty']='Soft tissues, sail outline, colours and exact dimensions are artistic. Crossbar soft-tissue cover is uncertain.'
root['scale_basis']='2.5m artistic genus-range target, not measured specimen';root['taxon']='Edaphosaurus boanerges'
source=audit_source(col,max_triangles=P['budgets']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
volumes={}
for o in col.objects:
    if o.type=='MESH':
        bm=bmesh.new();bm.from_mesh(o.data);volumes[o.name]=bm.calc_volume(signed=True);bm.free()
        if volumes[o.name]<=0: raise RuntimeError('Nonpositive signed volume '+o.name)
scene['asset_license']='CC-BY-4.0';scene['asset_author']='Leon Made This / s010s';scene['generator']='source/generate.py'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
 export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
 export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
 export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
avail={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(options)-avail:raise RuntimeError('Missing exporter options '+repr(set(options)-avail))
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',P['budgets']['max_triangles'],P['budgets']['max_materials'],P['budgets']['max_primitives'])
if glb['errors']:raise RuntimeError(glb['errors'])
if glb['bytes']>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB exceeds frozen byte budget')
b=source['bounds_blender_m'];expect={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(expect[s][i]-glb['bounds_m'][s][i]) for s in expect for i in range(3))
if delta>1e-4 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/GLB mismatch')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record={'status':'PASS','claim_scope':'source/GLB baseline geometry only; not independent visual, factual, GPU, scene or publication acceptance',
'asset_id':'edaphosaurus','revision':'r001','glb_sha256':digest(OUT/'model.glb'),'blend_sha256':digest(OUT/'model.blend'),
'generator_sha256':digest(Path(__file__)),'params_sha256':digest(HERE/'params.json'),'blender_version':bpy.app.version_string,'seed':P['seed'],
'consumer_three_version':'0.180.0','source':source,'glb':glb,'source_export_bounds_error_m':delta,'signed_component_volumes_m3':volumes,
'export_options':{k:v for k,v in options.items() if k!='filepath'},'intentional_intersections':['Limb roots into body','Toe lofts into closed palms','Eyes and mouth relief partially embedded in head','Continuous sail root embedded into back','Claw tips into toe ends'],
'geometry_limits':P['budgets'],'closed_parts':True,'four_feet_with_five_digits_each':True,'clay':args.clay,
'source_scene_nonexport_objects': [o.name for o in scene.objects if o not in set(col.all_objects)]}
(OUT/'qa'/'evidence'/'geometry.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'BUILD_PASS','triangles':glb['scene_triangles'],'glb_sha256':record['glb_sha256'],'bytes':glb['bytes']}))
