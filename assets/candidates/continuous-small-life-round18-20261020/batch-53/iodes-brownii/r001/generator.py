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
v=[];f=[];rv=[];L=48;H=32
# UV sphere using unique poles; thin Y lens, asymmetric egg taper.
v.append((0,0,1));rv.append(0)
for i in range(1,H):
 th=math.pi*i/H;z=math.cos(th)
 for j in range(L):
  ph=2*math.pi*j/L;x=math.sin(th)*math.cos(ph)*(1-.12*z);yb=.28*math.sin(th)*math.sin(ph);r=0;face=abs(math.sin(ph));y=yb+(1 if yb>=0 else -1)*.075*r*face
  v.append((x,y,z));rv.append(r)
bot=len(v);v.append((0,0,-1));rv.append(0)
for j in range(L):f.append((0,1+j,1+(j+1)%L))
for i in range(H-2):
 for j in range(L):a=1+i*L+j;b=1+i*L+(j+1)%L;f.append((a,b,b+L,a+L))
for j in range(L):f.append((1+(H-2)*L+j,bot,1+(H-2)*L+(j+1)%L))
ob=mesh_object('closed-lenticular-reticulate-endocarp',v,f,mats[:2],col)


# Explicit polygonal reticulation. Clip original sites into a disk, then author
# curved raised ridge volumes along deduplicated cell edges on BOTH broad faces.
def clip(poly,nx,nz,c):
 out=[]
 for A,B in zip(poly,poly[1:]+poly[:1]):
  da=A[0]*nx+A[1]*nz-c;db=B[0]*nx+B[1]*nz-c
  if da<=1e-9:out.append(A)
  if (da<0)!=(db<0):
   t=da/(da-db);out.append((A[0]+t*(B[0]-A[0]),A[1]+t*(B[1]-A[1])))
 return out
edges={}
for ix,(sx,sz) in enumerate(seeds):
 poly=[(.94*math.cos(2*math.pi*j/24),.94*math.sin(2*math.pi*j/24)) for j in range(24)]
 for j,(tx,tz) in enumerate(seeds):
  if ix!=j:poly=clip(poly,tx-sx,tz-sz,(tx*tx+tz*tz-sx*sx-sz*sz)/2)
 for A,B in zip(poly,poly[1:]+poly[:1]):
  if math.dist(A,B)<1e-5:continue
  key=tuple(sorted([tuple(round(x,5) for x in A),tuple(round(x,5) for x in B)]));edges[key]=(A,B)
vv=[];ff=[]
for sign in [-1,1]:
 for A,B in edges.values():
  pts=[]
  for j in range(5):
   t=j/4;x=A[0]*(1-t)+B[0]*t;z=A[1]*(1-t)+B[1]*t;y=sign*(.28*math.sqrt(max(.001,1-x*x-z*z))+.012);pts.append(Vector((x*(1-.12*z),y,z)))
  base=len(vv);K=6
  for j,c in enumerate(pts):
   tangent=(pts[min(j+1,4)]-pts[max(0,j-1)]).normalized();normal=Vector((0,sign,0));u=tangent.cross(normal).normalized();v2=tangent.cross(u).normalized()
   for k in range(K):
    a=2*math.pi*k/K;vv.append(tuple(c+.026*(math.cos(a)*u+math.sin(a)*v2)))
  for j in range(4):
   for k in range(K):ff.append((base+j*K+k,base+j*K+(k+1)%K,base+(j+1)*K+(k+1)%K,base+(j+1)*K+k))
  ff.extend([tuple(base+k for k in range(K-1,-1,-1)),tuple(base+4*K+k for k in range(K))])
mesh_object('connected-coarse-reticulate-ridge-volumes',vv,ff,mats[1],col)

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
