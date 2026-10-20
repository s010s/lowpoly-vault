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

def ring_surface(name,n,rings,point,matfn,topz):
 vs=[];fs=[];ms=[]
 for j,(r,z) in enumerate(rings):
  for i in range(n):vs.append(point(r,z,math.tau*i/n,j))
 for j in range(len(rings)-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(matfn(j,i))
 top=len(vs);vs.append((0,0,topz))
 base=len(vs)
 for i in range(n):vs.append((vs[i][0],vs[i][1],0))
 bot=len(vs);vs.append((0,0,0))
 for i in range(n):
  q=(i+1)%n;fs.append((top,(len(rings)-1)*n+i,(len(rings)-1)*n+q));ms.append(matfn(len(rings)-1,i))
  fs.append((i,base+i,base+q,q));ms.append(list(m)[-1]);fs.append((bot,base+q,base+i));ms.append(list(m)[-1])
 return multi(name,vs,fs,ms)

def stratovolcano():
 params=cfg['repair_parameters'];n=params['angular_samples']
 profile=[(1,8),(.94,110),(.81,300),(.66,560),(.51,920),(.38,1310),(.27,1670),(.17,2000),(.093,2230),(.061,2220),(.043,2080),(.018,2060)]
 def sample(r):
  for j in range(8):
   ra,za=profile[j];rb,zb=profile[j+1]
   if rb<=r<=ra:
    f=(ra-r)/(ra-rb);return za+(zb-za)*f,j+f
  return profile[8][1],8
 radii=sorted(set([p[0] for p in profile[:9]]+[.17+i*(.94-.17)/(params['flank_radial_samples']-1) for i in range(params['flank_radial_samples'])]),reverse=True)
 rings=[(r,sample(r)[0]) for r in radii]+profile[9:]
 def ang(t,c):return math.atan2(math.sin(t-c),math.cos(t-c))
 def cart(r,t):return (r*math.cos(t),r*math.sin(t))
 # Explicit nested drainage graph. Endpoints are shared exactly at confluences.
 channels=[];graph=[]
 for index,network in enumerate(params['networks']):
  c=network['angle'];dr=network['drift'];w=network['width'];depth=network['depth']
  def angle(r):return c+dr*(r-.45)+.045*math.sin(r*8+index)
  trunk=[cart(r,angle(r)) for r in [.23,.35,.48,.60,.72,.84,.96]]
  channels.append((trunk,w,depth));graph.append({'kind':'main','network':index,'points':trunk})
  for k,(offset,jr) in enumerate(zip(network['branches'],network['join_radii'])):
   # Branch heads lie uphill and offset sideways; endings attach to the trunk.
   ir=jr-.28-.025*(index%2);mr=jr-.12
   # Interpolate join coordinate on actual trunk rather than its analytic curve.
   rr=[.23,.35,.48,.60,.72,.84,.96]
   j=next(i for i in range(len(rr)-1) if rr[i]<=jr<=rr[i+1]);f=(jr-rr[j])/(rr[j+1]-rr[j]);join=tuple(trunk[j][a]*(1-f)+trunk[j+1][a]*f for a in (0,1))
   mid=cart(mr,angle(mr)+offset*.55)
   branch=[cart(ir,angle(ir)+offset),mid,join]
   channels.append((branch,w*.74,depth*.79));graph.append({'kind':'tributary','network':index,'points':branch})
   if k==0 or index in (2,4):
    # Nested tributary joins the interior branch node, not a floating incision.
    side=-1 if offset<0 else 1
    nested=[cart(mr-.17,angle(mr-.17)+offset*.55-side*.21),cart(mr-.08,angle(mr-.08)+offset*.55-side*.10),mid]
    channels.append((nested,w*.48,depth*.55));graph.append({'kind':'nested-tributary','network':index,'points':nested})
 def distance(x,y,points):
  best=1e9;along=0;length=sum(math.dist(a,b) for a,b in zip(points,points[1:]));offset=0
  for a,b in zip(points,points[1:]):
   dx=b[0]-a[0];dy=b[1]-a[1];le=math.hypot(dx,dy);u=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(le*le)))
   d=math.hypot(x-a[0]-u*dx,y-a[1]-u*dy)
   if d<best:best=d;along=(offset+u*le)/length
   offset+=le
  return best,along
 def p(r,z,t,j):
  jj=sample(r)[1] if r>=.093 else 9+(0 if r==.061 else 1 if r==.043 else 2)
  shape=1+.060*math.sin(3*t+.7)+.032*math.sin(7*t-1)
  relief=0
  if jj<9:
   envelope=math.sin(math.pi*jj/9)**.8
   for c,w,amp,drift in [(.25,.11,.075,.020),(1.18,.15,.11,-.014),(2.38,.10,.068,.025),(3.06,.18,.13,-.018),(4.42,.12,.085,.010),(5.61,.16,.10,-.022)]:
    center=c+drift*jj+.025*math.sin(jj*.85+c);relief+=amp*math.exp(-(ang(t,center)/w)**2)*envelope
   lower=math.exp(-((jj-3.0)/2.1)**2)
   relief+=.13*math.exp(-(ang(t,2.8)/.42)**2)*lower
   relief+=.10*math.exp(-(ang(t,5.0)/.32)**2)*math.exp(-((jj-2)/1.8)**2)
   for center,w,amp in [(1.58-.055*jj,.09,.06),(3.52-.045*jj,.11,.075),(5.93-.045*jj,.08,.055)]:relief+=amp*math.exp(-(ang(t,center)/w)**2)*lower
  rr=r*shape+relief
  zz=z+(12*math.sin(4*t+.6)+7*math.cos(9*t))*(.7 if jj>=8 else 1)
  if .17<r<.96:
   x,y=cart(r,t);cut=0
   for pts,width,depth in channels:
    dist,along=distance(x,y,pts)
    # Full connected trough at downstream joins; gradual blind head taper.
    head=min(1,max(0,along/.20))
    section=max(0,1-dist/width)**1.15
    cut=max(cut,depth*section*head)
   envelope=min(1,(r-.17)/.16,(.96-r)/.20)
   zz-=cut*max(0,envelope)
  return 3000*rr*math.cos(t),2700*rr*math.sin(t),max(2,zz)
 def mat(j,i):return 'gully' if j>=len(rings)-3 else 'rock'
 o=ring_surface('coherent_composite_volcano_nested_branching_eroded_flanks_small_summit_vent',n,rings,p,mat,2060)
 o['geomorphology']='Original generic concave composite volcano with explicit joined nested tributaries incised into coherent flanks; not DEM or orderly strata.'
 (out/'flank-network.json').write_text(json.dumps({'kind':'authored-illustrative-drainage-graph','channels':graph,'not_geographic_measurement':True},indent=2)+'\n')
stratovolcano()
ground_asset(col,center_xy=True)
# Bake original grounding into editable mesh coordinates so source and export use identical identity transforms.
from mathutils import Matrix
for obj in col.all_objects:
 if obj.type=='MESH':
  obj.data.transform(obj.matrix_local);obj.matrix_local=Matrix.Identity(4)
bpy.context.view_layer.update()
source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
