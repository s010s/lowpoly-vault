# SPDX-License-Identifier: MIT
"""Original batch84 geological geometry, authored after the immutable design freezes."""
import bpy,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 return o

def terrain_grid(name,nx,ny,coords,matfn):
 vs=[coords(i/nx,j/ny,i,j) for j in range(ny+1) for i in range(nx+1)];fs=[];ms=[]
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   ff=[(a,b,d),(a,d,c)] if (i+j)%2==0 else [(a,b,c),(b,d,c)]
   for f in ff:fs.append(f);ms.append(matfn([vs[k] for k in f],i,j))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];base=len(vs)
 for v in boundary:vs.append((vs[v][0],vs[v][1],0))
 for i,v in enumerate(boundary):q=(i+1)%len(boundary);fs.append((v,base+i,base+q,boundary[q]));ms.append('cut')
 center=len(vs);vs.append((0,0,0))
 for i in range(len(boundary)):fs.append((center,base+(i+1)%len(boundary),base+i));ms.append('cut')
 return multi(name,vs,fs,ms)

def delta():
 # Three unequal distributary centerlines split from the same river and flare towards the sea.
 def channels(y):
  if y>=2300:return [(90*math.sin(y*.00055),170+(6000-y)*.016)]
  t=(2300-y)/8300
  return [(-2550*t-110*math.sin(t*5),180+750*t**1.2),(140*math.sin(t*4)+260*t,210+820*t**1.25),(2440*t+190*math.sin(t*3),170+650*t**1.15)]
 # Irregular tidal creeks actually join the eastern/western distributaries.
 side=[([(-1350,-2100),(-2550,-1100),(-3020,700),(-3900,1250)],220), ([(1600,-2300),(2750,-1350),(3220,280),(3960,1150)],210),([(-2550,-1100),(-3300,-1500),(-3990,-600)],170)]
 def distance(x,y,pts):
  best=1e10
  for (ax,ay),(bx,by) in zip(pts,pts[1:]):
   dx=bx-ax;dy=by-ay;t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy)));best=min(best,math.hypot(x-ax-t*dx,y-ay-t*dy))
  return best
 def p(u,v,i,j):
  x=(u-.5)*10000;y=(v-.5)*12000
  d=min(abs(x-c)/w for c,w in channels(y))
  for pts,w in side:d=min(d,distance(x,y,pts)/w)
  sea=-4800+500*math.sin(x*.0007)+350*math.cos(x*.0013)
  d=min(d,max(0,(y-sea)/210))
  # One watertight material-region heightfield. No coplanar ocean sheet beneath separate land bars.
  land=max(0,min(1,(d-.72)/.65));z=15+land*(145+12*math.sin(x*.0012+y*.001)+6*math.cos(y*.003))
  return x,y,z
 def mat(pts,i,j):
  z=sum(p[2] for p in pts)/3
  return 'water' if z<35 else 'bar' if z<150 else 'sediment'
 o=terrain_grid('tide_delta_connected_downstream_flaring_channels_and_elongate_bars',76,80,p,mat);o['scope']='Original generic tide-dominated delta; static opaque water material regions, not site DEM or simulation.'

def cave():
 n=64;ny=36;vs=[];fs=[];ms=[]
 # Unequal recessed dissolution hollows spread over the internal walls and roof.
 hollows=[(-4.1,0.05,.95,.30,.20),(-2.0,.40,.75,.35,.24),(0.2,.18,1.00,.28,.19),(2.3,.65,.85,.34,.25),(4.7,.25,.72,.30,.20),(-3.8,2.8,.82,.30,.19),(-1.1,2.5,.90,.31,.22),(1.5,2.9,1.10,.29,.23),(4.1,2.6,.85,.32,.18),(-3.2,1.4,.9,.27,.15),(.3,1.7,.8,.28,.16),(3.3,1.3,1.1,.3,.18)]
 for outer in [False,True]:
  for j in range(ny+1):
   y=-6+12*j/ny;cx=.18*math.sin(y*.38);cz=2.7+.04*math.sin(y*.7)
   for i in range(n):
    t=math.tau*i/n
    if outer:
     k=1+.025*math.sin(t*7+y*.4)+.018*math.cos(t*11-y*.7)+.035*math.sin(t*3+y*.65);x=cx+5*math.cos(t)*k;z=cz+2.7*math.sin(t)*k;z=max(.0,z)
    else:
     recess=0
     for yy,tt,sy,st,amp in hollows:
      dt=math.atan2(math.sin(t-tt),math.cos(t-tt));recess+=amp*math.exp(-((y-yy)/sy)**2-(dt/st)**2)
     k=1+.025*math.sin(t*3+y*.65)+.015*math.sin(t*7-y*.45)+recess/4
     x=cx+4.05*math.cos(t)*k;z=cz+1.72*math.sin(t)*k
     if math.sin(t)<-.52:z=.84+.055*math.sin(y*.8)+.08*(math.cos(t))**2+.025*math.cos(y*1.7+t*3)
    if not outer:
     # Additional original shallow dissolution scallops are meter-bounded radial recesses.
     pass
    # Oblique front module end plane, not a hidden-surface rendering cutaway.
    yy=y+(1-j/ny)*(.35*x+1.75)
    vs.append((x,yy,z))
 shell=(ny+1)*n
 for j in range(ny):
  for i in range(n):
   q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(tuple(reversed(f)));ms.append('interior')
   for f in [(shell+a,shell+b,shell+d),(shell+a,shell+d,shell+c)]:fs.append(f);ms.append('limestone')
 for j in [0,ny]:
  for i in range(n):
   q=(i+1)%n;a=j*n+i;b=j*n+q
   fs.append((a,b,shell+b,shell+a) if j==0 else (a,shell+a,shell+b,b));ms.append('cut')
 o=multi('enclosed_solution_tube_scalloped_interior_two_disclosed_cut_module_ends',vs,fs,ms);o['scope']='Original enclosed carbonate passage with two artificial truncated end boundaries; not natural entrance, arch or lava tube.'

def neck():
 n=112;levels=[(1,0),(.92,12),(.78,30),(.62,52),(.49,78),(.44,110),(.425,145),(.42,185),(.40,225),(.385,265),(.36,300),(.30,330),(.255,347),(.12,349)]
 vs=[];fs=[];ms=[]
 for j,(r,z) in enumerate(levels):
  for i in range(n):
   t=math.tau*i/n
   # Vertically correlated unequal cliff facets and broken shoulders, not separate overlapping pillars.
   joint=.018*math.sin(t*13+.3)+.012*math.sin(t*23-1)+.008*math.cos(t*31)
   irregular=1+.16*math.sin(t*3+.7)+.085*math.cos(t*5-1)+.025*math.sin(t*9+j*.27)
   rr=r*irregular+(joint*(.5 if j<4 else 1.0))
   if j>=7:rr*=1+.045*math.sin(t*2+j*.7)
   if j<4:rr*=1+.08*math.cos(t*2+.5)
   zz=z+(math.sin(t*3+1)*6+math.cos(t*7)*5+math.sin(t*17)*2)*(0 if j==0 else .3 if j<3 else 1)
   vs.append((270*rr*math.cos(t)+11*math.sin(j*.25),245*rr*math.sin(t),zz))
 for j in range(len(levels)-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('weathered' if math.sin(i*.18+j*.21)>.55 else 'rock')
 top=len(vs);vs.append((11*math.sin((len(levels)-1)*.25),0,365));bot=len(vs);vs.append((0,0,0))
 for i in range(n):
  q=(i+1)%n;fs.append((top,(len(levels)-1)*n+i,(len(levels)-1)*n+q));ms.append('rock');fs.append((bot,q,i));ms.append('cut')
 o=multi('eroded_solid_volcanic_conduit_neck_irregular_crown_steep_jointed_core',vs,fs,ms);o['scope']='Original generic eroded resistant solid conduit remnant; no crater, intact volcanic cone or site reconstruction.'
{'tide-dominated-delta':delta,'solution-cave-passage':cave,'volcanic-neck':neck}[slug]()
ground_asset(col,center_xy=True)
# Bake origin placement into actual mesh vertices; no hidden parent translation offsets.
root=bpy.data.objects[col['asset_root']]
for obj in col.all_objects:
 if obj.type=='MESH':
  world=obj.matrix_world.copy();obj.data.transform(world);obj.matrix_world.identity();obj.parent=None
root.location=(0,0,0);bpy.context.view_layer.update()
source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
