# SPDX-License-Identifier: MIT
"""Original deterministic batch14 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 body=Part('soft-corrugated-unsegmented-trunk-with-stout-integrated-lobopods',m);n=32;nr=104;v=[];f=[]
 for j in range(nr+1):
  t=j/nr;y=-.030+.060*t;rad=.00065+.0048*math.sin(pi*(.06+.90*t))**.5;rad*=1+.055*math.cos(t*pi*2*32);cx=.0012*math.sin(t*pi*1.3)
  for k in range(n):
   a=2*pi*k/n;v.append((cx+rad*math.cos(a),y,.0095+rad*.86*math.sin(a)+.0008*math.sin(pi*t)))
 for j in range(nr):
  for k in range(n):f.append((j*n+k,(j+1)*n+k,(j+1)*n+(k+1)%n,j*n+(k+1)%n))
 f+=[tuple(reversed(range(n))),tuple(nr*n+k for k in range(n))];body.add(v,f,0)
 ends=[]
 for j in range(10):
  y=-.023+j*.0052;cx=.0012*math.sin(((y+.03)/.06)*pi*1.3)
  for side in [-1,1]:
   sweep=-.002 if j==9 else .0006*math.sin(j)
   pts=[(cx+side*.0035,y,.0083),(cx+side*.0058,y,.0063),(cx+side*.0072,y+sweep,.0035),(cx+side*.0074,y+sweep-.0005,.0017)];body.tube(catmull(pts,3),[.0021*(1-i/9)+.0010*(i/9) for i in range(10)],0,10);ends.append(Vector(pts[-1]))
 obj=body.finish(c,True)
 # Union only the original soft trunk/feet; keeps their attachment visibly continuous.
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 mod=obj.modifiers.new('fused-soft-foot-roots','REMESH');mod.mode='VOXEL';mod.voxel_size=.00028;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=obj.modifiers.new('soft-body-quiet-joins','SMOOTH');mod.factor=.35;mod.iterations=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 obj.data.calc_loop_triangles();mod=obj.modifiers.new('retain-corrugations-and-silhouette','DECIMATE');mod.ratio=min(1,8500/len(obj.data.loop_triangles));bpy.ops.object.modifier_apply(modifier=mod.name)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,dist=1e-9,edges=list(bm.edges));bm.verts.index_update();groups={}
 for face in bm.faces:groups.setdefault(tuple(sorted(v.index for v in face.verts)),[]).append(face)
 duplicate_islands=[face for faces in groups.values() if len(faces)>1 for face in faces]
 if duplicate_islands:bmesh.ops.delete(bm,geom=duplicate_islands,context='FACES')
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.validate(verbose=True,clean_customdata=True);obj.data.update()
 for face in obj.data.polygons:face.use_smooth=True
 claws=Part('simplified-terminal-claw-clusters',m)
 for j,end in enumerate(ends):
  side=-1 if j%2==0 else 1
  for k in [-1,0,1]:
   p=end+Vector((k*.00060,-.0001,0));curve_tube(claws,[p,p+Vector((side*.0005,-.0007,-.00045)),p+Vector((side*.0006,-.0011,-.0010))],.00029,.00005,1,6,2)
 claws.finish(c,True)
 face=Part('anterior-soft-appendages-mouth-and-papillae',m)
 # No invented eyes or armored head: blunt terminal mouth and small paired appendages.
 face.ellipsoid((.0001,-.0307,.0096),(.0010,.00030,.0010),2,16,8)
 for side in [-1,1]:
  curve_tube(face,[(side*.0015,-.0278,.011),(side*.003,-.031,.012),(side*.0045,-.034,.011)],.0007,.00025,0,8,3)
  for k in [0,1]:face.ellipsoid((side*(.0013+.0003*k),-.0303,.0084+.0020*k),(.00042,.00045,.00042),0,8,5)
 face.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='aysheaia');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='aysheaia';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#B78C74', '#716555', '#705C52'])];generate(c,m)
 if s!='cobbania':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round05-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'marine near-bottom lobopodian teaching concept','habitat_zh':'海生近底叶足动物教学概念','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, posture, simplified counts and fine relief are artistic. Original geometry only; no exact species/specimen, microscopic, locality, salinity or coexistence restoration. Cobbania mounts at the freshwater waterline with roots below it.','zh':'名义尺度、配色、姿态、简化数量及细小起伏为美术选择。仅含原创几何；不主张精确物种标本、显微结构、地点、耐盐性或共存复原。Cobbania 以淡水水面挂点为原点，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Aysheaia-inspired stout clawed lobopodian','zh':'受 Aysheaia 启发的粗短有爪叶足动物'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH14_COMPLETE',s)
if __name__=='__main__':main()
