"""Original Dimetrodon r002 art anatomy. Run with Blender --background --python this.py -- --graybox.
No source image sampling or reference geometry. Meter-sized, +Z up, -Y forward.
Union/remesh is intentionally editable via preserved hidden AnatomyLofts collection.
"""
import bpy,bmesh,math,json,hashlib,sys,shutil
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/deps'))
import asset_common as common
CONFIG=json.loads((ROOT/'generator-config.json').read_text())
if bpy.app.version_string!=CONFIG['blender_version']:raise RuntimeError('Pinned Blender version mismatch')
GRAY='--graybox' in sys.argv
REBUILD='--rebuild-check' in sys.argv
REBUILD_TAG=next((a.split('=',1)[1] for a in sys.argv if a.startswith('--rebuild-tag=')),'generator-rebuild')
if not REBUILD_TAG.replace('-','').isalnum():raise RuntimeError('Invalid local rebuild tag')
ARTIFACT_ROOT=ROOT/'evidence'/REBUILD_TAG if REBUILD else ROOT
ARTIFACT_ROOT.mkdir(parents=True,exist_ok=True)
RENDER='--no-render' not in sys.argv
COL=common.setup_scene('dimetrodon',seed=CONFIG['seed'])
scene=bpy.context.scene
scene.render.threads_mode='FIXED';scene.render.threads=CONFIG['blender_threads']
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=False
scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
scene.world=bpy.data.worlds.new('StudioWorld');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.28,.30,.32,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5

def mat(name,c,rough=.78):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;m.use_backface_culling=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough
 p.inputs['Metallic'].default_value=0;p.inputs['Specular IOR Level'].default_value=.25
 return m
M=[mat('Body | original muted moss',(.205,.25,.16)),mat('Ventral | olive ash',(.34,.37,.255)),mat('Sail | umber ochre',(.39,.26,.135)),mat('Sail ridge | smoked ochre',(.29,.19,.102)),mat('Eyes and mouth | charcoal',(.024,.032,.021),.52),mat('Teeth and claws | worn ivory',(.62,.57,.40))]
gray=mat('Graybox neutral',(.42,.45,.46))
# EXPORT/root supplied by shared setup_scene. Palette values below remain r001 linear values unchanged.
RAW=bpy.data.collections.new('AnatomyLofts_EDITABLE_SOURCE');scene.collection.children.link(RAW)
raw=[];features=[]
def mesh_obj(name,verts,faces,collection=COL):
 me=bpy.data.meshes.new(name+' Mesh');me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);collection.objects.link(ob)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(me);bm.free();return ob

def canonical_mesh(obj,triangulate=False):
 # Rebuild from THIS RUN's generated coordinates; never from a cached mesh.
 # Remesh and joins can enumerate equal geometry in unstable order. Canonicalizing
 # before smooth/decimate removes ordering-sensitive accumulation/tie-breaking.
 old=obj.data
 if triangulate:
  old.calc_loop_triangles()
  raw=[(tuple(t.vertices),old.polygons[t.polygon_index].material_index) for t in old.loop_triangles]
 else:raw=[(tuple(p.vertices),p.material_index) for p in old.polygons]
 coords=[tuple(float(x) for x in v.co) for v in old.vertices]
 ordered=sorted(set(coords));lookup={c:i for i,c in enumerate(ordered)}
 idx=[lookup[c] for c in coords]
 faces=[]
 for vv,mi in raw:
  face=tuple(idx[i] for i in vv)
  # Rotate only: preserve outward winding, do not reverse polygon orientation.
  face=min(face[k:]+face[:k] for k in range(len(face)))
  faces.append((mi,face))
 faces.sort(key=lambda x:(x[0],x[1]))
 name=old.name;mats=list(old.materials)
 me=bpy.data.meshes.new(name+'__ordered');me.from_pydata(ordered,[],[f for _,f in faces]);me.update()
 for m in mats:me.materials.append(m)
 for p,(mi,_) in zip(me.polygons,faces):p.material_index=mi;p.use_smooth=False
 obj.data=me
 if old.users==0:bpy.data.meshes.remove(old)
 me.name=name
 return obj

def loft_y(name,stations,n=20,power=1.0):
 # stations: y, center-x, bottom-z, top-z, half-width
 vs=[];fs=[]
 for y,x,b,t,w in stations:
  for j in range(n):
   a=2*math.pi*j/n;co,si=math.cos(a),math.sin(a)
   vs.append((x+w*math.copysign(abs(co)**power,co),y,(b+t)/2+(t-b)/2*math.copysign(abs(si)**power,si)))
 for i in range(len(stations)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;c=(i+1)*n+(j+1)%n;d=(i+1)*n+j;fs.append((a,b,c,d))
 fs.extend([tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]);o=mesh_obj(name,vs,fs,RAW);raw.append(o);return o

def tube(name,stations,n=12):
 # points x y z, width and depth in local radial frame
 vs=[];fs=[]
 for i,(p,w,d) in enumerate(stations):
  p=Vector(p);prev=Vector(stations[max(0,i-1)][0]);nxt=Vector(stations[min(len(stations)-1,i+1)][0]);t=(nxt-prev).normalized()
  ref=Vector((0,0,1)) if abs(t.z)<.93 else Vector((0,1,0));u=t.cross(ref).normalized();v=t.cross(u).normalized()
  for j in range(n):a=2*math.pi*j/n;vs.append(tuple(p+u*w*math.cos(a)+v*d*math.sin(a)))
 for i in range(len(stations)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 fs.extend([tuple(reversed(range(n))),tuple((len(stations)-1)*n+j for j in range(n))]);o=mesh_obj(name,vs,fs,RAW);raw.append(o);return o

loft_y('Trunk shoulder ribcage pelvis',[
 (-.35,0,.195,.345,.072),(-.29,0,.135,.375,.102),(-.23,0,.113,.387,.125),(-.15,0,.105,.386,.14),(-.05,0,.101,.38,.147),(.065,0,.106,.369,.144),(.16,0,.118,.352,.128),(.24,0,.129,.329,.111),(.31,0,.138,.303,.085),(.36,0,.148,.279,.061)],n=24)
loft_y('Short powerful neck', [(-.405,0,.222,.371,.079),(-.36,0,.21,.366,.085),(-.31,0,.195,.365,.091),(-.24,0,.17,.35,.098)],n=18)
loft_y('Deep maxilla cheek and cranium', [(-.644,0,.293,.339,.022),(-.627,0,.279,.36,.043),(-.592,0,.272,.378,.058),(-.552,0,.266,.391,.068),(-.515,0,.26,.401,.076),(-.47,0,.261,.416,.085),(-.426,0,.251,.425,.098),(-.383,0,.236,.397,.096),(-.34,0,.233,.362,.072)],n=20,power=.82)
loft_y('Lower jaw articulated rear', [(-.636,0,.242,.26,.018),(-.612,0,.223,.251,.045),(-.575,0,.211,.245,.058),(-.53,0,.205,.238,.066),(-.48,0,.207,.239,.075),(-.433,0,.214,.253,.086),(-.385,0,.225,.278,.084),(-.34,0,.24,.29,.064)],n=16,power=.8)
loft_y('Long gently curved tail',[(.265,0,.14,.319,.093),(.36,.003,.145,.28,.066),(.45,.01,.137,.239,.052),(.55,.021,.122,.202,.04),(.66,.037,.099,.164,.031),(.78,.054,.075,.125,.023),(.9,.061,.052,.088,.016),(1.00,.054,.037,.063,.011),(1.09,.037,.03,.046,.0065),(1.156,.012,.032,.036,.0015)],n=16)
# Four continuously joined limbs: outward proximal segments and bent low distal joints.
foot_specs=[]
for side in [-1,1]:
 s=side;tag='L' if s<0 else 'R'
 tube('Forelimb_'+tag,[((s*.074,-.245,.286),.066,.068),((s*.125,-.244,.246),.06,.056),((s*.18,-.216,.181),.047,.043),((s*.204,-.225,.128),.033,.034),((s*.207,-.269,.071),.024,.024),((s*.21,-.302,.03),.029,.019)],n=14)
 tube('Hindlimb_'+tag,[((s*.075,.215,.25),.073,.072),((s*.135,.258,.22),.066,.06),((s*.19,.318,.162),.052,.043),((s*.216,.304,.104),.032,.03),((s*.216,.262,.055),.022,.023),((s*.217,.232,.028),.029,.018)],n=14)
 for limb,px,py in [('fore',s*.211,-.302),('hind',s*.217,.232)]:
  loft_y(limb+' palm '+tag,[(py-.03,px,.006,.033,.027),(py,px,.004,.051,.036),(py+.031,px,.011,.041,.026)],n=14)
  for digit,(dx,dy,r) in enumerate([(-.038,-.048,.009),(-.019,-.077,.0105),(.006,-.093,.011),(.035,-.077,.010),(.06,-.041,.0085)],1):
   start=(px+s*dx*.24,py-.005,.025);mid=(px+s*dx*.65,py+dy*.54,.017);end=(px+s*dx,py+dy,.013)
   tube(f'{limb}_{tag}_digit_{digit}',[(start,r*1.15,r*.95),(mid,r,r*.76),(end,r*.56,r*.58)],n=9)
   foot_specs.append({'limb':limb,'side':tag,'digit':digit,'tip':end,'direction':(s*dx,dy,0),'radius':r})
# Single sealed sail volume; no free spine rods and no Edaphosaurus crossbars.
profile=[(-.325,.344),(-.29,.403),(-.25,.509),(-.205,.588),(-.15,.655),(-.09,.699),(-.025,.724),(.04,.731),(.10,.721),(.16,.69),(.215,.64),(.265,.571),(.31,.486),(.35,.397),(.385,.311)]
vs=[];fs=[];nf=6;fractions=[0,.12,.32,.55,.78,1]
for side in [-1,1]:
 for i,(y,top) in enumerate(profile):
  base=.31-.07*max(0,y)/.385
  for j,f in enumerate(fractions):
   # Taller middle: subtle broad radial planes, not embossed fossil skin.
   half=(.032*(1-f)**2+.0065)*(.72 if i in [0,len(profile)-1] else 1)
   yy=y + .025*math.sin((y+.325)/.71*math.pi)*f*(.1-y)
   vs.append((side*half,yy,base+(top-base)*f))
stride=len(profile)*nf
for side in range(2):
 for i in range(len(profile)-1):
  for j in range(nf-1):
   a=side*stride+i*nf+j;fs.append((a,a+1,a+nf+1,a+nf))
for i in range(len(profile)-1):
 for j in [0,nf-1]:
  a=i*nf+j;b=(i+1)*nf+j;fs.append((a,b,b+stride,a+stride))
for i in [0,len(profile)-1]:
 for j in range(nf-1):
  a=i*nf+j;fs.append((a,a+stride,a+stride+1,a+1))
sail=mesh_obj('Closed tall sail tissue volume',vs,fs,RAW);raw.append(sail)
# Archive fully editable input lofts; voxel union removes anatomy shell intersections.
for o in raw:o.hide_render=True;o.hide_set(True)
bpy.ops.object.select_all(action='DESELECT')
for o in raw:
 dup=o.copy();dup.data=o.data.copy();COL.objects.link(dup);dup.hide_render=False;dup.hide_set(False);dup.select_set(True)
bpy.context.view_layer.objects.active=dup;bpy.ops.object.join();body=bpy.context.object;body.name='Dimetrodon continuous anatomy'
rem=body.modifiers.new('Union anatomy at 2.7mm art resolution','REMESH');rem.mode='VOXEL';rem.voxel_size=.0027;rem.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=rem.name)
canonical_mesh(body)
sm=body.modifiers.new('Quiet anatomical transitions','SMOOTH');sm.factor=.65;sm.iterations=5;bpy.ops.object.modifier_apply(modifier=sm.name)
# Drop undersupported voxel islands if any; preserve largest connected exterior.
bm=bmesh.new();bm.from_mesh(body.data);seen=set();parts=[]
for v in bm.verts:
 if v in seen:continue
 part=[];todo=[v];seen.add(v)
 while todo:
  q=todo.pop();part.append(q)
  for e in q.link_edges:
   u=e.other_vert(q)
   if u not in seen:seen.add(u);todo.append(u)
 parts.append(part)
if len(parts)>1:
 parts.sort(key=len,reverse=True);bmesh.ops.delete(bm,geom=[v for p in parts[1:] for v in p],context='VERTS')
bm.to_mesh(body.data);bm.free()
body.data.calc_loop_triangles();initial_tri=len(body.data.loop_triangles)
for m in M:body.data.materials.append(m)
def back_top(y):
 pairs=[(-.35,.35),(-.23,.39),(-.05,.38),(.16,.352),(.31,.30),(.4,.26)]
 for (a,za),(b,zb) in zip(pairs,pairs[1:]):
  if a<=y<=b:return za+(zb-za)*(y-a)/(b-a)
 return .35 if y<-.35 else .26
for poly in body.data.polygons:
 c=poly.center;x,y,z=c
 if -.32<y<.39 and abs(x)<.06 and z>back_top(y)+.014:
  # Quiet spine rhythm is planar geometry, never false bony rods.
  poly.material_index=2
 else:poly.material_index=1 if z<(.165 if -.34<y<.36 else .10) else 0
 poly.use_smooth=False
dec=body.modifiers.new('Anatomical plane economy','DECIMATE');dec.ratio=min(1,5500/initial_tri);dec.use_collapse_triangulate=True;dec.delimit={'MATERIAL'};bpy.ops.object.modifier_apply(modifier=dec.name)
# Cut material-zone boundaries into the final economy mesh: palette edges are
# coherent contours, not arbitrary whole-triangle color spikes. Original surface
# shape is unchanged; cuts only subdivide intersected faces.
def partition_zone(ob,scalar,material):
 vs=[tuple(v.co) for v in ob.data.vertices];polys=[(list(p.vertices),p.material_index) for p in ob.data.polygons];cache={};out=[]
 def value(i):return scalar(Vector(vs[i]))
 def intersection(a,b,ga,gb):
  if abs(ga)<1e-10:return a
  if abs(gb)<1e-10:return b
  key=tuple(sorted([a,b]))
  if key not in cache:
   va,vb=Vector(vs[a]),Vector(vs[b]);cache[key]=len(vs);vs.append(tuple(va+(vb-va)*(ga/(ga-gb))))
  return cache[key]
 for indices,oldmat in polys:
  vals=[value(i) for i in indices]
  if min(vals)>=0:out.append((indices,material));continue
  if max(vals)<=0:out.append((indices,oldmat));continue
  for positive in [True,False]:
   poly=[]
   for j,a in enumerate(indices):
    b=indices[(j+1)%len(indices)];ga,gb=vals[j],vals[(j+1)%len(indices)];ia=ga>=0 if positive else ga<=0;ib=gb>=0 if positive else gb<=0
    if ia:poly.append(a)
    if ia!=ib:poly.append(intersection(a,b,ga,gb))
   # Avoid zero length edges at exactly-on-boundary vertices.
   clean=[]
   for a in poly:
    if not clean or clean[-1]!=a:clean.append(a)
   if len(clean)>1 and clean[0]==clean[-1]:clean.pop()
   if len(clean)>=3:out.append((clean,material if positive else oldmat))
 me=bpy.data.meshes.new(ob.name+' palette contour mesh');me.from_pydata(vs,[],[p for p,m in out]);me.update()
 for m in M:me.materials.append(m)
 for p,(_,m) in zip(me.polygons,out):p.material_index=m;p.use_smooth=False
 old=ob.data;ob.data=me;bpy.data.meshes.remove(old)
for p in body.data.polygons:p.material_index=0
partition_zone(body,lambda v:min(v.z-back_top(v.y)-.008,.39-v.y,v.y+.32,.06-abs(v.x)),2)
partition_zone(body,lambda v:min(.16-v.z,.35-v.y,v.y+.34),1)
# Small embedded details, not free-floating shell pieces.
def ellipsoid(name,loc,scale,material,segments=10,rings=6):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=rings,location=loc);o=bpy.context.object;o.name=name;o.scale=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for col in list(o.users_collection):col.objects.unlink(o)
 COL.objects.link(o);o.data.materials.append(M[material]);features.append(o);return o
# Interior sits behind the jaw lips, with the unioned jaw hinge closing the rear.
ellipsoid('Recessed oral cavity',(0,-.522,.256),(.058,.099,.026),4,12,8)
for s in [-1,1]:
 tag='L' if s<0 else 'R'
 ellipsoid('Recessed eye '+tag,(s*.085,-.442,.379),(.0065,.013,.0105),4)
 ellipsoid('Warm iris '+tag,(s*.091,-.444,.379),(.0018,.0065,.006),2)
 ellipsoid('Pupil '+tag,(s*.0925,-.446,.379),(.001,.0035,.004),4)
 ellipsoid('Nostril '+tag,(s*.0415,-.615,.342),(.004,.009,.004),4,10,6)
# Bent tapered cones, differentiated upper canine + modest unequal small teeth.
def pointed(name,pts,radii,material,n=7):
 vs=[];fs=[]
 for i in [0,1]:
  p=Vector(pts[i]);t=(Vector(pts[2])-Vector(pts[0])).normalized();ref=Vector((0,0,1)) if abs(t.z)<.93 else Vector((0,1,0));u=t.cross(ref).normalized();v=t.cross(u).normalized()
  for j in range(n):
   a=2*math.pi*j/n;vs.append(tuple(p+u*radii[i]*math.cos(a)+v*radii[i]*.8*math.sin(a)))
 vs.append(tuple(pts[2]))
 for j in range(n):fs.extend([(j,(j+1)%n,n+(j+1)%n,n+j),(n+j,n+(j+1)%n,2*n)])
 fs.append(tuple(reversed(range(n))))
 o=mesh_obj(name,vs,fs);o.data.materials.append(M[material]);features.append(o);return o
# Anchor each tooth in the lower lateral surface of the lofted maxilla.
# Exposed lengths are visibly differentiated; count is artistic simplification.
head_sections=[(-.644,.293,.339,.022),(-.627,.279,.36,.043),(-.592,.272,.378,.058),(-.552,.266,.391,.068),(-.515,.26,.401,.076),(-.47,.261,.416,.085),(-.426,.251,.425,.098),(-.383,.236,.397,.096),(-.34,.233,.362,.072)]
def maxilla_edge(y,x):
 for (y0,b0,t0,w0),(y1,b1,t1,w1) in zip(head_sections,head_sections[1:]):
  if y0<=y<=y1:
   f=(y-y0)/(y1-y0);b=b0+(b1-b0)*f;t=t0+(t1-t0)*f;w=w0+(w1-w0)*f
   cos=min(abs(x)/w,.999)**(1/.82);sin=(1-cos*cos)**.5
   return (b+t)/2-(t-b)/2*sin**.82
for s in [-1,1]:
 for i,(y,x,length,r) in enumerate([(-.611,.038,.016,.004),(-.583,.051,.020,.0048),(-.548,.062,.052,.0095),(-.509,.067,.021,.004),(-.482,.073,.016,.0035),(-.459,.078,.012,.003)]):
  z=maxilla_edge(y,x)
  pointed(f'Upper tooth {s} {i}',[(s*x*.78,y,z+.014),(s*x*.90,y+.002,z-.004),(s*x*.90,y+.005,z-length)],[r*.78,r*.70,.00035],5)
 for i,(y,x) in enumerate([(-.599,.043),(-.567,.055),(-.525,.060)]):
  pointed(f'Lower tooth {s} {i}',[(s*x*.78,y,.232),(s*x*.96,y-.001,.246),(s*x,y-.002,.253)],[.0035,.0027,.0003],5)
for f in foot_specs:
 p=Vector(f['tip']);d=Vector(f['direction']).normalized();start=p-d*.012;end=p+d*.015;end.z=.007
 pointed(f"Claw {f['limb']} {f['side']} {f['digit']}",[start,p+d*.002,end],[f['radius']*.45,f['radius']*.38,.0005],5,7)
# Pack accessory details by material to keep portable draws deliberately small.
feature_groups={material:[o for o in features if o.data.materials[0]==M[material]] for material in range(len(M))}
for material,group in feature_groups.items():
 if not group:continue
 bpy.ops.object.select_all(action='DESELECT')
 for o in group:o.select_set(True)
 bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();group[0].name={2:'Eyes iris inlays',4:'Dark recessed features',5:'Differentiated teeth and twenty claws'}[material]
assets=[o for o in COL.objects if o.type=='MESH']
# Ground at lowest foot and uniform whole-model normalization to 1.8 m nose-tail art length.
coords=[o.matrix_world@v.co for o in assets for v in o.data.vertices]
lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)];sc=1.8/(hi[1]-lo[1]);ground=min(v.z for v in coords if abs(v.x)>.16 and v.z<.07)
for o in assets:
 for v in o.data.vertices:
  v.co=o.matrix_world@v.co;v.co.z-=ground;v.co*=sc
 o.matrix_world.identity()
 o['taxon']='Dimetrodon';o['representation']='D. milleri-inspired adult art reconstruction';o['source_limit']='Not exact species/specimen restoration; soft tissue, colors, pose, scale artistic'
# Stable coordinates and winding-preserving face order are generated from THIS RUN only.
for o in assets:
 canonical_mesh(o)
 canonical_mesh(o,triangulate=True)
# Authorized minimal r002 sliver repair, default shared QA thresholds NOT weakened.
# Collapse only the shortest edge of a sub-1e-10 m^2 triangle, to an existing endpoint.
# All retained vertex coordinates remain unchanged; record every local change.
def repair_micro_slivers(obj):
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));repairs=[]
 before_vertices=len(bm.verts);before_faces=len(bm.faces)
 for attempt in range(8):
  small=[f for f in bm.faces if f.calc_area()<1e-10]
  if not small:break
  f=min(small,key=lambda f:(f.calc_area(),sorted(tuple(v.co) for v in f.verts)))
  e=min(f.edges,key=lambda e:(e.calc_length(),sorted(tuple(v.co) for v in e.verts)))
  pair=sorted(e.verts,key=lambda v:tuple(v.co));target=pair[0].co.copy()
  repairs.append({'triangle_positions_before':[list(v.co) for v in f.verts],'area_before_m2':f.calc_area(),'merged_vertex_positions':[list(v.co) for v in pair],'retained_endpoint':list(target),'maximum_merged_vertex_displacement_m':e.calc_length(),'material_index':f.material_index})
  bmesh.ops.pointmerge(bm,verts=pair,merge_co=target)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 else:raise RuntimeError('Micro-sliver repair exceeded minimal bounded edit budget')
 if any(f.calc_area()<1e-10 for f in bm.faces):raise RuntimeError('Source micro-sliver persists')
 info={'revision':'r002','scope':'Minimal topology repair plus EXPORT/root packaging; not strict geometry identity','shared_thresholds_unmodified':True,'triangle_area_threshold_m2':1e-10,'vertices_before':before_vertices,'vertices_after':len(bm.verts),'triangles_before':before_faces,'triangles_after':len(bm.faces),'repairs':repairs,'max_vertex_displacement_m':max((x['maximum_merged_vertex_displacement_m'] for x in repairs),default=0),'all_retained_coordinates_are_original_endpoints':True}
 bm.to_mesh(obj.data);bm.free();obj.data.update();canonical_mesh(obj,triangulate=True)
 (ROOT/'evidence').mkdir(exist_ok=True)
 (ARTIFACT_ROOT/'topology-repair.json').write_text(json.dumps(info,indent=2))
 return info
repair_info=repair_micro_slivers(body)
bpy.context.view_layer.update()
# r002 packaging: unchanged retained coordinates plus recorded one-edge microscopic repair.

for o in assets:common.link_object(o,COL,parent=True)
root=bpy.data.objects[COL['asset_root']]
root['revision']='r002'
# Raw source objects retained offstage and not export-selected, in unnormalized author units.
RAW.hide_render=True;RAW.hide_viewport=True
scene['scientific_scope']='Non-mammalian synapsid, not dinosaur. Genus asset. Conservative milleri-inspired adult art form.'
scene['scale_note']='1.8 m nose-tail nominal artistic scale, not fossil measurement.'
scene['raw_lofts_to_final_transform']=json.dumps({'uniform_scale':sc,'raw_ground_offset':ground})
scene['generation_limit']='Pinned 4.3.2/four-thread full builds tested separately for byte equality after canonical ordering. No cross-version determinism claim.'
if GRAY:
 for o in assets:
  o.data.materials.clear();o.data.materials.append(gray)
  for p in o.data.polygons:p.material_index=0
out=ROOT/'graybox' if GRAY else ARTIFACT_ROOT
blend=out/('dimetrodon-graybox.blend' if GRAY else 'dimetrodon-r002.blend')
bpy.ops.object.select_all(action='DESELECT')
for o in assets:o.select_set(True)
bpy.context.view_layer.objects.active=body
if GRAY:
 bpy.ops.wm.save_as_mainfile(filepath=str(blend))
else:
 # Shared helper owns source QA, fixed static export flags, isolation, bounds checks and output metadata.
 common.export_asset('dimetrodon',{'en':'Dimetrodon — D. milleri-inspired adult form','zh':'异齿龙（D. milleri 启发成年形态）'},'animals',COL,
  metadata={'revision':'r002','representation':'living-reconstruction','generator':'scripts/build_dimetrodon.py','description':{'en':'Original art reconstruction; root packaging and recorded microscopic topology repair of r001, not a species-exact restoration.','zh':'原创新复原模型；r001 包结构修订，并非物种精确复原。'},'reconstruction_notes':'Scale, soft tissues, colors and pose artistic. Harvard D. milleri inspired; Gilmore supplementary genus context only.'},
  output_root=ARTIFACT_ROOT/'helper-export',render=False,max_triangles=12000,max_materials=8,max_primitives=48)
 # Canonical handoff aliases are copies of THIS RUN helper outputs, never cached geometry inputs.
 helper_dir=ARTIFACT_ROOT/'helper-export/dimetrodon'
 shutil.copyfile(helper_dir/'dimetrodon.blend',ARTIFACT_ROOT/'dimetrodon-r002.blend')
 shutil.copyfile(helper_dir/'dimetrodon.glb',ARTIFACT_ROOT/'dimetrodon-r002.glb')
coords=[o.matrix_world@v.co for o in assets for v in o.data.vertices]
lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
report={'asset':'dimetrodon','revision':'r002','blender':bpy.app.version_string,'graybox':GRAY,'bounds_min':lo,'bounds_max':hi,'dimensions_m':[hi[i]-lo[i] for i in range(3)],'meshes':len(assets),'source_lofts':len(raw),'initial_union_triangles':initial_tri,'triangle_count':sum(len(o.data.loop_triangles) if (o.data.calc_loop_triangles() is None) else 0 for o in assets),'raw_to_final_uniform_scale':sc,'ground_offset':ground,'feet':4,'toe_rays_per_foot':5,'nominal_scale_is_artistic':True,'canonical_mesh_ordering':True,'generator_byte_equality_test_required':True}
(ROOT/'evidence'/('graybox-build-metadata.json' if GRAY else (REBUILD_TAG+'-metadata.json' if REBUILD else 'final-build-metadata.json'))).write_text(json.dumps(report,indent=2))
print('BUILD_COMPLETE',json.dumps(report),flush=True)
if GRAY and RENDER:
 exec(compile((ROOT/'scripts/render_views.py').read_text(),str(ROOT/'scripts/render_views.py'),'exec'))
 manifest=render_views(assets,ROOT/'graybox',samples=24)
 (ROOT/'evidence/graybox-view-manifest.json').write_text(json.dumps(manifest,indent=2))
