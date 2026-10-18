# SPDX-License-Identifier: MIT
"""Original low massive polygon-cup coral; deterministic Blender4.3.2."""
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
 outline=[(.09*math.cos(k*2*pi/16),.072*math.sin(k*2*pi/16)) for k in range(16)]
 seeds=[(-.052,-.035),(-.015,-.045),(.029,-.038),(.061,-.017),(-.066,.003),(-.026,-.003),(.013,.001),(.052,.025),(-.043,.037),(-.006,.038),(.025,.050),(-.070,-.023)]
 part=Part('continuous-low-massive-colony-with-shared-polygon-cup-walls',m)
 def top(x,y):return .024+.021*max(0,1-(x/.092)**2-(y/.075)**2)
 exterior_edges=[]
 for j,(cx,cy) in enumerate(seeds):
  poly=outline[:]
  for k,(qx,qy) in enumerate(seeds):
   if k!=j:poly=clip(poly,2*(qx-cx),2*(qy-cy),qx*qx+qy*qy-cx*cx-cy*cy)
  outer=[]
  for k,p0 in enumerate(poly):
   p1=poly[(k+1)%len(poly)]
   for h in range(8):t=h/8;outer.append((p0[0]*(1-t)+p1[0]*t,p0[1]*(1-t)+p1[1]*t))
  n=len(outer);v=[];f=[];mi=[]
  for ring,rad in enumerate([1,.94,.82,.65,.45,.25,.09]):
   for x,y in outer:
    xx=cx+(x-cx)*rad;yy=cy+(y-cy)*rad;a=math.atan2(y-cy,x-cx);depth=.012*(1-rad)**.65;septa=.004*max(0,math.cos(12*a+j*.1))**2*math.sin(pi*(1-rad))**.55
    zz=top(xx,yy)-depth+septa;v.append((xx,yy,zz))
  for h in range(6):
   for k in range(n):f.append((h*n+k,h*n+(k+1)%n,(h+1)*n+(k+1)%n,(h+1)*n+k));mi.append(0 if h==0 else 1)
  center=len(v);v.append((cx,cy,top(cx,cy)-.012))
  for k in range(n):f.append((6*n+k,6*n+(k+1)%n,center));mi.append(2)
  part.add(v,f,mi)
  for k,p0 in enumerate(outer):
   p1=outer[(k+1)%n]
   def is_boundary(pt):return any(abs((outline[(i+1)%len(outline)][0]-q[0])*(pt[1]-q[1])-(outline[(i+1)%len(outline)][1]-q[1])*(pt[0]-q[0]))<1e-9 for i,q in enumerate(outline))
   if is_boundary(p0) and is_boundary(p1):
    a=Vector((p0[0],p0[1],top(*p0)));bb=Vector((p1[0],p1[1],top(*p1)));v=[tuple(a),tuple(bb),(p1[0]*1.015,p1[1]*1.015,.005),(p0[0]*1.015,p0[1]*1.015,.005),(p1[0]*.90,p1[1]*.90,0),(p0[0]*.90,p0[1]*.90,0),(0,0,0)]
    part.add(v,[(0,3,2,1),(3,5,4,2),(5,6,4)],0)
 obj=part.finish(c,True)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='isastraea');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='isastraea';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.83) for i,color in enumerate(['#8C9C8B','#A4B09B','#8E9E88'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'marine low massive colonial coral; no exact depth/locality/coexistence claim','habitat_zh':'海生低块状群体珊瑚；不主张精确水深、地点或共存','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Original shared-wall polygonal cups and radial septal relief. Stable inventory spelling isastraea retained; sources also use Isastrea. Nominal scale, cup/septum counts, palette and simplified relief are artistic; not a strict species/specimen reconstruction.','zh':'原创相接多边杯与星隔浮雕。保留原清单稳定ID isastraea，来源亦使用 Isastrea 拼写。名义尺度、杯与隔壁数量、配色和简化起伏为美术选择，非严格物种或标本复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Isastraea-inspired low polygon-cup reef coral','zh':'受 Isastraea 启发的低块多边星隔杯珊瑚'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH17_COMPLETE',s)
if __name__=='__main__':main()
