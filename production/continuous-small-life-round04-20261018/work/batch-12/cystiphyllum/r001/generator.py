# SPDX-License-Identifier: MIT
"""Original deterministic batch12 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 part=Part('inflated-curved-solitary-cup-with-shallow-vesicular-floor',m);n=96;v=[];profiles=[]
 for j in range(21):
  t=j/20;z=.100*t;r=.005+.037*math.sin(t*pi*.56)**.92;cx=-.020*(1-t)**2+.008*t;profiles.append((cx,z,r,False))
 for j in range(21):
  r=.037*(1-j/22);z=.081+.019*(r/.037)**1.8;profiles.append((.008,z,r,True))
 for j,(cx,z,r,inside) in enumerate(profiles):
  for k in range(n):
   a=2*pi*k/n;rr=r*(1+.025*math.cos(3*a+.4));zz=z
   if inside:
    x=rr*math.cos(a);y=rr*math.sin(a);zz+=sum(.0035*math.exp(-(((x-px)/.0065)**2+((y-py)/.0060)**2)) for px,py in [(-.018,-.005),(-.008,.013),(.010,.016),(.021,0),(.010,-.017),(-.006,-.018),(0,0)])*max(0,(.100-z)/.019)
   else:rr+=.00045*math.cos(z*220+a*.2)*min(1,z/.020)
   v.append((cx+rr*math.cos(a),rr*.93*math.sin(a),zz+.00045*math.cos(4*a)*min(1,z/.10)))
 bot=len(v);v.append((-.020,0,0));floor=len(v);v.append((.008,0,.0845));f=[];mi=[]
 for k in range(n):f.append((bot,(k+1)%n,k));mi.append(0)
 for j in range(len(profiles)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j>=20 else 0)
 for k in range(n):f.append((floor,(len(profiles)-1)*n+k,(len(profiles)-1)*n+(k+1)%n));mi.append(1)
 part.add(v,f,mi);part.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cystiphyllum');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cystiphyllum';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B19A88', '#CBBEA7'])];generate(c,m)
 if s!='limnobiophyllum':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'marine solitary coral','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, pose, leaf/root/frond counts and fine relief are artistic. Original geometry only; no exact species, microscopic, locality, salinity or coexistence restoration. Limnobiophyllum mounting origin is the freshwater waterline; its roots extend below it.','zh':'名义尺度、配色、姿态、叶/根/羽片数量及细小起伏为美术选择。仅含原创几何；不主张精确物种、显微结构、地点、耐盐性或同域共存复原。Limnobiophyllum 原点为淡水水面，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Cystiphyllum-inspired inflated shallow cup coral','zh':'受 Cystiphyllum 启发的膨大浅杯珊瑚'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH12_COMPLETE',s)
if __name__=='__main__':main()
