# SPDX-License-Identifier: MIT
"""Original deterministic batch26 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 girdle=Part('conservative low soft girdle',m);girdle.ellipsoid((0,0,.0060),(.012,.0375,.0057),0,36,14);girdle.finish(c,True)
 plates=Part('serial broad overlapping dorsal plates',m)
 for j in range(8):
  yy=-.029+.0083*j;ww=.0102*(.79+.21*math.sin(pi*(j+.5)/8));length=.0108 if j not in [0,7] else .0117
  # Closed broad arched plate, low posterior apex; continuous natural sequence.
  n=20;v=[];f=[]
  for ring,(sy,sz) in enumerate([(-.48,.0),(.05,.0015),(.47,.0001)]):
   for k in range(n):
    a=2*pi*k/n;v.append((ww*math.cos(a),yy+sy*length+.0005*math.sin(a),.009+sz+.0047*math.sin(a)))
  for h in range(2):
   for k in range(n):f.append((h*n+k,h*n+(k+1)%n,(h+1)*n+(k+1)%n,(h+1)*n+k))
  f.extend([tuple(reversed(range(n))),tuple(2*n+k for k in range(n))]);plates.add(v,f,1 if j%3 else 2)
 plates.finish(c,True)
 spines=Part('large integrated outward lateral spines',m)
 for j in range(1,8):
  yy=-.029+.0083*j
  for sign in [-1,1]:
   pts=catmull([(sign*.0082,yy,.0097),(sign*.0155,yy+.0005,.011),(sign*.023,yy+.003,.0135),(sign*.029,yy+.005,.0145)],4)
   radii=[.0025*(1-k/(len(pts)-1))**1.15+.00032 for k in range(len(pts))]
   # Two restrained blunt tip sections reveal inner space; remaining tips closed.
   if j==4:
    n=12;v=[];frames=[]
    for k,p in enumerate(pts):
     d=Vector(pts[min(k+1,len(pts)-1)])-Vector(pts[max(0,k-1)]);d.normalize();u=d.cross(Vector((0,0,1))).normalized();w=d.cross(u).normalized();frames.append((u,w))
     for h in range(n):a=2*pi*h/n;v.append(tuple(Vector(p)+radii[k]*(u*math.cos(a)+w*math.sin(a))))
    off=len(v)
    for k,p in enumerate(pts):
     u,w=frames[k]
     for h in range(n):a=2*pi*h/n;v.append(tuple(Vector(p)+radii[k]*.54*(u*math.cos(a)+w*math.sin(a))))
    f=[];mi=[]
    for k in range(len(pts)-1):
     for h in range(n):hh=(h+1)%n;a=k*n+h;b=k*n+hh;f.extend([(a,b,b+n,a+n),(off+a,off+a+n,off+b+n,off+b)]);mi.extend([2,3])
    for k in [0,len(pts)-1]:
     for h in range(n):hh=(h+1)%n;a=k*n+h;b=k*n+hh;f.append((a,off+a,off+b,b));mi.append(2)
    spines.add(v,f,mi)
   else:spines.tube(pts,radii,2,n=12)
 # Tail spines emerge from the posterior plate, not an isolated extra object.
 for sign in [-1,1]:curve_tube(spines,[(sign*.004,.029,.0095),(sign*.007,.038,.011),(sign*.010,.044,.013)],.0021,.00035,2,10,4)
 spines.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='echinochiton');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='echinochiton';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#87978A', '#A8AD98', '#B7B098', '#6D786D'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Biome unspecified in original inventory; no coexisting habitat asserted','habitat_zh':'原始biomes未指定；不主张特定共存生境','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living whole-organism teaching interpretation: serial overlapping dorsal plates with integrated large lateral spines and conservative low soft girdle. Two restrained blunt-tip sections hint at hollow spines; no microscopic bone/scute counts, complete soft anatomy, exact fossil measurement or locomotor mechanism claimed. Muted palette, nominal 0.075 m body length and limited rounding are art choices. Original inventory biomes remains an empty array, not a universal habitat statement.','zh':'原创全体教学生活复原：连续叠覆背板、自然连接的大侧刺与保守低矮软质外套缘。两处克制钝端剖口提示刺内部空间，不主张微观骨片数、完整软组织、精确化石尺寸或运动机制。柔和配色、0.075米名义体长与圆润程度为美术设定。保留原始biomes空数组，不解释为通用生境。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Echinochiton-inspired serial-plated spiny mollusk','zh':'Echinochiton 连背板棘甲软体动物'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH26_COMPLETE',s)
if __name__=='__main__':main()
