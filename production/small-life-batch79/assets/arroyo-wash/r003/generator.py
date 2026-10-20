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
 nx=36;ny=150;vs=[];fs=[];ms=[]
 for j in range(ny+1):
  y=-.09+.18*j/ny
  for i in range(nx+1):
   ux=-1+2*i/nx;vy=y/.09;x=.075*ux*math.sqrt(1-.45*vy*vy);yp=y*math.sqrt(1-.45*ux*ux);u=x/.0575;v=yp/.065;r=math.sqrt(u*u+v*v)
   # Single top surface: broad low mould relief integrated with matrix, no second skin.
   mask=max(0,min(1,(1-r)*14));mask=mask*mask*(3-2*mask)
   seamx=.0005*math.sin(y*46);phase=(yp+.017*(abs(u)**1.4)*math.sin(yp*14)+(.00065 if x>seamx else 0))/.0039
   ribs=(.5+.5*math.cos(math.tau*phase))**.9
   amu=max(0,min(1,(.057-yp)/.020))
   z=.008+.00025*math.sin(x*90+y*63)+mask*(-.0008+.0026*ribs*amu+.00038*(1-r*r))
   seam=.00115*math.exp(-((x-seamx)/.0018)**2)*mask*amu;z-=seam
   # Irregular stone margins, not bilaterally perfect slab.
   xx=x+.0018*math.sin(y*64+.4)*(abs(x/.075)**8)
   yy=yp+.0016*math.sin(x*98-.2)*(abs(y/.09)**8)
   vs.append((xx,yy,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1;x,y,z=vs[a];mat='fossil' if (x/.0575)**2+(y/.065)**2<.99 else 'matrix'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 ob=gridclose('original_Dickinsonia_fossil_mould_in_continuous_matrix_SAM_P47720_informed',vs,fs,ms,nx,ny,'edge');ob['scope']='Fossil mould study, not complete living exterior; illustrative matrix and relief, not specimen replica.'

def wash():
 nx=62;ny=66;vs=[];fs=[];ms=[]
 for j in range(ny+1):
  y=-11+22*j/ny;center=.85*math.sin(y*.27)+.25*math.sin(y*.7+.5);width=1.7+.21*math.sin(y*.47)+.17*math.cos(y*.91)
  for i in range(nx+1):
   x=-7+14*i/nx;xx=x+rng.uniform(-.085,.085)*math.sin(math.pi*i/nx);yy=y+rng.uniform(-.12,.12)*math.sin(math.pi*j/ny)
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
 n=144;nz=31;vs=[];fs=[];ms=[]
 for j in range(nz):
  q=j/(nz-1);radius=(1-.96*q**3.0)
  for i in range(n):
   t=math.tau*i/n;ang=t+.006*math.sin(i*3.71+j*.81)*math.sin(math.pi*q)
   shape=1+.09*math.sin(3*t+.4)+.04*math.sin(7*t+1.2)
   x=1.6*radius*shape*math.cos(ang);y=.9*radius*shape*math.sin(ang)
   z=2.08*q+(.10*math.sin(t*3+.5)+.07*math.sin(7*t))*math.sin(math.pi*q)
   # Unequal steep foliation and localized joint offsets through whole rock skin.
   coord=x+.29*z+.08*math.sin(z*3.3+x*.8)+.055*math.sin(x*4.2)
   phase=coord*7.6+.36*math.sin(coord*4.7)+.13*math.sin(z*5.1+coord)
   f=phase-math.floor(phase);flake=f/.82 if f<.82 else (1-f)/.18
   amp=(.020+.027*(.5+.5*math.sin(z*5.2+math.floor(phase)*1.7)))*math.sin(math.pi*q)**.4
   rough=.025*math.sin(x*5.3+z*2.7)+.012*math.sin(y*7.4-z*4.1)
   delta=amp*(flake-.35)+rough*math.sin(math.pi*q)
   x+=math.cos(ang)*delta;y+=math.sin(ang)*delta
   vs.append((x,y,max(0,z)))
 for j in range(nz-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=a+n;d=b+n
   mat='mica' if rng.random()<.10 else 'schist'
   if rng.random()<.035:mat='fracture'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 base=len(vs);vs.append((0,0,0));top=len(vs);vs.append((0,0,2.13))
 for i in range(n):
  k=(i+1)%n;fs.append((base,k,i));ms.append('schist');fs.append((top,(nz-1)*n+i,(nz-1)*n+k));ms.append('schist')
 ob=multi('original_irregular_coherent_schist_outcrop_full_surface_wavy_flaky_foliation',vs,fs,ms);ob['scope']='Generic physically foliated mica schist, no exact locality/age. Unequal flakes are integral geometry.'
{'dickinsonia':fossil,'arroyo-wash':wash,'shield-volcano':shield,'schist-outcrop':schist}[slug]()
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps(dict(source=source,glb=qa,nominal_dimensions_blender_xyz_m=cfg['nominal_dimensions_blender_xyz_m'],measured_blender_xyz_m=source['bounds_blender_m']['size'],measured_glb_xyz_m=qa['bounds_m']['size'],blender_version=bpy.app.version_string,export_options={k:v for k,v in opts.items() if k!='filepath'},three_version='0.180.0',author='Leon Made This / s010s',asset_license='CC-BY-4.0',code_license='MIT'),indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
