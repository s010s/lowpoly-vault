"""Original Rhamphorhynchus r002, procedural evidence-informed art. No input mesh.
Usage: blender -b -t 4 --python scripts/build_rhamphorhynchus.py -- graybox|final [out_root]
All geometry is constructed below from numerical art parameters, not from saved GLB/Blend.
"""
import bpy,bmesh,math,json,sys,hashlib
from mathutils import Vector
from pathlib import Path
SOURCE_ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SOURCE_ROOT/'scripts'))
import asset_common as common
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
CONFIG_PATH=SOURCE_ROOT/'generator-config.json'
if '--config' in args:
 k=args.index('--config');CONFIG_PATH=Path(args[k+1]).resolve();args=args[:k]+args[k+2:]
CONFIG=json.loads(CONFIG_PATH.read_text())
assert bpy.app.version_string==CONFIG['blender_version']
STAGE=args[0] if args else 'graybox';ROOT=Path(args[1]).resolve()/'rhamphorhynchus-r002' if len(args)>1 else SOURCE_ROOT
for part in ['graybox','final','evidence','logs']:(ROOT/part).mkdir(parents=True,exist_ok=True)
export_collection=common.setup_scene('rhamphorhynchus',CONFIG['seed'])
asset_root=bpy.data.objects[export_collection['asset_root']]
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.threads_mode='FIXED';scene.render.threads=CONFIG['blender_threads']
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=CONFIG['render']['gray_samples' if STAGE=='graybox' else 'final_samples'];scene.cycles.use_denoising=False
scene.render.resolution_x=CONFIG['render']['width'];scene.render.resolution_y=CONFIG['render']['height'];scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
scene.world=bpy.data.worlds.new('Neutral QA world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.23,.27,.31,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
ASSETS=[]
def mat(name,col,rough=.83):
 m=bpy.data.materials.new(name);m.diffuse_color=(*col,1);m.use_nodes=True;m.use_backface_culling=True
 p=m.node_tree.nodes['Principled BSDF'];p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=0
 return m
def srgb(s):
 c=[int(s[i:i+2],16)/255 for i in (0,2,4)];return [x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in c]
M=[common.make_material(n,'#'+c,roughness=.83,double_sided=False) for n,c in zip(['Muted warm grey body','Pale ventral skin','Subdued ochre membrane','Dark membrane margin','Eye and nostril','Ivory dentition and claws'],CONFIG['palette_srgb_hex'])]
CLAY=common.make_material('True neutral graybox clay','#929292',roughness=.85)
def recalc(ob):
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(ob.data);bm.free();ob.data.update()
def mesh(name,vs,fs,mi=0):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();ob=bpy.data.objects.new(name,me);scene.collection.objects.link(ob);me.materials.append(M[mi]);ASSETS.append(ob);recalc(ob);return ob
def loft_y(name,rows,n=20,mi=0):
 vs=[];fs=[]
 for y,z,w,up,down in rows:
  for j in range(n):
   a=math.tau*j/n;s=math.sin(a);vs.append((math.cos(a)*w,y,z+s*(up if s>=0 else down)))
 for i in range(len(rows)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 fs.extend([tuple(range(n-1,-1,-1)),tuple((len(rows)-1)*n+j for j in range(n))]);return mesh(name,vs,fs,mi)
def tube(name,rows,n=10,mi=0):
 vs=[];fs=[]
 for i,(x,y,z,rx,ry) in enumerate(rows):
  p=Vector((x,y,z));t=(Vector(rows[min(i+1,len(rows)-1)][:3])-Vector(rows[max(0,i-1)][:3])).normalized()
  u=Vector((0,0,1)) if abs(t.z)<.9 else Vector((1,0,0));u=(u-t*u.dot(t)).normalized();v=t.cross(u).normalized()
  for j in range(n):
   a=math.tau*j/n;vs.append(tuple(p+u*(math.cos(a)*rx)+v*(math.sin(a)*ry)))
 for i in range(len(rows)-1):
  for j in range(n):fs.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 fs.extend([tuple(range(n-1,-1,-1)),tuple((len(rows)-1)*n+j for j in range(n))]);return mesh(name,vs,fs,mi)
def ellipsoid(name,loc,sc,mi,seg=16,rings=8):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,radius=1,location=loc);ob=bpy.context.object;ob.name=name;ob.scale=sc;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);ob.data.materials.append(M[mi]);ASSETS.append(ob);return ob
def combine(obs,name):
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();o=obs[0];o.name=name
 for x in obs[1:]:ASSETS.remove(x)
 return o
def canonical_mesh(obj,triangulate=False):
 old=obj.data
 if triangulate:
  old.calc_loop_triangles();raw=[(tuple(t.vertices),old.polygons[t.polygon_index].material_index) for t in old.loop_triangles]
 else:raw=[(tuple(p.vertices),p.material_index) for p in old.polygons]
 coords=[tuple(float(x) for x in v.co) for v in old.vertices];ordered=sorted(set(coords));lookup={c:i for i,c in enumerate(ordered)};idx=[lookup[c] for c in coords];faces=[]
 for vv,mi in raw:
  f=tuple(idx[i] for i in vv);f=min(f[k:]+f[:k] for k in range(len(f)));faces.append((mi,f))
 faces.sort(key=lambda x:(x[0],x[1]));name=old.name;mats=list(old.materials);me=bpy.data.meshes.new(name+'__ordered');me.from_pydata(ordered,[],[f for _,f in faces]);me.update()
 for m in mats:me.materials.append(m)
 for p,(mi,_) in zip(me.polygons,faces):p.material_index=mi;p.use_smooth=False
 obj.data=me
 if old.users==0:bpy.data.meshes.remove(old)
 me.name=name
# Quiet continuous compact trunk, short neck, and thin reinforced-looking tail.
BODY=[(-.153,.087,.010,.013,.012),(-.140,.087,.015,.016,.014),(-.122,.080,.017,.016,.014),(-.105,.071,.019,.019,.017),(-.085,.068,.024,.025,.022),(-.060,.067,.031,.029,.026),(-.030,.066,.033,.027,.029),(.005,.065,.030,.024,.026),(.035,.065,.025,.021,.021),(.060,.067,.019,.017,.016),(.080,.068,.011,.010,.010),(.100,.070,.0065,.0063,.0063),(.145,.072,.0046,.0047,.0047),(.200,.073,.0037,.0038,.0038),(.260,.073,.0030,.0031,.0031),(.320,.073,.0023,.0025,.0025),(.365,.073,.0018,.0020,.0020),(.407,.073,.0013,.0015,.0015),(.430,.073,.0006,.0007,.0007)]
body=loft_y('Continuous compact trunk short neck and long tail',BODY,24)
body.data.materials.append(M[1])
for p in body.data.polygons:p.material_index=1 if p.normal.z<-.40 else 0
# Slender head with distinct cranium, toothless tip, and restrained open jaw.
HEAD=[(-.258,.090,.0013,.0013,.0010),(-.248,.090,.003,.0025,.0020),(-.235,.092,.0048,.0048,.0035),(-.217,.094,.0068,.0070,.0050),(-.196,.096,.0085,.010,.0065),(-.177,.098,.0120,.0140,.0095),(-.160,.099,.017,.018,.014),(-.146,.096,.017,.017,.015),(-.138,.090,.010,.011,.010)]
head=loft_y('Slender cranium and pointed upper toothed jaw',HEAD,20)
JAW=[(-.253,.069,.001,.0013,.0010),(-.241,.068,.003,.0020,.002),(-.222,.068,.005,.0025,.003),(-.201,.071,.0068,.0035,.0037),(-.181,.075,.009,.0045,.0045),(-.161,.081,.012,.005,.006),(-.146,.088,.013,.007,.008)]
jaw=loft_y('Relaxed slender lower jaw',JAW,16,1)
for s in [-1,1]:
 ellipsoid(f'{s} flush orbital eye',(.0155*s,-.157,.104),(.0035,.006,.0058),4,16,8)
 ellipsoid(f'{s} nostril',(.0054*s,-.226,.0965),(.0011,.0023,.0016),4,12,6)
# r002: query each REAL closed faceted jaw surface, then place a basal ring inside it.
# This is not a bbox proxy: skin contact and roots are checked again on exactGLB.
TOOTH_ROOT_RECORDS=[]
def implant_root(jaw_object,rows,y,side,upper,old_base):
 a,b=next((a,b) for a,b in zip(rows,rows[1:]) if a[0]<=y<=b[0])
 t=(y-a[0])/(b[0]-a[0]);width=a[2]+(b[2]-a[2])*t;x=side*width*.60
 ray_origin=Vector((x,y,-.1 if upper else .3));ray_direction=Vector((0,0,1 if upper else -1))
 hit,skin,normal,face=jaw_object.ray_cast(ray_origin,ray_direction)
 if not hit:raise RuntimeError('No actual tooth-root jaw hit')
 root=skin-normal*CONFIG['dentition_root_embedding_m']
 TOOTH_ROOT_RECORDS.append({'jaw':jaw_object.name,'upper':upper,'side':side,'old_base':list(old_base),'skin_hit_pre_datum':list(skin),'outward_normal':list(normal),'embedded_root_pre_datum':list(root),'embed_m':CONFIG['dentition_root_embedding_m']})
 return tuple(root),tuple(skin)
def embedded_cone(root,tip,radius,tip_radius):
 # Retain original terminal position and its anteriorly angled upper/lower direction.
 # One continuously tapering conical centerline avoids an elbow at the former floating base.
 a,b=Vector(root),Vector(tip)
 return [(*tuple(a+(b-a)*t),radius*(1-t)+tip_radius*t,radius*(1-t)+tip_radius*t) for t in [0,.20,.43,.70,1]]
# Teeth: deliberately sparse, with toothless jaw tips. Count is artistic, not dental formula.
teeth=[]
for s in [-1,1]:
 for i,y in enumerate([-.234,-.220,-.206,-.192,-.178]):
  # Basal coordinates sit within upper jaw underside; oblique crown points anteriorly/down.
  t=(-y-.178)/.056;x=(.009-.004*t)*s;z=.088-.001*t;length=.008+.004*t
  root,skin=implant_root(head,HEAD,y,s,True,(x,y,z))
  teeth.append(tube(f'{s} upper conical tooth {i+1}',embedded_cone(root,(x*1.07,y-.004,z-length),.00145,.00018),7,5))
 for i,y in enumerate([-.227,-.213,-.199,-.185]):
  x=(.005+(.227+y)*.075)*s;z=.070+(.227+y)*.18;length=.0075
  root,skin=implant_root(jaw,JAW,y,s,False,(x,y,z))
  teeth.append(tube(f'{s} lower interleaving conical tooth {i+1}',embedded_cone(root,(x,y-.003,z+length),.00115,.00015),7,5))
combine(teeth,'Sparse interleaving dentition')
# Wings: ONE closed continuous volumetric surface per side. Leading skin thickness
# encompasses arm/wingfinger; no internal bat fingers, detached sails, or flat two-sided card.
sections=CONFIG['wing_sections'];chords=[0,.035,.08,.16,.28,.44,.61,.77,.90,.97,1]
wing_records=[]
for s in [-1,1]:
 rows=[]
 for a,b in zip(sections,sections[1:]):
  for j in range(3):rows.append([a[k]+(b[k]-a[k])*(j/3) for k in range(6)])
 rows.append(sections[-1]);vs=[];fs=[];n=len(chords)
 for x,le,te,zl,zt,r in rows:
  for side_z in [1,-1]:
   for q in chords:
    y=le+(te-le)*q;z=zl+(zt-zl)*q+.006*math.sin(math.pi*q)*(1-x/.65)
    half=.001+max(0,r-.001)*math.exp(-q*19)
    if x>.565:half*=max(.33,(.605-x)/.04)
    vs.append((s*x,y,z+side_z*half))
 for i in range(len(rows)-1):
  for k in range(2):
   for j in range(n-1):
    a=i*2*n+k*n+j;b=(i+1)*2*n+k*n+j;fs.append((a,a+1,b+1,b))
  for j in [0,n-1]:
   a=i*2*n+j;b=(i+1)*2*n+j;fs.append((a,b,b+n,a+n))
 for i in [0,len(rows)-1]:
  for j in range(n-1):a=i*2*n+j;fs.append((a,a+n,a+n+1,a+1))
 wing=mesh(('Left' if s<0 else 'Right')+' integrated closed ankle-attached wing',vs,fs,2);wing.data.materials.append(M[3]);wing.data.materials.append(M[0])
 for p in wing.data.polygons:
  # Parameter-space zoning stays continuous around the span; nearest-ring spatial
  # tests produce alternating blocks on swept edges and are intentionally avoided.
  q=sum(chords[int(idx)%n] for idx in p.vertices)/len(p.vertices)
  p.material_index=1 if q>=.935 else (2 if q<=.035 else 0)
 wing_records.append({'side':s,'object':wing.name,'wrist':[s*.17,-.095,.085],'ankle_attachment':[s*.075,.125,.038],'wingfinger_tip':[s*.60,.0745,.13],'free_digits':3})
 # Three small wrist digits ahead of leading edge; kept modest beside long digit IV.
 fingers=[];claws=[]
 for i,(dx,l) in enumerate([(-.009,.019),(0,.023),(.010,.018)]):
  x=(.17+dx)*s;y=-.094+abs(dx)*.28;z=.085
  fingers.append(tube(f'{s} free wrist digit {i+1}',[(x,y,z,.0022,.0022),(x+dx*.15*s,y-l*.55,z-.0005,.0017,.0017),(x+dx*.30*s,y-l,z-.002,.0011,.0011)],8))
  claws.append(tube(f'{s} wrist claw {i+1}',[(x+dx*.30*s,y-l+.001,z-.002,.0012,.0012),(x+dx*.35*s,y-l-.003,z-.004,.0008,.0008),(x+dx*.35*s,y-l-.004,z-.007,.00018,.00018)],7,5))
 combine(fingers,('Left' if s<0 else 'Right')+' three free manual digits');combine(claws,('Left' if s<0 else 'Right')+' three tiny manual claws')
 # Hindlimb only: attached from pelvic surface, small angled shank and trailing feet.
 tube(('Left' if s<0 else 'Right')+' hindleg',[(s*.016,.045,.064,.009,.010),(s*.039,.074,.044,.007,.008),(s*.049,.087,.035,.005,.005),(s*.061,.110,.035,.004,.004),(s*.075,.125,.038,.0035,.0035)],12)
 toes=[];tclaws=[]
 for i,(dx,L) in enumerate([(-.008,.018),(-.003,.023),(.003,.022),(.008,.017)]):
  x=s*(.075+dx);y=.128;z=.037
  toes.append(tube(f'{s} pedal ray {i+1}',[(s*(.075+dx*.25),y-.005,z,.0019,.0019),(x,y+L*.5,z-.002,.0015,.0015),(x+dx*s*.3,y+L,z-.003,.0009,.0009)],8))
  tclaws.append(tube(f'{s} pedal claw {i+1}',[(x+dx*s*.3,y+L-.001,z-.003,.001,.001),(x+dx*s*.4,y+L+.004,z-.005,.0006,.0006),(x+dx*s*.4,y+L+.005,z-.007,.00015,.00015)],7,5))
 toes.append(tube(f'{s} modest fifth pedal ray',[(s*.073,.124,.037,.0017,.0017),(s*.059,.140,.036,.0013,.0013),(s*.047,.145,.037,.0005,.0005)],8))
 combine(toes,('Left' if s<0 else 'Right')+' four pedal rays and fifth support');combine(tclaws,('Left' if s<0 else 'Right')+' four small pedal claws')
 # Conservative interpretive hind-membrane lobe. Small central extent, not a bat-tail fan.
 outline=[(s*.008,.060,.060),(s*.034,.077,.045),(s*.055,.108,.036),(s*.072,.125,.037),(s*.057,.141,.036),(s*.043,.142,.037),(s*.024,.122,.047),(s*.005,.100,.064)]
 c=sum((Vector(v) for v in outline),Vector())/len(outline);vv=[];ff=[]
 for dz in [-.0009,.0009]:
  vv.extend([(v[0],v[1],v[2]+dz) for v in outline]);vv.append(tuple(c+Vector((0,0,dz))))
 for i in range(8):ff.extend([(i,(i+1)%8,8),(9+i,17,9+(i+1)%8),(i,9+i,9+(i+1)%8,(i+1)%8)])
 mesh(('Left' if s<0 else 'Right')+' small interpretive hind membrane',vv,ff,2)
# Vane: sagittal/vertical closed leaf, broadest slightly distal of centre.
vane=loft_y('Vertical diamond tail vane',[(.355,.073,.0010,.0017,.0017),(.365,.073,.0012,.007,.007),(.380,.073,.0015,.015,.015),(.397,.073,.0017,.0225,.0225),(.404,.073,.0016,.021,.021),(.417,.073,.0012,.011,.011),(.429,.073,.0007,.0012,.0012),(.431,.073,.0004,.0004,.0004)],16,2)
# All unique static shapes are baked at identity; translate only vertical datum.
bpy.context.view_layer.update();coords=[o.matrix_world@v.co for o in ASSETS for v in o.data.vertices];lowest=min(v.z for v in coords)
for o in ASSETS:
 for v in o.data.vertices:v.co.z-=lowest
 o['asset_id']='rhamphorhynchus';o['revision']='r002';o['original_geometry']=True
 canonical_mesh(o);canonical_mesh(o,True)
bpy.context.view_layer.update();coords=[o.matrix_world@v.co for o in ASSETS for v in o.data.vertices];lo=Vector([min(v[i] for v in coords) for i in range(3)]);hi=Vector([max(v[i] for v in coords) for i in range(3)])
centerline=[(0,-.258,.09),(0,-.146,.096)]+[(0,r[0],r[1]) for r in BODY[1:]]
metadata={'asset_id':'rhamphorhynchus','revision':'r002','stage':STAGE,'blender':bpy.app.version_string,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest(),'wingspan_m':hi.x-lo.x,'nose_tail_centerline_m':sum((Vector(b)-Vector(a)).length for a,b in zip(centerline,centerline[1:])),'nominal_head_length_m':.12,'nominal_body_neck_length_m':.20,'tail_axis_length_m':.35,'vane_length_m':.076,'vane_height_m':.045,'dimensions_m':list(hi-lo),'bounds_min_blender_xyz':list(lo),'bounds_max_blender_xyz':list(hi),'datum_z_translation_m':-lowest,'wing_records':wing_records,'tooth_root_records':TOOTH_ROOT_RECORDS,'mesh_objects':len(ASSETS),'triangles':sum(len(o.data.polygons) for o in ASSETS),'materials':6,'source_axes':CONFIG['source_axes'],'scientific_limits':CONFIG['uncertainties'],'membrane_thickness_note':'Main membrane full thickness 2mm, leading arm skin deliberately thicker; terminal edge tapers to .66mm, not zero-area sheet. Vane thickness 0.8–3.4mm.'}
# Source-native production hierarchy: one identity empty and EXPORT collection.
asset_root['asset_id']='rhamphorhynchus';asset_root['revision']='r002';asset_root['unit']='meter';asset_root['mounting_origin']='Static airborne lowest-surface datum, not ground contact.'
for ob in ASSETS:common.link_object(ob,export_collection,parent=True)
metadata['source_hierarchy']={'collection':'EXPORT','root':'rhamphorhynchus','root_identity':True,'mesh_descendants':len(ASSETS)}
(ROOT/'evidence'/f'{STAGE}-build-metadata.json').write_text(json.dumps(metadata,indent=2))
if STAGE=='graybox':
 for o in ASSETS:
  o.data.materials.clear();o.data.materials.append(CLAY)
  for p in o.data.polygons:p.material_index=0
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'graybox/rhamphorhynchus-graybox.blend'))
else:
 common.export_asset('rhamphorhynchus-r002',{'en':'Rhamphorhynchus muensteri-inspired form','zh':'喙嘴翼龙（R. muensteri 启发形态）'},'animals',export_collection,metadata={'description':{'en':'Original evidence-informed static gliding reconstruction; not specimen-exact or aerodynamically validated.','zh':'原创证据参考静态滑翔重建；非标本复制或空气动力学验证。'},'generator':'scripts/build_rhamphorhynchus.py','origin_note':'Airborne lowest-surface datum; no flight-height or foot contact claim.','scientific_limits':CONFIG['uncertainties'],'sources':json.loads((SOURCE_ROOT/'references.json').read_text())['sources']},output_root=ROOT.parent,render=False,max_triangles=12000,max_materials=8,max_primitives=48,diagnostics=False)
 (ROOT/'evidence/shared-source-audit.json').write_text(json.dumps(common.audit_source(export_collection,12000),indent=2))
def render_views(assets,folder):
 collection=assets[0].users_collection[0]
 if collection.name!='EXPORT':
  collection=bpy.data.collections.new('EXPORT');scene.collection.children.link(collection)
  for ob in assets:
   for old in list(ob.users_collection):old.objects.unlink(ob)
   collection.objects.link(ob)
 paths=common.render_previews(collection,folder,views=('front','side','top','perspective'),resolution=1024,samples=scene.cycles.samples,transparent=False,floor_enabled=False)
 manifest=[]
 for record,old_path in zip(common.LAST_VIEW_RECORDS,paths):
  old=Path(old_path);p=folder/(record['view']+'.png');old.replace(p)
  manifest.append({**record,'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'color_management':'Standard / None; exposure 0; gamma 1','shared_helper_sha256':hashlib.sha256((SOURCE_ROOT/'scripts/asset_common.py').read_bytes()).hexdigest(),'background_srgb':'#E8E4DC','lighting':'Repository shared key/fill preset','no_floor':'Airborne static asset, no height claim'})
 return manifest
if STAGE=='graybox':(ROOT/'evidence/graybox-view-manifest.json').write_text(json.dumps(render_views(ASSETS,ROOT/'graybox'),indent=2))
print('BUILD_COMPLETE',json.dumps(metadata),flush=True)
