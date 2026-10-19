# SPDX-License-Identifier: MIT
"""Original deterministic batch48 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 basin=Part('one-continuous-shallow-mineral-cup',m);v=[(0,0,.014)];f=[];mi=[];N=64;J=12
 def edge(a):return .19*(1+.035*math.sin(3*a+.6)+.019*math.sin(7*a))
 for j in range(1,J+1):
  t=j/J
  for k in range(N):
   a=2*pi*k/N;r=edge(a)*t;u=max(0,(t-.49)/.51);u=u*u*(3-2*u);z=.014+.050*u+.0032*math.sin(3*a+.4)*u;v.append((r*math.cos(a),r*.82*math.sin(a),z))
 for k in range(N):f.append((0,1+k,1+(k+1)%N));mi.append(0)
 for j in range(J-1):
  for k in range(N):a=1+j*N+k;b=1+j*N+(k+1)%N;f.append((a,b,b+N,a+N));mi.append(0)
 old=[1+(J-1)*N+k for k in range(N)]
 for scale,z in [(.985,.030),(.91,0)]:
  ring=[]
  for k in range(N):a=2*pi*k/N;r=edge(a)*scale;ring.append(len(v));v.append((r*math.cos(a),r*.82*math.sin(a),z))
  for k in range(N):q=(k+1)%N;f.append((old[k],ring[k],ring[q],old[q]));mi.append(0)
  old=ring
 center=len(v);v.append((0,0,0))
 for k in range(N):f.append((center,old[(k+1)%N],old[k]));mi.append(0)
 basin.add(v,f,mi);basin.finish(c,True)
 pearls=Part('eight-discrete-unequal-rounded-mineral-concretions',m)
 records=[(-.055,-.020,.026),(-.004,-.025,.022),(.040,-.020,.021),(-.032,.026,.020),(.010,.025,.021),(.055,.028,.017),(-.075,.035,.014),(.000,.068,.012)]
 for j,(x,y,r) in enumerate(records):
  sx=r*(1.025 if j%2 else .985);sy=r*(.97 if j%3 else 1.015);sz=r*(.96+.025*(j%2));pearls.ellipsoid((x,y,.014+sz-.0002),(sx,sy,sz),1 if j%3 else 2,16,10)
 pearls.finish(c,True)
 allv=[p.co for o in c.objects if o.type=='MESH' for p in o.data.vertices];span=max(max(p[k] for p in allv)-min(p[k] for p in allv) for k in range(3));factor=.38/span
 for o in c.objects:
  if o.type=='MESH':
   for p in o.data.vertices:p.co*=factor
 return {'nominal_cup_and_concretions_span_m':.38,'pool_structure':{'discrete_concretions':8,'unequal_sizes':True,'original_basin_depth_m':.050*factor,'loose_original_layout':True},'geological_scope':'one original shallow concave mineral cup with eight unequal rounded discrete concretions; spacing/contact and supported floor seating retained, not eggs or a mechanical sphere array','water_scope':'Water omitted for a clear static mineral teaching display; no fluid simulation or measured drip mechanism. Palette, gentle irregularity, cup proportions and nominal size are artistic, not a sampled cave, age or biological egg nest.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cave-pearl-pool');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cave-pearl-pool';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B6B29C', '#D7D4BC', '#CAC8B1'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original shallow cave mineral-cup teaching concept','habitat_zh':'原创洞穴浅矿物凹盆教学概念','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'A real shallow concave mineral cup holds eight unequal rounded discrete concretions in a loose supported arrangement. Original ivory mineral tones and proportions; no egg nest, crystal cluster, mechanical array, exact cave or dated specimen.','zh':'真实浅矿物凹盆中松散承托八枚不等大圆整结核，离散及接触关系可辨；象牙矿物色和比例为原创选择，不是蛋窝、晶簇或机械球阵，不指定洞址和测年。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Cave pearl pool','zh':'洞穴珠穴'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH48_COMPLETE',s)
if __name__=='__main__':main()
