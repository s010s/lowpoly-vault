# SPDX-License-Identifier: MIT
"""Original deterministic batch19 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def shield_mesh(c,m):
 # Explicit concave outline: rounded front, swept rear wings, two deep ocular notches, bilobed rear middle.
 right=[(0,-.050),(.023,-.047),(.044,-.035),(.057,-.018),(.061,.004),(.060,.029),(.052,.050),(.044,.042),(.037,.018),(.031,.011),(.025,.014),(.020,.029),(.018,.040),(.009,.043),(0,.037)]
 outline=right+[(-x,y) for x,y in reversed(right[1:-1])];poly=[Vector((x,y,0)) for x,y in outline];part=Part('domed-horseshoe-shield-with-deep-ocular-notches',m)
 from mathutils.geometry import tessellate_polygon
 tris=tessellate_polygon([poly]);N=6
 def surf(x,y,top):return (x,y,(.012+.011*math.exp(-((x/.043)**2+((y+.012)/.049)**2))) if top else .008)
 for tri in tris:
  aa,bb,cc=[poly[t] if isinstance(t,int) else t for t in tri]
  for top in [True,False]:
   v=[];idx={};f=[]
   for i in range(N+1):
    for j in range(N+1-i):
     point=aa+(bb-aa)*(i/N)+(cc-aa)*(j/N);idx[i,j]=len(v);v.append(surf(point.x,point.y,top))
   for i in range(N):
    for j in range(N-i):
     f.append((idx[i,j],idx[i+1,j],idx[i,j+1]))
     if i+j<N-1:f.append((idx[i+1,j],idx[i+1,j+1],idx[i,j+1]))
   part.add(v,f,0 if top else 2)
 for i,p0 in enumerate(outline):
  p1=outline[(i+1)%len(outline)]
  for j in range(N):
   t=j/N;tt=(j+1)/N;x=p0[0]*(1-t)+p1[0]*t;y=p0[1]*(1-t)+p1[1]*t;xx=p0[0]*(1-tt)+p1[0]*tt;yy=p0[1]*(1-tt)+p1[1]*tt
   part.add([surf(x,y,True),surf(xx,yy,True),surf(xx,yy,False),surf(x,y,False)],[(0,1,2,3)],1)
 obj=part.finish(c,True)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()

def paddle(part,a,b,width,mi):
 a=Vector(a);b=Vector(b);d=(b-a).normalized();u=Vector((-d.y,d.x,0)).normalized();mid=(a+b)*.5;part.sheet([tuple(a),tuple(mid+u*width),tuple(b),tuple(mid-u*width)],.00065,mi,(0,0,1))

def generate(c,m):
 shield_mesh(c,m);body=Part('short-stout-soft-body-beneath-large-shield',m);flaps=Part('short-lateral-swimming-flaps-and-four-tail-blades',m);rakes=Part('paired-underhead-rake-appendages-simplified-inner-spines',m);eyes=Part('upward-elliptical-eyes-in-rear-notches',m);underside=Part('conservative-ventral-paddle-plates-and-mouth',m)
 n=24;nr=44;v=[];f=[]
 for j in range(nr+1):
  t=j/nr;r=.001+.010*math.sin(pi*(.06+.88*t))**.65*(1+.04*math.cos(t*22*pi));yy=.003+.052*t
  for k in range(n):a=k*2*pi/n;v.append((r*math.cos(a),yy,.0065+r*.54*math.sin(a)))
 f=[tuple(reversed(range(n)))]+[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(nr) for k in range(n)]+[tuple(nr*n+k for k in range(n))];body.add(v,f,2)
 for side in [-1,1]:
  for j in range(11):
   y=.007+j*.0042;w=.0065*(1-j*.025);paddle(flaps,(side*.005,y,.0045),(side*(.0145-.00025*j),y+.0038,.0035),w*.40,2)
  for j in range(2):paddle(flaps,(side*.003,.050,.006),(side*(.006+j*.004),.063-j*.003,.004),.0025,2)
  # Paired ventral head plates narrow together at the front; no crab walking legs added.
  paddle(underside,(side*.004,-.035,.0045),(side*.014,.001,.004),.0055,2)
  curve_tube(rakes,[(side*.010,-.021,.004),(side*.023,-.034,.0015),(side*.023,-.048,.001)],.0022,.0012,3,10,5)
  for j in range(5):
   y=-.030-j*.0042;x=side*(.020+.002*math.sin(j));curve_tube(rakes,[(x,y,.0018),(x-side*.004,y-.002,-.001),(x-side*(.009+.001*j),y-.003,-.0015),(x-side*(.011+.0005*j),y-.001,0)],.00065,.00015,3,7,3)
  curve_tube(eyes,[(side*.016,.011,.009),(side*.024,.018,.012),(side*.029,.023,.013)],.0015,.0011,2,8,3)
  eyes.ellipsoid((side*.029,.023,.014),(.0041,.0054,.0024),4,24,12)
  for j in range(3):
   y=.006+j*.009;curve_tube(rakes,[(side*.060,y,.012),(side*.063,y+.001,.012),(side*.064,y+.002,.011)],.00055,.00008,0,6,2)
 underside.ellipsoid((0,-.028,.003),(.004,.004,.0015),4,24,12)
 for part in [body,flaps,rakes,eyes,underside]:
  obj=part.finish(c,True)
  import bmesh
  bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cambroraster');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cambroraster';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#AD9D81', '#C0AE90', '#8F9985', '#ACAA89', '#414D43'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'marine near-bottom radiodont teaching concept; no exact coexistence or locomotion claim','habitat_zh':'海生近底奇虾类教学概念；不主张精确共存或运动机制','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Broad original horseshoe shield has swept rear wings, a bilobed center and deep notches with upward eyes. Short soft body, lateral flaps and paired rake appendages are original simplified geometry; fine filter/spine/segment counts, palette, nominal size and pose are artistic. Not a crab recolor, exact species/specimen or animated feeding reconstruction.','zh':'原创宽马蹄甲保留后掠侧翼、双叶后中部和容纳向上眼的深切口。短软躯体、侧游泳瓣及成对耙状前附肢均为原创简化几何；细滤刺/体节数量、配色、名义尺寸和姿态属美术选择，非蟹换色、精确物种标本或取食动画复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Cambroraster-inspired horseshoe-shield radiodont','zh':'受 Cambroraster 启发的马蹄甲奇虾类'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
