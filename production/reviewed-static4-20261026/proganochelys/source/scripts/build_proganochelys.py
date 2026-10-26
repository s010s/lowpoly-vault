# SPDX-License-Identifier: MIT
"""Original reference-led stem turtle. Editable authored lofts; no imported geometry."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).parent));import asset_common as ac
P=argparse.ArgumentParser();P.add_argument('--config',type=Path,required=True);P.add_argument('--output-dir',type=Path,required=True);P.add_argument('--gray',action='store_true')
A=P.parse_args(sys.argv[sys.argv.index('--')+1:]);C=json.loads(A.config.read_text());OUT=A.output_dir;OUT.mkdir(exist_ok=True,parents=True)
assert bpy.app.version_string==C['blender_version']
COL=ac.setup_scene(C['asset_id'],C['seed']);root=bpy.data.objects[C['asset_id']]
bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
M={k:ac.make_material(k,'#929292' if A.gray else v,roughness=.87,double_sided=False) for k,v in C['palette'].items()}
RAW=bpy.data.collections.new('ANATOMY_LOFTS_EDITABLE_NOT_EXPORTED');bpy.context.scene.collection.children.link(RAW)
raw=[];parts={};links=[];foot_specs=[]
def mesh(name,v,f,collection,material=None):
 o=ac.mesh_object(name,v,f,material or M['skin'],collection)
 if collection==RAW:o.parent=None;raw.append(o)
 else:parts[name]=o
 return o

def loft_y(name,stations,n=20,power=1):
 v=[];f=[]
 for y,x,b,t,w in stations:
  for j in range(n):
   a=2*math.pi*j/n;c,s=math.cos(a),math.sin(a);v.append((x+w*math.copysign(abs(c)**power,c),y,(b+t)/2+(t-b)/2*math.copysign(abs(s)**power,s)))
 for i in range(len(stations)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 for i,rev in [(0,True),(len(stations)-1,False)]:
  y,x,b,t,w=stations[i];ci=len(v);v.append((x,y,(b+t)/2))
  for j in range(n):
   q=(ci,i*n+j,i*n+(j+1)%n);f.append(q[::-1] if rev else q)
 return mesh(name,v,f,RAW)

def tube(name,stations,n=12,collection=RAW,material=None):
 v=[];f=[]
 for i,(p,w,d) in enumerate(stations):
  p=Vector(p);t=(Vector(stations[min(i+1,len(stations)-1)][0])-Vector(stations[max(i-1,0)][0])).normalized();ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0));u=t.cross(ref).normalized();q=t.cross(u).normalized()
  for j in range(n):a=2*math.pi*j/n;v.append(tuple(p+u*w*math.cos(a)+q*d*math.sin(a)))
 for i in range(len(stations)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 for i,rev in [(0,True),(len(stations)-1,False)]:
  ci=len(v);v.append(tuple(stations[i][0]))
  for j in range(n):
   z=(ci,i*n+j,i*n+(j+1)%n);f.append(z[::-1] if rev else z)
 return mesh(name,v,f,collection,material)

def canonical(o):
 old=o.data;coords=[tuple(float(x) for x in v.co) for v in old.vertices];ordered=sorted(set(coords));lut={c:i for i,c in enumerate(ordered)};ix=[lut[c] for c in coords];faces=[]
 for p in old.polygons:
  f=tuple(ix[i] for i in p.vertices);f=min(f[k:]+f[:k] for k in range(len(f)));faces.append((p.material_index,f))
 faces.sort();new=bpy.data.meshes.new(old.name+'-canonical');new.from_pydata(ordered,[],[f for m,f in faces]);new.update()
 for m in old.materials:new.materials.append(m)
 for p,(m,f) in zip(new.polygons,faces):p.material_index=m;p.use_smooth=False
 o.data=new
 if old.users==0:bpy.data.meshes.remove(old)

# Body under shell, short nonretracted armored neck, small blunt head, substantial tail.
loft_y('Editable living trunk beneath complete shell',[(-.245,0,.115,.194,.070),(-.21,0,.105,.224,.120),(-.14,0,.105,.243,.172),(0,0,.104,.250,.185),(.14,0,.105,.238,.170),(.21,0,.112,.215,.115),(.255,0,.122,.185,.058)],24)
loft_y('Editable short extended neck',[(-.37,0,.170,.224,.034),(-.34,0,.150,.221,.038),(-.30,0,.139,.217,.044),(-.26,0,.135,.214,.055),(-.225,0,.133,.212,.067)],20)
loft_y('Editable modest turtle skull and beak',[(-.445,0,.182,.214,.016),(-.433,0,.172,.227,.028),(-.408,0,.169,.244,.039),(-.383,0,.169,.252,.046),(-.358,0,.170,.244,.040),(-.34,0,.174,.226,.029)],24,power=.86)
loft_y('Editable armored tail core and moderate distal club',[(.225,0,.121,.187,.044),(.26,0,.116,.177,.041),(.30,.004,.108,.161,.035),(.34,.012,.099,.147,.030),(.38,.024,.092,.135,.025),(.415,.039,.087,.125,.022),(.45,.054,.086,.137,.031),(.48,.064,.088,.132,.028),(.505,.067,.099,.117,.013),(.516,.067,.105,.111,.004)],18)
for s in [-1,1]:
 tag='L' if s<0 else 'R'
 tube('Editable short bent forelimb '+tag,[((s*.112,-.193,.170),.036,.038),((s*.171,-.213,.143),.035,.035),((s*.228,-.184,.101),.027,.029),((s*.243,-.226,.053),.022,.025),((s*.240,-.255,.025),.019,.022)],14)
 tube('Editable short bent hindlimb '+tag,[((s*.100,.185,.155),.041,.038),((s*.163,.198,.122),.038,.035),((s*.212,.168,.086),.029,.029),((s*.231,.211,.048),.022,.023),((s*.232,.229,.023),.018,.021)],14)
 for limb,px,py,scale in [('fore',s*.240,-.270,1.),('hind',s*.232,.223,.95)]:
  loft_y('Editable '+limb+' palm '+tag,[(py-.025*scale,px,.005,.028,.023*scale),(py,px,.004,.040,.034*scale),(py+.027*scale,px,.008,.032,.024*scale)],16)
  for digit,(dx,dy) in enumerate([(-.029,-.029),(-.015,-.042),(0,-.049),(.016,-.041),(.030,-.028)],1):
   dx*=scale;dy*=scale;r=.0075*scale
   start=(px+s*dx*.58,py-.010,.021);middle=(px+s*dx*.88,py+dy*.75,.013);end=(px+s*dx,py+dy,.010)
   tube(f'Editable {limb} {tag} digit {digit}',[(start,r*1.25,r*1.05),(middle,r,r*.85),(end,r*.80,r*.70)],10)
   direction=Vector((s*dx*.17,dy*.30,0)).normalized();foot_specs.append({'limb':limb,'side':tag,'digit':digit,'root':end,'direction':tuple(direction),'radius':r,'claw_length_m':.013})
# Voxel-union copies, retaining the original semantic lofts for editing.
for o in raw:o.hide_render=True;o.hide_set(True)
bpy.ops.object.select_all(action='DESELECT')
for o in raw:
 d=o.copy();d.data=o.data.copy();COL.objects.link(d);d.hide_render=False;d.hide_set(False);d.select_set(True)
bpy.context.view_layer.objects.active=d;bpy.ops.object.join();body=bpy.context.object;body.name='continuous-living-head-neck-trunk-four-limbs-20-digits-tail';body.parent=root
rem=body.modifiers.new('Original loft union 3mm','REMESH');rem.mode='VOXEL';rem.voxel_size=C['voxel_size_m'];rem.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=rem.name);canonical(body)
sm=body.modifiers.new('Anatomical transitions','SMOOTH');sm.factor=.50;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
body.data.calc_loop_triangles();initial=len(body.data.loop_triangles);dec=body.modifiers.new('Low polygon planes','DECIMATE');dec.ratio=min(1,C['target_body_triangles']/initial);dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name);canonical(body)
for v in body.data.vertices:
 if v.co.z<.007:v.co.z=0
body.data.update();body.data.materials.clear();body.data.materials.append(M['skin']);body.data.materials.append(M['beak_claws'])
for p in body.data.polygons:p.material_index=0;p.use_smooth=False
parts[body.name]=body
for name,pred in [('head',lambda v:v.y<-.34),('neck',lambda v:-.34<=v.y<-.25),('trunk',lambda v:abs(v.y)<.25 and abs(v.x)<.18),('tail',lambda v:v.y>.25 and abs(v.x)<.1),('feet',lambda v:v.z<.05),('left_limbs',lambda v:v.x<-.18),('right_limbs',lambda v:v.x>.18)]:
 ids=[v.index for v in body.data.vertices if pred(v.co)]
 if ids:body.vertex_groups.new(name=name).add(ids,1,'REPLACE')

# Custom continuous carapace heightfield. Six stylized central/lateral scute regions, twelve marginal pairs; counts not specimen-exact.
ys=[-.275,-.245,-.205,-.155,-.10,-.05,0,.05,.10,.155,.205,.245,.275]
width=[.065,.145,.184,.202,.210,.214,.215,.214,.210,.202,.184,.145,.065]
xs=[-1,-.86,-.34,.34,.86,1]
def hz(x,y):
 # Local plan width avoids a high vertical slab around narrow front/rear corners.
 iy=next((i for i in range(len(ys)-1) if ys[i]<=y<=ys[i+1]),0 if y<ys[0] else len(ys)-2)
 t=max(0,min(1,(y-ys[iy])/(ys[iy+1]-ys[iy])));w=width[iy]*(1-t)+width[iy+1]*t
 return .163+.172*max(0,1-(x/w)**2)**.82*max(.25,1-(y/.305)**2)**.48
v=[];f=[];mi=[];lookup={}
def at(ix,iy):
 key=(ix,iy)
 if key not in lookup:
  sx=xs[ix]+(math.copysign(.075,xs[ix]) if ix in [2,3] and iy%2 else 0)
  x=sx*width[iy];y=ys[iy];z=hz(x,y)-.0025
  if ix in [0,5]:z=.161+.005*math.cos(iy*math.pi)
  lookup[key]=len(v);v.append((x,y,z))
 return lookup[key]
# Main scutes span two rows; margins are individual, with shared midpoint vertices.
for lane in range(5):
 spans=[(i,i+1) for i in range(12)] if lane in [0,4] else [(i,i+2) for i in range(0,12,2)]
 for a,b in spans:
  border=[at(lane,a)]+[at(lane+1,j) for j in range(a,b+1)]+[at(lane,j) for j in range(b,a,-1)]
  center=sum((Vector(v[i]) for i in border),Vector())/len(border);inner=[]
  for old in border:
   p=Vector(v[old]);p=center+(p-center)*.87;p.z=hz(p.x,p.y)+(.001 if lane in [1,2,3] else -.005)
   inner.append(len(v));v.append(tuple(p))
  ci=len(v);v.append((center.x,center.y,hz(center.x,center.y)+.002))
  for j in range(len(border)):
   k=(j+1)%len(border);f.append((border[j],border[k],inner[k],inner[j]));mi.append(2 if lane in [0,4] else (0 if lane==2 else 1));f.append((inner[j],inner[k],ci));mi.append(2 if lane in [0,4] else (0 if lane==2 else 1))
# Fix triangulation BEFORE shell duplication; otherwise reverse-wound nonplanar quads may pick different diagonals.
tri=[];tm=[]
for face,m in zip(f,mi):
 for j in range(1,len(face)-1):tri.append((face[0],face[j],face[j+1]));tm.append(m)
f=tri;mi=tm
N=len(v);top_faces=list(f);top_mi=list(mi)
# Inner carapace follows the curved dorsal shell, not a flat cosmetic floor.
v.extend((x,y,z-.018) for x,y,z in list(v));f.extend(tuple(i+N for i in face[::-1]) for face in top_faces);mi.extend(top_mi)
from collections import Counter
edges=Counter(tuple(sorted((p[i],p[(i+1)%len(p)]))) for p in top_faces for i in range(len(p)))
for (a,b),n in edges.items():
 if n==1:f.append((a,b,b+N,a+N));mi.append(2)
shell=mesh('moderately-domed-carapace-sculpted-scutes',v,f,COL,[M['carapace'],M['scute'],M['margin']])
for p,m in zip(shell.data.polygons,mi):p.material_index=m
shell['anatomy']='Continuous thick curved carapace; keratin-scute styling not underlying bone map; no texture.'
links.append({'child':shell.name,'parent':body.name,'purpose':'Carapace lower sides physically overlap living trunk; nonfloating solid roof.'})
# Complete butterfly/hourglass plastron, including rising lateral bridges in SAME manifold.
pys=[-.250,-.214,-.178,-.127,0,.127,.178,.214,.250];pws=[.065,.073,.101,.199,.207,.199,.101,.073,.065];pxs=[-1,-.78,-.4,0,.4,.78,1];pv=[];pf=[]
for y,w in zip(pys,pws):
 for s in pxs:
  x=s*w;rise=.057*max(0,(abs(x)-.145)/.062)**1.25
  # Modest anterior gular/extragular projections; exact living edge artistic.
  yy=y-(.022*(1-abs(abs(s)-.4)) if y==pys[0] else 0)
  pv.append((x,yy,.119+rise))
for iy in range(len(pys)-1):
 for ix in range(len(pxs)-1):a=iy*len(pxs)+ix;pf.append((a,a+1,a+1+len(pxs),a+len(pxs)))
pf=[(face[0],face[j],face[j+1]) for face in pf for j in range(1,len(face)-1)]
PN=len(pv);top=list(pf);pv.extend((x,y,z-.019) for x,y,z in list(pv));pf.extend(tuple(i+PN for i in face[::-1]) for face in top)
edges=Counter(tuple(sorted((p[i],p[(i+1)%len(p)]))) for p in top for i in range(len(p)))
for (a,b),n in edges.items():
 if n==1:pf.append((a,b,b+PN,a+PN))
plastron=mesh('complete-shaped-plastron-with-integral-left-right-bridges',pv,pf,COL,M['plastron'])
links.extend([{'child':plastron.name,'parent':shell.name,'purpose':'Left/right rising bridges physically overlap carapace lateral rim.'},{'child':plastron.name,'parent':body.name,'purpose':'Continuous shaped lower shell covers belly with front/rear limb notches, not cosmetic flat cap.'}])

def ellipsoid(name,c,r,mat,n=12,rings=6):
 v=[(c[0],c[1],c[2]+r[2])];f=[]
 for i in range(1,rings):
  a=math.pi*i/rings
  for j in range(n):b=2*math.pi*j/n;v.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
 v.append((c[0],c[1],c[2]-r[2]))
 for j in range(n):f.append((0,1+j,1+(j+1)%n))
 for i in range(rings-2):
  for j in range(n):f.append((1+i*n+j,1+(i+1)*n+j,1+(i+1)*n+(j+1)%n,1+i*n+(j+1)%n))
 for j in range(n):f.append((len(v)-1,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
 return mesh(name,v,f,COL,M[mat])
# Closed low wedge osteoderms: broad base sunk into exact ray-landed skin, no floating spikes.
def armor(name,start,direction,length,width,depth):
 p=Vector(start);d=Vector(direction).normalized()
 o=tube(name,[(tuple(p-d*.007),width,depth),(tuple(p+d*length*.4),width*.72,depth*.75),(tuple(p+d*length),width*.12,depth*.12)],8,COL,M['armor'])
 links.append({'child':o.name,'parent':body.name,'purpose':'Osteoderm base penetrates living skin; modest art-chosen keratin height, not exact preserved count.'});return o
for s in [-1,1]:
 tag='L' if s<0 else 'R'
 hit,co,no,index=body.ray_cast(Vector((s*.15,-.390,.224)),Vector((-s,0,0)));assert hit
 eye=ellipsoid('small-lateral-eye-'+tag,(co.x-s*.0014,-.390,.224),(.0044,.0071,.0064),'eye');links.append({'child':eye.name,'parent':body.name,'purpose':'Small shallow lateral eye embedded in living head; no emissive or detached bead.'})
 for i,y in enumerate([-.342,-.309,-.277]):
  z=.198;hit,co,no,index=body.ray_cast(Vector((s*.15,y,z)),Vector((-s,0,0)));assert hit
  armor(f'neck-osteoderm-{tag}-{i+1}',tuple(co),(s*.78,.1,.62),.034-i*.002,.018,.012)
 for limb,x,y,z in [('fore',s*.222,-.200,.112),('hind',s*.204,.186,.100)]:
  hit,co,no,index=body.ray_cast(Vector((x,y,.3)),Vector((0,0,-1)));assert hit
  armor(f'{limb}-low-limb-armor-{tag}',tuple(co),(s*.45,0,.9),.014,.024,.017)
# Successive tail groups with modest paired outward ridges; final distal club is integrated core.
for i,(y,x,z) in enumerate([(.275,.001,.151),(.310,.006,.138),(.347,.014,.125),(.385,.026,.115),(.425,.043,.109),(.463,.059,.110)]):
 hit,co,no,index=body.ray_cast(Vector((x,y,.3)),Vector((0,0,-1)));assert hit
 armor(f'tail-dorsal-osteoderm-group-{i+1}',tuple(co),(0,-.15,.99),.018-i*.0010,.028-i*.0018,.016-i*.001)
for spec in foot_specs:
 p=Vector(spec['root']);d=Vector(spec['direction']);length=spec['claw_length_m'];r=spec['radius']
 claw=tube(f"{spec['limb']}-{spec['side']}-claw-{spec['digit']}",[(tuple(p-d*.008+Vector((0,0,.001))),r*.72,r*.62),(tuple(p+d*length*.42+Vector((0,0,-.001))),r*.52,r*.43),(tuple(p+d*length+Vector((0,0,-.002))),r*.20,r*.19)],8,COL,M['beak_claws'])
 links.append({'child':claw.name,'parent':body.name,'purpose':'Compact claw sunk into one of five continuous digits per foot; generalized exact spread/length.'})
# Exact source geometry joins, not bounding-box guesses.
bpy.context.view_layer.update()
def tree(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],epsilon=0)
trees={n:tree(o) for n,o in parts.items()}
def inside(p,t):
 d=Vector((1,.137,.219)).normalized();pos=p.copy();n=0
 for _ in range(200):
  hit,_,_,_=t.ray_cast(pos,d,2)
  if hit is None:break
  n+=1;pos=hit+d*1e-8
 return bool(n%2)
for link in links:
 a,b=link['child'],link['parent'];hits=len(trees[a].overlap(trees[b]));contained=sum(inside(parts[a].matrix_world@v.co,trees[b]) for v in parts[a].data.vertices)
 link.update(boundary_intersection_pairs=hits,child_vertices_inside_parent=contained,status='PASS' if contained and hits else 'FAIL')
failed=[r for r in links if r['status']=='FAIL'];assert not failed,failed
# Origin contract is actual Z0 contact-footprint bbox center, NOT whole-animal bbox.
shift=ac.ground_asset(COL,center_xy=False)
contacts=[o.matrix_world@v.co for o in COL.all_objects if o.type=='MESH' for v in o.data.vertices if abs((o.matrix_world@v.co).z)<=1e-8]
assert contacts
clo=[min(p[i] for p in contacts) for i in range(2)];chi=[max(p[i] for p in contacts) for i in range(2)];cc=[(a+b)/2 for a,b in zip(clo,chi)]
for o in COL.all_objects:
 if o.type=='MESH':
  world=o.matrix_world.copy();world.translation+=Vector((-cc[0],-cc[1],0));o.matrix_world=world
shift[0]-=cc[0];shift[1]-=cc[1]
bpy.context.view_layer.update()
contacts_after=[o.matrix_world@v.co for o in COL.all_objects if o.type=='MESH' for v in o.data.vertices if abs((o.matrix_world@v.co).z)<=1e-8]
clo_after=[min(p[i] for p in contacts_after) for i in range(2)];chi_after=[max(p[i] for p in contacts_after) for i in range(2)];center_after=[(a+b)/2 for a,b in zip(clo_after,chi_after)]
assert max(abs(v) for v in center_after)<1e-7
(OUT/'ground-contact-origin.json').write_text(json.dumps({'status':'PASS','method':'Default helper only grounds Z; then center XY from actual world vertices at Z0 (absolute tolerance1e-8m). Not whole body bounds. All mesh transforms baked afterward; root stays identity.','contact_vertex_count':len(contacts_after),'precenter_contact_min_xy_m':clo,'precenter_contact_max_xy_m':chi,'applied_xy_translation_m':[-cc[0],-cc[1]],'final_contact_min_xy_m':clo_after,'final_contact_max_xy_m':chi_after,'final_contact_center_xy_m':center_after,'contact_z_tolerance_m':1e-8,'total_authored_to_export_offset_m':list(shift),'foot_quadrant_contact_counts':{f'{sx},{sy}':sum(p.x*sx>0 and p.y*sy>0 for p in contacts_after) for sx in [-1,1] for sy in [-1,1]}},indent=2))
for o in COL.all_objects:
 if o.type=='MESH':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
RAW['not_exported']=True;RAW['final_export_datum_offset_m']=list(shift)
root['taxon']='Proganochelys quenstedtii (selected sources: quenstedti)';root['reference_limits']='AMNH restored skeletal display; Schoch/Sues review reconstruction Fig3 rightmost and5B only';root['artistic_parts']='living tissue,colors,stance,exact osteoderm height/count,digit spread,nominal scale'
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'Actual source triangle BVH boundary overlaps and ray-parity inside vertices; not AABB-only. Interobject anatomy joins intentional; per-mesh strict self-intersections checked separately on exact final GLB.','checks':links,'failed':failed,'count':len(links),'feet':4,'toes_per_foot':5,'source_loft_count':len(raw),'foot_parameters':foot_specs,'carapace_length_m':.55,'carapace_width_m':.43,'moderate_dome_height_m':.18,'complete_plastron_integral_bridges':True},indent=2))
record=ac.export_asset('proganochelys',{'en':'Proganochelys — armored stem turtle','zh':'原颚龟（带甲颈尾早期龟）'},'reptiles',COL,metadata={'revision':'r001','representation':'living-reconstruction','description':{'en':'Original moderately domed stem turtle, complete plastron and bridges, armored short neck and tail, four five-toed feet.','zh':'原创中度穹顶原颚龟，完整腹甲与甲桥、短颈和尾骨甲、四足各五趾。'},'reconstruction_notes':C['notes'],'generator':'scripts/build_proganochelys.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.95,'origin_note':'Actual Z0 contact-vertex XY footprint bbox centered at origin, not whole-animal bounds; source authored datum offset documented.','source_reference_images_incorporated':False},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'default_area_epsilon_m2':1e-10,'initial_voxel_triangles':initial,'editable_anatomical_lofts':len(raw),'export_meshes':len(parts),'datum_offset_m':list(shift),'glb_sha256':record['sha256']['glb']},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
