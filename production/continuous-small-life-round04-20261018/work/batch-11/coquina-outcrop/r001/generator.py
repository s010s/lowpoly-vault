# SPDX-License-Identifier: MIT
"""Original deterministic batch11 geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import random
 random.seed(2026101813);n=80;nr=36;v=[(0,0,.35)];f=[]
 pores=[(random.uniform(0,2*pi),random.uniform(.25,1.35),random.uniform(.006,.013)) for _ in range(24)]
 def surface(theta,a):
  st=math.sin(theta);co=math.cos(a);si=math.sin(a);z=.175+.175*math.copysign(abs(math.cos(theta))**.65,math.cos(theta));shape=1+.035*math.sin(a*5+theta*3)+.020*math.cos(9*a-2*theta)
  indent=sum(depth*math.exp(-((math.atan2(math.sin(a-pa),math.cos(a-pa))/.09)**2+((theta-pt)/.10)**2)) for pa,pt,depth in pores)
  return Vector(((.4*st**.65*math.copysign(abs(co)**.68,co)-indent*co)*shape,(.275*st**.65*math.copysign(abs(si)**.68,si)-indent*si)*shape,z-indent*.7))
 for j in range(1,nr):
  for k in range(n):v.append(tuple(surface(pi*j/nr,2*pi*k/n)))
 bottom=len(v);v.append((0,0,0))
 for k in range(n):f.append((0,1+k,1+(k+1)%n))
 for j in range(nr-2):
  for k in range(n):a=1+j*n+k;bb=1+j*n+(k+1)%n;f.append((a,a+n,bb+n,bb))
 for k in range(n):f.append((bottom,1+(nr-2)*n+(k+1)%n,1+(nr-2)*n+k))
 matrix=Part('continuous-lithified-porous-shell-rock-matrix',m);matrix.add(v,f,0);matrix.finish(c,True)
 shells=Part('embedded-broken-shell-arcs-and-exposed-cross-sections',m)
 for j in range(70):
  a=2*pi*((j*.61803398875)%1);theta=.22+(j%10)*.13;p=surface(theta,a);normal=(surface(theta,a+.001)-surface(theta,a-.001)).cross(surface(theta+.001,a)-surface(theta-.001,a)).normalized();normal=normal if normal.dot(p-Vector((0,0,.175)))>0 else -normal;u=normal.cross(Vector((0,0,1)))
  if u.length<.1:u=Vector((1,0,0))
  u.normalize();w=normal.cross(u).normalized();angle=j*.83;u,w=u*math.cos(angle)+w*math.sin(angle),-u*math.sin(angle)+w*math.cos(angle)
  radius=.030+.020*((j*7%11)/11);start=-1.2+.25*math.sin(j);end=1.1+.3*math.cos(j);verts=[];steps=10
  # Solid curved ribbon fragment, seated into the matrix rather than a whole shell.
  for depth in [-.006,.002]:
   for rr in [radius*.60,radius]:
    for k in range(steps+1):
     q=start+(end-start)*k/steps;verts.append(tuple(p+u*(rr*math.cos(q))+w*(rr*.65*math.sin(q))+normal*(depth+.002*math.sin(q))))
  L=steps+1;faces=[]
  for k in range(steps):
   faces.extend([(k,k+1,L+k+1,L+k),(2*L+k,3*L+k,3*L+k+1,2*L+k+1),(k,2*L+k,2*L+k+1,k+1),(L+k,L+k+1,3*L+k+1,3*L+k)])
  faces.extend([(0,L,3*L,2*L),(steps,2*L+steps,3*L+steps,L+steps)]);shells.add(verts,faces,1 if j%4 else 2)
 shells.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='coquina-outcrop');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='coquina-outcrop';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B09F81', '#D8C9AB', '#BDA889'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'coastal sedimentary rock concept; not living shells or an exact site','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, color, pose and repeated detail counts are artistic choices; no exact species/specimen/coexistence reconstruction. Original geometry only.','zh':'名义尺度、颜色、姿态及细小重复结构数量为美术选择；不主张精确物种、标本或同域共存复原。仅含原创几何。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Stylized lithified coquina outcrop','zh':'风格化固结贝壳灰岩露头'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH11_COMPLETE',s)
if __name__=='__main__':main()
