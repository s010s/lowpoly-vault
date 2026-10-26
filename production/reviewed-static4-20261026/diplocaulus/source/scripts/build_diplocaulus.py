# SPDX-License-Identifier: MIT
"""Original primary-reference-led Diplocaulus, no imported animal/template geometry."""
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
raw=[];parts={};links=[];limb_records=[]
def mesh(name,v,f,collection,material=None):
 # All topology explicitly triangulated before source save and export.
 f=[(p[0],p[j],p[j+1]) for p in f for j in range(1,len(p)-1)]
 o=ac.mesh_object(name,v,f,material or M['skin'],collection)
 if collection==RAW:o.parent=None;raw.append(o)
 else:parts[name]=o
 return o

def tube(name,stations,n=16,collection=COL,material=None):
 v=[];f=[]
 for i,(p,w,d) in enumerate(stations):
  p=Vector(p);t=(Vector(stations[min(i+1,len(stations)-1)][0])-Vector(stations[max(i-1,0)][0])).normalized();ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0));u=t.cross(ref).normalized();q=t.cross(u).normalized()
  for j in range(n):a=2*math.pi*j/n;v.append(tuple(p+u*w*math.cos(a)+q*d*math.sin(a)))
 for i in range(len(stations)-1):
  for j in range(n):f.extend([(i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n),(i*n+j,(i+1)*n+(j+1)%n,(i+1)*n+j)])
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

def save_editable(o):
 d=o.copy();d.data=o.data.copy();RAW.objects.link(d);d.parent=None;d.name='Editable '+o.name;raw.append(d);return d
# Concave boomerang skull cap: ordered X cross-strips, each front/back boundary sampled.
# No global n-gon, external-center fan or guessed exporter diagonal anywhere.
rows=[(-.120,-.213,-.209,.0038),(-.116,-.225,-.211,.0048),(-.104,-.245,-.219,.0065),(-.086,-.272,-.231,.0080),(-.064,-.299,-.245,.0100),(-.042,-.324,-.261,.0125),(-.024,-.343,-.273,.0150),(0,-.350,-.278,.0160),(.024,-.343,-.273,.0150),(.042,-.324,-.261,.0125),(.064,-.299,-.245,.0100),(.086,-.272,-.231,.0080),(.104,-.245,-.219,.0065),(.116,-.225,-.211,.0048),(.120,-.213,-.209,.0038)]
fractions=[0,.18,.4,.62,.82,1];v=[];f=[]
for x,yf,yb,t in rows:
 for a in fractions:
  y=yf+(yb-yf)*a;z=.005+t*(.60+.40*math.sin(math.pi*a));v.append((x,y,z))
N=len(v);v.extend((x,y,-.005-(z-.005)*.43) for x,y,z in list(v))
for i in range(len(rows)-1):
 for j in range(len(fractions)-1):
  a=i*len(fractions)+j;b=a+len(fractions)
  # Individually planar triangles from valid interior quad strips.
  f.extend([(a,b,b+1),(a,b+1,a+1),(a+N,b+1+N,b+N),(a+N,a+1+N,b+1+N)])
border=list(range(len(fractions)))+[i*len(fractions)+len(fractions)-1 for i in range(1,len(rows))]+list(range(N-2,N-len(fractions)-1,-1))+[i*len(fractions) for i in range(len(rows)-2,0,-1)]
for a,b in zip(border,border[1:]+border[:1]):f.extend([(a,b,b+N),(a,b+N,a+N)])
head=mesh('boomerang-head-finite-thickness-explicit-cross-strips',v,f,COL,[M['head'],M['belly']]);save_editable(head)
for p in head.data.polygons:p.material_index=1 if p.center.z<-.004 else 0
head['triangulation']='Interior X strips, two explicit triangle diagonals per surface cell; finite positive tip thickness; no concave n-gon or external fan.'
# Body/tail one uninterrupted custom axial loft. Tail is laterally compressed, not ribbon-fin.
stations=[((0,-.290,0),.019,.012),((0,-.270,0),.025,.017),((0,-.243,0),.039,.022),((0,-.215,0),.052,.026),((0,-.178,0),.060,.030),((0,-.136,0),.061,.031),((0,-.094,0),.057,.029),((0,-.055,0),.049,.026),((0,-.022,0),.039,.023),((0,.010,0),.030,.022),((.002,.045,0),.023,.024),((.006,.083,0),.018,.026),((.012,.122,.001),.014,.028),((.022,.163,.002),.0115,.028),((.034,.205,.003),.0094,.025),((.045,.248,.004),.0072,.021),((.050,.290,.006),.0055,.016),((.047,.328,.007),.0040,.0115),((.039,.360,.008),.0028,.0078),((.031,.383,.009),.0017,.0045),((.026,.400,.010),.0008,.0018)]
body=tube('continuous-low-trunk-and-long-tapering-tail',stations,24,COL,[M['skin'],M['belly']]);save_editable(body)
for p in body.data.polygons:p.material_index=1 if p.center.z<-.014 else 0
links.append({'child':head.name,'parent':body.name,'purpose':'Central posterior skull joins narrow living axial neck; horns are free posterior extensions, no sail.'})
# Authored bent limbs, palms and separated rounded digits; each limb becomes one connected remeshed solid.
for side in [-1,1]:
 tag='L' if side<0 else 'R'
 for kind,base_y,palm_y,digits,px in [('fore',-.223,-.171,4,.093),('hind',-.033,.025,5,.081)]:
  start=len(raw);z=-.008
  specs=[((side*.032,base_y,z),.015,.014),((side*.058,base_y+.012,z-.010),.014,.012),((side*.078,base_y+.024,z-.018),.011,.010),((side*px,palm_y-.006,z-.019),.010,.008)]
  tube('Editable '+kind+' arm '+tag,specs,14,RAW)
  palm=(side*px,palm_y,z-.019)
  tube('Editable '+kind+' palm '+tag,[((palm[0],palm[1]-.013,palm[2]),.009,.007),((palm[0]+side*.005,palm[1],palm[2]),.015,.0075),((palm[0]+side*.008,palm[1]+.009,palm[2]),.012,.006)],14,RAW)
  digit_data=[]
  angles=[-62,-22,22,62] if digits==4 else [-70,-35,0,35,70]
  for j,angle in enumerate(angles):
   a=math.radians(angle);length=(.021 if digits==4 else .025)*(1-.20*abs(angle)/70);dx=side*(.008+math.sin(a)*.012);dy=math.cos(a)*.009
   rootp=Vector((palm[0]+dx,palm[1]+dy,palm[2]));direction=Vector((side*math.sin(a),math.cos(a),.02));tip=rootp+direction*length
   tube(f'Editable {kind} {tag} digit {j+1}',[(tuple(rootp),.0045,.0038),(tuple(rootp+direction*length*.55),.0036,.0032),(tuple(tip),.0023,.0023)],10,RAW)
   digit_data.append({'digit':j+1,'root':list(rootp),'tip':list(tip)})
  batch=raw[start:]
  bpy.ops.object.select_all(action='DESELECT')
  for o in batch:
   d=o.copy();d.data=o.data.copy();COL.objects.link(d);d.hide_render=False;d.hide_set(False);d.select_set(True)
  bpy.context.view_layer.objects.active=d;bpy.ops.object.join();limb=bpy.context.object;limb.name=f'{kind}-{tag}-continuous-arm-palm-{digits}-rounded-digits';limb.parent=root
  rem=limb.modifiers.new('Unify authored limb roots and digits','REMESH');rem.mode='VOXEL';rem.voxel_size=C['voxel_size_m'];bpy.ops.object.modifier_apply(modifier=rem.name);canonical(limb)
  sm=limb.modifiers.new('Soft amphibian joins','SMOOTH');sm.factor=.45;sm.iterations=2;bpy.ops.object.modifier_apply(modifier=sm.name)
  limb.data.calc_loop_triangles();dec=limb.modifiers.new('Deliberate lowpoly limb planes','DECIMATE');dec.ratio=min(1,C['target_limb_triangles']/len(limb.data.loop_triangles));dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name);canonical(limb)
  limb.data.materials.clear();limb.data.materials.append(M['skin']);parts[limb.name]=limb
  links.append({'child':limb.name,'parent':body.name,'purpose':'True finite arm root enters trunk; hand/digits one continuous solid, not loose beads.'})
  limb_records.append({'side':tag,'kind':kind,'digit_count':digits,'digit_evidence':'4 foredigits observed UC1009' if digits==4 else '5 hinddigits restored convention;1317 incomplete','authored_root':specs[0][0],'digits':digit_data})
# Subtle shallow dorsal eyes in anterior-central skull; genuine body surface ray landing.
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
for s in [-1,1]:
 tag='L' if s<0 else 'R';x=s*.017;y=-.325
 hit,co,no,idx=head.ray_cast(Vector((x,y,.1)),Vector((0,0,-1)));assert hit
 rim=ellipsoid('shallow-dorsal-eyelid-'+tag,(x,y,co.z-.0017),(.0075,.009,.0042),'eye_rim');eye=ellipsoid('small-dorsal-eye-'+tag,(x,y-.0005,co.z+.0003),(.0043,.0056,.0034),'eye')
 links.extend([{'child':rim.name,'parent':head.name,'purpose':'Low dorsal eyelid embedded in head; no detached raised bead.'},{'child':eye.name,'parent':rim.name,'purpose':'Small nonemissive eye inset into eyelid.'}])
# Actual triangle intersections AND point containment for every separate anatomical attachment.
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
# Required swimming datum: entire final evaluated EXPORT bounds XYZ, never a ground footprint.
allverts=ac._vertices_world(COL);lo,hi=ac._bounds(allverts);shift=Vector(tuple(-(a+b)/2 for a,b in zip(lo,hi)))
for o in COL.all_objects:
 if o.type=='MESH':
  for v in o.data.vertices:v.co+=shift
  o.data.update()
for o in raw:o.hide_render=True;o.hide_set(True)
RAW['not_exported']=True;RAW['authored_to_export_offset_m']=list(shift)
bpy.context.view_layer.update();vlo,vhi=ac._bounds(ac._vertices_world(COL));center=[(a+b)/2 for a,b in zip(vlo,vhi)];assert max(abs(x) for x in center)<1e-7
for name,o in parts.items():
 ids=[v.index for v in o.data.vertices];o.vertex_groups.new(name=name[:60]).add(ids,1,'REPLACE')
root['taxon']='Diplocaulus magnicornis-inspired';root['scientific_limits']=C['notes'];root['pose']='neutral unsupported aquatic presentation';root['origin']='ALL final exported vertices XYZ AABB center; not floor or footprint'
(OUT/'non-grounded-origin.json').write_text(json.dumps({'status':'PASS','method':'ALL final evaluated EXPORT mesh world vertices XYZ AABB center; includes every horn,toe,eye,tail. No ground shift or footprint used.','precenter_min_xyz_m':lo,'precenter_max_xyz_m':hi,'translation_xyz_m':list(shift),'final_min_xyz_m':vlo,'final_max_xyz_m':vhi,'final_center_xyz_m':center,'tolerance_m':1e-5},indent=2))
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'Actual source triangle BVH boundary overlaps plus inside child vertices, not AABB. Interobject joins intentional. Each limb arm/palm/digits unified; exact-GLB per-mesh internal crossings tested separately.','checks':links,'failed':failed,'count':len(links),'limbs':limb_records,'editable_source_lofts':len(raw),'head_topology':'Explicit valid interior cross-strip triangles, positive finite thickness; no concave cap ngon/exterior fan.','horn_tip_thickness_m':.0038*1.43+.010},indent=2))
record=ac.export_asset('diplocaulus',{'en':'Diplocaulus — boomerang-headed aquatic reconstruction','zh':'笠头螈（宽角头形态复原）'},'amphibians',COL,metadata={'revision':'r001','representation':'living-reconstruction','description':{'en':'Original low-profile boomerang-headed amphibian with four small limbs and long tapered tail.','zh':'原创低伏宽角头两栖动物，四短肢与修长渐细尾。'},'reconstruction_notes':C['notes'],'generator':'scripts/build_diplocaulus.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.75,'origin_note':'Entire evaluated EXPORT XYZ AABB centered, neutral swimming datum, not footprint.','source_reference_images_incorporated':False},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'default_area_epsilon_m2':1e-10,'editable_anatomical_lofts':len(raw),'export_meshes':len(parts),'datum_offset_m':list(shift),'glb_sha256':record['sha256']['glb']},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
