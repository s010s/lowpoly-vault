# SPDX-License-Identifier: MIT
"""Original deterministic Regaliceratops living reconstruction; Blender 4.3.2.
Usage: blender -b -t 2 --python source/generate.py -- --out DIR [--gray|--render]
All Python build dependencies are adjacent in deps/. No reference image is read.
"""
import sys, json, math, argparse, hashlib, shutil
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy, bmesh
from mathutils import Vector
import asset_common as ac
from qa_glb import audit_glb, read_glb, semantic_digest
P=json.loads((Path(__file__).parent/'params.json').read_text())
args=argparse.ArgumentParser();args.add_argument('--out',required=True);args.add_argument('--gray',action='store_true');args.add_argument('--render',action='store_true');a=args.parse_args(sys.argv[sys.argv.index('--')+1:])
OUT=Path(a.out).resolve();OUT.mkdir(parents=True,exist_ok=True);(OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
COL=ac.setup_scene('regaliceratops',seed=405)
M=[ac.make_material(k,v,roughness=.88) for k,v in P['palette_srgb'].items()]
SEM=[]

def mesh(name,v,f,mi=0,indices=None):
 o=ac.mesh_object(name,v,f,M,COL)
 for i,poly in enumerate(o.data.polygons):poly.material_index=indices[i] if indices else mi
 o['semantic_part']=name;SEM.append(o);return o

def loft_y(name,rings,n=16,mi=0,skin=False):
 # Each ring: y,z_center,width_radius,height_radius. Profile stations are custom.
 v=[(rx*math.cos(2*math.pi*j/n),y,z+rz*math.sin(2*math.pi*j/n)) for y,z,rx,rz in rings for j in range(n)]
 f=[tuple(range(n-1,-1,-1))];inds=[mi]
 for i in range(len(rings)-1):
  for j in range(n):
   f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
   angle=2*math.pi*(j+.5)/n
   inds.append(1 if skin and math.sin(angle)>.79 else 2 if skin and math.sin(angle)<-.65 else mi)
 f.append(tuple((len(rings)-1)*n+j for j in range(n)));inds.append(mi)
 return mesh(name,v,f,mi,inds)

def loft_z(name,rings,n=12,mi=0):
 # Ring: center_x,center_y,z, radius_x,radius_y.
 v=[(x+rx*math.cos(2*math.pi*j/n),y+ry*math.sin(2*math.pi*j/n),z) for x,y,z,rx,ry in rings for j in range(n)]
 f=[tuple(range(n-1,-1,-1))]
 for i in range(len(rings)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 f.append(tuple((len(rings)-1)*n+j for j in range(n)))
 return mesh(name,v,f,mi)

def tube(name,centers,radii,n=10,mi=3,aspect=1):
 v=[]
 for i,c in enumerate(centers):
  c=Vector(c);t=Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(i-1,0)]);t.normalize()
  e=t.cross(Vector((1,0,0)));e.normalize();q=t.cross(e).normalized()
  for j in range(n):v.append(tuple(c+radii[i]*(math.cos(2*math.pi*j/n)*e+aspect*math.sin(2*math.pi*j/n)*q)))
 f=[tuple(range(n-1,-1,-1))]
 for i in range(len(centers)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 f.append(tuple((len(centers)-1)*n+j for j in range(n)))
 return mesh(name,v,f,mi)

def ellipsoid(name,c,r,mi,n=12,lat=6):
 v=[(c[0],c[1],c[2]+r[2])]
 for k in range(1,lat):
  ph=math.pi*k/lat
  for j in range(n):
   th=2*math.pi*j/n;v.append((c[0]+r[0]*math.sin(ph)*math.cos(th),c[1]+r[1]*math.sin(ph)*math.sin(th),c[2]+r[2]*math.cos(ph)))
 v.append((c[0],c[1],c[2]-r[2]));last=len(v)-1
 f=[(0,1+j,1+(j+1)%n) for j in range(n)]
 for k in range(lat-2):
  for j in range(n):f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):f.append((last,1+(lat-2)*n+(j+1)%n,1+(lat-2)*n+j))
 return mesh(name,v,f,mi)

# Barrel-shaped ceratopsid body, not evidence of preserved postcranium.
loft_y('Torso_inferred',[( -1.03,1.24,.23,.33),(-.82,1.28,.41,.46),(-.55,1.25,.59,.55),(-.15,1.21,.69,.61),(.30,1.20,.72,.62),(.70,1.20,.66,.58),(1.04,1.21,.52,.49),(1.28,1.22,.34,.34),(1.44,1.20,.18,.20)],20,skin=True)
loft_y('Neck_under_frill',[(-1.54,1.19,.25,.28),(-1.30,1.24,.37,.35),(-1.08,1.26,.43,.38),(-.80,1.27,.38,.34)],16,skin=True)
# Long tapering tail, carried clear of ground, no invented clubs or spikes.
loft_y('Tail_inferred',[(1.14,1.24,.31,.31),(1.42,1.22,.28,.28),(1.68,1.15,.21,.22),(1.92,1.05,.15,.17),(2.18,.94,.095,.12),(2.43,.85,.049,.064),(2.48,.83,.010,.014)],12,skin=True)
# Four load-bearing articulated columnar limbs and broad feet.
for s in [-1,1]:
 tag='L' if s<0 else 'R'
 loft_z('Forelimb_'+tag,[(s*.55,-.63,1.43,.25,.28),(s*.62,-.65,1.13,.25,.25),(s*.66,-.59,.81,.20,.20),(s*.61,-.69,.49,.17,.18),(s*.61,-.76,.21,.19,.23),(s*.61,-.77,.07,.22,.28),(s*.61,-.77,.015,.21,.27)],12)
 loft_z('Hindlimb_'+tag,[(s*.49,.83,1.46,.29,.34),(s*.61,.81,1.19,.31,.34),(s*.65,.68,.86,.23,.25),(s*.62,.89,.60,.17,.20),(s*.61,.86,.26,.18,.23),(s*.61,.77,.09,.24,.31),(s*.61,.77,.015,.23,.30)],12)
 for y in [-.77,.77]:
  for j in [-1,0,1]:
   x=s*.61+j*.125
   loft_z(('Fore' if y<0 else 'Hind')+'_ungual_'+tag+'_'+str(j),[(x,y-.235,.02,.055,.085),(x,y-.25,.06,.064,.095),(x,y-.235,.13,.048,.063)],8,mi=3)
# Broad triangular cheek, narrowing muzzle and reconstructed rostral beak.
loft_y('Cranium_skin',[(-2.39,1.06,.115,.105),(-2.25,1.10,.20,.19),(-2.08,1.19,.25,.25),(-1.86,1.29,.31,.31),(-1.65,1.34,.43,.33),(-1.46,1.31,.42,.29),(-1.28,1.26,.31,.25)],16,skin=True)
loft_y('Lower_jaw_reconstructed',[(-2.40,.96,.10,.06),(-2.23,.94,.18,.095),(-1.97,.99,.27,.12),(-1.69,1.06,.36,.14),(-1.47,1.13,.31,.14)],12,mi=2)
loft_y('Horny_beak_reconstructed',[(-2.52,1.005,.018,.045),(-2.46,1.08,.10,.105),(-2.35,1.105,.151,.115),(-2.28,1.09,.166,.105)],12,mi=3)
# A thin recessed dark mouth line, kept within cheek silhouette.
for s in [-1,1]:
 tube('Mouth_line_'+str(s),[(s*.12,-2.38,.992),(s*.205,-2.22,1.005),(s*.28,-1.98,1.06),(s*.345,-1.76,1.125)],[.008,.009,.010,.006],6,5)
 ellipsoid('Cheek_boss_'+str(s),(s*.385,-1.51,1.17),(.14,.20,.15),0)
 # modest epijugal triangular point, skin-covered rather than extravagant horns.
 tube('Epijugal_'+str(s),[(s*.39,-1.54,1.17),(s*.50,-1.58,1.12),(s*.57,-1.63,1.10)],[.10,.065,.008],8,0)
 ellipsoid('Eye_socket_'+str(s),(s*.318,-1.743,1.473),(.074,.113,.090),1)
 ellipsoid('Eye_'+str(s),(s*.371,-1.765,1.485),(.030,.061,.046),5)
 ellipsoid('Eye_glint_'+str(s),(s*.396,-1.787,1.50),(.008,.013,.012),3,8,4)
 ellipsoid('Nostril_'+str(s),(s*.208,-2.233,1.17),(.019,.045,.025),5,10,4)
# Dominant nasal horn and explicitly abbreviated paired supraorbital horns.
tube('Dominant_nasal_horn',[(0,-2.055,1.38),(0,-2.08,1.60),(0,-2.13,1.84),(0,-2.20,2.04),(0,-2.22,2.13)],[.155,.132,.087,.031,.004],12,3,aspect=.92)
for s in [-1,1]:
 tube('Short_brow_horn_'+str(s),[(s*.265,-1.65,1.55),(s*.28,-1.67,1.68),(s*.29,-1.73,1.81),(s*.29,-1.78,1.84)],[.112,.080,.034,.004],10,3)
# Filled soft-tissue frill: no bone fenestrae punched through living skin.
C=Vector((0,-1.39,1.48));U=Vector((1,0,0));V=Vector((0,.56,.8284926071));N=U.cross(V).normalized();RX=.75;RZ=.66
# N faces rostrally (-Y), hence front surface uses positive normal offsets.
n=40;v=[]
for depth,fac in [( .075,0),(.075,.48),(.030,1),(-.075,1),(-.065,.48),(-.065,0)]:
 if fac==0:v.append(tuple(C+N*depth));continue
 for j in range(n):
  t=2*math.pi*j/n
  # Taper the lower neck notch without perforating the living shield.
  x=RX*math.sin(t)*fac;vv=RZ*math.cos(t)*fac
  x*=1+.18*min(0,math.cos(t))
  v.append(tuple(C+U*x+V*vv+N*depth))
# indices front center 0, rings 1..40,41..80,81..120,121..160, back center161.
f=[];idx=[]
for j in range(n):f.append((0,1+j,1+(j+1)%n));idx.append(4)
for st,en in [(1,41),(41,81),(81,121)]:
 for j in range(n):f.append((st+j,en+j,en+(j+1)%n,st+(j+1)%n));idx.append(4 if st==1 else 0)
for j in range(n):f.append((161,121+(j+1)%n,121+j));idx.append(0)
mesh('Short_crown_frill',v,f,indices=idx)
# Fifteen flattened marginal ossifications: P0 and seven named pairs.
def crown_plate(name,theta,width,length,depth,forward=0):
 t=math.radians(theta);rad=(U*math.sin(t)+V*math.cos(t)).normalized();tan=(U*math.cos(t)-V*math.sin(t)).normalized()
 base=C+U*(RX*math.sin(t)*(1+.18*min(0,math.cos(t))))+V*(RZ*math.cos(t))+N*forward-rad*.066
 outline=[(-width*.43,0),(-width*.51,length*.39),(-width*.37,length*.78),(-width*.15,length*.96),(0,length),(width*.23,length*.92),(width*.46,length*.61),(width*.43,0)]
 verts=[tuple(base+tan*x+rad*y+N*z) for z in [-depth/2,depth/2] for x,y in outline]
 # Thick bevel-free solids, flat in frill plane not conical spikes.
 k=len(outline);faces=[tuple(range(k-1,-1,-1)),tuple(k+i for i in range(k))]
 faces += [(j,(j+1)%k,(j+1)%k+k,j+k) for j in range(k)]
 o=mesh(name,verts,faces,3);o['cranial_homology']=name;return o
for s in [-1,1]:
 for label,theta,w,l in [('P1',18,.30,.29),('P2',41,.30,.27),('PS',64,.245,.225),('S1',83,.19,.18),('S2',99,.155,.145),('S3',113,.14,.12),('S4',126,.135,.11)]:
  crown_plate(label+('_L' if s<0 else '_R'),theta*s,w,l,.065 if label.startswith('P') else .05)
crown_plate('P0_median_rostrally_offset',0,.21,.225,.14,.065)
# Origin is center of weight-bearing footprint. Feet are flattened at the floor.
ac.ground_asset(COL,False)
qa=ac.audit_source(COL,max_triangles=6500)
if qa['errors']:raise RuntimeError(qa['errors'])
# Preserve editable semantic solids in .blend; export-only merge is lossless.
bpy.context.scene['reconstruction_scope']='Living reconstruction. Skull TMP2005.055.0001; body comparative and artistic.'
bpy.context.scene['frill_plate_homologies']='P0 + bilateral P1,P2,PS,S1,S2,S3,S4'
bpy.context.scene['source_generator']='source/generate.py'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
# Initial low-cost neutral diagnostic views are source-only and private.
if a.gray:
 for mat in M:
  b=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');b.inputs['Base Color'].default_value=(.28,.28,.28,1)
 ac.render_previews(COL,OUT/'gray',views=('front','side','top','hero'),resolution=512,samples=6)
else:
 root=bpy.data.objects.get(COL['asset_root']);bpy.ops.object.select_all(action='DESELECT')
 for o in SEM:o.select_set(True)
 bpy.context.view_layer.objects.active=SEM[0];bpy.ops.object.join();joined=bpy.context.object;joined.name='Regaliceratops_render_mesh';joined.parent=root
 root.select_set(True)
 options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
 avail={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties};assert set(options)<=avail
 bpy.ops.export_scene.gltf(**options)
 qg=audit_glb(OUT/'model.glb',6500,6,12);doc,binary,raw=read_glb(OUT/'model.glb')
 if qg['errors']:raise RuntimeError(qg['errors'])
 source=qa['bounds_blender_m'];expected={'min':[source['min'][0],source['min'][2],-source['max'][1]],'max':[source['max'][0],source['max'][2],-source['min'][1]]}
 delta=max(abs(qg['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3));assert delta<.00001
 assert qg['scene_triangles']==qa['triangles'] and qg['bytes']<=2000000
 report={'status':'PASS','claim_scope':'Source geometry, static self-contained GLB audit, axis/bounds equivalence. Not Khronos, GPU, independent quality or scene performance.','blender_version':bpy.app.version_string,'seed':405,'source':qa,'glb':qg,'export_options':{k:v for k,v in options.items() if k!='filepath'},'bounds_roundtrip_max_error_m':delta,'semantic_digest':semantic_digest(doc,binary),'semantic_parts':[o['name'] for o in qa['parts']],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((Path(__file__).parent/'params.json').read_bytes()).hexdigest()}
 (OUT/'qa/evidence/technical.json').write_text(json.dumps(report,indent=2)+'\n')
 if a.render:
  bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
  imported=bpy.data.collections.new('IMPORTED_EXACT_GLB');bpy.context.scene.collection.children.link(imported)
  for obj in list(bpy.context.scene.objects):
   for c in list(obj.users_collection):c.objects.unlink(obj)
   imported.objects.link(obj)
  paths=ac.render_previews(imported,OUT/'private/final-render-temp',views=('front','side','top','hero'),resolution=1024,samples=24)
  (OUT/'views').mkdir(exist_ok=True)
  for view in ['front','side','top']:shutil.copy2(OUT/f'private/final-render-temp/preview-{view}.png',OUT/f'views/{view}.png')
  shutil.copy2(OUT/'private/final-render-temp/preview-hero.png',OUT/'views/perspective.png');shutil.copy2(OUT/'views/perspective.png',OUT/'preview.png')
  (OUT/'qa/evidence/render.json').write_text(json.dumps({'status':'RENDERED','origin':'Clean import of exact delivered model.glb; not source scene','glb_sha256':qg['sha256'],'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','threads':2,'resolution':[1024,1024],'samples':24,'views':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'camera':'Orthographic; perspective filename denotes oblique hero, not a perspective projection','color_management':'Standard / None, exposure 0, gamma 1','preview_reuses':'views/perspective.png','gpu':'NOT_RUN','scene':'NOT_RUN'},indent=2)+'\n')
print('GENERATOR_COMPLETE',OUT)
