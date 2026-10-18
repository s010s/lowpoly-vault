# SPDX-License-Identifier: MIT
"""Original deterministic batch31 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 shell=Part('continuous-cephalon-thorax-pygidium',m)
 n=56;rows=76;v=[(0,-.0375,.0028)];f=[]
 def width(t):
  y=-.0375+.075*t
  # broad head, tapering articulated thorax and rounded pygidium
  return .023*math.sin(pi*t)**.54*(1-.18*t+.07*math.exp(-((t-.22)/.16)**2))
 for j in range(1,rows):
  t=j/rows;y=-.0375+.075*t;w=width(t)
  for k in range(n):
   a=2*pi*k/n;u=math.cos(a);upper=math.sin(a);x=w*u
   if upper>=0:
    z=.0028+.0067*upper**.72
    axis=math.exp(-(u/.31)**4);z+=.0021*axis*upper
    # shallow organic axial furrows separate three lobes, not a flat oval shield.
    z-=.00105*math.exp(-((abs(u)-.34)/.065)**2)*upper
    if .36<t<.70:
     phase=(t-.36)/.34*8
     z+=.00070*math.sin(pi*phase)**2*upper*(.65+.35*abs(u))
     z-=.00050*math.exp(-(math.sin(pi*phase)/.30)**2)*upper
    # actual head/tail transitions, coherent underlying shell.
    z-=.00085*math.exp(-((t-.354)/.012)**2)*upper
    z-=.00075*math.exp(-((t-.703)/.013)**2)*upper
   else:z=.0028+.00135*upper
   v.append((x,y,z))
 end=len(v);v.append((0,.0375,.0028))
 for k in range(n):f.append((0,1+(k+1)%n,1+k))
 for j in range(rows-2):
  for k in range(n):
   a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,b,b+n,a+n))
 for k in range(n):f.append((end,1+(rows-2)*n+k,1+(rows-2)*n+(k+1)%n))
 shell.add(v,f,0);shell.finish(c,True)
 towers=Part('head-rooted-tapered-eye-towers',m);eyes=Part('compact-terminal-eye-surfaces',m)
 for sign in [-1,1]:
  pts=[(sign*.0082,-.020,.0078),(sign*.0095,-.0192,.014),(sign*.0110,-.0185,.025),(sign*.0130,-.0187,.036),(sign*.0140,-.0198,.042)]
  curve_tube(towers,pts,.00245,.00140,0,n=12,steps=5)
  eyes.ellipsoid((sign*.0140,-.0201,.0418),(.00185,.00215,.00145),2,n=16,rings=8)
 towers.finish(c,True);eyes.finish(c,True)
 # Conservative underside hints; no particular soft-anatomy count or locomotor claim.
 ventral=Part('restrained-ventral-soft-part-hints',m)
 for j in range(6):
  y=-.010+j*.004
  for sign in [-1,1]:
   curve_tube(ventral,[(sign*.007,y,.0024),(sign*.012,y+.001,.0011),(sign*.015,y+.002,.0009)],.00075,.00035,1,n=6,steps=3)
 ventral.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='asaphus');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='asaphus';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#718680', '#596e68', '#354c48'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Marine teaching concept; separate from other batch subjects','habitat_zh':'海生教学概念，与同批其他素材不主张共存','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living inspired-by long-eye form only: smooth oval tripartite shell, coherent head/thorax/tail and tapered high eye towers rooted in the cephalon. AMNH named Asaphus kowalewskii reference supports conspicuous stalked eyes; does not establish this for the whole genus. Nominal75mm body, palette, shallow segmentation, pose and restrained ventral hints are art choices, not exact specimen/soft-anatomy/movement reconstruction.','zh':'原创活体inspired-by，仅选高眼柱形态：光滑椭圆三叶甲，头胸尾连续，高眼柱渐细并根植头甲。AMNH具名Asaphus kowalewskii支持长眼柱，不推广为全属特征。75毫米名义体长、配色、浅分节、姿态及克制腹面提示均为美术设定，不是精确标本、软体或运动复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Asaphus eye-tower trilobite inspired teaching model','zh':'Asaphus 高眼柱三叶虫灵感教学模型'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH31_COMPLETE',s)
if __name__=='__main__':main()
