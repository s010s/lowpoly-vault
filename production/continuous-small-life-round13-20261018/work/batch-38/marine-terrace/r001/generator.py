# SPDX-License-Identifier: MIT
"""Original deterministic batch38 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 profile=[(-5,.15),(-4.3,.25),(-3.7,.36),(-3.5,.48),(-3.25,2.3),(-2.9,2.8),(-2.5,2.88),(-1.6,2.94),(-.6,2.99),(.4,3.0),(1.1,3.08),(1.4,3.4),(1.8,5.4),(2.3,5.8),(3,6),(4.2,6.2)]
 nx=47;ny=len(profile);v=[];f=[];mi=[]
 for j,(y,z) in enumerate(profile):
  for k in range(nx):
   u=k/(nx-1);x=-8+16*u;edge=.12*math.sin(y*1.8)+.08*math.cos(y*3);xx=x+edge*(abs(2*u-1)**6);yy=y+.17*math.sin(u*7+.3)+.08*math.cos(u*17+j*.12)
   # Low coherent erosion facets, not a noisy stone pile; upper bench is clearly raised above current datum.
   amp=.09 if 5<=j<=10 else .16;zz=z+amp*math.sin(u*12+j*.2)+amp*.35*math.cos(u*25-j*.5);v.append((xx,yy,zz))
 for j in range(ny-1):
  for k in range(nx-1):
   a=j*nx+k;f.append((a,a+1,a+1+nx,a+nx));mi.append(2 if 5<=j<10 else (3 if j>=13 else (1 if j in [3,4,11,12] else 0)))
 border=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(reversed(range((ny-1)*nx,(ny-1)*nx+nx-1)))+[j*nx for j in reversed(range(1,ny-1))];off=len(v)
 for i in border:v.append((v[i][0],v[i][1],-.8))
 for j,i in enumerate(border):kk=(j+1)%len(border);f.append((i,border[kk],off+kk,off+j));mi.append(0)
 f.append(tuple(off+j for j in reversed(range(len(border)))));mi.append(0)
 p=Part('Continuous raised marine terrace and abandoned rear cliff',m);p.add(v,f,mi);o=p.finish(c,False);span=max(v.co.x for v in o.data.vertices)-min(v.co.x for v in o.data.vertices);scale=16/span
 for v in o.data.vertices:v.co*=scale
 return {'coastal_display':{'current_coast_datum_m_after_grounding':1.25*scale,'raised_bench_typical_height_m_after_grounding':3.74*scale,'abandoned_rear_cliff_typical_top_m_after_grounding':6.6*scale,'convention':'Original illustrative dry coastal section. Lower seaward ledge marks present coastal datum; broad elevated bench and rear abandoned cliff are real geometry. Water is optional separate presentation, not another asset or simulation.','no_site_age_or_uplift_rate_claim':True}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='marine-terrace');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='marine-terrace';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#989084', '#857f75', '#b3ad90', '#9c9d80'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round13-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic coastal teaching cut','habitat_zh':'通用海岸教学裁片','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'One original raised coastal section: broad former shore bench above a lower present-coast datum, abandoned rear sea cliff and clear seaward front margin. Nominal16m width is an illustrative landscape crop, not a surveyed full landform. No water simulation, dated site or uplift rate claim.','zh':'原创抬升海岸剖面：宽阔旧台面高于较低的当前展示海岸基准，后方废弃海崖与前缘关系明确。16米是景观教学裁片名义宽度，非全地貌测绘；不承诺水体模拟、实际古地点、测年或抬升速率。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Marine terrace','zh':'海成阶地'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH38_COMPLETE',s)
if __name__=='__main__':main()
