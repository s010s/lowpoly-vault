# SPDX-License-Identifier: MIT
"""Original deterministic batch33 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 bench=Part('continuous-low-abrasion-bench-and-retreated-rear-cliff',m);nx=64;ny=48;v=[];f=[]
 for j in range(ny+1):
  t=j/ny
  for i in range(nx+1):
   x=-3.5+7*i/nx
   front=-2.55+.23*math.sin(1.7*x+.4)+.07*math.sin(3*x)
   rear=2.15+.08*math.sin(1.2*x)
   y=front*(1-t)+rear*t
   z=.18+.028*(y+2.55)+.025*math.sin(.9*x+.4)*math.sin(.7*y)
   # Broad low platform dominates, with a steep rear retreat face, not high stacked terraces.
   line=1.10+.22*math.sin(1.1*x)+.10*math.sin(2.2*x+.6)
   q=max(0,min(1,(y-line)/.28));q=q*q*(3-2*q)
   z+=q*(1.55+.27*math.sin(.9*x+.3)+.14*math.sin(2*x))
   # Few shallow weathered pans and joint traces; quiet walking-scale bench preserved.
   z-=.125*math.exp(-((x+1.6)/.65)**4-((y+.65)/.43)**4)*(1-q)
   z-=.085*math.exp(-((x-1.45)/.55)**4-((y+.15)/.60)**4)*(1-q)
   z-=.065*math.exp(-((x+.23*y-.35)/.10)**2)*(1-q)*max(0,1-((y+.2)/2.5)**4)
   v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;d=a+nx+1;e=d+1
   f.extend([(a,b,e),(a,e,d)] if (i+j)%2==0 else [(a,b,d),(b,e,d)])
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 bottom=[]
 for a in boundary:
  x,y,z=v[a];bottom.append(len(v));v.append((x,y,0))
 for k,a in enumerate(boundary):
  nxt=(k+1)%len(boundary);b=boundary[nxt];f.append((a,b,bottom[nxt],bottom[k]))
 center=len(v);v.append((0,0,0))
 for k,a in enumerate(bottom):f.append((center,bottom[(k+1)%len(bottom)],a))
 bench.add(v,f,0);bench.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='wave-cut-platform');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='wave-cut-platform';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#91978b'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Coastal rock platform concept; no specific age or water scene','habitat_zh':'海岸岩台概念；不指定年代，不混入水体','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original7m-wide representative shore-platform patch: a broad low gently seaward-sloping abrasion bench remains continuous with a retreated rear cliff face, with restrained shallow weathered pans and one joint. Clear cropped bedrock sides and back, no high waterfall stair, tiny isolated stone or sea-stack substitution. NPS coastal context and primary GSA shore-platform/cliff study consulted. Weathering and erosion contributions vary; not a claim that waves alone universally cut platforms. Nominal dimensions, local slope, palette and layout are art choices, not a mapped ancient site, exact tide level or fluid simulation.','zh':'原创7米宽代表海岸岩台片区：宽低、向海缓倾的磨蚀岩台与后缘退缩岩面连续，以少量浅蚀洼及一条节理提示结构。岩层侧缘和后缘为明确裁切，不做高瀑布台阶、小独石或海蚀柱替代。已查NPS海岸背景及GSA岩台与海崖实地研究。风化与侵蚀贡献各异，不主张所有岩台均仅由波浪直接切成。名义尺寸、局部坡度、配色及布局为美术设定，不是古地点测绘、精确潮位或流体模拟。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Wave-cut shore-platform teaching landscape patch','zh':'海蚀平台教学地形片区'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH33_COMPLETE',s)
if __name__=='__main__':main()
