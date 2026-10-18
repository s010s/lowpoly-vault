# SPDX-License-Identifier: MIT
"""Original deterministic batch22 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 p=Part('continuous billowy ropy lava crust',m);v=[];faces=[];mi=[];nx=64;ny=72
 centers=[-.245,-.164,-.076,.021,.122,.216];amps=[.010,.022,.025,.021,.018,.011];widths=[.019,.020,.022,.023,.022,.020]
 for j in range(ny+1):
  vv=j/ny;y0=-.30+.60*vv
  for i in range(nx+1):
   u=i/nx;x0=-.45+.90*u
   x=x0*(.88+.12*math.sin(pi*vv)+.035*math.sin(10*vv+1)+.018*math.sin(23*vv));y=y0+.024*math.sin(8*u+.4)+.012*math.sin(19*u)*abs(2*vv-1)**4
   phase=y+.135*(x/.45)**2+.014*math.sin(7*x+1)
   z=.035+.023*math.exp(-((x+.045)/.43)**4-((y+.02)/.38)**4)
   for k,(ce,amp,wd) in enumerate(zip(centers,amps,widths)):
    ce+=.026*math.sin(8*x+k*.78)+.010*math.sin(19*x+k*1.1)
    z+=amp*(.70+.30*math.cos(8*x+k*.9))*math.exp(-((phase-ce)/(wd*(.82+.22*math.cos(12*x+k))))**2)
   z+=.015*math.exp(-((x+.23)/.20)**2-((y-.12)/.12)**2)+.012*math.exp(-((x-.17)/.22)**2-((y-.03)/.13)**2)
   # A lower secondary tongue grades smoothly into the main moving crust.
   local=y-.035+.05*((x-.25)/.22)**2
   z+=.008*math.exp(-((local-.06)/.018)**2)*math.exp(-((x-.26)/.18)**4)
   z+=.0012*math.sin(19*x+4*y)*math.sin(17*y-3*x)
   v.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1));mi.append(1 if j%19==7 and i<10 else 0)
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 bottom=[]
 for a in boundary:bottom.append(len(v));v.append((v[a][0],v[a][1],.0025+.0015*math.sin(v[a][0]*6)**2))
 center=len(v);v.append((0,0,.0025))
 for k,a in enumerate(boundary):
  kk=(k+1)%len(boundary);faces.append((a,bottom[k],bottom[kk],boundary[kk]));mi.append(1);faces.append((center,bottom[kk],bottom[k]));mi.append(1)
 p.add(v,faces,mi);o=p.finish(c,True)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='pahoehoe-lava-surface');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='pahoehoe-lava-surface';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#6F7575', '#666D6E'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original illustrative basaltic flow-surface patch','habitat_zh':'原创玄武质熔岩流表面教学片段','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Geological-form artistic concept: one closed continuous crust mesh, with rounded bowed folds following a common flow direction and a subordinate overlapping tongue. Original cropped patch, cool matte basalt palette and nominal 0.9 m scale; not a precise site, eruption stage, cooling history or flow-rate reconstruction. No image textures, detached ropes, pillow stack or seamless-tiling claim.','zh':'地质形态艺术概念：单一封闭连续壳体，以顺共同流向弯曲的圆润褶皱与次级舌状流前缘表现层次。原创截取片段，冷灰哑光玄武岩色系，0.9米为名义艺术尺度；不主张精确地点、喷发阶段、冷却历史或流速。不使用图像贴图，不堆放独立绳条或枕状块，不宣称无缝平铺。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Pāhoehoe-inspired continuous ropy lava crust','zh':'绳状熔岩连续壳面'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
