# SPDX-License-Identifier: MIT
"""Original deterministic batch46 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 slab=Part('one-continuous-sediment-slab-with-true-negative-footprints',m);v=[];f=[];nx=51;ny=101;prints=[]
 for j in range(15):
  for sign in [-1,1]:prints.append((sign*(.034+.0015*math.sin(j*.53)),-.112+j*.016+sign*.0012,.0125*(.94+.06*math.sin(j*.9)),.0045*(.92+.08*math.cos(j*.7)),.0035*(.94+.06*math.sin(j*.8+.3)),sign))
 top=[]
 for j in range(ny):
  y=-.14+.28*j/(ny-1);corner=max(0,(abs(y)-.111)/.029);w=.0725*(1-.15*corner)
  for i in range(nx):
   x=w*(2*i/(nx-1)-1);depth=0
   for cx,cy,rx,ry,d,sign in prints:
    u=(x-cx)/rx;curved_y=cy+.00075*math.sin(pi*u)*sign;local_ry=ry*(.84+.16*(sign*u+1)/2);q=u*u+((y-curved_y)/local_ry)**2
    if q<1:depth=max(depth,d*(1-q)**1.16)
   z=.012-depth;v.append((x,y,z));top.append((x,y,z))
 for j in range(ny-1):
  for i in range(nx-1):a=j*nx+i;f.append((a,a+1,a+nx+1,a+nx))
 per=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)];lower=[]
 for a in per:lower.append(len(v));x,y,z=v[a];v.append((x,y,-.003))
 for j,a in enumerate(per):q=(j+1)%len(per);f.append((a,lower[j],lower[q],per[q]))
 center=len(v);v.append((0,0,-.003))
 for j,a in enumerate(lower):f.append((center,lower[(j+1)%len(lower)],a))
 slab.add(v,f,0);slab.finish(c,False)
 strip=[z for x,y,z in top if abs(x)<.015]
 return {'trace_display':'negative-impression','nominal_track_slab_span_m':.28,'impression_structure':{'rows':2,'independent_footprints':30,'painted_dark_marks':False,'central_axis_or_tail_groove':False,'blank_center_strip_width_m':.03,'actual_center_strip_height_range_m':max(strip)-min(strip),'nominal_top_m_before_grounding':.012,'sampled_actual_max_recess_m':.012-min(z for x,y,z in top)},'trace_scope':'one original interpretive negative-impression slab: two separated parallel rows of shallow elongated slightly tapering independent footprints, empty center; no producer identity or exact behavior','artistic_note':'Thirty impressions, spacing, small curvature, sediment tone, crop outline and nominal size are teaching-art choices, not a copied specimen, Arthropleura identification, track speed or exact depositional site.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='diplichnites-paired-trackway');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='diplichnites-paired-trackway';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#92978A'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original negative sediment-impression teaching trackway','habitat_zh':'原创沉积凹印教学步迹','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Two separated rows of true independent shallow negative footprints leave an empty central path. One continuous original slab and uniform material keep geometry responsible for shading; no painted black marks, tail groove, named producer or copied specimen.','zh':'两列真正独立浅凹足印保留空白中道；一体原创基底使用同一材质，由几何形成阴影，不涂黑充足迹、不添尾沟、不指定制造者或复制标本。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Diplichnites paired trackway','zh':'Diplichnites 双列足迹'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH46_COMPLETE',s)
if __name__=='__main__':main()
