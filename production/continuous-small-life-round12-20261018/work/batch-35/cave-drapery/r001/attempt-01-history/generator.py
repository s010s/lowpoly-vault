# SPDX-License-Identifier: MIT
"""Original deterministic batch35 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 curtain=Part('thick-folded-mineral-drapery-and-sloping-attachment-edge',m);nu=72;nt=28;v=[];f=[]
 def surf(u,t):
  top=.46+.080*u+.012*math.sin(1.7*u)
  # Unequal mineral growth lengths, rather than a sewn horizontal textile hem.
  bottom=.035+.045*(u+.20)**2+.009*math.sin(4.6*u+.7)
  x=.19*u+.007*t*math.sin(3*u+.3)
  phase=4.7*u+.6*math.sin(1.8*u)+.17*t
  amp=.004+.034*t**.90
  y=amp*(math.sin(phase)+.15*math.sin(2.8*phase+.4))+.012*u
  z=top*(1-t)+bottom*t
  return Vector((x,y,z))
 for side in [-1,1]:
  for j in range(nt+1):
   t=j/nt
   for k in range(nu+1):
    u=-1+2*k/nu;p=surf(u,t);d=(surf(min(1,u+.001),t)-surf(max(-1,u-.001),t)).normalized();normal=Vector((-d.y,d.x,0)).normalized();thickness=.0065*(1-t)+.0032*t
    v.append(tuple(p+normal*side*thickness/2))
 N=(nt+1)*(nu+1)
 for j in range(nt):
  for k in range(nu):
   a=j*(nu+1)+k;b=a+1;d=a+nu+1;e=d+1;f.extend([(a,d,e,b),(N+a,N+b,N+e,N+d)])
 boundary=list(range(nu+1))+[j*(nu+1)+nu for j in range(1,nt+1)]+[nt*(nu+1)+k for k in range(nu-1,-1,-1)]+[j*(nu+1) for j in range(nt-1,0,-1)]
 for i,a in enumerate(boundary):b=boundary[(i+1)%len(boundary)];f.append((a,b,N+b,N+a))
 curtain.add(v,f,0);o=curtain.finish(c,True)
 low=min(p.co.z for p in o.data.vertices);high=max(p.co.z for p in o.data.vertices);scale=.45/(high-low)
 for p in o.data.vertices:p.co*=scale
 edge=[surf(-1+2*k/8,0)*scale for k in range(9)]
 return {'mounting':{'kind':'mineral growth attachment to a sloping host ceiling seam; host ceiling not included','root':'identity static-display root at lowest visible point after recorded grounding; attach host to upper edge, not a floor-standing curtain','attachment_edge_m_after_grounding':[[p.x,p.y,p.z-low*scale] for p in edge],'gravity_blender':[0,0,-1],'display_support':'upper mineral edge is intended attachment; no textile rod or invented pedestal'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cave-drapery');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cave-drapery';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#b9a888'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cave mineral growth concept; no ancient coast or named cave inferred','habitat_zh':'洞穴矿物生长概念；不推断古海岸或具名洞穴','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original opaque thin mineral drapery with a sloping upper attachment seam, gravity-directed unequal lower growth, broad dominant folds, secondary furls and real graded thickness. NPS Draperies basic growth description consulted. Upper attachment polyline and display root convention recorded; no host ceiling, textile rod, cloth hem or painted single plane. Nominal0.45m height, amber-calcite-like palette and fold layout are art choices, not a specific cave specimen, measured mineral chemistry, ancient shoreline or translucent simulation.','zh':'原创不透明薄矿物石幔，具倾斜上缘附着缝、重力方向的不等长下缘生长、主褶和次级卷曲及真实渐变厚度。已查NPS Draperies基本生长描述。记录上缘挂点折线及展示原点约定；不混入宿主洞顶、纺织挂杆、布帘缝边或单面贴图。0.45米名义高度、琥珀方解石式配色及褶形布局为美术设定，不是具名洞穴标本、矿物化学测量、古海岸或透光模拟。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Cave drapery folded-mineral teaching form','zh':'石幔褶皱矿物教学形态'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH35_COMPLETE',s)
if __name__=='__main__':main()
