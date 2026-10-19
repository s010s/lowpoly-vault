# SPDX-License-Identifier: MIT
"""Original deterministic batch33 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 shell=Part('continuous-long-hinge-wing-folded-ribbed-shell',m);nx=112;ny=24;v=[];f=[]
 # A transverse hinge line expands to long alae while the anterior central shell stays short.
 # Top and lower preserved valves meet along the same margin, with a visible quiet suture.
 for side in [1,-1]:
  for j in range(ny+1):
   t=j/ny
   for i in range(nx+1):
    u=-1+2*i/nx;x=.05*u
    central=math.exp(-(abs(u)/.47)**3.6)
    front=-.002-.030*central-.004*(1-abs(u))
    back=.004+.0018*central
    y=front*(1-t)+back*t
    edge=math.sin(pi*t)**.64*(max(0,1-u*u))**.5
    dome=.0034+.0058*central
    # Diverging rib axes arise at the umbo, their amplitudes taper into wing tips and margins.
    angle=math.atan2(x,(.006-y));ribs=.0006*(.5+.5*math.cos(angle*31))
    fold=.0020*math.exp(-(x/.0065)**2)*math.sin(pi*t)
    z=side*((dome+ribs)*edge+.00024)+fold*(1 if side==1 else -.50)
    v.append((x,y,z))
 N=(ny+1)*(nx+1)
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;d=a+nx+1;e=d+1
   f.extend([(a,b,e,d),(N+a,N+d,N+e,N+b)])
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 for k,a in enumerate(boundary):b=boundary[(k+1)%len(boundary)];f.append((a,N+a,N+b,b))
 shell.add(v,f,0);shell.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='mucrospirifer');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='mucrospirifer';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#aaa28e'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved marine brachiopod shell concept; no living soft body','habitat_zh':'保存海生腕足壳体概念；不复原活体软组织','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original fossil-shell specimen concept with very long transverse hinge wings continuous with a short convex folded/ribbed central shell. NHM named shell caption and PRI Remarks consulted for basic form only. Both preserved valve surfaces and restrained suture are geometric; no invented foot, pedicle, lophophore, colour evidence, exact species or copied specimen. Nominal0.10m hinge span, palette and simplified ribs/fold are art choices, not new fossil measurements; no living variant counted.','zh':'原创化石壳体标本概念，极长横向铰合翼与短而凸起的褶肋中央壳连续。NHM具名壳体图注与PRI Remarks仅作基本形态参考。保存双瓣表面及克制接缝均为几何；不生造足、柄、触手冠，不主张化石原色、精确种或复制标本。0.10米名义铰合展幅、配色及简化褶肋为美术设定，非新测标本尺寸；不另计活体变体。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Mucrospirifer preserved winged-shell teaching specimen','zh':'Mucrospirifer 长翼保存壳体教学标本'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH33_COMPLETE',s)
if __name__=='__main__':main()
