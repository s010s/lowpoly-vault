#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Quetzalcoatlus lawsoni, standing folded-wing reconstruction.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output /path/build
No internet, another asset, or working-directory dependency. All dimensions metres.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
SRC=Path(__file__).resolve().parent
sys.path.insert(0,str(SRC/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene,make_material,mesh_object,export_asset
P=json.loads((SRC/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);a=a.parse_args(argv)
C=setup_scene(P['asset_id'],seed=P['seed'])
M=[make_material(k,v,roughness=.86) for k,v in P['palette_srgb'].items()]
# Accumulators retain semantic editable objects and named material slots.
class Part:
 def __init__(self,name): self.name=name;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mat=0):
  n=len(self.v);self.v.extend(v);self.f.extend([tuple(n+i for i in face) for face in f]);self.mi.extend([mat]*len(f))
 def tube(self,points,radii,sides=10,mat=0,ventral=False):
  v=[];f=[];m=[]
  for i,(p,r) in enumerate(zip(points,radii)):
   tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])
   tangent.normalize();u=Vector((1,0,0));u=(u-tangent*u.dot(tangent)).normalized();w=tangent.cross(u)
   rx,ry=r if isinstance(r,(tuple,list)) else (r,r)
   for j in range(sides):
    th=2*math.pi*j/sides;v.append(tuple(Vector(p)+u*math.cos(th)*rx+w*math.sin(th)*ry))
  f.append(tuple(reversed(range(sides))));m.append(mat)
  for i in range(len(points)-1):
   for j in range(sides):
    f.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    # Cross-section phase faces neck anterior side for z-dominant paths.
    m.append(1 if ventral and j in (6,7,8) else mat)
  f.append(tuple((len(points)-1)*sides+j for j in range(sides)));m.append(mat)
  off=len(self.v);self.v.extend(v);self.f.extend([tuple(off+j for j in x) for x in f]);self.mi.extend(m)
 def ellipsoid(self,p,scale,mat=0,sides=10,rings=6):
  v=[(p[0],p[1],p[2]+scale[2])]
  for r in range(1,rings):
   th=math.pi*r/rings
   for j in range(sides):
    ph=2*math.pi*j/sides;v.append((p[0]+scale[0]*math.sin(th)*math.cos(ph),p[1]+scale[1]*math.sin(th)*math.sin(ph),p[2]+scale[2]*math.cos(th)))
  v.append((p[0],p[1],p[2]-scale[2]));f=[]
  for j in range(sides):f.append((0,1+j,1+(j+1)%sides))
  for r in range(rings-2):
   for j in range(sides):
    q=1+r*sides;f.append((q+j,q+sides+j,q+sides+(j+1)%sides,q+(j+1)%sides))
  bot=len(v)-1;q=1+(rings-2)*sides
  for j in range(sides):f.append((q+j,bot,q+(j+1)%sides))
  self.add(v,f,mat)
 def finish(self):
  o=mesh_object(self.name,self.v,self.f,M,C)
  for poly,mi in zip(o.data.polygons,self.mi):poly.material_index=mi
  o['construction']='Original deterministic lofts and explicitly closed meshes; intentional overlapping anatomical attachments.'
  return o
body=Part('01-torso-neck-short-tail')
body.tube([(0,.37,1.00),(0,.29,1.04),(0,.13,1.055),(0,-.07,1.05),(0,-.23,1.07),(0,-.28,1.11)],[(.035,.055),(.105,.13),(.16,.19),(.17,.19),(.12,.15),(.075,.09)],12)
body.tube([(0,-.16,1.06),(0,-.25,1.16),(0,-.29,1.30),(0,-.32,1.46),(0,-.35,1.62),(0,-.385,1.78),(0,-.43,1.91),(0,-.48,1.99)],[(.105,.10),(.091,.09),(.072,.076),(.06,.064),(.054,.06),(.05,.058),(.047,.058),(.051,.062)],12,ventral=True)
body.tube([(0,.28,1.01),(0,.37,1.00),(0,.46,.985)],[(.048,.047),(.025,.025),(.004,.004)],8)
body.finish()
head=Part('02-long-toothless-head-and-mandible')
# Horizontal cranial/bill loft, flattened rhomboid sections, no fossil fenestra holes.
head.tube([(0,-.285,2.04),(0,-.38,2.05),(0,-.48,2.035),(0,-.60,2.015),(0,-.78,1.993),(0,-1.02,1.97),(0,-1.25,1.951),(0,-1.425,1.941)],[(.010,.02),(.055,.083),(.064,.073),(.054,.060),(.038,.046),(.023,.028),(.010,.013),(.0017,.0025)],10,2)
# Low rear cranial crest with tapered profile, not the lower image's upright crest.
head.add([(-.018,-.34,2.047),(.018,-.34,2.047),(-.009,-.27,2.145),(.009,-.27,2.145),(-.023,-.46,2.111),(.023,-.46,2.111)],[(0,4,2),(1,3,5),(0,1,5,4),(4,5,3,2),(2,3,1,0)],2)
# Closed mandible seam: narrow lip stripe embedded into head sides, not teeth.
head.tube([(0,-.41,1.989),(0,-.58,1.967),(0,-.80,1.955),(0,-1.05,1.944),(0,-1.34,1.938)],[(.051,.0045),(.046,.0034),(.033,.0028),(.018,.002),(.003,.001)],8,4)
head.finish()
face=Part('03-eyes-and-nares')
for s in (-1,1):
 face.ellipsoid((s*.061,-.463,2.052),(.010,.018,.016),4,10,5)
 face.ellipsoid((s*.041,-.70,2.019),(.003,.012,.005),4,8,4)
face.finish()
hind=Part('04-paired-hindlimbs-and-four-toed-feet')
fore=Part('05-paired-forelimbs-and-three-fingered-hands')
wing=Part('06-folded-wing-fingers')
mem=Part('07-folded-leathery-wing-membranes')
contact=[]
for s in (-1,1):
 # Hip, knee, ankle are a single tapered bent limb. Four toes are short and grounded.
 hind.tube([(s*.105,.18,1.015),(s*.16,.23,.83),(s*.215,.32,.57),(s*.218,.30,.40),(s*.21,.245,.095)],[(.072,.075),(.052,.055),(.031,.033),(.024,.026),(.019,.022)],9)
 hind.ellipsoid((s*.21,.23,.056),(.046,.067,.056),0,10,5)
 for j in range(4):
  x=s*(.21+(j-1.5)*.023);endY=.075+abs(j-1.5)*.018
  hind.tube([(s*.21,.23,.055),(x,.16,.025),(x,endY,.014)],[(.017,.018),(.013,.012),(.008,.009)],7)
  hind.tube([(x,endY+.008,.017),(x,endY-.026,.007),(x,endY-.037,.004)], [.009,.006,.0018],6,4)
 contact.append({'part':'hind-foot-'+str(s),'x':s*.21,'y':.17,'z':0.0})
 # Shoulder to elbow, radius/ulna, elongated metacarpal and grounded hand.
 fore.tube([(s*.14,-.14,1.09),(s*.205,-.10,.96),(s*.255,-.065,.82),(s*.305,-.22,.56),(s*.34,-.39,.30),(s*.35,-.47,.066)],[(.069,.067),(.049,.048),(.035,.038),(.026,.029),(.020,.023),(.022,.026)],9)
 fore.ellipsoid((s*.35,-.47,.042),(.041,.046,.042),0,10,5)
 for j in range(3):
  x=s*(.35+(j-1)*.028);ey=-.58+abs(j-1)*.015
  fore.tube([(s*.35,-.475,.046),(x,-.535,.020),(x,ey,.012)],[(.016,.018),(.011,.013),(.007,.008)],7)
  fore.tube([(x,ey,.014),(x,ey-.027,.005),(x,ey-.039,.003)], [.009,.0055,.0015],6,4)
 contact.append({'part':'wing-hand-'+str(s),'x':s*.35,'y':-.51,'z':0.0})
 # One fourth finger per side folded posterior/upward. Four segments, never bat fingers.
 finger=[(s*.37,-.459,.08),(s*.395,-.285,.285),(s*.405,-.09,.51),(s*.405,.06,.68),(s*.39,.15,.78)]
 wing.tube(finger,[(.020,.022),(.018,.020),(.014,.016),(.009,.011),(.0025,.003)],8)
 # Compact pleated membrane between arm, single finger and flank, not an outspread wing.
 # Closed double-sided thickness geometry, two gently ridged fans with original topology.
 outline=[(s*.20,-.10,1.025),(s*.265,-.065,.82),(s*.35,-.45,.085),(s*.399,-.285,.285),(s*.414,-.09,.51),(s*.410,.06,.68),(s*.390,.15,.78),(s*.255,.23,.84),(s*.20,.27,.49)]
 # Strip-like lower boundary folds back into flank; approximately 8 mm thickness.
 center=Vector((s*.31,-.055,.57));v=[tuple(center+Vector((s*.006,0,0)))]+outline+[tuple(center-Vector((s*.006,0,0)))]+[(x-s*.008,y,z) for x,y,z in outline]
 n=len(outline);f=[]
 for j in range(n):
  f.append((0,1+j,1+(j+1)%n));f.append((n+1,n+2+(j+1)%n,n+2+j));f.append((1+j,n+2+j,n+2+(j+1)%n,1+(j+1)%n))
 mem.add(v,f,3)
for p in (hind,fore,wing,mem):p.finish()
# Place the exact lowest toe vertices at the floor while preserving identity root.
low=min((o.matrix_world@v.co).z for o in C.objects if o.type=='MESH' for v in o.data.vertices)
for o in C.objects:
 if o.type=='MESH':
  for v in o.data.vertices:
   v.co.z-=low
   v.co.y+=.17
for c in contact:c['y']+=.17
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=export_asset(P['asset_id'],{'en':'Quetzalcoatlus','zh':'风神翼龙'},'pterosaurs',C,
 metadata={'description':{'en':'Original faceted Quetzalcoatlus lawsoni in an inferred four-contact folded-wing standing pose.','zh':'原创低多边形 Q. lawsoni 四点支撑折翼站姿重建。'},'generator':'source/generate.py','reconstruction_notes':P['reconstruction_notes'],'reference_unfolded_wingspan_m':4.5,'source_params_sha256':hashlib.sha256((SRC/'params.json').read_bytes()).hexdigest(),'runtime_profile':'static-palette-opaque'},
 output_root=a.output,render=False,max_triangles=6500,max_materials=6,max_primitives=12)
out=a.output/P['asset_id'];(out/'anatomical-landmarks.json').write_text(json.dumps({'forelimb_count':2,'hindlimb_count':2,'folded_fourth_fingers':2,'contacts':contact,'ground_shift_m':-low,'scale_note':'4.5 m describes estimated extended wingspan, never folded bounding width. Standing bounds and soft tissues are artistic, not measured holotype.'},indent=2)+'\n')
print('BUILD_COMPLETE',json.dumps(record))
