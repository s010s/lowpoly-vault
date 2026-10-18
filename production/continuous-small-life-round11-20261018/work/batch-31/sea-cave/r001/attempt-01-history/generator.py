# SPDX-License-Identifier: MIT
"""Original deterministic batch31 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 rock=Part('continuous-rock-face-with-real-blind-wave-cavity',m);n=64;v=[];f=[];mi=[]
 def outer(a,t):
  co=math.cos(a);si=math.sin(a)
  x=1.75*math.copysign(abs(co)**.46,co)*(1-.075*t)
  z=1.12+1.12*math.copysign(abs(si)**.53,si)
  # Coherent bedding shoulders and two broad fracture surfaces; no random facet noise.
  z+=.055*math.sin(3*a+.4)*max(0,si)+.035*t
  y=-.73+1.64*t+.075*math.sin(3*a+.5)*(1-.6*t)
  x+=.035*math.sin(5*a)*math.sin(pi*t)
  return x,y,z
 def opening(a,t):
  # A low wide mouth, roof and floor taper into a short blind recess.
  co=math.cos(a);si=math.sin(a);shape=1+.045*math.sin(3*a+.8)+.026*math.cos(5*a)
  x=-.16+.055*t+1.11*(1-.30*t)*co*shape
  z=.66+.60*(1-.25*t)*si*shape+.035*t
  y=-.79+1.13*t+.055*math.sin(2*a-.3)*(1-.5*t)
  return x,y,z
 # First, front annulus connects an irregular face directly to the recessed mouth.
 for j in range(9):
  t=j/8
  for k in range(n):
   a=2*pi*k/n;o=Vector(outer(a,0));h=Vector(opening(a,0));p=o.lerp(h,t)
   # Small uneven bevel/erosion lip, mostly quiet broad rock planes.
   p.y-=.055*math.sin(pi*t)**2*(.6+.4*math.sin(3*a+.5))
   p.z+=.025*math.sin(pi*t)*math.sin(4*a)
   v.append(tuple(p))
 for j in range(8):
  for k in range(n):
   a=j*n+k;b=j*n+(k+1)%n;f.append((a,b,b+n,a+n));mi.append(0)
 # Exterior sweep has a solid rear. This is modeled from the cave volume outward.
 outerstart=len(v)
 for j in range(1,9):
  for k in range(n):v.append(outer(2*pi*k/n,j/8))
 for j in range(8):
  prev=0 if j==0 else outerstart+(j-1)*n;curr=outerstart+j*n
  for k in range(n):
   a=prev+k;b=prev+(k+1)%n;d=curr+k;e=curr+(k+1)%n;f.append((a,d,e,b));mi.append(0 if j<5 else 1)
 # Rear rock face closes to a center behind the cave's blind wall.
 rear=outerstart+7*n;center=len(v);v.append((0,.99,1.13))
 for k in range(n):f.append((center,rear+k,rear+(k+1)%n));mi.append(1)
 # Inner tunnel continues from the same mouth vertices: thick ceiling, sides and floor.
 innerstart=len(v)
 for j in range(1,11):
  for k in range(n):v.append(opening(2*pi*k/n,j/10))
 for j in range(10):
  prev=8*n if j==0 else innerstart+(j-1)*n;curr=innerstart+j*n
  for k in range(n):
   a=prev+k;b=prev+(k+1)%n;d=curr+k;e=curr+(k+1)%n;f.append((a,b,e,d));mi.append(0)
 # Actual concave blind back; no dark paint, separate plug or rear exit.
 last=innerstart+9*n;back=len(v);v.append((-.105,.44,.695))
 for k in range(n):f.append((back,last+(k+1)%n,last+k));mi.append(0)
 rock.add(v,f,mi);o=rock.finish(c,True)
 # Normalize the explicitly declared representative face width to3.5m, no unit-cube scaling.
 lo=min(p.co.x for p in o.data.vertices);hi=max(p.co.x for p in o.data.vertices)
 for p in o.data.vertices:p.co.x*=3.5/(hi-lo)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='sea-cave');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='sea-cave';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#92938a', '#83877e'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Coastal landform teaching patch; water scene separate','habitat_zh':'海岸地形教学片区；水体场景另分','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original3.5m-wide representative coastal wall with an eroded low broad entrance, real thick roof/side walls/floor and a short blind cavity with solid rear. Whole volume modeled as one continuous surface from exterior face into the recess, not an old arch sealed by a plug. NPS supports basic sea-cave context; blind layout, local proportions, fracture simplification and palette are art choices. No copied real coast, ancient locality, exact rock age, fluid simulation or included water.','zh':'原创3.5米宽代表海岸岩壁，具低宽浪蚀入口、真实厚顶、侧壁、底面及短盲腔后壁。外岩面至洞腔为连续整体曲面，不是旧石拱加塞封堵。NPS支持基本海蚀洞背景；盲腔布局、局部比例、简化裂面及配色为美术设定。不复制具体海岸，不主张古地点、精确岩龄或流体模拟，不混入水体。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Sea cave coastal rock-face teaching module','zh':'海蚀洞海岸岩壁教学模块'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH31_COMPLETE',s)
if __name__=='__main__':main()
