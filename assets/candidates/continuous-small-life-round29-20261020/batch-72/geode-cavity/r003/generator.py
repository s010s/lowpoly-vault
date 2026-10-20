# SPDX-License-Identifier: MIT
"""Original batch72 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
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


# Original geometry authored after complete 2026-10-20T14:52:28Z design freeze.
import random
from mathutils.geometry import tessellate_polygon
rng=random.Random(cfg['seed'])
def prism_polygon(name,xy,z0,z1,mat):
 n=len(xy);vs=[(x,y,z0) for x,y in xy]+[(x,y,z1) for x,y in xy]
 tris=tessellate_polygon([[Vector((x,y,0)) for x,y in xy]])
 # Resolve tessellation vertices to immutable outline indices.
 ix=lambda v:v if isinstance(v,int) else min(range(n),key=lambda i:(xy[i][0]-v.x)**2+(xy[i][1]-v.y)**2)
 fs=[tuple(ix(v)+n for v in t) for t in tris]+[tuple(reversed([ix(v) for v in t])) for t in tris]
 fs += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 part(name,vs,fs,mat)
def terrain_volume(name,vs,faces,perimeter,bottom,mat):
 n=len(vs);v=vs+[(vs[i][0],vs[i][1],bottom) for i in perimeter];fs=list(faces);k=len(perimeter)
 fs.extend((perimeter[i],perimeter[(i+1)%k],n+(i+1)%k,n+i) for i in range(k))
 fs.append(tuple(n+i for i in reversed(range(k))));part(name,v,fs,mat)
if slug=='baiera':
 outline=[]
 for i in range(24):
  a=math.tau*i/24;r=1+.045*math.sin(3*a+.7)+.055*math.cos(7*a)
  outline.append((.055*r*math.cos(a),.074*r*math.sin(a)))
 prism_polygon('thin_irregular_original_shale_support',outline,0,.004,'shale')
 # One flattened silhouette, genuine deep notches and two unequal distal forks.
 base=(0,-.036);angles=[-49,-37,-25,-10,4,19,35,48];lengths=[.077,.091,.099,.104,.105,.099,.090,.076]
 notches=[.059,.029,.031,.056,.030,.034,.054]
 xy=[(-.0015,-.066),(-.0022,-.035)]
 for i,(deg,length) in enumerate(zip(angles,lengths)):
  a=math.radians(deg);w=.0018 if i in [0,7] else .0025
  cx=length*math.sin(a);cy=base[1]+length*math.cos(a)
  xy.extend([(cx-w*math.cos(a),cy+w*math.sin(a)),(cx+w*math.cos(a),cy-w*math.sin(a))])
  if i<len(notches):
   a2=math.radians((deg+angles[i+1])/2);rr=notches[i];xy.append((rr*math.sin(a2),base[1]+rr*math.cos(a2)))
 xy.extend([(.0022,-.035),(.0015,-.066)])
 prism_polygon('one_flat_deeply_divided_Baiera_leaf',xy,.00402,.00465,'leaf')
 # Sparse restrained relief lines follow the selected lobe axes, not invented reticulation.
 for i in [0,2,4,6]:
  a=math.radians(angles[i]);L=lengths[i];pts=[]
  for r in [.020,L*.62,L*.95]:pts.append((r*math.sin(a),base[1]+r*math.cos(a),.00469))
  # Broad shallow strips rather than cylindrical needle anatomy.
  left=[(x-.00020,y) for x,y,z in pts];right=[(x+.00020,y) for x,y,z in reversed(pts)]
  prism_polygon('subordinate_parallel_relief',left+right,.00464,.00476,'vein')
elif slug=='transverse-dune-ridge':
 # Width across wind is X. Long windward ramp, short steep slipface in Y.
 nx=35;sections=[(-52,0),(-43,.4),(-32,1.9),(-19,4.6),(-6,8.0),(3,11.4),(9,14.5),(16,10.2),(25,5.0),(34,0),(38,0)]
 vs=[]
 for i in range(nx):
  x=-60+120*i/(nx-1);wave=2.2*math.sin(x*.059)+.8*math.sin(x*.131+.7);hscale=1+.055*math.sin(x*.072+.4)
  for j,(y,h) in enumerate(sections):
   dy=wave*(h/14.5);jit=.55*math.sin(i*2.7+j*1.9) if j not in [0,len(sections)-1] else 0
   # Crest and slipface remain continuous with fine nonperiodic faceting.
   xx=x+(.45*math.sin(j*3.1+i) if i not in [0,nx-1] else 0)
   z=h*hscale+(jit*.18 if h>0 and j!=6 else 0)
   vs.append((xx,y+dy,max(0,z)+2.0))
 ny=len(sections);fs=[]
 for i in range(nx-1):
  for j in range(ny-1):
   a=i*ny+j;b=a+ny
   fs += [(a,b,b+1),(a,b+1,a+1)] if (i+j)%2 else [(a,b,a+1),(b,b+1,a+1)]
 per=[i*ny for i in range(nx)]+[(nx-1)*ny+j for j in range(1,ny)]+[i*ny+ny-1 for i in reversed(range(nx-1))]+[j for j in reversed(range(1,ny-1))]
 terrain_volume('continuous_transverse_asymmetric_ridge',vs,fs,per,0,'sand')
elif slug=='braided-river-reach':
 # Deliberately unequal branch graph. Centerline coordinates are (x,y,width).
 paths=[[(0,-75,5),(-4,-58,5),(-14,-39,4),(-9,-16,5),(5,4,5),(15,26,5),(7,47,5),(-1,75,6)],
 [(0,-75,4),(13,-57,3.7),(22,-37,3.3),(19,-18,4),(5,4,4)],
 [(-4,-58,3.2),(-22,-41,3.3),(-26,-16,3.8),(-18,6,4),(-4,24,4),(7,47,4)],
 [(19,-18,2.6),(27,4,3),(22,22,3.2),(15,26,3.7)],
 [(-18,6,2.8),(-23,31,3),(-17,56,4),(-1,75,5)],
 [(-9,-16,2.2),(0,-13,2.4),(12,-8,2.7),(19,-18,2.6)],
 [(-4,24,2.2),(3,35,2.5),(7,47,3.3)]]
 segments=[(p[i],p[i+1]) for p in paths for i in range(len(p)-1)]
 def nearest(x,y):
  best=999
  for a,b in segments:
   dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
   dist=math.hypot(x-a[0]-dx*t,y-a[1]-dy*t);w=a[2]*(1-t)+b[2]*t
   best=min(best,dist/w)
  return best
 nx,ny=45,79;vs=[]
 for i in range(nx):
  for j in range(ny):
   x=-41+82*i/(nx-1);y=-75+150*j/(ny-1)
   if i not in [0,nx-1] and j not in [0,ny-1]:x+=rng.uniform(-.30,.30);y+=rng.uniform(-.28,.28)
   d=nearest(x,y);u=max(0,min(1,(d-.42)/.94));smooth=u*u*(3-2*u)
   z=1.3+2.4*smooth+.13*math.sin(x*.41+y*.15)*smooth+.11*math.cos(y*.31-x*.21)*smooth
   vs.append((x,y,z))
 fs=[];water_v=[];water_f=[];level=2.38
 for i in range(nx-1):
  for j in range(ny-1):
   a=i*ny+j;b=a+ny
   fs.extend([(a,b,b+1),(a,b+1,a+1)] if (i+j)%2 else [(a,b,a+1),(b,b+1,a+1)])
 # Clip one coherent horizontal surface against actual terrain triangles.
 for tri in fs:
  poly=[vs[k] for k in tri];clipped=[]
  for k,p in enumerate(poly):
   q=poly[(k+1)%3];inside=p[2]<level
   if inside:clipped.append((p[0],p[1],level))
   if inside!=(q[2]<level):
    t=(level-p[2])/(q[2]-p[2]);clipped.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1]),level))
  if len(clipped)>=3:
   n=len(water_v);water_v.extend(clipped);water_f.extend((n,n+k,n+k+1) for k in range(1,len(clipped)-1))
 per=[i*ny for i in range(nx)]+[(nx-1)*ny+j for j in range(1,ny)]+[i*ny+ny-1 for i in reversed(range(nx-1))]+[j for j in reversed(range(1,ny-1))]
 terrain_volume('incised_continuous_alluvial_floodplain_and_unequal_bars',vs,fs,per,0,'bar')
 part('connected_shallow_water_clipped_to_inset_channels',water_v,water_f,'water')
 # Small scattered embedded gravel, never evenly repeated discs or material-only bars.
 for _ in range(78):
  x=rng.uniform(-35,35);y=rng.uniform(-70,70);d=nearest(x,y)
  if 1.4<d<3.7:
   size=rng.uniform(.28,.65);z=3.7+.13*math.sin(x*.41+y*.15)+.11*math.cos(y*.31-x*.21)
   ellipsoid('uneven_exposed_bar_gravel',(x,y,z),(size,size*rng.uniform(.55,1.1),size*.35),'gravel',n=5,k=2)
elif slug=='geode-cavity':
 import bmesh
 from collections import Counter
 # Original irregular geodesic shell: no latitude rings, repeated belts or pole fan.
 axis=Vector((.36,-.84,.40)).normalized();center=Vector((0,0,.079));cut=math.cos(math.radians(67))
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=3,radius=1);bm.verts.ensure_lookup_table();bm.verts.index_update();bm.faces.ensure_lookup_table()
 rawfaces=[[(v.index,v.co.copy()) for v in f.verts] for f in bm.faces];bm.free();units=[];faces=[];indices={}
 def addunit(p,key):
  if key not in indices:
   indices[key]=len(units);units.append(Vector(tuple(round(x,6) for x in p)))
  return indices[key]
 for raw in rawfaces:
  clipped=[]
  for i,(pi,p) in enumerate(raw):
   qi,q=raw[(i+1)%len(raw)];ip=p.dot(axis)<=cut;iq=q.dot(axis)<=cut
   if ip:clipped.append((p,('v',pi)))
   if ip!=iq:
    t=(cut-p.dot(axis))/((q-p).dot(axis));clipped.append((p.lerp(q,t),('e',min(pi,qi),max(pi,qi))))
  if len(clipped)>=3:
   ids=[addunit(p,key) for p,key in clipped]
   faces.extend((ids[0],ids[i],ids[i+1]) for i in range(1,len(ids)-1))
 edges=Counter(tuple(sorted((f[i],f[(i+1)%3]))) for f in faces for i in range(3));rimedges=[e for e,n in edges.items() if n==1]
 def irregular(p):return 1+.043*math.sin(p.x*7+p.y*3+p.z*2)+.031*math.cos(p.y*9-p.z*5)+.018*math.sin(p.z*13+p.x*8)
 def point(p,radius):
  p=Vector(p);r=radius*irregular(p);return tuple(center+Vector((p.x*r*1.02,p.y*r*.96,p.z*r)))
 outer=[point(p,.078) for p in units];middle=[point(p,.070) for p in units];inner=[point(p,.057) for p in units]
 # One integrated closed shell with shared boundaries and real material regions.
 n=len(units);rimids=sorted({i for e in rimedges for i in e});midlookup={i:2*n+k for k,i in enumerate(rimids)}
 shellvs=outer+inner+[middle[i] for i in rimids]
 shellfs=list(faces)+[tuple(n+i for i in reversed(f)) for f in faces];mats=[0]*len(faces)+[1]*len(faces)
 for aa,bb in rimedges:
  shellfs.extend([(aa,bb,midlookup[bb],midlookup[aa]),(midlookup[aa],midlookup[bb],n+bb,n+aa)]);mats.extend([2,1])
 closed=Counter(tuple(sorted((f[i],f[(i+1)%len(f)]))) for f in shellfs for i in range(len(f)))
 assert all(count==2 for count in closed.values()),('nonclosed-shell',Counter(closed.values()))
 shell=mesh_object('integrated_enclosing_rind_layered_cut_rim_and_hollow_liner',shellvs,shellfs,[m['rind'],m['chalcedony'],m['rinddark']],col)
 for poly,mi in zip(shell.data.polygons,mats):poly.material_index=mi
 # Inward small quartz, nonperiodic positions and unequal six-sided prism habits.
 accepted=[];k=0;attempt=0
 while k<350 and attempt<12000:
  attempt+=1;d=Vector((rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(-1,1)))
  if d.length<.1 or d.length>1:continue
  d.normalize()
  if d.dot(axis)>cut-.025:continue
  p=Vector(point(d,.057));radius=rng.uniform(.0028,.0045)
  if any((p-q).length<.0049 for q in accepted):continue
  accepted.append(p);direction=(center-p).normalized();q=direction.cross(Vector((0,0,1)))
  if q.length<.1:q=direction.cross(Vector((1,0,0)))
  q.normalize();r=direction.cross(q).normalized();length=rng.uniform(.0047,.0090)
  rings=[]
  for offset,rr in [(-.0015,radius),(length*.55,radius*.84)]:
   rings.append([tuple(p+direction*offset+rr*(q*math.cos(i*math.tau/6)+r*math.sin(i*math.tau/6))) for i in range(6)])
  verts=rings[0]+rings[1]+[tuple(p+direction*length)];ff=[tuple(reversed(range(6)))]+[(i,(i+1)%6,6+(i+1)%6,6+i) for i in range(6)]+[(6+i,6+(i+1)%6,12) for i in range(6)]
  part('small_unequal_inward_quartz_lining',verts,ff,'quartz' if k%5 else 'quartzshade');k+=1
 assert k==350,('quartz_count',k)

for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
