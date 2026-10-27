# SPDX-License-Identifier: MIT
"""Original deterministic Alalcomenaeus geometry. No borrowed meshes or textures.
Run: blender -b -t 2 --factory-startup --python build_alalcomenaeus.py -- --config config.json --output-dir PATH [--gray]
All construction coordinates below are mm, converted once to meters. Every part
is a closed solid. Separate intersecting cuticular parts are intentional joints.
"""
import bpy, bmesh, json, math, sys, argparse, hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent))
import asset_common as ac

def args():
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--gray',action='store_true')
 return p.parse_args(sys.argv[sys.argv.index('--')+1:])
A=args();C=json.loads(A.config.read_text());OUT=A.output_dir.resolve();OUT.mkdir(parents=True,exist_ok=True)
coll=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[coll['asset_root']]
S=C['model_space_mm_to_m'];parts={};groups={};links=[];anatomy=[]
mats={k:ac.make_material('alalcomenaeus-'+k,'#929292' if A.gray else col) for k,col in C['palette'].items()}

def add(name,verts,faces,material,group):
 o=ac.mesh_object(name,[[a*S for a in v] for v in verts],faces,mats[material],coll)
 parts[name]=o;groups.setdefault(group,[]).append(o)
 vg=o.vertex_groups.new(name=name);vg.add(list(range(len(o.data.vertices))),1,'REPLACE')
 return name

def connect(child,parent,kind):links.append({'child':child,'parent':parent,'kind':kind})

def tube(name,points,radii,mat,group,n=6):
 points=[Vector(p) for p in points];verts=[]
 for i,p in enumerate(points):
  tangent=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
  axis=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0))
  u=tangent.cross(axis).normalized();v=tangent.cross(u).normalized()
  for j in range(n):verts.append(tuple(p+radii[i]*(u*math.cos(2*math.pi*j/n)+v*math.sin(2*math.pi*j/n))))
 faces=[tuple(reversed(range(n)))]
 for i in range(len(points)-1):
  for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 faces.append(tuple((len(points)-1)*n+j for j in range(n)))
 return add(name,verts,faces,mat,group)

def ellipsoid(name,center,radii,mat,group,n=10,rings=4):
 v=[(center[0],center[1],center[2]+radii[2])]
 for k in range(1,rings):
  t=math.pi*k/rings
  for j in range(n):
   a=2*math.pi*j/n;v.append((center[0]+radii[0]*math.sin(t)*math.cos(a),center[1]+radii[1]*math.sin(t)*math.sin(a),center[2]+radii[2]*math.cos(t)))
 v.append((center[0],center[1],center[2]-radii[2]));f=[]
 for j in range(n):f.append((0,1+j,1+(j+1)%n))
 for k in range(rings-2):
  for j in range(n):f.append((1+k*n+j,1+(k+1)*n+j,1+(k+1)*n+(j+1)%n,1+k*n+(j+1)%n))
 for j in range(n):f.append((len(v)-1,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
 return add(name,v,f,mat,group)

def loft(name,sections,mat,group,carina=True):
 # Closed transverse rings with paired dorsal carinae and enclosing flanks.
 # Each section: y, halfwidth, floor, roof. CCW outward repaired by common helper.
 verts=[]
 for y,w,lo,hi in sections:
  if carina:
   profile=[(0,hi-.28),(.35*w,hi+.35),(.64*w,hi-.30),(.94*w,hi-1.1),(w,lo+.8),(.83*w,lo), (0,lo-.2),(-.83*w,lo),(-w,lo+.8),(-.94*w,hi-1.1),(-.64*w,hi-.30),(-.35*w,hi+.35)]
  else:
   profile=[(0,hi),(.5*w,hi-.2),(.82*w,hi-.7),(w,(lo+hi)/2),(.8*w,lo+.1),(0,lo),(-.8*w,lo+.1),(-w,(lo+hi)/2),(-.82*w,hi-.7),(-.5*w,hi-.2)]
  verts.extend((x,y,z) for x,z in profile)
 n=len(profile);faces=[tuple(reversed(range(n)))]
 for k in range(len(sections)-1):
  for j in range(n):faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 faces.append(tuple((len(sections)-1)*n+j for j in range(n)))
 return add(name,verts,faces,mat,group)

def blade(name,polygon,z,thick,mat,group):
 # Solid flat blade: explicit top and bottom surfaces, not alpha cards.
 n=len(polygon);v=[(x,y,z-thick/2) for x,y in polygon]+[(x,y,z+thick/2) for x,y in polygon]
 f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]
 f += [(j,(j+1)%n,n+(j+1)%n,n+j) for j in range(n)]
 return add(name,v,f,mat,group)

head=loft('cephalic-shield',[(-21,2.3,5.4,7.9),(-19.4,4.5,4.9,9.1),(-15.2,6.1,4.5,9.6),(-11.1,5.85,4.4,9.0)],'shield','01-cephalic-shield',False)
segments=[]
for i in range(C['trunk_segments']):
 y=C['trunk_start_mm']+i*C['trunk_step_mm'];t=i/10;w=5.8-2.55*t*t;z=9.0-3.0*t*t
 name=loft(f'tergite-{i+1:02d}',[(y-1.54,w*.965,4.05-.65*t,z-.18),(y-.10,w,3.95-.65*t,z),(y+1.54,w*.98,3.95-.65*t,z-.15)],'tergites','02-eleven-tergites')
 segments.append(name);connect(name,head if i==0 else segments[i-1],'overlapping tergite articulation')
 anatomy.append({'type':'trunk-segment','index':i+1,'name':name,'center_mm':[0,y,6]})
# One spatulate telson: widening distally, rounded corners, visible straight rear edge.
telson=blade('single-spatulate-telson',[(-2.3,19.5),(-3.0,21.0),(-4.65,25.2),(-4.45,28.3),(-3.7,29),(3.7,29),(4.45,28.3),(4.65,25.2),(3.0,21.0),(2.3,19.5)],3.7,.85,'shield','03-telson-and-fringe')
connect(telson,segments[-1],'telson embeds last trunk segment')
for j in range(C['telson_fringe_elements']):
 x=-3.6+.9*j;end=31.5+.5*(1-abs(x)/3.6)
 nm=blade(f'telson-flat-spine-{j+1:02d}',[(x-.23,28.7),(x+.23,28.7),(x+.16,end),(x-.16,end)],3.7,.20,'fringe','03-telson-and-fringe')
 connect(nm,telson,'posterior planar telson fringe')
# Two lateral short-stalked eyes, plus understated selected three median ocelli.
for s,side in [(-1,'L'),(1,'R')]:
 stalk=tube(f'{side}-lateral-eye-stalk',[(s*3.2,-19.3,6.9),(s*4.4,-20.25,7.25),(s*4.9,-20.7,7.7)],[.52,.43,.40],'shield','04-eyes-and-stalks',8);connect(stalk,head,'lateral eye stalk to head')
 eye=ellipsoid(f'{side}-lateral-eye',(s*4.95,-20.8,7.8),(.80,.84,.72),'eyes','04-eyes-and-stalks',12,5);connect(eye,stalk,'eye to stalk')
for j,(x,y,z) in enumerate([(-.68,-20.45,8.15),(0,-20.7,8.05),(.68,-20.45,8.15)]):
 eye=ellipsoid(f'median-ocellus-{j+1:02d}-interpretive',(x,y,z),(.30,.32,.25),'eyes','04-eyes-and-stalks',8,4);connect(eye,head,'tiny median ocellus selected disputed interpretation')
# Compact great appendage base, three claw fingers continuing into six total flagella.
for s,side in [(-1,'L'),(1,'R')]:
 base=tube(f'{side}-great-appendage-base',[(s*2.6,-18.2,5.8),(s*2.8,-20.4,4.6),(s*3.1,-22.2,5.6)],[.86,.72,.61],'endopods','05-great-appendages',8);connect(base,head,'great appendage base to ventral head')
 for j in range(3):
  x=s*(2.8+.65*j);y=-22.0-.2*j;z=5.6+.45*j
  claw=tube(f'{side}-great-claw-{j+1}',[(s*3.1,-21.9,5.4),(x,y-.7,z+1.3),(x+s*.30,y-2.3,z+2.0),(x+s*.30,y-3.5,z+1.9)],[.43,.36,.25,.19],'endopods','05-great-appendages',6);connect(claw,base,'one of three flagellate fingers')
  flag=tube(f'{side}-flagellum-{j+1}',[(x+s*.30,y-3.3,z+1.9),(x+s*.45,y-5.8,z+1.3),(x+s*.6,y-8.2,z+.3),(x+s*.75,y-11.4,z-.3)],[.20,.17,.14,.12],'fringe','05-great-appendages',6);connect(flag,claw,'claw continuation to flagellum')
# Posterior cephalic + trunk biramous pairs: common basipod, inner jointed leg,
# lateral flap-like exopod and five broad stylized lamellae, all mapped.
limb_positions=[('cephalic-1',-16.0,5.5,head),('cephalic-2',-12.8,5.6,head)]+[(f'trunk-{i+1:02d}',C['trunk_start_mm']+i*C['trunk_step_mm'],5.5-2.3*(i/10)**2,segments[i]) for i in range(11)]
for k,(tag,y,w,parent) in enumerate(limb_positions):
 t=k/12;z=4.7-.7*t
 for s,side in [(-1,'L'),(1,'R')]:
  prefix=f'{side}-{tag}'
  basis=tube(prefix+'-basipod',[(s*2.0,y,z+.3),(s*(w-.3),y+.1,z-.3)],[.66,.57],'endopods','06-biramous-limb-bases',6);connect(basis,parent,'basipod to named segment ventrum')
  points=[(s*(w-.5),y,z-.1),(s*(w+.35),y+.35,z-1.2),(s*(w+1.1),y+1.2,z-2.0),(s*(w+.75),y+2.0,z-2.8),(s*(w+.1),y+2.8,.65+.25*t),(s*(w-.5),y+3.15,.45+.2*t)]
  endo=tube(prefix+'-endopod',points,[.53,.49,.41,.32,.24,.16],'endopods','07-jointed-endopods',6);connect(endo,basis,'inner walking branch originates at common basipod')
  # Sparse inward spines are interpretive simplifications, not setal counts.
  for q in [2,3]:
   a=points[q];b=(a[0]-s*.7,a[1]-.28,a[2]-.45)
   spin=tube(prefix+f'-endopod-spine-{q}',[a,b],[.19,.12],'fringe','07-jointed-endopods',5);connect(spin,endo,'restrained endopod spine')
  exo=tube(prefix+'-exopod-stalk',[(s*(w-.45),y,z),(s*(w+1.1),y+.9,z-.2)],[.46,.38],'paddles','08-exopods-and-lamellae',6);connect(exo,basis,'outer swimming branch originates at common basipod')
  # tilted long-axis paddle represented by a shallow solid rounded blade
  x=s*(w+1.6);pz=z-.3
  poly=[(x-s*.85,y+.5),(x+s*.45,y+.8),(x+s*1.0,y+2.25),(x+s*.65,y+4.2),(x-s*.25,y+4.5),(x-s*.7,y+2.6)]
  paddle=blade(prefix+'-exopod-paddle',poly,pz,.42,'paddles','08-exopods-and-lamellae');connect(paddle,exo,'flap to exopod stalk')
  for j in range(C['fringe_elements_per_paddle']):
   by=y+1.35+j*.59;bx=x+s*(.65 if j<4 else .4)
   lam=blade(prefix+f'-lamella-{j+1}',[(bx-s*.2,by-.13),(bx+s*.2,by-.13),(bx+s*1.25,by+.65),(bx+s*1.1,by+.86)],pz,.16,'fringe','08-exopods-and-lamellae');connect(lam,paddle,'solid simplified lamellar fringe')
  anatomy.append({'type':'biramous-limb','side':side,'segment':tag,'basipod':basis,'endopod':endo,'exopod':paddle,'parent':parent})
# Actual mesh boundary intersection / containment checks before joining.
bpy.context.view_layer.update()
def bvh(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],all_triangles=False,epsilon=0)
cache={n:bvh(o) for n,o in parts.items()}
def inside(p,tree):
 # parity ray; tiny deterministic off-axis avoids edge coincidences
 d=Vector((1,.137,.219)).normalized();pos=p.copy();count=0
 for _ in range(40):
  hit,normal,index,dist=tree.ray_cast(pos,d,1)
  if hit is None:break
  count+=1;pos=hit+d*1e-9
 return count%2==1
for link in links:
 a,b=link['child'],link['parent'];overlap=len(cache[a].overlap(cache[b]));contained=any(inside(parts[a].matrix_world@v.co,cache[b]) for v in parts[a].data.vertices)
 link.update({'boundary_intersection_pairs':overlap,'child_vertex_inside_parent':contained,'status':'PASS' if overlap or contained else 'FAIL'})
failed=[x for x in links if x['status']!='PASS']
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'exact source geometry BVH surface intersections or parity-contained child vertex; not only object names or bounding boxes','count':len(links),'failed':failed,'checks':links,'anatomy':anatomy,'nonadjacent_self_intersections':'NOT_EXHAUSTIVELY_TESTED; expected overlapping cuticle joints recorded'},indent=2))
if failed:raise RuntimeError('Anatomical mesh connections failed: '+repr(failed))
# Join by anatomical layer, retaining per-component vertex groups for editability.
for group,objects in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();o=objects[0];o.name=group
 o['anatomical_components']=[name for name,obj in parts.items() if obj in objects] if False else 'Preserved as named vertex groups'
# Bounds-center display datum, not environmental grounding claim.
offset=ac.ground_asset(coll,center_xy=True)
for o in coll.all_objects:
 if o.type=='MESH':
  bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
root['scientific_limits']=C['reconstruction_notes'];root['median_eyes_interpretation']='three tiny ocelli: selected1999/2023 interpretation, disputed, not consensus';root['representation']='living-reconstruction'
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
record=ac.export_asset(C['asset_id'],{'en':'Alalcomenaeus cambricus','zh':'阿拉尔柯美纳虫'},'arthropods',coll,metadata={'representation':'living-reconstruction','revision':C['revision'],'description':{'en':'Original low-poly Alalcomenaeus with eleven trunk segments, paired triflagellate appendages and a single spatulate telson.','zh':'原创低多边形复原：11躯干节、成对三指丝状前肢和单块铲形尾节。'},'reconstruction_notes':C['reconstruction_notes'],'origin_note':'Horizontal bounds centered; lowest exported surface Z0 display datum, not foot-ground or habitat assertion','generator':'scripts/build_alalcomenaeus.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'body_head_to_telson_m':.05},output_root=OUT,render=False,diagnostics=False)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'anatomical_components':len(parts),'anatomical_links':len(links),'mesh_groups':len(groups),'datum_offset_m':offset,'glb_sha256':record['sha256']['glb']},indent=2))
print('BUILD_COMPLETE',record['sha256']['glb'])
