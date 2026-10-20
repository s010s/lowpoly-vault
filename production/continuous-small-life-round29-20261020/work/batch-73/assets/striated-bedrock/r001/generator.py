# SPDX-License-Identifier: MIT
"""Original batch73 geometry authored after all four immutable15:01:31Z freezes."""
import bpy,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,mats):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,mats):p.material_index=keys.index(k)
 return o

def finish_grid(name,vs,fs,ms,nx,ny,mat):
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];b=len(vs);vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],b+q,b+i));ms.append(mat)
 fs.append(tuple(b+i for i in range(len(boundary)-1,-1,-1)));ms.append(mat);return multi(name,vs,fs,ms)

def fractofusus():
 nx,ny=114,48;vs=[];fs=[];ms=[];foss=[]
 for j in range(ny+1):
  y=-.0575+.115*j/ny
  for i in range(nx+1):
   x=-.15+.30*i/nx;ex=abs(x/.15);ey=abs(y/.0575)
   xx=x*(.978+.022*math.cos(y*71)+.006*math.sin(y*271));yy=y*(.96+.03*math.sin(x*51)+.012*math.sin(x*127));u=(x+.133)/.266
   width=.0405*math.sin(math.pi*max(0,min(1,u)))**.71 if 0<u<1 else 0
   z=.009+.00025*math.sin(x*61+y*49)+.00012*math.cos(x*143-y*91);inside=width>0 and abs(y)<width
   if inside:
    v=abs(y)/width;ax=x+.0015*math.sin(x*35);phase=(ax+.133)/.0107+.34*v**1.3*(1 if x<0 else -1);frac=phase-math.floor(phase)
    # Compact primary modules, integrated fine side subdivisions, never freestanding fern twigs.
    primary=math.sin(math.pi*frac)**.72;secphase=v*(6.5+1.2*math.sin(x*47))+.16*math.sin(frac*math.pi);secondary=.48+.52*math.sin(math.pi*(secphase%1))**.55
    tertiary=.88+.12*math.sin(v*math.pi*29+frac*5)**2
    edge=min(1,(1-v)*12);z+=edge*(.0018*primary*secondary*tertiary-.0009*(1-primary))
    if abs(y)<.0013:z=.0085+.0002*math.cos(x*100)
   vs.append((xx,yy,z));foss.append(inside)
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in [(a,c,d),(a,d,b)]:
    fs.append(f);ms.append('fossil' if sum(foss[k] for k in f)>1 else 'matrix')
 o=finish_grid('original_shallow_fusiform_fossil_cast_with_opposed_hierarchical_modules',vs,fs,ms,nx,ny,'matrix');o['scope']='Fossil-form specimen study, not whole living reconstruction';o['uncertainty']='Living affinity, feeding and exact3D anatomy uncertain'

def striated():
 nx=28;grooves=[(-3.20,.075,.10),(-2.72,.19,.23),(-1.88,.12,.16),(-1.08,.25,.29),(-.28,.10,.12),(.54,.16,.21),(1.43,.23,.26),(2.31,.10,.15),(3.08,.15,.19)]
 ys=sorted(set([-4,-3.7,3.7,4]+[c+w*t for c,w,d in grooves for t in [-1.8,-1,-.35,0,.35,1,1.8]]));ny=len(ys)-1;vs=[];fs=[];ms=[]
 for j,y in enumerate(ys):
  for i in range(nx+1):
   x=-6+12*i/nx;xx=x+(.08*math.sin(y*2.2)+.04*math.cos(y*4.3))*abs(x/6)**8;yy=y*(.982+.018*math.sin(x*.72))
   z=1.05+.055*math.sin(x*.43)+.026*math.cos(y*.9+x*.14)
   for k,(c,w,d) in enumerate(grooves):
    drift=.028*math.sin(x*.55+k*.19);width=w*(1+.12*math.sin(x*.44+k));dist=abs((y-c-drift)/width)
    if dist<1.8:z-=d*(1-dist/1.8)**.72*(.88+.12*math.cos(x*.39+k*.4))
   # Two genuine shorter fine subsidiary scratches, subordinate to long grooves.
   for c,start,stop in [(-.62,-3.8,1.9),(1.94,-1.5,4.8)]:
    if start<x<stop:z-=.035*math.exp(-((y-c)/.055)**2)*math.sin((x-start)/(stop-start)*math.pi)
   vs.append((xx,yy,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in ([(a,c,d),(a,d,b)] if rng.random()<.5 else [(a,c,b),(b,c,d)]):fs.append(f);ms.append('bedrock')
 finish_grid('single_smoothed_bedrock_volume_with_unequal_incised_glacial_grooves',vs,fs,ms,nx,ny,'edge')

def fumarole():
 n=96;vs=[];fs=[];ms=[];rings=[]
 # Outside boundary through surface, mineral lip, recessed wall, cavity floor: one integrated manifold.
 for ring in range(8):
  rr=[]
  for i in range(n):
   t=i*math.tau/n;noise=.065*math.sin(t*7+.3)+.035*math.sin(t*13-1)+.025*math.cos(t*23)
   jag=1+noise;cx=.10*math.sin(t*2);cy=.05*math.sin(t*3+.4)
   radii=[(2.,1.4),(1.61,1.10),(1.35,.69),(1.22,.43),(1.10,.32),(1.02,.25),(.87,.20),(.70,.14)]
   rx,ry=radii[ring];x=rx*math.cos(t)*jag+cx*(1 if ring>1 else .3);y=ry*math.sin(t)*jag+cy
   # Crooked slit, unequal shoulders and two tapering end fractures rather than round basin.
   y+=.085*math.sin(x*2.7)*(ring/7)
   z=[.31,.39,.43,.49,.46,.31,.11,.075][ring]+(.045*math.sin(t*5)+.024*math.cos(t*11))*(1 if ring<6 else .2)
   if ring in [2,3,4]:
    crust=math.sin(t*3+.4)+.45*math.sin(t*8)>-.3
    if crust:z+=.055*(.5+.5*math.sin(t*19+.3))*(1 if ring==3 else .6)
   if ring<5:
    for crack in [.12,2.95,4.8]:
     da=abs((t-crack+math.pi)%math.tau-math.pi);z-=.12*math.exp(-(da/.045)**2)*(1 if ring<3 else .45)
   rr.append((x,y,z))
  rings.append(rr)
 vs=[v for r in rings for v in r]
 for j in range(len(rings)-1):
  for i in range(n):
   q=(i+1)%n;t=(i+.5)*math.tau/n;crust=math.sin(t*3+.4)+.45*math.sin(t*8)>-.3
   mat='interior' if j>=4 else ('ochre' if math.sin(t*9)>0.45 else 'crust') if j in [2,3] and crust else 'rock'
   a=j*n+i;b=j*n+q;c=(j+1)*n+i;d=(j+1)*n+q
   for f in [(a,c,d),(a,d,b)]:fs.append(f);ms.append(mat)
 center=len(vs);vs.append((.04,.015,.065))
 for i in range(n):fs.append(((len(rings)-1)*n+i,center,(len(rings)-1)*n+(i+1)%n));ms.append('interior')
 bot=len(vs);vs.extend([(p[0],p[1],0) for p in rings[0]])
 for i in range(n):q=(i+1)%n;fs.append((i,q,bot+q,bot+i));ms.append('rock')
 fs.append(tuple(bot+i for i in range(n-1,-1,-1)));ms.append('rock');o=multi('integrated_fractured_vent_with_discontinuous_relief_crust_and_recessed_fissure',vs,fs,ms);o['scope']='Static generic mineral-encrusted vent, no chemistry or temperature claim'

def bif():
 n=44;units=32;th=[rng.uniform(.7,1.38) for _ in range(units)];total=sum(th);levels=[0]
 for d in th:levels.append(levels[-1]+d/total*.65)
 vs=[];fs=[];ms=[];records=[]
 # Full closed single surface; unequal real ribs are part of same mesh, not overlapping layered boxes.
 for j in range(units):
  lo,hi=levels[j:j+2]
  for q,fraction in enumerate([0,.23,.48,.74]):
   z0=lo+(hi-lo)*fraction;h=z0/.65;rib=[-.003,.006,.001,-.004][q]*(.8+.2*math.sin(j*1.9));records.append((j,q))
   for i in range(n):
    t=i*math.tau/n;shape=1+.05*math.sin(t*5+.4)+.025*math.cos(t*9-1)
    # Superellipse broad broken faces, natural taper across height.
    xx=math.copysign(abs(math.cos(t))**.57,math.cos(t));yy=math.copysign(abs(math.sin(t))**.57,math.sin(t));taper=.91+.10*math.sin(math.pi*h)-.05*h
    x=(.4*taper+rib)*xx*shape;y=(.2*taper+rib*.75)*yy*shape
    x+=.010*math.sin(j*.49+t*4)*math.sin(math.pi*h)**2
    y+=.005*math.sin(j*.37+t*6)*math.sin(math.pi*h)**2
    fold=.041*math.sin(x*7+.6)+.018*math.sin(x*13-y*3);z=z0+fold*math.sin(math.pi*h)+.010*math.sin(t*3+1)*h**5
    vs.append((x,y,z))
 records.append((units-1,4))
 for i in range(n):
  t=i*math.tau/n;shape=1+.05*math.sin(t*5+.4)+.025*math.cos(t*9-1);xx=math.copysign(abs(math.cos(t))**.57,math.cos(t));yy=math.copysign(abs(math.sin(t))**.57,math.sin(t));vs.append((.4*.86*xx*shape,.2*.86*yy*shape,.65+.010*math.sin(t*3+1)+.018*math.sin(t*7)))
 for j in range(len(records)-1):
  unit,q=records[j];mat='iron' if q in [0,1] else 'silica'
  for i in range(n):
   k=(i+1)%n;a=j*n+i;b=j*n+k;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 fs.append(tuple(range(n-1,-1,-1)));ms.append('break');o=(len(records)-1)*n;fs.append(tuple(o+i for i in range(n)));ms.append('break');o=multi('one_solid_bif_specimen_with_unequal_folded_fine_laminae_and_eroded_ribs',vs,fs,ms);o['lamination']='32 unequal units,64 alternating laminae; actual rib relief, not annual cadence';o['scope']='Generic rock specimen, no age/locality/sole mechanism asserted'
{'fractofusus':fractofusus,'striated-bedrock':striated,'fumarole-vent':fumarole,'banded-iron-formation':bif}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
