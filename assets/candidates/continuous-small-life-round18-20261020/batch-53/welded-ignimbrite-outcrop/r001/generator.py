# SPDX-License-Identifier: MIT
"""Original massive ignimbrite, shaped closed fiamme relief via deterministic Boolean cuts."""
import sys,json,math,argparse
from pathlib import Path
import bpy
from mathutils import Vector
R=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'));from asset_common import setup_scene,mesh_object,make_material,ground_asset,export_asset,_vertices_world,_bounds
p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);ar=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(ar.config).read_text());s=cfg['asset_id'];col=setup_scene(s,53)
base=make_material('fused-rose-taupe-ash-matrix','#AA857B');dark=make_material('weathered-flattened-pumice-lenses','#6B574E');top=make_material('quiet-upper-fracture-plane','#BC978A')
foot=[(-.70,-.29),(-.60,-.425),(.36,-.425),(.70,-.28),(.66,.26),(.48,.425),(-.50,.425),(-.70,.18)]
v=[(x,y,0) for x,y in foot]
for i,(x,y) in enumerate(foot):v.append((x*.88+.02,y*.86,.88-.18*(x+.7)/1.4+(.04 if i in [6,7] else 0)))
f=[tuple(range(7,-1,-1)),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
rock=mesh_object('coherent-consolidated-ash-flow-outcrop',v,f,[base,dark,top],col);rock.data.polygons[1].material_index=2
# Fiamme use original asymmetric thin biconvex cutter volumes. Cross-section
# width:height mostly 7–12:1; cavities stand for weathered differential relief.
def cut_lens(name,c,axes,orient):
 vv=[];ff=[];K=12
 # local X long, Y normal/depth, Z strongly flattened thickness
 vv.append((0,0,axes[2]))
 for lat in [math.pi/4,math.pi/2,3*math.pi/4]:
  for j in range(K):
   a=2*math.pi*j/K;vv.append((axes[0]*math.sin(lat)*math.cos(a),axes[1]*math.sin(lat)*math.sin(a),axes[2]*math.cos(lat)+.06*axes[2]*math.sin(a)))
 bot=len(vv);vv.append((0,0,-axes[2]))
 for j in range(K):ff.append((0,1+j,1+(j+1)%K))
 for k in range(2):
  for j in range(K):a=1+k*K+j;b=1+k*K+(j+1)%K;ff.append((a,b,b+K,a+K))
 for j in range(K):ff.append((1+2*K+j,bot,1+2*K+(j+1)%K))
 # front/rear tangential faces share local XZ; side swaps X with Y.
 points=[]
 for q in vv:
  x,y,z=q
  if orient=='side':x,y=y,x
  elif orient=='top':x,y,z=x,z,y
  points.append((x+c[0],y+c[1],z+c[2]))
 cutter=mesh_object(name,points,ff,[base,dark,top],col)
 for pp in cutter.data.polygons:pp.material_index=1
 mod=rock.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 bpy.context.view_layer.objects.active=rock;rock.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# x,z,length,half-height. Unaligned rows, no sedimentary bedding bands.
front=[(-.37,.18,.17,.023),(.16,.14,.10,.016),(.34,.27,.16,.025),(-.08,.34,.25,.029),(-.41,.45,.13,.019),(.27,.47,.19,.026),(-.15,.60,.20,.023),(.35,.62,.09,.014),(-.38,.73,.12,.016),(.02,.75,.09,.014)]
for sign in [-1,1]:
 for i,(x,z,L,h) in enumerate(front if sign<0 else [(-x*.85,z*.92+.025,L*.8,h*.9) for x,z,L,h in front[:8]]):
  # front long face y tapers linearly with height
  y=sign*(.425*(1-.14*z/.83)-.009)
  cut_lens(f'fiamme-{sign}-{i}',(x,y,z),(L,.044,h),'front')
# Side faces and sloping top retain volume clues on alternate views.
for sign in [-1,1]:
 for i,(y,z,L,h) in enumerate([(-.12,.22,.10,.019),(.04,.40,.14,.023),(.12,.61,.09,.016)]):
  x=sign*(.68*(1-.12*z/.8))+.01
  cut_lens(f'side-fiamme-{sign}-{i}',(x,y,z),(.10,.045,h),'side')
for i,(x,y,L) in enumerate([(-.27,.03,.16),(.12,-.14,.12),(.31,.13,.10)]):
 z=.88-.18*(x+.7)/1.4
 cut_lens(f'top-fiamme-{i}',(x,y,z),(L,.043,.020),'top')

# Coherent structural fractures: one offset shoulder, a tapering top notch,
# and one chipped base corner. The untouched lower matrix connects the masses.
def cut_prism(name,poly,y0,y1,material_index=0):
 n=len(poly);verts=[(x,y0,z) for x,z in poly]+[(x,y1,z) for x,z in poly]
 faces=[tuple(range(n-1,-1,-1)),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
 obj=mesh_object(name,verts,faces,[base,dark,top],col)
 for pp in obj.data.polygons:pp.material_index=material_index
 md=rock.modifiers.new(name,'BOOLEAN');md.operation='DIFFERENCE';md.solver='EXACT';md.object=obj
 bpy.context.view_layer.objects.active=rock;bpy.ops.object.modifier_apply(modifier=md.name);bpy.data.objects.remove(obj,do_unlink=True)
cut_prism('offset-weathered-right-shoulder',[(.24,.64),(.72,.58),(1.1,.61),(1.1,1.4),(.24,1.4)],-.8,.8,2)
cut_prism('tapering-front-fracture',[(.015,.25),(.07,.47),(.035,.68),(.09,1.2),(.145,1.2),(.09,.66),(.105,.47)],-.8,-.29,0)
cut_prism('chipped-lower-left-corner',[(-.9,-.2),(-.43,-.2),(-.68,.15),(-.9,.22)],-.8,-.15,0)

# Retain the explicit flat fracture planes; no indiscriminate vertex noise.
rock.data.shade_flat();low,high=_bounds(_vertices_world(col));dims=cfg['nominal_dimensions_blender_xyz_m'];fac=[dims[i]/(high[i]-low[i]) for i in range(3)]
for ve in rock.data.vertices:
 for i in range(3):ve.co[i]*=fac[i]
ground_asset(col,center_xy=True)
export_asset(s,{'en':'Welded ignimbrite outcrop','zh':'熔结凝灰岩露头'},'geology',col,metadata={'claim_scope':'Original generic massive welded ash-flow rock with weathered flattened fiamme relief; no locality, eruption or age assertion.','nominal_dimensions_blender_xyz_m':dims,'textures':0},output_root=Path(ar.output),render=False,max_triangles=14000,max_materials=6,max_primitives=30)
