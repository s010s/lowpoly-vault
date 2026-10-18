# SPDX-License-Identifier: MIT
"""Original deterministic batch12 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def steady_tube(part,points,r0,r1,mi=0,n=12,steps=4):
 points=[Vector(p) for p in catmull(points,steps)];v=[];prev=None
 for j,p in enumerate(points):
  d=(points[min(j+1,len(points)-1)]-points[max(j-1,0)]).normalized()
  u=prev-d*prev.dot(d) if prev is not None else d.cross(Vector((0,0,1)))
  if u.length<.001:u=d.cross(Vector((0,1,0)))
  u.normalize();w=d.cross(u).normalized();prev=u.copy();t=j/(len(points)-1);radius=r0*(1-t)**1.1+r1*t
  for k in range(n):v.append(tuple(p+radius*(u*math.cos(2*pi*k/n)+w*math.sin(2*pi*k/n))))
 f=[tuple(reversed(range(n)))]+[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(points)-1) for k in range(n)]+[tuple((len(points)-1)*n+k for k in range(n))];part.add(v,f,mi)

def generate(c,m):
 wood=Part('open-divaricate-bennettitalean-shrub-scaffold',m)
 steady_tube(wood,[(0,0,.006),(-.012,.008,.105),(0,0,.230),(.004,0,.240)],.028,.018,0,14,4)
 forks=[(Vector((0,0,.210)),Vector((-.130,.015,.460))),(Vector((0,0,.225)),Vector((.135,-.015,.450)))]
 tips=[]
 for j,(start,fork) in enumerate(forks):
  steady_tube(wood,[start,(start+fork)*.5,fork],.018,.012,0,12,4)
  sign=-1 if j==0 else 1
  for k,(dx,dy,dz) in enumerate([(sign*.12,-.075,.205),(sign*.035,.100,.245),(-sign*.040,-.010,.275)]):
   tip=fork+Vector((dx,dy,dz));steady_tube(wood,[fork,fork+Vector((dx*.55,dy*.5,dz*.45)),tip],.0115,.0042,0,12,4);tips.append(tip)
 obj=wood.finish(c,True)
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 mod=obj.modifiers.new('soft-continuous-branch-forks','REMESH');mod.mode='VOXEL';mod.voxel_size=.0030;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=obj.modifiers.new('quiet-woody-transitions','SMOOTH');mod.factor=.6;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 obj.data.calc_loop_triangles();mod=obj.modifiers.new('shape-focused-lowpoly','DECIMATE');mod.ratio=min(1,2700/len(obj.data.loop_triangles));bpy.ops.object.modifier_apply(modifier=mod.name)
 for face in obj.data.polygons:face.use_smooth=True
 fronds=Part('small-terminal-leaf-clusters-with-visible-branch-support',m);ribs=Part('slender-pinnate-leaf-axes',m)
 for j,tip in enumerate(tips):
  for leafno in range(2):
   a=math.atan2(tip.y,tip.x)+(leafno-.5)*1.3;u=Vector((math.cos(a),math.sin(a),.48 if leafno==0 else .25)).normalized();w=Vector((-u.y,u.x,0)).normalized();length=.145+.018*math.sin(j)
   def pos(t):return tip+u*(length*t)+Vector((0,0,.020*math.sin(pi*t)-.018*t*t))
   ribs.tube([pos(t) for t in [0,.2,.4,.6,.8,1]],[.0024,.0020,.0015,.0010,.0006,.00020],1,7)
   for q in range(1,9):
    t=.08+q*.095;p=pos(t);span=.029*math.sin(pi*t)**.8
    for side in [-1,1]:
     end=p+w*side*span+u*.006+Vector((0,0,.003));mid=(p+end)*.5+u*.0015;th=.0007;verts=[tuple(p-u*.002),tuple(mid-u*.0028),tuple(end),tuple(mid+u*.0028),tuple(p+u*.002),tuple(mid+Vector((0,0,-th)))];faces=[(0,1,2),(0,2,3),(0,3,4),(0,5,1),(1,5,2),(2,5,3),(3,5,4),(4,5,0)];fronds.add(verts,faces,1 if (j+q)%4 else 2)
 ribs.finish(c,True);fronds.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='wielandiella');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='wielandiella';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#99846B', '#8E9F75', '#A5AF87'])];generate(c,m)
 if s!='limnobiophyllum':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'terrestrial/shore shrub; no exact salinity/coexistence claim','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, pose, leaf/root/frond counts and fine relief are artistic. Original geometry only; no exact species, microscopic, locality, salinity or coexistence restoration. Limnobiophyllum mounting origin is the freshwater waterline; its roots extend below it.','zh':'名义尺度、配色、姿态、叶/根/羽片数量及细小起伏为美术选择。仅含原创几何；不主张精确物种、显微结构、地点、耐盐性或同域共存复原。Limnobiophyllum 原点为淡水水面，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Wielandiella-inspired divaricate shrub','zh':'受 Wielandiella 启发的叉枝灌木'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH12_COMPLETE',s)
if __name__=='__main__':main()
