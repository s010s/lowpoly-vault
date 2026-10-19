# SPDX-License-Identifier: MIT
"""Original deterministic batch45 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 body=Part('continuous-long-tapered-segmented-trunk',m);pts=[];r=[]
 for j in range(121):
  t=j/120;pts.append((-.047+.078*t,0,.010+.001*math.sin(pi*t)));r.append((.0008+.0043*math.sin(pi*t)**.65)*(1-.07*(.5+.5*math.cos(2*pi*30*t))))
 body.tube(pts,r,0,12);body.finish(c,True)
 shell=Part('broad-paired-lobate-carapace-valves',m)
 for sign in [-1,1]:
  # Each closed solid half has a broad curved outer face and a hidden medial closure.
  v=[(.030,0,.016)];f=[];nt=18;na=15
  for j in range(1,nt):
   th=pi*j/nt
   for k in range(na+1):
    a=pi*k/na;v.append((.030*math.cos(th)-.001,sign*.0175*math.sin(th)*math.sin(a),.016+.010*math.sin(th)*math.cos(a)))
  tail=len(v);v.append((-.032,0,.016))
  for k in range(na):f.append((0,1+k,1+k+1))
  for j in range(nt-2):
   for k in range(na):a=1+j*(na+1)+k;f.append((a,a+na+1,a+na+2,a+1))
  for k in range(na):f.append((tail,1+(nt-2)*(na+1)+k+1,1+(nt-2)*(na+1)+k))
  edge=[0]+[1+j*(na+1) for j in range(nt-1)]+[tail]+[1+j*(na+1)+na for j in reversed(range(nt-1))];f.append(tuple(reversed(edge)));shell.add(v,f,1)
 shell.finish(c,True)
 limbs=Part('economical-jointed-walking-limbs-and-flaps',m)
 for j in range(18):
  x=-.041+j*.0038;t=j/17
  for sign in [-1,1]:
   p=(x,sign*.002,.009);el=(x-.001,sign*(.009+.003*t),.005);tip=(x+.002,sign*(.010+.003*t),.001)
   curve_tube(limbs,[p,el,tip],.0007,.00035,2,6,3)
   if j<11:limbs.ellipsoid((x,sign*.008,.009),(.0024,.005,.0009),3,8,5)
 limbs.finish(c,True)
 claw=Part('large-articulated-front-pincers-with-open-gaps',m)
 for sign in [-1,1]:
  curve_tube(claw,[(.020,sign*.008,.011),(.030,sign*.014,.010),(.039,sign*.019,.011)],.0025,.0021,2,10,5)
  claw.ellipsoid((.039,sign*.019,.011),(.0027,.0027,.0027),2,10,6)
  claw.ellipsoid((.046,sign*.020,.0115),(.0065,.0042,.003),4,14,7)
  curve_tube(claw,[(.048,sign*.0225,.0115),(.056,sign*.025,.012),(.063,sign*.0215,.012)],.0023,.00055,4,10,5)
  curve_tube(claw,[(.047,sign*.017,.0114),(.054,sign*.014,.0117),(.060,sign*.0165,.012)],.0019,.0005,4,10,5)
 claw.finish(c,True)
 tips=Part('short-antennules-and-paired-caudal-rami',m)
 for sign in [-1,1]:
  curve_tube(tips,[(.028,sign*.003,.013),(.034,sign*.0045,.0135),(.037,sign*.006,.014)],.0008,.0003,2,8,4)
  curve_tube(tips,[(-.045,sign*.0007,.011),(-.050,sign*.0025,.010),(-.053,sign*.0045,.010)],.001,.0004,3,8,4)
 tips.finish(c,True)
 # Pin total body-and-pincer length without object transforms.
 allv=[p.co for o in c.objects if o.type=='MESH' for p in o.data.vertices];lo=min(p.x for p in allv);hi=max(p.x for p in allv);factor=.1/(hi-lo)
 for o in c.objects:
  if o.type=='MESH':
   for p in o.data.vertices:p.co*=factor
 return {'nominal_body_and_pincers_length_m':.1,'anatomical_scope':'single whole Tokummia-inspired bivalved mandibulate; broad valves over long multisegmented trunk, large jointed anterior pincers with open gape, short antennules and paired rami','simplification':'Economical limb/segment/flap counts, original muted palette and calm static posture; no exact fossil replica, grasp animation or restored conspicuous eyes.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='tokummia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='tokummia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8E9B90', '#799D98', '#C4B69B', '#A7B9A5', '#BD8A70'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine benthos inspiration','habitat_zh':'寒武纪海底环境启发','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original broad bivalved carapace over a long segmented trunk, paired large articulated front pincers, short antennules and caudal rami. Reduced limb counts, palette and posture are artistic; no grasp animation or exact specimen claim.','zh':'原创宽双瓣甲覆盖长分节躯干，具成对关节前钳、短触角和尾叉；经济简化肢节数量，配色与姿态为美术选择，不承诺抓取动画或精确标本复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Tokummia pincer-bearing mandibulate','zh':'Tokummia 钳肢有颚动物'},'fauna',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH45_COMPLETE',s)
if __name__=='__main__':main()
