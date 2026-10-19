# SPDX-License-Identifier: MIT
"""Original deterministic batch43 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 terrain=Part('continuous-foreshore-low-ridge-and-inland-crop',m);v=[];f=[];mat=[];nx=49;ny=45
 def surface(x,y):
  coast=.12*math.sin(.55*x)+.07*math.cos(.93*x)
  yy=y-coast
  # Gentle rising foreshore, low shore-parallel crest, then a broad landward swale/slope.
  base=.12+.53*(yy+4)/9
  ridge=.58*math.exp(-((yy-.95)/1.05)**2)
  inland=.20/(1+math.exp(-(yy-3.3)*2))
  z=base+ridge+inland+.024*math.sin(x*1.7+y*.6)+.012*math.cos(x*.6-y*1.1)
  return z,yy
 for j in range(ny):
  y=-4+9*j/(ny-1)
  for i in range(nx):
   x=-7+14*i/(nx-1)
   # Slightly clipped rounded crop corners; one continuous mainland, never an offshore island.
   corner=max(0,abs(y-.5)-3.9)/.6;x*=1-.018*corner**2
   z,_=surface(x,y);v.append((x,y,z))
 for j in range(ny-1):
  for i in range(nx-1):
   a=j*nx+i;f.append((a,a+1,a+nx+1,a+nx));_,yy=surface(v[a][0],v[a][1]);mat.append(1 if yy<-2.65 else 0)
 perimeter=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)]
 lower=[]
 for k in perimeter:lower.append(len(v));x,y,z=v[k];v.append((x*.995,y*.995,-.20))
 for j,k in enumerate(perimeter):h=(j+1)%len(perimeter);f.append((k,lower[j],lower[h],perimeter[h]));mat.append(2)
 f.append(tuple(reversed(lower)));mat.append(2)
 terrain.add(v,f,mat);terrain.finish(c,False)
 return {'nominal_crop_width_m':14.0,'coastal_water_datum_m':.45,'coastal_axis_note':'Blender negative Y is seaward, positive Y inland; GLB positive Z is seaward after axis conversion. Datum includes 0.20m grounding offset.','process_scope':'one continuous onshore sediment crop with gently sloping active foreshore and a low shore-parallel crest behind it, fading into inland swale/slope; no island or cliff terrace','water_context':'Optional exact-GLB context uses an original separate flat plane at 0.45m, not included in asset or simulated water. Crop dimensions, crest height and sediment palette are artistic.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='beach-ridge');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='beach-ridge';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#CCB48A', '#A99679', '#A78D69'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round15-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Representative shoreline sediment landform; no exact site','habitat_zh':'代表性岸线沉积地貌，非具体地点复原','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'One continuous shore crop: active gently rising foreshore, a low alongshore ridge landward of it and gentle inland transition. Nominal width14 m, subdued relief and sediment tones are artistic; no detached barrier island, giant ripple or exact age/site.','zh':'一片连续岸滩：缓升活动前滨、后方低矮沿岸堤脊与平缓陆侧过渡；14米名义宽度、起伏及沉积色为美术选择，不是离岸岛、放大波痕或特定地点年代复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Beach ridge','zh':'海滩堤脊'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH43_COMPLETE',s)
if __name__=='__main__':main()
