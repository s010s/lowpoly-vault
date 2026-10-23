# SPDX-License-Identifier: MIT
"""Original deterministic Kentrosaurus reconstruction. Blender --background --python generate.py -- --output-dir DIR.
Only this file, params.json and declared deps are needed. All coordinates are metres.
Six anterior plate pairs and six posterior spike pairs are an artistic arrangement;
shoulder lateral spines follow the reference mount, not demonstrated life-position.
"""
from pathlib import Path
import argparse, sys, json, math, shutil
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
P=json.loads((HERE/'params.json').read_text())
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args(args)
out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
C=setup_scene('kentrosaurus',P['seed'])
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
M={k:make_material('kentro-'+k,v,roughness=.88 if k!='eye' else .55) for k,v in P['palette'].items()}

class Group:
 def __init__(self,name,mats): self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[];self.parts=[]
 def add(self,name,verts,faces,indices=0):
  st=len(self.v);self.v.extend([tuple(v) for v in verts]);self.f.extend([tuple(i+st for i in f) for f in faces]);self.mi.extend(indices if isinstance(indices,list) else [indices]*len(faces));self.parts.append((name,st,len(self.v)))
 def finish(self):
  ob=mesh_object(self.name,self.v,self.f,[M[k] for k in self.mats],C)
  for f,i in zip(ob.data.polygons,self.mi):f.material_index=i
  for name,lo,hi in self.parts:ob.vertex_groups.new(name=name).add(list(range(lo,hi)),1,'REPLACE')
  ob['editing']='Named vertex groups isolate closed semantic parts; select linked for individual components.'
  return ob
skin=Group('Body-neck-tail-limbs',['skin','dorsal','underside'])
armour=Group('Paired-plates-and-spines',['armour','horn'])
detail=Group('Eyes-and-mouth',['eye'])

# A single profile loft from small skull through neck, arched trunk and long tail.
# Stations: Y, Z centre, lateral radius, vertical radius.
body=[(-1.93,.835,.055,.046),(-1.87,.852,.080,.065),(-1.76,.881,.118,.089),(-1.65,.904,.132,.100),(-1.54,.925,.107,.091),(-1.40,.979,.127,.118),(-1.23,1.046,.186,.166),(-1.04,1.091,.294,.255),(-.81,1.115,.388,.350),(-.48,1.143,.480,.412),(-.12,1.169,.526,.443),(.23,1.190,.512,.448),(.52,1.217,.451,.418),(.76,1.235,.344,.329),(.96,1.226,.258,.246),(1.19,1.212,.202,.192),(1.43,1.186,.160,.152),(1.70,1.157,.125,.119),(1.98,1.128,.093,.089),(2.25,1.105,.065,.063),(2.51,1.094,.041,.041),(2.76,1.096,.023,.025),(2.94,1.108,.012,.014),(3.07,1.125,.0035,.005)]
N=16;verts=[];faces=[];mats=[]
for y,z,rx,rz in body:
 for j in range(N):
  t=2*math.pi*j/N
  verts.append((rx*math.cos(t),y,z+rz*math.sin(t)))
faces.append(tuple(range(N-1,-1,-1)));mats.append(0)
for i in range(len(body)-1):
 for j in range(N):
  faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
  s=math.sin(2*math.pi*(j+.5)/N)
  mats.append(1 if s>.70 else 2 if s<-.54 else 0)
faces.append(tuple((len(body)-1)*N+j for j in range(N)));mats.append(0)
skin.add('Continuous skull-neck-trunk-tail',verts,faces,mats)

def vertical_loft(group,name,stations,n=10,material=0):
 vs=[];fs=[]
 for x,y,z,rx,ry in stations:
  for j in range(n):
   t=2*math.pi*j/n;vs.append((x+rx*math.cos(t),y+ry*math.sin(t),z))
 fs.append(tuple(range(n-1,-1,-1)))
 for i in range(len(stations)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 fs.append(tuple((len(stations)-1)*n+j for j in range(n)))
 group.add(name,vs,fs,material)

def tube(group,name,centers,radii,n=8,base_mat=0,tip_mat=None,flatten=1.):
 centers=[Vector(c) for c in centers];vs=[];fs=[];mi=[]
 for i,(c,r) in enumerate(zip(centers[:-1],radii[:-1])):
  tangent=(centers[min(i+1,len(centers)-1)]-centers[max(i-1,0)]).normalized()
  u=tangent.cross(Vector((0,1,0)))
  if u.length<.01:u=tangent.cross(Vector((1,0,0)))
  u.normalize();v=tangent.cross(u).normalized()
  for j in range(n):
   t=2*math.pi*j/n;vs.append(c+u*(r*math.cos(t))+v*(r*flatten*math.sin(t)))
 fs.append(tuple(range(n-1,-1,-1)));mi.append(base_mat)
 rings=len(centers)-1
 for i in range(rings-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j));mi.append(tip_mat if tip_mat is not None and i>=rings-2 else base_mat)
 tip=len(vs);vs.append(centers[-1])
 for j in range(n):fs.append(((rings-1)*n+j,(rings-1)*n+(j+1)%n,tip));mi.append(tip_mat if tip_mat is not None else base_mat)
 group.add(name,vs,fs,mi)

for sign,side in [(1,'left'),(-1,'right')]:
 # Forelegs: robust proximal arm, slightly back-directed elbow, more forward wrist.
 vertical_loft(skin,side+' foreleg',[(sign*.30,-.75,1.16,.16,.18),(sign*.37,-.71,.92,.145,.145),(sign*.41,-.59,.62,.106,.112),(sign*.43,-.66,.36,.084,.087),(sign*.44,-.70,.13,.078,.088)],10)
 vertical_loft(skin,side+' forefoot',[(sign*.44,-.72,0,.115,.145),(sign*.44,-.72,.055,.127,.152),(sign*.44,-.70,.16,.090,.101),(sign*.435,-.695,.21,.075,.080)],10)
 # Hindlegs: large high haunch merging into trunk, knee forward, ankle behind.
 vertical_loft(skin,side+' hindleg',[(sign*.30,.57,1.44,.205,.25),(sign*.42,.56,1.19,.217,.249),(sign*.47,.40,.91,.170,.177),(sign*.49,.50,.62,.122,.123),(sign*.50,.74,.30,.086,.093),(sign*.50,.73,.13,.091,.095)],12)
 vertical_loft(skin,side+' hindfoot',[(sign*.50,.69,0,.149,.20),(sign*.50,.69,.054,.16,.201),(sign*.50,.715,.15,.110,.13),(sign*.50,.73,.20,.087,.096)],12)
 # Compact keratin tips: forefeet have two visible tips; hindfeet three blunt toes.
 for label,fx,fy,num,span in [('fore',.44,-.84,2,.062),('hind',.50,.52,3,.083)]:
  for j in range(num):
   x=sign*(fx+(j-(num-1)/2)*span)
   vertical_loft(armour,f'{side} {label} toe tip {j+1}',[(x,fy,.018,.036,.054),(x,fy-.006,.065,.042,.062),(x,fy+.015,.10,.025,.030)],8,1)

# Closed, thin polygonal plates, wider in YZ than in transverse X; outer face has a subtle ridge.
def plate(name,sign,y,base_z,x,height,width):
 outline=[(-.50,0),(-.66,.26),(-.39,.67),(.12,1),(.61,.59),(.51,.14),(.34,0)]
 vs=[]
 for layer in [-1,1]:
  for py,pz in outline:
   vs.append((sign*(x+.15*height*pz)+layer*.022*(1-.70*pz),y+py*width,base_z+pz*height))
 n=len(outline);fs=[]
 # Fan each broad face to a deliberate central ridge rather than a flat n-gon.
 for layer in range(2):
  mid=len(vs);vs.append((sign*(x+.075*height)+(1 if layer else -1)*.038,y,base_z+.43*height))
  for j in range(n):fs.append((layer*n+j,layer*n+(j+1)%n,mid))
 for j in range(n):fs.append((j,(j+1)%n,n+(j+1)%n,n+j))
 armour.add(name,vs,fs,0)
plates=[(-1.39,1.068,.060,.13,.14),(-1.13,1.237,.085,.21,.19),(-.88,1.398,.115,.29,.25),(-.58,1.514,.145,.36,.30),(-.25,1.560,.160,.39,.32),(.08,1.582,.160,.41,.31)]
for i,(y,z,x,h,w) in enumerate(plates):
 for sign,side in [(1,'left'),(-1,'right')]:plate(f'{side} anterior plate {i+1}',sign,y,z,x,h,w)

# Posterior armour progressively changes from a stout dorsal blade to slender tail spines.
spikes=[(.43,1.584,.16,.55,.11,.095),(.80,1.472,.16,.64,.24,.09),(1.19,1.351,.14,.70,.38,.080),(1.64,1.239,.10,.61,.50,.070),(2.10,1.175,.073,.48,.57,.061),(2.55,1.124,.037,.30,.55,.050)]
for i,(y,z,x,h,spread,r) in enumerate(spikes):
 for s,side in [(1,'left'),(-1,'right')]:
  base=Vector((s*x,y,z));tip=Vector((s*(x+spread),y+.24,z+h))
  d=tip-base
  centers=[base,base+d*.25+Vector((0,-.018,.018)),base+d*.58+Vector((0,-.020,.025)),base+d*.83,tip]
  tube(armour,f'{side} posterior spine {i+1}',centers,[r,r*.78,r*.43,r*.18,0],8,0,1,flatten=.72)
 # Shoulder spikes have an explicitly uncertain anatomical location.
for s,side in [(1,'left'),(-1,'right')]:
 b=Vector((s*.315,-.79,1.175));t=Vector((s*1.09,-.51,1.57));d=t-b
 tube(armour,side+' interpretative shoulder spine',[b,b+d*.22,b+d*.55,b+d*.82,t],[.115,.09,.055,.025,0],10,0,1,flatten=.7)

# Small lateral eyes and jaw seam. No invented giant eye or teeth display.
for s,side in [(1,'left'),(-1,'right')]:
 vertical_loft(detail,side+' eye',[(s*.117,-1.718,.924,.012,.021),(s*.131,-1.718,.943,.016,.023),(s*.119,-1.718,.960,.009,.014)],10)
 tube(detail,side+' closed jaw line',[(s*.054,-1.922,.821),(s*.082,-1.86,.817),(s*.118,-1.74,.824),(s*.117,-1.665,.844)],[.004,.004,.004,0],5)
 tube(armour,side+' beak edge',[(s*.047,-1.932,.836),(s*.067,-1.89,.849),(s*.070,-1.866,.854)],[.009,.007,0],6,1)
for g in [skin,armour,detail]:g.finish()
root=bpy.data.objects[C['asset_root']]
root['reconstruction_note']='Shoulder spines, exact armour count, colours and keratin are interpretations. Reference mount is composite, not an articulated whole fossil.'
root['scale_note']='5.0 m genus-scale estimate, not the length of the photographed femur specimen or mount.'
record=export_asset('kentrosaurus',{'en':'Kentrosaurus','zh':'钉状龙'},'animals',C,
 metadata={'generator':'source/generate.py','revision':'r001','description':{'en':'Original stylized whole Kentrosaurus, with small anterior plates transitioning to long posterior and tail spines.','zh':'原创钉状龙全身复原，前部小背板逐步转为后部与尾部长刺。'},'reconstruction_notes':['Composite mount reference; not an in-situ articulated fossil.','Lateral shoulder placement is disputed and treated as interpretation.','5 m is a genus scale estimate.'],'sources':['https://dinosaurpalaeo.wordpress.com/2014/06/10/a-digital-dino-bone/']},
 output_root=out/'work',render=False,max_triangles=P['max_triangles'],max_materials=P['max_materials'],max_primitives=P['max_primitives'])
s=out/'work/kentrosaurus'
for old,new in [('kentrosaurus.glb','model.glb'),('kentrosaurus.blend','model.blend'),('qa.json','source-export.json'),('metadata.json','build-metadata.json')]:shutil.copy2(s/old,out/new)
assert (out/'model.glb').stat().st_size<=P['max_glb_bytes']
print(json.dumps({'complete':True,'triangles':record['triangles'],'bytes':record['glb_bytes'],'out':str(out)}))
