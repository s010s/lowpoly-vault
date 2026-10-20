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
 # A deterministic population of elliptical fused growth centers. All are sampled into one continuous closed surface.
 caps=[]
 for i in range(42):
  x=rng.uniform(-.205,.218);y=rng.uniform(-.105,.14)
  if (x/.24)**2+(y/.17)**2>.88 or (x<-.05 and y<-.035):continue
  radius=rng.uniform(.021,.047); ridge=math.exp(-((x-.075)/.11)**2-((y-.075)/.085)**2)
  z=.065+.069*ridge+rng.uniform(-.004,.009)
  caps.append((x,y,z,radius,radius*rng.uniform(.8,1.15),radius*rng.uniform(.75,1.3)))
  if i%2==0:caps.append((x+radius*.6,y-radius*.45,z+radius*.24,radius*.48,radius*.51,radius*.58))
 # High rear ridge gives the mass hierarchy from the inspected concept.
 caps.extend([(.065,.07,.135,.064,.061,.072),(.13,.058,.108,.052,.048,.058),(-.055,.07,.093,.046,.046,.05)])
 def height(x,y):
  z=.048+.012*math.sin(x*18+y*8)+.006*math.cos(y*31-x*7)
  for cx,cy,cz,rx,ry,rz in caps:
   q=((x-cx)/rx)**2+((y-cy)/ry)**2
   if q<1.5:
    h=cz+rz*math.sqrt(max(0,1-q)) if q<1 else cz-rz*math.sqrt(q-1)
    # smooth maximum creates broad solid necks instead of detached ball boundaries
    k=.009;d=max(k-abs(z-h),0)/k;z=max(z,h)+d*d*k*.25
  return z
 N=c['angular_steps'];S=c['radial_steps'];v=[(0,0,height(0,0))];faces=[]
 for j in range(1,S+1):
  for i in range(N):
   t=2*math.pi*i/N;rr=j/S;edge=1+.055*math.sin(3*t+.2)+.034*math.cos(7*t);x=.275*rr*math.cos(t)*edge;y=.20*rr*math.sin(t)*edge
   v.append((x,y,height(x,y)))
 for i in range(N):faces.append((0,1+i,1+(i+1)%N))
 for j in range(S-1):
  for i in range(N):
   a0=1+j*N+i;b=1+j*N+(i+1)%N;c0=a0+N;d=b+N
   faces.extend([(a0,c0,d),(a0,d,b)])
 edge=1+(S-1)*N;bottom=len(v)
 for i in range(N):x,y,z=v[edge+i];v.append((x*.97,y*.97,0))
 for i in range(N):a0=edge+i;b=edge+(i+1)%N;cc=bottom+i;d=bottom+(i+1)%N;faces.extend([(a0,b,d),(a0,d,cc)])
 v.append((0,0,0));center=len(v)-1
 for i in range(N):faces.append((center,bottom+(i+1)%N,bottom+i))
 # Explicit art-scale normalization. Bounds are also independently measured after export.
 mins=[min(p[k] for p in v) for k in range(3)];maxs=[max(p[k] for p in v) for k in range(3)];dims=c['nominal_art_dimensions_blender_xyz_m']
 v=[tuple((p[k]-(mins[k]+maxs[k])/2)*dims[k]/(maxs[k]-mins[k]) if k<2 else (p[k]-mins[k])*dims[k]/(maxs[k]-mins[k]) for k in range(3)) for p in v]
 ob=mesh_object('continuous-calcite-on-limestone',v,faces,mats,col)
 for poly in ob.data.polygons:
  z=sum(ob.data.vertices[i].co.z for i in poly.vertices)/len(poly.vertices)
  poly.material_index=0 if z<.079 else (1 if rng.random()<.19 else 2)
 for name,predicate in [('mineral-crust',lambda z:z>=.079),('limestone-substrate',lambda z:z<.079)]:
  group=ob.vertex_groups.new(name=name);group.add([x.index for x in ob.data.vertices if predicate(x.co.z)],1,'REPLACE')
 ob['construction']='one continuous closed sampled mineral substrate; no discrete spheres';ob['growth_center_count']=len(caps)
 export_asset(c['asset_id'],{'en':'Cave popcorn','zh':'洞穴葡萄状结核'},'geology',col,metadata={'nominal_art_dimensions_blender_xyz_m':dims,'dimension_claim':'invented illustrative art scale, not a measured specimen','generator':'generator.py','texture_policy':'texture-free','description':{'en':'Rounded fused calcite nodules on a connected limestone ledge.','zh':'相连石灰岩基底上的融合圆状方解石结核。'}},output_root=a.output_dir,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
if __name__=='__main__':main()
