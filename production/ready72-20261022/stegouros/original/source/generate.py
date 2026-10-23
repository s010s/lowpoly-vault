# SPDX-License-Identifier: MIT
"""Original deterministic Stegouros living reconstruction. Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir PATH
Only declared source/deps, adjacent params.json, Blender and Python stdlib are used.
"""
from pathlib import Path
import sys,json,math,hashlib,argparse
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'params.json').read_text())
parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',required=True)
a=parser.parse_args(sys.argv[sys.argv.index('--')+1:]); OUT=Path(a.output_dir).resolve(); OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene('stegouros',seed=P['seed'])
M=[make_material(n,c) for n,c in P['palette'].items()]
class Group:
    def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[];self.parts=[]
    def add(self,name,v,f,mi=0):
        off=len(self.v);self.v.extend(v);self.f.extend([tuple(i+off for i in face) for face in f]);self.mi.extend(mi if isinstance(mi,list) else [mi]*len(f));self.parts.append((name,off,len(self.v)))
    def finish(self):
        o=mesh_object(self.name,self.v,self.f,self.mats,C)
        for poly,idx in zip(o.data.polygons,self.mi):poly.material_index=idx
        for name,first,last in self.parts:o.vertex_groups.new(name=name).add(list(range(first,last)),1,'REPLACE')
        o['semantic_parts']=json.dumps([p[0] for p in self.parts]);return o
skin=Group('skin_torso_head_neck',[M[0],M[1],M[2]])
limbs=Group('four_limbs_and_feet',[M[0],M[1]])
armour=Group('low_osteoderms_and_pelvic_shield',[M[3]])
weapon=Group('tail_seven_pairs_distal_five_fused',[M[3]])
horn=Group('beak_and_short_toe_tips',[M[4]])
dark=Group('eyes_nostrils_mouth',[M[5]])

def loft(group,name,rings,n=16,mi=0,region=False):
    # y, center_z, half_width_x, half_depth_z; deliberately shaped closed ring loft.
    v=[];f=[];ids=[]
    for y,z,rx,rz in rings:
        for j in range(n):
            t=2*math.pi*j/n;v.append((rx*math.cos(t),y,z+rz*math.sin(t)))
    for k in range(len(rings)-1):
        for j in range(n):
            f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
            mid=math.sin(2*math.pi*(j+.5)/n)
            ids.append((2 if mid<-.45 else 1 if mid<.3 else 0) if region else mi)
    f.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))]);ids.extend([mi,mi]);group.add(name,v,f,ids)

def tube(group,name,points,radii,n=8,mi=0):
    v=[];f=[]
    for i,p in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        axis=tangent.normalized();u=axis.cross(Vector((0,1,0)))
        if u.length<.1:u=axis.cross(Vector((1,0,0)))
        u.normalize();w=axis.cross(u).normalized()
        rx,ry=radii[i] if isinstance(radii[i],(tuple,list)) else (radii[i],radii[i])
        for j in range(n):v.append(tuple(Vector(p)+u*(rx*math.cos(2*math.pi*j/n))+w*(ry*math.sin(2*math.pi*j/n))))
    for i in range(len(points)-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]);group.add(name,v,f,mi)

def ellipsoid(group,name,center,scale,n=10,r=5,mi=0):
    v=[(center[0],center[1],center[2]-scale[2])];f=[]
    for k in range(1,r):
        ph=-math.pi/2+math.pi*k/r
        for j in range(n):
            t=2*math.pi*j/n;v.append((center[0]+scale[0]*math.cos(ph)*math.cos(t),center[1]+scale[1]*math.cos(ph)*math.sin(t),center[2]+scale[2]*math.sin(ph)))
    v.append((center[0],center[1],center[2]+scale[2]));top=len(v)-1
    for j in range(n):f.append((0,1+(j+1)%n,1+j));f.append((top,1+(r-2)*n+j,1+(r-2)*n+(j+1)%n))
    for k in range(r-2):
        for j in range(n):f.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
    group.add(name,v,f,mi)

def scute(group,name,x,y,z,wx,ly,h,mi=0):
    # Surface-following osteoderm: all skirt vertices seat slightly within the skin.
    # Osteoderm positions are an artistic reconstruction, not preserved articulated rows.
    if y>-.45:
        rings=[(-.48,.402,.065,.090),(-.40,.414,.145,.158),(-.26,.430,.197,.193),(-.08,.439,.218,.205),(.10,.446,.220,.210),(.27,.440,.181,.197),(.37,.400,.118,.142),(.425,.352,.062,.086)];n=18
    elif y<-.53:
        rings=[(-.766,.356,.041,.040),(-.735,.361,.073,.062),(-.678,.376,.104,.079),(-.615,.387,.113,.086),(-.555,.387,.086,.075),(-.515,.387,.061,.060)];n=14
    else:
        rings=[(-.605,.387,.063,.067),(-.54,.389,.087,.084),(-.46,.399,.092,.100),(-.365,.418,.135,.132)];n=14
    def interp(yy):
        yy=max(rings[0][0],min(rings[-1][0],yy))
        for a,b in zip(rings,rings[1:]):
            if a[0]<=yy<=b[0]:
                t=(yy-a[0])/(b[0]-a[0]);return tuple(a[k]*(1-t)+b[k]*t for k in (1,2,3))
        return rings[-1][1:]
    _,rx,_=interp(y);theta=math.acos(max(-.98,min(.98,x/rx)))
    def surface(u,v,raise_h=0):
        yy=y+v*ly;zc,rx,rz=interp(yy);th=theta-u*wx/rx
        # Piecewise angular interpolation follows the actual flat-shaded loft shell.
        segment=th*n/(2*math.pi);j=math.floor(segment);t=segment-j
        cx=(1-t)*math.cos(j*2*math.pi/n)+t*math.cos((j+1)*2*math.pi/n)
        sz=(1-t)*math.sin(j*2*math.pi/n)+t*math.sin((j+1)*2*math.pi/n)
        return (rx*cx+math.cos(th)*raise_h,yy,zc+rz*sz-.003+math.sin(th)*raise_h)
    outline=[(-.80,-.55),(-.45,-1),(.45,-.94),(.92,-.28),(.85,.65),(0,1),(-.86,.60)]
    v=[surface(u,w) for u,w in outline]+[surface(0,-.30,h),surface(0,.45,h*.75)]
    f=[tuple(reversed(range(7))),(0,1,7),(1,2,7),(2,3,7),(3,8,7),(3,4,8),(4,5,8),(5,6,8),(6,0,7,8)]
    group.add(name,v,f,mi)

# Main forms: small, deep-bellied quadruped; the shoulder remains lower than hip.
loft(skin,'torso',[
(-.48,.402,.065,.090),(-.40,.414,.145,.158),(-.26,.430,.197,.193),(-.08,.439,.218,.205),(.10,.446,.220,.210),(.27,.440,.181,.197),(.37,.400,.118,.142),(.425,.352,.062,.086)],n=18,region=True)
loft(skin,'short_neck',[(-.605,.387,.063,.067),(-.54,.389,.087,.084),(-.46,.399,.092,.100),(-.365,.418,.135,.132)],n=14,region=True)
loft(skin,'rounded_beaked_head',[(-.766,.356,.041,.040),(-.735,.361,.073,.062),(-.678,.376,.104,.079),(-.615,.387,.113,.086),(-.555,.387,.086,.075),(-.515,.387,.061,.060)],n=14,region=True)
loft(horn,'cropped_prehensile_beak',[(-.780,.350,.031,.022),(-.764,.352,.054,.038),(-.742,.351,.065,.042)],n=10)
# Tail muscular stalk is separate from its pale low blade; terminal length 1.9 m.
loft(skin,'tail_stalk',[ (.31,.340,.108,.095),(.43,.319,.072,.066),(.53,.300,.052,.048),(.63,.287,.036,.034),(.73,.282,.028,.026),(.82,.278,.026,.021)],n=12,mi=0)
# Slim limbs, with real negative space under torso. Four planted feet.
for s,label in [(-1,'left'),(1,'right')]:
    tube(limbs,label+'_forelimb',[(s*.134,-.325,.432),(s*.180,-.330,.345),(s*.217,-.248,.214),(s*.211,-.304,.092),(s*.221,-.318,.043)],[(.058,.068),(.048,.055),(.034,.039),(.027,.029),(.032,.032)],n=10)
    tube(limbs,label+'_hindlimb',[(s*.127,.228,.453),(s*.190,.170,.340),(s*.225,.185,.231),(s*.201,.299,.114),(s*.220,.275,.045)],[(.079,.091),(.069,.070),(.047,.047),(.029,.033),(.036,.033)],n=10)
    for fore,y in [(True,-.344),(False,.252)]:
        lab=label+('_front' if fore else '_rear')
        # Low sole ring on z=0 guarantees intentional ground contacts.
        cx=s*.221
        v=[];f=[]
        for zz,rx,ry in [(0,.046,.067),(.022,.051,.069),(.050,.034,.041)]:
            for j in range(10):v.append((cx+rx*math.cos(2*math.pi*j/10),y+ry*math.sin(2*math.pi*j/10),zz))
        for k in range(2):
            for j in range(10):f.append((k*10+j,k*10+(j+1)%10,(k+1)*10+(j+1)%10,(k+1)*10+j))
        f.extend([tuple(reversed(range(10))),tuple(20+j for j in range(10))]);limbs.add(lab+'_foot',v,f,1)
        for d in range(4):
            x=cx+(d-1.5)*.020; yf=y-.054 +abs(d-1.5)*.003
            tube(horn,lab+'_toe'+str(d+1),[(x,yf,.017),(x,yf-.025,.010)],[(.010,.013),(.005,.005)],n=6)
    # Small lateral eye set inside a sculpted brow, not a mammalian ear.
    ellipsoid(dark,label+'_eye',(s*.106,-.636,.409),(.007,.012,.011),n=10,r=5)
    scute(armour,label+'_brow',s*.086,-.636,.438,.035,.041,.012)
    ellipsoid(dark,label+'_nostril',(s*.057,-.742,.376),(.004,.006,.004),n=8,r=4)
    tube(dark,label+'_mouth_line',[(s*.062,-.752,.334),(s*.082,-.704,.331),(s*.090,-.659,.337)],[(.002,.002)]*3,n=5)
# The source paper's dorsal osteoderm positions are speculative. This deliberately
# sparse artistic pattern is not a claim of an articulated complete dorsal armour.
for i,(y,wx,top) in enumerate([(-.345,.112,.569),(-.19,.139,.614),(-.015,.147,.631),(.155,.134,.628),(.285,.106,.590)]):
    for s,lab in [(-1,'L'),(1,'R')]:scute(armour,f'dorsal_{i+1}_{lab}',s*wx*.65,y,top,.050,.067,.025 if i<3 else .019)
for s,lab in [(-1,'L'),(1,'R')]:
    for i,(y,x,z) in enumerate([(-.30,.172,.506),(-.13,.198,.529),(.05,.199,.538),(.225,.165,.522)]):
        scute(armour,f'flank_{i+1}_{lab}',s*x,y,z,.039,.054,.014)
    scute(armour,'pelvic_shield_'+lab,s*.053,.277,.616,.065,.092,.013)
    scute(armour,'neck_low_scute_'+lab,s*.051,-.492,.483,.032,.038,.011)
# Proximal two pairs are separate ossicles around the skin stalk.
for k,(y,outer,span) in enumerate([(.674,.092,.030),(.746,.105,.032)],1):
    for s,lab in [(-1,'L'),(1,'R')]:
        # Pentagonal, laterally broad, dorsoventrally flattened flanges.
        ol=[(.024,y-span),(.059,y-span*1.04),(outer,y-.007),(outer*.87,y+span*.74),(.022,y+span)]
        ol=[(s*x,yy) for x,yy in ol]
        v=[(x,yy,.273) for x,yy in ol]+[(s*.055,y,.303)]
        f=[tuple(reversed(range(5)))]+[(j,(j+1)%5,5) for j in range(5)]
        weapon.add(f'pair_{k}_{lab}_independent',v,f)
# One closed continuous lens with five lobed pairs, central ridge and lateral valleys.
# Width extrema are the visible paired units 3..7; edges are blunt plates, not spikes.
profile=[(.779,.037),(.793,.076),(.816,.113),(.840,.097),(.865,.123),(.893,.100),(.927,.112),(.955,.086),(.987,.087),(1.014,.060),(1.054,.054),(1.083,.029),(1.120,.008)]
v=[];f=[]
for i,(y,w) in enumerate(profile):
    z=.276 +.008*((y-.779)/.341)
    h=.023*(.75+.25*w/.123)
    # Four upper and four lower nodes, source normals recomputed outward.
    v.extend([(0,y,z+h),(w*.55,y,z+h*.70),(w,y,z),(w*.55,y,z-h*.65),(0,y,z-h*.85),(-w*.55,y,z-h*.65),(-w,y,z),(-w*.55,y,z+h*.70)])
for i in range(len(profile)-1):
    for j in range(8):f.append((i*8+j,i*8+(j+1)%8,(i+1)*8+(j+1)%8,(i+1)*8+j))
f.extend([tuple(reversed(range(8))),tuple((len(profile)-1)*8+j for j in range(8))]);weapon.add('pairs_3_to_7_fused_frond',v,f)
objs=[g.finish() for g in (skin,limbs,armour,weapon,horn,dark)]
# Recenter the identity root on the actual floor-contact footprint, not the whole tail bbox.
contacts=[v.co.copy() for o in objs for v in o.data.vertices if abs(v.co.z)<1e-7]
contact_center=[(min(p[i] for p in contacts)+max(p[i] for p in contacts))/2 for i in (0,1)]
for o in objs:
    for vertex in o.data.vertices:
        vertex.co.x-=contact_center[0];vertex.co.y-=contact_center[1]
# semantic annotations are useful editing context, not assertions of exact soft tissue.
weapon_obj=objs[3];weapon_obj['lateral_pair_count']=7;weapon_obj['independent_proximal_pairs']=2;weapon_obj['fused_distal_pairs']=5
weapon_obj['basis']='CPAP-3165 Fig1p and Fig2 CT, original mesh not extracted CT'
bpy.context.scene['anatomical_uncertainty']='Dorsal armour arrangement, skull soft tissue and palette artistic; not exact complete fossil.'
bpy.context.scene['generator_seed']=P['seed'];bpy.context.preferences.filepaths.save_version=0
source=audit_source(C,6500)
if source['errors']:raise RuntimeError(source['errors'])
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available:raise RuntimeError('Missing exporter options: '+str(set(opts)-available))
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(OUT/'model.glb',6500,6,12)
b=source['bounds_blender_m'];expected_min=[b['min'][0],b['min'][2],-b['max'][1]];expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
if glb['errors'] or delta>1e-5 or glb['scene_triangles']!=source['triangles'] or glb['bytes']>2000000:raise RuntimeError('Export QA failure '+repr(glb['errors']))
meta={'asset_id':'stegouros','revision':'r001','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'parameters_sha256':hashlib.sha256((ROOT/'params.json').read_bytes()).hexdigest(),'source_generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'total_length_m':1.9,'foot_contact_z_m':0,'origin_footprint_offset_before_recentering_xy_m':contact_center,'origin':'Identity transform at center of actual foot contact extent','style':'Faceted palette-only reconstruction, no texture, closed constituent meshes with intentional anatomical overlaps','source_scene_has_camera_or_light':any(o.type in ('CAMERA','LIGHT') for o in bpy.data.objects),'claim_scope':'Maker technical checks only; independent visual/factual and GPU/scene gates separate.'}
(OUT/'build-report.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({'status':'BUILT','glb':glb['sha256'],'triangles':glb['scene_triangles'],'primitive_count':glb.get('scene_primitives'),'size':glb['bounds_m'],'errors':glb['errors']}))
