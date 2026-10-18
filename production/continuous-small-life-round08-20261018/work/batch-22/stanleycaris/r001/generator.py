# SPDX-License-Identifier: MIT
"""Original deterministic batch22 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 body=Part('soft segmented trunk',m);v=[];f=[];n=28;nr=69
 # Closed elliptical trunk, rounded taper; shallow annulations follow a continuous body.
 for j in range(nr):
  t=j/(nr-1);y=-.026+.072*t;rad=.0011+.0062*(math.sin(pi*t)**.65)*(1-.38*t)
  rad*=1-.035*math.cos(2*pi*17*t)
  for k in range(n):
   a=2*pi*k/n;v.append((rad*math.cos(a),y,.010+rad*.70*math.sin(a)))
 for j in range(nr-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 f.extend([tuple(reversed(range(n))),tuple((nr-1)*n+k for k in range(n))]);body.add(v,f,0);body.finish(c,True)
 h=Part('short soft head and small domed anterior plate',m)
 h.ellipsoid((0,-.027,.011),(.0083,.012,.0056),0,24,12)
 h.ellipsoid((0,-.033,.0157),(.0085,.0087,.0026),1,28,10)
 h.ellipsoid((0,-.033,.0062),(.0036,.004,.0012),3,16,6);h.finish(c,True)
 fins=Part('seventeen paired swimming flaps',m)
 for j in range(17):
  t=j/16;y=-.020+.062*t;root=.0049*(1-.48*t);span=.0075*(math.sin(pi*(.10+.83*t))**.65)*(1-.38*t)
  for sign in [-1,1]:
   # Flattened gently curved leaf flaps, wide overlapping root within trunk.
   out=[(sign*(root-.0026),y-.0025,.0095),(sign*(root+.0017),y-.0024,.0092),(sign*(root+span),y+.0005,.0072),(sign*(root+span*.82),y+.0033,.0069),(sign*(root+.001),y+.0026,.0090)]
   fins.sheet(out,.00058,1,axis=(0,0,1))
 o=fins.finish(c,True)
 eyes=Part('three eyes with embedded stalk roots',m)
 for sign in [-1,1]:
  curve_tube(eyes,[(sign*.0056,-.028,.0135),(sign*.0097,-.031,.0157),(sign*.014,-.033,.0169)],.00145,.00115,0,10,3)
  eyes.ellipsoid((sign*.0148,-.0339,.0173),(.0034,.0041,.0028),3,20,10)
 eyes.ellipsoid((0,-.0212,.0171),(.0031,.0035,.0021),3,24,10);eyes.finish(c,True)
 arms=Part('paired curved rake appendages',m)
 for sign in [-1,1]:
  curve_tube(arms,[(sign*.0055,-.033,.010),(sign*.009,-.041,.008),(sign*.010,-.050,.009),(sign*.0075,-.057,.012)],.0024,.00065,2,12,5)
  for j in range(5):
   y=-.041-.0027*j;x=.009+.0006*math.sin(j*pi/4)
   curve_tube(arms,[(sign*x,y,.0086),(sign*(x-.0021),y-.001,.0063),(sign*(x-.0044),y-.0027,.0069)],.00072,.00018,2,8,3)
 arms.finish(c,True)
 tails=Part('four delicate caudal blades',m)
 for j,(xend,yend) in enumerate([(-.0135,.067),(-.005,.073),(.005,.073),(.0135,.067)]):
  xr=(-.0018 if xend<0 else .0018);pts=catmull([(xr,.041,.010),(xend*.48,.053,.0085),(xend,yend,.008)],5)
  # Filiform tail blades retain a visible flattened, gently tapering profile.
  for k in range(len(pts)-1):
   a=Vector(pts[k]);bb=Vector(pts[k+1]);wd=.00090*(1-k/len(pts))+.00013
   tails.sheet([tuple(a+Vector((-wd,0,0))),tuple(bb+Vector((-wd*.87,0,0))),tuple(bb+Vector((wd*.87,0,0))),tuple(a+Vector((wd,0,0)))],.00036,2,axis=(0,0,1))
 tails.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='stanleycaris');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='stanleycaris';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#7F8E86', '#95A198', '#A6A28A', '#35483C'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Cambrian marine water-column and near-seabed teaching reconstruction','habitat_zh':'寒武纪海洋水体及近海底教学复原','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Original living whole-organism interpretation: small domed anterior head plate, a large median eye behind it, paired stalked lateral eyes, long segmented trunk, paired swimming flaps, rake-like frontal appendages and four filamentous tail blades. Nominal art proportions and colors; no brain, gill microstructure or exact spine-tooth counts claimed. Soft closed parts deliberately overlap at organic roots; no detached appendage placement.','zh':'原创全身生活复原：小型前部拱头甲、位于甲后的中央眼、两侧具柄眼、细长分节躯干、成对游泳瓣、耙状前附肢与四条丝状尾叶。尺寸比例及色彩为艺术设定；不复原脑或鳃微观结构，不主张精确刺齿数。封闭软组织部件在根部有意交叠连接。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Stanleycaris-inspired slender three-eyed radiodont','zh':'史丹利虾属启发的细长三眼放射齿动物'},'prehistoric-animal',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
