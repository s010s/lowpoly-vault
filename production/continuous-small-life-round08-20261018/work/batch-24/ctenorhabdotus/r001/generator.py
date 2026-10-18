# SPDX-License-Identifier: MIT
"""Original deterministic batch24 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 def radius(z):
  t=max(0,min(1,(z-.003)/.050));return .0105+.0120*(math.sin(pi*t)**.65)
 def point(a,z,off=0):
  rr=radius(z)+off;return (rr*math.cos(a),rr*.90*math.sin(a),z)
 body=Part('short ovoid barrel with flattened oral and aboral poles',m);n=64;nr=29;v=[];f=[]
 for j in range(nr):
  z=.003+.050*j/(nr-1)
  for k in range(n):v.append(point(2*pi*k/n,z))
 for j in range(nr-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 f.extend([tuple(reversed(range(n))),tuple((nr-1)*n+k for k in range(n))]);body.add(v,f,0);body.finish(c,True)
 bands=Part('eight convergent sets of three comb bands',m);combs=Part('simplified broad comb plate rhythm',m)
 for group in range(8):
  base=2*pi*group/8
  for lane in [-1,0,1]:
   lo,hi=(.009,.050) if lane else (.019,.041);count=15 if lane else 9;pts=[]
   for j in range(count):
    z=lo+(hi-lo)*j/(count-1);t=(z-.003)/.050;a=base+lane*(.22*(1-t)+.040);pts.append(point(a,z,-.00012))
   bands.tube(pts,[.00039]*len(pts),1,n=6)
   for j in range(9 if lane else 5):
    z=lo+.002+(hi-lo-.004)*j/(8 if lane else 4);t=(z-.003)/.050;a=base+lane*(.22*(1-t)+.040);center=Vector(point(a,z,.00026));tangent=Vector((-math.sin(a),.90*math.cos(a),0)).normalized();normal=Vector((math.cos(a),math.sin(a),0)).normalized();up=Vector((0,0,1));wid=.00085 if lane else .00065
    outline=[tuple(center-tangent*wid-up*.00032),tuple(center+tangent*wid-up*.00032),tuple(center+tangent*(wid*.87)+up*.00032),tuple(center-tangent*(wid*.87)+up*.00032)];combs.sheet(outline,.00038,2,axis=tuple(normal))
  strand=[point(base,.048+j*.0007,-.00010) for j in range(8)];bands.tube(strand,[.00048]*8,1,n=7)
 bands.finish(c,True);combs.finish(c,True)
 cap=Part('subtle aboral capsule and oral margin',m);cap.ellipsoid((0,0,.0535),(.0033,.0033,.0015),1,20,8)
 pts=[]
 for k in range(65):
  a=2*pi*k/64;pts.append((.01055*math.cos(a),.0095*math.sin(a),.0035+.00040*math.sin(8*a)))
 cap.tube(pts,[.00038]*len(pts),1,n=7);cap.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='ctenorhabdotus');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='ctenorhabdotus';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#94ABA7', '#7F9D97', '#A7BBB0'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine water-column teaching reconstruction','habitat_zh':'寒武纪海洋水体教学复原','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living whole-organism interpretation: short ovoid barrel with relatively flat poles, eight groups of three broad comb bands, shorter middle bands and converging aboral strands, plus a small conservative aboral capsule. Repeated broad plates express coarse hierarchy without microscopic cilia. Opaque muted sea-green palette and nominal 0.055 m height are artistic choices. No jellyfish bell, tentacle curtain, feeding mechanism, transparency physics or exact preserved cell-count claim. Closed comb parts sit partly embedded in the continuous body surface.','zh':'原创全身生活复原：两端较平的短卵桶体、八组三联宽栉带、较短中央列与向反口端会聚的条带，并保守表现小型反口端囊状结构。重复宽片只表达粗层次，不表现微纤毛。不透明柔和海绿色与0.055米名义高度为艺术设定。不添加水母钟体或触手幕，不主张摄食机制、透明体物理或精确保存细胞数量。封闭栉片局部嵌入连续体表。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Ctenorhabdotus-inspired many-combed barrel ctenophore','zh':'Ctenorhabdotus 多栉列桶形栉水母'},'prehistoric-animal',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH24_COMPLETE',s)
if __name__=='__main__':main()
