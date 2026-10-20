# SPDX-License-Identifier: MIT
"""Original raised Halopoa-inspired overlapping longitudinally furrowed probes."""
import sys,json,math,argparse
from pathlib import Path
import bpy
from mathutils import Vector
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'));from asset_common import setup_scene,mesh_object,make_material,ground_asset,export_asset,_vertices_world,_bounds
p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);ar=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(ar.config).read_text());s=cfg['asset_id'];col=setup_scene(s,53)
stone=make_material('quiet-ochre-sandstone-host','#AA864B');trace=make_material('preserved-raised-sandstone-trace','#C3A066');side=make_material('slab-break-plane','#94713F')
foot=[(-.12,-.05),(-.103,-.078),(-.045,-.085),(.02,-.079),(.09,-.075),(.12,-.035),(.112,.033),(.085,.071),(.025,.085),(-.04,.08),(-.107,.062),(-.118,.015)];N=len(foot)
v=[(x*.98,y*.98,0) for x,y in foot]+[(x,y,.012+.0008*math.sin(i*1.8)) for i,(x,y) in enumerate(foot)];v.append((0,0,.012));f=[tuple(range(N-1,-1,-1))]
for i in range(N):f.append((i,(i+1)%N,(i+1)%N+N,i+N));f.append((N+i,N+(i+1)%N,2*N))
base=mesh_object('one-closed-sandstone-bedding-slab',v,f,[stone,side],col)
for pp in base.data.polygons:pp.material_index=0 if len(pp.vertices)==3 else 1
# Unequal lengths, staggered crossings, positive preservation. No radial spoke hub.
plans=[('long-low-probe',(-.101,-.034),(.092,.025),.013,0),('oblique-overlapping-probe',(-.078,.047),(.078,-.039),.0115,.012),('short-offcenter-probe',(-.095,.008),(-.018,.048),.010,0)]
for name,A,B,rmax,lift in plans:
 vv=[];ff=[];steps=28 if name!='short-offcenter-probe' else 18;K=48;direction=Vector((B[0]-A[0],B[1]-A[1],0)).normalized();u=Vector((-direction.y,direction.x,0))
 for i in range(steps+1):
  t=i/steps;r=.00065+rmax*math.sin(math.pi*t)**.48;c=Vector((A[0]*(1-t)+B[0]*t,A[1]*(1-t)+B[1]*t,.012+.40*r+lift*math.exp(-((t-.52)/.20)**2)))+u*(.0025*math.sin(math.pi*t))
  for j in range(K):
   ph=2*math.pi*j/K;corr=1+.20*math.cos(8*ph+.21*math.sin(2*math.pi*t));q=c+u*(r*corr*math.cos(ph))+Vector((0,0,r*corr*math.sin(ph)));vv.append(tuple(q))
 for i in range(steps):
  for j in range(K):ff.append((i*K+j,i*K+(j+1)%K,(i+1)*K+(j+1)%K,(i+1)*K+j))
 ff.extend([tuple(range(K-1,-1,-1)),tuple(steps*K+j for j in range(K))]);ob=mesh_object(name,vv,ff,trace,col)
 # Smooth only the curved probes: longitudinal corrugations remain real geometry.
 for pp in ob.data.polygons:pp.use_smooth=True
low,high=_bounds(_vertices_world(col));dims=cfg['nominal_dimensions_blender_xyz_m'];fac=[dims[i]/(high[i]-low[i]) for i in range(3)]
for ob in col.all_objects:
 if ob.type=='MESH':
  for ve in ob.data.vertices:
   for i in range(3):ve.co[i]*=fac[i]
ground_asset(col,center_xy=True)
export_asset(s,{'en':'Halopoa-inspired furrowed raised trace','zh':'纵褶潜穴凸浮雕'},'traces',col,metadata={'claim_scope':'Original raised trace-morphology teaching slab, overlapping cylindrical probes with longitudinal furrows; no producer or behavior certainty.','nominal_dimensions_blender_xyz_m':dims,'trace_display':'raised-fossil-relief','textures':0,'smooth_normals_note':'Intentional smooth probe normals expose continuous longitudinal corrugation; sandstone host remains faceted. Semantic closed parts overlap at preservation contacts, not a printable single solid.'},output_root=Path(ar.output),render=False,max_triangles=14000,max_materials=6,max_primitives=30)
