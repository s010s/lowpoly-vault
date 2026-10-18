# SPDX-License-Identifier: MIT
"""Original connected bulbous lava lobes and bounded teaching outcrop; no textures."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def flow(part,control,bulges,base,phase):
 points=[Vector(p) for p in catmull(control,20)];n=32;v=[];f=[]
 for j,p in enumerate(points):
  t=j/(len(points)-1);d=(points[min(j+1,len(points)-1)]-points[max(0,j-1)]).normalized();u=d.cross(Vector((0,0,1))).normalized();w=d.cross(u).normalized();envelope=math.sin(pi*t)**.38;rr=.004+(base+sum(height*math.exp(-((t-center)/width)**2) for center,width,height in bulges))*envelope
  for k in range(n):
   a=2*pi*k/n;groove=.080*max(0,math.cos(5*a+phase))**12;skin=1+.018*math.cos(3*a+t*7+phase)-groove;zflat=.74+.035*math.sin(t*2*pi+phase);offset=(u*math.cos(a)+w*math.sin(a)*zflat)*rr*skin;v.append(tuple(p+offset))
 for j in range(len(points)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
 f+=[tuple(reversed(range(n))),tuple((len(points)-1)*n+k for k in range(n))];part.add(v,f,0)

def generate(c,m):
 lava=Part('original-continuous-unequal-pillow-lobes-with-constricted-necks',m)
 flow(lava,[(-.43,-.075,.095),(-.27,-.060,.110),(-.05,-.080,.115),(.18,-.060,.108),(.43,-.035,.100)],[(.18,.125,.112),(.53,.135,.126),(.84,.100,.100)],.018,.2)
 flow(lava,[(-.15,-.035,.108),(-.175,.065,.150),(-.25,.205,.170),(-.30,.265,.165)],[(.60,.28,.099)],.015,1.3)
 flow(lava,[(.16,-.025,.110),(.19,.080,.158),(.29,.175,.182),(.35,.235,.170)],[(.58,.27,.108)],.014,2.5)
 flow(lava,[(.020,-.020,.120),(.005,.080,.175),(.030,.165,.215)],[(.64,.25,.071)],.012,3.4)
 # Lower exposure boundary is cut from the original joined lobes themselves.
 obj=lava.finish(c,True);bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 mod=obj.modifiers.new('joined-original-lobes-and-natural-necks','REMESH');mod.mode='VOXEL';mod.voxel_size=.0038;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=obj.modifiers.new('quiet-cooled-skin-connections','SMOOTH');mod.factor=.38;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 obj.data.calc_loop_triangles();mod=obj.modifiers.new('spend-geometry-on-lobes-and-necks','DECIMATE');mod.ratio=min(1,7600/len(obj.data.loop_triangles));bpy.ops.object.modifier_apply(modifier=mod.name)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.verts.index_update();groups={}
 for face in bm.faces:groups.setdefault(tuple(sorted(v.index for v in face.verts)),[]).append(face)
 duplicates=[face for fs in groups.values() if len(fs)>1 for face in fs]
 if duplicates:bmesh.ops.delete(bm,geom=duplicates,context='FACES')
 bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-7,plane_co=(0,0,.012),plane_no=(0,0,1),clear_inner=True,clear_outer=False)
 boundary=[edge for edge in bm.edges if edge.is_boundary]
 if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.validate(clean_customdata=True);obj.data.update()
 # Match the brief nominal width uniformly, retaining the authored lobe proportions.
 width=max(v.co.x for v in obj.data.vertices)-min(v.co.x for v in obj.data.vertices);factor=.95/width
 for vertex in obj.data.vertices:vertex.co*=factor
 obj.data.update()
 for face in obj.data.polygons:
  face.material_index=1 if face.center.z<.013*factor else 0;face.use_smooth=face.center.z>.014*factor

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='pillow-lava-outcrop');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='pillow-lava-outcrop';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.87) for i,color in enumerate(['#73817B','#65726D'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'lava-water/ice interaction process teaching concept with a bounded exposed outcrop; no exact ancient locality, age or eruption-rate claim','habitat_zh':'熔岩与水/冰作用过程的有界露头教学概念；不主张精确古地点、年代或喷发速率','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometric cooled-skin relief; zero textures','representation':cfg['representation'],'origin':'Flat teaching cut at the lower outcrop contact; no presentation stage exported.','reconstruction_notes':{'en':'Original lofts vary lobe size, elongation, neck width and curvature before soft union. Restrained skin channels converge around inflated ends; bounded flat cut is a teaching presentation choice. Colors, nominal dimensions and simplified layout are artistic. Shape alone is not a field diagnosis proving submarine origin; no exact site or date reconstruction.','zh':'原创放样先变化流瓣大小、伸长、颈宽和曲率，再柔和连接。克制的冷却表皮沟纹在膨鼓端附近汇合；有界平裁底面是教学展示选择。配色、名义尺寸及简化布局为美术选择。仅凭造型不能作证实海底成因的野外诊断，不复原精确地点或年代。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Pillow-lava connected-lobe teaching outcrop','zh':'连续枕瓣枕状熔岩教学露头'},'terrain',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH17_COMPLETE',s)
if __name__=='__main__':main()
