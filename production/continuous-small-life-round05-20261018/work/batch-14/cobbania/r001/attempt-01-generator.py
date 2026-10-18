# SPDX-License-Identifier: MIT
"""Original deterministic batch14 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 leaf=Part('three-radially-folded-trumpet-leaves-with-basal-pouches',m);roots=Part('freshwater-hanging-root-fan',m);stem=Part('short-common-floating-axis',m)
 stem.ellipsoid((0,0,-.006),(.009,.009,.011),2,16,8)
 for j,(cx,cy,height,rad,angle) in enumerate([(0,.025,.073,.046,0),(-.039,-.019,.053,.033,-.35),(.035,-.025,.047,.030,.45)]):
  node=Vector((cx,cy,-.005));curve_tube(stem,[(0,0,-.005),(cx*.5,cy*.5,-.008),node],.0035,.003,2,10,4)
  # Closed inner/outer longitudinal profile expresses the swollen basal pouch and leaf funnel.
  profiles=[(-.014,.002),(-.011,.006),(-.005,.009),(.005,.010),(.014,.012),(.024,.018),(.037,.027),(.052,.039),(.062,.046)]
  profiles=[(z*height/.062,rr*rad/.046,False) for z,rr in profiles]
  profiles += [(z*height/.062,rr*rad/.046,True) for z,rr in [(.063,.0445),(.052,.0375),(.037,.0255),(.024,.0165),(.014,.0105),(.006,.0085),(.002,.004)]]
  n=64;v=[];f=[];mi=[]
  for z,rr,inner in profiles:
   for k in range(n):
    a=2*pi*k/n;flute=1+.055*math.cos(a*10+.3*j);notch=math.exp(-((math.atan2(math.sin(a-1.1),math.cos(a-1.1)))/.20)**2);t=max(0,z/height);zz=z-.010*t**4*notch+.0025*math.cos(3*a+j)*t*t
    v.append((cx+rr*math.cos(a)*flute+angle*z,cy+rr*math.sin(a)*flute+.10*z,zz))
  for h in range(len(profiles)-1):
   for k in range(n):f.append((h*n+k,h*n+(k+1)%n,(h+1)*n+(k+1)%n,(h+1)*n+k));mi.append(1 if profiles[h][2] else 0)
  bot=len(v);v.append((cx,cy,-.014*height/.062));center=len(v);v.append((cx,cy,.002*height/.062))
  for k in range(n):f.extend([(bot,(k+1)%n,k),(center,(len(profiles)-1)*n+k,(len(profiles)-1)*n+(k+1)%n)]);mi.extend([2,1])
  leaf.add(v,f,mi)
  for k in range(6):
   a=k*pi/3+j*.4;d=Vector((math.cos(a),math.sin(a),0));length=.045+.018*((j+k)%3)/2;start=node+Vector((0,0,-.007))
   pts=[start,start+d*.004+Vector((0,0,-.015)),start+d*.010+Vector((0,0,-length*.7)),start+d*.017+Vector((0,0,-length))];curve_tube(roots,pts,.0008,.00013,3,7,3)
   if k%3==0:
    for side in [-1,1]:curve_tube(roots,[pts[2],pts[2]+Vector((side*.008,0,-.005)),pts[2]+Vector((side*.013,.001,-.013))],.00028,.00007,3,5,2)
 leaf.finish(c,True);roots.finish(c,True);stem.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cobbania');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cobbania';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#7C9A60', '#91A971', '#718653', '#8F8066'])];generate(c,m)
 if s!='cobbania':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'freshwater floating wetland plant only; never marine seagrass','habitat_zh':'仅用于淡水湿地浮生层；并非海草或海底植被','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, posture, simplified counts and fine relief are artistic. Original geometry only; no exact species/specimen, microscopic, locality, salinity or coexistence restoration. Cobbania mounts at the freshwater waterline with roots below it.','zh':'名义尺度、配色、姿态、简化数量及细小起伏为美术选择。仅含原创几何；不主张精确物种标本、显微结构、地点、耐盐性或共存复原。Cobbania 以淡水水面挂点为原点，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Cobbania-inspired trumpet-leaf floating rosette','zh':'受 Cobbania 启发的喇叭叶浮生莲座'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH14_COMPLETE',s)
if __name__=='__main__':main()
