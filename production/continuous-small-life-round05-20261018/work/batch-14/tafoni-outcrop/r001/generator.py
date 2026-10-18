# SPDX-License-Identifier: MIT
"""Original deterministic batch14 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def clip(poly,a,b,cc):
 out=[]
 for i,p in enumerate(poly):
  q=poly[(i+1)%len(poly)];dp=a*p[0]+b*p[1]-cc;dq=a*q[0]+b*q[1]-cc
  if dp<=1e-10:out.append(p)
  if (dp<0)!=(dq<0):
   t=dp/(dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
 return out

def generate(c,m):
 # A single closed original outcrop. Shared polygon ribs surround unequal rounded pockets.
 outline=[(-.45,.015),(.45,.015),(.43,.30),(.26,.56),(-.08,.64),(-.36,.48),(-.44,.26)]
 seeds=[(-.32,.12),(-.13,.11),(.13,.12),(.33,.12),(-.31,.31),(-.075,.31),(.17,.34),(.33,.30),(-.19,.49),(.065,.51),(.23,.48)]
 rock=Part('continuous-weathered-rock-ribs-and-rounded-recesses',m);boundary={}
 for j,(cx,cz) in enumerate(seeds):
  poly=outline[:]
  for k,(qx,qz) in enumerate(seeds):
   if k!=j:poly=clip(poly,2*(qx-cx),2*(qz-cz),qx*qx+qz*qz-cx*cx-cz*cz)
  # Sampling each straight shared edge identically allows welding adjacent rib boundaries.
  outer=[]
  for k,p0 in enumerate(poly):
   p1=poly[(k+1)%len(poly)]
   for h in range(5):t=h/5;outer.append((p0[0]*(1-t)+p1[0]*t,p0[1]*(1-t)+p1[1]*t))
  n=len(outer);v=[];f=[];mi=[];depth=.095+.035*((j*7)%4);rx=.060+.012*(j%3);rz=.050+.015*((j+1)%3)
  for ring in range(8):
   # Outer angular cell melts into rounded lip, deep wall and closed dished floor.
   t=ring/7
   for x,z in outer:
    a=math.atan2(z-cz,x-cx);distance=math.hypot(x-cx,z-cz);ellipse=1/math.sqrt((math.cos(a)/rx)**2+(math.sin(a)/rz)**2);radius=min(ellipse,distance*.80);circx=cx+radius*math.cos(a);circz=cz+radius*math.sin(a)
    if ring==0:xx,zz=x,z;yy=-.13+.015*math.sin(x*5+z*4)
    elif ring==1:xx=x*.20+circx*.80;zz=z*.20+circz*.80;yy=-.139+.009*math.sin(a*3+j)
    else:
     rad=[1,.95,.83,.64,.40,.15][ring-2];xx=cx+(circx-cx)*rad;zz=cz+(circz-cz)*rad;yy=-.13+depth*math.sin((ring-2)/5*pi/2)
    v.append((xx,yy,zz))
  for h in range(7):
   for k in range(n):f.append((h*n+k,h*n+(k+1)%n,(h+1)*n+(k+1)%n,(h+1)*n+k));mi.append(0 if h<2 else (1 if h<5 else 2))
  center=len(v);v.append((cx,-.13+depth,cz))
  for k in range(n):f.append(((7*n)+k,(7*n)+(k+1)%n,center));mi.append(2)
  rock.add(v,f,mi)
  for k,p0 in enumerate(outer):
   p1=outer[(k+1)%n];key=tuple(sorted([(round(p0[0],7),round(p0[1],7)),(round(p1[0],7),round(p1[1],7))]));boundary[key]=boundary.get(key,0)+1
 # Wrap all exterior front edges around a quieter rounded back, keeping the rock solid.
 for (p0,p1),count in boundary.items():
  if count!=1:continue
  # Internal boundaries repeat; exterior edges lie on the supplied convex outline.
  def exterior(pt):
   return any(abs((outline[(i+1)%len(outline)][0]-p[0])*(pt[1]-p[1])-(outline[(i+1)%len(outline)][1]-p[1])*(pt[0]-p[0]))<1e-6 for i,p in enumerate(outline))
  if not(exterior(p0) and exterior(p1)):continue
  verts=[]
  for x,z in [p0,p1]:
   verts += [(x,-.13+.015*math.sin(x*5+z*4),z),(x*.97,.08,z*.98+.004),(x*.85,.19,z*.84+.035)]
  rock.add(verts,[(0,1,4,3),(1,2,5,4)],0)
  rock.add([verts[2],verts[5],(0,.205,.28)],[(0,1,2)],0)
 obj=rock.finish(c,True)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='tafoni-outcrop');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='tafoni-outcrop';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B09A7C', '#A28B6D', '#927C61'])];generate(c,m)
 if s!='cobbania':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'exposed weathered rock teaching face; no exact ancient site, age or salinity mechanism claim','habitat_zh':'风化岩体教学露面；不主张精确古地点、年代或盐度成因','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, posture, simplified counts and fine relief are artistic. Original geometry only; no exact species/specimen, microscopic, locality, salinity or coexistence restoration. Cobbania mounts at the freshwater waterline with roots below it.','zh':'名义尺度、配色、姿态、简化数量及细小起伏为美术选择。仅含原创几何；不主张精确物种标本、显微结构、地点、耐盐性或共存复原。Cobbania 以淡水水面挂点为原点，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Tafoni rounded-cavity weathered outcrop','zh':'蜂窝风化圆穴岩体'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH14_COMPLETE',s)
if __name__=='__main__':main()
