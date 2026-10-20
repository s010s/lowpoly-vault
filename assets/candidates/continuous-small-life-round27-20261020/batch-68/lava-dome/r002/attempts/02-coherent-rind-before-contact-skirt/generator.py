# SPDX-License-Identifier: MIT
"""Original batch68 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
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


# Original r002 continuous fractured extrusion, authored after immutable repair freeze.
import random
rng=random.Random(cfg['seed'])
def fractured_dome():
 # Coarse fracture regions distributed in plan across summit AND flanks, never in a latitude belt.
 seeds=[]
 while len(seeds)<72:
  p=(rng.uniform(-1,1),rng.uniform(-1,1))
  if p[0]*p[0]+p[1]*p[1]<1.03 and all(math.hypot(p[0]-x,p[1]-y)>.13 for x,y in seeds):seeds.append(p)
 outline=[]
 for i in range(48):
  a=i*math.tau/48;r=1+.035*math.sin(3*a+.4)+.022*math.sin(7*a)
  outline.append((r*math.cos(a),r*math.sin(a)))
 def clip(poly,A,B,C):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   f=A*p[0]+B*p[1]-C;g=A*q[0]+B*q[1]-C
   if f<=1e-9:out.append(p)
   if (f<0)!=(g<0):
    t=f/(f-g);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return out
 def height(x,y):
  a=math.atan2(y,x);lim=1+.035*math.sin(3*a+.4)+.022*math.sin(7*a);r=math.hypot(x,y)/lim
  return 40*math.sqrt(max(0,1-min(1,r)**3.1))*(1+.018*math.sin(x*3+y*2))
 vertices=[];faces=[];materials=[];lookup={}
 def vert(x,y,z):
  p=(round(60*x,7),round(50*y,7),round(z,7))
  if p not in lookup:lookup[p]=len(vertices);vertices.append(p)
  return lookup[p]
 for k,(x,y) in enumerate(seeds):
  poly=outline[:]
  for j,(u,v) in enumerate(seeds):
   if k!=j:poly=clip(poly,2*(u-x),2*(v-y),u*u+v*v-x*x-y*y)
  if len(poly)<3:continue
  cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly);n=len(poly)
  # A joined seam, a narrow fractured shoulder and a broad irregular inclined rock plate.
  # Every region remains physically welded into the single extrusion surface.
  lift=rng.uniform(.5,5.5);lifts=[0,lift,rng.uniform(.3,5.2)];rings=[];inner=rng.uniform(.58,.82);shoulder=rng.uniform(.88,.97);tiltx=rng.uniform(-12,12);tilty=rng.uniform(-12,12)
  for j,t in enumerate([1,shoulder,inner]):
   ring=[]
   for x,y in poly:
    xx=cx+(x-cx)*t;yy=cy+(y-cy)*t;h=height(xx,yy)
    if j==0:z=max(0,h-1.25)
    else:z=h+lifts[j]*(.72+.28*math.sin(k*1.1+x*11-y*9))+(xx-cx)*tiltx+(yy-cy)*tilty
    ring.append(vert(xx,yy,z))
   rings.append(ring)
  mat='block' if (cx*.7+cy*.2)>.06 else 'core'
  for j in range(2):
   for i in range(n):q=(i+1)%n;faces.append((rings[j][i],rings[j][q],rings[j+1][q],rings[j+1][i]));materials.append('dark' if j==0 and k%5==0 else mat)
  c=vert(cx,cy,height(cx,cy)+rng.uniform(.5,5.5))
  for i in range(n):faces.append((rings[-1][i],rings[-1][(i+1)%n],c));materials.append(mat)
 # The exterior edge closes to a shallow irregular contact skirt and solid underside.
 edges={}
 for f in faces:
  for a,b in zip(f,f[1:]+f[:1]):key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
 boundary=[e for e,n in edges.items() if n==1];base=[]
 for a,b in boundary:
  x,y,z=vertices[a];u,v,w=vertices[b];aa=vert(x/60,y/50,-.6);bb=vert(u/60,v/50,-.6);faces.append((a,b,bb,aa));materials.append('rubble');base.extend([aa,bb])
 base=sorted(set(base),key=lambda i:math.atan2(vertices[i][1]/50,vertices[i][0]/60));faces.append(tuple(base));materials.append('core')
 obj=mesh_object('single_welded_bulbous_dome_coarse_fractured_summit_and_flanks',vertices,faces,[m[k] for k in cfg['palette']],col);keys=list(cfg['palette'])
 for p,k in zip(obj.data.polygons,materials):p.material_index=keys.index(k)
fractured_dome()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
