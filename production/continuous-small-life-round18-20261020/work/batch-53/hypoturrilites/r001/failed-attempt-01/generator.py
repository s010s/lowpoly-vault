# SPDX-License-Identifier: MIT
"""Original continuous helicoid shell; run inside Blender. No downloaded geometry."""
import sys,json,math,argparse
from pathlib import Path
from mathutils import Vector
import bpy
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,ground_asset,export_asset,_vertices_world,_bounds
p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());s=cfg['asset_id'];col=setup_scene(s,cfg['seed']);cream=make_material('warm-limestone','#CDB485');node=make_material('rounded-ochre-nodes','#B99A66');inner=make_material('aperture-interior','#977A50')
v=[];f=[];N=264;K=12;turns=5.5
# The cross-section grows continuously; overlapping whorl contacts are intentional.
def section(t):
 th=2*math.pi*turns*t;rad=.003*12**t
 c=Vector((rad*math.cos(th),rad*math.sin(th),.12-2*rad));a=.38*rad;b=.80*rad
 return th,rad,c,a,b
for i in range(N+1):
 th,rad,c,a,b=section(i/N)
 for j in range(K):
  ph=2*math.pi*j/K;v.append(tuple(c+Vector((math.cos(th)*a*math.cos(ph),math.sin(th)*a*math.cos(ph),b*math.sin(ph)))))
for i in range(N):
 for j in range(K):f.append((i*K+j,i*K+(j+1)%K,(i+1)*K+(j+1)%K,(i+1)*K+j))
f.append(tuple(range(K-1,-1,-1)))
# Inward shell rim and a bounded cavity make the terminal mouth a real volume.
th,rad,c,a,b=section(1);start=len(v)
for depth,scale in [(0,.78),(.009,.65),(.018,.28)]:
 tangent=Vector((-math.sin(th),math.cos(th),-.15))
 for j in range(K):
  ph=2*math.pi*j/K;v.append(tuple(c-tangent*depth+Vector((math.cos(th)*a*scale*math.cos(ph),math.sin(th)*a*scale*math.cos(ph),b*scale*math.sin(ph)))))
for ring in range(3):
 outer=N*K if ring==0 else start+(ring-1)*K;inside=start+ring*K
 for j in range(K):f.append((outer+j,outer+(j+1)%K,inside+(j+1)%K,inside+j))
f.append(tuple(start+2*K+j for j in range(K)))
obj=mesh_object('one-continuous-growing-helicoid',v,f,cream,col)
# Internal faces grouped by structural material, never a baked shadow texture.
obj.data.materials.append(inner)
for poly in list(obj.data.polygons)[N*K+K:]:poly.material_index=1
nv=[];nf=[]
def ellipsoid(c,axes):
 base=len(nv);nv.append(tuple(c+Vector((0,0,axes[2]))))
 for lat in [math.pi/4,math.pi/2,3*math.pi/4]:
  for j in range(8):
   a=2*math.pi*j/8;nv.append(tuple(c+Vector((axes[0]*math.sin(lat)*math.cos(a),axes[1]*math.sin(lat)*math.sin(a),axes[2]*math.cos(lat)))))
 bottom=len(nv);nv.append(tuple(c-Vector((0,0,axes[2]))))
 for j in range(8):nf.append((base,base+1+j,base+1+(j+1)%8))
 for k in range(2):
  for j in range(8):a=base+1+k*8+j;b=base+1+k*8+(j+1)%8;nf.append((a,b,b+8,a+8))
 for j in range(8):nf.append((base+17+j,bottom,base+17+(j+1)%8))
for i in range(8,111):
 t=i/111;th,rad,c,a,b=section(t)
 for ph in [-.56,.56]:
  center=c+Vector((math.cos(th)*a*.97*math.cos(ph),math.sin(th)*a*.97*math.cos(ph),b*math.sin(ph)))
  ellipsoid(center,(rad*.14,rad*.14,rad*.18))
mesh_object('two-descending-rows-rounded-nodes',nv,nf,node,col)
low,high=_bounds(_vertices_world(col));dims=cfg['nominal_dimensions_blender_xyz_m'];fac=[dims[i]/(high[i]-low[i]) for i in range(3)]
for obj in col.all_objects:
 if obj.type=='MESH':
  for ve in obj.data.vertices:
   for i in range(3):ve.co[i]*=fac[i]
ground_asset(col,center_xy=True)
export_asset(s,{'en':'Hypoturrilites-inspired turret fossil','zh':'塔形菊石化石形态'},'animals',col,metadata={'claim_scope':'Original stylized fossil-form only; no living soft tissue, specimen copy or measured fossil scale.','nominal_dimensions_blender_xyz_m':dims,'textures':0,'preview_status':'Exact GLB proofs generated separately.'},output_root=Path(args.output),render=False,max_triangles=14000,max_materials=6,max_primitives=30)
# asset_common appends slug, so --output names the exact final slug directory.
