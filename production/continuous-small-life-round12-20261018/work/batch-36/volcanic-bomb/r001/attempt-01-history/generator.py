# SPDX-License-Identifier: MIT
"""Original deterministic batch36 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 p=Part('Single stretched spindle clast with integral cooling crust',m);v=[(-.125,0,.004)];f=[];mi=[];n=72;nr=48
 for j in range(1,nr):
  u=j/nr;x=-.125+.25*u;r=.044*math.sin(pi*u)**.77*(1+.14*math.sin(3.5*u-.4));cy=.004*math.sin(2*pi*u);cz=.008*math.sin(pi*u)+.009*(u-.5)**3
  for k in range(n):
   a=2*pi*k/n;shape=1+.035*math.sin(3*a+u*3)+.018*math.cos(5*a-u*6)
   crack=0
   for ang in [.25,2.3,4.2]:
    delta=math.atan2(math.sin(a-ang-.9*u-.1*math.sin(u*9)),math.cos(a-ang-.9*u-.1*math.sin(u*9)))
    crack+=.055*math.exp(-(delta/.074)**2)*math.sin(pi*u)**2
   rr=r*(shape-crack);v.append((x,cy+rr*math.cos(a),cz+rr*.84*math.sin(a)))
 end=len(v);v.append((.125,0,.0012))
 for k in range(n):f.append((0,1+(k+1)%n,1+k));mi.append(0)
 for j in range(nr-2):
  for k in range(n):
   a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,b,b+n,a+n));u=(j+1.5)/nr;ang=2*pi*(k+.5)/n
   distance=min(abs(math.atan2(math.sin(ang-t-.9*u-.1*math.sin(u*9)),math.cos(ang-t-.9*u-.1*math.sin(u*9)))) for t in [.25,2.3,4.2]);mi.append(1 if distance<.07 and .15<u<.85 else (2 if math.sin(ang*3+u*7)>.86 else 0))
 for k in range(n):f.append((end,1+(nr-2)*n+k,1+(nr-2)*n+(k+1)%n));mi.append(0)
 p.add(v,f,mi);p.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='volcanic-bomb');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='volcanic-bomb';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#665e58', '#4e4a47', '#75685c'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic volcanic clast','habitat_zh':'通用火山喷出块','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'One original spindle-shaped solidified clast. Continuous taper, slightly stretched ends and a few integral shallow cooling grooves. Nominal0.25m length and muted crust palette are art choices. No exact eruption, specimen, modern weapon, breadcrust or damage variants.','zh':'单件原创梭形凝固喷出块，连续收尖、略拉长的端部及少量实际浅冷却沟槽。0.25米名义长和灰褐壳色为美术选择；不指定喷发或标本，不包含现代武器、面包壳或破损变体。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Volcanic spindle bomb','zh':'梭形火山弹'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH36_COMPLETE',s)
if __name__=='__main__':main()
