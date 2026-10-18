# SPDX-License-Identifier: MIT
"""Original deterministic batch19 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 rock=Part('continuous-bedrock-surface-with-deep-rounded-pothole-wall-and-floor',m);n=128;cx=.045;cy=.012
 outline=[(-.40,-.25),(-.31,-.32),(.27,-.31),(.40,-.20),(.39,.21),(.26,.32),(-.29,.31),(-.40,.16)]
 def cross(a,b):return a[0]*b[1]-a[1]*b[0]
 def distance(a):
  d=(math.cos(a),math.sin(a));ts=[]
  for i,p in enumerate(outline):
   q=outline[(i+1)%len(outline)];e=(q[0]-p[0],q[1]-p[1]);v=(p[0]-cx,p[1]-cy);den=cross(d,e)
   if abs(den)>1e-10:
    t=cross(v,e)/den;u=cross(v,d)/den
    if t>0 and 0<=u<=1:ts.append(t)
  return min(ts)
 def surface(x,y):return .292+.024*x+.008*math.sin(x*8+y*3)+.003*math.cos(y*12)
 profiles=[]
 for t in [1,.86,.70,.54,.38,.24,.12,0]:profiles.append(('top',t,0))
 keys=[(.156,.292),(.151,.280),(.145,.255),(.143,.220),(.140,.165),(.132,.105),(.116,.057),(.080,.035),(.040,.028)]
 for j in range(len(keys)-1):
  for h in range(1,3):
   t=h/2;r=keys[j][0]*(1-t)+keys[j+1][0]*t;z=keys[j][1]*(1-t)+keys[j+1][1]*t;profiles.append(('wall',r,z))
 v=[];f=[];mi=[]
 for kind,t,z in profiles:
  for k in range(n):
   a=k*2*pi/n
   if kind=='top':
    rr=distance(a)*t+.156*(1-t);x=cx+rr*math.cos(a);y=cy+rr*math.sin(a);zz=surface(x,y)
   else:
    flute=.0035*math.sin(3*a+z*15)*math.sin(pi*max(0,min(1,(z-.028)/.264)));rr=t*(1+.018*math.cos(3*a))+flute;x=cx+rr*math.cos(a);y=cy+rr*math.sin(a);zz=z+(surface(cx+.156*math.cos(a),cy+.156*math.sin(a))-.292)*max(0,(z-.22)/.072)
   v.append((x,y,zz))
 for j in range(len(profiles)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(0 if j<7 else 1)
 floor=len(v);v.append((cx,cy,.025))
 for k in range(n):f.append(((len(profiles)-1)*n+k,(len(profiles)-1)*n+(k+1)%n,floor));mi.append(1)
 # Exterior sides and sealed underside preserve an actual finite rock volume below the cavity floor.
 outerbottom=[]
 for k in range(n):
  a=k*2*pi/n;rr=distance(a);outerbottom.append(len(v));v.append((cx+rr*.98*math.cos(a),cy+rr*.98*math.sin(a),0))
 bottom=len(v);v.append((0,0,0))
 for k in range(n):
  kk=(k+1)%n;f.extend([(k,outerbottom[k],outerbottom[kk],kk),(outerbottom[k],bottom,outerbottom[kk])]);mi.extend([2,2])
 rock.add(v,f,mi);obj=rock.finish(c,True)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()
 for face in obj.data.polygons:
  if face.material_index==2:face.use_smooth=False
 pebble=Part('one-quiet-rounded-clast-on-visible-pothole-floor',m);pebble.ellipsoid((cx+.013,cy-.015,.042),(.024,.020,.015),0,20,12);pebble.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='bedrock-pothole');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='bedrock-pothole';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#A5A38F', '#999B88', '#858A7A'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'exposed freshwater streambed erosion teaching patch; no exact ancient site or flow-rate claim','habitat_zh':'裸露淡水河床侵蚀教学地块；不主张精确古地点或流速','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Original continuous bedrock volume with a deep rounded cavity, gently fluted wall, closed floor and one simplified rounded clast. Nominal dimensions, rock palette and cut outline are artistic. Actual geometry, not a painted dark circle; no arbitrary seamless tiling or exact paleo-river reconstruction.','zh':'原创连续基岩体具有深圆穴、轻微沟纹侧壁、封闭底面与一枚简化圆砾。名义尺寸、岩石配色和裁切边界为美术选择。孔穴使用真实几何，非黑圆贴画；不承诺任意无缝拼接或精确古河床复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Bedrock pothole with geometric wall and floor','zh':'具有真实侧壁与底面的河床壶穴'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
