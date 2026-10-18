# SPDX-License-Identifier: MIT
"""Original deterministic batch12 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # Real polygon plates and tapering open channels, not a noise/color texture.
 seeds=[(-.49,-.35),(-.25,-.39),(.04,-.37),(.31,-.36),(.51,-.24),(-.46,-.08),(-.20,-.11),(.12,-.10),(.37,-.06),(-.51,.19),(-.30,.24),(-.04,.16),(.21,.21),(.47,.23),(-.42,.41),(-.13,.40),(.12,.43),(.40,.42)]
 def clip(poly,nx,ny,d):
  out=[]
  for a,bb in zip(poly,poly[1:]+poly[:1]):
   va=nx*a[0]+ny*a[1]-d;vb=nx*bb[0]+ny*bb[1]-d;ina=va<=1e-10;inb=vb<=1e-10
   if ina:out.append(a)
   if ina!=inb:
    t=va/(va-vb);out.append((a[0]+t*(bb[0]-a[0]),a[1]+t*(bb[1]-a[1])))
  return out
 plates=Part('interlocking-drying-mud-plates-and-raised-edges',m)
 for j,seed in enumerate(seeds):
  poly=[(-.6,-.48),(.6,-.48),(.6,.48),(-.6,.48)]
  for other in seeds:
   if other==seed:continue
   nx=other[0]-seed[0];ny=other[1]-seed[1];d=(other[0]**2+other[1]**2-seed[0]**2-seed[1]**2)/2;poly=clip(poly,nx,ny,d)
  cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly);outline=[]
  for a,bb in zip(poly,poly[1:]+poly[:1]):
   for k in range(4):t=k/4;outline.append((a[0]*(1-t)+bb[0]*t,a[1]*(1-t)+bb[1]*t))
  n=len(outline);top=.025+.003*math.sin(j*.8);shrink=.955 if j in [2,6,11,12] else .975;v=[(cx,cy,top)];f=[]
  # The perimeter lifts slightly as the mud dries. Gaps narrow down toward their floors.
  rings=[(.32,top+.0003),(.65,top+.0007),(.87,top+.002),(shrink,top+.004),(shrink+.010,.014),(.996,.007)]
  for h,(factor,z) in enumerate(rings):
   for k,(x,y) in enumerate(outline):
    height=z+.0006*math.sin(k*.55+j)*min(h/3,1);v.append((cx+(x-cx)*factor,cy+(y-cy)*factor,height))
  for k in range(n):f.append((0,1+k,1+(k+1)%n))
  for h in range(len(rings)-1):
   for k in range(n):a=1+h*n+k;bb=1+h*n+(k+1)%n;f.append((a,bb,bb+n,a+n))
  bottom=len(v);v.append((cx,cy,.007))
  for k in range(n):f.append((bottom,1+(len(rings)-1)*n+(k+1)%n,1+(len(rings)-1)*n+k))
  plates.add(v,f,0 if j%5 else 1)
 plates.finish(c,True)
 base=Part('continuous-mud-base-below-real-crack-floors',m);v=[(-.6,-.48,0),(.6,-.48,0),(.6,.48,0),(-.6,.48,0),(-.6,-.48,.007),(.6,-.48,.007),(.6,.48,.007),(-.6,.48,.007)];f=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];base.add(v,f,2);base.finish(c,False)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='desiccation-crack-surface');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='desiccation-crack-surface';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B19A7C', '#AB9476', '#806F59'])];generate(c,m)
 if s!='limnobiophyllum':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'subaerial drying of exposed wet sediment; not permanently underwater formation','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, pose, leaf/root/frond counts and fine relief are artistic. Original geometry only; no exact species, microscopic, locality, salinity or coexistence restoration. Limnobiophyllum mounting origin is the freshwater waterline; its roots extend below it.','zh':'名义尺度、配色、姿态、叶/根/羽片数量及细小起伏为美术选择。仅含原创几何；不主张精确物种、显微结构、地点、耐盐性或同域共存复原。Limnobiophyllum 原点为淡水水面，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Stylized drying-mud crack surface','zh':'风格化干露泥裂地表'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH12_COMPLETE',s)
if __name__=='__main__':main()
