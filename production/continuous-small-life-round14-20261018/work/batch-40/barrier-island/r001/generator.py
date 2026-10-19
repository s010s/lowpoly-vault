# SPDX-License-Identifier: MIT
"""Original deterministic batch40 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 p=Part('Long detached offshore sand barrier',m);n=80;nr=12;v=[(0,-2,1.25)];f=[];mi=[]
 for j in range(1,nr+1):
  r=j/nr
  for k in range(n):
   a=2*pi*k/n;x=9.2*r*math.cos(a);cy=-2+.22*math.sin(x*.43);width=1.17*(1+.13*math.sin(x*.66+.2));y=cy+width*r*math.sin(a);z=.10+(1-r*r)**1.35*(1.12+.16*math.sin(x*.65)+.07*math.cos(x*1.3));v.append((x,y,z))
 for k in range(n):f.append((0,1+k,1+(k+1)%n));mi.append(0)
 for j in range(nr-1):
  for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b));mi.append(1 if j>8 else 0)
 bottom=len(v);v.append((0,-2,0));off=len(v)
 for k in range(n):q=v[1+(nr-1)*n+k];v.append((q[0],q[1],0))
 for k in range(n):kk=(k+1)%n;a=1+(nr-1)*n+k;b=1+(nr-1)*n+kk;f.extend([(a,b,off+kk,off+k),(bottom,off+k,off+kk)]);mi.extend([1,1])
 p.add(v,f,mi);p.finish(c,False)
 # A genuinely separate mainland shore leaves a wide, open back-barrier lagoon corridor.
 nx=41;ny=8;v=[];f=[];mi=[]
 for j in range(ny):
  t=j/(ny-1)
  for k in range(nx):
   u=k/(nx-1);x=-10+20*u;shore=3.8+.35*math.sin(u*6)+.12*math.cos(u*17);y=shore+(8.6-shore)*t;z=.1+1.9*math.sin(t*pi/2)**.7+.12*math.sin(u*13)*t;v.append((x,y,z))
 for j in range(ny-1):
  for k in range(nx-1):a=j*nx+k;f.append((a,a+1,a+1+nx,a+nx));mi.append(1 if j==0 else 2)
 border=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(reversed(range((ny-1)*nx,(ny-1)*nx+nx-1)))+[j*nx for j in reversed(range(1,ny-1))];off=len(v)
 for i in border:v.append((v[i][0],v[i][1],0))
 for j,i in enumerate(border):kk=(j+1)%len(border);f.append((i,border[kk],off+kk,off+j));mi.append(1)
 f.append(tuple(off+j for j in reversed(range(len(border)))));mi.append(1);p=Part('Separate mainland coast teaching crop',m);p.add(v,f,mi);p.finish(c,False)
 return {'coastal_display':{'water_datum_m_after_grounding':.30,'lagoon_scope':'Open corridor between separate mainland shore at BlenderY>3.3m and offshore barrier nearY-2m. Both barrier ends remain detached; ocean side is lower BlenderY.','width_m':20,'presentation':'Original dry landscape teaching crop with optional separate flat water datum. No flow simulation, surveyed whole island, exact site/age or co-occurrence claim.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='barrier-island');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='barrier-island';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#bfb38e', '#d4c49f', '#929b7b'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic coast teaching crop','habitat_zh':'通用海岸教学裁片','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original elongated detached sand island, separate mainland shore and open intervening lagoon corridor, with a distinct ocean-facing side. Nominal20m landscape crop is illustrative, not a measured entire island. Water is separate display context, not an added asset or simulation.','zh':'原创离岸长条沙岛与独立大陆岸线之间留出开放潟湖通道，外海侧岸线明确。20米为示意景观裁片，非完整实测岛屿。水面仅为独立展示背景，不计新资产或流体模拟。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Barrier island','zh':'障壁岛'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH40_COMPLETE',s)
if __name__=='__main__':main()
