# SPDX-License-Identifier: MIT
"""Batch56 original concept-guided geometry. Blender 4.3.2; --config PATH --output DIR.
Shared helpers are pinned by dependency hashes. No third-party geometry or texture.
"""
import bpy,sys,json,math,argparse,pathlib,datetime,hashlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};groups={}
def part(name,vs,fs,mat):
 v,f=groups.setdefault((name,mat),([],[]));n=len(v);v.extend(vs);f.extend([tuple(n+i for i in face) for face in fs])
def loft(name,rings,mat):
 n=len(rings[0]);vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));part(name,vs,fs,mat)
def slab(sx,sy,h):
 outline=[(-.5,-.35),(-.36,-.5),(.26,-.48),(.5,-.32),(.48,.31),(.31,.48),(-.30,.5),(-.49,.26)]
 loft('illustrative_sediment_support',[[(x*sx*s,y*sy*s,z) for x,y in outline] for s,z in [(.96,0),(1,h*.45),(.95,h)]],'light')
def tube(name,points,radii,mat,n=10):
 rings=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);tangent.normalize();u=Vector((-tangent.y,tangent.x,0));u.normalize();w=tangent.cross(u).normalized()
  rings.append([tuple(Vector(p)+radii[i]*(u*math.cos(j*2*math.pi/n)+w*math.sin(j*2*math.pi/n))) for j in range(n)])
 loft(name,rings,mat)
def cycadeoidea():
 pockets=[(-1.85,.37),(-.85,.78),(-2.0,1.01),(.9,.59)]
 def radius(z):return .34+.035*math.sin(z/1.2*math.pi)-.04*(z/1.2)
 rings=[]
 for k in range(25):
  z=k*1.2/24;ring=[]
  for i in range(64):
   t=i*2*math.pi/64;d=min(((math.atan2(math.sin(t-th),math.cos(t-th))/.24)**2+((z-zh)/.115)**2) for th,zh in pockets);r=radius(z)-.08*max(0,1-d)**2
   ring.append((r*math.cos(t),r*math.sin(t),z))
  rings.append(ring)
 loft('trunk_core_recessed_sites',rings,'dark')
 for row in range(8):
  z=.085+row*.145
  for j in range(16):
   t=j*2*math.pi/16+(row%2)*math.pi/16;d=min((math.atan2(math.sin(t-th),math.cos(t-th))/.30)**2+((z-zh)/.14)**2 for th,zh in pockets)
   if d<1.1:continue
   # Leaf-base diamonds vary by growth row, with a broad central ridge.
   r=radius(z);u=Vector((-math.sin(t),math.cos(t),0));v=Vector((0,0,1));n=Vector((math.cos(t),math.sin(t),0));c=n*r+v*z
   ring=[c-u*.069,c-v*.083,c+u*.069,c+v*.083];vs=[tuple(p-n*.015) for p in ring]+[tuple(p+n*.039) for p in ring]+[tuple(c+n*.071+u*.008)]
   fs=[(3,2,1,0)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]+[(i+4,(i+1)%4+4,8) for i in range(4)]
   part('staggered_leaf_base_armor',vs,fs,'armor' if row%3 else 'stone')
 # Shallow inset cups lie inward of armor, visibly recessed with closed backs.
 for th,z in pockets:
  n=Vector((math.cos(th),math.sin(th),0));u=Vector((-math.sin(th),math.cos(th),0));v=Vector((0,0,1));c=n*(radius(z)-.045)+v*z
  rings=[[tuple(c+n*depth+(u*math.cos(i*math.tau/12)*.083+v*math.sin(i*math.tau/12)*.105)*s) for i in range(12)] for s,depth in [(.10,-.032),(.72,-.024),(1,.022),(1.12,.028)]]
  loft('embedded_reproductive_recesses',rings,'fossil')
def gondwanagaricites():
 slab(.026,.055,.002)
 # Flat mineralized side silhouette rests on a slab: Y follows stalk axis.
 tube('mineralized_stalk',[(.0004*math.sin(t*2),.017-.034*t,.0030) for t in [i/16 for i in range(17)]],[.0016+.00035*math.cos(i/16*math.pi) for i in range(17)],'fossil',10)
 # Cap side silhouette in XY; its illustrated hidden depth is only 2mm.
 outline=[(-.005,-.017),(-.0048,-.0195),(-.0031,-.0226),(-.001,-.0243),(.0014,-.0245),(.0035,-.0224),(.005,-.019),(.0047,-.017),(.0025,-.0176),(0,-.018),(-.0025,-.0176)]
 loft('compressed_convex_cap',[[(x*s,y,.003+z) for x,y in outline] for s,z in [(1,-.001),(1,0),(.93,.001)]],'fossil')
 # Gills shown as shallow converging ridges in side-relief lower cap strip.
 for i in range(9):
  x=-.0042+i*.00105
  tube('shallow_exposed_gill_relief',[(x,-.01735,.0031),(x*.62,-.0181,.0041),(x*.25,-.0188,.0042)],[.00012,.00015,.00009],'dark',4)
def deflation():
 n=48;nr=14;vs=[(0,-.18,.09)];fs=[]
 # Nested contours: broad floor, scooped walls, downwind rim, outer skirt.
 for k in range(1,nr+1):
  r=k/nr
  for j in range(n):
   t=j*math.tau/n;down=max(0,math.sin(t));x=2*r*math.cos(t)*(1+.025*math.sin(3*t));y=2.5*r*math.sin(t)
   z=.09+.36*(min(r/.78,1)**2.8)+.27*down**3*math.exp(-((r-.79)/.15)**2)
   z-=.22*max(0,(r-.82)/.18);z-=.22*max(0,-math.sin(t))**4*math.exp(-((r-.65)/.35)**2)
   z+=.012*math.sin(j*2.3+k*.7)*r*r
   vs.append((x,y,max(.035,z)))
 for j in range(n):fs.append((0,1+j,1+(j+1)%n))
 for k in range(nr-1):
  b=1+k*n;c=b+n
  for j in range(n):q=(j+1)%n;fs.extend([(b+j,c+j,c+q),(b+j,c+q,b+q)])
 start=len(vs)
 for j in range(n):x,y,z=vs[1+(nr-1)*n+j];vs.append((x,y,0))
 for j in range(n):q=(j+1)%n;fs.append((1+(nr-1)*n+j,start+j,start+q,1+(nr-1)*n+q))
 fs.append(tuple(start+j for j in range(n-1,-1,-1)));part('continuous_scooped_wind_basin',vs,fs,'stone')
def arthrophycus():
 slab(.24,.19,.012)
 # Three unequal curves, each one continuous closed cast with transverse ribs.
 for idx,(x0,y0,span,bend,count) in enumerate([(-.075,-.048,.134,.022,15),(-.079,.020,.150,-.010,18),(-.043,.065,.104,.010,12)]):
  pts=[];rs=[];steps=count*6
  for i in range(steps+1):
   t=i/steps;x=x0+span*t;y=y0+bend*math.sin(t*math.pi*1.3);z=.0165
   pts.append((x,y,z));r=.0081*(1+.17*math.cos(t*math.tau*count));r*=min(1,.38+min(t,1-t)*22);rs.append(r)
  tube('continuous_transversely_annulated_casts',pts,rs,'fossil',10)
{'cycadeoidea':cycadeoidea,'gondwanagaricites':gondwanagaricites,'deflation-hollow':deflation,'arthrophycus-annulated-burrow':arthrophycus}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000)
assert not source['errors'],source
# Metrics separate artistic nominal targets from actual authoring and glTF axes.
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts)
qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n')
print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
