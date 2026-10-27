# SPDX-License-Identifier: MIT
"""Original Habelia optata Morph A; design units mm, exported meters.
Full scene built from scratch; no external geometry or downloaded meshes.
"""
import bpy, bmesh, sys, json, math, hashlib, shutil
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import asset_common as common
C=json.loads((ROOT/'generator-config.json').read_text())
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
GRAY='--graybox' in ARGS
DEST=Path(ARGS[ARGS.index('--out')+1]).resolve() if '--out' in ARGS else ROOT
DEST.mkdir(parents=True,exist_ok=True)
collection=common.setup_scene('habelia',C['seed'])
scene=bpy.context.scene
scene.render.threads_mode='FIXED';scene.render.threads=C['render']['threads']
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
mats={k:common.make_material(k,'#929292' if GRAY else v) for k,v in C['palette'].items()}
class Shape:
 def __init__(self,name,mat,role):self.name=name;self.mat=mat;self.role=role;self.v=[];self.f=[];self.components=[]
 def add(self,vs,fs,label):
  n=len(self.v);self.v.extend(vs);self.f.extend(tuple(n+i for i in f) for f in fs);self.components.append({'label':label,'vertex_start':n,'vertex_count':len(vs)})
 def finish(self):
  o=common.mesh_object(self.name,[tuple(x*.001 for x in v) for v in self.v],self.f,mats[self.mat],collection)
  o['anatomical_role']=self.role;o['closed_subcomponents']=json.dumps(self.components,separators=(',',':'))
  return o

def tube(shape,pts,radii,label,sides=8,flatten=1):
 pts=[Vector(p) for p in pts];vs=[];fs=[]
 for i,p in enumerate(pts):
  d=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized()
  ref=Vector((0,0,1)) if abs(d.z)<.9 else Vector((0,1,0))
  u=d.cross(ref).normalized();v=d.cross(u).normalized()
  for j in range(sides):
   a=j*2*math.pi/sides;vs.append(tuple(p+radii[i]*(math.cos(a)*u+math.sin(a)*v*flatten)))
 for i in range(len(pts)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;fs.append((a,b,b+sides,a+sides))
 fs.append(tuple(range(sides-1,-1,-1)));fs.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
 shape.add(vs,fs,label)

def spear(shape,start,bend,tip,r0,r1,label,sides=6):
 # True apex, not a microscopic final capped ring.
 ps=[Vector(start),Vector(bend)];vs=[];fs=[]
 for i,p in enumerate(ps):
  d=(Vector(tip)-Vector(start)).normalized();u=d.cross(Vector((0,1,0))).normalized()
  if u.length<.1:u=d.cross(Vector((1,0,0))).normalized()
  v=d.cross(u).normalized();r=[r0,r1][i]
  for j in range(sides):vs.append(tuple(p+r*(math.cos(j*2*math.pi/sides)*u+math.sin(j*2*math.pi/sides)*v)))
 vs.append(tuple(tip))
 for j in range(sides):fs.extend([(j,(j+1)%sides,(j+1)%sides+sides,j+sides),(j+sides,(j+1)%sides+sides,2*sides)])
 fs.append(tuple(range(sides-1,-1,-1)));shape.add(vs,fs,label)

def loft(shape,sections,label,n=12):
 # Closed domed dorsal shell + shallow ventral arc, wide flat pleural edges.
 vs=[];fs=[]
 for y,w,z,h in sections:
  for j in range(n):
   a=2*math.pi*j/n;v=math.sin(a)
   vs.append((w*math.cos(a),y,z+h*(v if v>=0 else .30*v)))
 for i in range(len(sections)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;fs.append((a,b,b+n,a+n))
 fs.extend([tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))]);shape.add(vs,fs,label)

def oval(shape,center,radii,label,n=10,rings=4):
 # Ellipsoid with poles, no duplicated degenerate pole vertices.
 vs=[(center[0],center[1],center[2]-radii[2])];fs=[]
 for i in range(1,rings):
  p=-math.pi/2+math.pi*i/rings
  for j in range(n):a=2*math.pi*j/n;vs.append((center[0]+radii[0]*math.cos(p)*math.cos(a),center[1]+radii[1]*math.cos(p)*math.sin(a),center[2]+radii[2]*math.sin(p)))
 vs.append((center[0],center[1],center[2]+radii[2]));top=len(vs)-1
 for j in range(n):fs.append((0,1+(j+1)%n,1+j))
 for i in range(rings-2):
  for j in range(n):a=1+i*n+j;b=1+i*n+(j+1)%n;fs.append((a,b,b+n,a+n))
 for j in range(n):fs.append((top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n))
 shape.add(vs,fs,label)

def leaf(shape,start,tip,width,depth,label):
 # Solid paddle with tapering proximal pedicle. Section tube adapted along long axis.
 p=Vector(start);q=Vector(tip);d=q-p;pts=[p,p+d*.27,p+d*.64,q]
 tube(shape,pts,[.10,width*.85,width,.075],label,sides=6,flatten=depth/width)

# Cephalic shield with anterior ocular constrictions; eyes nest in these, never stalked.
head=Shape('cephalic-shield','carapace','Broad domed shield, anterolateral ocular notches, subhorizontal pleurae')
loft(head,[(-8,.38,2.0,.45),(-7.7,1.1,2.0,.78),(-7.25,1.65,2.0,1.10),(-6.8,1.40,2.0,1.28),(-6.3,2.20,2.0,1.36),(-5.2,2.85,1.95,1.38),(-3.65,3.04,1.9,1.1),(-3.05,2.25,1.85,.7)],'notched-domed-head',n=14);head.finish()
lab=Shape('labrum','armature','Restrained anterior labrum; no visible internal anatomy');oval(lab,(0,-7.92,1.9),(.55,.44,.38),'labrum',n=10);lab.finish()
for s,tag in [(-1,'L'),(1,'R')]:
 eye=Shape('notch-eye-'+tag,'eyes','Sessile lateral eye within shield notch; no peduncle');oval(eye,(s*1.54,-6.96,2.38),(.38,.36,.35),'sessile-eye',n=8);eye.finish()
# Trunk is exactly twelve articulated closed tergo-pleurae. Small overlap hides inner articulation.
ys=[];widths=[]
for i in range(12):
 y=-2.7+i*1.25;w=[2.70,2.90,3.02,2.94,2.76,2.58,2.36,2.12,1.84,1.54,1.23,.96][i];ys.append(y);widths.append(w)
 h=1.10-i*.042;z=1.79-i*.015
 shell=Shape(f'tergite-{i+1:02d}','armature' if i%2==0 else 'carapace',f'Trunk tergite {i+1} of exactly 12; '+('thoracic' if i<5 else 'postthoracic'))
 loft(shell,[(y-.48,w*.79,z,h*.76),(y-.16,w*.96,z,h*.98),(y+.51,w,z,h),(y+.83,w*.76,z,h*.72)],f'tergite-{i+1:02d}',n=10)
 # Lateral pleural spines branch from the shell, shortened posteriorly.
 for s in [-1,1]:
  spear(shell,(s*w*.82,y+.16,z+.04),(s*(w+.22),y+.61,z+.04),(s*(w+.48),y+1.03,z+.05),.18,.11,f'pleural-{i+1}-{s}',sides=5)
 shell.finish()
# Three paired tall dorsal projections (A); posterior levels low and swept, no B morph mounts.
dorsal=Shape('paired-dorsal-armature','ridge','First three paired projections dominate; posterior relief subdued, morph A only')
for i,(y,w) in enumerate(zip(ys,widths)):
 z=1.79-i*.015+(1.10-i*.042)*.91
 for s in [-1,1]:
  x=s*w*.36
  ht=[2.18,1.92,1.62][i] if i<3 else .42-.022*(i-3)
  sweep=[.08,.50,.78][i] if i<3 else .66
  spear(dorsal,(x,y+.18,z-.15),(x+s*.07,y+.27+sweep*.3,z+ht*.48),(x+s*.10,y+.29+sweep,z+ht),.24 if i<3 else .20,.12 if i<3 else .09,f'dorsal-pair-{i+1}-{s}',sides=5)
dorsal.finish()
# Sparse shield margin spines only; no blanket spiked spheres.
relief=Shape('head-margin-relief','armature','Sparse triangular marginal ornaments, deliberately simplified tiny tubercles')
for s in [-1,1]:
 for y,w in [(-5.95,2.37),(-5.30,2.78),(-4.6,2.96),(-3.9,3.03)]:spear(relief,(s*(w-.12),y,1.99),(s*(w+.10),y+.13,2.03),(s*(w+.34),y+.28,2.06),.15,.09,f'head-margin-{s}-{y}',5)
# Six short blunt tubercles retain the sparse head ornament required by the brief.
# They are rooted in the actual dome, not hovering spheres; microscopic density is not claimed.
for j,(x,y,z) in enumerate([(0,-5.55,3.25),(-.72,-5.02,3.22),(.72,-5.02,3.22),(-.70,-6.05,3.25),(.70,-6.05,3.25),(0,-4.28,3.12)]):
 oval(relief,(x,y,z),(.16,.19,.15),f'blunt-head-tubercle-{j+1}',n=6,rings=3)
relief.finish()
# Cephalic pair 1 reduced; no giant pincer.
fr=Shape('cephalic-pair-1-reduced','limbs','One reduced frontal pair; terminal shape uncertain and simplified')
for s in [-1,1]:tube(fr,[(s*.38,-7.25,1.76),(s*.55,-8.0,1.50),(s*.72,-8.43,1.65)],[.18,.13,.065],f'reduced-frontal-{s}',6)
fr.finish()
# Five gnathobasic units paired, growing posteriorward; raptorial ramus and thin dorsal exopod fan.
gn=Shape('cephalic-pairs-2-to-6-gnathobases','limbs','Five paired hypertrophied basipods, organized beneath shield, simplified tooth edges')
for s,tag in [(-1,'L'),(1,'R')]:
 rap=Shape('raptorial-fan-'+tag,'limbs','Five forward raptorial rami, seven visible shaft sections each; no fused giant chela')
 ex=Shape('cephalic-exopod-fan-'+tag,'paddles','Five slender segmented sensory-like branches; uncertain basal arrangement interpreted conservatively')
 for i in range(5):
  y=-6.9+i*.70;x=.60+i*.24
  # Root is below/buried in continuous shield. Basipod front arm remains connected.
  tube(gn,[(s*x,y,1.85),(s*(x+.165),(y+(-7.42+i*.10))/2,1.565),(s*(x+.33),-7.42+i*.10,1.28)],[.20+i*.025,.23+i*.023,.18+i*.022],f'gnathobase-pair-{i+2}-{tag}',5)
  start=Vector((s*(x+.33),-7.42+i*.10,1.28));end=Vector((s*(1.2+i*.75),-9.02+i*.12,1.30+i*.14))
  pts=[]
  for j in range(8):
   t=j/7;p=start.lerp(end,t);p.z+=.45*math.sin(math.pi*t);pts.append(tuple(p))
  tube(rap,pts,[.18-.014*j for j in range(8)],f'raptorial-pair-{i+2}-{tag}',6)
  # Tiny enditic rows reduced to two readable inboard teeth, not fictional density.
  for j in [3,5]:
   p=Vector(pts[j]);spear(rap,p,p+Vector((-s*.14,-.10,.10)),p+Vector((-s*.30,-.20,.16)),.095,.065,f'endite-{i}-{j}',5)
  start=Vector((s*(1.15+i*.19),-6.55+i*.36,2.02));end=Vector((s*(1.80+i*.88),-9.20+i*.63,2.10+i*.04));pts=[]
  for j in range(8):
   t=j/7;p=start.lerp(end,t);p.z+=.20*math.sin(math.pi*t);pts.append(tuple(p))
  tube(ex,pts,[.105-.005*j for j in range(8)],f'cephalic-exopod-{i+2}-{tag}',5)
 rap.finish();ex.finish()
gn.finish()
# Thoracic-like seventh cephalic pair and exactly five trunk walking pairs.
for s,tag in [(-1,'L'),(1,'R')]:
 legs=Shape('walking-endopods-'+tag,'limbs','Seventh cephalic pair plus five thoracic walking endopods; seven shaft sections including terminal claw')
 ep=Shape('thoracic-fringed-exopods-'+tag,'paddles','Six paddles: cephalic7 plus trunk1-5; thick tapered lamellar fringe, not alpha cards')
 for i in range(6):
  y=-3.55 if i==0 else ys[i-1];stretch=.72 if i==0 else 1 if i<4 else 1.1+(i-4)*.05
  root=Vector((s*1.25,y,1.90));knee=Vector((s*(3.1*stretch),y+.20,1.48));foot=Vector((s*(4.75*stretch),y+.56,.07))
  pts=[root,root.lerp(knee,.48),knee,knee.lerp(foot,.22),knee.lerp(foot,.48),knee.lerp(foot,.72),knee.lerp(foot,.9),foot]
  tube(legs,pts,[.30,.26,.22,.19,.16,.13,.10,.07],f'{"cephalic7" if i==0 else "thoracic"+str(i)}-{tag}',6)
  # Paddles extend posterior-laterally without making unattached petals.
  a=(s*1.42,y+.10,1.64);b=(s*(3.70*stretch),y+.72,1.10)
  leaf(ep,a,b,.43*stretch,.14,f'paddle-{i}-{tag}')
  # Two broad solid lamellar tips attached at edge of each paddle, intentionally simplified.
  for j in range(2):
   p=Vector(a).lerp(Vector(b),.49+j*.22);q=p+Vector((s*.32,.46,.0))
   leaf(ep,p,q,.12,.075,f'lamella-{i}-{j}-{tag}')
 legs.finish();ep.finish()
# Postthorax: seven smaller unornamented rounded paddles, no invented walking legs.
for s,tag in [(-1,'L'),(1,'R')]:
 post=Shape('postthoracic-paddles-'+tag,'paddles','Seven rounded exopods on trunk segments 6–12; posterior endopods not asserted')
 for i in range(5,12):
  y=ys[i];w=widths[i];sz=.66-(i-5)*.055 if i<11 else .22
  leaf(post,(s*w*.66,y+.15,1.60),(s*(w+.40),y+.60,1.15),sz,.20,f'postthoracic-{i+1}-{tag}')
 post.finish()
# Bipartite telson 15 + 5 mm: broad first 1/9 then narrow rod, separately articulated distal rod.
tail1=Shape('telson-proximal','carapace','Proximal telson, 15mm nominal, broad base and long gently concave rod')
loft(tail1,[(11.70,.72,1.63,.68),(12.45,.70,1.60,.55),(13.65,.24,1.55,.27),(17.5,.20,1.60,.22),(22.5,.16,1.85,.18),(27.0,.13,2.12,.15)],'proximal-telson',n=8)
for s in [-1,1]:
 for j,y in enumerate([12.6,13.4,15.1,17.0,19.1,21.4,23.8,25.5]):
  w=.48 if j==0 else .27 if j==1 else .19;z=1.57+max(0,y-17)*.055
  spear(tail1,(s*w,y,z),(s*(w+.12),y+.18,z),(s*(w+.27-j*.015),y+.35,z),.10,.065,f'telson-spine-{s}-{j}',5)
tail1.finish()
tail2=Shape('telson-distal','ridge','Distal articulated telson, 5mm nominal, about one-third proximal')
tube(tail2,[(0,26.96,2.12),(0,28.7,2.18),(0,30.8,2.23),(0,32,2.24)],[.15,.12,.09,.065],'distal-telson',sides=8,flatten=.7);tail2.finish()
# Center and ground by editing vertices, keeping ALL native transforms exactly identity.
allcoords=[v.co for o in collection.objects if o.type=='MESH' for v in o.data.vertices]
lo=[min(v[k] for v in allcoords) for k in range(3)];hi=[max(v[k] for v in allcoords) for k in range(3)]
offset=Vector((-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]))
for o in collection.objects:
 if o.type=='MESH':
  for v in o.data.vertices:v.co+=offset
  o.data.update()
scene['fact_boundary']='Morph A; trunk12=5+7. Family diagnosis 5+8 discrepancy retained in brief. Colors, depth, posture, microscopic setae interpretive.'
scene['generator_config_sha256']=hashlib.sha256((ROOT/'generator-config.json').read_bytes()).hexdigest()
audit=common.audit_source(collection,max_triangles=12000)
(DEST/'source-audit.json').write_text(json.dumps(audit,indent=2))
if audit['errors']:raise RuntimeError(audit['errors'])
record=common.export_asset('habelia-r001',{'en':'Habelia optata — Morph A','zh':'哈贝尔虫（A形态）'},'animals',collection,metadata={'asset_id':'habelia','revision':'r001','representation':'living-reconstruction','generator':'scripts/build_habelia.py','reconstruction_notes':C['scope']},output_root=DEST/'export',render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
for f in ['habelia-r001.glb','habelia-r001.blend','qa.json','metadata.json']:shutil.copy2(DEST/'export/habelia-r001'/f,DEST/f)
meta={'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256((ROOT/'generator-config.json').read_bytes()).hexdigest(),'seed':C['seed'],'graybox':GRAY,'offset_m':list(offset),'anatomical_counts':{'trunk_tergites':12,'cephalic_appendage_pairs':7,'walking_trunk_pairs':5,'postthoracic_paddles':7,'telson_parts':2,'tall_dorsal_projection_pairs':3},'mesh_count':len([o for o in collection.objects if o.type=='MESH']),'triangles':audit['triangles'],'materials':len(audit['materials'])}
(DEST/'build-metadata.json').write_text(json.dumps(meta,indent=2));print('BUILD_COMPLETE',meta,flush=True)
