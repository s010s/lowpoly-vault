# SPDX-License-Identifier: MIT
"""Original deterministic batch24 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 import bmesh,random
 from mathutils.bvhtree import BVHTree
 rng=random.Random(2026101818)
 def clip(bm,co,no):
  bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00000001,plane_co=co,plane_no=no,clear_inner=True,clear_outer=False)
  edges=[e for e in bm.edges if e.is_boundary]
  if edges:bmesh.ops.holes_fill(bm,edges=edges,sides=0)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 def finish_bm(bm,name,mat,smooth=False):
  bm.verts.index_update();v=[tuple(x.co) for x in bm.verts];f=[tuple(x.index for x in face.verts) for face in bm.faces];p=Part(name,m);p.add(v,f,mat);bm.free();return p.finish(c,smooth)
 bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=3,radius=1)
 for v in bm.verts:
  x,y,z=v.co;fac=1+.040*math.sin(5*x+3*z)+.025*math.sin(9*y-4*x);v.co=(x*.40*fac,y*.26*fac,.205+z*.235*fac)
 clip(bm,Vector((0,0,.003)),Vector((0,0,1)));clip(bm,Vector((0,-.14,0)),Vector((0,1,0)));matrix=finish_bm(bm,'continuous finer-grained matrix with original teaching fracture',0,False)
 # Two modest actual recesses, subordinate to the large rounded-clast structure.
 for i,(x,z,rad) in enumerate([(-.18,.265,.014),(.19,.115,.012)]):
  p=Part('temporary recess cutter',m);p.ellipsoid((x,-.139,z),(rad,rad*.9,rad*.8),0,12,7);o=p.finish(c,False);bpy.context.view_layer.objects.active=matrix;matrix.select_set(True);o.select_set(False);mod=matrix.modifiers.new('small matrix recess '+str(i),'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(o,do_unlink=True)
 bm=bmesh.new();bm.from_mesh(matrix.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00001);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(matrix.data);bm.free()
 bm=bmesh.new();bm.from_mesh(matrix.data);tree=BVHTree.FromBMesh(bm);bm.free();clasts=Part('rounded clasts embedded through continuous matrix',m)
 def pebble(center,rad,mat,cut=False,detail=2):
  bm=bmesh.new();bmesh.ops.create_icosphere(bm,subdivisions=detail,radius=1);sx=rad*rng.uniform(.88,1.12);sy=rad*rng.uniform(.78,1.06);sz=rad*rng.uniform(.72,1.05);angle=rng.uniform(0,pi)
  for v in bm.verts:
   a=v.co.copy();fac=1+.035*math.sin(4*a.x+3*a.y+2*a.z);x=a.x*sx*fac;y=a.y*sy*fac;v.co=Vector(center)+Vector((x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),a.z*sz*fac))
  if cut:clip(bm,Vector((0,-.1405,0)),Vector((0,1,0)))
  bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00003);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
  bm.verts.index_update();v=[tuple(x.co) for x in bm.verts];f=[tuple(x.index for x in face.verts) for face in bm.faces];clasts.add(v,f,mat);bm.free()
 # Exposed fracture face: different planar sections through embedded rounded pebbles.
 count=0
 for row,z in enumerate([.065,.137,.211,.285,.355]):
  for col,x in enumerate([-.28,-.185,-.09,.005,.10,.195,.29]):
   x+=rng.uniform(-.014,.014);zz=z+rng.uniform(-.012,.012)
   if (x/.355)**2+((zz-.205)/.208)**2>.80:continue
   rad=rng.uniform(.028,.043);pebble((x,-.125+rng.uniform(-.008,.007),zz),rad,1+(row+col)%3,True,3 if count%7==0 else 2);count+=1
 # Natural outer face: half-embedded, varied-size rounded clasts over top/back/sides.
 center=Vector((0,0,.205));placed=[];attempt=0
 while len(placed)<32 and attempt<800:
  attempt+=1;direction=Vector((rng.uniform(-1,1),rng.uniform(-.20,1),rng.uniform(-.10,1))).normalized();hit,normal,idx,dist=tree.ray_cast(center,direction,2)
  if hit is None or hit.z<.065 or hit.y<-.115:continue
  rad=rng.uniform(.025,.046)
  if any((hit-a).length<rad+r*.88 for a,r in placed):continue
  placed.append((hit.copy(),rad));pos=hit-normal*rad*.53;pebble(pos,rad,1+len(placed)%3,False,3 if len(placed)%9==0 else 2)
 clasts.finish(c,True)
 for o in c.objects:
  if o.type=='MESH':
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='conglomerate-outcrop');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='conglomerate-outcrop';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#978C77', '#AFB1A5', '#88958D', '#B29F86'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round08-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Original generic sedimentary rock teaching outcrop; no locality or age assignment','habitat_zh':'原创通用沉积岩教学露头，不指定产地或年代','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Geological-form artistic concept: one continuous fine matrix body contains varied rounded pebbles. An original teaching fracture exposes differently sized sections, while curved outer surfaces retain partly embedded rounded relief and two small matrix recesses. Nominal 0.8 m width, muted mineral palette and layout are art choices; no exact deposition site, age, clast chemistry, grain count or process reconstruction. Closed clasts deliberately intersect the matrix, not a loose sphere pile; no source-media textures or copied rock mesh.','zh':'地质形态艺术概念：单一连续细粒基质包含大小有变化的圆砾。原创教学破裂面露出不同尺寸剖切面，曲面外缘保留局部嵌入的圆润凸露，并有两处小基质凹隙。0.8米名义宽度、柔和矿物配色和排列为美术设定，不主张精确沉积地点、年代、砾石化学、颗粒计数或过程复原。封闭砾石有意嵌入基质，不是松散球堆；不使用来源图像贴图或复制岩石网格。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Conglomerate-inspired rounded-clast outcrop','zh':'圆砾嵌生砾岩露头'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH24_COMPLETE',s)
if __name__=='__main__':main()
