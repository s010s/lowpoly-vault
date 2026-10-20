# SPDX-License-Identifier: MIT
"""Original r002 geometry repair authored after15:32:39Z repair freezes; r001 retained."""
import bpy,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 return o

def gridclose(name,vs,fs,ms,nx,ny,mat):
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];b=len(vs);vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],b+q,b+i));ms.append(mat)
 fs.append(tuple(b+i for i in range(len(boundary)-1,-1,-1)));ms.append(mat);return multi(name,vs,fs,ms)

def parvancorina():
 nx,ny=66,70;vs=[];fs=[];ms=[];inside=[];ridge=[]
 for j in range(ny+1):
  y=-.04+.08*j/ny
  for i in range(nx+1):
   x=-.035+.07*i/nx;u=(y+.029)/.058
   # Broad rounded anchor end at negative Y, tapering opposite end.
   width=.024*(math.sin(math.pi*max(0,min(1,u)))**.52)*(1.20-.49*u) if 0<u<1 else 0
   f=width>0 and abs(x)<width;z=.003+.00013*math.sin(x*210+y*137);r=False
   if f:
    edge=min(1,(width-abs(x))/.0016);z+=.00035*edge+.00018*(1-abs(x)/width)
    ybar=-.0125-.006*(abs(x)/.023)**1.5;dbar=abs(y-ybar);bar=.00125*max(0,1-dbar/.0025)*min(1,max(0,(.0235-abs(x))/.003))
    stem=.00110*max(0,1-abs(x)/.0022)*min(1,max(0,(y+.014)/.003))*min(1,max(0,(.025-y)/.006))
    rim=.00035*math.exp(-((abs(x)-width+.0007)/.0006)**2);z+=edge*max(bar,stem)+rim;r=max(bar,stem)>.0004
   xx=x*(.98+.02*math.sin(y*61)+.012*math.sin(y*193));yy=y*(.98+.02*math.cos(x*101));vs.append((xx,yy,z));inside.append(f);ridge.append(r)
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in [(a,c,d),(a,d,b)]:fs.append(f);ms.append('ridge' if sum(ridge[k] for k in f)>1 else 'cast' if sum(inside[k] for k in f)>1 else 'matrix')
 o=gridclose('one_shallow_shield_fossil_positive_cast_with_integral_anchor_T_ridge',vs,fs,ms,nx,ny,'matrix');o['scope']='Fossil-form positive cast, not living arthropod reconstruction';o['uncertainty']='Affinity, A-P orientation, mobility, feeding and minor ridge nature uncertain'

def horn():
 n=64;rs=[1,.91,.78,.65,.51,.38,.25,.13,.055];vs=[];fs=[];ms=[]
 for j,r in enumerate(rs):
  for i in range(n):
   t=i*math.tau/n;edge=1+.045*math.sin(t*7+.4)+.025*math.cos(t*11);den=abs(math.cos(t))+abs(math.sin(t));x=15*r*math.cos(t)/den*edge;y=14*r*math.sin(t)/den*edge
   # Four short summit ridges, four physically concave cirque-facing hollows.
   z=.65+24.35*(1-r)-3.8*math.sin(2*t+.23)**2*math.sin(math.pi*r)**1.25
   z=max(.45,z);z+=.28*math.sin(t*9+j*.4)*math.sin(math.pi*r)
   vs.append((x,y,z))
 for j in range(len(rs)-1):
  for i in range(n):q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n
  # faces retain continuous shared vertices, no cliff skins.
  for i in range(n):
   q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('talus' if j<2 else 'face' if math.sin((i+.5)*math.tau/n*2+.23)**2>.55 else 'rock')
 apex=len(vs);vs.append((.12,-.09,25))
 for i in range(n):fs.append(((len(rs)-1)*n+i,(len(rs)-1)*n+(i+1)%n,apex));ms.append('rock')
 b=len(vs);vs.extend([(v[0],v[1],0) for v in vs[:n]])
 for i in range(n):q=(i+1)%n;fs.append((i,b+i,b+q,q));ms.append('rock')
 fs.append(tuple(b+i for i in range(n-1,-1,-1)));ms.append('rock');o=multi('compact_four_face_glacial_horn_with_convergent_ridges_and_cirque_hollows',vs,fs,ms);o['scope']='Generic pyramidal horn, no named site or glacial date'

def fissure():
 nx=100;cross=[-2.75,-2.25,-1.65,-1.2,-1,-.78,-.45,0,.45,.78,1,1.2,1.65,2.25,2.75];ny=len(cross)-1;vs=[];fs=[];ms=[]
 for j,v in enumerate(cross):
  for i in range(nx+1):
   x=-10+20*i/nx;end=max(.08,math.sin(math.pi*i/nx)**.6);vent=sum(a*math.exp(-((x-c)/w)**2) for c,w,a in [(-6.6,.9,.50),(-2.3,1.05,.64),(2.2,.78,.45),(6.3,1.12,.58)])
   width=(.24+vent)*end;cy=.15*math.sin(x*.69)+.06*math.sin(x*1.61);av=abs(v)
   if av<=1.2:
    y=cy+v*width
    if av<=.45:z=.11+.025*math.cos(x*1.9)
    elif av<=.78:z=.18+vent*.15+.07*math.sin(x*3+j)*end
    elif av<=1:z=.59+vent*.85+.08*math.sin(x*2.7+j)*end
    else:z=.55+vent*.67+.04*math.cos(x*3.3+j)
   else:
    frac=(av-1.2)/(2.75-1.2);outer=2.75*(1+.055*math.sin(x*1.7+j*.8)+.025*math.cos(x*3.1));y=cy*(1-frac)+(1 if v>0 else -1)*(1.2*width+(outer-1.2*width)*frac);z=.48+.09*math.sin(x*.81+j*1.3)+vent*.35*(1-frac)
   vs.append((x+.06*math.sin(j*1.8)*abs(x/10)**6,y,z))
 for j in range(ny):
  mid=(abs(cross[j])+abs(cross[j+1]))/2
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1;mat='interior' if mid<.46 else 'wall' if mid<.91 else 'spatter' if mid<1.45 else 'basalt'
   for f in [(a,c,d),(a,d,b)]:fs.append(f);ms.append(mat)
 o=gridclose('one_open_elongated_crack_with_four_linked_low_spatter_vent_lips',vs,fs,ms,nx,ny,'basalt');o['scope']='Static generic eruptive fissure, no active flow or temperature claim'

def gneiss():
 n=72;units=8;vs=[];fs=[];ms=[];records=[];th=[.7,1.12,.82,1.23,.77,1.04,.92,1.16];levels=[0]
 for t in th:levels.append(levels[-1]+t/sum(th)*2.2)
 for j in range(units):
  lo,hi=levels[j:j+2]
  for q,f in enumerate([0,.22,.5,.78]):
   h=(lo+(hi-lo)*f)/2.2;records.append((j,q))
   for i in range(n):
    t=i*math.tau/n;cx=math.copysign(abs(math.cos(t))**.42,math.cos(t));cy=math.copysign(abs(math.sin(t))**.50,math.sin(t));rough=.045*math.sin(t*17+j*1.7+q*.8)+.023*math.sin(t*29-j*.8);rib=[-.018,.04,.025,-.015][q]*(1 if j%2==0 else .6);shape=.91+.09*math.sin(math.pi*h)-.04*h
    x=(1.7*shape+rib+rough)*cx*(1+.045*math.sin(t*5+.3));y=(.8*shape+rib*.8+rough*.7)*cy
    fold=.37*math.sin(x*1.85+.35+y*.22)+.12*math.sin(x*3.15-.5);z=2.2*h+fold*math.sin(math.pi*h)**.65+.021*math.sin(t*13+j+q*.7)*math.sin(math.pi*h)
    vs.append((x,y,z))
 records.append((units-1,4))
 for i in range(n):
  t=i*math.tau/n;cx=math.copysign(abs(math.cos(t))**.42,math.cos(t));cy=math.copysign(abs(math.sin(t))**.50,math.sin(t));vs.append((1.7*.87*cx*(1+.045*math.sin(t*5+.3)),.8*.87*cy,2.2+.045*math.sin(t*7+.6)))
 for j in range(len(records)-1):
  unit,q=records[j]
  for i in range(n):
   k=(i+1)%n;a=j*n+i;b=j*n+k;c=a+n;d=b+n;mat='felsic' if unit%2==0 else 'mafic'
   if unit%2==0 and (i*7+j*11)%19<3:mat='feldspar'
   if unit%2==1 and (i*11+j*7)%23<2:mat='matrix'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 fs.append(tuple(range(n-1,-1,-1)));ms.append('matrix')
 # Integrated rough broken top: triangulated concentric shared-vertex rings, original mineral regions continue across fracture surface.
 last=(len(records)-1)*n
 for r in [.82,.61,.39,.18]:
  start=len(vs)
  for i in range(n):
   v=vs[(len(records)-1)*n+i];x=v[0]*r;y=v[1]*r;t=i*math.tau/n;z=2.2-.16*(1-r)+.08*math.sin(x*3.2+y*2.1)*math.sin(math.pi*r)+.025*math.sin(t*11+r*14);vs.append((x,y,z))
  for i in range(n):
   q=(i+1)%n
   for f in [(last+i,last+q,start+q),(last+i,start+q,start+i)]:
    fs.append(f);cx=sum(vs[k][0] for k in f)/3;cy=sum(vs[k][1] for k in f)/3;cz=sum(vs[k][2] for k in f)/3;phase=cz-.37*math.sin(cx*1.85+.35+cy*.22)-.12*math.sin(cx*3.15-.5);ms.append('felsic' if int((phase+.07)/.24)%2==0 else 'mafic')
  last=start
 center=len(vs);vs.append((0,0,2.05))
 for i in range(n):fs.append((last+i,last+(i+1)%n,center));ms.append('felsic' if i%17<9 else 'mafic')
 o=multi('solid_coarse_eight_band_gneiss_with_integral_folded_ribs_and_crystalline_facets',vs,fs,ms);o['scope']='Generic coarse folded foliation, not sedimentary layers/BIF/vein';o['structure']='Eight unequal broad mineral bands with physical erosion ribs and broken banded top; no stacked shells'
{'parvancorina':parvancorina,'glacial-horn':horn,'eruptive-fissure':fissure,'banded-gneiss-outcrop':gneiss}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
