# SPDX-License-Identifier: MIT
"""Original batch66 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
import bpy,sys,json,math,argparse,pathlib,datetime,hashlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
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
def tube(name,points,radii,mat,n=6):
 rings=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.95 else Vector((1,0,0));u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
  rings.append([tuple(Vector(p)+radii[i]*(u*math.cos(j*math.tau/n)+w*math.sin(j*math.tau/n))) for j in range(n)])
 loft(name,rings,mat)
def ellipsoid(name,c,r,mat,n=12,k=6):
 rings=[]
 for j in range(k+1):
  t=-math.pi/2+.15+(math.pi-.30)*j/k
  rings.append([(c[0]+r[0]*math.cos(t)*math.cos(i*math.tau/n),c[1]+r[1]*math.cos(t)*math.sin(i*math.tau/n),c[2]+r[2]*math.sin(t)) for i in range(n)])
 loft(name,rings,mat)


# Isolatedr002 geometry authored AFTER frozen derived repair plan. Originalr001 untouched.
import random
rng=random.Random(cfg['seed'])
def louisella():
 n=20
 def center(t):return Vector((.014*math.sin(t*math.tau),-.15+.30*t,.018+.003*math.sin(t*math.tau)))
 def radius(t):
  if t>=.97:return .0075*math.sqrt(max(.004,1-((t-.97)/.03)**2))
  levels=[(0,.0015),(.08,.0024),(.16,.0045),(.24,.0048),(.28,.011),(.38,.013),(.43,.015),(.60,.0145),(.64,.012),(.85,.011),(.88,.0078),(.97,.0075)]
  for (a,r),(b,s) in zip(levels,levels[1:]):
   if a<=t<=b:return r+(s-r)*(t-a)/(b-a)
  return .0075
 def frame(t):
  tangent=(center(min(1,t+.001))-center(max(0,t-.001))).normalized();u=Vector((tangent.y,-tangent.x,0)).normalized();v=u.cross(tangent).normalized();return u,v
 rings=[]
 samples=[(.009,.00035),(0,.0008),(0,.0015)]
 for i in range(1,121):
  t=.97*i/120
  # Four distinct structural textures; smooth posterior is not a pointed annulated cone.
  amplitude=.105 if .41<t<.63 else .022 if t<.87 else 0
  rr=radius(t)*(1+amplitude*math.cos((t-.41)*math.tau/.0162));samples.append((t,rr))
 for j in range(1,13):
  t=.97+.03*j/12;samples.append((t,radius(t)))
 for t,r in samples:
  c=center(t);u,v=frame(t);rings.append([tuple(c+r*(u*math.cos(k*math.tau/n)+v*math.sin(k*math.tau/n))) for k in range(n)])
 loft('whole_body_spiny_anterior_coarse_annular_middle_papillate_zone_smooth_blunt_rear',rings,'body')
 # Dense short scalids on anterior trunk, sparse fine trunk rings toward papillate zone.
 for j in range(15):
  t=.29+j*.038;c=center(t);u,v=frame(t);r=radius(t)
  for k in range(10):
   a=k*math.tau/10+(j%2)*.2;d=u*math.cos(a)+v*math.sin(a);length=.0018 if t<.41 else .0009
   tube('short_trunk_spine_rings_rear_excluded',[tuple(c+d*(r-.0002)),tuple(c+d*(r+length))],[.00048,.00009],'spines',5)
 for j in range(7):
  t=.025+j*.028;c=center(t);u,v=frame(t)
  for k in range(8):
   a=k*math.tau/8+j*.3;d=u*math.cos(a)+v*math.sin(a);r=radius(t);tube('fine_proboscis_scalids',[tuple(c+d*(r-.0001)),tuple(c+d*(r+.00065))],[.00024,.00006],'spines',5)
 t=.125;c=center(t);u,v=frame(t)
 for k in range(25):
  a=k*math.tau/25;d=u*math.cos(a)+v*math.sin(a);tube('proboscis_exactly_25_long_midlength_scalids',[tuple(c+d*(radius(t)-.0001)),tuple(c+d*(radius(t)+.0042)+Vector((0,-.001,0)))],[.00045,.00008],'spines',5)
 # Widely separated genuinely cylindrical blunt papillae, NOT tiny pointed surface dots/legs.
 for j in range(22):
  t=.46+j*.0185;c=center(t);u,v=frame(t);r=radius(t)
  for side in [-1,1]:
   d=(v*.70+u*side*.714).normalized();start=c+d*(r-.0003);end=c+d*(r+.0048)
   tube('two_widely_separated_dorsal_longitudinal_blunt_papilla_rows',[tuple(start),tuple(start.lerp(end,.82)),tuple(end)],[.00145,.0014,.00115],'papilla',7)
 # Tiny posterior aperture at the center of a hemispherical rear, no projecting tail appendage.
 c=center(1);ellipsoid('small_posterior_aperture',tuple(c+Vector((0,.00004,0))),(.0005,.00010,.0005),'mouth',10,4)
def hoodoo():
 n=28;rings=[]
 # Continuous shaft taper, no periodic radius expansions at4global tier levels.
 # Local asymmetric shoulders occupy limited azimuth spans and unequal elevations.
 ledges=[(1.20,.42,.35,.80,.38),(3.72,.36,.31,3.25,.62),(6.18,.26,.23,5.20,.43)]
 def adiff(a,b):return (a-b+math.pi)%math.tau-math.pi
 for j in range(42):
  z=7.35*j/41;cx=.22*math.sin(z*.66)+.12*math.sin(z*1.5);cy=.16*math.sin(z*.8)
  # Broad eroded foot, unequal broad shoulders; neither encircles full shaft.
  base=.46+1.0*math.exp(-z/1.32)+.09*math.exp(-((z-4.6)/.8)**2)
  ring=[]
  for i in range(n):
   a=i*math.tau/n
   r=base*(1+.10*math.sin(a*3+z*.6)+.055*math.sin(a*7-z*.8))
   r+=.22*math.exp(-((z-2.25)/.63)**2)*math.exp(-(adiff(a,1.8)/1.0)**4)
   r+=.16*math.exp(-((z-5.1)/.92)**2)*math.exp(-(adiff(a,4.4)/.8)**4)
   for h,amp,width,az,span in ledges:
    local=math.exp(-(adiff(a,az)/span)**4)
    # Narrow projection plus soft undercut below, spatially local not a full rim.
    r+=local*(amp*math.exp(-((z-h)/width)**4)-amp*.32*math.exp(-((z-(h-.38))/(width*.8))**2))
   zz=z if j==0 else z+.065*math.sin(3*a+z*.4)
   ring.append((cx+r*math.cos(a),cy+r*.90*math.sin(a),zz))
  rings.append(ring)
 # Real coherent modest cap joined to shaft, not a detached broad boulder.
 for z,r in [(7.38,.65),(7.67,.67),(8.0,.55)]:
  cx=.22*math.sin(z*.66)+.12*math.sin(z*1.5);cy=.16*math.sin(z*.8)
  rings.append([(cx+r*(1+.10*math.sin(i*1.7))*math.cos(i*math.tau/n),cy+r*.90*(1+.1*math.sin(i*2.1))*math.sin(i*math.tau/n),z+.06*math.sin(i*1.3)) for i in range(n)])
 loft('irregular_tapered_erosional_pillar_with_three_interrupted_unequal_local_ledges',rings,'rock')
{'louisella':louisella,'hoodoo':hoodoo}[slug]()
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if mat=='body':
  for k in ['pale','neck','mouth']:obj.data.materials.append(m[k])
  obj.data.update()
  for p in obj.data.polygons:
   t=(p.center.y+.15)/.30;p.material_index=3 if t<.01 and p.center.y>-.1498 else 2 if .26<t<.41 else 1 if t>.87 or .41<t<.64 else 0
 elif slug=='hoodoo':
  for k in ['pale','rust','cap']:obj.data.materials.append(m[k])
  obj.data.update()
  for p in obj.data.polygons:
   x,y,z=p.center;a=math.atan2(y,x)
   # Broken mineral bands follow limited asymmetrical eroded patches, no4horizontal rings.
   pale=(abs(z-(1.25+.20*math.sin(a*2)))<.24 and math.cos(a-.35)>.35) or (abs(z-(3.8+.24*math.sin(a)))<.28 and math.cos(a-3.25)>.65) or (abs(z-(6.2+.13*math.sin(a*3)))<.18 and math.cos(a-5.2)>.72)
   p.material_index=3 if z>7.35 else 1 if pale else 2 if (2.7<z<3.35 and x>-.1) or (4.65<z<5.75 and y<.15) else 0
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
