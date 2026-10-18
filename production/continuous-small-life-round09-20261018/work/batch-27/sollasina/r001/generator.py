# SPDX-License-Identifier: MIT
"""Original deterministic batch27 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 body=Part('low conservative body and soft podium roots',m);body.ellipsoid((0,0,.0078),(.013,.012,.0058),0,32,14);body.finish(c,True)
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=3,radius=1);bm.verts.ensure_lookup_table();tiles=Part('restrained original dorsal plate mosaic',m)
 def place(n,d=0):return (n.x*(.013+d),n.y*(.012+d),.0078+n.z*(.0058+d))
 for vert in bm.verts:
  normal=vert.co.normalized()
  if normal.z<.12:continue
  u=normal.cross(Vector((0,0,1)))
  if u.length<.01:u=normal.cross(Vector((0,1,0)))
  u.normalize();vv=normal.cross(u).normalized();cen=[face.calc_center_median().normalized() for face in vert.link_faces];cen.sort(key=lambda a:math.atan2(a.dot(vv),a.dot(u)));n=len(cen);base=[normal.lerp(a,.94).normalized() for a in cen];upper=[normal.lerp(a,.82).normalized() for a in cen];v=[place(a,-.00012) for a in base]+[place(a,.00020) for a in upper]+[place(normal,.00042)];f=[tuple(reversed(range(n)))]
  for k in range(n):j=(k+1)%n;f.extend([(k,j,n+j,n+k),(2*n,n+k,n+j)])
  tiles.add(v,f,1 if vert.index%6 else 2)
 bm.free();tiles.finish(c,True)
 feet=Part('ordered curved tube feet with subtle plated rhythm',m)
 for group in range(5):
  for lane,(offset,length,lift) in enumerate([(-.23,.93,.002),(-.075,.77,.004),(.085,.88,.002),(.245,1.06,.005)]):
   a=2*pi*group/5+offset;rr=Vector((math.cos(a),math.sin(a),0));tan=Vector((-math.sin(a),math.cos(a),0));L=.030*length;pts=[]
   controls=[rr*.008+Vector((0,0,.0085)),rr*.015+tan*.0015+Vector((0,0,.0085)),rr*(L*.88)+tan*(.0025 if lane%2 else -.0025)+Vector((0,0,.0033+lift*.3)),rr*L+tan*.002+Vector((0,0,.0038+lift))]
   pts=catmull([tuple(p) for p in controls],5);radii=[]
   for j in range(len(pts)):
    t=j/(len(pts)-1);rad=(.00135*(1-t)**.75+.00042*t)*(1-.045*math.cos(2*pi*10*t));radii.append(rad)
   feet.tube(pts,radii,2 if lane in [0,3] else 0,n=9)
 feet.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='sollasina');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='sollasina';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8E9F93', '#ABA993', '#A2AF9D'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round09-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Silurian marine teaching interpretation; no coexisting scene or specific site','habitat_zh':'志留纪海生教学复原；不指定共存场景或地点','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Original living whole-organism teaching interpretation: low plated body, organically embedded slender curved tube feet with primary/secondary gaps and restrained articulated surface rhythm. Colors, nominal0.07m span, simplified repeated plates and static pose are art choices. No exact microscopic plate or podium counts, internal water-vascular reconstruction, feeding/movement mechanism or named specimen replica claimed. Blunt flexible-looking tips and curved paths distinguish podia from rigid random spines.','zh':'原创全体教学生活复原：低矮板甲体、自然嵌接的细长弯曲管足、主次间隙与克制的分节表面节奏。颜色、0.07米名义跨度、重复板片简化及静态姿态为美术设定。不主张精确微板或管足数、内部水管系统、摄食/运动机制或具名标本复制。钝柔足端及弯曲走向区别于随机刚刺。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Sollasina-inspired plated tube-foot echinoderm','zh':'Sollasina 板甲管足棘皮动物'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH27_COMPLETE',s)
if __name__=='__main__':main()
