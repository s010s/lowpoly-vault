# SPDX-License-Identifier: MIT
"""Original batch74 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
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


# Geometry authored after actual batch74 design freeze2026-10-20T15:20:41Z.
import random
rng=random.Random(cfg['seed'])
def terrain(name,vs,fs,per,bottom,mat):
 n=len(vs);k=len(per);v=vs+[(vs[i][0],vs[i][1],bottom) for i in per]
 faces=list(fs)+[(per[i],per[(i+1)%k],n+(i+1)%k,n+i) for i in range(k)]+[tuple(n+i for i in reversed(range(k)))]
 part(name,v,faces,mat)
def grid_faces(nx,ny):
 fs=[]
 for i in range(nx-1):
  for j in range(ny-1):
   a=i*ny+j;b=a+ny
   fs.extend([(a,b,b+1),(a,b+1,a+1)] if (i+j)%2 else [(a,b,a+1),(b,b+1,a+1)])
 per=[i*ny for i in range(nx)]+[(nx-1)*ny+j for j in range(1,ny)]+[i*ny+ny-1 for i in reversed(range(nx-1))]+[j for j in reversed(range(1,ny-1))]
 return fs,per
def angdist(a,b):return (a-b+math.pi)%math.tau-math.pi
if slug=='tribrachidium':
 # One continuous positive-relief original fossil-form surface. No embedded tubes.
 n=96;nr=24;vs=[(0,0,.0029)]
 def height(r,ph):
  u=r/.02;z=.00085+.00155*max(0,1-u*u)
  for k in range(3):
   # Positive angle sweep outward is counterclockwise in +Z view.
   axis=k*math.tau/3-.4+1.15*u*u
   d=angdist(ph,axis);width=.19+.045*u
   z+=.00135*math.exp(-(d/width)**2)*math.sin(min(1,u/.9)*math.pi*.8)
   # Bulla stays on inner primary ridge, pits occupy intervening sectors.
   z+=.00040*math.exp(-((u-.35)/.16)**2-(d/.31)**2)
   pitaxis=k*math.tau/3+.55
   z-=.00052*math.exp(-((u-.32)/.16)**2-(angdist(ph,pitaxis)/.43)**2)
   # Subordinate faint roughly transverse relief. Never free appendages.
   z+=.00011*math.exp(-((abs(d)-.34)/.2)**2)*max(0,math.cos(u*53+d*6))**8*math.sin(math.pi*u)**2
  return z+.000025*math.sin(ph*9+u*17)*math.sin(math.pi*u)
 for j in range(1,nr+1):
  r=.02*j/nr
  for i in range(n):
   ph=math.tau*i/n;rr=r*(1+.012*math.sin(5*ph)+.008*math.cos(9*ph))
   vs.append((rr*math.cos(ph),rr*math.sin(ph),height(r,ph)))
 fs=[(0,1+i,1+(i+1)%n) for i in range(n)]
 for j in range(nr-1):
  for i in range(n):
   a=1+j*n+i;b=1+j*n+(i+1)%n;c=b+n;d=a+n;fs.extend([(a,b,c),(a,c,d)])
 per=[1+(nr-1)*n+i for i in range(n)]
 terrain('integrated_low_positive_relief_three_armed_fossil_form',vs,fs,per,0,'sandstone')
elif slug=='arete-ridge':
 nx=57;ys=[-50,-43,-34,-26,-18,-11,-5,-1.4,0,1.4,5,11,18,26,34,43,50];ny=len(ys);vs=[]
 crest=[(-120,23),(-108,34),(-94,47),(-80,35),(-66,56),(-52,42),(-37,51),(-23,32),(-8,43),(7,59),(20,46),(34,50),(46,35),(61,48),(77,32),(92,44),(106,30),(120,24)]
 def line(x):
  for a,b in zip(crest,crest[1:]):
   if a[0]<=x<=b[0]:return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0])
  return 25
 for i in range(nx):
  x=-120+240*i/(nx-1);cy=2.2*math.sin(x*.035)+.8*math.sin(x*.08)
  for j,y in enumerate(ys):
   t=abs(y)/50;h=line(x);profile=(1-t)**2.5
   # Asymmetric hollow floors with buttresses at ends; both concave slopes remain.
   z=2+h*profile+3.2*(abs(x)/120)**3*math.sin(math.pi*t)**2
   z+=.7*math.sin(x*.17+j*.72)*math.sin(math.pi*t)
   xx=x+(.6*math.sin(i*1.7+j*2) if i not in [0,nx-1] and j!=8 else 0)
   vs.append((xx,y+cy*(1-t),z))
 fs,per=grid_faces(nx,ny);terrain('one_continuous_serrated_arete_two_concave_hollows',vs,fs,per,0,'rock')
elif slug=='crevasse-splay':
 paths=[[(-39,-60,5),(-37,-35,5),(-38,-12,5),(-40,12,5),(-39,38,5),(-37,60,5)],
 [(-38,-12,3.5),(-25,-12,3.4),(-13,-10,3.2),(0,-7,2.8),(16,-1,2.2),(31,6,1.6),(49,15,.8)],
 [(-13,-10,2.6),(-1,0,2.1),(10,13,1.8),(24,25,1.2),(38,33,.6)],
 [(0,-7,2.4),(14,-13,2),(29,-15,1.3),(47,-12,.7)],
 [(-1,0,1.8),(1,14,1.6),(9,28,1.0),(14,41,.5)],
 [(14,-13,1.7),(23,-27,1.4),(38,-34,.7)],
 [(16,-1,1.6),(28,0,1.2),(45,-1,.5)]]
 segments=[(p[i],p[i+1]) for p in paths for i in range(len(p)-1)]
 def channel(x,y):
  best=999
  for a,b in segments:
   dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
   best=min(best,math.hypot(x-a[0]-dx*t,y-a[1]-dy*t)/(a[2]*(1-t)+b[2]*t))
  return best
 def fan(x,y):
  xx=x+25;yy=y+12
  if xx<=0:return 0
  rr=math.hypot(xx,yy*.86);a=abs(math.atan2(yy,xx))
  return max(0,1-(rr/85)**3)*max(0,min(1,(.84-a)*5))
 nx=58;ny=58;vs=[]
 for i in range(nx):
  for j in range(ny):
   x=-60+120*i/(nx-1);y=-60+120*j/(ny-1)
   if i not in [0,nx-1] and j not in [0,ny-1]:x+=rng.uniform(-.24,.24);y+=rng.uniform(-.24,.24)
   f=fan(x,y);lev=2.0*math.exp(-((x+25)/3.1)**2)*(1-math.exp(-((y+12)/5.2)**4))
   lev+=1.3*math.exp(-((x+50)/4)**2)
   base=2.15+.55*f+.06*math.sin(x*.4+y*.17)+lev
   d=channel(x,y);u=max(0,min(1,(d-.35)/1.0));s=u*u*(3-2*u)
   z=1.05+(base-1.05)*s;vs.append((x,y,z))
 fs,per=grid_faces(nx,ny)
 # One terrain object, shared vertices/material indices. No layered coplanar fan patches.
 terrain('integrated_breached_levee_fan_and_incised_floodplain',vs,fs,per,0,'floodplain')
 water_v=[];water_f=[];level=1.68
 for tri in fs:
  poly=[vs[k] for k in tri];cl=[]
  for k,p in enumerate(poly):
   q=poly[(k+1)%3];inside=p[2]<level
   if inside:cl.append((p[0],p[1],level))
   if inside!=(q[2]<level):
    t=(level-p[2])/(q[2]-p[2]);cl.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1]),level))
  if len(cl)>=3:
   nn=len(water_v);water_v.extend(cl);water_f.extend((nn,nn+k,nn+k+1) for k in range(1,len(cl)-1))
 part('continuous_shallow_water_clipped_to_actual_channels',water_v,water_f,'water')
elif slug=='coal-seam-outcrop':
 # Full host beds, genuinely recessed coal, uneven orthogonal cleat segmentation.
 outline=[(-1.8,-.69),(-1.35,-.77),(-.75,-.67),(-.2,-.73),(.45,-.64),(1.1,-.72),(1.72,-.60),(1.83,-.12),(1.69,.63),(.85,.71),(.05,.64),(-.85,.73),(-1.73,.58)]
 for name,z0,z1,mat in [('resistant_lower_host_bed',0,.74,'hostshade'),('resistant_upper_host_bed',1.62,2.48,'host')]:
  rings=[]
  for lev in range(3):
   z=z0+(z1-z0)*lev/2;rings.append([(x*(1-.025*lev),y*(1-.035*lev),z+(.045*math.sin(k*2.3+lev) if lev else 0)) for k,(x,y) in enumerate(outline)])
  loft(name,rings,mat)
 cuts=[-1.70,-1.39,-1.18,-.84,-.39,-.16,.22,.47,.91,1.17,1.48,1.68]
 for i,(x0,x1) in enumerate(zip(cuts,cuts[1:])):
  yfront=-.39+.055*math.sin(i*1.9);ys=[yfront,-.04+.06*math.sin(i*2.8),.25+.04*math.cos(i),.61]
  for j,(ya,yb) in enumerate(zip(ys,ys[1:])):
   gap=.015 if j else .013;a=x0+.013;b=x1-.013;c=ya+gap;d=yb-gap;z0=.79+.015*math.sin(i+j);z1=1.57-.02*math.cos(i*2+j)
   # Inset beveled/chipped front corners, not regular rectangular masonry.
   w=min(.045,(b-a)*.15);xy=[(a+w,c),(b-w*.7,c+.012*math.sin(i)),(b,c+w),(b,d-w*.8),(b-w,d),(a+w*.8,d),(a,d-w),(a,c+w)]
   rings=[[(x,y,z0) for x,y in xy],[(x+(rng.uniform(-.012,.012)),y+(rng.uniform(-.012,.012)),z0+(z1-z0)*.54) for x,y in xy],[(x,y,z1) for x,y in xy]]
   loft('unequal_face_cleat_blocks_short_terminating_butt_cleats',rings,'coalbright' if (i+j)%4==0 else 'coal')

for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if slug=='crevasse-splay' and name.startswith('integrated_'):
  obj.data.materials.append(m['sand']);obj.data.materials.append(m['levee'])
  for poly in obj.data.polygons:
   c=poly.center
   if poly.normal.z>.1:
    if fan(c.x,c.y)>.09:poly.material_index=1
    if abs(c.x+25)<5 and abs(c.y+12)>6 or abs(c.x+50)<5:poly.material_index=2
 if slug=='arete-ridge':
  obj.data.materials.append(m['shadowrock']);obj.data.materials.append(m['palerock'])
  for poly in obj.data.polygons:
   if poly.normal.z>.1:poly.material_index=1 if poly.normal.y>.25 else 2 if poly.normal.y<-.35 and poly.center.z>18 else 0

ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
