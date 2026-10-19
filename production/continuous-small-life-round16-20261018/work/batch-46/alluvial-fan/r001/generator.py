# SPDX-License-Identifier: MIT
"""Original deterministic batch46 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 fan=Part('continuous-single-inflow-sloping-fan-apron',m);v=[];f=[];mi=[];nx=61;ny=49
 def height(x,t):
  z=.35+3.1*(1-t)**1.7+.36*(1-(x/(.8+8.2*t**.85))**2)*math.sin(pi*t)
  paths=[(.13*math.sin(t*5),.23)]
  if t>.23:
   u=(t-.23)/.77
   paths.extend([(end*u**power+.10*math.sin(8*t+end)*u,.17*(.4+.6*math.sin(pi*u/2))) for end,power in [(-5.6,1.03),(-2.8,1.12),(2.25,1.10),(5.25,1.06)]])
  depth=max(d*math.exp(-((x-cx)/(.17+.10*t))**2) for cx,d in paths)
  return z-depth+.027*math.sin(1.6*x+4*t)*math.sin(pi*t),depth
 for j in range(ny):
  t=j/(ny-1);w=.8+8.2*t**.85
  for i in range(nx):
   u=2*i/(nx-1)-1;x=w*u;y=7-13*t-.9*t**8*(1-u*u);z,dep=height(x,t);v.append((x,y,z))
 for j in range(ny-1):
  for i in range(nx-1):a=j*nx+i;f.append((a,a+1,a+nx+1,a+nx));mi.append(0)
 per=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)];lower=[]
 for a in per:lower.append(len(v));x,y,z=v[a];v.append((x,y,-.18))
 for j,a in enumerate(per):q=(j+1)%len(per);f.append((a,lower[j],lower[q],per[q]));mi.append(1)
 center=len(v);v.append((0,0,-.18))
 for j,a in enumerate(lower):f.append((center,lower[(j+1)%len(lower)],a));mi.append(1)
 fan.add(v,f,mi);fan.finish(c,False)
 clasts=Part('restrained-coarse-apex-sediment',m)
 for j,(x,t) in enumerate([(-.7,.16),(.65,.19),(-.45,.27),(.9,.30),(-1.05,.34),(.47,.38),(-1.2,.44),(1.45,.47),(-2,.53),(2,.57),(-3,.67),(3.5,.71)]):
  y=7-13*t;z,_=height(x,t);s=.12+.025*(j%3);clasts.ellipsoid((x,y,z+.05),(s,s*.73,.085),2,6,4)
 clasts.finish(c,False)
 return {'nominal_fan_apron_crop_width_m':18.0,'process_scope':'one original sloping18m-wide representative fan-apron crop; single narrow apex inflow opens downslope into a widening sediment surface with shallow radiating distributary channels','elevation_note':'Continuous real relief: high confined fanhead to lower broader toe. Channel cuts are geometry under one surface material; clasts are subordinate original sediment context. No delta, coast, full watershed, mapped whole fan, age or site claim.','water_scope':'Dry teaching exposure; no water mesh, hydraulic simulation or separately counted water/light asset.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='alluvial-fan');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='alluvial-fan';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#BCA47D', '#927E60', '#A99476'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round16-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic mountain-front depositional apron teaching concept','habitat_zh':'泛化坡脚沉积扇教学概念','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'One confined apex inflow opens onto a continuous downslope-widening fan surface with shallow radiating channels and restrained coarse sediment near the fanhead.18m is an artistic teaching crop, not a full measured fan, river delta, coast, watershed, site or age.','zh':'一条受限扇顶入流通向连续沿坡展宽扇面，具真实浅放射分流和克制扇顶粗沉积；18米为美术教学裁片，非实测全扇、河海三角洲、海岸、完整流域或具体地点年代。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Alluvial fan','zh':'冲积扇'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH46_COMPLETE',s)
if __name__=='__main__':main()
