# SPDX-License-Identifier: MIT
"""Original deterministic batch11 geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 plates=Part('anterior-and-posterior-dorsal-shields',m)
 # Explicit rounded-square anterior plan, elongated posterior plan, calm convex axial region.
 def shield(cx,cy,wx,wy,h,mi,power):
  n=48;rings=12;v=[(cx,cy,.0038+h)];f=[]
  for j in range(1,rings):
   phi=pi*j/rings
   for k in range(n):
    a=2*pi*k/n;x=wx*math.sin(phi)*math.copysign(abs(math.cos(a))**power,math.cos(a));y=wy*math.sin(phi)*math.copysign(abs(math.sin(a))**power,math.sin(a));v.append((cx+x,cy+y,.0038+h*math.cos(phi)))
  bot=len(v);v.append((cx,cy,.0038-h))
  for k in range(n):f.append((0,1+k,1+(k+1)%n))
  for j in range(rings-2):
   for k in range(n):a=1+j*n+k;bb=1+j*n+(k+1)%n;f.append((a,a+n,bb+n,bb))
  for k in range(n):f.append((bot,1+(rings-2)*n+(k+1)%n,1+(rings-2)*n+k))
  plates.add(v,f,mi)
 shield(0,-.014,.0128,.0108,.0028,0,.64);shield(0,.0115,.0122,.0172,.0032,1,.94);plates.finish(c,True)
 limbs=Part('small-paired-walking-limbs-and-gill-blades',m)
 for j in range(13):
  y=-.021+j*.0037;w=.0105*(.85+.15*math.sin(j*pi/13))
  for side in [-1,1]:
   curve_tube(limbs,[(side*.005,y,.003),(side*w,y+.0005,.0023),(side*(w+.0038),y+.0018,.0007),(side*(w+.005),y+.0032,.0004)],[.0005][0],.00010,2,7,3)
   limbs.ellipsoid((side*.0082,y+.0006,.0026),(.0021,.00065,.00035),3,8,4)
 for side in [-1,1]:curve_tube(limbs,[(side*.003,-.021,.003),(side*.005,-.030,.003),(side*.009,-.039,.0027),(side*.011,-.044,.0022)],.0005,.00009,2,8,5)
 limbs.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='naraoia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='naraoia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#849E9C', '#8AA6A0', '#5D7979', '#A8BCB0'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'marine benthic','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, color, pose and repeated detail counts are artistic choices; no exact species/specimen/coexistence reconstruction. Original geometry only.','zh':'名义尺度、颜色、姿态及细小重复结构数量为美术选择；不主张精确物种、标本或同域共存复原。仅含原创几何。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Naraoia-inspired two-shield arthropod','zh':'受 Naraoia 启发的双盾节肢动物'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH11_COMPLETE',s)
if __name__=='__main__':main()
