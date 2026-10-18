# SPDX-License-Identifier: MIT
"""Original deterministic batch24 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh
 core=Part('compact ovulate receptacle and short stalk',m)
 core.ellipsoid((0,0,.066),(.023,.0215,.032),0,28,16)
 curve_tube(core,[(0,0,.003),(-.001,.001,.018),(0,0,.039)],.0045,.0061,0,14,5);core.finish(c,True)
 # Original polygonal tessellation derived from a dual icosphere; no media input.
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=3,radius=1);bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table();tiles=Part('restrained interseminal surface mosaic',m)
 def place(n,depth=0):
  return (n.x*(.023+depth),n.y*(.0215+depth),.066+n.z*(.032+depth))
 for vert in bm.verts:
  normal=vert.co.normalized()
  if normal.z<-.86:continue
  u=normal.cross(Vector((0,0,1)))
  if u.length<.01:u=normal.cross(Vector((0,1,0)))
  u.normalize();vv=normal.cross(u).normalized();centers=[face.calc_center_median().normalized() for face in vert.link_faces];centers.sort(key=lambda a:math.atan2(a.dot(vv),a.dot(u)));n=len(centers)
  base=[(normal.lerp(a,.94)).normalized() for a in centers];upper=[(normal.lerp(a,.80)).normalized() for a in centers];v=[place(a,-.00020) for a in base]+[place(a,.00055) for a in upper]+[place(normal,.0010)]
  f=[tuple(reversed(range(n)))]
  for k in range(n):j=(k+1)%n;f.append((k,j,n+j,n+k));f.append((2*n,n+k,n+j))
  tiles.add(v,f,1 if vert.index%9 in [0,2] else 2)
 bm.free();o=tiles.finish(c,True)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='williamsonia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='williamsonia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8C8069', '#AA9B7F', '#A19378'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Preserved terrestrial botanical ovulate organ teaching specimen','habitat_zh':'保存的陆生植物种子球果器官教学标本','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Fossil-specimen organ only: compact ovoid receptacle, restrained polygonal interseminal surface mosaic and short attached stalk. Original conservative three-dimensional thickness, beige fossil palette and nominal 0.1 m height; no whole parent plant, leaf whorl, daisy-like petals, inferred stamens, trunk-embedded structure or modern conifer scales. The mosaic expresses basic surface organization without claiming exact ovules, cellular anatomy or a specimen replica.','zh':'仅化石保存器官：紧凑卵形承托体、克制的多边形间种鳞片镶嵌表面及短柄。保守三维厚度、米褐化石色与0.1米名义高度为原创美术设定；不添加整株、叶轮、雏菊状花瓣、推断雄蕊、干体嵌生结构或现代针叶树球果鳞片。镶嵌仅表达基本表面组织，不主张精确胚珠、细胞结构或标本复制。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Williamsonia-inspired preserved ovulate cone organ','zh':'Williamsonia 本内苏铁类种子球果器官'},'fossil-plant',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH24_COMPLETE',s)
if __name__=='__main__':main()
