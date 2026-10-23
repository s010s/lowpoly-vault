# SPDX-License-Identifier: MIT
"""Original deterministic Pterodaustro whole-organism reconstruction.
Usage: blender -b -t 2 --python source/generate.py -- --out OUTPUT [--gray|--render]
All model-building imports are bundled in source/deps or in Blender 4.3.2.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse, shutil
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source, _look_at, _vertices_world, _bounds, srgb_to_linear
from qa_glb import audit_glb
P=json.loads((SOURCE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); ap.add_argument('--gray',action='store_true'); ap.add_argument('--render',action='store_true')
a=ap.parse_args(argv); OUT=Path(a.out).resolve(); OUT.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
collection=setup_scene('pterodaustro',seed=P['seed'])
root=bpy.data.objects['pterodaustro'];root['mounting_origin']='Airborne thorax center at (0,0,0), not floor contact.'
M={key:make_material(key,col,roughness=0.86) for key,col in P['palette'].items()}
class Part:
    def __init__(self,name,mats): self.name=name; self.mats=mats; self.v=[]; self.f=[]; self.mi=[]
    def add(self,v,f,mi=0):
        off=len(self.v);self.v.extend(tuple(x) for x in v);self.f.extend(tuple(off+i for i in face) for face in f);self.mi.extend([mi]*len(f))
    def make(self):
        obj=mesh_object(self.name,self.v,self.f,[M[m] for m in self.mats],collection)
        for p,i in zip(obj.data.polygons,self.mi):p.material_index=i
        return obj
# Explicit oval profiles. Longitudinal y/z path, cross-section axes X and local dorsal.
def loft(part, sections, sides=12, mi=0):
    v=[]; f=[]
    for j,(x,y,z,rx,rz) in enumerate(sections):
        prev=Vector(sections[max(j-1,0)][:3]); nex=Vector(sections[min(j+1,len(sections)-1)][:3]); t=(nex-prev).normalized()
        u=Vector((1,0,0)); w=t.cross(u).normalized()
        if w.z<0:w=-w
        for k in range(sides):
            th=2*math.pi*k/sides; v.append(Vector((x,y,z))+u*(rx*math.cos(th))+w*(rz*math.sin(th)))
    for j in range(len(sections)-1):
        for k in range(sides): f.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    f.extend([tuple(range(sides-1,-1,-1)),tuple((len(sections)-1)*sides+k for k in range(sides))]);part.add(v,f,mi)
# General tapered tubing, no zero-radius/degenerate end triangles.
def tube(part, pts, radii, sides=8, mi=0):
    v=[];f=[]
    for j,p in enumerate(pts):
        p=Vector(p);t=(Vector(pts[min(j+1,len(pts)-1)])-Vector(pts[max(0,j-1)])).normalized()
        ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((1,0,0));u=t.cross(ref).normalized();w=t.cross(u).normalized()
        rr=radii[j];rx,ry=(rr,rr) if isinstance(rr,(int,float)) else rr
        for k in range(sides):
            th=2*math.pi*k/sides;v.append(p+u*(rx*math.cos(th))+w*(ry*math.sin(th)))
    for j in range(len(pts)-1):
        for k in range(sides): f.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
    f.extend([tuple(range(sides-1,-1,-1)),tuple((len(pts)-1)*sides+k for k in range(sides))]);part.add(v,f,mi)
body=Part('Torso_Neck_ShortTail',['skin','bill'])
loft(body,[(0,.245,-.016,.010,.013),(0,.20,-.004,.038,.035),(0,.13,.003,.056,.053),(0,.035,.009,.071,.068),(0,-.055,.018,.072,.068),(0,-.12,.035,.055,.049),(0,-.16,.058,.036,.033),(0,-.205,.088,.026,.027),(0,-.25,.112,.022,.025),(0,-.29,.125,.024,.027),(0,-.32,.127,.026,.027)],14)
# A distinct slightly raised breast patch, deliberately overlapping dorsal body skin.
loft(body,[(0,.14,-.035,.021,.009),(0,.07,-.049,.046,.017),(0,-.015,-.049,.052,.019),(0,-.085,-.028,.047,.016),(0,-.12,-.002,.025,.009)],10,1)
loft(body,[(0,.224,-.005,.019,.016),(0,.268,-.007,.010,.011),(0,.299,-.002,.0016,.0025)],8)
head=Part('Slender_Cranium',['skin','bill'])
loft(head,[(0,-.288,.133,.013,.019),(0,-.315,.145,.031,.032),(0,-.345,.151,.041,.040),(0,-.382,.147,.037,.034),(0,-.415,.137,.029,.024),(0,-.438,.134,.022,.018)],14)
# Bill coordinates are artistic adult composite, not enlargement of MIC-V241 juvenile.
def bill(t): return (-.421-.392*t, .117+.004*t+.121*t*t)
def width(t):return .022*(1-.83*t)
jaws=Part('Recurved_Upper_And_Lower_Jaws',['bill'])
lower=[]; upper=[]
for k in range(17):
    t=k/16;y,z=bill(t);w=width(t)
    lower.append((0,y,z,w,.0078*(1-.68*t)))
    # Open narrow filter slot between long jaws; upper jaw follows the same upward curve.
    gap=.029*(math.sin(math.pi*(.12+.88*t))**.7)+.007*(1-t)
    upper.append((0,y,z+gap,w*.96,.009*(1-.72*t)))
loft(jaws,lower,8);loft(jaws,upper,8)
# Two arrays of fine lower-jaw bristles. 40 per side, deliberately reduced from fossil tooth count.
teeth=Part('Lower_Jaw_Filter_Comb_40_Per_Side',['filter_ivory'])
for sign in [-1,1]:
    for i in range(P['tooth_segments_per_side']):
        t=.09+.85*i/(P['tooth_segments_per_side']-1);y,z=bill(t);w=width(t)
        gap=.029*(math.sin(math.pi*(.12+.88*t))**.7)+.007*(1-t)
        h=max(.007,gap-.007)
        x=sign*w*.86
        tube(teeth,[(x,y,z+.003),(x+sign*.0007,y-.002,z+.003+h*.52),(x+sign*.0003,y-.003,z+.003+h)], [.00085,.00066,.00038],5)
# Wing membrane: closed two-sided shell with physically thin thickness, not alpha sheets.
wing=Part('Paired_Continuous_Wing_Membranes',['membrane','edge'])
rows=[(.044,-.137,.165,.017),(.115,-.150,.265,.015),(.175,-.158,.350,.002),(.245,-.166,.321,.006),(.35,-.176,.300,.021),(.48,-.173,.280,.042),(.60,-.190,.215,.054),(.76,-.200,.150,.068),(.94,-.180,.040,.084),(1.09,-.130,-.040,.100),(1.2,-.0708,-.0692,.111)]
nc=6; nr=len(rows)
for sign in [-1,1]:
    v=[];f=[];mis=[]
    for surface in [1,-1]:
        for i,(x,yl,yt,z) in enumerate(rows):
            for j in range(nc+1):
                u=j/nc;y=yl*(1-u)+yt*u;camber=.025*(1-x/1.3)*math.sin(math.pi*u)
                # Inboard membrane falls naturally to the hind-limb ankle.
                drop=-.052*math.exp(-((x-.17)/.12)**2)*u**2
                thickness=.0018*(.35+.65*math.sin(math.pi*u))
                v.append((sign*x,y,z+camber+drop+surface*thickness))
    layer=nr*(nc+1)
    for surf in range(2):
        for i in range(nr-1):
            for j in range(nc):
                A=surf*layer+i*(nc+1)+j;B=A+1;D=A+(nc+1);C=D+1
                # alternate diagonals for controlled broad facets
                tris=[(A,B,D),(B,C,D)] if (i+j)%2 else [(A,B,C),(A,C,D)]
                f.extend(tris);mis.extend([1 if j==0 else 0]*2)
    # perimeter stitch. Thin edge is opaque and outward-facing after normal recalculation.
    boundary=list(range(nc+1))+[i*(nc+1)+nc for i in range(1,nr)]+[(nr-1)*(nc+1)+j for j in range(nc-1,-1,-1)]+[i*(nc+1) for i in range(nr-2,0,-1)]
    for k,A in enumerate(boundary):B=boundary[(k+1)%len(boundary)];f.append((A,B,B+layer,A+layer));mis.append(1)
    off=len(wing.v);wing.v.extend(v);wing.f.extend(tuple(off+k for k in face) for face in f);wing.mi.extend(mis)
# Wing-leading structural path: one elongated digit IV per wing, not bat-like multiple spars.
arms=Part('Forelimbs_And_Single_Wing_Digits',['skin'])
limbs=Part('Hindlimbs_And_Four_Toed_Feet',['skin'])
claws=Part('Small_Manual_And_Pedal_Claws',['dark'])
for sign in [-1,1]:
    mirror=lambda pts:[(sign*x,y,z) for x,y,z in pts]
    tube(arms,mirror([(.055,-.087,.032),(.14,-.035,.04),(.235,.008,.036),(.35,-.070,.049),(.48,-.160,.055)]),[.021,.018,.015,.012,.011],9)
    tube(arms,mirror([(.48,-.160,.055),(.60,-.190,.062),(.76,-.200,.076),(.94,-.180,.089),(1.09,-.130,.104),(1.199,-.070,.112)]),[.010,.009,.0072,.0058,.0036,.0008],8)
    # Three short free fingers at the wrist, each with a very small hooked claw.
    for k in range(3):
        x=.472+(k-1)*.015;y=-.163;end=(x+.012*(k-1),y-.045-.009*(1-abs(k-1)),.05)
        mid=(x+.005*(k-1),y-.027,.060)
        tube(arms,mirror([(x,y,.057),mid,end]),[.0038,.0032,.0018],6)
        tube(claws,mirror([end,(end[0],end[1]-.006,.046),(end[0],end[1]-.004,.041)]),[.002,.0015,.00045],5)
    leg=[(.044,.13,-.022),(.11,.20,-.051),(.155,.292,-.052),(.177,.351,-.051)]
    tube(limbs,mirror(leg),[.020,.014,.0085,.0065],8)
    # Four main pedal digits: splayed and rear-directed in this gliding pose.
    for k in range(4):
        x=.174+(k-1.5)*.008;length=[.037,.051,.055,.045][k]
        y=.35; mid=(x+(k-1.5)*.006,y+length*.58,-.058);end=(x+(k-1.5)*.011,y+length,-.064)
        tube(limbs,mirror([(x,y,-.051),mid,end]),[.0038,.003,.0018],6)
        tube(claws,mirror([end,(end[0],end[1]+.006,-.067),(end[0],end[1]+.007,-.071)]),[.002,.0013,.00045],5)
# No long tail vane: only a small inferred inter-femoral membrane behind the pelvis.
wing.add([(-.05,.17,-.015),(.05,.17,-.015),(.12,.24,-.05),(0,.273,-.013),(-.12,.24,-.05),(-.05,.17,-.018),(.05,.17,-.018),(.12,.24,-.053),(0,.273,-.016),(-.12,.24,-.053)],[(0,1,3),(1,2,3),(0,3,4),(5,8,6),(6,8,7),(5,9,8),(0,5,6,1),(1,6,7,2),(2,7,8,3),(3,8,9,4),(4,9,5,0)],0)
eyes=Part('Paired_Eyes_And_Nostrils',['dark'])
# Latitudinal lens meshes sit proud of the skull; smooth only the tiny eyes deliberately.
for sign in [-1,1]:
    center=(sign*.037,-.362,.164)
    # Short axial spindle from skull into shallow eye lens.
    tube(eyes,[(sign*.033,-.362,.164),(sign*.0396,-.362,.164),(sign*.041,-.362,.164)],[(.009,.009),(.0085,.0085),(.0045,.0045)],12)
    tube(eyes,[(sign*.026,-.415,.144),(sign*.028,-.415,.144)],[(.0027,.0038),(.0024,.0032)],8)
parts=[body,head,jaws,teeth,wing,arms,limbs,claws,eyes]
for part in parts:
    obj=part.make()
    if part is eyes:
        for face in obj.data.polygons:face.use_smooth=True
# Geometry metadata for independent feature measurements.
source=audit_source(collection,max_triangles=6500)
if source['errors']:raise RuntimeError(str(source['errors']))
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(options)-{p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if missing:raise RuntimeError('Unsupported exporter options '+str(missing))
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in collection.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
bpy.ops.export_scene.gltf(**options)
glb=audit_glb(OUT/'model.glb',6500,6,12)
if glb['errors']:raise RuntimeError(str(glb['errors']))
b=source['bounds_blender_m']; expected_min=[b['min'][0],b['min'][2],-b['max'][1]];expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
assert delta<.0001 and glb['scene_triangles']==source['triangles']
# Canonical geometry/material semantics independent of .blend timestamp or container bytes.
semantic=[]
for obj in sorted([o for o in collection.all_objects if o.type=='MESH'],key=lambda o:o.name):
    obj.data.calc_loop_triangles();semantic.append({'name':obj.name,'vertices':[[round(float(x),8) for x in v.co] for v in obj.data.vertices],'triangles':[list(t.vertices) for t in obj.data.loop_triangles],'materials':[m.name for m in obj.data.materials],'material_indices':[p.material_index for p in obj.data.polygons]})
materials={k:{'srgb':v,'roughness':.86,'metallic':0} for k,v in P['palette'].items()}
digest=hashlib.sha256(json.dumps({'geometry':semantic,'materials':materials},sort_keys=True,separators=(',',':')).encode()).hexdigest()
write(OUT/'qa/evidence/geometry.json',{'asset_id':'pterodaustro','revision':'r001','glb_sha256':sha(OUT/'model.glb'),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'normalized_geometry_material_digest':digest,'feature_checks':{'wingspan_m':glb['bounds_m']['size'][0],'lower_filter_bristles_per_side':P['tooth_segments_per_side'],'main_toes_per_hindfoot':4,'long_wing_digits_per_side':1,'short_free_manual_digits_per_side':3,'tail_centerline_length_m':.075,'bill_foreaft_extent_m':.392,'bill_tip_upturn_m':.125,'adult_composite_proportions':True,'mouth_filter_slot_m':'variable approximately 0.008–0.034'},'intentional_assemblies':['Closed skin parts overlap at anatomical joins; no claim of one watertight union.','Wing shells close their perimeter and join body and hindlimb anchor; membrane is opaque, not transparent double-sided artwork.','Only the tiny eye/nostril mesh uses smooth shading.','Root is airborne thorax mount; negative Z is intentional, not ground-contact error.']})
write(OUT/'qa/evidence/build.json',{'blender_version':bpy.app.version_string,'exporter':list(__import__('io_scene_gltf2').bl_info['version']) if hasattr(__import__('io_scene_gltf2'),'bl_info') else 'Blender bundled','seed':P['seed'],'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_parts':[p.name for p in parts],'glb_sha256':sha(OUT/'model.glb'),'blend_sha256':sha(OUT/'model.blend'),'normalized_geometry_material_digest':digest,'license':'CC-BY-4.0','author':'Leon Made This / s010s','origin':'Airborne thorax mounting point (0,0,0)','palette':materials})
if a.gray or a.render:
    # Rendering begins from a factory scene and ONLY the emitted delivered GLB.
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
    imported=list(bpy.context.scene.objects);collection=bpy.data.collections.new('IMPORTED_EXACT_GLB');bpy.context.scene.collection.children.link(collection)
    for obj in imported:
        for old in list(obj.users_collection):old.objects.unlink(obj)
        collection.objects.link(obj)
    from render_views import render
    render(collection,OUT,sha(OUT/'model.glb'),gray=a.gray,resolution=P['render']['gray_resolution'] if a.gray else P['render']['resolution'],samples=P['render']['gray_samples'] if a.gray else P['render']['samples'])
print('BUILD_COMPLETE',str(OUT),glb['scene_triangles'],sha(OUT/'model.glb'),flush=True)
