# SPDX-License-Identifier: MIT
"""Deterministic Scutellosaurus lawleri reconstruction. Blender 4.3.2.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output /absolute/output [--gray|--final]
Only params.json and relative deps are read. No photographs are required at runtime.
"""
import argparse, hashlib, json, math, random, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
args=argparse.ArgumentParser();args.add_argument('--output',type=Path,required=True);args.add_argument('--gray',action='store_true');args.add_argument('--final',action='store_true')
a=args.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
p=json.loads((HERE/'params.json').read_text());random.seed(p['seed'])
col=ac.setup_scene('scutellosaurus',p['seed']);scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
m={k:ac.make_material(k,v,roughness=.86) for k,v in p['palette'].items()}
class Group:
 def __init__(self): self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  off=len(self.v);self.v.extend(v);self.f.extend([tuple(off+i for i in face) for face in f]);self.mi.extend([mi]*len(f))
 def finish(self,name,mats):
  obj=ac.mesh_object(name,self.v,self.f,mats,col)
  for poly,mi in zip(obj.data.polygons,self.mi):poly.material_index=mi
  return obj

def tube(group,points,radii,sides=8,mi=0):
 vs=[]
 for i,(center,r) in enumerate(zip(points,radii)):
  c=Vector(center);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize()
  ref=Vector((1,0,0)) if abs(t.x)<.85 else Vector((0,0,1));u=t.cross(ref).normalized();v=t.cross(u).normalized()
  r1,r2=r if isinstance(r,(tuple,list)) else (r,r)
  for j in range(sides):
   ang=2*math.pi*j/sides;vs.append(tuple(c+u*(math.cos(ang)*r1)+v*(math.sin(ang)*r2)))
 fs=[tuple(reversed(range(sides)))]
 for i in range(len(points)-1):
  for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
 fs.append(tuple((len(points)-1)*sides+j for j in range(sides)));group.add(vs,fs,mi)

# Profile loft integrates muzzle, skull, lowered neck, light ribcage and long tapering tail.
# Stations: y, center-z, x-radius, z-radius. Total length is exactly 1.2 m.
stations=[(-.450,.337,.007,.010),(-.430,.346,.016,.018),(-.405,.351,.023,.025),(-.379,.352,.027,.030),(-.354,.344,.024,.029),(-.337,.325,.022,.027),(-.306,.303,.024,.030),(-.270,.289,.029,.037),(-.232,.281,.041,.052),(-.190,.275,.052,.065),(-.132,.274,.058,.072),(-.068,.276,.059,.073),(-.010,.280,.054,.065),(.045,.282,.048,.056),(.095,.281,.039,.043),(.160,.278,.031,.034),(.235,.272,.025,.027),(.315,.263,.020,.022),(.400,.252,.015,.017),(.490,.241,.0105,.0125),(.580,.232,.0068,.0085),(.660,.225,.0038,.0048),(.720,.219,.002,.0026),(.750,.216,.001,.0013)]
body=Group();n=16;v=[]
for y,z,rx,rz in stations:
 for j in range(n):
  t=2*math.pi*j/n;v.append((rx*math.sin(t),y,z+rz*math.cos(t)))
f=[tuple(reversed(range(n)))];mis=[0]
for i in range(len(stations)-1):
 for j in range(n):
  f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j));mis.append(1 if 5<=j<=10 and i<17 else 0)
f.append(tuple((len(stations)-1)*n+j for j in range(n)));mis.append(0)
body.add(v,f);body.mi=mis;body.finish('Integrated head neck torso and tapering tail',[m['body'],m['belly']])
claws=Group()
# Long hindlimbs, forward knee and backward hock. Both feet rest on ground.
for sign,label,dy in [(1,'right',-.013),(-1,'left',.018)]:
 g=Group();x=sign*.062
 tube(g,[(sign*.042,.014+dy,.282),(sign*.059,-.022+dy,.235),(x,-.053+dy,.190),(x,-.039+dy,.169),(x,.016+dy,.084),(x,.009+dy,.038),(x,-.005+dy,.018)],[(.029,.033),(.032,.034),(.023,.024),(.018,.018),(.012,.013),(.010,.011),(.013,.011)],10)
 # Three major forward toes and a small raised medial hallux.
 for k in (-1,0,1):
  end=(x+k*.019,-.077+dy-(.012 if k==0 else 0),.009)
  tube(g,[(x+k*.006,-.006+dy,.018),(x+k*.014,-.039+dy,.011),end],[.008,.007,.0045],6)
  tube(claws,[end,(end[0]+k*.002,end[1]-.013,end[2]-.001)],[.0046,.0014],6)
 tube(g,[(x-sign*.007,.002+dy,.027),(x-sign*.019,.025+dy,.016),(x-sign*.020,.031+dy,.012)],[.0055,.004,.0025],6)
 g.finish('Hind limb and articulated foot '+label,m['body'])
# Short suspended arms and medially-facing hands, no quadrupedal support.
for sign,label in [(1,'right'),(-1,'left')]:
 g=Group();sx=sign*.040
 tube(g,[(sx,-.231,.285),(sign*.047,-.210,.239),(sign*.048,-.190,.210),(sign*.048,-.211,.171),(sign*.047,-.216,.153)],[(.015,.016),.013,.010,.008,(.008,.010)],8)
 # Fingers splay mainly in the sagittal plane, palms face inward, not down.
 for k in range(5):
  y=-.218+(k-2)*.004;length=[.012,.020,.022,.018,.012][k]
  tip=(sign*(.047-.003*abs(k-2)),y-.008,.153-length)
  tube(g,[(sign*.047,y,.155),(sign*.047,y-.004,.146),tip],[.0035,.0028,.0018],5)
 g.finish('Suspended forelimb and five-digit hand '+label,m['body'])
claws.finish('Small hind toe claws',m['claws'])

# Small low keeled osteoderms: individual convex closed solids, arranged artistically.
def section(y):
 for i in range(len(stations)-1):
  if stations[i][0]<=y<=stations[i+1][0]:
   a,b=stations[i],stations[i+1];t=(y-a[0])/(b[0]-a[0]);return [a[j]*(1-t)+b[j]*t for j in (1,2,3)]
 raise ValueError(y)
scutes=Group();scute_count=0

def scute(y,theta,width,length,height,mi):
 global scute_count
 z,rx,rz=section(y);normal=Vector((math.sin(theta)/rx,0,math.cos(theta)/rz)).normalized();cross=Vector((math.cos(theta),0,-math.sin(theta))).normalized();long=Vector((0,1,0))
 center=Vector((rx*math.sin(theta),y,z+rz*math.cos(theta)))-normal*.0014
 verts=[center-cross*width,center-long*length,center+cross*width,center+long*length,center-long*length*.45+normal*height,center+long*length*.42+normal*height*.8]
 faces=[(0,1,4),(1,2,4),(2,5,4),(2,3,5),(3,0,5),(0,4,5),(3,2,1,0)]
 scutes.add([tuple(v) for v in verts],faces,mi);scute_count+=1
# Loose staggered trunk and neck positions. Seven strips are not a literal life-row claim.
for j,t in enumerate([0,-.42,.42,-.84,.84,-1.20,1.20]):
 for i in range(18):
  y=-.280+i*.020+(j%2)*.010;scale=.72 if y<-.235 else 1.0
  scute(y,t+random.uniform(-.04,.04),.0073*scale,.0095*scale,.0055*scale,0 if abs(t)<.8 else 1)
# Neck below skull, smaller low units.
for j,t in enumerate([0,-.62,.62]):
 for i in range(3):scute(-.329+i*.014+(j%2)*.005,t,.0047,.006,.0038,0)
# Tail scutes decrease continuously to tiny bumps; no terminal weapon.
for j,t in enumerate([0,-.66,.66]):
 for i in range(26):
  y=.091+i*.022+(j%2)*.008;factor=max(.18,1-(y-.09)/.72)
  scute(y,t,.0065*factor,.009*factor,.0048*factor,0 if j==0 else 1)
scutes.finish('Illustrative low keeled osteoderms',[m['osteoderm'],m['osteoderm_side']])
# Small eye lenses, nostrils and fine closed-mouth seam. None are horns.
face=Group()
for sign in (-1,1):
 tube(face,[(sign*.0254,-.384,.360),(sign*.0270,-.384,.360),(sign*.0273,-.384,.360)],[(.0053,.0053),(.0045,.0045),(.003,.003)],10)
 tube(face,[(sign*.015,-.432,.350),(sign*.0173,-.432,.350)],[.0017,.0015],6)
 mouth=[]
 theta=2.09;k=int(theta/(2*math.pi/16));blend=(theta-k*2*math.pi/16)/(2*math.pi/16)
 ax=math.sin(k*2*math.pi/16)*(1-blend)+math.sin((k+1)*2*math.pi/16)*blend
 az=math.cos(k*2*math.pi/16)*(1-blend)+math.cos((k+1)*2*math.pi/16)*blend
 for yy in [-.443,-.430,-.405,-.386]:
  zz,rx,rz=section(yy);mouth.append((sign*(rx*ax+.0002),yy,zz+rz*az))
 tube(face,mouth,[.00045,.00045,.00045,.00035],5)
face.finish('Eyes nostrils and closed-mouth seams',m['eyes'])
# Align intended toe contacts exactly with Z=0, retaining root identity and footprint-centered XY.
shift=ac.ground_asset(col,center_xy=False)
bpy.context.view_layer.update()
footpoints=[o.matrix_world@v.co for o in col.objects if o.type=='MESH' and ('Hind limb' in o.name or 'toe claws' in o.name) for v in o.data.vertices if (o.matrix_world@v.co).z<.025]
foot_offset=Vector(tuple(-(min(v[i] for v in footpoints)+max(v[i] for v in footpoints))/2 for i in (0,1))+(0,))
for o in col.objects:
 if o.type=='MESH':o.location+=foot_offset
shift=[shift[i]+foot_offset[i] for i in range(3)]
bpy.context.view_layer.update()
root=bpy.data.objects[col['asset_root']];root['scute_count']=scute_count;root['scute_arrangement']='Artistic, not known from disarticulated fossils';root['life_reconstruction']='Original stylized Scutellosaurus lawleri';root['specimen_scale']='Approximate genus length 1.2m, not specimen measurement'
source=ac.audit_source(col,p['max_triangles']);assert not source['errors'],source['errors']
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
missing=set(opts)-{x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties};assert not missing,missing
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(out/'model.glb',p['max_triangles'],p['max_materials'],p['max_primitives']);glb['file']='model.glb';assert not glb['errors'],glb['errors'];assert glb['bytes']<=p['max_glb_bytes']
b=source['bounds_blender_m'];expected_min=[b['min'][0],b['min'][2],-b['max'][1]];expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
err=max(abs(glb['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3));assert err<1e-5,err
save(out/'qa/evidence/technical.json',{'status':'PASS','scope':'Source geometry and static uncompressed standalone GLB only','source':source,'glb':glb,'source_to_export_max_bound_error_m':err,'blender_version':bpy.app.version_string,'generator_sha256':digest(__file__),'params_sha256':digest(HERE/'params.json'),'scute_count':scute_count,'scute_count_claim':'Artistic modeled count only; not a fossil count or known life arrangement','ground_shift_m':shift,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'blend_sha256':digest(out/'model.blend'),'gpu':'NOT_RUN','populated_scene':'NOT_RUN'})
if a.gray or a.final:
 from render_model import render_glb
 render_glb(out,gray=a.gray)
print('BUILD_COMPLETE',glb['sha256'],glb['scene_triangles'],scute_count)
