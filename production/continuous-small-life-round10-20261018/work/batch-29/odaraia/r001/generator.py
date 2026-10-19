# SPDX-License-Identifier: MIT
"""Original deterministic batch29 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 shell=Part('natural open-ended tubular carapace',m);n=64;nr=21;v=[];f=[];mi=[]
 for inner in [False,True]:
  for j in range(nr):
   t=j/(nr-1);y=-.042+.084*t;rx=.0168*(1-.12*t+.055*math.sin(pi*t));rz=.0118*(1-.10*t+.025*math.sin(pi*t));th=.00085 if inner else 0
   for k in range(n):a=2*pi*k/n;v.append(((rx-th)*math.cos(a),y,.018+(rz-th)*math.sin(a)))
 off=nr*n
 for j in range(nr-1):
  for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.extend([(a,b,b+n,a+n),(off+a,off+a+n,off+b+n,off+b)]);mi.extend([0,1])
 for j in [0,nr-1]:
  for k in range(n):a=j*n+k;b=j*n+(k+1)%n;f.append((a,off+a,off+b,b));mi.append(1)
 shell.add(v,f,mi);shell.finish(c,True)
 trunk=Part('enclosed soft trunk and projecting short head',m);pts=[(0,-.047+.104*j/48,.017) for j in range(49)];r=[(.0048-.0018*j/48)*(1-.035*math.cos(2*pi*18*j/48)) for j in range(49)];trunk.tube(pts,r,2,n=20);trunk.ellipsoid((0,-.047,.018),(.0070,.0080,.0053),2,24,12);trunk.finish(c,True)
 limbs=Part('restrained internal paired paddles',m)
 for j in range(14):
  y=-.032+.065*j/13
  for sign in [-1,1]:
   curve_tube(limbs,[(sign*.0028,y,.015),(sign*.0058,y+.001,.0115),(sign*.009,y+.003,.011)],.00062,.00030,2,7,2)
   limbs.ellipsoid((sign*.009,y+.003,.011),(.0018,.0025,.00045),2,8,4)
 limbs.finish(c,True)
 eyes=Part('proportionate paired large eyes with embedded stalks',m)
 for sign in [-1,1]:
  curve_tube(eyes,[(sign*.004,-.048,.020),(sign*.008,-.053,.021),(sign*.013,-.055,.022)],.0015,.0014,2,10,3)
  eyes.ellipsoid((sign*.0148,-.056,.0227),(.0054,.0052,.0048),3,24,12)
 eyes.finish(c,True)
 tail=Part('connected three-bladed telson',m)
 for sign in [-1,1]:
  out=[(sign*.001,.050,.017),(sign*.007,.053,.0176),(sign*.018,.064,.0178),(sign*.022,.073,.017),(sign*.017,.075,.0168),(sign*.008,.068,.017),(sign*.001,.061,.017)]
  tail.sheet(out,.00105,1,axis=(0,0,1))
 out=[(0,.050,.017),(0,.053,.024),(0,.063,.034),(0,.072,.035),(0,.077,.028),(0,.069,.020),(0,.060,.017)]
 tail.sheet(out,.00110,1,axis=(1,0,0));tail.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='odaraia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='odaraia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#91A299', '#A7B09B', '#7D9387', '#3E5146'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round10-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine teaching reconstruction; no exact swimming or feeding simulation','habitat_zh':'寒武纪海生教学复原；不模拟精确游泳或取食机制','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living whole-organism interpretation: soft internal trunk and short projecting head enclosed by a naturally tapered tube carapace open at both ends, proportionate large paired eyes, simplified internal paddles and a connected telson with two lateral blades plus one vertical blade. Nominal0.1m tube/body scale, muted palette and static pose are art choices. No closed bivalve capsule, lateral long-spine substitute, reused Dollocaris/Isoxys mesh, exact segment/limb count, fine head-organ or swimming-mechanism claim. Closed semantic roots overlap organically while shell apertures remain actual geometry.','zh':'原创全体生活复原：柔软内躯与短前伸头部包于自然渐收、两端开口的筒甲中，具比例克制的大型双眼、简化内侧桨肢，以及两侧各一叶和一片竖叶组成的相连三叶尾。0.1米名义筒甲/体尺度、柔和配色及静姿为美术设定。不做封闭双瓣囊甲或长侧刺替代，不复用Dollocaris/Isoxys网格，不主张精确体节/肢数、细小头器官或游泳机制。封闭语义部件在根部自然交叠，筒甲孔口保留真实几何。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Odaraia-inspired open-tube carapace swimmer','zh':'Odaraia 开口筒甲游泳动物'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH29_COMPLETE',s)
if __name__=='__main__':main()
