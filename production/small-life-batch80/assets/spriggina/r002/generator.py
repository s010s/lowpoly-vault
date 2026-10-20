# SPDX-License-Identifier: MIT
"""Original batch80 geometry, authored only after complete immutable16:34:53Z design freeze."""
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

def spriggina():
 def point(u,v,i,j):
  # Dense axis sampling across the35mm fossil, coarser surrounding original slab.
  x=(u-.5)*.050;y=(v-.5)*.065;edgeu=abs(2*u-1);edgev=abs(2*v-1)
  x*=1-.13*edgev**5+.055*math.sin(18*v+1)*edgeu**4+.025*math.cos(31*v)*edgeu**6;y*=1-.10*edgeu**5+.045*math.sin(19*u)*edgev**4
  z=.0051+.00013*math.sin(x*220+y*330)+.00009*math.cos(x*530-y*150)
  t=(y+.018)/.035
  if 0<t<1:
   w=.0070*(1-t)**.55*(min(1,t/.10)**.5)
   if abs(x)<w and w>0:
    xn=abs(x)/w;inside=max(0,1-xn*xn)**.25
    # Negative hyporelief body with median ridge positive relative to impressed body.
    z-=.00155*inside
    if t>.14:
     phase=(t-.14)*26/.86-.25*xn*xn
     groove=math.exp(-(math.sin(math.pi*phase)/.33)**2)
     z-=.00048*groove*min(1,abs(x)/.0010)*inside
     z+=.0010*math.exp(-(x/.00070)**2)*inside
    else:z-=.00018*inside
  return x,y,z
 def mat(x,y,z,i,j):return 'impression' if z<.00445 else 'sandstone'
 o=grid('negative_hyporelief_N14_03_informed_spriggina_impression_integral_sandstone_slab',44,132,point,mat)
 o['scope']='Original simplified fossil-specimen study informed byFig2I N14-03, not replica or living animal; no eyes legs or settled affinity.'

def pediment():
 def p(u,v,i,j):
  x=(u-.5)*220*(1-.13*abs(2*v-1)**4+.035*math.sin(v*13));y=(v-.5)*260
  apron=2+v*19
  if v>.73:
   q=(v-.73)/.27;h=40*(math.sin(math.pi*q)**.75)+11*q
   jag=.68+.23*math.sin(3*x/100+1)**2+.18*math.sin(x/15)**2
   apron+=h*jag
  g=0
  for c,w,d in [(-67,7,1.7),(-11,5,2.2),(42,8,1.0)]:g+=d*math.exp(-((x-c-7*math.sin(v*3))/w)**2)
  z=apron-g*(math.sin(math.pi*v)**.7)+.20*math.sin(x*.11+y*.04)
  return x,y,max(.5,z)
 def mat(x,y,z,i,j):return 'mountain' if y>62 else 'weathered' if (i+j*3)%17<3 else 'bedrock'
 o=grid('continuous_shallow_bedrock_erosional_apron_and_abrupt_receding_mountain_front',58,52,p,mat);o['geomorphology']='Erosional pediment, not depositional alluvial fan. Apron shallow gradient, continuous bedrock.'

def kame():
 def p(u,v,i,j):
  x=(u-.5)*80;y=(v-.5)*70
  # Natural footprint tapered at corners, no streamlined long axis or circular cone.
  x*=1-.17*abs(2*v-1)**4+.04*math.sin(v*11);y*=1-.13*abs(2*u-1)**4
  edge=max(0,1-abs(2*u-1)**2.1)*max(0,1-abs(2*v-1)**2.1)
  h=22*math.exp(-((x+8)/22)**2-((y-2)/21)**2)+9*math.exp(-((x-20)/14)**2-((y+10)/14)**2)
  # An unequal collapsed flank scoop, sediment surface not a crater.
  scoop=5*math.exp(-((x+19)/8)**2-((y+16)/10)**2)
  z=.55+(h-scoop)*edge**.24+(rng.random()-.4)*.95*edge**.3
  return x,y,max(.3,z)
 def mat(x,y,z,i,j):return 'gravel' if rng.random()<.19 else 'earth' if rng.random()<.14 else 'sand'
 o=grid('irregular_ice_contact_sand_gravel_kame_mound_unequal_crest_shoulder_collapse',54,48,p,mat);o['geomorphology']='Generic glaciofluvial kame mound; not thermal-cemented, drumlin, esker or volcanic cone.'

def tuya():
 # Ring loft: all material regions in one manifold full volume with integral volcanic facies.
 n=144;vs=[];fs=[];ms=[];rings=[(1,8),(.94,36),(.87,108),(.79,215),(.73,300),(.73,330),(.70,349),(.52,350),(.25,351)]
 for j,(r,z) in enumerate(rings):
  for i in range(n):
   t=math.tau*i/n;shape=1+.05*math.sin(3*t+.7)+.035*math.cos(7*t)
   notch=math.exp(-((math.atan2(math.sin(t-.9),math.cos(t-.9)))/.23)**2)
   rr=r*shape-(.045 if j>2 else .01)*notch
   joints=.004*math.sin(36*t)+.003*math.sin(19*t+.5)
   rr+=joints if 4<=j<=6 else .012*math.sin(11*t+j*.7)
   # Localized rounded pillow-fragment-like relief on lower flank, integral not intersecting clasts.
   patch=math.exp(-(math.atan2(math.sin(t-3.7),math.cos(t-3.7))/.6)**4)
   if j in [1,2,3]:rr+=.014*patch*(.5+.5*math.cos(25*t+j*1.7))
   zz=z+(3.7*math.sin(5*t+1)+2.4*math.cos(9*t))*(1 if j<7 else .3)
   zz-=18*notch if j in [3,4,5,6] else 0
   vs.append((600*rr*math.cos(t),475*rr*math.sin(t),max(2,zz)))
 for j in range(len(rings)-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=a+n;d=b+n;t=math.tau*i/n
   mat='basalt' if j>=4 else 'breccia' if (j<3 and 2.7<t<4.6) else 'tuff'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 top=len(vs);vs.append((0,0,351));bot=len(vs);vs.append((0,0,0))
 for i in range(n):
  q=(i+1)%n;fs.append((top,(len(rings)-1)*n+i,(len(rings)-1)*n+q));ms.append('basalt');fs.append((bot,q,i));ms.append('breccia')
 o=multi('flat_top_subglacial_tuya_coherent_lava_cap_tuff_breccia_pillow_fragment_flank',vs,fs,ms);o['geomorphology']='Generic subglacial volcanic edifice with broad cap over water-contact volcanic facies, not sedimentary mesa.'
{'spriggina':spriggina,'pediment':pediment,'kame-mound':kame,'tuya':tuya}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
