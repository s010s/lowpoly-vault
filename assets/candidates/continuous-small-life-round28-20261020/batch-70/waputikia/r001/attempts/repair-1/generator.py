# SPDX-License-Identifier: MIT
"""Original batch70 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
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


# Original batch70 geometry authored after2026-10-20T14:18:58Z premodel freezes.
import random
rng=random.Random(cfg['seed'])
def matmesh(name,vs,fs,labels):
 keys=list(cfg['palette']);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,labels):p.material_index=keys.index(k)
 return o

def polar_solid(name,ring,zbottom,mat):
 n=len(ring);bottom=[(x,y,zbottom) for x,y,z in ring]
 loft(name,[bottom,ring],mat)

def waputikia():
 # Vertical specimen mount, finite broken thick axis; no inferred organism base.
 n=23;boundary=[]
 for i in range(n):
  a=i*math.tau/n;rr=1+.065*math.sin(i*1.81)+.025*math.cos(i*.7)
  boundary.append((.049*rr*math.cos(a),.0015,.044+.047*rr*math.sin(a)))
 # Surface support vertical to retain all specimen branches in front silhouette.
 vs=[(x,y+.003,z) for x,y,z in boundary]+boundary;fs=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))];labs=['edge','shale']
 for i in range(n):fs.append((i,(i+1)%n,(i+1)%n+n,i+n));labs.append('edge')
 matmesh('irregular_shale_specimen_support',vs,fs,labs)
 axis=[(-.003,0,.008),(-.001,-.0002,.024),(.002,-.0003,.045),(.0005,0,.064),(.004,0,.074)]
 tube('robust_preserved_axis',axis,[.0032,.0034,.0027,.0022,.0014],'fossil',7)
 # Irregular major branch positions, angle and lengths, unlike uniform tree whorls.
 majors=[((-.001,-.0008,.020),(-.025,-.001,.032),.0021),((.0005,-.0009,.030),(.026,-.0015,.040),.0023),((.0015,-.0008,.042),(-.023,-.001,.055),.0019),((.001,-.0008,.052),(.020,-.001,.061),.0016),((.001,-.0008,.061),(-.013,-.001,.072),.0013)]
 def split(p,d,length,r,depth):
  # Fine terminal dichotomous fans in specimen plane, not leaves or foliage.
  end=(p[0]+math.cos(d)*length,p[1]+rng.uniform(-.00008,.00008),p[2]+math.sin(d)*length)
  mid=((p[0]+end[0])*.5,p[1]-.00005,(p[2]+end[2])*.5)
  tube('dichotomous_fine_terminal_sprays',[p,mid,end],[r,r*.79,max(.00013,r*.5)],'fossil',5)
  if depth:
   for sign in [-1,1]:split(end,d+sign*rng.uniform(.30,.61),length*rng.uniform(.56,.72),max(.00013,r*.48),depth-1)
 for p,e,r in majors:
  mid=((p[0]+e[0])*.5,-.0012,(p[2]+e[2])*.5);tube('irregular_stout_lateral_branches',[p,mid,e],[r,r*.77,r*.40],'fossil',6)
  d=math.atan2(e[2]-p[2],e[0]-p[0])
  for sign in [-1,1]:split(e,d+sign*.48,.0072,r*.33,4)
 # Smaller irregular terminal fan on the preserved distal axis end, no crown organism claim.
 split(axis[-1],1.3,.004,.00038,3)

def dune():
 nx=43;cross=[-1,-.70,-.30,0,.34,.74,1];vs=[];fs=[];labels=[]
 for i in range(nx):
  t=i/(nx-1);x=-100+200*t;cy=3.6*math.sin(2.0*math.pi*t-.5)+1.1*math.sin(5.1*math.pi*t);height=.8+15.8*math.sin(math.pi*t)**.63*(.94+.09*math.sin(t*19));width=5+12*math.sin(math.pi*t)**.7
  for j,u in enumerate(cross):
   y=cy+u*width;z=1.2+height*(1-abs(u))**.92
   if u:z+=.25*math.sin(i*1.7+j*2.1)*math.sin(math.pi*t)*abs(u)
   vs.append((x,y,z))
 for i in range(nx-1):
  for j in range(6):
   a=i*7+j;b=a+7
   for f in [(a,a+1,b+1),(a,b+1,b)]:fs.append(f);labels.append('light' if j==2 else 'shade' if j>3 else 'sand')
 perimeter=list(range(7))+[i*7+6 for i in range(1,nx)]+[(nx-1)*7+j for j in range(5,-1,-1)]+[i*7 for i in range(nx-2,0,-1)]
 bot=[]
 for k in perimeter:bot.append(len(vs));vs.append((vs[k][0],vs[k][1],0))
 for i,k in enumerate(perimeter):q=(i+1)%len(perimeter);fs.append((k,perimeter[q],bot[q],bot[i]));labels.append('base')
 fs.append(tuple(reversed(bot)));labels.append('base');matmesh('one_longitudinal_sinuous_two_flank_sand_ridge',vs,fs,labels)

def kettle():
 # Irregular jittered triangulated terrain, continuous low floor below hummocks.
 nx=29;ny=27;vs=[];fs=[];labs=[]
 hummocks=[(-28,-19,2.2,11),(-23,20,2.5,13),(19,22,1.8,12),(29,-12,2.1,10),(2,27,1.5,10),(-34,3,1.4,9)]
 def height(x,y):
  rr=math.sqrt(((x-2)/23)**2+((y+1)/18)**2)
  h=2.8+2.5*(1-math.exp(-rr**3))
  for a,b,c,d in hummocks:h+=c*math.exp(-((x-a)**2+(y-b)**2)/(d*d))
  h+=.25*math.sin(x*.19+y*.22)+.12*math.sin(x*.42-y*.31)
  return h
 for j in range(ny):
  for i in range(nx):
   x=-40+80*i/(nx-1);y=-34+68*j/(ny-1)
   if 0<i<nx-1 and 0<j<ny-1:x+=rng.uniform(-.55,.55);y+=rng.uniform(-.55,.55)
   vs.append((x,y,height(x,y)))
 for j in range(ny-1):
  for i in range(nx-1):
   a=j*nx+i;b=a+nx
   faces=[(a,a+1,b),(a+1,b+1,b)] if (i+j)%2 else [(a,a+1,b+1),(a,b+1,b)]
   for f in faces:
    fs.append(f);av=sum(vs[k][2] for k in f)/3;labs.append('grass' if av>5.0 and rng.random()<.7 else 'till')
 perimeter=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)]
 bot=[]
 for k in perimeter:bot.append(len(vs));vs.append((vs[k][0],vs[k][1],0))
 for i,k in enumerate(perimeter):q=(i+1)%len(perimeter);fs.append((k,perimeter[q],bot[q],bot[i]));labs.append('earth')
 fs.append(tuple(reversed(bot)));labs.append('earth');matmesh('continuous_hummocky_glacial_till_closed_depression',vs,fs,labs)
 # Water surface follows real below-water contour via clipping grid triangles. No circular added rim.
 waterz=3.65;wv=[];wf=[]
 def clip(poly):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   f=p[2]-waterz;g=q[2]-waterz
   if f<=0:out.append((p[0],p[1],waterz))
   if (f<0)!=(g<0):t=f/(f-g);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1]),waterz))
  return out
 # Thin closed water patches fully embedded in till; original floor continuous beneath.
 for f in fs[:2*(nx-1)*(ny-1)]:
  poly=clip([vs[k] for k in f])
  if len(poly)>=3:
   n=len(poly);idx=len(wv);wv.extend([(x,y,z-.04) for x,y,z in poly]+poly);wf.extend([tuple(idx+i for i in range(n-1,-1,-1)),tuple(idx+n+i for i in range(n))]);wf.extend([(idx+i,idx+(i+1)%n,idx+n+(i+1)%n,idx+n+i) for i in range(n)])
 part('shallow_partial_pond',wv,wf,'water')
 for k in range(18):
  x=rng.uniform(-36,36);y=rng.uniform(-30,30);z=height(x,y)
  if z<waterz+.35:continue
  s=rng.uniform(.4,1.0);ellipsoid('irregular_embedded_till_stones',(x,y,z-.07),(s,s*.76,s*.58),'stone',7,3)

def rimstone():
 n=61;ring=[]
 for i in range(n):
  a=math.tau*i/n;r=1+.13*math.sin(3*a+.4)+.06*math.sin(5*a-1.1)+.035*math.cos(8*a+.8)
  ring.append((.94*r*math.cos(a),.62*r*math.sin(a)))
 # Original attached cave floor extends beyond entire enclosure, closed volume.
 floor=[]
 for i,(x,y) in enumerate(ring):floor.append((x*1.26,y*1.30,.12+.018*math.sin(i*.77)))
 polar_solid('attached_original_cave_floor',floor,0,'floor')
 vs=[];fs=[];labels=[]
 # Four perimeter loops produce annular wall, not capped overlapping bowls.
 for layer in range(4):
  for i,(x,y) in enumerate(ring):
   inner=layer>=2;s=.967 if inner else 1.0;z=.30+.018*math.sin(i*.91)+.008*math.cos(i*1.37) if layer in [1,2] else .10
   vs.append((x*s,y*s,z))
 for k in range(4):
  kk=(k+1)%4
  for i in range(n):j=(i+1)%n;fs.append((k*n+i,k*n+j,kk*n+j,kk*n+i));labels.append('crest' if k==1 else 'calcite')
 matmesh('one_thin_sinuous_calcite_enclosing_dam',vs,fs,labels)
 # Opaque shallow original water volume fully below crest and inside wall.
 water=[(x*.965,y*.965,.263) for x,y in ring];polar_solid('one_enclosed_cave_pool',water,.119,'water')

{'waputikia':waputikia,'linear-dune':dune,'kettle-basin':kettle,'rimstone-dam':rimstone}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
