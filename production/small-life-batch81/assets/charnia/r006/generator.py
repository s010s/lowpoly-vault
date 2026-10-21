# SPDX-License-Identifier: MIT
"""Charnia C81-01 repair r006; original r001 scope and r006 repair freeze precede this generator."""
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
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(matfn(sum(vs[k][0] for k in f)/3,sum(vs[k][1] for k in f)/3,sum(vs[k][2] for k in f)/3,i,j))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];base=len(vs)
 for v in boundary:vs.append((vs[v][0],vs[v][1],0))
 for i,v in enumerate(boundary):q=(i+1)%len(boundary);fs.append((v,base+i,base+q,boundary[q]));ms.append(list(m)[-1])
 center=len(vs);vs.append((0,0,0))
 for i in range(len(boundary)):fs.append((center,base+(i+1)%len(boundary),base+i));ms.append(list(m)[-1])
 return multi(name,vs,fs,ms)

def charnia():
 P=cfg['repair_parameters'];N=P['primary_units_per_side'];ny=N*P['subdivisions_per_primary'];nh=P['lateral_frond_intervals_per_half'];nb=P['lateral_blank_intervals_per_side']
 ts=[-.025/.21,-.01875/.21,-.0125/.21,-.00625/.21]+[j/ny for j in range(ny+1)]+[1+.00625/.21,1+.0125/.21,1+.01875/.21,1+.025/.21]
 ss=[-(1+i/nb) for i in range(nb,0,-1)]+[i/nh for i in range(-nh,nh+1)]+[1+i/nb for i in range(1,nb+1)]
 vs=[];fs=[];ms=[]
 for t in ts:
  tc=max(0,min(1,t));yb=-.105+.21*t;v=(yb+.13)/.26
  axis=.0035*math.sin(5*tc)*math.sin(math.pi*tc)
  w=max(.0008,.029*(1-tc)**.64*min(1,tc/.10)**.35)
  edge=.06*(1-.16*abs(2*v-1)**5+.02*math.sin(12*v))
  for si,sn in enumerate(ss):
   sign=1 if sn>=0 else -1;s=abs(sn)
   if s<=1:
    x=axis+sign*w*s
    # Branch-aligned rows, concentrating topology inside the identifying impression.
    y=yb+P['branch_aligned_longitudinal_bow_m']*(s-.30*s*s)*math.sin(math.pi*tc)
   else:
    f=s-1;x=(axis+sign*w)*(1-f)+sign*edge*f
    y=yb+P['branch_aligned_longitudinal_bow_m']*.70*math.sin(math.pi*tc)*(1-f)-yb*.07*f**5
   # Outside the frond only, recover evenly sampled original rounded end outlines.
   end_blend=min(1,max(0,-t,t-1)/(.025/.21))
   if end_blend:
    uniform=2*si/(len(ss)-1)-1
    x=x*(1-end_blend)+edge*uniform*end_blend
    y=y*(1-end_blend)+yb*(1-.07*abs(uniform)**5)*end_blend
   z=.011+.00012*math.sin(111*x+57*y)
   if 0<t<1 and s<1:
    taper=max(0,1-s*s)**.33*min(1,t/.03,(1-t)/.035)
    z-=P['baseline_impression_depth_m']*taper
    phase=N*t-(.5 if sign>0 else 0);f=phase%1
    boundary=math.exp(-(math.sin(math.pi*phase)/.29)**2)
    start=min(1,s/.08)
    z-=P['primary_groove_depth_m']*boundary*taper*start
    # Three subordinate, gently curved furled divisions terminate inside each parent unit.
    # Unlike a crosswise oscillation, their trajectories are expressed in parent-unit coordinates.
    secondary=0.0
    for center in P['nested_division_centers']:
     curve=center+.10*(f-.5)+.025*math.sin(math.pi*f)
     secondary=max(secondary,math.exp(-((s-curve)/P['nested_division_halfwidth'])**2))
    ends=max(0,math.sin(math.pi*max(0,min(1,(f-.08)/.84))))**.65 if .08<f<.92 else 0
    z-=P['secondary_groove_depth_m']*secondary*ends*taper*start
   vs.append((x,y,z))
 nx=len(ss)-1;nr=len(ts)-1
 for j in range(nr):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in [(a,b,d),(a,d,c)]:
    fs.append(f);ms.append('impression' if sum(vs[k][2] for k in f)/3<.0099 else 'sandstone')
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,nr+1)]+[nr*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(nr-1,0,-1)];base=len(vs)
 for i in boundary:vs.append((vs[i][0],vs[i][1],0))
 for j,i in enumerate(boundary):k=(j+1)%len(boundary);fs.append((i,base+j,base+k,boundary[k]));ms.append('edge')
 center=len(vs);vs.append((0,0,0))
 for j in range(len(boundary)):fs.append((center,base+(j+1)%len(boundary),base+j));ms.append('edge')
 o=multi('Charnia_masoni_fossil_impression_BGS_GSM105873_informed_not_facsimile',vs,fs,ms)
 o['scope']='Shallow fossil impression only. Continuous alternating primary units with nested subordinate divisions. No living fern, stalk, holdfast, reconstructed underside or holotype equivalence.'
 o['topology']='One closed shared-vertex heightfield. Dense branch-aligned frond grid; sparse surrounding slab. No separate overlay skins.'
charnia()

ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
