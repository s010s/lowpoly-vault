# SPDX-License-Identifier: MIT
"""Original deterministic batch14 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 part=Part('continuous-pedicel-flared-cup-and-radial-septa',m);n=120;v=[];profiles=[]
 # One continuous corallum: restrained holdfast, visible narrow pedicel, wide calice.
 keys=[(.0,.010),(.006,.011),(.018,.008),(.032,.008),(.043,.011),(.055,.019),(.073,.031),(.092,.043),(.110,.051),(.118,.053)]
 for j in range(len(keys)-1):
  for k in range(3):
   t=k/3;z=keys[j][0]*(1-t)+keys[j+1][0]*t;rr=keys[j][1]*(1-t)+keys[j+1][1]*t;profiles.append((z,rr,False))
 profiles.append((.118,.053,False));profiles.append((.120,.0515,True))
 for j in range(1,17):
  t=j/17;rr=.0515*(1-t);profiles.append((.078+.042*(rr/.0515)**1.7,rr,True))
 for z,rr,inside in profiles:
  for k in range(n):
   a=2*pi*k/n;cx=.005*(z/.12)**2;rad=rr*(1+.025*math.cos(3*a+.3));zz=z+.001*math.cos(5*a)*min(1,z/.075)
   if inside:zz+=.0030*max(0,math.cos(24*a))**2*math.sin(pi*min(1,rr/.053))**.45
   else:rad+=.00032*math.cos(a*24)*min(1,z/.06)
   v.append((cx+rad*math.cos(a),rad*.92*math.sin(a),zz))
 f=[];mi=[]
 for j in range(len(profiles)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if profiles[j][2] else 0)
 bot=len(v);v.append((0,0,0));top=len(v);v.append((.005,0,.078))
 for k in range(n):f.extend([(bot,(k+1)%n,k),(top,(len(profiles)-1)*n+k,(len(profiles)-1)*n+(k+1)%n)]);mi.extend([0,1])
 part.add(v,f,mi);part.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='montlivaltia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='montlivaltia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B99A82', '#CFB596'])];generate(c,m)
 if s!='cobbania':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'marine solitary coral; no exact depth or coexistence claim','habitat_zh':'海生单体珊瑚；不主张精确水深或同域共存','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, posture, simplified counts and fine relief are artistic. Original geometry only; no exact species/specimen, microscopic, locality, salinity or coexistence restoration. Cobbania mounts at the freshwater waterline with roots below it.','zh':'名义尺度、配色、姿态、简化数量及细小起伏为美术选择。仅含原创几何；不主张精确物种标本、显微结构、地点、耐盐性或共存复原。Cobbania 以淡水水面挂点为原点，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Montlivaltia-inspired stalked solitary cup coral','zh':'受 Montlivaltia 启发的有柄单体杯状珊瑚'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH14_COMPLETE',s)
if __name__=='__main__':main()
