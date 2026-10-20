# SPDX-License-Identifier: MIT
"""Original batch88 geometry, authored after every immutable premodel freeze."""
import bpy,bmesh,sys,json,math,argparse,pathlib,random,hashlib,datetime
from mathutils import Vector,Matrix
from mathutils.geometry import delaunay_2d_cdt
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed']);semantic={};repair=cfg.get('repair_parameters',{})

def tube(groups,pts,radii,mat,sides=8):
 vs,fs=groups[mat];off=len(vs);ps=[Vector(p) for p in pts]
 for j,p in enumerate(ps):
  t=(ps[min(j+1,len(ps)-1)]-ps[max(0,j-1)]).normalized();u=t.cross(Vector((0,1,0)))
  if u.length<.1:u=t.cross(Vector((1,0,0)))
  u.normalize();v=t.cross(u).normalized()
  for k in range(sides):vs.append(tuple(p+radii[j]*(math.cos(math.tau*k/sides)*u+math.sin(math.tau*k/sides)*v)))
 fs.append(tuple(off+k for k in reversed(range(sides))))
 for j in range(len(ps)-1):
  for k in range(sides):q=(k+1)%sides;x=off+j*sides+k;y=off+j*sides+q;fs.append((x,y,y+sides,x+sides))
 fs.append(tuple(off+(len(ps)-1)*sides+k for k in range(sides)))

def sample_curve(control,n):
 # Clamped Catmull-Rom interpolation of an original designed branch path.
 ps=[Vector(p) for p in control];out=[]
 for j in range(n):
  q=(len(ps)-1)*j/(n-1);i=min(int(q),len(ps)-2);t=q-i;p0=ps[max(0,i-1)];p1=ps[i];p2=ps[i+1];p3=ps[min(len(ps)-1,i+2)]
  out.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
 return out

def plant():
 groups={k:[[],[]] for k in m};leaf_count=0;axes=[]
 # One continuous low main axis, splitting into ascending and long sprawling branches.
 branches=[
 ([(0,0,.045),(.01,.01,.12),(-.025,.035,.26),(-.09,.055,.40),(-.13,.09,.59)],.025,.009,100),
 ([(0,0,.075),(-.12,-.04,.11),(-.28,-.08,.16),(-.45,-.08,.25),(-.59,-.05,.28)],.022,.008,112),
 ([(0,0,.075),(.13,.025,.11),(.29,.05,.16),(.43,.06,.28),(.56,.10,.40)],.022,.007,110),
 ([(-.25,-.075,.15),(-.28,-.01,.26),(-.32,.035,.39),(-.38,.09,.48)],.014,.006,65),
 ([(.28,.05,.155),(.30,.17,.25),(.32,.25,.37),(.39,.29,.44)],.014,.006,65),
 ([(-.035,.04,.28),(.04,-.07,.38),(.13,-.12,.48),(.22,-.15,.61)],.015,.007,80),
 ([(.015,.01,.12),(.03,-.12,.15),(.09,-.25,.18),(.18,-.32,.22)],.016,.006,72)]
 def leaf(base,tangent,radial,length,width,mat):
  nonlocal leaf_count
  vs,fs=groups[mat];off=len(vs);b=Vector(base);t=tangent.normalized();u=radial.normalized();side=t.cross(u).normalized();normal=side.cross((u*.82+t*.4).normalized()).normalized()
  vs.append(tuple(b))
  for frac,w,h in [(.15,width*.50,.0009),(.76,width*.50,.00055)]:
   center=b+u*(length*(frac-.18*frac*frac))+t*(length*(.22*frac+.3*frac*frac))
   vs.extend([tuple(center+side*w),tuple(center+normal*h),tuple(center-side*w),tuple(center-normal*h)])
  tip=b+u*length*.72+t*length*.60;vs.append(tuple(tip))
  for k in range(4):fs.append((off,off+1+k,off+1+(k+1)%4));fs.append((off+1+k,off+5+k,off+5+(k+1)%4,off+1+(k+1)%4));fs.append((off+9,off+5+(k+1)%4,off+5+k))
  leaf_count+=1
 for bi,(control,r0,r1,nleaf) in enumerate(branches):
  if repair:
   r0*=repair.get('stem_radius_multiplier',1);r1*=repair.get('stem_radius_multiplier',1);nleaf=repair.get('leaf_counts',[x[3] for x in branches])[bi]
  control=[tuple(Vector(p)*repair.get('axis_path_scale',1)) for p in control]
  pts=sample_curve(control,24);rads=[r0+(r1-r0)*(j/23)**.8 for j in range(24)];tube(groups,pts,rads,'axis');axes.append({'index':bi,'control_points':control,'leaves':nleaf})
  highres=sample_curve(control,nleaf+4)
  for j in range(nleaf):
   k=j+2;p=highres[k];t=(highres[k+1]-highres[k-1]).normalized();u=t.cross(Vector((0,1,0)))
   if u.length<.1:u=t.cross(Vector((1,0,0)))
   u.normalize();v=t.cross(u);theta=j*2.399963229728653+bi*.83;rad=u*math.cos(theta)+v*math.sin(theta);f=k/(nleaf+3);r=r0+(r1-r0)*f**.8
   length=(.044+.009*math.sin(j*.91+bi))*(.72+.28*math.sin(math.pi*f)**.5);width=.0038+.0006*math.cos(j*1.3)
   if repair:
    length=repair['leaf_length_min_m']+(repair['leaf_length_max_m']-repair['leaf_length_min_m'])*(.5+.5*math.sin(j*.91+bi));width=repair['leaf_width_m']
   leaf(p+rad*r*.85,t,rad,length,width,'leaf_light' if j%7==0 else 'leaf')
 # Small generic root connection, clearly artistic and subordinate, with no elaborate modern root architecture.
 for k in range(5):
  ang=k*math.tau/5+.2;v=Vector((math.cos(ang),math.sin(ang),0));tube(groups,[(0,0,.055),tuple(v*.018+Vector((0,0,.025))),tuple(v*.035+Vector((0,0,.005)))],[.007,.004,.0012],'root',6)
 for key,(vs,fs) in groups.items():mesh_object('baragwanathia_'+key+'_editable',vs,fs,m[key],col)
 semantic.update(axis_paths=axes,leaf_count=leaf_count,leaf_attachment='successive spiral, not whorled',source_scope='whole-plant concept; root/connectivity/pose artistic')

def inside(p,poly):
 return all((poly[(i+1)%len(poly)][0]-v[0])*(p[1]-v[1])-(poly[(i+1)%len(poly)][1]-v[1])*(p[0]-v[0])>=-1e-10 for i,v in enumerate(poly))

def trace_slab(paths,rc,rt,width,depth,base,kind):
 # Adaptive 2D triangulation samples actual trace cross profiles. One continuous closed
 # sediment/trace surface, not coincident tubes pasted onto a plane.
 poly=[(-.45*width,-.50*depth),(.32*width,-.50*depth),(.50*width,-.33*depth),(.50*width,.32*depth),(.38*width,.50*depth),(-.32*width,.50*depth),(-.50*width,.33*depth),(-.50*width,-.30*depth)]
 points=list(poly);segments=[]
 for path in paths:
  ps=[Vector(p) for p in path]
  for x,y in zip(ps,ps[1:]):segments.append((x,y))
  for j,p in enumerate(ps):
   t=(ps[min(j+1,len(ps)-1)]-ps[max(0,j-1)]).normalized();n=Vector((-t.y,t.x))
   offsets=[-rt*1.3,-rt,-rc,-rc*.52,0,rc*.52,rc,rt,rt*1.3] if kind=='phycosiphon' else [-rc*1.35,-rc,-rc*.65,0,rc*.65,rc,rc*1.35]
   for d in offsets:
    q=p+n*d
    if inside(q,poly):points.append(tuple(q))
  for p in [ps[0],ps[-1]]:
   for rr in [rc,rt*1.2]:
    for k in range(12):
     q=p+Vector((math.cos(math.tau*k/12),math.sin(math.tau*k/12)))*rr
     if inside(q,poly):points.append(tuple(q))
 # Quiet coarse host mesh; natural facets restrained and not random triangulation texture.
 for j in range(19):
  for i in range(25):
   q=((i/24-.5)*width,(j/18-.5)*depth)
   if inside(q,poly):points.append(q)
 vv,ee,ff,_,_,_=delaunay_2d_cdt([Vector(p) for p in points],[],[],0,0.000025)
 def nearest(p):
  d=1e6
  for a,b in segments:
   v=b-a;f=max(0,min(1,(p-a).dot(v)/v.length_squared));d=min(d,(p-(a+v*f)).length)
  return d
 def calc(p):
  d=nearest(p);host=base+.00012*math.sin(p.x/width*7)*math.sin(p.y/depth*5)
  if kind=='phycosiphon':
   mantel=repair.get('mantle_relief_height_m',.00032)*math.sqrt(max(0,1-(d/rt)**2));core=repair.get('core_relief_height_m',.00070)*math.sqrt(max(0,1-(d/rc)**2));return host+mantel+core,('core' if d<rc*.93 else 'mantle' if d<rt*.99 else 'host')
  return host+rc*repair.get('trace_relief_radius_multiplier',.82)*math.sqrt(max(0,1-(d/rc)**2)),('fill' if d<rc*.99 else 'host')
 vs=[(p.x,p.y,calc(p)[0]) for p in vv];fs=[tuple(f) for f in ff];ms=[]
 for f in ff:ms.append(calc(sum((vv[k] for k in f),Vector((0,0)))/len(f))[1])
 edges={}
 for f in ff:
  for a,b in zip(f,f[1:]+f[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
 bound=[es[0] for es in edges.values() if len(es)==1];baseidx={}
 for a,b in bound:
  for k in [a,b]:
   if k not in baseidx:baseidx[k]=len(vs);vs.append((vv[k].x,vv[k].y,0))
 center=len(vs);vs.append((0,0,0))
 for a,b in bound:
  fs.extend([(a,baseidx[a],baseidx[b],b),(center,baseidx[b],baseidx[a])]);ms.extend(['cut','cut'])
 keys=list(m);o=mesh_object(slug+'_continuous_sediment_and_trace_relief',vs,fs,[m[k] for k in keys],col)
 for face,key in zip(o.data.polygons,ms):face.material_index=keys.index(key)
 # Deterministic precision cleanup handles sub25-micron slivers from intersecting offset
 # samples. This is construction, before audits/save/export, not suppressed diagnostics.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.dissolve_degenerate(bm,dist=.000025,edges=list(bm.edges));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 o['trace_scope']='Illustrative relief; trace name is not producer. No physical wall lining.'
 semantic.update(centerline_paths=paths,core_radius_m=rc,mantle_radius_m=rt,mesh_construction='Single continuous closed heightfield with adaptive trace profile sampling; no overlapping visible surfaces',trace_kind=kind)

def chondrites():
 paths=[]
 def line(a,b,spacing=.0016):
  n=max(2,int((Vector(b)-Vector(a)).length/spacing)+1);return [tuple(Vector(a).lerp(Vector(b),i/(n-1))) for i in range(n)]
 # Unequal branches with repeated acute ramifications, open non-crossing twigs.
 main=[(0,-.067),(-.005,-.033),(-.009,.005),(-.018,.042),(-.025,.066)]
 for a,b in zip(main,main[1:]):paths.append(line(a,b))
 branches=[((-.003,-.041),(-.036,-.009),(-.069,.006)),((-.007,-.006),(.022,.025),(.049,.055)),((-.015,.028),(-.044,.051),(-.070,.061)),((-.001,-.055),(.031,-.038),(.064,-.013))]
 for k,(p0,p1,p2) in enumerate(branches):
  paths.extend([line(p0,p1),line(p1,p2)]);a=Vector(p0);b=Vector(p1);c=Vector(p2);side=1 if k%2 else -1
  # Secondary forks diverge consistently into their own unoccupied sector.
  q=a.lerp(b,.60);v=(b-a).normalized();n=Vector((-v.y,v.x))*side;tip=q+v*.022+n*.016;paths.append(line(q,tip))
  q2=q.lerp(tip,.61);tip2=q2+v*.012+n*.010;paths.append(line(q2,tip2))
  q3=b.lerp(c,.58);tip3=q3+(c-b).normalized()*.012+n*.013;paths.append(line(q3,tip3))
 # Independent small companion on the clear lower-left region.
 paths.extend([line((-.072,-.053),(-.055,-.033)),line((-.061,-.041),(-.078,-.029)),line((-.069,-.034),(-.076,-.020))])
 trace_slab(paths,.00105,.00105,.20,.16,.014,'chondrites');semantic['branch_orders']=3

def phycosiphon():
 paths=[]
 # Eight narrow recurved lobes in loose groups, never a continuous branch network.
 for cx,cy,ang,scale in [(-.024,-.016,-.25,1),(-.006,-.018,.12,.9),(.013,-.016,-.10,1.08),(.027,.004,.48,.88),(.009,.012,.22,1),(-.012,.009,-.18,1.02),(-.028,.014,-.45,.85),(-.003,.023,.55,.72)]:
  local=[];radius=.0036*scale;arm=.0085*scale
  for j in range(9):local.append((-radius,arm*(1-j/8)))
  for j in range(1,15):t=math.pi+math.pi*j/14;local.append((radius*math.cos(t),radius*math.sin(t)))
  for j in range(1,9):local.append((radius,arm*j/8))
  paths.append([(cx+x*math.cos(ang)-y*math.sin(ang),cy+x*math.sin(ang)+y*math.cos(ang)) for x,y in local])
 trace_slab(paths,.0006,.00145,.08,.065,.0063,'phycosiphon');semantic['recurved_lobes']=8

def planolites():
 pts=[]
 for j in range(81):x=-.079+.158*j/80;y=.017*math.sin(x/.079*math.pi);pts.append((x,y))
 trace_slab([pts],.006,.006,.16,.10,.015,'planolites');semantic['unbranched_paths']=1

{'baragwanathia':plant,'chondrites-branching-trace':chondrites,'phycosiphon-looping-trace':phycosiphon,'planolites-smooth-burrow':planolites}[slug]()
ground_asset(col,center_xy=True);root=bpy.data.objects[col['asset_root']]
for obj in col.all_objects:
 if obj.type=='MESH':
  world=obj.matrix_world.copy();obj.data.transform(world);obj.parent=None;obj.matrix_world.identity();obj.parent=root;obj.matrix_parent_inverse=Matrix.Identity(4)
root.location=(0,0,0);bpy.context.view_layer.update()
source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');(out/'geometry-semantics.json').write_text(json.dumps(semantic,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
