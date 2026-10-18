# SPDX-License-Identifier: MIT
"""Original deterministic batch22 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 calyx=Part('one-continuous-five-sepal-preserved-calyx-with-shallow-cup',m);veins=Part('restrained-original-primary-sepal-veins',m);n=128;nr=14;v=[];f=[];mi=[]
 def radius(a):return .021+.0115*((.5+.5*math.cos(5*a))**1.35)
 def point(a,t,top=True):
  r=radius(a)*t;z=.003+.0055*(1-math.exp(-(r/.008)**2))+.0011*math.cos(5*a+.10)*t*t+.0003*math.sin(3*a)*t
  if not top:z-=.00095+.0002*t
  return Vector((r*math.cos(a),r*math.sin(a),z))
 for top in [True,False]:
  for j in range(1,nr+1):
   t=j/nr
   for k in range(n):v.append(tuple(point(k*2*pi/n,t,top)))
  v.append((0,0,.003 if top else .00205))
 size=nr*n+1
 for side in range(2):
  off=side*size;center=off+nr*n
  for k in range(n):f.append((center,off+k,off+(k+1)%n));mi.append(1)
  for j in range(nr-1):
   for k in range(n):f.append((off+j*n+k,off+j*n+(k+1)%n,off+(j+1)*n+(k+1)%n,off+(j+1)*n+k));mi.append(0)
 for k in range(n):f.append(((nr-1)*n+k,(nr-1)*n+(k+1)%n,size+(nr-1)*n+(k+1)%n,size+(nr-1)*n+k));mi.append(0)
 calyx.add(v,f,mi);obj=calyx.finish(c,True)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()
 for j in range(5):
  a=j*2*pi/5;pts=[point(a,t)+Vector((0,0,.00009)) for t in [.18,.35,.55,.75,.96]];curve_tube(veins,pts,.00020,.00008,2,6,3)
  for sign in [-1,1]:
   pts=[point(a,.48),point(a+sign*.12,.60),point(a+sign*.20,.73)];pts=[q+Vector((0,0,.00008)) for q in pts];curve_tube(veins,pts,.00011,.00004,2,5,3)
 veins.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='florissantia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='florissantia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B3A78D', '#A4967A', '#958E74'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'preserved terrestrial botanical calyx organ teaching specimen; no complete parent plant or marine vegetation','habitat_zh':'保存的陆地植物萼器官教学标本；非完整母株或海洋植被','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Fossil-specimen / specimen scope only: five broad partially joined sepals, a shallow central cup and restrained major veins. No inferred corolla, stamen array, stem-root system or whole mother plant. Nominal span, muted fossil palette and gentle three-dimensional thickness are artistic; not a measured replica or modern five-petal flower.','zh':'仅 fossil-specimen / specimen 范围：五枚宽大部分连合的萼片、浅中央杯与克制主脉。不推测完整花冠、雄蕊阵列、茎根或母株。名义跨度、化石配色和轻微三维厚度为美术选择，非实测复制品或现代五瓣花。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Florissantia-inspired five-sepal preserved calyx organ','zh':'受 Florissantia 启发的五萼保存花器官'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
