# SPDX-License-Identifier: MIT
"""Original batch79 geometry authored after complete16:28:29Z immutable premodel freezes."""
import bpy,bmesh,sys,json,math,argparse,pathlib,random
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True);slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};rng=random.Random(cfg['seed'])
def multi(name,vs,fs,ms):
 keys=list(m);o=mesh_object(name,vs,fs,[m[k] for k in keys],col)
 for p,k in zip(o.data.polygons,ms):p.material_index=keys.index(k)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=bm.faces);bm.to_mesh(o.data);bm.free();o.data.update();return o

def gridclose(name,vs,fs,ms,nx,ny,mat):
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];b=len(vs);vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],b+q,b+i));ms.append(mat)
 center=len(vs);vs.append((0,0,0))
 for i in range(len(boundary)):fs.append((center,b+(i+1)%len(boundary),b+i));ms.append(mat)
 return multi(name,vs,fs,ms)

def fossil():
 nx=28;ny=140;vs=[];fs=[];ms=[]
 # Rows follow ribs exactly so ridges are actual coherent geometry, not grid aliasing.
 for j in range(1,ny):
  v=-1+2*j/ny;yb=.065*v;width=.0575*math.sqrt(1-v*v)
  for i in range(nx+1):
   u=-1+2*i/nx;x=width*u;y=yb+.006*u*u*v*(1-v*v)+.00055*math.tanh(x/.002)*(1-v*v)
   mask=(max(0,1-u*u))**.35;amu=max(0,min(1,(.045-yb)/.018))
   rib=(.5+.5*math.cos(math.tau*j/4))**.8
   z=.008+mask*(-.0006+.0022*rib*amu+.00025*(1-v*v))-.0010*math.exp(-(x/.0018)**2)*amu
   vs.append((x,y,z))
 rows=ny-1
 for j in range(rows-1):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('fossil' if j%4 in [0,1] or j>108 else 'matrix')
 south=len(vs);vs.append((0,-.065,.008));north=len(vs);vs.append((0,.065,.008))
 for i in range(nx):
  fs.append((south,i+1,i));ms.append('fossil');a=(rows-1)*(nx+1)+i;fs.append((north,a,a+1));ms.append('fossil')
 boundary=[south]+[j*(nx+1)+nx for j in range(rows)]+[north]+[j*(nx+1) for j in range(rows-1,-1,-1)]
 outer=len(vs)
 for k in boundary:
  x,y,z=vs[k];t=math.atan2(y/.065,x/.0575);rad=1+.035*math.sin(5*t+.4)+.018*math.sin(9*t)
  vs.append((.075*rad*math.cos(t),.09*rad*math.sin(t),.008+.00025*math.sin(t*4+.2)))
 n=len(boundary)
 for i,a in enumerate(boundary):q=(i+1)%n;fs.append((a,boundary[q],outer+q,outer+i));ms.append('matrix')
 bottom=len(vs);vs.extend([(vs[outer+i][0],vs[outer+i][1],0) for i in range(n)])
 for i in range(n):q=(i+1)%n;fs.append((outer+i,outer+q,bottom+q,bottom+i));ms.append('edge')
 center=len(vs);vs.append((0,0,0))
 for i in range(n):fs.append((center,bottom+(i+1)%n,bottom+i));ms.append('edge')
 ob=multi('continuous_rib_aligned_Dickinsonia_fossil_mould_SAM_P47720_informed_matrix',vs,fs,ms);ob['scope']='Original broad oval fossil mould study;35 simplified serial ribs per side. Not living exterior or specimen facsimile.'

def wash():
 nx=62;ny=66;vs=[];fs=[];ms=[]
 for j in range(ny+1):
  y=-11+22*j/ny;center=.85*math.sin(y*.27)+.25*math.sin(y*.7+.5);width=1.7+.21*math.sin(y*.47)+.17*math.cos(y*.91)
  for i in range(nx+1):
   x=-7+14*i/nx;xx=x+rng.uniform(-.085,.085)*math.sin(math.pi*i/nx)+.22*math.sin(y*.53+.4)*abs(x/7)**8;yy=y+rng.uniform(-.12,.12)*math.sin(math.pi*j/ny)+.20*math.sin(x*.72+.9)*abs(y/11)**8
   notch=.18*math.sin(y*1.1)+.12*math.sin(y*2.9+1)
   q=(abs(xx-center)-width-notch)/.48;h=max(0,min(1,q));h=h*h*(3-2*h)
   grain=rng.uniform(-.052,.052)
   z=.60+.90*h+.065*math.sin(y*.23+x*.6)*h+grain
   vs.append((xx,yy,max(.5,z)))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1;z=sum(vs[k][2] for k in [a,b,c,d])/4
   mat='sand' if z<.8 else 'bank' if z<1.35 else 'earth'
   if z<.8 and rng.random()<.025:mat='gravel'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 ob=gridclose('coherent_dry_shallow_sinuous_incised_arroyo_wash_low_unequal_eroded_banks',vs,fs,ms,nx,ny,'earth');ob['scope']='Generic normally dry shallow arid wash, no water or flood simulation.'

def shield():
 n=144;rs=[.018,.035,.052,.072,.10,.14,.19,.25,.32,.40,.49,.58,.67,.76,.84,.91,.96,1.0];vs=[];fs=[];ms=[]
 for j,r in enumerate(rs):
  for i in range(n):
   t=math.tau*i/n;rad=1+.018*math.sin(5*t+.3)+.012*math.sin(9*t+1.1)
   x=800*r*rad*math.cos(t);y=650*r*rad*math.sin(t)
   if r<.052:z=110+.6*math.sin(3*t)*r/.052
   elif r<.072:z=110+(r-.052)/.02*10
   else:z=120*(1-((r-.072)/.928)**1.65)
   z+=10*math.sin(t*7+r*25)*r*(1-r)+7*math.sin(13*t-r*21)*r*(1-r)
   vs.append((x,y,max(.6,z)))
 for j in range(len(rs)-1):
  for i in range(n):
   q=(i+1)%n;a=j*n+i;b=j*n+q;c=a+n;d=b+n;t=math.tau*i/n;r=rs[j]
   # Broad nonuniform cooled flow regions, no repeated concentric material rings.
   cx,cy,_=vs[a];fval=math.sin(cx*.006+math.sin(cy*.007))+.6*math.sin(cy*.009+cx*.003);mat='flow' if fval>1.15 else 'weathered' if fval<-.9 else 'basalt'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 c=len(vs);vs.append((0,0,110))
 for i in range(n):fs.append((c,i,(i+1)%n));ms.append('basalt')
 outer=(len(rs)-1)*n;b=len(vs);vs.extend([(vs[outer+i][0],vs[outer+i][1],0) for i in range(n)])
 for i in range(n):q=(i+1)%n;fs.append((outer+i,b+i,b+q,outer+q));ms.append('basalt')
 fs.append(tuple(b+i for i in range(n-1,-1,-1)));ms.append('basalt')
 ob=multi('broad_low_angle_convex_shield_volcano_small_shallow_summit_depression',vs,fs,ms);ob['scope']='Generic shield, illustrative1600m module; not named island DEM or eruption.'

def schist():
 # Irregular unequal foliation-controlled cross sections form one connected solid.
 outline=[(-.65,0),(-.92,.2),(-.86,.65),(-.75,1.1),(-.65,1.6),(-.45,1.9),(-.05,2.1),(.35,2.04),(.65,1.7),(.80,1.2),(.72,.7),(.88,.25),(.6,0)];n=len(outline);stations=[];u=-1.6;layer=0
 while u<1.6:
  width=rng.uniform(.045,.14);end=min(1.6,u+width)
  stations.extend([(u,layer,.0),(max(u+.008,end-.010),layer,1.)]);u=end;layer+=1
 stations.append((1.6,layer,0.))
 vs=[];fs=[];ms=[]
 for j,(u,layer,flange) in enumerate(stations):
  endtaper=.70+.30*math.sin(math.pi*(u+1.6)/3.2)**.45
  for k in range(n):
   t=math.tau*k/n;cy=math.cos(t);sz=math.sin(t)
   y,z=outline[k];z*=.95+.12*math.sin(u*1.7)+.07*math.sin(u*4+.3)+.015*math.sin(layer*.8)
   # Unequal plate breaks and wavy edges, no perfect periodic barcode or ruled roof.
   shape=endtaper*(1+.10*math.sin(t*3+u*1.2)+.014*math.sin(t*7+layer*.7))
   ledge=(.018+.040*(.5+.5*math.sin(layer*2.3+t*.7)))*flange*max(0,math.sin(t*2.7+layer*1.3))**2
   y=y*shape+math.copysign(ledge,y);z=z*(.97+.03*math.sin(u*2.1+t*.8))+ledge*max(0,sz)
   x=u-.22*(z-.99)+.060*math.sin(z*3.8+u*.2)
   vs.append((x,y,max(.0,z-.16)))
 rings=len(stations)
 for j in range(rings-1):
  for k in range(n):
   q=(k+1)%n;a=j*n+k;b=j*n+q;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:
    fs.append(f);v=rng.random();ms.append('mica' if v<.035 else 'fracture' if v>.985 else 'schist')
 for row in [0,rings-1]:
  center=len(vs);u=stations[row][0];vs.append((u+.060*math.sin(.99*3.8+u*.2),0,.83))
  for k in range(n):fs.append((center,row*n+k,row*n+(k+1)%n));ms.append('schist')
 ob=multi('irregular_schist_unequal_wavy_steep_foliation_controlled_full_volume_plate_fracture',vs,fs,ms);ob['scope']='Generic schist outcrop; unequal physical plate-like fractures on all surfaces, not banded gneiss or painted stripe.'

{'dickinsonia':fossil,'arroyo-wash':wash,'shield-volcano':shield,'schist-outcrop':schist}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
