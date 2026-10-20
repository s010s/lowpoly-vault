# SPDX-License-Identifier: MIT
"""Original batch73 r002 implementation repairs authored after15:07:20Z repair freezes; r001 retained."""
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
    v=abs(y)/width;best=-1.;bestk=0;bestlocal=0
    # Unequal compact lobate primary units, each with its OWN branching phase.
    for k in range(-13,14):
     root=k*.0096+.00035*math.sin(k*1.7);bend=.0038*math.sin(v*1.8)*(-1 if k>0 else 1)+.0004*math.sin(k*2.1)*v
     half=.0047*(1-.46*v*v)*(1+.06*math.sin(k*1.41));local=(x-root-bend)/half
     shape=max(0,1-local*local)**.65
     if shape>best:best=shape;bestk=k;bestlocal=local
    primary=max(0,best);k=bestk;local=bestlocal
    phase=v*(5.4+.63*math.sin(k*1.37))+.23*local+.08*math.sin(v*10+k)
    secondary=max(0,math.sin(math.pi*(phase%1)))**.8
    tertiary=.82+.18*max(0,math.sin(phase*math.pi*3+local*1.3))
    edge=min(1,(1-v)*15);z+=edge*(.0016*primary+.0010*primary*secondary*tertiary-.0008*(1-primary))
    if abs(y)<.0012:z=.0091+.00013*math.cos(x*100)
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
   x=-6+12*i/nx;xx=x+(.19*math.sin(y*1.7)+.10*math.cos(y*3.1))*abs(x/6)**8;yy=y*(.94+.04*math.sin(x*.58)+.02*math.cos(x*1.33))
   z=1.05+.075*math.sin(x*.43)+.035*math.cos(y*.9+x*.14)+.012*math.sin(x*2.1+y*3.1)
   z-=.10*math.exp(-((x+1.2-.24*y)/.11)**2)
   z-=.08*max(0,(abs(y)-3.5)/.5)
   for k,(c,w,d) in enumerate(grooves):
    drift=.028*math.sin(x*.55+k*.19);width=w*(1+.22*math.sin(x*.44+k));dist=abs((y-c-drift)/width)
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
 nx=38;ny=16;vs=[];fs=[];ms=[];tags=[]
 for j in range(ny+1):
  for i in range(nx+1):
   x=-2+4*i/nx;end=max(0,1-(x/1.43)**2);w=.035+.23*end**.48;wl=w*(1+.23*math.sin(x*4+.7));wr=w*(1+.17*math.sin(x*5-1))
   outer=1.29+.08*math.sin(x*3.4)+.04*math.sin(x*8);center=.075*math.sin(x*2.8)+.035*math.sin(x*7)
   ys=[-outer,-1,-.68,-wl-.18,-wl-.065,-wl,-wl*.91,-wl*.55,0,wr*.55,wr*.91,wr,wr+.065,wr+.18,.68,1,outer]
   y=ys[j]+center;xx=x+(.10*math.sin(y*3.9)+.055*math.cos(y*8))*abs(x/2)**8
   z=.43+.037*math.sin(x*3.7+y*2)+.025*math.sin(x*8-y*5)+.015*math.cos(x*11+y*9)
   active=end>0
   if j in [7,8,9]:z=.075+.025*math.sin(x*4+y*5) if active else z-.045
   elif j in [6,10]:z=.19+.035*math.sin(x*7+j) if active else z-.055
   elif j in [5,11]:z-=.055 if active else .09
   crust=active and j in [3,4,5,11,12,13] and ((j<8 and math.sin(x*4+.4)>-.35) or (j>8 and math.sin(x*4-1)>.0))
   if crust:z+=.035+.035*(.5+.5*math.sin(i*2.2+j*1.7))
   # A branching ground crack extends diagonally off the crooked terminal slit.
   crack=abs(y-(.50+.65*(x-.6)))
   if x>.55 and j>10:z-=.085*math.exp(-(crack/.055)**2)
   vs.append((xx,y,z));tags.append('interior' if active and 6<=j<=10 else 'crust' if crust else 'rock')
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in ([(a,c,d),(a,d,b)] if (i+j)%2 else [(a,c,b),(b,c,d)]):
    fs.append(f);ncr=sum(tags[k]=='crust' for k in f);ni=sum(tags[k]=='interior' for k in f);mat='interior' if ni>=2 else ('ochre' if (i+j)%7==1 else 'crust') if ncr>=2 else 'rock';ms.append(mat)
 o=finish_grid('single_fractured_terrain_with_crooked_deep_fissure_and_rough_interrupted_crust',vs,fs,ms,nx,ny,'rock');o['scope']='Static generic mineral-encrusted vent, no chemistry/temperature claim'

def bif():
 n=44;units=32;th=[rng.uniform(.7,1.38) for _ in range(units)];total=sum(th);levels=[0]
 for d in th:levels.append(levels[-1]+d/total*.65)
 vs=[];fs=[];ms=[];records=[]
 # Full closed single surface; unequal real ribs are part of same mesh, not overlapping layered boxes.
 for j in range(units):
  lo,hi=levels[j:j+2]
  for q,fraction in enumerate([0,.23,.48,.74]):
   z0=lo+(hi-lo)*fraction;h=z0/.65;rib=[-.002,.005,.001,-.003][q]*(.65+.35*math.sin(j*1.9)**2);records.append((j,q))
   for i in range(n):
    t=i*math.tau/n;shape=1+.05*math.sin(t*5+.4)+.025*math.cos(t*9-1)
    # Superellipse broad broken faces, natural taper across height.
    xx=math.copysign(abs(math.cos(t))**.57,math.cos(t));yy=math.copysign(abs(math.sin(t))**.57,math.sin(t));taper=(.70+.31*math.sin(math.pi*h))*(1-.66*max(0,(h-.66)/.34)**1.15)
    erosion=.007*math.sin(t*5+j*.43)+.004*math.sin(t*11-j*.27)
    rib*=.7+.3*math.sin(t*3+j*.31)**2
    notch=.020*math.exp(-((t-2.8)/.17)**2)*math.exp(-((h-.48)/.20)**2)
    x=(.4*taper+rib+erosion-notch)*xx*shape;y=(.2*taper+rib*.75+erosion*.6-notch*.6)*yy*shape
    x+=.010*math.sin(j*.49+t*4)*math.sin(math.pi*h)**2
    y+=.005*math.sin(j*.37+t*6)*math.sin(math.pi*h)**2
    fold=.041*math.sin(x*7+.6)+.018*math.sin(x*13-y*3);z=z0+fold*math.sin(math.pi*h)+.022*math.sin(t*3+1)*h**5+.0022*math.sin(t*7+j*.37)*math.sin(math.pi*h)
    vs.append((x,y,z))
 records.append((units-1,4))
 for i in range(n):
  t=i*math.tau/n;shape=1+.05*math.sin(t*5+.4)+.025*math.cos(t*9-1);xx=math.copysign(abs(math.cos(t))**.57,math.cos(t));yy=math.copysign(abs(math.sin(t))**.57,math.sin(t));vs.append((.4*.238*xx*shape,.2*.238*yy*shape,.65+.022*math.sin(t*3+1)))
 for j in range(len(records)-1):
  unit,q=records[j];mat='iron' if q in [0,1] else 'silica'
  for i in range(n):
   k=(i+1)%n;a=j*n+i;b=j*n+k;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 fs.append(tuple(range(n-1,-1,-1)));ms.append('break');o=(len(records)-1)*n;center=len(vs);vs.append((.012,-.008,.665))
 for i in range(n):fs.append((o+i,o+(i+1)%n,center));ms.append('break')
 o=multi('one_solid_bif_specimen_with_unequal_folded_fine_laminae_and_eroded_ribs',vs,fs,ms);o['lamination']='32 unequal units,64 alternating laminae; actual rib relief, not annual cadence';o['scope']='Generic rock specimen, no age/locality/sole mechanism asserted'
{'fractofusus':fractofusus,'striated-bedrock':striated,'fumarole-vent':fumarole,'banded-iron-formation':bif}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
