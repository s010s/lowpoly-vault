# SPDX-License-Identifier: MIT
"""Original attached-cone organ teaching specimen, never a whole Araucaria tree."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 core=Part('rounded-preserved-cone-core',m);scales=Part('original-mosaic-polygonal-cone-scales',m);twig=Part('one-short-supporting-twig-and-attached-pedicel',m)
 center=Vector((.027,0,.052));radii=Vector((.038,.035,.045));core.ellipsoid(center,radii,2,48,24)
 def surf(theta,phi,height=0):
  point=Vector((radii.x*math.sin(theta)*math.cos(phi),radii.y*math.sin(theta)*math.sin(phi),radii.z*math.cos(theta)));normal=Vector((point.x/radii.x**2,point.y/radii.y**2,point.z/radii.z**2)).normalized();return tuple(center+point+normal*height)
 for row in range(12):
  theta=.18+row*(pi-.36)/11;n=max(5,round(17*math.sin(theta)));dp=pi/n
  for k in range(n):
   phi=2*pi*(k+.5*(row%2))/n+.04*math.sin(row);uv=[(0,-.118),(.90*dp,-.055),(.90*dp,.055),(0,.118),(-.90*dp,.055),(-.90*dp,-.055)];v=[]
   for scale,h in [(1,.0007),(.74,.0023)]:
    for du,dv in uv:v.append(surf(theta+dv*scale,phi+du*scale,h))
   v.append(surf(theta,phi,.0030));v.append(surf(theta,phi,.0005));f=[]
   for j in range(6):f.extend([(j,(j+1)%6,6+(j+1)%6,6+j),(6+j,6+(j+1)%6,12),((j+1)%6,j,13)])
   scales.add(v,f,0 if (k+row)%4 else 1)
 # A short curved twig plus a conservative attached cone stalk; no leaves or mother crown.
 curve_tube(twig,[(-.097,-.004,.012),(-.066,-.003,.014),(-.027,0,.017),(.008,.003,.019),(.050,.010,.021)],.0070,.0043,3,16,5)
 curve_tube(twig,[(.014,.004,.018),(.020,.001,.024),(.026,0,.031)],.0065,.0080,3,14,4)
 # Restrained original bark ridges along the short twig, no bark image.
 for k in range(5):
  a=2*pi*k/5;pts=[(-.085+t*.115,-.002+math.cos(a)*(.0062-.0015*t),.013+.006*t+math.sin(a)*(.0062-.0015*t)) for t in [0,.25,.5,.75,1]];curve_tube(twig,pts,.0005,.00025,2,5,2)
 core.finish(c,True);scales.finish(c,True);twig.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='araucaria-mirabilis');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='araucaria-mirabilis';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.84) for i,color in enumerate(['#B5A084','#AA9378','#96816A','#8F7B62'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'preserved botanical organ teaching specimen; terrestrial cone-bearing plant context only, not a whole parent tree or marine vegetation','habitat_zh':'保存植物器官教学标本；仅陆地球果植物背景，非完整母树或海洋植被','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':'fossil-specimen','reconstruction_type':'specimen','organ_scope':{'en':'One short twig with one attached rounded mosaic-scaled cone; no complete tree, roots, foliage crown or unknown associated organs.','zh':'仅一段短枝与一个附生圆形镶嵌鳞片球果；无整树、根、叶冠或未知伴生器官。'},'reconstruction_notes':{'en':'Original rounded teaching geometry of the preserved organ, not a scan or measured replica. Nominal scale, scale count, muted fossil colors and short-branch curvature are artistic simplifications. Museum text supports attached-cone scope; no source photograph copied.','zh':'保存器官的原创圆厚教学几何，非扫描或实测复制品。名义尺度、鳞片数量、化石配色及短枝弯曲为美术简化。博物馆文字支持附枝球果范围，未复制来源照片。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Araucaria mirabilis-inspired attached cone organ specimen','zh':'受 Araucaria mirabilis 启发的短枝附生球果器官标本'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH17_COMPLETE',s)
if __name__=='__main__':main()
