"""Original, continuous closed Y. greenlandica internal-mould art study.
Inputs are explicit shape parameters, not extracted reference geometry. No remesh,
boolean, random topology or cached mesh. Projection replaces a cap surface patch.
"""
import bpy, bmesh, json, math, hashlib, sys
from pathlib import Path
from mathutils import Vector
SOURCE_ROOT=Path(__file__).resolve().parents[1]
C=json.loads((SOURCE_ROOT/'generator-config.json').read_text())
if bpy.app.version_string != C['blender_version']: raise RuntimeError('Blender version mismatch')
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
STAGE=args[0] if args else 'graybox';ROOT=Path(args[1]).resolve() if len(args)>1 else SOURCE_ROOT
for d in ['evidence','logs','graybox','final']: (ROOT/d).mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(SOURCE_ROOT/'scripts/deps'))
from asset_common import setup_scene, make_material, export_asset, audit_source
export_collection=setup_scene('yochelcionella',seed=C['seed']);scene=bpy.context.scene
root=bpy.data.objects[export_collection['asset_root']]
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
scene.render.threads_mode='FIXED';scene.render.threads=C['blender_threads']

M=[make_material(name,h,roughness=C['roughness'],double_sided=False) for name,h in C['palette_srgb']]
vs=[];fs=[];mi=[];n=C['angular_segments'];profile=C['profile'];nr=len(profile)
def face(v,m=0):fs.append(v);mi.append(m)
for i,(u,cy,rx,ry) in enumerate(profile):
 for j in range(n):
  th=math.tau*j/n;front=math.cos(th)
  bulge=0
  for r in C['rugae']:
   mask=1-math.exp(-((1-front)/.22)**2) if r['exclude_subapical'] else 1
   bulge+=r['amplitude']*math.exp(-((u-r['height'])/r['width'])**2)*mask
  x=(rx+bulge)*math.sin(th); y=cy-(ry+bulge)*front
  # Broad ruga rows inclined toward subapical projection, no high frequency noise.
  z=u+.035*math.sin(math.pi*u)*front
  if i==0:z+=.003*(1-math.cos(th*4))
  vs.append((x,y,z))
p=C['port'];low=p['lower_ring'];high=p['upper_ring'];half=p['half_angular_span']
def ix(i,j):return i*n+(j%n)
for i in range(nr-1):
 for j in range(n):
  js=j if j<n//2 else j-n
  if low<=i<high and -half<=js<half:continue
  mid=(profile[i][0]+profile[i+1][0])/2
  matidx=1 if i>=21 else 0
  face((ix(i,j),ix(i,j+1),ix(i+1,j+1),ix(i+1,j)),matidx)
# Top closed rounded boss and basal closed mould surface, not original shell cavity.
top=len(vs);vs.append((0,-.262,1.0))
for j in range(n):face((ix(nr-1,j),ix(nr-1,j+1),top))
basal=[]
for j in range(n):
 th=math.tau*j/n;basal.append(len(vs));vs.append((.24*math.sin(th),.075-.39*math.cos(th),.006*(1-math.cos(th*2))))
for j in range(n):face((ix(0,j+1),ix(0,j),basal[j],basal[(j+1)%n]),2)
center=len(vs);vs.append((0,.075,.005))
for j in range(n):face((basal[(j+1)%n],basal[j],center),2)
# Boundary of removed surface patch, in continuous order. Its lower/top corners
# map to corresponding sectors of the rounded snorkel-fill cross section.
boundary=[ix(low,j) for j in range(-half,half+1)]
boundary += [ix(i,half) for i in range(low+1,high+1)]
boundary += [ix(high,j) for j in range(half-1,-half-1,-1)]
boundary += [ix(i,-half) for i in range(high-1,low,-1)]
k=len(boundary);prev=boundary
for s in p['stages']:
 ring=[]
 for j in range(k):
  # 16 perimeter steps: lower-left is -135deg, bottom midpoint -90deg.
  a=-math.pi*.75+math.tau*j/k
  ring.append(len(vs));vs.append((s['rx']*math.cos(a),s['y'],s['z']+s['rz']*math.sin(a)))
 for j in range(k):face((prev[j],prev[(j+1)%k],ring[(j+1)%k],ring[j]))
 prev=ring
end=len(vs);s=p['stages'][-1];vs.append((0,s['y']-.003,s['z']))
for j in range(k):face((prev[j],prev[(j+1)%k],end))
# Remove unused vertices from excised patch; canonically order generated mesh.
used=sorted({v for f in fs for v in f});index={v:i for i,v in enumerate(used)}
verts=[(vs[i][0]*C['meters_per_design_unit'],(vs[i][1]-C['origin_shift_y_design_units'])*C['meters_per_design_unit'],vs[i][2]*C['meters_per_design_unit']) for i in used]
faces=[tuple(index[v] for v in f) for f in fs]
me=bpy.data.meshes.new('Continuous cap and solid snorkel fill');me.from_pydata(verts,[],faces);me.update()
ob=bpy.data.objects.new('Yochelcionella greenlandica internal mould',me);export_collection.objects.link(ob);ob.parent=root;root['representation']='fossil-specimen';root.select_set(True)
for m in M:me.materials.append(m)
for f,m in zip(me.polygons,mi):f.material_index=m
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
# Canonical ordered explicit triangles keep whole-generator fresh processes equal.
me.calc_loop_triangles();coords=[tuple(float(x) for x in v.co) for v in me.vertices];ordered=sorted(set(coords));lookup={c:i for i,c in enumerate(ordered)};ixs=[lookup[c] for c in coords]
tri=[]
for t in me.loop_triangles:
 f=tuple(ixs[i] for i in t.vertices);f=min(f[j:]+f[:j] for j in range(3));tri.append((me.polygons[t.polygon_index].material_index,f))
tri.sort();new=bpy.data.meshes.new('Canonical continuous internal mould');new.from_pydata(ordered,[],[f for m,f in tri]);new.update()
for m in M:new.materials.append(m)
for f,(m,_) in zip(new.polygons,tri):f.material_index=m;f.use_smooth=False
ob.data=new;bpy.data.meshes.remove(me);me=new
ob['asset_id']=C['asset_id'];ob['revision']=C['revision'];ob['representation']='fossil-specimen';ob['scope']='Original nominal 1mm internal-mould study, not shell or living organism';ob['source_specimen']='MGUH27016';ob['meters_per_design_unit']=C['meters_per_design_unit']
bpy.context.view_layer.objects.active=ob;ob.select_set(True)
lo=[min(v.co[i] for v in me.vertices) for i in range(3)];hi=[max(v.co[i] for v in me.vertices) for i in range(3)]
metadata={'asset_id':C['asset_id'],'revision':C['revision'],'stage':STAGE,'blender':bpy.app.version_string,'generator_config_sha256':hashlib.sha256((SOURCE_ROOT/'generator-config.json').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'triangles':len(tri),'vertices':len(me.vertices),'bounds_min':lo,'bounds_max':hi,'dimensions_m':[hi[i]-lo[i] for i in range(3)],'scale':'Uniform 0.001m per design unit, nominal art only','topology':'One explicit continuous closed boundary surface including solid projection and basal closure; no boolean/remesh/overlap components','shading':'Purposeful flat exported normals','material_palette_srgb':C['palette_srgb'],'stage_helpers_exported':False}
(ROOT/'evidence'/f'{STAGE}-build-metadata.json').write_text(json.dumps(metadata,indent=2))
if STAGE=='graybox':
 clay=make_material('Graybox neutral clay','#898C8D',roughness=C['roughness'],double_sided=False);me.materials.clear();me.materials.append(clay)
 for f in me.polygons:f.material_index=0
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'graybox/yochelcionella-graybox.blend'))
else:
 record=export_asset('yochelcionella-r001',{'en':'Yochelcionella greenlandica — internal mould','zh':'Yochelcionella greenlandica 内模化石'},'animals',export_collection,metadata={'description':{'en':'Original nominal 1mm fossil internal-mould study of MGUH27016; not living animal or hollow shell.','zh':'名义1毫米内模化石形态研究，不是活体或空壳。'},'representation':'fossil-specimen','generator':'scripts/build_yochelcionella.py','sources':[{'id':'ATKINS-PEEL2004','specimen':'MGUH27016','figure':'2 A-D'}],'scope':'Isolated local candidate; no publication or runtime acceptance'},output_dir_override=str(ROOT),render=False,max_triangles=6000,max_materials=4,max_primitives=16)
 (ROOT/'evidence/source-helper-checks.json').write_text(json.dumps(json.loads((ROOT/'qa.json').read_text())['source'],indent=2))

def render_views(assets,folder,samples):
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=samples;scene.cycles.use_denoising=False
 scene.render.threads_mode='FIXED';scene.render.threads=C['blender_threads'];scene.render.image_settings.file_format='PNG';scene.render.resolution_x=C['render']['resolution'];scene.render.resolution_y=C['render']['resolution'];scene.render.resolution_percentage=100
 scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 scene.world=bpy.data.worlds.new('QA neutral world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(*C['render']['background'],1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.7
 # Millimeter lighting uses squared distance power scaling, no mesh scaling.
 scale=.001
 for name,pos,power,size in [('Key',(3,-4,5),210,3),('Fill',(-4,-2,2),100,3),('Rim',(1,4,4),180,2.5)]:
  ld=bpy.data.lights.new('QA '+name,'AREA');light=bpy.data.objects.new('QA '+name,ld);scene.collection.objects.link(light);light.location=Vector(pos)*scale;ld.energy=power*scale*scale;ld.shape='DISK';ld.size=size*scale;light.rotation_euler=(Vector((0,0,.0005))-light.location).to_track_quat('-Z','Y').to_euler()
 camd=bpy.data.cameras.new('QA canonical camera');cam=bpy.data.objects.new('QA canonical camera',camd);scene.collection.objects.link(cam);scene.camera=cam;camd.type='ORTHO';camd.ortho_scale=C['render']['orthographic_m'];camd.clip_start=.000001;camd.clip_end=.05
 center=Vector((0,0,.0005));views={'front':(0,-.006,.0005),'side':(.006,0,.0005),'top':(0,0,.006),'perspective':(.004,-.004,.0045)};manifest=[]
 for name,pos in views.items():
  target=Vector((0,0,0)) if name=='top' else center
  cam.location=pos;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
  if name=='top':cam.rotation_euler=(0,0,0)
  scene.render.filepath=str(folder/(name+'.png'));bpy.ops.render.render(write_still=True);p=folder/(name+'.png')
  manifest.append({'view':name,'path':str(p.relative_to(ROOT)),'camera_m':list(pos),'target_m':list(target),'orthographic_m':camd.ortho_scale,'source_geometry_scale_modified':False,'render_engine':'Blender Cycles CPU','samples':samples,'color_management':'Standard / None; exposure0 gamma1','resolution':[C['render']['resolution']]*2,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
 return manifest
if STAGE=='graybox':
 manifest=render_views([ob],ROOT/'graybox',C['render']['samples_graybox']);(ROOT/'evidence/graybox-view-manifest.json').write_text(json.dumps(manifest,indent=2))
print('BUILD_COMPLETE',json.dumps(metadata),flush=True)
