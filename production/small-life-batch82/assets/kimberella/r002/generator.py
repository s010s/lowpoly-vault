# SPDX-License-Identifier: MIT
"""Original batch82 geometry, authored after immutable premodel design freeze."""
import bpy,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 return o

def grid(name,nx,ny,coords,matfn):
 vs=[];fs=[];ms=[]
 for j in range(ny+1):
  for i in range(nx+1):vs.append(coords(i/nx,j/ny,i,j))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   faces=[(a,b,d),(a,d,c)] if (i+j)%2==0 else [(a,b,c),(b,d,c)]
   for f in faces:fs.append(f);ms.append(matfn(sum(vs[k][0] for k in f)/3,sum(vs[k][1] for k in f)/3,sum(vs[k][2] for k in f)/3,i,j))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];base=len(vs)
 for v in boundary:vs.append((vs[v][0],vs[v][1],0))
 for i,v in enumerate(boundary):q=(i+1)%len(boundary);fs.append((v,base+i,base+q,boundary[q]));ms.append(list(m)[-1])
 center=len(vs);vs.append((0,0,0))
 for i in range(len(boundary)):fs.append((center,base+(i+1)%len(boundary),base+i));ms.append(list(m)[-1])
 return multi(name,vs,fs,ms)

def kimberella():
 def p(u,v,i,j):
  x=(u-.5)*.065;y=(v-.5)*.100
  x*=1-.15*abs(2*v-1)**5+.028*math.sin(v*13);y*=1-.10*abs(2*u-1)**5+.012*math.cos(u*15)
  z=.0060+.00010*math.sin(x*480+y*290)+.00007*math.cos(x*260-y*430)
  t=(y+.035)/.070
  if 0<t<1:
   # Broad rounded front and narrower truncated rear; central depression and lateral frill only.
   width=.0180*(math.sqrt(max(0,1-((t-.46)/.46)**2)) if t<.46 else 1-.30*((t-.46)/.54)**1.2)
   xn=abs(x)/max(width,1e-10)
   if xn<1:
    edge=min(1,(1-xn)/.10);ends=min(1,t/.055,(1-t)/.040);z-=.00145*edge*ends
    # Smooth central fossil region; fine transverse marginal grooves confined to border.
    frill=math.exp(-((xn-.82)/.13)**4)
    phase=t*32+.14*math.sin(t*17)+(0.12 if x>0 else 0)
    z-=.00062*frill*(.25+.75*math.exp(-(math.sin(math.pi*phase)/.45)**2))*ends
    z-=.00015*math.exp(-((xn-.62)/.055)**2)*ends
    z+=.00012*math.sin(t*6)*math.exp(-(x/.008)**2)*ends
  return x,y,z
 def mat(x,y,z,i,j):return 'impression' if z<.0055 else 'sandstone'
 o=grid('P49391_informed_Kimberella_negative_external_mould_with_marginal_frill_in_sandstone',64,92,p,mat);o['scope']='Fossil-specimen negative impression; not living mollusc reconstruction. Original simplified P49391-informed study.'

def badlands():
 # Explicit unequal dendritic channel graph: tributaries join a common main collector and secondary cuts join tributaries.
 trunk=[(-7,-155),(-9,-97),(5,-30),(-4,42),(10,100),(1,157)]
 branches=[([(-9,-97),(-49,-54),(-101,-35),(-135,-3)],10), ([(5,-30),(-35,11),(-80,38),(-123,73)],9), ([(-4,42),(-44,68),(-66,105),(-112,147)],8), ([(10,100),(-20,125),(-40,157)],7), ([(-9,-97),(33,-76),(80,-47),(128,-24)],11), ([(5,-30),(45,4),(98,29),(135,68)],9), ([(-4,42),(36,67),(65,108),(111,151)],8)]
 secondary=[([(-49,-54),(-69,-12),(-63,12)],5),([(-80,38),(-112,29),(-137,43)],5),([(-44,68),(-25,98),(-27,121)],4),([(80,-47),(103,-84),(132,-104)],5), ([(45,4),(63,-19),(70,-38)],4), ([(65,108),(97,88),(132,91)],5)]
 def distance(x,y,pts):
  best=1e9
  for (ax,ay),(bx,by) in zip(pts,pts[1:]):
   dx=bx-ax;dy=by-ay;t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy)));best=min(best,math.hypot(x-ax-t*dx,y-ay-t*dy))
  return best
 def p(u,v,i,j):
  x=(u-.5)*260;y=(v-.5)*300;x*=1-.09*abs(2*v-1)**5+.025*math.sin(v*14);y*=1-.05*abs(2*u-1)**5
  # Height above downstream floor rises away from each incised channel, preserving connected divides.
  d=distance(x,y,trunk)/13
  for pts,w in branches+secondary:d=min(d,distance(x,y,pts)/w)
  relief=38*(1-math.exp(-d**1.12))
  slope=7+v*30;var=1+.12*math.sin(x*.049+y*.037)+.07*math.cos(x*.09-y*.07)
  z=slope+relief*var+1.1*math.sin(x*.14+y*.06)*min(1,d)
  return x,y,z
 def mat(x,y,z,i,j):
  rel=z-(7+(y/300+.5)*30)
  return 'gully' if rel<6 else 'ridge' if rel>29 else 'sediment'
 o=grid('connected_branching_erosional_gullies_and_narrow_badlands_ridge_divides',76,76,p,mat);o['geomorphology']='Original dendritic incisions with converging tributaries and connected divides, not isolated cones or checkerboard.'

def ring_surface(name,n,rings,point,matfn,topz):
 vs=[];fs=[];ms=[]
 for j,(r,z) in enumerate(rings):
  for i in range(n):vs.append(point(r,z,math.tau*i/n,j))
 for j in range(len(rings)-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(matfn(j,i))
 top=len(vs);vs.append((0,0,topz));bot=len(vs);vs.append((0,0,0))
 for i in range(n):
  q=(i+1)%n;fs.append((top,(len(rings)-1)*n+i,(len(rings)-1)*n+q));ms.append(matfn(len(rings)-1,i));fs.append((bot,q,i));ms.append(list(m)[-1])
 return multi(name,vs,fs,ms)

def playa():
 rings=[(1,7),(.96,12),(.90,15),(.83,10),(.74,4.6),(.64,3),(.48,3),(.28,3),(.10,3)]
 def p(r,z,t,j):
  shape=1+.035*math.sin(3*t+.8)+.023*math.sin(7*t)
  # Broad planar floor, low continuous irregular rim, no drainage breach.
  h=(1.8*math.sin(3*t+1)+1.1*math.cos(5*t))*(1 if j<4 else .13 if j==4 else 0)
  return 300*r*shape*math.cos(t),240*r*shape*math.sin(t),z+h
 def mat(j,i):return 'rim' if j<3 else 'margin' if j<5 else 'floor'
 o=ring_surface('closed_dry_playa_basin_broad_flat_floor_low_irregular_enclosing_margin',128,rings,p,mat,3);o['geomorphology']='Generic dry-state closed basin, no open river outlet, nearly flat central floor. Rim intentionally subtle, not crater.'

def stratovolcano():
 # Radius declines rapidly with height near top: concave main profile and small summit crater.
 rings=[(1,8),(.94,110),(.81,300),(.66,560),(.51,920),(.38,1310),(.27,1670),(.17,2000),(.093,2230),(.061,2220),(.043,2080),(.018,2060)]
 def p(r,z,t,j):
  shape=1+.045*math.sin(3*t+.7)+.023*math.sin(7*t-1)
  # Integrated unequal flank ridges, phase varies radially to avoid a rigid repeated wedge fan.
  cut=(.5+.5*math.cos(11*t+.4*math.sin(3*t)+j*.13))**2
  cut2=(.5+.5*math.cos(19*t+.8*math.sin(2*t)-j*.1))**4
  relief=(.025*cut+.012*cut2)*math.sin(math.pi*min(1,j/9)) if j<9 else 0
  rr=r*shape+relief
  zz=z+(12*math.sin(4*t+.6)+7*math.cos(9*t))*(.7 if j>=8 else 1)
  return 3000*rr*math.cos(t),2700*rr*math.sin(t),zz
 def mat(j,i):
  t=math.tau*i/144
  return 'gully' if j>=9 or math.sin(t*11+j*.11)>.72 else 'weathered' if math.sin(t*3-j*.2)>.5 else 'rock'
 o=ring_surface('steep_concave_composite_volcano_integrated_radial_ridges_and_small_summit_vent',144,rings,p,mat,2060);o['geomorphology']='Generic steep composite volcano, broad concave lower skirt, small summit vent. No uniform strata, eruption or named-site reproduction.'
{'kimberella':kimberella,'badlands-ridge-network':badlands,'playa-basin':playa,'stratovolcano':stratovolcano}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
