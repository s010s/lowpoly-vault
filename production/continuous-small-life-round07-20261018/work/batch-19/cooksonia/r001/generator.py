# SPDX-License-Identifier: MIT
"""Original deterministic batch19 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def steady(part,points,r0,r1):
 pts=[Vector(p) for p in catmull(points,5)];v=[];n=12;u=None
 for j,p in enumerate(pts):
  d=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized()
  if u is None:u=d.cross(Vector((0,1,0))).normalized()
  else:u=(u-d*u.dot(d)).normalized()
  ww=d.cross(u).normalized();r=r0+(r1-r0)*j/(len(pts)-1)
  for k in range(n):a=k*2*pi/n;v.append(tuple(p+r*(u*math.cos(a)+ww*math.sin(a))))
 f=[tuple(reversed(range(n)))]+[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(pts)-1) for k in range(n)]+[tuple((len(pts)-1)*n+k for k in range(n))];part.add(v,f,0)

def generate(c,m):
 axes=Part('sparse-naked-dichotomous-axes-with-soft-Y-junctions',m);caps=Part('flattened-terminal-sporangial-capsules',m);tips=[]
 for j,(bx,by,h) in enumerate([(-.011,.004,.064),(.004,-.006,.052),(.014,.009,.043)]):
  base=Vector((bx,by,.0008));fork=base+Vector((.001,0,h*.49));steady(axes,[base,base+Vector((-.001,0,h*.25)),fork],.00105,.00080)
  for side in [-1,1]:
   if j==0:
    node=fork+Vector((side*.008,.001,h*.26));steady(axes,[fork,(fork+node)*.5,node],.00080,.00064)
    for ss in [-1,1]:
     tip=node+Vector((ss*.005,side*.003,h*.25-.001*ss));steady(axes,[node,(node+tip)*.5,tip],.00064,.00046);tips.append(tip)
   else:
    tip=fork+Vector((side*(.008+j*.001),.002*side,h*.50-.002*side));steady(axes,[fork,(fork+tip)*.5+Vector((0,.0006,0)),tip],.00080,.00048);tips.append(tip)
 obj=axes.finish(c,True);bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 mod=obj.modifiers.new('continuous-slender-fork-roots','REMESH');mod.mode='VOXEL';mod.voxel_size=.00018;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=obj.modifiers.new('natural-fork-flow','SMOOTH');mod.factor=.4;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 obj.data.calc_loop_triangles();mod=obj.modifiers.new('silhouette-only-axis-detail','DECIMATE');mod.ratio=min(1,3200/len(obj.data.loop_triangles));bpy.ops.object.modifier_apply(modifier=mod.name)
 for face in obj.data.polygons:face.use_smooth=True
 for j,tip in enumerate(tips):
  v=[];n=24;profile=[(-.0003,.0005),(0,.0011),(.001,.0026),(.0025,.0034),(.0040,.0035),(.0047,.0029),(.0050,.0016)]
  for z,r in profile:
   for k in range(n):a=k*2*pi/n;v.append(tuple(tip+Vector((r*math.cos(a),r*.72*math.sin(a),z))))
  bottom=len(v);v.append(tuple(tip+Vector((0,0,-.0003))));top=len(v);v.append(tuple(tip+Vector((0,0,.0051))));f=[];mi=[]
  for h in range(len(profile)-1):
   for k in range(n):f.append((h*n+k,h*n+(k+1)%n,(h+1)*n+(k+1)%n,(h+1)*n+k));mi.append(1)
  for k in range(n):f.extend([(bottom,(k+1)%n,k),(top,(len(profile)-1)*n+k,(len(profile)-1)*n+(k+1)%n)]);mi.extend([1,2])
  caps.add(v,f,mi)
 caps.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='cooksonia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='cooksonia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#7F956C', '#999C6B', '#B0AA79'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'early terrestrial plant teaching concept; not marine vegetation','habitat_zh':'早期陆地植物教学概念；非海洋植被','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Same stable Cooksonia ID restored from deferred unbuilt planning. Sparse naked Y-branching axes and flattened terminal spore capsules; no modern leaves, flowers or speculative root system. Nominal size, colors, axis/capsule count and layout are artistic, not exact species/specimen reconstruction.','zh':'从延后未制作计划恢复的同一 Cooksonia 稳定ID。稀疏裸露Y形分叉与扁平顶生孢子囊；不添现代叶、花或推测根系。名义尺度、配色、枝囊数量及布局为美术选择，非精确物种或标本复原。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Cooksonia-inspired sparse sporangial shoots','zh':'受 Cooksonia 启发的稀疏顶囊裸轴'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
