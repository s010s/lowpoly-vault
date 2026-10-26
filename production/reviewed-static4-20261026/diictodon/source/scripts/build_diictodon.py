# SPDX-License-Identifier: MIT
"""Original reference-led Diictodon feliceps tusked morph. No reference mesh or pixel sampling.
Factory builds preserve original editable anatomical lofts outside EXPORT.
"""
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
   a=2*math.pi*j/n;c,s=math.cos(a),math.sin(a)
   v.append((x+w*math.copysign(abs(c)**power,c),y,(b+t)/2+(t-b)/2*math.copysign(abs(s)**power,s)))
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
  p=Vector(p);t=(Vector(stations[min(i+1,len(stations)-1)][0])-Vector(stations[max(i-1,0)][0])).normalized()
  ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0));u=t.cross(ref).normalized();q=t.cross(u).normalized()
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

# Quiet rounded cylindrical trunk: broad shoulder and hip transitions, raised belly.
loft_y('Editable compact cylindrical trunk',[(-.125,0,.078,.142,.034),(-.105,0,.060,.151,.048),(-.075,0,.052,.158,.057),(-.025,0,.048,.160,.061),(.035,0,.048,.157,.061),(.085,0,.052,.150,.056),(.125,0,.063,.137,.044),(.151,0,.077,.119,.025)],24)
# Broad cheeks, short narrowing snout, closed jaw and keratin beak region.
loft_y('Editable short head and neck',[(-.222,0,.122,.144,.015),(-.216,0,.113,.154,.022),(-.203,0,.107,.166,.030),(-.188,0,.105,.177,.036),(-.168,0,.104,.183,.043),(-.148,0,.105,.181,.048),(-.130,0,.104,.173,.046),(-.114,0,.096,.158,.037),(-.097,0,.083,.148,.034)],24,power=.84)
loft_y('Editable short tapering tail',[(.125,0,.076,.124,.031),(.150,0,.079,.117,.024),(.172,.004,.078,.107,.017),(.191,.009,.079,.099,.011),(.210,.013,.081,.093,.006),(.228,.012,.084,.087,.0017)],16)
for s in [-1,1]:
 tag='L' if s<0 else 'R'
 tube('Editable forelimb '+tag,[((s*.041,-.092,.122),.026,.029),((s*.062,-.089,.096),.024,.025),((s*.078,-.067,.067),.019,.020),((s*.081,-.083,.043),.014,.015),((s*.081,-.109,.019),.012,.013)],14)
 tube('Editable hindlimb '+tag,[((s*.034,.101,.110),.029,.031),((s*.052,.091,.087),.027,.027),((s*.066,.088,.059),.020,.020),((s*.068,.119,.037),.013,.014),((s*.069,.101,.016),.011,.012)],14)
 for limb,px,py,scale in [('fore',s*.081,-.117,1.),('hind',s*.069,.098,.81)]:
  loft_y('Editable '+limb+' palm '+tag,[(py-.018*scale,px,.003,.022,.017*scale),(py,px,.0025,.027,.022*scale),(py+.017*scale,px,.006,.023,.016*scale)],16)
  for digit,(dx,dy) in enumerate([(-.020,-.021),(-.011,-.032),(0,-.037),(.012,-.032),(.022,-.022)],1):
   dx*=scale;dy*=scale;r=.0048*scale
   start=(px+s*dx*.60,py-.008*scale,.012);middle=(px+s*dx*.90,py+dy*.73,.008);end=(px+s*dx,py+dy,.0066)
   tube(f'Editable {limb} {tag} toe {digit}',[(start,r*1.2,r),(middle,r,r*.87),(end,r*.77,r*.7)],10)
   direction=Vector((s*dx*.14,dy*.3,0)).normalized();foot_specs.append({'limb':limb,'side':tag,'digit':digit,'root':end,'direction':tuple(direction),'radius':r,'claw_length_m':(.010 if limb=='fore' else .0065)})
# Preserve all genuine authored primitives for editable source; union only duplicates.
for o in raw:o.hide_render=True;o.hide_set(True)
bpy.ops.object.select_all(action='DESELECT')
for o in raw:
 d=o.copy();d.data=o.data.copy();COL.objects.link(d);d.hide_render=False;d.hide_set(False);d.select_set(True)
bpy.context.view_layer.objects.active=d;bpy.ops.object.join();body=bpy.context.object;body.name='continuous-skull-trunk-four-limbs-five-toed-feet-short-tail';body.parent=root
rem=body.modifiers.new('Original anatomy union 1.2 mm','REMESH');rem.mode='VOXEL';rem.voxel_size=C['voxel_size_m'];rem.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=rem.name);canonical(body)
sm=body.modifiers.new('Soft anatomical transitions','SMOOTH');sm.factor=.55;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
body.data.calc_loop_triangles();initial=len(body.data.loop_triangles)
dec=body.modifiers.new('Deliberate low polygon planes','DECIMATE');dec.ratio=min(1,C['target_body_triangles']/initial);dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name);canonical(body)
# Real underside contact planes. Clamping only thin toe/palm underside, not limbs.
for v in body.data.vertices:
 if v.co.z<.0043:v.co.z=0
body.data.update();body.data.materials.clear()
for m in M.values():body.data.materials.append(m)
keys=list(M)
for p in body.data.polygons:
 c=p.center
 p.material_index=keys.index('beak_claws') if c.y<-.200 else 0
 p.use_smooth=False
parts[body.name]=body
body['construction']='Original lofts voxel-unioned, smoothed and canonicalized then decimated; no external geometry.'
# Named semantic groups allow editing surface regions without rebuilding.
for name,pred in [('head',lambda v:v.y<-.11),('trunk',lambda v:-.11<=v.y<=.14 and abs(v.x)<.06),('tail',lambda v:v.y>.14),('feet',lambda v:v.z<.03),('left_limbs',lambda v:v.x<-.06),('right_limbs',lambda v:v.x>.06)]:
 ids=[v.index for v in body.data.vertices if pred(v.co)]
 if ids:body.vertex_groups.new(name=name).add(ids,1,'REPLACE')
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
# Exactly two rooted upper tusks. Root disks are inside the upper cheek.
for s in [-1,1]:
 tag='L' if s<0 else 'R'
 tusk=tube('upper-tusk-'+tag,[((s*.034,-.184,.137),.006,.006),((s*.038,-.183,.125),.0057,.0053),((s*.040,-.180,.112),.0045,.0042),((s*.040,-.175,.101),.0027,.0025),((s*.039,-.171,.097),.0007,.0007)],12,COL,M['tusk'])
 links.append({'child':tusk.name,'parent':body.name,'purpose':'Upper tusk root embedded within cheek, not lower tusk; exactly one each side.'})
 # Ray-landed shallow lateral eye, no separate protruding bead or large ears.
 hit,co,no,index=body.ray_cast(Vector((s*.15,-.157,.158)),Vector((-s,0,0)))
 assert hit
 eye=ellipsoid('small-lateral-eye-'+tag,(co.x-s*.0012,-.157,.158),(.0033,.0057,.0048),'eye')
 links.append({'child':eye.name,'parent':body.name,'purpose':'Shallow eye lens root ray-anchored to exact living head surface.'})
 hit,co,no,index=body.ray_cast(Vector((s*.15,-.209,.146)),Vector((-s,0,0)))
 assert hit
 nostril=ellipsoid('subtle-nostril-'+tag,(co.x-s*.0004,-.209,.146),(.0015,.0022,.0012),'eye',10,5)
 links.append({'child':nostril.name,'parent':body.name,'purpose':'Shallow nostril mark embedded into short beak side.'})
# Blunt compact claws attach to continuous toes; generalized distal morphology.
for spec in foot_specs:
 p=Vector(spec['root']);d=Vector(spec['direction']);length=spec['claw_length_m'];r=spec['radius']
 claw=tube(f"{spec['limb']}-{spec['side']}-claw-{spec['digit']}",[(tuple(p-d*.006+Vector((0,0,.001))),r*.70,r*.6),(tuple(p+d*length*.42+Vector((0,0,-.001))),r*.52,r*.42),(tuple(p+d*length+Vector((0,0,-.0017))),r*.19,r*.18)],8,COL,M['beak_claws'])
 links.append({'child':claw.name,'parent':body.name,'purpose':'Claw root overlaps integrated toe; foreclaw longer, broad blunt tip, not needle.'})
# Explicit numerical connection evidence (not AABB overlap alone).
bpy.context.view_layer.update()
def tree(o):return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons],epsilon=0)
trees={n:tree(o) for n,o in parts.items()}
def inside(p,t):
 d=Vector((1,.137,.219)).normalized();pos=p.copy();n=0
 for _ in range(200):
  hit,_,_,_=t.ray_cast(pos,d,1)
  if hit is None:break
  n+=1;pos=hit+d*1e-9
 return bool(n%2)
for link in links:
 a,b=link['child'],link['parent'];hits=len(trees[a].overlap(trees[b]));contained=sum(inside(parts[a].matrix_world@v.co,trees[b]) for v in parts[a].data.vertices)
 link.update(boundary_intersection_pairs=hits,child_vertices_inside_parent=contained,status='PASS' if contained and hits else 'FAIL')
failed=[r for r in links if r['status']=='FAIL'];assert not failed,failed
# Ground/center by exact final footprint extents; identity root remains unchanged.
shift=ac.ground_asset(COL,center_xy=True)
for o in COL.all_objects:
 if o.type=='MESH':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# r002 only: move every exported local vertex by one exact declared offset.
# Root and object transforms remain identity. The reference geometry, topology,
# palette, seed, construction and normal policy are unchanged.
contacts=sorted(set(tuple(float(x) for x in v.co) for o in COL.all_objects if o.type=='MESH' for v in o.data.vertices if v.co.z==0))
assert len(contacts)==C['origin_placement']['expected_contact_count'],len(contacts)
lo=[min(p[k] for p in contacts) for k in range(3)];hi=[max(p[k] for p in contacts) for k in range(3)];center=[(a+b)*.5 for a,b in zip(lo,hi)]
delta=C['origin_placement']['translation_m'];assert max(abs(delta[k]+center[k]) for k in range(3))<1e-12,(delta,center)
for o in COL.all_objects:
 if o.type=='MESH':
  for v in o.data.vertices:v.co=tuple(float(v.co[k])+delta[k] for k in range(3))
  o.data.update()
post=sorted(set(tuple(float(x) for x in v.co) for o in COL.all_objects if o.type=='MESH' for v in o.data.vertices if v.co.z==0))
post_lo=[min(p[k] for p in post) for k in range(3)];post_hi=[max(p[k] for p in post) for k in range(3)];post_center=[(a+b)*.5 for a,b in zip(post_lo,post_hi)]
assert len(post)==41 and max(abs(x) for x in post_center)<=C['origin_placement']['origin_tolerance_m']
placement={'status':'PASS_SOURCE_ORIGIN_ONLY','algorithm':C['origin_placement']['definition'],'contact_count':len(post),'pre_translation_contact_points_m':contacts,'pre_translation_bbox_center_m':center,'translation_blender_m':delta,'post_translation_contact_points_m':post,'post_translation_bbox_min_m':post_lo,'post_translation_bbox_max_m':post_hi,'post_translation_bbox_center_m':post_center,'mesh_local_data_translated':True,'root_and_mesh_transforms_unchanged_identity':True}
(OUT/'origin-placement.json').write_text(json.dumps(placement,indent=2))
shift=[shift[k]+delta[k] for k in range(3)]
root['origin_algorithm']=C['origin_placement']['definition']
# Original input lofts retain their authored datum, labeled in source.
RAW['not_exported']=True;RAW['final_export_datum_offset_m']=list(shift)
root['taxon']='Diictodon feliceps';root['morph']='tusked, sex unspecified';root['artistic_parts']='skin, colors, neutral stance, distal digits/claws, tail outline';root['reference_limits']='Ray 2003 primary abstract only; Iziko cast status unverified; Ray 2006 excluded from geometry.'
(OUT/'anatomical-connections.json').write_text(json.dumps({'method':'Actual source triangle BVH boundary overlaps and ray-parity inside vertices; not AABB-only. Interobject joins intentionally intersect; per-mesh self-intersections checked separately on exact final GLB.','checks':links,'failed':failed,'count':len(links),'tusks':2,'feet':4,'toes_per_foot':5,'source_loft_count':len(raw),'foot_parameters':foot_specs},indent=2))
record=ac.export_asset('diictodon',{'en':'Diictodon feliceps — tusked morph','zh':'双犬齿兽（具獠牙形态）'},'synapsids',COL,metadata={'revision':C['revision'],'representation':'living-reconstruction','description':{'en':'Original compact short-limbed dicynodont, blunt beak and exactly two moderate upper tusks. Sex unspecified.','zh':'原创短肢柱状体双犬齿兽，钝喙及两枚上颌獠牙，不推定性别。'},'reconstruction_notes':C['notes'],'generator':'scripts/build_diictodon.py','config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'nominal_total_length_m':.45,'origin_note':'Exact XY bbox midpoint of 41 unique Z0 sole contact vertices centered at root XY0; all four feet grounded. Not whole projected head/trunk/tail bounds.','source_reference_images_incorporated':False},output_root=OUT,render=False,diagnostics=False,max_triangles=12000,max_materials=8,max_primitives=48)
(OUT/'build-record.json').write_text(json.dumps({'status':'COMPLETE','factory_startup':True,'gray':A.gray,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(A.config.read_bytes()).hexdigest(),'seed':C['seed'],'blender':bpy.app.version_string,'threads':2,'default_area_epsilon_m2':1e-10,'initial_voxel_triangles':initial,'editable_anatomical_lofts':len(raw),'export_meshes':len(parts),'datum_offset_m':list(shift),'origin_placement':placement,'glb_sha256':record['sha256']['glb']},indent=2));print('BUILD_COMPLETE',record['sha256']['glb'])
