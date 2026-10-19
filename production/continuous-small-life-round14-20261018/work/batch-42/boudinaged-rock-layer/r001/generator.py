# SPDX-License-Identifier: MIT
"""Original deterministic batch42 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # Analytic extrusion of one connected matrix with four real through-windows; no opaque host covering pasted lenses.
 lenses=[(-.316,.090,.040),(-.115,.085,.034),(.112,.108,.045),(.326,.079,.036)]
 xs=[-.425,.425]
 for center,width,h in lenses:xs.extend([round(center-width+2*width*j/24,12) for j in range(25)])
 for i in range(3):xs.append((lenses[i][0]+lenses[i][1]+lenses[i+1][0]-lenses[i+1][1])/2)
 xs=sorted(set(xs));profile=[]
 for x in xs:
  centerz=.14+.010*math.sin(5*x+.5);half=0
  for li,(center,width,h) in enumerate(lenses):
   t=(x-center)/width
   if abs(t)<1-1e-9:half=h*max(0,1-abs(t)**4)**.72*(1+.12*math.sin(2*pi*t+li*.8))
  profile.append((0,centerz-half,centerz+half,.285+.004*math.sin(x*12)+.002*math.cos(x*31)))
 v=[];index={};f=[];front=[];back=[]
 def vert(x,y,z):
  key=tuple(round(a,11) for a in (x,y,z))
  if key not in index:index[key]=len(v);v.append((x,y,z))
  return index[key]
 for x,zs in zip(xs,profile):front.append([vert(x,-.11,z) for z in zs]);back.append([vert(x,.11,z) for z in zs])
 for j in range(len(xs)-1):
  a=front[j];b=front[j+1];aa=back[j];bb=back[j+1]
  for lo,hi in [(0,1),(2,3)]:f.append((a[lo],b[lo],b[hi],a[hi]));f.append((aa[hi],bb[hi],bb[lo],aa[lo]))
  f.append((a[0],aa[0],bb[0],b[0]));f.append((a[3],b[3],bb[3],aa[3]))
  if (profile[j][2]-profile[j][1])+(profile[j+1][2]-profile[j+1][1])>1e-8:
   f.append((a[1],b[1],bb[1],aa[1]));f.append((a[2],aa[2],bb[2],b[2]))
 for j in [0,len(xs)-1]:
  a=front[j];b=back[j]
  for lo,hi in [(0,1),(2,3)]:f.append((a[lo],a[hi],b[hi],b[lo]))
 p=Part('Continuous enclosing matrix with filled inter-lens necks',m);p.add(v,f,0);p.finish(c,False)
 p=Part('Four unequal elongated boudin lenses',m)
 for li,(center,width,h) in enumerate(lenses):
  xx=[x for x in xs if center-width-1e-9<=x<=center+width+1e-9];bottom=[];top=[]
  for x in xx:
   t=(x-center)/width;half=0 if abs(t)>=1-1e-9 else h*max(0,1-abs(t)**4)**.72*(1+.12*math.sin(2*pi*t+li*.8));cz=.14+.010*math.sin(5*x+.5);bottom.append((x,0,cz-half));top.append((x,0,cz+half))
  outline=bottom+list(reversed(top[1:-1]));p.sheet(outline,.228,1+li%2,(0,1,0))
 p.finish(c,False)
 # Shallow continuous matrix-foliation relief follows both interfaces and pinches into every neck.
 p=Part('Continuous matrix foliation around necked layer',m)
 for upper in [False,True]:
  path=[]
  for x,zs in zip(xs,profile):path.append((x,-.111,zs[2 if upper else 1]+(.010 if upper else -.010)))
  outline=[(x,y,z-.0017) for x,y,z in path]+[(x,y,z+.0017) for x,y,z in reversed(path)];p.sheet(outline,.004,0,(0,1,0))
 p.finish(c,False)
 return {'boudin_structure':{'separated_lenses':4,'matrix':'One connected extruded solid with true lens-shaped windows. Matrix fills every inter-lens gap and joins above/below; interfaces and slight exposure relief readable in gray.','scope':'Unequal elongated boudin sections replacing one necked layer. Counts, widths, section and palette illustrative, no exact strain/site/age or balls on an intact layer.'}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='boudinaged-rock-layer');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='boudinaged-rock-layer';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#979487', '#b3a489', '#a69880'])];extra=generate(c,m) or {};ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round14-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Generic structural-geology teaching section','habitat_zh':'通用构造地质教学剖面','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original stretched-layer section with four unequal elongated lenses, narrowed separated ends and continuously enclosing matrix filling the necks and joining above/below. Actual matrix windows and lens interfaces remain readable in gray. Nominal0.85m width and proportions are illustrative; no exact strain, site or age claim.','zh':'原创拉伸层剖面有四条不等长透镜体及收窄分离端，围岩真正填入颈部并连通上下。真实基质窗口和透镜界面在灰色下仍可读。0.85米宽度及比例属教学示意，不指定精确应变、地点或年代。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta.update(extra)
 export_asset(s,{'en':'Boudinaged rock layer','zh':'布丁构造岩层'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH42_COMPLETE',s)
if __name__=='__main__':main()
