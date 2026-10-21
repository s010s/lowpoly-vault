# SPDX-License-Identifier: MIT
"""Original batch83 geometry, authored after immutable original design freezes."""
import bpy,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 return o

def cloudina():
 n=48;collars=14;vs=[];fs=[];ms=[]
 # One continuous wall, with actual eccentric funnel steps rather than overlapping rings.
 stations=[]
 for j in range(collars):
  s=j/collars;nexts=(j+1)/collars
  stations.extend([(s,0,j),(s+.78/collars,.78,j),(nexts-.055/collars,1,j),(nexts-.005/collars,.05,j)])
 stations.append((1,0,collars))
 def center(s):return .00085*math.sin(s*2.5)-.0003*s,.00023*math.sin(s*4),.012*s
 for layer in [0,1]:
  for h,(s,flare,j) in enumerate(stations):
   cx,cy,z=center(s);base=.00105+.00042*s
   for i in range(n):
    t=math.tau*i/n;ecc=.00007*math.sin(j*1.71)*math.cos(t-.8)+.000035*math.cos(j*2.2)*math.sin(t)
    radius=base+(.00019*flare*(1+.12*math.sin(t*3+j*.4)) if layer==0 else -.000075)+ecc
    # Jagged broken rims at both ends only; all intermediate rings continuous.
    zz=z+.00010*(.5+.5*math.sin(5*t+.5))*(1-s)**8+(.00014*math.sin(4*t+.4)+.00004*math.cos(7*t))*s**8
    vs.append((cx+radius*math.cos(t),cy+radius*math.sin(t),zz))
 L=len(stations);offset=L*n
 for layer in [0,1]:
  for h in range(L-1):
   for i in range(n):
    p=layer*offset+h*n+i;q=layer*offset+h*n+(i+1)%n;f=(p,q,q+n,p+n)
    fs.append(f if layer==0 else tuple(reversed(f)));ms.append('edge' if layer==0 and h%4==1 else 'carbonate' if layer==0 else 'interior')
 for h in [0,L-1]:
  for i in range(n):
   p=h*n+i;q=h*n+(i+1)%n;f=(p,p+offset,q+offset,q);fs.append(f if h==L-1 else tuple(reversed(f)));ms.append('edge')
 o=multi('single_Cloudina_incomplete_hollow_skeletal_fragment_nested_eccentric_funnels',vs,fs,ms);o['scope']='Genus-level fossil-skeletal fragment. Both ends broken; no living animal, basal apex or life position asserted.'

def grid(name,nx,ny,coords,matfn):
 vs=[];fs=[];ms=[]
 for j in range(ny+1):
  for i in range(nx+1):vs.append(coords(i/nx,j/ny,i,j))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in ([(a,b,d),(a,d,c)] if (i+j)%2==0 else [(a,b,c),(b,d,c)]):fs.append(f);ms.append(matfn(sum(vs[k][0] for k in f)/3,sum(vs[k][1] for k in f)/3,sum(vs[k][2] for k in f)/3,i,j))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];base=len(vs)
 for v in boundary:vs.append((vs[v][0],vs[v][1],0))
 for i,v in enumerate(boundary):q=(i+1)%len(boundary);fs.append((v,base+i,base+q,boundary[q]));ms.append(list(m)[-1])
 center=len(vs);vs.append((0,0,0))
 for i in range(len(boundary)):fs.append((center,base+(i+1)%len(boundary),base+i));ms.append(list(m)[-1])
 return multi(name,vs,fs,ms)

def delta():
 def shore(x):return -220-220*math.exp(-((x-30)/680)**2)+13*math.sin(x/670)
 def channel(y):return -80+115*math.sin((y+420)/290)+35*math.sin((y+420)/115)
 def dchannel(x,y):
  d=abs(x-channel(y))/43
  if y<150:
   # A single subdued secondary distributary diverges naturally near mouth.
   second=channel(150)+.36*(150-y)
   d=min(d,abs(x-second)/23)
  return d
 def p(u,v,i,j):
  x=(u-.5)*2400;y=(v-.5)*1800;x*=1-.025*abs(2*v-1)**6;y*=1-.025*abs(2*u-1)**6
  inland=y-shore(x);h=20+23*min(1,max(0,inland/70))+8*max(0,y/900)
  # Low arcuate beach ridges remain integrated, subordinate to shore shape.
  h+=2.2*math.exp(-((inland-125)/25)**2)+1.2*math.exp(-((inland-205)/32)**2)
  d=dchannel(x,y)
  if inland>0:h=min(h,20+24*min(1,max(0,(d-.62)/.70)))
  if inland<0:h=20
  return x,y,h
 def mat(x,y,z,i,j):
  inland=y-shore(x)
  return 'water' if z<22.5 else 'beach' if inland<105 or dchannel(x,y)<1.30 else 'sediment'
 o=grid('wave_reworked_smooth_arcuate_delta_coast_with_subdued_mouths_physical_channels',80,64,p,mat);o['scope']='Generic wave-dominated delta coast. Physical lowered opaque water region and river channels; no named site, crop grids or ecosystem.'

def lava():
 n=64;ny=12;vs=[];fs=[];ms=[]
 for layer in [0,1]:
  for j in range(ny+1):
   y=-8+(21 if layer==0 else 19)*j/ny
   for i in range(n):
    t=math.tau*i/n;s=math.sin(t);c=math.cos(t)
    if layer==0:
     width=16*(1+.025*math.sin(j*.72));x=width*c;z=1.5+(7.1 if s>0 else 1.5)*s
     z+=max(0,s)*(.38*math.sin(i*.81+j*1.1)+.23*math.cos(i*1.7-j*.6));z=max(.0,z)
    else:
     width=9*(1-.08*j/ny+.025*math.sin(j*.8));x=width*c;z=1.6+(4.25 if s>0 else .30)*s
     z+=.10*math.sin(i*1.6+j*.9)*max(.1,abs(s))
    vs.append((x,y,z))
 L=(ny+1)*n
 for layer in [0,1]:
  for j in range(ny):
   for i in range(n):
    a=layer*L+j*n+i;b=layer*L+j*n+(i+1)%n;f=(a,b,b+n,a+n)
    fs.append(tuple(reversed(f)) if layer==0 else f);ms.append('interior' if layer else 'weathered' if math.sin(i*.37+math.sin(j*.71)*1.8)+.7*math.cos(i*.79-j*.83)>.8 else 'basalt')
 # Front lip joins actual outer and inner wall, rear likewise. Rear aperture closes with real wall.
 for j in [0]:
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;f=(a,b,b+L,a+L);fs.append(f if j==0 else tuple(reversed(f)));ms.append('weathered' if j==0 else 'basalt')
 for layer in [0,1]:
  back=len(vs);vs.append((0,13 if layer==0 else 11,2.8))
  for i in range(n):
   f=(back,layer*L+ny*n+(i+1)%n,layer*L+ny*n+i);fs.append(f if layer==0 else tuple(reversed(f)));ms.append('basalt' if layer==0 else 'interior')
 o=multi('thick_integrated_basalt_roof_and_walls_real_low_arched_bounded_tunnel',vs,fs,ms);o['scope']='Short entrance conduit segment. Back closure is module bound, not claim cave terminates. Real hollow volume and floor, no flat black mouth.'
 # A separate approach slab touches only front boundary, not a coplanar overlapping surface.
 def p(u,v,i,j):
  x=(u-.5)*32;y=-14+6*v;z=1.25+.10*math.sin(x*1.4+y*.8)+.04*math.cos(x*.7-y*2)
  return x*(.96+.04*v),y,z
 grid('solidified_lava_floor_foreground_approach_with_integrated_low_flow_ridges',24,12,p,lambda x,y,z,i,j:'basalt' if math.sin(x*.3+y*.7)<.5 else 'weathered')

def crater():
 n=144;rings=[(1,260),(.91,260),(.81,264),(.72,276),(.64,305),(.58,355),(.54,403),(.51,389),(.47,299),(.42,225),(.36,151),(.29,89),(.21,47),(.12,35),(.04,35)];vs=[];fs=[];ms=[]
 for j,(r,z) in enumerate(rings):
  for i in range(n):
   t=math.tau*i/n;shape=1+.025*math.cos(4*t+.4)+.018*math.sin(7*t);cx=math.cos(t);sy=math.sin(t);square=max(0,1-j/3);xx=math.copysign(abs(cx)**.5,cx);yy=math.copysign(abs(sy)**.5,sy);x=1200*r*shape*(cx*(1-square)+xx*square);y=1100*r*shape*(sy*(1-square)+yy*square)
   rim=11*math.sin(5*t+.3)+7*math.cos(11*t)
   gullies=(.5+.5*math.cos(23*t+.3*math.sin(5*t)+j*.07))**4
   zz=z+(rim if 4<=j<=8 else rim*.25 if 2<=j<=10 else 0)-(9*gullies if 7<=j<=11 else 0)
   vs.append((x,y,zz))
 for j in range(len(rings)-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('plain' if j<4 else ('rim' if math.sin(i*.11)+.6*math.cos(i*.29+j*.7)>.15 else 'plain') if j<7 else ('wall' if math.sin(i*.12+j*.3)<.8 else 'floor') if j<12 else 'floor')
 center=len(vs);vs.append((0,0,35));bottom=len(vs);vs.append((0,0,0));base=len(vs)
 for i in range(n):vs.append((vs[i][0],vs[i][1],0))
 for i in range(n):
  q=(i+1)%n;fs.extend([(center,(len(rings)-1)*n+i,(len(rings)-1)*n+q),(i,base+i,base+q,q),(bottom,base+q,base+i)]);ms.extend(['floor','plain','plain'])
 o=multi('simple_impact_crater_excavated_bowl_below_plain_disrupted_raised_rim_ejecta_apron',vs,fs,ms);o['scope']='Generic terrestrial simple impact form. Shape not impact-origin proof; no central peak, exact site or eruption.'
{'cloudina':cloudina,'wave-dominated-delta':delta,'lava-tube-entrance':lava,'impact-crater':crater}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
