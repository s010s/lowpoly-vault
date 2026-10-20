# SPDX-License-Identifier: MIT
"""Original lenticular endocarp with geometric Voronoi-like reticulation and opposed face horns."""
import sys,json,math,argparse,random
from pathlib import Path
import bpy
from mathutils import Vector
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'));from asset_common import setup_scene,mesh_object,make_material,ground_asset,export_asset,_vertices_world,_bounds
p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);ar=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(ar.config).read_text());s=cfg['asset_id'];col=setup_scene(s,53)
mats=[make_material('quiet-umber-cell-floors','#795332'),make_material('raised-reticulate-ridges','#AF8552'),make_material('horns-and-margin','#9A713F')]
# Original staggered seeds: coarse polygonal cells, not imported specimen geometry.
seeds=[(-.56,-.60),(.01,-.72),(.55,-.56),(-.75,-.14),(-.24,-.24),(.31,-.23),(.78,-.02),(-.60,.36),(-.05,.23),(.47,.42),(-.21,.73),(.20,.84)]
def ridge(x,z):
 ds=sorted(((x-a)**2+(z-b)**2,k) for k,(a,b) in enumerate(seeds));d0,k=ds[0];d1,l=ds[1];dist=math.sqrt(sum((seeds[k][j]-seeds[l][j])**2 for j in range(2)));edge=(d1-d0)/(2*dist);return math.exp(-(edge/.045)**2)
v=[];f=[];rv=[];L=88;H=68
# UV sphere using unique poles; thin Y lens, asymmetric egg taper.
v.append((0,0,1));rv.append(0)
for i in range(1,H):
 th=math.pi*i/H;z=math.cos(th)
 for j in range(L):
  ph=2*math.pi*j/L;x=math.sin(th)*math.cos(ph)*(1-.12*z);yb=.28*math.sin(th)*math.sin(ph);r=ridge(x,z);face=abs(math.sin(ph));y=yb+(1 if yb>=0 else -1)*.075*r*face
  v.append((x,y,z));rv.append(r)
bot=len(v);v.append((0,0,-1));rv.append(0)
for j in range(L):f.append((0,1+j,1+(j+1)%L))
for i in range(H-2):
 for j in range(L):a=1+i*L+j;b=1+i*L+(j+1)%L;f.append((a,b,b+L,a+L))
for j in range(L):f.append((1+(H-2)*L+j,bot,1+(H-2)*L+(j+1)%L))
ob=mesh_object('closed-lenticular-reticulate-endocarp',v,f,mats[:2],col)
for poly in ob.data.polygons:poly.material_index=1 if sum(rv[i] for i in poly.vertices)/len(poly.vertices)>.38 else 0
# Exactly two small horns. Roots are on broad +/-Y faces, well inside the margin.
for sign in [-1,1]:
 vv=[];ff=[];K=10
 for k,(y,rr,zshift) in enumerate([(.19,.16,0),(.34,.115,.025),(.52,.055,.075),(.58,.018,.10)]):
  for j in range(K):
   a=2*math.pi*j/K;vv.append((.10+rr*math.cos(a),sign*y,.60+zshift+rr*math.sin(a)))
 for k in range(3):
  for j in range(K):ff.append((k*K+j,k*K+(j+1)%K,(k+1)*K+(j+1)%K,(k+1)*K+j))
 ff.extend([tuple(range(K-1,-1,-1)),tuple(3*K+j for j in range(K))]);mesh_object('front-subapical-face-horn' if sign<0 else 'rear-subapical-face-horn',vv,ff,mats[2],col)
low,high=_bounds(_vertices_world(col));dims=cfg['nominal_dimensions_blender_xyz_m'];fac=[dims[i]/(high[i]-low[i]) for i in range(3)]
for ob in col.all_objects:
 if ob.type=='MESH':
  for ve in ob.data.vertices:
   for i in range(3):ve.co[i]*=fac[i]
ground_asset(col,center_xy=True)
export_asset(s,{'en':'Iodes brownii-inspired two-face-horn endocarp','zh':'双面角内果皮化石形态'},'plants',col,metadata={'claim_scope':'Stylized inspired-by endocarp only; one horn per opposed face, no whole plant or microscopic papillae. Nominal dimensions artistic.','nominal_dimensions_blender_xyz_m':dims,'textures':0},output_root=Path(ar.output),render=False,max_triangles=14000,max_materials=6,max_primitives=30)
