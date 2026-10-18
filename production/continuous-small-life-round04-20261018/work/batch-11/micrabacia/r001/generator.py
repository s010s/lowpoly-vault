# SPDX-License-Identifier: MIT
"""Original deterministic batch11 geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 n=128;nt=25;nb=10;v=[(0,0,.003)];f=[]
 for j in range(1,nt+1):
  t=j/nt;r=.030*t
  for k in range(n):
   a=2*pi*k/n;ridge=.0011*(max(0,math.cos(32*a))**3)*math.sin(pi*t)**.45;z=.003+.004*math.sin(pi*t*.9)+.002*t+ridge
   v.append((r*math.cos(a),r*math.sin(a),z))
 for k in range(n):f.append((0,1+k,1+(k+1)%n))
 for j in range(nt-1):
  for k in range(n):a=1+j*n+k;bb=1+j*n+(k+1)%n;f.append((a,a+n,bb+n,bb))
 outer=1+(nt-1)*n;last=outer
 for j in range(nb,0,-1):
  t=j/nb;r=.030*t;start=len(v)
  for k in range(n):a=k*2*pi/n;v.append((r*math.cos(a),r*math.sin(a),.002*t*t))
  for k in range(n):f.append((last+k,last+(k+1)%n,start+(k+1)%n,start+k))
  last=start
 pole=len(v);v.append((0,0,0))
 for k in range(n):f.append((last+k,last+(k+1)%n,pole))
 part=Part('low-central-cup-and-continuous-radial-disc-relief',m);part.add(v,f,0);part.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='micrabacia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='micrabacia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#C7BDA5'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'marine','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, color, pose and repeated detail counts are artistic choices; no exact species/specimen/coexistence reconstruction. Original geometry only.','zh':'名义尺度、颜色、姿态及细小重复结构数量为美术选择；不主张精确物种、标本或同域共存复原。仅含原创几何。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Micrabacia-inspired radial-disc coral','zh':'受 Micrabacia 启发的放射盘珊瑚'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH11_COMPLETE',s)
if __name__=='__main__':main()
