# SPDX-License-Identifier: MIT
"""Original deterministic batch42 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # Continuous gravity slope beneath the fissile source ledge.
 nx=25;ny=11;v=[];f=[]
 for j in range(ny):
  y=-.33+.55*j/(ny-1)
  for k in range(nx):
   x=-.425+.85*k/(nx-1);z=.028+.38*(y+.33)+.007*math.sin(x*16)*math.sin(pi*j/(ny-1));v.append((x,y,z))
 for j in range(ny-1):
  for k in range(nx-1):a=j*nx+k;f.append((a,a+1,a+1+nx,a+nx))
 border=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(reversed(range((ny-1)*nx,(ny-1)*nx+nx-1)))+[j*nx for j in reversed(range(1,ny-1))];off=len(v)
 for i in border:v.append((v[i][0],v[i][1],0))
 for j,i in enumerate(border):kk=(j+1)%len(border);f.append((i,border[kk],off+kk,off+j))
 f.append(tuple(off+j for j in reversed(range(len(border)))));p=Part('Connected scree slope substrate',m);p.add(v,f,0);p.finish(c,False)
 p=Part('Fissile source bedrock with broken thin bedding edges',m)
 for i in range(7):
  z=.201+.022*i;outline=[]
  xy=[(-.31,.10),(-.25,.073),(-.10,.078),(.03,.061),(.16,.084),(.30,.095),(.323,.21),(.20,.239),(-.17,.23),(-.315,.204)]
  for j,(x,y) in enumerate(xy):outline.append((x+.006*math.sin(i+j),y+.007*math.sin(i*.8+j),z+.008*x))
  p.sheet(outline,.023,1+i%3,(0,0,1))
 p.finish(c,False)
 p=Part('Unequal angular platy scree and subordinate chips',m);ex=Vector((1,0,0));ey=Vector((0,1,.38)).normalized();normal=ex.cross(ey).normalized();count=0
 def flake(x,y,size,aspect,thick,angle,index):
  nonlocal count
  u=ex*math.cos(angle)+ey*math.sin(angle);vv=-ex*math.sin(angle)+ey*math.cos(angle);nn=normal;tilt=.12*math.sin(index*1.8);u=(u*math.cos(tilt)+nn*math.sin(tilt)).normalized();nn=u.cross(vv).normalized();center=Vector((x,y,.028+.38*(y+.33)+.007*math.sin(x*16)*math.sin(pi*(y+.33)/.55)+.003));outline=[]
  for k in range(7):
   a=2*pi*k/7;rr=1+.12*math.sin(k*2.1+index*.9);outline.append(tuple(center+u*(size*rr*math.cos(a))+vv*(size*aspect*rr*math.sin(a))))
  # The thin solid prism is original, angular and partly embedded in the slope; not an equal round disk.
  p.sheet(outline,thick,1+index%3,tuple(nn));count+=1
 for row in range(5):
  for col in range(10):
   index=row*10+col;x=-.355+.078*col+.012*math.sin(index*2.3);y=-.282+.073*row+.010*math.cos(index*1.4);size=.027+.012*(1-row/5)+.006*(.5+.5*math.sin(index*1.9));flake(x,y,size,.48+.15*math.sin(index*.8)**2,.0055+.002*math.sin(index)**2,.45*math.sin(index*1.7),index)
 for i in range(6):flake(-.25+.10*i,.065+.006*math.sin(i),.047,.54,.008,.18*math.sin(i*2),50+i)
 for i in range(12):flake(-.36+.065*i,-.300+.022*math.sin(i*.9),.012+.004*math.sin(i)**2,.55,.003,.8*math.sin(i),56+i)
 p.finish(c,False)
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.85/(max(p.x for p in coords)-min(p.x for p in coords))
 for o in obs:
  for v in o.data.vertices:v.co*=scale
 return {'scree_structure':{'fissile_source_layers':7,'platy_fragments':count,'composition':'Unequal angular thin slabs on a connected downslope substrate below an exposed fissile ledge; larger pieces near contact and toe, subordinate chips. Counts and tilts artistic, no exact site/age or simulated fall.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='shale-scree');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='shale-scree';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#96948b', '#868c88', '#a2a49a', '#767e7b'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic rockfall teaching patch','habitat_zh':'通用岩屑堆积教学裁片','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original fissile source ledge above a connected gravity slope of unequal thin angular shale plates and subordinate chips. Thickness and tilt hierarchy are actual geometry, not equal discs or a recoloured lava pile. Nominal0.85m width, counts, palette and layout are art choices; no exact site, age or falling-rock simulation.','zh':'原创易劈裂薄层基岩下接连续重力坡，堆积不等大的薄片状角砾及次要小碎屑。实际几何有厚薄和倾角主次，非等大薄盘或熔岩堆换色。0.85米宽度、数量、配色及布局属美术选择，不指定地点、年代或落石模拟。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Shale scree','zh':'页岩碎屑坡'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH42_COMPLETE',s)
if __name__=='__main__':main()
