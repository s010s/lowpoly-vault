# SPDX-License-Identifier: MIT
"""Original Amphicyon reconstruction. Run with Blender --python and -- --output DIR.
The frozen parameters are qualitative reconstruction targets, not specimen metrics.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source,link_object,render_previews
from qa_glb import audit_glb

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
args=argparse.ArgumentParser();args.add_argument('--output',type=Path,required=True);args.add_argument('--clay',action='store_true')
args=args.parse_args(sys.argv[sys.argv.index('--')+1:]);OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
P=json.loads((HERE/'params.json').read_text());C=setup_scene('amphicyon',P['seed']);root=bpy.data.objects[C['asset_root']]
scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
M={n:make_material(n,col,roughness=.88) for n,col in P['palette_srgb'].items()}
construct=bpy.data.collections.new('EDITABLE_PROFILE_CONSTRUCTION');scene.collection.children.link(construct)
parts=[]
# All input sections are designed contours, retained separately in the source.
def loft(name,sections,n=16,axis='Y'):
 vs=[];fs=[]
 for c,a,b in sections:
  for j in range(n):
   t=2*math.pi*j/n
   if axis=='Y':vs.append((c[0]+a*math.cos(t),c[1],c[2]+b*math.sin(t)))
   else:vs.append((c[0]+a*math.cos(t),c[1]+b*math.sin(t),c[2]))
 for i in range(len(sections)-1):
  for j in range(n):
   k=i*n+j;l=i*n+(j+1)%n;fs.append((k,l,l+n,k+n))
 fs += [tuple(reversed(range(n))),tuple((len(sections)-1)*n+j for j in range(n))]
 ob=mesh_object(name,vs,fs,M['coat'],C);parts.append(ob);return ob
# Elongate trunk: deep chest, slightly tucked abdomen and broad haunches.
loft('trunk',[( (0,y,z),rx,rz) for y,z,rx,rz in [(-.67,.65,.12,.16),(-.56,.64,.215,.235),(-.40,.64,.255,.25),(-.16,.62,.27,.25),(.10,.615,.25,.235),(.33,.62,.235,.22),(.52,.62,.24,.235),(.67,.62,.185,.19),(.75,.59,.115,.125),(.80,.56,.055,.07)]],24)
loft('neck',[( (0,y,z),rx,rz) for y,z,rx,rz in [(-.51,.66,.21,.22),(-.66,.72,.177,.185),(-.79,.77,.145,.15),(-.91,.80,.115,.125)]],20)
# Broad temporal area flows into a distinctly lengthened, modestly low rostrum.
loft('cranial-profile',[( (0,y,z),rx,rz) for y,z,rx,rz in [(-.79,.81,.09,.115),(-.88,.825,.13,.132),(-.97,.815,.123,.12),(-1.055,.785,.086,.082),(-1.14,.758,.069,.062),(-1.24,.752,.062,.054),(-1.30,.755,.045,.043)]],20)
# Continuous lower jaw: broad rear angle and low, tapered closed chin.
loft('lower-jaw',[( (0,y,z),rx,rz) for y,z,rx,rz in [(-.89,.724,.105,.063),(-1.00,.712,.087,.055),(-1.12,.704,.065,.037),(-1.235,.708,.055,.03),(-1.29,.717,.037,.022)]],16)
feet=[]
for side,fore_y,hind_y in [(1,-.47,.48),(-1,-.23,.72)]:
 x=side*.224
 # Asymmetrical bent profiles avoid straight toy cylinders; their tops lie inside the trunk.
 loft(('right' if side>0 else 'left')+'-forelimb',[( (xx,y,z),rx,ry) for xx,y,z,rx,ry in [(side*.075,fore_y+.035,.78,.125,.14),(side*.17,fore_y+.015,.65,.12,.13),(side*.215,fore_y,.51,.098,.11),(x,fore_y+.035,.38,.078,.084),(x,fore_y+.018,.20,.061,.07),(x,fore_y-.005,.075,.063,.075)]],16,'Z')
 loft(('right' if side>0 else 'left')+'-hindlimb',[( (xx,y,z),rx,ry) for xx,y,z,rx,ry in [(side*.065,hind_y-.015-(.14 if side<0 else 0),.76,.115,.14),(side*.17,hind_y-.04-(.08 if side<0 else 0),.64,.12,.145),(side*.225,hind_y-.08-(.04 if side<0 else 0),.51,.108,.125),(side*.235,hind_y-.13,.38,.08,.095),(side*.23,hind_y+.025,.21,.06,.075),(side*.23,hind_y+.005,.07,.062,.075)]],16,'Z')
 for kind,y,fx,length in [('fore',fore_y-.045,x,.205),('hind',hind_y-.045,side*.23,.25)]:
  # Wide low plantigrade sole; continuous paw, not a fan of separate capsules.
  loft(('right' if side>0 else 'left')+'-'+kind+'-plantigrade-paw',[( (fx,y+dy,z),rx,ry) for z,rx,ry,dy in [(-.015,.048,length*.30,0),(.015,.073,length*.46,0),(.052,.075,length*.50,-.005),(.095,.057,length*.37,.02),(.14,.043,length*.23,.04)]],16,'Z')
  feet.append({'side':side,'kind':kind,'x':fx,'y':y,'length':length})
# Tail follows a long descending curve with a slight lift, no tuft or ring.
tail=[((0,.63,.675),.105),((.015,.75,.63),.092),((.035,.90,.50),.077),((.065,1.05,.33),.058),((.095,1.19,.19),.042),((.13,1.31,.14),.028),((.16,1.42,.175),.017),((.175,1.48,.23),.012)]
def tube(name,points,radii,mat,n=12,body=False):
 vs=[];fs=[]
 for i,(p,r) in enumerate(zip(points,radii)):
  p=Vector(p);d=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]);d.normalize();u=d.cross(Vector((1,0,0)))
  if u.length<.1:u=d.cross(Vector((0,1,0)))
  u.normalize();v=d.cross(u).normalized()
  for j in range(n):vs.append(tuple(p+r*(math.cos(2*math.pi*j/n)*u+math.sin(2*math.pi*j/n)*v)))
 for i in range(len(points)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;fs.append((a,b,b+n,a+n))
 fs.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))])
 ob=mesh_object(name,vs,fs,mat,C)
 if body:parts.append(ob)
 return ob
tube('continuous-long-tail',[p for p,r in tail],[r for p,r in tail],M['coat'],16,True)
for s in [-1,1]:
 loft(('left' if s<0 else 'right')+'-small-ear',[( (s*x,y,z),rx,ry) for x,y,z,rx,ry in [(.09,-.875,.89,.065,.065),(.12,-.868,.945,.052,.043),(.132,-.863,.991,.032,.025),(.13,-.866,1.012,.009,.010)]],12,'Z')
# Preserve every designed profile before making the connected skin.
for ob in parts:
 cp=ob.copy();cp.data=ob.data.copy();cp.name='profile-'+ob.name;construct.objects.link(cp);cp.parent=None;cp.hide_render=True
construct.hide_render=True;construct.hide_viewport=True
bpy.ops.object.select_all(action='DESELECT')
for ob in parts:ob.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();skin=parts[0];skin.name='connected-anatomical-skin'
rem=skin.modifiers.new('Integrated loft union','REMESH');rem.mode='VOXEL';rem.voxel_size=.014;rem.use_smooth_shade=False
bpy.ops.object.modifier_apply(modifier=rem.name)
smo=skin.modifiers.new('Broad tissue transitions','SMOOTH');smo.factor=.62;smo.iterations=4;bpy.ops.object.modifier_apply(modifier=smo.name)
skin.data.calc_loop_triangles();before_tri=len(skin.data.loop_triangles)
dec=skin.modifiers.new('Faceted silhouette retention','DECIMATE');dec.ratio=min(1,6200/before_tri);dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name)
# Flatten the four broad soles, keeping the rest of the body intact.
for v in skin.data.vertices:
 if v.co.z<.018:v.co.z=0
bm=bmesh.new();bm.from_mesh(skin.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-6);
# Sole flattening can collapse coplanar triples; remove exact duplicates explicitly.
seen=set();duplicates=[]
for face in bm.faces:
 key=frozenset(face.verts)
 if key in seen:duplicates.append(face)
 else:seen.add(key)
if duplicates:bmesh.ops.delete(bm,geom=duplicates,context='FACES_ONLY')
boundary=[e for e in bm.edges if e.is_boundary]
if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=4)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(skin.data);bm.free();skin.data.update();skin.data.shade_flat()
if skin.data.validate(verbose=True):raise RuntimeError('Skin needs geometry repair')
skin.data.materials.clear()
for n in ['coat','coat_shadow','underside','muzzle']:skin.data.materials.append(M[n])
for f in skin.data.polygons:
 c=f.center;f.material_index=0
 if c.z<.43 and -.56<c.y<.43 and abs(c.x)<.16:f.material_index=2
 if c.y<-1.045:f.material_index=3
 if c.y<-.95 and c.z<.72:f.material_index=2
skin['construction']='Designed cross-section lofts, integrated via deterministic voxel union, smoothed and decimated; semantic input profiles retained.'
skin['scientific_scope']='Species-informed composite with interpreted soft tissue; not one measured specimen.'
# Surface-bound small facial details: eyes and mouth seam are embedded in the skin.
bpy.context.view_layer.update();tree=BVHTree.FromObject(skin,bpy.context.evaluated_depsgraph_get())
def lateral_surface(y,z,s):
 hit=tree.ray_cast(Vector((s*.6,y,z)),Vector((-s,0,0)),1.2)
 if hit[0] is None:raise RuntimeError('Facial anchor did not intersect skin')
 return hit[0]
def ellipsoid(name,center,scales,mat,n=12,rings=7):
 vs=[(center[0],center[1],center[2]-scales[2])];fs=[]
 for k in range(1,rings):
  ph=-math.pi/2+math.pi*k/rings
  for j in range(n):
   t=2*math.pi*j/n;vs.append((center[0]+scales[0]*math.cos(ph)*math.cos(t),center[1]+scales[1]*math.cos(ph)*math.sin(t),center[2]+scales[2]*math.sin(ph)))
 top=len(vs);vs.append((center[0],center[1],center[2]+scales[2]))
 for j in range(n):fs.append((0,1+(j+1)%n,1+j))
 for k in range(rings-2):
  for j in range(n):a=1+k*n+j;b=1+k*n+(j+1)%n;fs.append((a,b,b+n,a+n))
 for j in range(n):fs.append((top,1+(rings-2)*n+j,1+(rings-2)*n+(j+1)%n))
 return mesh_object(name,vs,fs,mat,C)
anchors=[]
for s in [-1,1]:
 p=lateral_surface(-1.035,.831,s);p.x-=s*.003
 eye=ellipsoid(('left' if s<0 else 'right')+'-embedded-eye',p,(.011,.017,.013),M['nose_eyes'],12,6)
 anchors.append({'feature':eye.name,'center':list(p),'surface_inset_m':.003,'normal_axis':'X','eye_half_thickness_m':.011})
 seam=[]
 for y,z in [(-1.265,.727),(-1.215,.718),(-1.15,.711),(-1.085,.714)]:
  p=lateral_surface(y,z,s);p.x-=s*.0005;seam.append(tuple(p))
 # The closed lower-jaw contour carries the lip break without raised black tubes.
ellipsoid('restrained-nose',(0,-1.296,.761),(.048,.024,.031),M['nose_eyes'],16,7)
claws=[]
for foot in feet:
 for j in range(4):
  x=foot['x']+(j-1.5)*.028;y=foot['y']-foot['length']*.43
  claws.append(tube('short-claw',[(x,y,.032),(x,y-.021,.024),(x,y-.029,.017)],[.010,.008,.0015],M['claws'],6))
bpy.ops.object.select_all(action='DESELECT')
for ob in claws:ob.select_set(True)
bpy.context.view_layer.objects.active=claws[0];bpy.ops.object.join();claws[0].name='short-integrated-claws'
# Translation is baked into all meshes while the asset root stays identity.
footprint_offset=.09125
for ob in list(C.all_objects)+list(construct.objects):
 if ob.type=='MESH':
  for v in ob.data.vertices:v.co.y-=footprint_offset
  ob.data.update()
root['reconstruction_note']='Original Amphicyon longiramus composite; coat, ears, tail outline and display pose are artistic.'
source=audit_source(C,max_triangles=P['geometry_policy']['max_triangles'])
if source['errors']:raise RuntimeError(str(source['errors']))
scene['asset_license']='CC-BY-4.0';scene['asset_author']='Leon Made This / s010s';scene['generator']='source/generate.py'
bpy.context.preferences.filepaths.save_version=0
# Reset inherited file-browser and render-output buffers before the first source save.
# Fill the full fixed-size buffer first so old startup directory bytes do not remain.
scene.render.filepath='//' + './'*500
scene.render.filepath='//renders/'
for screen in bpy.data.screens:
 for area in screen.areas:
  for space in area.spaces:
   if space.type=='FILE_BROWSER' and space.params:
    space.params.directory=b'//' + b'./'*500
    space.params.directory=b'//'
    space.params.filename=''
# Explicit resolved output prevents dependence on invocation working directory.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in C.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=root
options=dict(filepath=str(OUT/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties};missing=set(options)-available
if missing:raise RuntimeError('Exporter flags absent: '+str(missing))
bpy.ops.export_scene.gltf(**options)
g=audit_glb(OUT/'model.glb',P['geometry_policy']['max_triangles'],P['geometry_policy']['max_materials'],P['geometry_policy']['max_primitives'])
if g['errors']:raise RuntimeError(str(g['errors']))
if g['bytes']>P['geometry_policy']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(g['bounds_m'][side][i]-expected[i]) for side,expected in [('min',emin),('max',emax)] for i in range(3))
print('COUNTS',source['triangles'],g['scene_triangles'],'DELTA',delta,flush=True)
assert delta<.0001 and source['triangles']==g['scene_triangles']
import io_scene_gltf2
record={'asset_id':'amphicyon','revision':'r001','scope':'Static source/export checks only; not independent visual, GPU, populated-scene or publication acceptance.','glb_sha256':digest(OUT/'model.glb'),'blend_sha256':digest(OUT/'model.blend'),'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'blender_version':bpy.app.version_string,'exporter_version':list(io_scene_gltf2.bl_info['version']),'seed':P['seed'],'source':source,'glb':{**g,'file':'model.glb'},'source_to_glb_bounds_max_error_m':delta,'export_options':{k:v for k,v in options.items() if k!='filepath'},'facial_anchors':anchors,'contact_footprint_center_shift_y_m':footprint_offset,'canonical_helper_use':['setup_scene','make_material','mesh_object','audit_source','audit_glb','render_previews for private clay only'],'construction_note':'Connected loft-based body with retained editable semantic profile meshes. No unchanged sphere-and-cylinder assembly.','nominal_interpretive_dimensions':P['dimensions_m'],'warnings_review':[]}
write(OUT/'build-evidence.json',record)
if args.clay:
 clay=make_material('_temporary_clay','#929292',roughness=.9);original=[]
 for ob in C.all_objects:
  if ob.type=='MESH':
   original.append((ob,list(ob.data.materials)));ob.data.materials.clear();ob.data.materials.append(clay)
 render_previews(C,OUT/'clay',views=('front','side','top','hero'),resolution=400,samples=8,transparent=False)
print('CANDIDATE_BUILD_COMPLETE',g['scene_triangles'],g['bytes'],g['semantic_sha256'])
