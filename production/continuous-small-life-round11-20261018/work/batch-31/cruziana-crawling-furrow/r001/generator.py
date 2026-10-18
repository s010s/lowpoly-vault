# SPDX-License-Identifier: MIT
"""Original deterministic batch31 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 slab=Part('one-negative-impression-surface-with-paired-scratched-furrows',m);nx=56;ny=100;v=[];f=[]
 for j in range(ny+1):
  y=-.15+.30*j/ny
  width=.085*(1-.105*(abs(y)/.15)**8)+.0015*math.sin(27*y+.4)
  centre=.007*math.sin(16*y+.5)
  # Tapered ends and small organized curvature: one continuous trace, no producer model.
  taper=max(0,1-(abs(y)/.131)**12)
  for i in range(nx+1):
   x=(-1+2*i/nx)*width
   z=.019+.0006*math.sin(17*x+12*y)
   d=x-centre
   for sign in [-1,1]:
    lateral=(d-sign*.019)/.013
    trough=math.exp(-lateral**4)
    z-=.0075*trough*taper
    # Scratches are recessed into the two furrow floors. Bilateral obliquity has a common forward sense.
    phase=(y-sign*.68*(d-sign*.019))/.014
    scratch=math.exp(-(math.sin(pi*phase)/.26)**2)
    z-=.0017*scratch*trough*taper
   v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;d=a+nx+1;e=d+1
   # Alternating split avoids a single directional grid crease; each triangle carries actual relief.
   f.extend([(a,b,e),(a,e,d)] if (i+j)%2==0 else [(a,b,d),(b,e,d)])
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
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cruziana-crawling-furrow');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cruziana-crawling-furrow';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#969696'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round11-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Tidal-flat trace teaching slab; original inventory context only','habitat_zh':'潮坪潜迹教学岩板；仅保留原始分类背景','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original negative-impression teaching slab with one long gently curved pair of depressed furrows and repeated bilateral oblique recessed scratches. Neutral-gray geometry must show internal relief from top and oblique views; substrate outline is not the identifier. KGS basic ichnogenus discussion consulted, whose cited specimens are mostly positive hyporelief; this is an interpretive negative display as frozen, not a copy of those specimens. Nominal0.30m slab, depths and scratch spacing are art choices. No named ichnospecies, excavated specimen, specific producer, Asaphus connection, exact motion or coexistence claim.','zh':'原创凹陷教学岩板，以一条缓弯成对凹沟和双侧重复斜向凹刮痕表达。中性灰几何须在顶视及斜视显示内部浮雕，底板轮廓不作识别依据。已查KGS潜迹属基本论述，其具名标本多为底面正浮雕；本项按冻结要求作原创新的负印迹示意，不复制这些标本。0.30米名义岩板、深度及刮痕间距为美术设定。不指定种、出土标本、制造者，不绑定Asaphus，不主张精确运动或共存。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta['trace_display']='negative-impression'
 export_asset(s,{'en':'Cruziana paired crawling-furrow teaching impression','zh':'Cruziana 双叶爬行沟凹陷教学印迹'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH31_COMPLETE',s)
if __name__=='__main__':main()
