# SPDX-License-Identifier: MIT
"""Original deterministic batch35 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 cup=Part('stalk-basal-cup-and-five-inset-spiral-ambulacra',m);n=100;rows=48;v=[(0,0,0)];f=[]
 # Smooth non-threaded stalk-to-cup silhouette, five grooves follow the growing body.
 profile=[(0,.0035),(.012,.0030),(.022,.0042),(.029,.010),(.040,.021),(.054,.026),(.069,.024),(.083,.018),(.093,.010),(.098,.0045)]
 def radius(z):
  for i in range(len(profile)-1):
   if z<=profile[i+1][0]:
    a,r=profile[i];b,s=profile[i+1];t=(z-a)/(b-a);t=t*t*(3-2*t);return r*(1-t)+s*t
  return profile[-1][1]
 for j in range(rows+1):
  z=.098*j/rows;r=radius(z)
  active=max(0,min(1,(z-.029)/.014))*max(0,min(1,(.099-z)/.009))
  for k in range(n):
   a=2*pi*k/n;turn=1.65*((z-.030)/.068)
   # Five inset grooves, with quiet broad intervening fields and slight growth asymmetry.
   phase=5*(a-turn);groove=math.exp(-(math.sin(phase/2)/.23)**2)
   rr=r-active*.00165*groove
   rr*=1+.025*math.sin(a+z*18)*active
   v.append((rr*math.cos(a),rr*math.sin(a),z))
 for k in range(n):f.append((0,1+(k+1)%n,1+k))
 for j in range(rows):
  for k in range(n):
   a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,b,b+n,a+n))
 # Shallow top mouth depression, continuous and not a capped industrial nut.
 inner=len(v)
 for k in range(n):
  a=2*pi*k/n;v.append((.0014*math.cos(a),.0014*math.sin(a),.0975))
 for k in range(n):f.append((1+rows*n+k,1+rows*n+(k+1)%n,inner+(k+1)%n,inner+k))
 pole=len(v);v.append((0,0,.0971))
 for k in range(n):f.append((pole,inner+k,inner+(k+1)%n))
 cup.add(v,f,0);cup.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='helicocystis');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='helicocystis';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#a3917a'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Marine stalked echinoderm inspired concept; no co-occurrence claim','habitat_zh':'海生有柄棘皮动物灵感概念；不主张共存','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living inspired-by short-stalked basal cup and rounded body with five inset spiral ambulacra, following PRI Helicocystoidea basic description. Broad quiet skeletal fields and continuous stalk/cup connection, no machined screw thread or mechanical nut. Nominal0.10m-class height, palette, simplified shallow top depression and omitted microplates/soft anatomy are art choices; no exact species, fossil scan or feeding mechanics claim.','zh':'原创活体inspired-by短柄基杯及圆体，五条内嵌螺旋沟依据PRI Helicocystoidea基本描述。保留宽阔平静骨骼区，柄杯连续，不作车削螺纹或机械螺母。约0.10米名义高度、配色、简化顶部浅凹及省略微板/软组织均为美术设定；不主张精确种、化石扫描或取食机制复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Helicocystis spiral-cup inspired teaching model','zh':'Helicocystis 螺杯棘皮动物灵感教学模型'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH35_COMPLETE',s)
if __name__=='__main__':main()
