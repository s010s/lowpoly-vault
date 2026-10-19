# SPDX-License-Identifier: MIT
"""Original deterministic batch48 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 section=Part('continuous-sediment-longitudinal-cutaway-with-serial-J-half-channels',m);v=[];f=[];NX=113;NZ=49;radius=.0036
 nodes=[(-.12+j*.035,0,.023+.006*(j%2)) for j in range(8)]
 route=catmull(nodes,5);curves=[route]
 for j,(x,y,z) in enumerate(nodes[:-1]):
  rise=.051 if j==3 else .039+.003*math.sin(j*.8)
  curves.append(catmull([(x,0,z),(x+.008,0,z-.001),(x+.016,0,z+.006),(x+.017,0,z+rise*.52),(x+.011,0,z+rise*.86),(x+.004,0,z+rise)],5))
 segments=[]
 for points in curves:
  for a,b in zip(points,points[1:]):
   ax,az=a[0],a[2];dx,dz=b[0]-ax,b[2]-az;segments.append((ax,az,dx,dz,dx*dx+dz*dz))
 depths=[]
 for j in range(NZ):
  z=.08*j/(NZ-1)
  for i in range(NX):
   x=-.14+.28*i/(NX-1);best=1
   for ax,az,dx,dz,length2 in segments:
    t=max(0,min(1,((x-ax)*dx+(z-az)*dz)/length2));d2=(x-ax-t*dx)**2+(z-az-t*dz)**2
    if d2<best:best=d2
   depth=math.sqrt(max(0,radius*radius-best));v.append((x,depth,z));depths.append(depth)
 for j in range(NZ-1):
  for i in range(NX-1):a=j*NX+i;f.append((a,a+1,a+NX+1,a+NX))
 per=list(range(NX))+[j*NX+NX-1 for j in range(1,NZ)]+[(NZ-1)*NX+i for i in range(NX-2,-1,-1)]+[j*NX for j in range(NZ-2,0,-1)];back=[]
 for a in per:back.append(len(v));x,y,z=v[a];v.append((x,.035,z))
 for j,a in enumerate(per):q=(j+1)%len(per);f.append((a,back[j],back[q],per[q]))
 center=len(v);v.append((0,.035,.04))
 for j,a in enumerate(back):f.append((center,back[(j+1)%len(back)],a))
 section.add(v,f,0);obj=section.finish(c,False)
 for poly in list(obj.data.polygons)[:(NX-1)*(NZ-1)]:poly.use_smooth=True
 return {'trace_display':'sectional-structure','nominal_probe_section_span_m':.28,'section_structure':{'serial_J_probes':7,'main_route':'one gently zigzag uniserial path','sampled_max_half_channel_depth_m':max(depths),'matrix_depth_m':.035,'presentation':'Illustrative longitudinal vertical cutaway removes near half of the sediment/burrows. True recessed half-round channels expose the connected internal route and angled J junctions; one probe reaches the illustrated upper interface.'},'trace_scope':'original schematic internal section of serial near-end joined J/downbowed probes; no excavated specimen, named producer, feeding/locomotion mechanism or exact spatial reconstruction','geometry_note':'A single continuous closed sediment mesh includes real channel voids in its cut face. Uniform material; no painted network or free-floating positive-relief tubes. Layout, depth and exposure are artistic teaching choices.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='treptichnus-serial-probe-burrow');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='treptichnus-serial-probe-burrow';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#A4A18C'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original interpretive longitudinal burrow section','habitat_zh':'原创潜穴纵向剖面示意','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'A true longitudinal sediment cutaway exposes a gently zigzag route joined to seven short angled J-shaped probes. Half-round channel voids and the upper interface make internal connections visible. Original teaching layout; no named maker, behavior or copied specimen.','zh':'真实沉积物纵剖面露出曲折路线及七个斜向短J探穴，半圆负形通道与上界面显示内部连接；布局为原创教学示意，不指定制造者、行为或复制标本。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Treptichnus serial-probe burrow','zh':'Treptichnus 串列探穴'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH48_COMPLETE',s)
if __name__=='__main__':main()
