# SPDX-License-Identifier: MIT
"""Original deterministic batch11 geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 stems=Part('prostrate-leafy-axis-and-directional-K-junctions',m);roots=Part('unbranched-root-bearing-axes-with-fine-lateral-roots',m);leaves=Part('small-subordinate-triangular-leaves',m)
 main=[(-.010,-.120,.009),(-.008,-.070,.010),(.004,-.018,.010),(-.002,.040,.011),(.014,.105,.013),(.022,.130,.020)]
 curve_tube(stems,main,.0044,.0018,0,12,5)
 leafy=[]
 for j,(y,x,s) in enumerate([(-.080,-.008,-1),(-.027,.002,1),(.035,-.002,-1),(.090,.010,1)]):
  node=Vector((x,y,.010));fork=node+Vector((s*.014,.001,.001));curve_tube(stems,[node,node+Vector((s*.008,0,.001)),fork],.0031,.0025,0,10,3)
  tip=fork+Vector((s*(.028 if j%2 else .035),.035,.018+.009*(j%2)));path=[fork,fork+Vector((s*.018,.013,.005)),tip,tip+Vector((s*.007,.010,.008))];leafy.append(path);curve_tube(stems,path,.0026,.0007,0,10,4)
  rootpath=[fork,fork+Vector((s*.010,-.013,-.004)),fork+Vector((s*.015,-.030,-.009))];curve_tube(roots,rootpath,.0016,.00055,1,9,4)
  end=rootpath[-1]
  for q in [-1,1]:
   pts=[end,end+Vector((q*.012,-.005,-.001)),end+Vector((q*.022,-.009,-.001))];curve_tube(roots,pts,.00065,.00015,1,6,3)
 # Tiny leaves track leafy stems; roots remain distinct and unleafed.
 for path in [main]+leafy:
  points=catmull(path,5)
  for j in range(2,len(points)-1,2):
   p=Vector(points[j]);a=j*2.4;u=Vector((math.cos(a),math.sin(a),.45));w=Vector((-u.y,u.x,0)).normalized();length=.0035
   leaves.sheet([p-w*.0006,p+u*length,p+w*.0006,p-Vector((0,0,.0003))],.0003,2,axis=u.cross(w).normalized())
 stems.finish(c,True);roots.finish(c,True);leaves.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='sengelia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='sengelia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#7F9271', '#99846A', '#A3AF84'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'terrestrial / wetland shore; not marine vegetation','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, color, pose and repeated detail counts are artistic choices; no exact species/specimen/coexistence reconstruction. Original geometry only.','zh':'名义尺度、颜色、姿态及细小重复结构数量为美术选择；不主张精确物种、标本或同域共存复原。仅含原创几何。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Sengelia-inspired K-branching ground plant','zh':'受 Sengelia 启发的 K 形匍匐植物'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH11_COMPLETE',s)
if __name__=='__main__':main()
