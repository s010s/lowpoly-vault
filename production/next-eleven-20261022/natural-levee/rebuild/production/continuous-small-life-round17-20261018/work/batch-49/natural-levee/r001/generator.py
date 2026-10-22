# SPDX-License-Identifier: MIT
"""Original deterministic batch49 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 p=Part('Continuous channel levees and backplain sediment crop',m);nx=72;ny=48;v=[];f=[];mi=[]
 for j in range(ny+1):
  y=-5+10*j/ny;half=6.78+.22*math.cos(y*pi/10)**2;cx=.68*math.sin(y*.52)
  for i in range(nx+1):
   x=half*(-1+2*i/nx);d=x-cx;a=abs(d);side=1 if d>0 else -1
   ridge=(.44+.07*side+.035*math.sin(y*.7))*math.exp(-((a-1.72)/(.82+.06*side))**2)
   channel=.86*math.exp(-(a/1.18)**4)
   z=1.02+ridge-channel+.025*math.sin(x*.85+y*.6)+.012*y
   v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;f.extend([(a,a+1,a+nx+2),(a,a+nx+2,a+nx+1)])
   x=(v[a][0]+v[a+1][0])/2;y=v[a][1];d=abs(x-.68*math.sin(y*.52));material=0 if d<1.28 else (1 if d<2.85 else 2);mi.extend([0]*2)
 top_count=len(f)
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 nb=len(v);v.extend([(v[k][0],v[k][1],0) for k in boundary]);center=len(v);v.append((0,0,0))
 for k,a in enumerate(boundary):
  h=(k+1)%len(boundary);f.append((a,boundary[h],nb+h,nb+k));mi.append(3);f.append((center,nb+k,nb+h));mi.append(3)
 p.add(v,f,mi);o=p.finish(c,False)
 for poly in o.data.polygons:
  if poly.index<top_count:poly.use_smooth=True
 return {'nominal_scale':{'meters':14,'axis':'river-bank teaching crop width','kind':'artistic crop; not a measured full river'},'geometry_parameters':{'channel':'one sinuous continuous recessed channel crossing crop','levees':'two asymmetric broad low integral near-bank ridges','ridge_height_above_backplain_m':[.37,.55],'water':'none in asset; any water is separately labeled presentation context','textures':0},'landform_scope':'Original conceptual 14m crop including channel, near-bank levees and lower back plains; vertical relief is illustrative, no hydrodynamic or event claim.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='natural-levee');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='natural-levee';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#bba581', '#c7ac7d', '#aaa681', '#987b5e'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round17-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Fluvial landform process concept; not an exact river site.','habitat_zh':'河流地貌过程概念，非具体实地河段。','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Single continuous sediment surface contains central sinuous channel, paired broad low near-bank ridges and lower back plains. Nominal14m crop with illustrative relief and original palette; no engineered walls, water simulation or flood forecast.','zh':'连续沉积地形包括主河槽、两岸宽缓低堤和后侧低平面。14米示意裁片，起伏颜色为美术，不作人工堤墙、水动力或洪水预测。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Natural levee river-bank teaching crop','zh':'天然堤河岸教学裁片'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH49_COMPLETE',s)
if __name__=='__main__':main()
