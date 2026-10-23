# SPDX-License-Identifier: MIT
"""Deterministic original Monolophosaurus living reconstruction, metres.
Usage: blender -b -t 2 --python source/generate.py -- --output OUTPUT
Only the standard library, Blender bundled modules, params.json and vendored
source/deps are required. Limbs/distal tail are comparative reconstruction.
"""
import sys, json, math, hashlib, argparse, shutil
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
SRC=Path(__file__).resolve().parent
sys.path.insert(0,str(SRC/'deps'))
import asset_common as ac
from qa_glb import audit_glb
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=SRC.parent);ap.add_argument('--clay',action='store_true');ap.add_argument('--final-views',action='store_true');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=True);(OUT/'qa/evidence').mkdir(parents=True,exist_ok=True)
P=json.loads((SRC/'params.json').read_text());C=ac.setup_scene('monolophosaurus',seed=P.get('seed',317))
M=[ac.make_material(n,c) for n,c in [('skin-moss-taupe','#827960'),('underside-sand','#B2A58C'),('median-crest-earth','#8D6F55'),('eye-nostril-mouth','#292923'),('claw-horn','#C9B99B'),('iris-ochre','#AA8E50')]]
V=[];F=[];MI=[];GROUP=[]
def mesh_part(name,vs,fs,mat=0,face_materials=None):
 start=len(V); V.extend(vs);F.extend(tuple(start+i for i in f) for f in fs);MI.extend(face_materials if face_materials is not None else [mat]*len(fs));GROUP.append((name,start,len(V)))
def loft(name,sections,n=12,mat=0,belly=False):
 # Cross sections in X/Z at measured longitudinal stations. Elliptical but
 # intentionally differing dorsal/ventral dimensions create anatomical profiles.
 vs=[];fs=[];ms=[]
 for y,x,z,rx,ru,rd in sections:
  for j in range(n):
   t=2*math.pi*j/n;c=math.cos(t);vs.append((x+rx*math.sin(t),y,z+(ru if c>=0 else rd)*c))
 for k in range(len(sections)-1):
  for j in range(n):
   fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));ms.append(1 if belly and n*.32<j<n*.68 else mat)
 for end,rev in ((0,True),(len(sections)-1,False)):
  y,x,z,rx,ru,rd=sections[end];c=len(vs);vs.append((x,y,z))
  for j in range(n):
   fs.append((c,end*n+(j+1)%n,end*n+j) if rev else (c,end*n+j,end*n+(j+1)%n));ms.append(mat)
 mesh_part(name,vs,fs,mat,ms)
def sweep(name,sections,n=10,mat=0):
 # Adaptive cross sections transported along a bent centreline, avoiding
 # primitive sphere/cylinder appendages and keeping every segment closed.
 points=[Vector(s[:3]) for s in sections];vs=[];fs=[]
 for i,s in enumerate(sections):
  t=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
  u=t.cross(Vector((0,1,0)))
  if u.length<.1:u=t.cross(Vector((0,0,1)))
  u.normalize();v=t.cross(u).normalized()
  for j in range(n):
   a=2*math.pi*j/n;p=points[i]+u*math.cos(a)*s[3]+v*math.sin(a)*s[4];vs.append(tuple(p))
 for i in range(len(points)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 for i,rev in ((0,True),(len(points)-1,False)):
  c=len(vs);vs.append(tuple(points[i]))
  for j in range(n):fs.append((c,i*n+(j+1)%n,i*n+j) if rev else (c,i*n+j,i*n+(j+1)%n))
 mesh_part(name,vs,fs,mat)
def oval(name,center,radii,mat,n=10,rings=6):
 # Closed latitude loft with actual single pole vertices, no degenerate caps.
 x,y,z=center;rx,ry,rz=radii;vs=[(x,y,z+rz)];fs=[]
 for k in range(1,rings):
  a=math.pi*k/rings
  for j in range(n):
   t=2*math.pi*j/n;vs.append((x+rx*math.sin(a)*math.cos(t),y+ry*math.sin(a)*math.sin(t),z+rz*math.cos(a)))
 bot=len(vs);vs.append((x,y,z-rz))
 for j in range(n):fs.append((0,1+j,1+(j+1)%n))
 for k in range(rings-2):
  for j in range(n):fs.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):fs.append((bot,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
 mesh_part(name,vs,fs,mat)
# ONE continuous axial envelope: muzzle, skull, S-neck, ribcage, pelvis and tail.
loft('continuous-head-neck-trunk-tail',[
 (-2.45,0,1.940,.075,.075,.066),(-2.40,0,1.955,.125,.094,.078),
 (-2.23,0,1.976,.136,.103,.090),(-2.03,0,1.990,.155,.120,.105),
 (-1.84,0,2.005,.175,.146,.129),(-1.68,0,1.985,.172,.155,.150),
 (-1.55,0,1.910,.148,.155,.161),(-1.42,0,1.786,.159,.191,.210),
 (-1.20,0,1.610,.219,.250,.256),(-.95,0,1.490,.295,.311,.308),
 (-.62,0,1.460,.373,.364,.350),(-.23,0,1.460,.397,.393,.360),
 (.15,0,1.460,.365,.374,.310),(.45,0,1.449,.289,.303,.273),
 (.70,0,1.449,.232,.236,.221),(1.03,0,1.432,.182,.180,.165),
 (1.40,.025,1.383,.138,.139,.122),(1.80,.060,1.318,.100,.100,.086),
 (2.18,.096,1.238,.068,.070,.061),(2.55,.120,1.165,.044,.043,.038),
 (2.90,.125,1.117,.023,.023,.021),(3.16,.115,1.103,.009,.011,.009),
 (3.25,.110,1.102,.002,.003,.002)],n=14,belly=True)
# Distinct lower jaw, held closed. Upper edge terminates at the jaw hinge.
loft('articulated-mandible',[
 (-2.43,0,1.885,.060,.030,.037),(-2.35,0,1.873,.115,.043,.055),
 (-2.12,0,1.860,.137,.048,.064),(-1.91,0,1.859,.154,.048,.072),
 (-1.72,0,1.876,.168,.048,.074),(-1.59,0,1.905,.121,.030,.040)],n=10,mat=0,belly=True)
# One sagittal crest, broad side profile and narrow transverse section.
loft('single-median-nasal-crest',[
 (-2.34,0,2.069,.017,.013,.030),(-2.26,0,2.142,.033,.082,.070),
 (-2.13,0,2.181,.041,.156,.105),(-1.94,0,2.195,.044,.155,.096),
 (-1.77,0,2.197,.043,.153,.072),(-1.67,0,2.163,.030,.110,.056),
 (-1.60,0,2.132,.012,.012,.030)],n=8,mat=2)
for s,tag,dy in [(1,'right',-.065),(-1,'left',.065)]:
 # Continuous bent hindleg profile, broad thigh fades into flank.
 sweep(tag+'-thigh-shank-ankle',[
 (s*.235,.23+dy,1.49,.205,.245),(s*.365,.13+dy,1.26,.224,.250),
 (s*.425,-.105+dy,.995,.174,.188),(s*.439,-.045+dy,.835,.125,.133),
 (s*.445,.207+dy,.545,.077,.095),(s*.444,.274+dy,.397,.066,.078),
 (s*.443,.176+dy,.170,.052,.061),(s*.443,.095+dy,.094,.065,.071)],n=12)
 # Three main toes, separated at tips, grounded on a planar underside.
 for k in (-1,0,1):
  x=s*.443+k*.074;endx=s*.443+k*.154;ey=(-.435 if k==0 else -.345)+dy
  sweep(tag+'-toe-'+str(k+2),[(x,.112+dy,.080,.050,.049),
    (x+k*.025,-.050+dy,.036,.044,.034),
    (endx,ey+.09,.029,.034,.025),(endx,ey,.028,.024,.019)],n=8)
  sweep(tag+'-toe-claw-'+str(k+2),[(endx,ey+.018,.036,.025,.021),
    (endx,ey-.052,.027,.019,.016),(endx,ey-.102,.010,.002,.002)],n=6,mat=4)
 # Three digits are comparative tetanuran anatomy, not preserved on IVPP84019.
 sweep(tag+'-upperarm-forearm-palm',[
 (s*.245,-.858,1.490,.104,.114),(s*.361,-.731,1.290,.086,.090),
 (s*.388,-.642,1.125,.070,.070),(s*.405,-.797,1.076,.056,.061),
 (s*.400,-.984,1.063,.047,.049),(s*.392,-1.045,1.005,.044,.060),
 (s*.393,-1.000,.945,.038,.065),(s*.393,-.965,.910,.028,.045)],n=10)
 for k in range(3):
  yy=-1.078+k*.054;zz=1.044-k*.060
  sweep(tag+'-inward-palm-digit-'+str(k+1),[
   (s*.393,yy+(.04 if k==0 else 0),zz-(.02 if k==0 else 0),.027,.027),(s*(.408+k*.018),yy-.114,zz-.055,.022,.024),
   (s*(.390+k*.018),yy-.160,zz-.129,.015,.018)],n=7)
  sweep(tag+'-manual-claw-'+str(k+1),[
   (s*(.390+k*.018),yy-.154,zz-.121,.017,.018),
   (s*(.363+k*.018),yy-.158,zz-.167,.012,.011),
   (s*(.342+k*.018),yy-.142,zz-.185,.0018,.002)],n=6,mat=4)
 # Eyes are recessed into skull, not floating globes; iris faces laterally.
 oval(tag+'-orbital-shadow',(s*.154,-1.768,2.038),(.026,.059,.040),3,n=10,rings=6)
 oval(tag+'-iris',(s*.177,-1.781,2.042),(.007,.028,.026),5,n=10,rings=5)
 oval(tag+'-pupil',(s*.183,-1.786,2.042),(.003,.013,.019),3,n=8,rings=5)
 # Subtle bony brow, not a horn or second crest.
 sweep(tag+'-brow',[(s*.116,-1.854,2.087,.019,.016),(s*.125,-1.783,2.091,.020,.017),(s*.122,-1.686,2.086,.019,.016)],n=8)
 oval(tag+'-nostril',(s*.120,-2.301,2.001),(.009,.028,.017),3,n=8,rings=5)
 # Narrow fitted mouth seam with no unsupported teeth or open cavity.
 sweep(tag+'-mouth-seam',[(s*.056,-2.430,1.885,.0015,.0015),(s*.110,-2.350,1.873,.002,.002),
 (s*.131,-2.12,1.860,.002,.002),(s*.147,-1.91,1.859,.002,.002),
 (s*.160,-1.720,1.876,.002,.002),(s*.114,-1.590,1.905,.0015,.0015)],n=5,mat=3)
# Place all three toe pads per foot on the same support plane. Their
# paired claws translate with them, preserving the toe/claw joint.
for side in ('left','right'):
 for number in (1,2,3):
  toe=next((a,b) for name,a,b in GROUP if name==side+'-toe-'+str(number))
  dz=-min(V[i][2] for i in range(*toe))
  for name,a,b in GROUP:
   if name in (side+'-toe-'+str(number),side+'-toe-claw-'+str(number)):
    for i in range(a,b): V[i]=(V[i][0],V[i][1],V[i][2]+dz)
obj=ac.mesh_object('anatomical-surface',V,F,M,C)
for p,mi in zip(obj.data.polygons,MI):p.material_index=mi
for name,a,b in GROUP:obj.vertex_groups.new(name=name).add(list(range(a,b)),1,'REPLACE')
obj['construction']='Original profile lofts and transported tapered sections; semantic vertex groups retained.'
obj['reconstruction_caution']='IVPP84019 preserves skull, pelvis and axial column through sixth caudal; limbs and distal tail are comparative reconstruction.'
# Feet support points define the floor; preserve a single identity root.
ac.ground_asset(C,False)
qa=ac.audit_source(C,max_triangles=6000)
if qa['errors']:raise RuntimeError(qa['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in C.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects['monolophosaurus']
opts=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
avail={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-avail:raise RuntimeError('Missing exporter options: '+str(set(opts)-avail))
bpy.ops.export_scene.gltf(**opts)
g=audit_glb(OUT/'model.glb',6000,6,12)
g['file']='model.glb'
if g['errors']:raise RuntimeError(g['errors'])
b=qa['bounds_blender_m']; exp={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
delta=max(abs(g['bounds_m'][k][i]-exp[k][i]) for k in ('min','max') for i in range(3))
assert delta<1e-4 and g['scene_triangles']==qa['triangles'] and g['bytes']<2000000
report={'asset_id':'monolophosaurus','revision':'r001','glb_sha256':g['sha256'],'blender':bpy.app.version_string,'seed':317,'source':qa,'glb':g,'bounds_roundtrip_max_error_m':delta,'source_generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((SRC/'params.json').read_bytes()).hexdigest(),'export_options':{k:v for k,v in opts.items() if k!='filepath'},'semantic_groups':[x[0] for x in GROUP],'scope':'Maker technical checks only, independent review and browser/GPU/scene are NOT_RUN.'}
(OUT/'qa/evidence/build.json').write_text(json.dumps(report,indent=2)+'\n')
if args.clay or args.final_views:
 # Discard source scene and import EXACT exported bytes for all image evidence.
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.gltf(filepath=str(OUT/'model.glb'))
 imported=list(bpy.context.scene.objects);RC=bpy.data.collections.new('EXACT_GLB');bpy.context.scene.collection.children.link(RC)
 for o in imported:
  for old in list(o.users_collection):old.objects.unlink(o)
  RC.objects.link(o)
 bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
 if args.clay:
  clay=ac.make_material('selfcheck-clay','#929292');bpy.context.view_layer.material_override=clay
  files=ac.render_previews(RC,OUT/'private/clay',views=('front','side','top','hero'),resolution=384,samples=6)
  (OUT/'private/clay/evidence.json').write_text(json.dumps({'glb_sha256':g['sha256'],'views':[Path(x).name for x in files],'resolution':384,'samples':6,'scope':'Maker low-cost structural selfcheck, not independent QA'},indent=2)+'\n')
 if args.final_views:
  bpy.context.view_layer.material_override=None
  files=ac.render_previews(RC,OUT/'private/final-render',views=('front','side','top','hero'),resolution=900,samples=20)
  (OUT/'views').mkdir(exist_ok=True)
  for view in ('front','side','top'):shutil.copy2(OUT/'private/final-render'/('preview-'+view+'.png'),OUT/'views'/(view+'.png'))
  shutil.copy2(OUT/'private/final-render/preview-hero.png',OUT/'preview.png');shutil.copy2(OUT/'preview.png',OUT/'views/perspective.png')
  vr={'glb_sha256':g['sha256'],'source':'Clean import of delivered model.glb, not source-scene render','renderer':'Blender Cycles CPU','resolution':[900,900],'samples':20,'threads':2,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'background_srgb':'#E8E4DC','directions':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'perspective_reuses_preview':True,'files':{p.relative_to(OUT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT/'preview.png',*(OUT/'views'/f'{v}.png' for v in ('front','side','top','perspective'))]}}
  (OUT/'qa/evidence/views.json').write_text(json.dumps(vr,indent=2)+'\n')
print('BUILD_COMPLETE',json.dumps({'triangles':g['scene_triangles'],'bytes':g['bytes'],'glb_sha256':g['sha256']}))
