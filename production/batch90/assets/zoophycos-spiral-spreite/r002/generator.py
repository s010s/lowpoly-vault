# SPDX-License-Identifier: MIT
"""Original batch90 geometry authored strictly after immutable original freeze."""
import bpy,bmesh,sys,json,math,argparse,pathlib,random,hashlib,datetime,os
from mathutils import Vector,Matrix
from mathutils.geometry import delaunay_2d_cdt
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(args.config).read_text());p=cfg['parameters'];out=pathlib.Path(args.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(slug,cfg['seed']);m=[make_material(k,v) for k,v in cfg['palette'].items()];semantic={}
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi):
  off=len(self.v);self.v+=v;self.f += [tuple(off+x for x in face) for face in f];self.mi += [mi]*len(f)
 def emit(self,name):
  o=mesh_object(name,self.v,self.f,m,col)
  for face,i in zip(o.data.polygons,self.mi):face.material_index=i
  return o

def tube(M,points,radii,sides=6,mi=0):
 vs=[];pts=[Vector(q) for q in points]
 for i,q in enumerate(pts):
  t=(pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)]).normalized();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();v=t.cross(u).normalized()
  for j in range(sides):vs.append(tuple(q+radii[i]*(u*math.cos(math.tau*j/sides)+v*math.sin(math.tau*j/sides))))
 fs=[tuple(reversed(range(sides)))]
 for i in range(len(pts)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;fs.append((a,b,b+sides,a+sides))
 fs.append(tuple(range((len(pts)-1)*sides,len(pts)*sides)));M.add(vs,fs,mi)

def curve(control,n):
 ps=[Vector(q) for q in control];result=[]
 for j in range(n):
  q=(len(ps)-1)*j/(n-1);i=min(int(q),len(ps)-2);t=q-i;a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(i+2,len(ps)-1)]
  result.append(tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)))
 return result

def plant():
 H=p['height_m'];N=p['tube_sides'];main=Mesh();path=[(.003*math.sin(i*.32),.0025*math.sin(i*.41),H*i/20) for i in range(21)];path[0]=(0,0,0);path[1]=(0,0,H/20);path[-1]=(path[-2][0],path[-2][1],H);tube(main,path,[p['main_axis_base_radius_m']*(1-.86*i/20) for i in range(21)],8,0);main.emit('dominant-upright-axis')
 base=Mesh()
 for k in range(4):
  a=k*math.pi/2+.3;r=p['base_anchorage_radius_m'];tube(base,[(0,0,.016),(r*.65*math.cos(a),r*.65*math.sin(a),.006),(r*math.cos(a),r*math.sin(a),.0015)],[.005,.0025,.0008],6,3)
 base.emit('minimal-conjectural-basal-anchorage')
 terminal=[];lateral_meshes=[]
 fertile_indices={1,2,4,5,7,8,10,11,13,14}
 for i in range(p['lateral_count']):
  fertile=i in fertile_indices;M=Mesh();z=.12+.75*i/15;a=.35-i*math.pi/2;q=Vector((.003*math.sin(z/H*20*.32),.0025*math.sin(z/H*20*.41),z));L=.115*(1-.48*i/15)
  def fork(q,ang,L,level,serial):
   end=q+Vector((math.cos(ang)*L,math.sin(ang)*L,L*.36));mid=q.lerp(end,.5)+Vector((0,0,L*.04));r=.0008+.00072*level
   tube(M,[q,end],[r,r*.68],N,0 if level>1 else 1)
   if level:
    for sg in [-1,1]:fork(end,ang+sg*((.23 if level>1 else .38) if fertile else (.42 if level>1 else .55)),L*(.48 if fertile else .60),level-1,serial*2+(sg+1)//2)
   elif fertile:
    tangent=Vector((math.cos(ang)*.45,math.sin(ang)*.45,.90)).normalized();side=Vector((-math.sin(ang),math.cos(ang),0));r=p['sporangium_diameter_m']/2;length=p['sporangium_length_m']
    for sg in [-1,1]:
     foot=end+side*sg*.0026;neck=foot+tangent*.004;tube(M,[end,neck],[.00075,.00062],5,1)
     tube(M,[neck,neck+tangent*(length*.45),neck+tangent*length],[r*.12,r,r*.1],6,2)
     terminal.append((i,tuple(neck),tuple(neck+tangent*length)))
  fork(q,a,L,p['lateral_fork_depth'],i)
  obj=M.emit('lateral-%02d-%s'%(i,'fertile' if fertile else 'sterile'));obj['insertion_height_m']=z;obj['artistic_rank']=i%4;lateral_meshes.append(obj)
  vg=obj.vertex_groups.new(name='lateral-%02d-%s'%(i,'fertile' if fertile else 'sterile'));vg.add(list(range(len(obj.data.vertices))),1,'REPLACE')
 bpy.ops.object.select_all(action='DESELECT')
 for obj in lateral_meshes:obj.select_set(True)
 bpy.context.view_layer.objects.active=lateral_meshes[0];bpy.ops.object.join();bpy.context.object.name='sixteen-four-rank-lateral-systems'
 semantic.update(laterals=16,fertile_laterals=10,terminal_sporangia=len(terminal),sporangia_paths=terminal,construction='Closed branch and fusiform modules with volumetric branch junctions, not flat foliage.',uncertainty='Basal anchorage, dimensions, exact counts, pose and coloration artistic.')

def poly_outline(W,D):return [(-.50*W,-.35*D),(-.39*W,-.50*D),(.30*W,-.50*D),(.50*W,-.32*D),(.48*W,.35*D),(.28*W,.50*D),(-.35*W,.48*D),(-.50*W,.20*D)]
def inside(q,poly):return all((poly[(i+1)%len(poly)][0]-a[0])*(q[1]-a[1])-(poly[(i+1)%len(poly)][1]-a[1])*(q[0]-a[0])>=-1e-11 for i,a in enumerate(poly))
def relief(paths,W,D,T,r,h,beads=None):
 poly=poly_outline(W,D);points=list(poly);segments=[]
 for path in paths:
  ps=[Vector(q) for q in path]
  for a,b in zip(ps,ps[1:]):segments.append((a,b))
  for j,q in enumerate(ps):
   tangent=(ps[min(j+1,len(ps)-1)]-ps[max(j-1,0)]).normalized();normal=Vector((-tangent.y,tangent.x))
   for off in [-1.45,-1,-.6,0,.6,1,1.45]:
    v=q+normal*r*off
    if inside(v,poly):points.append(tuple(v))
  for q in [ps[0],ps[-1]]:
   for j in range(12):points.append(tuple(q+Vector((math.cos(math.tau*j/12),math.sin(math.tau*j/12)))*r))
 if beads:
  for q,br,bh in beads:
   points.append(q)
   for frac in [.35,.70,1,1.25]:
    for j in range(16):points.append((q[0]+br*frac*math.cos(math.tau*j/16),q[1]+br*frac*math.sin(math.tau*j/16)))
 for j in range(15):
  for i in range(21):
   q=((i/20-.5)*W,(j/14-.5)*D)
   if inside(q,poly):points.append(q)
 # Delaunay heightfield is one watertight full-volume relief, so crossings cannot z-fight.
 vv,ee,ff,*_=delaunay_2d_cdt([Vector(q) for q in points],[],[],0,.000015)
 def height(q):
  best=1e9
  for a,b in segments:
   v=b-a;t=max(0,min(1,(q-a).dot(v)/v.length_squared));best=min(best,(q-a-v*t).length)
  bump=h*math.sqrt(max(0,1-(best/r)**2)) if best<r else 0
  if beads:
   for center,br,bh in beads:
    dist=(q-Vector(center)).length
    if dist<br:bump=max(bump,bh*math.sqrt(max(0,1-(dist/br)**2)))
  return T+bump,bump
 vs=[(q.x,q.y,height(q)[0]) for q in vv];fs=[];mi=[]
 for f in ff:
  centroid=sum((vv[k] for k in f),Vector((0,0)))/len(f)
  if inside(centroid,poly):fs.append(tuple(f));mi.append(2 if max(vs[k][2]-T for k in f)>h*.22 else 0)
 boundary={}
 for face in fs:
  for a,b in zip(face,face[1:]+face[:1]):
   key=tuple(sorted((a,b)));boundary[key]=boundary.get(key,0)+1
 indices=sorted(set(i for e,count in boundary.items() if count==1 for i in e));bot={i:len(vs)+j for j,i in enumerate(indices)};vs +=[(vv[i].x,vv[i].y,0) for i in indices]
 for (a,b),cnt in boundary.items():
  if cnt==1:fs.append((a,b,bot[b],bot[a]));mi.append(1)
 # Single bottom ngon oriented by angle; outer triangulation hull is convex clipped outline.
 ring=sorted(indices,key=lambda i:math.atan2(vv[i].y,vv[i].x));fs.append(tuple(bot[i] for i in ring));mi.append(1)
 M=Mesh();M.v=vs;M.f=fs;M.mi=mi;o=M.emit('integrated-full-volume-trace-relief')
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.dissolve_degenerate(bm,dist=.000012,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 semantic.update(paths=paths,bead_centers=beads,construction='Continuous closed triangulated raised relief, united compressed crossings; full solid slab underside. No surface overlays.')

def rosary():
 def xy(t):return (-.040+.080*t,.009*math.sin(math.tau*t-.4))
 pts=[xy(i/96) for i in range(97)];beads=[]
 for i in range(13):
  r=.0027+.0005*(.5+.5*math.sin(i*1.3+.2));beads.append((xy(i/12),r,.0033*(.90+.10*math.cos(i*.8))))
 relief([pts],*p['slab_dimensions_m'],p['neck_radius_m'],p['neck_relief_height_m'],beads);semantic['chamber_count']=13

def lumbricaria():
 controls=[
 [(-.058,-.028),(-.042,-.031),(-.028,-.012),(-.040,.003),(-.051,-.004),(-.043,-.019),(-.019,-.027),(.004,-.019),(.001,.003),(-.015,.015),(-.032,.029),(-.014,.038),(.004,.025),(.025,.019),(.039,.006),(.019,-.001),(-.001,.009),(.017,.027),(.043,.023),(.058,.036)],
 [(-.057,.026),(-.044,.035),(-.038,.019),(-.026,.008),(-.007,-.004),(-.016,-.026),(-.004,-.038),(.015,-.033),(.021,-.017),(.005,-.004),(.018,.011),(.037,-.005),(.044,-.026),(.025,-.035),(.011,-.022),(.034,-.018),(.058,-.031)],
 [(-.051,.001),(-.032,-.001),(-.019,.019),(-.034,.025),(-.047,.015),(-.035,-.011),(-.011,-.014),(.014,-.005),(.020,.013),(.006,.023),(.012,.034),(.034,.037)]]
 paths=[curve(c,110 if i<2 else 75) for i,c in enumerate(controls)];relief(paths,*p['slab_dimensions_m'],p['cord_radius_m'],p['cord_relief_height_m']);semantic['original_path_count']=3

def zoophycos():
 W,D,T=p['slab_dimensions_m'];poly=poly_outline(W,D);M=Mesh();n=len(poly);v=[(x,y,z) for z in [0,T] for x,y in poly];f=[tuple(range(n))[::-1],tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];M.add(v,f,0);M.emit('solid-quiet-sediment-slab')
 N=p['sheet_angular_segments'];Q=p['sheet_radial_segments'];turns=p['sheet_turns'];vs=[]
 for side in [0,1]:
  for i in range(N+1):
   t=i/N;theta=turns*math.tau*t-.5;outer=p['sheet_outer_radius_m']*(.9875+.0125*math.sin(theta*3+.3))
   for j in range(Q+1):
    u=j/Q;r=p['sheet_inner_radius_m']+(outer-p['sheet_inner_radius_m'])*u;a=theta+.43*(1-u);crest=(.5+.5*math.cos(math.tau*(p['primary_lamellae_count']*t+.5)))**2*p['lamella_relief_height_m']*u**.35;rim=.0012*max(0,(u-.80)/.20)**2
    z=.018+p['sheet_rise_m']*t-.003*u+side*p['sheet_thickness_m']
    if side:z+=crest+rim
    vs.append((r*math.cos(a),r*math.sin(a),z))
 row=Q+1;plane=(N+1)*row;fs=[];mi=[]
 for i in range(N):
  for j in range(Q):
   a=i*row+j;fs.extend([(a,a+1,a+row+1,a+row),(a+plane,a+plane+row,a+plane+row+1,a+plane+1)]);mi.extend([2,3 if i%4==0 else 2])
 for i in range(N):
  a=i*row;fs.extend([(a,a+row,a+row+plane,a+plane),(a+Q,a+Q+plane,a+row+Q+plane,a+row+Q)]);mi.extend([2,2])
 for j in range(Q):fs.extend([(j,j+plane,j+plane+1,j+1),(N*row+j,N*row+j+1,N*row+j+plane+1,N*row+j+plane)]);mi.extend([2,2])
 M=Mesh();M.v=vs;M.f=fs;M.mi=mi;M.emit('broad-spiral-spreite-sheet-with-integrated-lamellae-and-margin')
 shaft=Mesh();tube(shaft,[(0,0,T*.95),(0,0,p['shaft_height_m'])],[p['shaft_radius_m']]*2,10,4);shaft.emit('narrow-cylindrical-central-shaft');semantic.update(sheet_turns=turns,lamellae=40,construction='One solid helicoidal sheet with real curved relief lamellae, integrated margin, closed underside and narrow supporting shaft. Display exposure illustrative.')

{'pertica':plant,'rosary-shaped-chambered-burrow-hormosiroidea-type':rosary,'zoophycos-spiral-spreite':zoophycos,'lumbricaria-thread-like-coprolite':lumbricaria}[slug]()
ground_asset(col,center_xy=True);root=bpy.data.objects[col['asset_root']]
for o in col.all_objects:
 if o.type=='MESH':
  world=o.matrix_world.copy();o.data.transform(world);o.parent=None;o.matrix_world.identity();o.parent=root;o.matrix_parent_inverse=Matrix.Identity(4)
root.location=(0,0,0);bpy.context.view_layer.update();source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');(out/'geometry-semantics.json').write_text(json.dumps(semantic,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'));bpy.ops.object.select_all(action='DESELECT')
for o in col.all_objects:o.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n')
(out/'execution.json').write_text(json.dumps(dict(pid=os.getpid(),parent_pid=os.getppid(),started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),generator_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),config_sha256=hashlib.sha256(pathlib.Path(args.config).read_bytes()).hexdigest(),blender=bpy.app.version_string,argv=sys.argv),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
