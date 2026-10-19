# SPDX-License-Identifier: MIT
"""Original deterministic batch33 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 slab=Part('positive-spoon-casts-continuous-with-exposed-bed-sole',m);nx=56;ny=92;v=[];f=[]
 # Original aligned spoon layout, variable scale/offset without random pebble forms.
 casts=[(-.115,-.245,.255,.080,.030),(.018,-.215,.290,.074,.027),(.126,-.140,.245,.067,.025),(-.058,.065,.200,.064,.024),(-.150,.085,.165,.055,.019),(.085,.105,.145,.052,.018)]
 for j in range(ny+1):
  y=-.30+.60*j/ny
  half=.19*(1-.05*(abs(y)/.30)**8)+.002*math.sin(16*y+.3)
  for i in range(nx+1):
   x=(-1+2*i/nx)*half;z=.030+.00055*math.sin(11*x+8*y)
   for cx,start,length,width,height in casts:
    t=(y-start)/length
    if 0<t<1:
     w=width*.74*math.sin(pi*t)**.55*(1-.65*t)
     u=(x-cx)/w
     if abs(u)<1:
      # Steep rounded bulb grades into a long shallow pointed tail; positive filled relief.
      z+=height*math.sin(pi*t)**.48*(1-t)**.70*(1-u*u)**1.15
   v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;d=a+nx+1;e=d+1;f.extend([(a,b,e),(a,e,d)] if (i+j)%2==0 else [(a,b,d),(b,e,d)])
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 bottom=[]
 for a in boundary:
  x,y,z=v[a];bottom.append(len(v));v.append((x,y,0))
 for k,a in enumerate(boundary):
  nxt=(k+1)%len(boundary);b=boundary[nxt];f.append((a,b,bottom[nxt],bottom[k]))
 center=len(v);v.append((0,0,0))
 for k,a in enumerate(bottom):f.append((center,bottom[(k+1)%len(bottom)],a))
 slab.add(v,f,0);slab.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='flute-cast-slab');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='flute-cast-slab';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#969696'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Sedimentary sole-mark teaching concept; no age or precise locality inferred','habitat_zh':'沉积层底构造教学概念；不推断年代或精确地点','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original positive-cast bed-sole slab deliberately shown sole-face-up for teaching. Six aligned rounded spoon-like raised forms grade into thinner pointed tails and merge continuously with neutral-gray substrate. SERC/NAGT sole-mark description consulted; unavailable inherited USGS PDFs retained without full-read claims. Nominal0.60m span, relief depths, spacing and orientation are original art choices. No excavated specimen replica, animal footprints, random pebbles, negative furrows, exact paleoflow measurement or process simulation.','zh':'原创正凸模层底岩板，教学展示主动将层底朝上。六个同向圆匙状隆起渐变为较薄尖尾，与中性灰基底连续。已查SERC/NAGT层底构造说明；原USGS PDF访问受限如实保留，不声称已读全文。0.60米名义片区、浮雕深度、间距及方向为原创美术设定。不复制出土标本，不作动物足迹、随机卵石或凹沟，不主张精确古流向测定或过程模拟。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta['exposed_bedding_face']='bed-sole deliberately flipped upward for teaching display'
 meta['relief_polarity']='positive-cast'
 export_asset(s,{'en':'Flute cast exposed bed-sole teaching slab','zh':'槽模岩板露出层底教学模块'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH33_COMPLETE',s)
if __name__=='__main__':main()
