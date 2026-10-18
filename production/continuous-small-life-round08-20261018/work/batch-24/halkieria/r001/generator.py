# SPDX-License-Identifier: MIT
"""Original deterministic batch24 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 body=Part('elongated flattened soft mantle and sole',m);body.ellipsoid((0,0,.0060),(.0105,.035,.0053),0,36,14);body.ellipsoid((0,0,.0031),(.0100,.0335,.0025),0,32,10);body.finish(c,True)
 shells=Part('distinct anterior and posterior cap shells',m)
 for yy,sx,sy,h in [(-.023,.0089,.0096,.0055),(.0238,.0081,.0091,.0045)]:
  n=36;nr=8;v=[(0,yy-.001,.012+h)];f=[]
  for j in range(1,nr+1):
   t=j/nr
   for k in range(n):
    a=2*pi*k/n;z=.0100+h*(1-t*t)**.75
    v.append((sx*t*math.cos(a),yy+sy*t*math.sin(a)-.001*(1-t),z))
  for k in range(n):f.append((0,1+k,1+(k+1)%n))
  for j in range(nr-1):
   for k in range(n):a=1+j*n+k;bb=1+j*n+(k+1)%n;f.append((a,bb,bb+n,a+n))
  center=len(v);v.append((0,yy,.0084))
  for k in range(n):f.append((center,1+(nr-1)*n+(k+1)%n,1+(nr-1)*n+k))
  shells.add(v,f,1)
  for rr in [.66,.88]:
   pts=[]
   for k in range(37):
    a=2*pi*k/36;pts.append((sx*rr*math.cos(a),yy+sy*rr*math.sin(a)-.001*(1-rr),.0100+h*(1-rr*rr)**.75+.00005))
   shells.tube(pts,[.00014]*len(pts),2,n=5)
 shells.finish(c,True)
 armor=Part('ordered overlapping dorsal armour zones',m)
 for j in range(12):
  y=-.019+.0034*j
  for col,xx in enumerate([-.0080,-.0044,0,.0044,.0080]):
   z=.006+.0053*math.sqrt(max(.05,1-(xx/.0105)**2-(y/.035)**2));cx=xx;cy=y+(.001 if col%2 else 0)
   # Leaf-like closed shallow plates; soft lower roots overlap mantle.
   outline=[(-.0017,-.0016),(-.0018,.0002),(-.0010,.0020),(0,.0027),(.0011,.0020),(.0018,.0002),(.0016,-.0016),(0,-.0020)]
   v=[(cx+x,cy+dy,z-.00040) for x,dy in outline]+[(cx+x*.80,cy+dy*.82,z+.00062) for x,dy in outline]+[(cx,cy+.0003,z+.0010)];f=[tuple(reversed(range(8)))]
   for k in range(8):kk=(k+1)%8;f.append((k,kk,8+kk,8+k));f.append((16,8+k,8+kk))
   armor.add(v,f,2 if (j+col)%7 else 1)
 # Short ordered marginal sickle plates, not randomly distributed spikes.
 for sign in [-1,1]:
  for j in range(16):
   y=-.025+.0033*j;x=sign*.0092*math.sqrt(max(.15,1-(y/.035)**2))
   curve_tube(armor,[(x,y,.006),(x+sign*.0019,y+.0004,.0059),(x+sign*.0034,y+.0020,.0051)],.00067,.00018,2,7,2)
 armor.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='halkieria');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='halkieria';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#879588', '#B1AA91', '#A2A58F'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Early Cambrian near-seabed teaching reconstruction','habitat_zh':'早寒武世近海底教学复原','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living whole-organism interpretation: elongated flattened soft mantle and sole, one cap shell near each end, ordered overlapping dorsal armour and short marginal sclerites. Simplified counts and muted green-grey shell colors are artistic choices, not measured fossil evidence. Molluscan-inspired classification is retained; no reptile identity, exact phylogenetic conclusion, mouthparts, locomotor mechanism or microstructure claimed. Closed armour roots intentionally overlap the continuous mantle.','zh':'原创全身生活复原：长扁软体背部与腹足、前后两端各一枚帽壳、有序叠片背甲和短边缘骨片。简化数量及柔和灰绿色配色为美术设定，非化石测量。保留软体动物启发分类，不当作爬行类，不主张精确系统位置、口器、运动机制或微观结构。封闭骨片根部有意嵌入连续外套体。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Halkieria-inspired two-shell armoured crawler','zh':'Halkieria 双壳鳞甲软体爬行动物'},'prehistoric-animal',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH24_COMPLETE',s)
if __name__=='__main__':main()
