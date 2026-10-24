# SPDX-License-Identifier: MIT
"""Original deterministic adult Stegoceras validum living reconstruction.
Blender 4.3.2: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir output
Dependencies are adjacent params.json and the declared local deps/ only.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
sys.path.insert(0, str(Path(__file__).resolve().parent/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
SRC=Path(__file__).resolve().parent
P=json.loads((SRC/'params.json').read_text())
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);OUT=a.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
C=setup_scene(P['asset_id'],seed=P['seed'])
M=[make_material(k,v,roughness=.86 if k!='dark' else .6) for k,v in P['palette'].items()]
class Group:
    def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[];self.parts=[]
    def add(self,name,v,f,mi=0):
        off=len(self.v);self.v.extend(v);self.f.extend(tuple(i+off for i in face) for face in f);self.mi.extend(mi if isinstance(mi,list) else [mi]*len(f));self.parts.append((name,off,len(self.v)))
    def finish(self):
        o=mesh_object(self.name,self.v,self.f,self.mats,C)
        for poly,index in zip(o.data.polygons,self.mi):poly.material_index=index
        for name,start,end in self.parts:o.vertex_groups.new(name=name).add(list(range(start,end)),1,'REPLACE')
        o['semantic_parts']=json.dumps([n for n,_,_ in self.parts]);return o
skin=Group('body_neck_head_and_long_tail',[M[0],M[1],M[2]])
limbs=Group('paired_hindlimbs_short_arms',[M[1],M[2]])
roof=Group('adult_rounded_dome_flat_rear_shelf',[M[3]])
keratin=Group('short_beak_blunt_digit_tips',[M[4]])
dark=Group('eyes_nostrils_closed_mouth',[M[5]])

def loft(g,name,rings,n=16,mi=0,regions=False):
    v=[];f=[];ids=[]
    for y,z,rx,rz in rings:
        for j in range(n):
            t=2*math.pi*j/n;v.append((rx*math.cos(t),y,z+rz*math.sin(t)))
    for i in range(len(rings)-1):
        for j in range(n):
            f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
            t=math.sin(2*math.pi*(j+.5)/n);ids.append((0 if t>.35 else 2 if t<-.55 else 1) if regions else mi)
    f.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))]);ids.extend([mi,mi]);g.add(name,v,f,ids)

def tube(g,name,points,radii,n=10,mi=0):
    v=[];f=[]
    for i,pt in enumerate(points):
        t=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])).normalized()
        ref=Vector((1,0,0)) if abs(t.x)<.85 else Vector((0,1,0));u=(ref-t*ref.dot(t)).normalized();w=t.cross(u).normalized()
        rx,rz=radii[i] if isinstance(radii[i],(list,tuple)) else (radii[i],radii[i])
        for j in range(n):
            z=2*math.pi*j/n;v.append(tuple(Vector(pt)+u*(rx*math.cos(z))+w*(rz*math.sin(z))))
    for i in range(len(points)-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]);g.add(name,v,f,mi)

def ellipsoid(g,name,c,r,n=12,rings=6,mi=0):
    v=[(c[0],c[1],c[2]-r[2])];f=[]
    for k in range(1,rings):
        ph=-math.pi/2+math.pi*k/rings
        for j in range(n):
            t=2*math.pi*j/n;v.append((c[0]+r[0]*math.cos(ph)*math.cos(t),c[1]+r[1]*math.cos(ph)*math.sin(t),c[2]+r[2]*math.sin(ph)))
    top=len(v);v.append((c[0],c[1],c[2]+r[2]))
    for j in range(n):f.extend([(0,1+(j+1)%n,1+j),(top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n)])
    for k in range(rings-2):
        for j in range(n):f.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
    g.add(name,v,f,mi)

# Broad torso and pelvis, inferred soft tissue over partial UALVP2 postcrania.
loft(skin,'broad_barrel_torso',[(-.350,.645,.055,.075),(-.282,.636,.106,.138),(-.170,.630,.159,.174),(-.025,.634,.187,.188),(.110,.649,.185,.184),(.218,.664,.153,.154),(.306,.672,.110,.112),(.365,.669,.071,.081)],regions=True)
# Smoothly declining, relatively stiff balance tail. No club, plates or exposed tendons.
loft(skin,'long_tapered_tail',[(.245,.662,.129,.135),(.370,.660,.103,.102),(.510,.650,.078,.074),(.680,.637,.055,.051),(.855,.623,.036,.032),(1.020,.613,.021,.019),(1.170,.609,.010,.009),(1.314,.610,.0015,.002)],n=14,regions=True)
# Short broad neck with high cranial attachment, not the giraffe-like vertical neck.
tube(skin,'short_curved_neck',[(0,-.280,.679),(0,-.365,.701),(0,-.425,.756),(0,-.449,.802)],[(.085,.091),(.071,.080),(.056,.066),(.051,.060)],n=14,mi=1)
# Wedge-shaped face: relatively narrow beak, roomy cheeks, short posterior skull.
loft(skin,'cranial_face_and_cheeks',[(-.666,.807,.027,.025),(-.636,.815,.042,.037),(-.598,.829,.055,.052),(-.551,.841,.070,.059),(-.501,.846,.077,.063),(-.453,.844,.067,.054),(-.421,.829,.043,.034)],n=14,regions=True)
loft(skin,'lower_jaw',[(-.657,.786,.025,.012),(-.615,.778,.041,.016),(-.564,.777,.053,.020),(-.511,.785,.057,.022),(-.468,.802,.045,.020)],n=12,mi=2)
loft(keratin,'upper_short_beak',[(-.686,.801,.019,.015),(-.673,.807,.032,.025),(-.649,.808,.035,.026)],n=10)
loft(keratin,'lower_short_beak',[(-.681,.784,.016,.007),(-.661,.784,.028,.011),(-.641,.784,.030,.012)],n=10)
# A single continuous sagittal-profile cranial roof carries the low adult dome
# and an explicitly lower, broad, nearly horizontal posterior shelf.
# This is original living-reconstruction geometry, not a trace or scan of the photograph.
roof_rings=[(-.616,.854,.031,.011),(-.588,.879,.048,.024),(-.563,.893,.060,.032),(-.535,.905,.067,.043),(-.505,.908,.069,.042),(-.477,.900,.068,.037),(-.453,.884,.065,.021),(-.436,.878,.065,.011),(-.408,.876,.071,.011),(-.378,.875,.076,.011),(-.365,.874,.063,.010)]
loft(roof,'continuous_dome_to_flat_posterior_shelf',roof_rings,n=16)
# Small rounded posterior marginal nodes, not long Stygimoloch spikes.
for s,l in [(-1,'left'),(1,'right')]:
    for i,(x,y,z,r) in enumerate([(.058,-.385,.878,.009),(.043,-.367,.878,.009),(.020,-.362,.878,.007)]):
        ellipsoid(roof,l+'_small_rear_shelf_node_'+str(i+1),(s*x,y,z),(r,r*.75,r*.65),n=8,rings=4)
    # Eye is seated just under the dome margin; tiny brow is integrated skin.
    ellipsoid(skin,l+'_orbit_brow',(s*.071,-.523,.858),(.010,.024,.018),n=12,rings=5,mi=0)
    ellipsoid(dark,l+'_eye',(s*.078,-.527,.854),(.006,.013,.011),n=12,rings=5)
    ellipsoid(dark,l+'_nostril',(s*.032,-.653,.820),(.0027,.0048,.0032),n=8,rings=4)
    tube(dark,l+'_closed_mouth_line',[(s*.030,-.659,.790),(s*.044,-.618,.792),(s*.054,-.575,.795),(s*.061,-.541,.802)],[.0015,.0016,.0017,.0013],n=5)
    # Neutral supported biped. Femur slopes forward, shin returns to ankle.
    tube(limbs,l+'_continuous_hindlimb',[(s*.123,.177,.634),(s*.177,.116,.543),(s*.181,-.030,.389),(s*.180,.070,.262),(s*.158,.167,.151),(s*.160,.134,.094),(s*.165,.063,.038)],[(.086,.096),(.079,.089),(.045,.051),(.034,.037),(.024,.028),(.021,.023),(.025,.026)],n=12)
    # Three clearly separated main toes. Sole points are deliberately at Z=0.
    for d in range(3):
        x=s*(.165+(d-1)*.033);y=-.114-(.028 if d==1 else 0)
        tube(limbs,l+'_foot_digit_'+str(d+2),[(s*.165,.065,.034),(x,.000,.020),(x+s*(d-1)*.012,y,.014)],[(.016,.017),(.013,.020),(.008,.013)],n=8)
        tube(keratin,l+'_short_toe_tip_'+str(d+2),[(x+s*(d-1)*.012,y,.013),(x+s*(d-1)*.013,y-.023,.007),(x+s*(d-1)*.013,y-.029,.004)],[(.009,.011),(.005,.006),(.001,.002)],n=7)
    tube(limbs,l+'_small_hallux',[(s*.148,.104,.065),(s*.125,.134,.047),(s*.118,.151,.040)],[.008,.006,.002],n=7)
    # Arms shorter than hindlimbs; palms in sagittal planes facing inward.
    tube(limbs,l+'_upper_arm',[(s*.094,-.255,.661),(s*.125,-.295,.582),(s*.136,-.288,.516)],[(.033,.040),(.028,.032),(.020,.024)],n=10)
    tube(limbs,l+'_forearm',[(s*.136,-.288,.517),(s*.145,-.337,.490),(s*.152,-.389,.477)],[(.021,.023),(.016,.018),(.014,.015)],n=8)
    tube(limbs,l+'_inward_palm',[(s*.152,-.385,.479),(s*.157,-.405,.454),(s*.157,-.420,.433)],[(.015,.014),(.018,.016),(.014,.012)],n=8)
    for d in range(5):
        y=-.433+d*.010;z=.439-abs(d-2)*.004;length=[.025,.037,.042,.034,.023][d]
        tube(limbs,l+'_hand_digit_'+str(d+1),[(s*.158,y,z),(s*.160,y-.007,z-length*.7),(s*.151,y-.013,z-length)],[(.0055,.005),(.004,.004),(.002,.002)],n=6)
# Keep the soft-tissue head in the small-skull proportion of the 212 mm UALVP2
# skull within the 2 m adult estimate. This envelope is not a measured skull mesh.
for group in (skin,roof,keratin,dark):
    for name,start,end in group.parts:
        head_part=(group in (roof,dark) or name in ('cranial_face_and_cheeks','lower_jaw','upper_short_beak','lower_short_beak') or name.endswith('_orbit_brow'))
        if head_part:
            for i in range(start,end):
                x,y,z=group.v[i];group.v[i]=(x*.75,-.425+(y+.425)*.75,.830+(z-.830)*.75)
objs=[g.finish() for g in (skin,limbs,roof,keratin,dark)]
# Author at real-world estimate. Whole envelope scale is an artistic proxy, not a
# claim that UALVP2 soft tissue was preserved or its body measured directly.
pts=[v.co for o in objs for v in o.data.vertices];minz=min(v.z for v in pts)
length=max(v.y for v in pts)-min(v.y for v in pts);scale=P['total_length_target_m']/length
for o in objs:
    for v in o.data.vertices:v.co*=scale;v.co.z-=minz*scale
# The support footprint is bilateral toes, not the long-tail bounding-box center.
contact=[v.co.copy() for o in objs for v in o.data.vertices if v.co.z<.004]
ox=(min(v.x for v in contact)+max(v.x for v in contact))/2;oy=(min(v.y for v in contact)+max(v.y for v in contact))/2
for o in objs:
    for v in o.data.vertices:v.co.x-=ox;v.co.y-=oy
bpy.context.scene['anatomical_basis']='UALVP2 original skull photograph; C. Brown skeletal restoration; partial postcranial anatomy, not whole articulated preserved skeleton.'
bpy.context.scene['scientific_limits']='Adult estimated 2 m. Dome comparatively low but not flat juvenile. Soft tissues, colours and neutral supported pose inferred. No head-butting behavioural claim.'
bpy.context.scene['generator_seed']=P['seed'];bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
bpy.context.preferences.filepaths.save_version=0
# Clear factory UI directory strings before saving an original public source.
bpy.context.scene.render.filepath='//'
for screen in bpy.data.screens:
    for area in screen.areas:
        for space in area.spaces:
            if space.type=='FILE_BROWSER':
                if space.params:space.params.directory=b'//'
                if getattr(space,'browse_mode',None)=='ASSETS' and getattr(space,'params',None):
                    try:space.params.directory=b'//'
                    except Exception:pass
source=audit_source(C,P['geometry_policy']['max_triangles'])
if source['errors']:raise RuntimeError(source['errors'])
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[C['asset_root']]
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available:raise RuntimeError('Missing exporter options '+str(set(opts)-available))
bpy.ops.export_scene.gltf(**opts)
g=audit_glb(OUT/'model.glb',**{k:P['geometry_policy'][k] for k in ('max_triangles','max_materials','max_primitives')});g['file']='model.glb'
b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(g['bounds_m'][side][i]-e[i]) for side,e in [('min',emin),('max',emax)] for i in range(3))
if g['errors'] or delta>1e-5 or g['scene_triangles']!=source['triangles'] or g['bytes']>P['geometry_policy']['max_glb_bytes']:raise RuntimeError('Export failure: '+str(g['errors']))
meta={'asset_id':P['asset_id'],'revision':P['revision'],'source':source,'glb':g,'bounds_roundtrip_max_error_m':delta,'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'parameters_sha256':hashlib.sha256((SRC/'params.json').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'total_length_m':P['total_length_target_m'],'scale_is_estimate':True,'origin':'Identity transform centered on support footprint, floor Z=0','footprint_recentering_xy_m':[ox,oy],'source_scene_has_camera_or_light':any(o.type in ('CAMERA','LIGHT') for o in bpy.data.objects),'style':'Faceted palette-only closed constituent meshes; intentional anatomical overlaps, not printable union','claim_scope':'Maker source/export technical checks; not independent review or runtime GPU approval.'}
(OUT/'build-report.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({'status':'BUILT','glb_sha256':g['sha256'],'triangles':g['scene_triangles'],'primitives':g.get('scene_primitives'),'glb_bytes':g['bytes']}))
