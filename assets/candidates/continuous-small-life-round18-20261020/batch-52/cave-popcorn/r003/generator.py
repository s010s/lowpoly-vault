# SPDX-License-Identifier: MIT
from pathlib import Path
import sys,json,math,random,argparse,datetime
import bpy
R=Path(__file__).resolve()
while not (R/'scripts/asset_common.py').exists():R=R.parent
sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(a.config.read_text());rng=random.Random(c['seed']);col=setup_scene(c['asset_id'],c['seed']);mats=[make_material(n,x) for n,x in zip(['limestone','calcite-shadow','calcite-ivory'],c['palette'])]
 # Original closed slab plus overlapping mineral growth volumes, voxel-unioned into a single closed mesh.
 N=48;v=[(0,0,.055)];f=[]
 for z in [.055,0]:
  for i in range(N):
   t=i*2*math.pi/N;rr=1+.055*math.sin(3*t+.2)+.034*math.cos(7*t);v.append((.275*math.cos(t)*rr,.2*math.sin(t)*rr,z))
 for i in range(N):
  a0=1+i;b=1+(i+1)%N;cc=a0+N;d=b+N;f.extend([(0,a0,b),(a0,cc,d),(a0,d,b)])
 v.append((0,0,0));bc=len(v)-1
 for i in range(N):f.append((bc,1+N+(i+1)%N,1+N+i))
 ob=mesh_object('continuous-calcite-on-limestone',v,f,mats,col)
 caps=[]
 for i in range(42):
  x=rng.uniform(-.205,.218);y=rng.uniform(-.105,.14)
  if (x/.24)**2+(y/.17)**2>.88 or (x<-.05 and y<-.035):continue
  r=rng.uniform(.021,.047);ridge=math.exp(-((x-.075)/.11)**2-((y-.075)/.085)**2);z=.061+.045*ridge
  caps.append((x,y,z,r,r*rng.uniform(.85,1.15),r*rng.uniform(.8,1.15)))
  if i%2==0:caps.append((x+r*.55,y-r*.4,z+r*.27,r*.55,r*.52,r*.6))
 caps.extend([(.065,.07,.122,.064,.061,.072),(.13,.058,.099,.052,.048,.058),(-.055,.07,.084,.046,.046,.05)])
 for i,(x,y,z,rx,ry,rz) in enumerate(caps):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(x,y,z));part=bpy.context.object;part.name='growth-'+str(i)
  for vv in part.data.vertices:vv.co.x*=rx;vv.co.y*=ry;vv.co.z*=rz
  from asset_common import link_object
  link_object(part,col)
 bpy.ops.object.select_all(action='DESELECT')
 for part in col.objects:
  if part.type=='MESH':part.select_set(True)
 bpy.context.view_layer.objects.active=ob;bpy.ops.object.join()
 mod=ob.modifiers.new('fused-mineral-union','REMESH');mod.mode='VOXEL';mod.voxel_size=.0037;mod.use_smooth_shade=False;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=ob.modifiers.new('remove-voxel-stairsteps','SMOOTH');mod.factor=1.1;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 count=len(ob.data.polygons);mod=ob.modifiers.new('intentional-low-poly-facets','DECIMATE');mod.ratio=min(1,7400/(count*2));bpy.ops.object.modifier_apply(modifier=mod.name)
 # Lock art dimensions after union; dimensions remain an artistic choice, not specimen measurements.
 dims=c['nominal_art_dimensions_blender_xyz_m'];mins=[min(p.co[k] for p in ob.data.vertices) for k in range(3)];maxs=[max(p.co[k] for p in ob.data.vertices) for k in range(3)]
 for vv in ob.data.vertices:
  for k in range(3):vv.co[k]=(vv.co[k]-(mins[k]+maxs[k])/2)*dims[k]/(maxs[k]-mins[k]) if k<2 else (vv.co[k]-mins[k])*dims[k]/(maxs[k]-mins[k])
 ob.data.materials.clear()
 for m in mats:ob.data.materials.append(m)
 for poly in ob.data.polygons:
  z=sum(ob.data.vertices[i].co.z for i in poly.vertices)/len(poly.vertices);poly.material_index=0 if z<.077 else (1 if rng.random()<.035 else 2);poly.use_smooth=False
 ob['construction']='closed voxel union of original slab and intersecting mineral nodule volumes; no disconnected spheres';ob['growth_center_count']=len(caps)
 export_asset(c['asset_id'],{'en':'Cave popcorn','zh':'洞穴葡萄状结核'},'geology',col,metadata={'nominal_art_dimensions_blender_xyz_m':dims,'dimension_claim':'invented illustrative art scale, not a measured specimen','generator':'generator.py','texture_policy':'texture-free','description':{'en':'Rounded fused calcite nodules on a connected limestone ledge.','zh':'相连石灰岩基底上的融合圆状方解石结核。'}},output_root=a.output_dir,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
if __name__=='__main__':main()
