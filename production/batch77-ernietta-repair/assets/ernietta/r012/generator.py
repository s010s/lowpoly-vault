# SPDX-License-Identifier: MIT
"""Basal-seam-only repair authored after repair-intent-freeze.json. Original upper wall retained."""
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


def ernietta():
 n=180;vs=[];fs=[];ms=[]
 # Cross-section traverses lower outer wall upward, rounded broken lip, then inside down.
 rings=[(.10,.002),(.40,.004),(.68,.009),(.86,.016),(.98,.027),(1,.038),(.96,.047),(.94,.051),(.81,.051),(.78,.046),(.73,.038),(.59,.028),(.35,.022),(.10,.020)]
 for j,(r,z) in enumerate(rings):
  for i in range(n):
   t=math.tau*i/n;rib=(.5+.5*math.cos(30*t))**.8
   # Unequal truncation, not living fan apex.
   lip=.0030*math.sin(3*t+.3)+.0018*math.sin(7*t+1.1)+.0010*math.sin(13*t)
   w=max(0,min(1,(z-.025)/.022));rr=r+(.073 if j<8 else .026)*rib*math.sin(math.pi*min(1,z/.055))
   x=.04*rr*math.cos(t)*(1+.018*math.sin(5*t));y=.025*rr*math.sin(t)*(1+.025*math.cos(3*t))
   if j==0:
    x=.030*math.cos(t);y=-.014*math.sin(t)**2+.001*math.sin(t)
   if j==1:
    x=.032*math.cos(t);y=-.004*math.sin(t)**2+.010*math.sin(t)*(1+.066*math.cos(30*t))-.002*max(0,-math.sin(t))**3
   if j==2:x=.035*math.cos(t)*(1+.025*rib);y=.017*math.sin(t)*(1+.04*rib)
   # Zigzag relief of the basal joining region, integral with rounded bottom.
   seam=0
   zz=z+w*lip
   if j==1:zz=.007+.0025*max(0,-math.sin(t))**3-.0045*max(0,math.sin(t))**3+.0002*math.cos(30*t)
   if j==2:zz=.0105
   if j==0:
    # Same long-axis zigzag on the opposed wall lips; ends join without an added collar.
    zig=(2/math.pi)*math.asin(math.cos(30*t))
    taper=math.sin(t)**2
    zz=.0030+.0035*math.sin(t)**2+.00070*zig*taper-.00065*math.sin(t)**3
   vs.append((x,y,zz))
 for j in range(len(rings)-1):
  for i in range(n):
   q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n
   mat='infill' if j>11 else 'tube' if (i%6 in [0,1,5] and j<8) else 'fossil'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 # Join the opposed basal wall lips via one recessed long-axis zigzag groove.
 # Bottom lip (rear half) folds beneath the body; upper lip (front half) carries
 # the tubular palisade down to the juncture. The two fields meet, not a belt.
 chain=[0]
 for i in range(1,n//2):
  p=vs[i];q=vs[n-i];chain.append(len(vs))
  vs.append(((p[0]+q[0])/2,(p[1]+q[1])/2+.00145*max(0,(math.sin(math.pi*i/(n//2))-.45)/.55),(p[2]+q[2])/2))
 chain.append(n//2)
 for i in range(n//2):
  rear0=i;rear1=i+1;front0=(-i)%n;front1=(-(i+1))%n;c0=chain[i];c1=chain[i+1]
  for f in [(rear0,c0,c1),(rear0,c1,rear1),(c0,front0,front1),(c0,front1,c1)]:
   if len(set(f))==3:fs.append(f);ms.append('fossil')
 row=len(rings)-1;c=len(vs);vs.append((0,0,.020))
 for i in range(n):fs.append((c,row*n+i,row*n+(i+1)%n));ms.append('infill')
 o=multi('incomplete_elliptical_ernietta_basal_fossil_sack_integral_palisade_ribs_open_cavity',vs,fs,ms)
 o['scope']='Incomplete preserved basal sack fossil form, not complete organism. Missing trunk and paired fans not reconstructed.'
 o['morphology']='30 integral tubular ribs around central cavity, truncated distal boundary, compressed slightly folded base and real recessed long-axis basal zigzag joining groove. No circumferential belt.'
assert slug=='ernietta'
ernietta()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
