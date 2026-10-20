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
# Original geometry authored after four immutable premodel freezes2026-10-20T15:44:14.790616Z.
if slug=='rangea':
 # Single closed six-lobed bilaminar radial spindle. No stacked intersection tubes.
 nz=58;np=108;vs=[]
 for j in range(nz+1):
  t=.018+.964*j/nz;x=.14*(t-.5);width=.021*math.sin(math.pi*t)**.83
  for i in range(np):
   ph=math.tau*i/np;sector=round(ph/(math.pi/3));axis=sector*math.pi/3;q=(ph-axis)/(math.pi/6)
   core=.0013*math.sin(math.pi*t)**.6;u=abs(q)
   phase=t*12*math.tau+u*5.0
   primary=max(0,math.cos(phase))**3
   secondary=max(0,math.cos(t*25*math.tau+u*15))**5
   radial=core*math.cos(q*math.pi/6)+width*(1-u)**.85
   tang=core*math.sin(q*math.pi/6)
   if u>1e-8:tang+=math.copysign((.0003+.0012*primary+.00022*secondary)*math.sin(math.pi*u)**.45*math.sin(math.pi*t),q)
   vs.append((x,radial*math.cos(axis)-tang*math.sin(axis),radial*math.sin(axis)+tang*math.cos(axis)))
 fs=[]
 for j in range(nz):
  for i in range(np):
   a=j*np+i;b=j*np+(i+1)%np;c=b+np;d=a+np;fs.extend([(a,b,c),(a,c,d)])
 lo=len(vs);vs.append((-.14*(.5-.018),0,0));hi=len(vs);vs.append((.14*(.5-.018),0,0))
 fs.extend((lo,(i+1)%np,i) for i in range(np));fs.extend((hi,nz*np+i,nz*np+(i+1)%np) for i in range(np))
 part('six_bilaminar_radial_vanes_integrated_hierarchical_ribbed_fossil',vs,fs,'fossil')
elif slug=='serac':
 nx=57;ny=57;vs=[]
 for i in range(nx):
  for j in range(ny):
   x=-15+30*i/(nx-1);y=-15+30*j/(ny-1)
   u=x+.6*math.sin(y*.27)+.18*math.sin(y*.87)
   v=y+.5*math.sin(x*.31+1)
   dx=min(abs(u-4.1),abs(u+4.4));dy=min(abs(v-4.0),abs(v+4.7));d=min(dx,dy)
   ch=max(0,min(1,(d-.28)/.88));ch=ch*ch*(3-2*ch)
   central=abs(u)<3.6 and abs(v)<3.5
   roof=(16.8+.045*x-.12*y+1.0*math.sin(x*.6)*math.sin(y*.42)) if central else (5.5+.09*y+.6*math.sin(x*.35+y*.18))
   z=.65+(roof-.65)*ch
   if not central:z+=.15*math.sin(i*2.1+j*.7)*ch
   vs.append((x,y,z))
 fs,per=grid_faces(nx,ny);terrain('continuous_glacier_angular_tower_two_crossing_crevasse_systems',vs,fs,per,0,'ice')
elif slug=='moulin-shaft':
 n=64;nr=10;vs=[]
 def boundary(ph,k):
  # Rays connect an asymmetric opening to a square glacier tile.
  c=math.cos(ph);s=math.sin(ph);outer=10/max(abs(c),abs(s));inner=3.2*(1+.13*math.sin(3*ph)+.08*math.cos(5*ph))
  r=inner+(outer-inner)*k/nr;x=r*c;y=r*s
  inlet=math.exp(-(angdist(ph,math.pi/2)/.13)**2)
  z=11.8+.13*math.sin(ph*5+k*.9)-1.15*inlet
  return (x,y,z)
 for k in range(nr+1):
  for i in range(n):vs.append(boundary(math.tau*i/n,k))
 fs=[]
 for k in range(nr):
  for i in range(n):
   a=k*n+i;b=k*n+(i+1)%n;c=b+n;d=a+n;fs.extend([(a,d,c),(a,c,b)])
 # Inner walls are steep and visibly have depth, with a genuine open truncated lower shaft.
 inner_last=list(range(n))
 for level in [8.1,4.1,0]:
  start=len(vs)
  for i in range(n):
   ph=math.tau*i/n;x,y,z=boundary(ph,0);scale=.93 if level>4 else .85
   vs.append((x*scale,y*scale,level))
  new=list(range(start,start+n))
  for i in range(n):fs.append((inner_last[i],inner_last[(i+1)%n],new[(i+1)%n],new[i]))
  inner_last=new
 outerbottom=[]
 for i in range(n):
  x,y,z=vs[nr*n+i];outerbottom.append(len(vs));vs.append((x,y,0))
 for i in range(n):
  a=nr*n+i;b=nr*n+(i+1)%n;c=outerbottom[(i+1)%n];d=outerbottom[i];fs.append((a,b,c,d));fs.append((d,c,inner_last[(i+1)%n],inner_last[i]))
 part('true_open_upper_moulin_annular_ice_volume',vs,fs,'ice')
 # Original ribbon is inside the carved inlet/shaft, not a coplanar decal.
 wv=[]
 for k in range(12):
  y=10-6.9*k/11;z=10.70+.035*math.sin(k*.5)
  wv.extend([(-.29,y,z),(.29,y,z)])
 wf=[(2*k,2*k+1,2*k+3,2*k+2) for k in range(11)]
 part('shallow_surface_meltwater_inlet',wv,wf,'water')
 ph=math.pi/2;x,y,z=boundary(ph,0)
 part('upper_wall_meltwater_descent',[(-.24,y-.17,10.66),(.24,y-.17,10.66),(.19,y*.92-.15,4.35),(-.19,y*.92-.15,4.35)],[(0,3,2,1)],'water')
elif slug=='solifluction-lobe':
 nx=53;ny=65;vs=[]
 def lobe(x,y):
  width=5.3;u=abs(x-.25*math.sin(y*.3))/width
  if u>=1:return 0
  front=5.1+3.0*u*u+.18*math.sin(x*1.2)
  q=max(0,min(1,(y-front)/.45));q=q*q*(3-2*q)
  neck=max(0,min(1,(18.5-y)/4.8));neck=neck*neck*(3-2*neck)
  edge=max(0,min(1,(1-u)/.16));edge=edge*edge*(3-2*edge)
  return .65*q*neck*edge
 for i in range(nx):
  for j in range(ny):
   x=-9+18*i/(nx-1);y=24*j/(ny-1)
   z=1+.115*y+lobe(x,y)+.035*math.sin(x*.7+y*.4)
   # One much subtler offset partial lobe, not regular steps.
   z+=.12*math.exp(-((x+5)/3)**4)*math.exp(-((y-20)/2.2)**4)
   vs.append((x,y-12,z))
 fs,per=grid_faces(nx,ny);terrain('continuous_soil_mantle_shallow_rounded_downslope_tongue',vs,fs,per,0,'turf')

for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if slug in ['serac','moulin-shaft'] and mat=='ice':
  obj.data.materials.append(m['pale']);obj.data.materials.append(m['deepice' if slug=='serac' else 'wall'])
  for poly in obj.data.polygons:poly.material_index=1 if poly.normal.z>.55 else 2 if poly.normal.z<.4 else 0
 if slug=='solifluction-lobe':
  obj.data.materials.append(m['soil']);obj.data.materials.append(m['turfshade'])
  for poly in obj.data.polygons:
   if poly.normal.z<.85:poly.material_index=1
   elif math.sin(poly.center.x*.9+poly.center.y*.7)>.65:poly.material_index=2
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
