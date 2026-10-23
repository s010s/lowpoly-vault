# SPDX-License-Identifier: MIT
"""Original deterministic Naticarius interpretation. Run in Blender 4.3.2:
blender -b --factory-startup -t 2 --python source/generate.py -- --output OUTPUT
Only this source tree, bundled deps, params, and Blender runtime are required.
"""
from pathlib import Path
import sys, json, math, hashlib, shutil, argparse
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
args=argparse.ArgumentParser(); args.add_argument('--output',required=True)
a=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=Path(a.output).resolve(); out.mkdir(parents=True,exist_ok=True)
ev=out/'qa'/'evidence'; ev.mkdir(parents=True,exist_ok=True)
C=ac.setup_scene(P['asset_id'],P['seed'])
mats=[ac.make_material(name,P['palette'][key],P['roughness']) for name,key in [('fossil-ivory-exterior','exterior'),('warm-stone-inner-lining','lining'),('pale-columellar-callus-and-lip','lip_callus'),('subtle-suture-tone','suture')]]
N=P['body_segments']; vv=[]; ff=[]; mm=[]
# Each cross-section is an original D-profile. Rear rings form an inflated globe;
# front rings bend continuously around the lip into a genuinely recessed lining.
# Values are millimeters prior to final metric conversion.
# (center-x, y, center-z, right-radius, left-radius, vertical-radius, flatten-left)
outer=[(-1,12.8,12.4,0.0,0.0,0.0,0),
 (-1,12.3,12.4,3.8,3.9,3.7,0),(-1,11.3,12.4,6.6,6.8,6.3,0),
 (-1,9.8,12.4,9.4,9.6,8.7,0),(-1,7.8,12.4,11.7,12,10.5,0),
 (-1,5.3,12.4,13.2,13.7,11.7,0),(-1,2.5,12.4,14.1,14.6,12.2,0),
 (-0.7,-0.2,12.4,14.8,14.3,12.4,0),(-0.2,-2.6,12.3,14.5,13.7,12.3,0),
 (0.8,-4.6,12.15,13.5,12.4,12.0,0), (2.0,-6.2,11.9,12.0,10.4,11.6,0.1),
 (3.0,-7.5,11.7,10.8,8.4,11.25,0.3), (4.0,-8.4,11.55,9.7,6.8,10.9,0.65),
 (4.6,-8.85,11.4,9.0,6.0,10.7,0.8),
 # Rounded attached rim. Columellar side has deliberately greater thickness.
 (4.7,-9.10,11.4,8.7,5.5,10.45,0.9),
 (4.75,-9.05,11.4,8.35,4.7,10.05,0.95)]
inner=[(4.7,-8.65,11.4,8.1,4.5,9.85,.96),
 (4.6,-7.8,11.5,8.35,4.7,9.8,.9),(4.2,-6.5,11.65,8.8,5.1,9.7,.7),
 (3.5,-4.8,11.9,9.3,5.6,9.5,.4),(2.7,-2.8,12.05,9.5,6.2,9.05,.2),
 (1.9,-0.6,12.1,9.3,6.9,8.4,.05),(1.3,1.7,12.1,8.5,7.15,7.35,0),
 (.8,3.8,12.1,7.1,6.8,6.0,0),(.5,5.5,12.1,5.35,5.3,4.4,0),
 (.3,6.6,12.1,3.25,3.3,2.65,0),(.25,7.1,12.1,1.5,1.5,1.25,0),
 (.25,7.25,12.1,0.,0.,0.,0)]
def ring_point(row,j,is_outer=False,idx=0):
 cx,y,cz,rr,lr,rz,flat=row; th=2*math.pi*j/N
 c,s=math.cos(th),math.sin(th)
 # Flatten only the inner/columellar left side; broad right outer lip stays round.
 xx=c*(rr if c>=0 else lr)
 if c<0: xx=-lr*((-c)**(1-0.65*flat))
 x=cx+xx; z=cz+rz*s
 # Upper opening tilts slightly backwards; lower lip projects naturally.
 y+=0.50*s+0.25*math.cos(2*th)
 # Small blind umbilical recess, actually depressed into the outer shell,
 # immediately beside upper columellar shoulder. Not a dark color patch.
 if is_outer and 9<=idx<=14:
  angle=math.atan2(math.sin(th-2.78),math.cos(th-2.78))
  angle+=.06*(idx-12.6)
  depth=5.0*math.exp(-((idx-12.6)/1.05)**2-(angle/.23)**2)
  y+=depth
 return (x*.001,y*.001,z*.001)
# Use single vertices at the two closed poles to avoid degenerate ring triangles.
vv.append((outer[0][0]*.001,outer[0][1]*.001,outer[0][2]*.001))
outer_rows=[]
for k in range(1,len(outer)):
 outer_rows.append((outer[k],k))
 if 9<=k<=13:
  outer_rows.append(([(a+b)/2 for a,b in zip(outer[k],outer[k+1])],k+.5))
ring_rows=[row for row,idx in outer_rows]+inner[:-1]
for k,row in enumerate(ring_rows):
 for j in range(N): vv.append(ring_point(row,j,k<len(outer_rows),outer_rows[k][1] if k<len(outer_rows) else 0))
for j in range(N): ff.append((0,1+(j+1)%N,1+j)); mm.append(0)
for k in range(len(ring_rows)-1):
 orig_idx=outer_rows[k][1] if k<len(outer_rows) else 99
 mat=0 if orig_idx<12 else 2 if orig_idx<=15 else 1
 for j in range(N):
  u=1+k*N+j; v=1+k*N+(j+1)%N
  ff.append((u,v,v+N,u+N)); mm.append(mat)
last=len(vv); row=inner[-1]; vv.append((row[0]*.001,row[1]*.001,row[2]*.001))
base=1+(len(ring_rows)-1)*N
for j in range(N): ff.append((base+j,base+(j+1)%N,last)); mm.append(1)
body=ac.mesh_object('inflated-body-open-aperture-continuous-lining',vv,ff,mats[:3],C)
for p,mi in zip(body.data.polygons,mm):
 p.material_index=mi
 p.use_smooth=True
# Deliberately smooth normals on low-polygon shell; no opaque plug or detached lip ring.
body['construction']='One closed shell wall: exterior, curved lip, columella and shallow continuous cavity.'
body['umbilicus']='Blind geometric depression on outer wall beside upper columella; not a texture.'
# NAT-01: A continuous dextral spiral groove in a single triangulated mantle.
# Constrained Delaunay edges follow the actual descending suture and both lips.
# The mantle's outer skirt lies within the accepted body; no nested ring shoulders.
from mathutils.geometry import delaunay_2d_cdt
from mathutils import Vector as V2
xy=[];zz=[];edges=[]
def dome(r):
 return 28.2-.62*r-.04*r*r-1.2*max(0,r-6.0)**2

def add(x,y,z):
 xy.append(V2((x,y)));zz.append(z);return len(xy)-1
center_index=add(0,0,28.2)
T=math.log(6.6/.25)/.24;steps=168
curve_ids=[[],[],[]]
for k in range(steps+1):
 t=T*k/steps;theta=-t+1.3;r=.25*math.exp(.24*t)
 width=.10*r+.05
 for lane,delta in enumerate([-width,0,width]):
  radius=r+delta
  lip=[.24,-.46,.27][lane]*min(1,r/.65)
  z=dome(radius)+lip
  curve_ids[lane].append(add(radius*math.cos(theta),radius*.9*math.sin(theta),z))
for ids in curve_ids:
 for u,v in zip(ids,ids[1:]):edges.append((u,v))
# Sparse fill samples give the broad rounded whorl shoulders their own geometry.
# They use the same phase field, so no flat bridges erase the constrained suture.
def surface(r,th):
 if r<.2:return dome(r)
 phase=math.log(r/.25)/.24+th-1.3
 wrap=math.atan2(math.sin(phase),math.cos(phase))
 center=r*math.exp(-.24*wrap);width=.1*center+.05
 d=r-center
 if abs(d)<=width:delta=-.46+.72*(abs(d)/width)**.6
 else:delta=.22+.10*math.sin(wrap/2)**2
 return dome(r)+delta*min(1,r/.65)

for radius in [.45,.85,1.4,2.1,3.0,4.2,5.6,6.6]:
 for j in range(40):
  th=2*math.pi*(j+.37)/40
  add(radius*math.cos(th),radius*.9*math.sin(th),surface(radius,th))
outer=[]
for j in range(48):
 th=2*math.pi*j/48;outer.append(add(7.6*math.cos(th),7.6*.9*math.sin(th),19.8))
for u,v in zip(outer,outer[1:]+outer[:1]):edges.append((u,v))
rv,re,rf,origv,orige,origf=delaunay_2d_cdt(xy,edges,[],0,1e-6,True)
sv=[];mapping={}
for i,(point,orig) in enumerate(zip(rv,origv)):
 if not orig:raise RuntimeError('Unexpected intersecting suture constraints; fix source')
 z=sum(zz[v] for v in orig)/len(orig)
 for v in orig:mapping[v]=i
 sv.append(((point.x-3.5)*.001,(point.y+1.2)*.001,z*.001))
sf=[tuple(face) for face in rf]
bottom=len(sv);sv.append((-.0035,.0012,.0192))
for j in range(48):sf.append((bottom,mapping[outer[(j+1)%48]],mapping[outer[j]]))
spire=ac.mesh_object('low-dextral-spire-continuous-descending-suture',sv,sf,[mats[0],mats[3]],C)
for p in spire.data.polygons:
 p.use_smooth=True
 # Color only the full constrained furrow strip, avoiding per-triangle dotted edges.
 inside=[]
 for vi in p.vertices:
  mid=spire.data.vertices[vi].co
  xx=mid.x*1000+3.5;yy=(mid.y*1000-1.2)/.9
  rad=math.hypot(xx,yy);th=math.atan2(yy,xx)
  if not (.32<rad<6.4 and mid.z>.023):inside.append(False);continue
  phase=math.log(rad/.25)/.24+th-1.3
  wrap=math.atan2(math.sin(phase),math.cos(phase));rr=rad*math.exp(-.24*wrap)
  inside.append(abs(rad-rr)<=(.1*rr+.05)*1.02)
 if all(inside):p.material_index=1

spire['construction']='Single closed low mantle with a clockwise-outward expanding, descending geometric suture and asymmetric lips; outer skirt embeds into body whorl.'
spire['suture_turns']=T/(2*math.pi)
# Exact requested working dimensions, derived from photographic estimates, not calipers.
bpy.context.view_layer.update(); pts=ac._vertices_world(C);lo,hi=ac._bounds(pts)
factors=[P['target_dimensions_m'][i]/(hi[i]-lo[i]) for i in range(3)]
for obj in C.all_objects:
 if obj.type=='MESH':
  for v in obj.data.vertices:
   for d in range(3):v.co[d]*=factors[d]
  obj.data.update()
ac.ground_asset(C,center_xy=True)
# Bake the grounding translation into mesh vertices while keeping identity transforms.
for ob in C.all_objects:
 if ob.type=='MESH':
  M=ob.matrix_world.copy()
  for v in ob.data.vertices:v.co=M@v.co
  ob.matrix_world.identity()
bpy.context.view_layer.update()
stage=out/'private'/'generated'; stage.mkdir(parents=True,exist_ok=True)
record=ac.export_asset('naticarius',{'en':'Naticarius rounded fossil moon-snail shell','zh':'Naticarius 圆体玉螺化石壳'},'invertebrates',C,
 metadata={'description':{'en':'Original fossil-shell interpretation of PRI 69688: inflated body whorl, low dextral spire and genuinely recessed open aperture.','zh':'依据 PRI 69688 的原创化石贝壳形态解释：圆体圈、低螺塔和真实开口。'},'generator':'source/generate.py','sources':['https://neogeneatlas.net/species/naticarius-plicatella/'],'reconstruction_notes':['Photographic working scale, not specimen-exact scan.','Spire base intersects main shell intentionally; opening is one continuous shell-wall mesh.']},
 output_root=stage,render=False,max_triangles=6000,max_materials=5,max_primitives=8)
for src,dst in [('naticarius.glb','model.glb'),('naticarius.blend','model.blend')]:shutil.copy2(stage/'naticarius'/src,out/dst)
qa=json.loads((stage/'naticarius'/'qa.json').read_text())
qa['glb']['file']='model.glb'
(ev/'source-and-glb.json').write_text(json.dumps(qa,indent=2)+'\n')
for k in ('glb','blend','preview'):record[k]={'glb':'model.glb','blend':'model.blend','preview':'preview.png'}[k]
record['source_hashes']={p.relative_to(HERE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix in ['.py','.json','.cjs']}
record['brief_scale_note']='H28 W30 D25 mm are image estimates (PRI69688 5mm scale), not caliper measurements; approximately 15% proportional uncertainty.'
record['exporter_version']='4.3.47'
record['consuming_three_version']='0.180.0'
(ev/'build-metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print('MODEL_GENERATED',json.dumps({'glb_sha256':qa['glb']['sha256'],'triangles':qa['glb']['scene_triangles'],'bytes':qa['glb']['bytes']}))
