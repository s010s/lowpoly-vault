# SPDX-License-Identifier: MIT
"""Original broad-wing early bat teaching model; static, no animation claim."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def clean_union(obj,target,voxel):
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 mod=obj.modifiers.new('soft-continuous-mammal-connections','REMESH');mod.mode='VOXEL';mod.voxel_size=voxel;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=obj.modifiers.new('quiet-rounded-body-flow','SMOOTH');mod.factor=.45;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 obj.data.calc_loop_triangles();mod=obj.modifiers.new('retain-silhouette-and-face','DECIMATE');mod.ratio=min(1,target/len(obj.data.loop_triangles));bpy.ops.object.modifier_apply(modifier=mod.name)
 import bmesh
 bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.verts.index_update();groups={}
 for f in bm.faces:groups.setdefault(tuple(sorted(v.index for v in f.verts)),[]).append(f)
 duplicates=[f for fs in groups.values() if len(fs)>1 for f in fs]
 if duplicates:bmesh.ops.delete(bm,geom=duplicates,context='FACES')
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.validate(clean_customdata=True);obj.data.update()
 for f in obj.data.polygons:f.use_smooth=True

def wing_shell(part,outline):
 # A curved thin closed membrane, with an original scalloped perimeter and gently filled surface.
 pts=[Vector(p) for p in outline];edge=[]
 for i in range(len(pts)):
  aa,bb,cc,dd=pts[(i-1)%len(pts)],pts[i],pts[(i+1)%len(pts)],pts[(i+2)%len(pts)]
  for h in range(4):
   t=h/4;edge.append(.5*((2*bb)+(-aa+cc)*t+(2*aa-5*bb+4*cc-dd)*t*t+(-aa+3*bb-3*cc+dd)*t*t*t))
 n=len(edge);center=sum(edge,Vector())/n;center.z=.036;v=[];f=[]
 for side in [1,-1]:
  for rad in [.28,.62,1]:
   for point in edge:
    q=center+(point-center)*rad;q.z+=.0012*math.sin(pi*rad)+side*.00045;v.append(tuple(q))
  v.append(tuple(center+Vector((0,0,side*.00045))))
 size=3*n+1
 for side in range(2):
  off=side*size;cap=off+3*n
  for k in range(n):f.append((cap,off+k,off+(k+1)%n))
  for h in range(2):
   for k in range(n):f.append((off+h*n+k,off+(h+1)*n+k,off+(h+1)*n+(k+1)%n,off+h*n+(k+1)%n))
 for k in range(n):f.append((2*n+k,2*n+(k+1)%n,size+2*n+(k+1)%n,size+2*n+k))
 part.add(v,f,1)

def generate(c,m):
 fur=Part('compact-mammal-trunk-head-and-soft-shoulder-roots',m);fur.ellipsoid((0,0,.036),(.010,.026,.011),0,24,14);fur.ellipsoid((0,-.025,.042),(.009,.010,.008),0,24,14);fur.ellipsoid((0,-.034,.040),(.0055,.0055,.0048),0,20,12)
 wings=Part('two-broad-curved-closed-wing-membranes-and-tail-web',m);supports=Part('short-arms-and-four-long-supporting-wing-digits',m);claws=Part('five-wing-digit-claws-per-side-and-small-foot-claws',m);features=Part('friendly-eyes-and-small-mammal-nose',m);ears=Part('small-rounded-upright-mammal-ears',m)
 for sign in [-1,1]:
  def point(x,y,z):return Vector((sign*x,y,z))
  shoulder=point(.008,-.015,.042);elbow=point(.033,0,.046);wrist=point(.060,-.026,.047);hip=point(.009,.018,.031);ankle=point(.023,.045,.017)
  curve_tube(fur,[shoulder,point(.018,-.008,.045),point(.026,-.003,.046)],.0042,.0029,0,12,4)
  curve_tube(supports,[point(.024,-.004,.046),elbow,point(.047,-.012,.047),wrist],.0026,.0018,2,10,4)
  tips=[point(.118,-.029,.052),point(.134,.004,.045),point(.112,.043,.034),point(.070,.063,.026)]
  midpoints=[point(.087,-.029,.051),point(.099,-.012,.049),point(.095,.018,.043),point(.072,.024,.040)]
  outline=[shoulder,elbow,wrist,tips[0],point(.108,-.006,.040),tips[1],point(.100,.024,.032),tips[2],point(.073,.038,.027),tips[3],point(.041,.045,.024),ankle,hip]
  wing_shell(wings,outline)
  for j,tip in enumerate(tips):
   curve_tube(supports,[wrist,midpoints[j],tip],.0015,.00065,2,8,4)
   d=(tip-midpoints[j]).normalized();curve_tube(claws,[tip,tip+d*.0025+Vector((0,0,.0016)),tip+d*.0047+Vector((0,0,.0008)),tip+d*.0038+Vector((0,0,-.0014))],.00080,.00012,3,7,3)
  thumb=point(.062,-.038,.050);curve_tube(supports,[wrist,point(.061,-.033,.050),thumb],.0018,.0010,2,9,3)
  curve_tube(claws,[thumb,point(.064,-.042,.052),point(.067,-.044,.051),point(.068,-.042,.049)],.0010,.00018,3,8,3)
  curve_tube(fur,[hip,point(.020,.030,.023),ankle],.0036,.0019,0,10,4)
  for k in [-1,0,1]:curve_tube(claws,[ankle+Vector((sign*k*.0011,.0006,0)),ankle+Vector((sign*k*.0016,.0035,-.003)),ankle+Vector((sign*k*.0015,.0028,-.005))],.00055,.00011,3,6,3)
  ears.ellipsoid((sign*.006,-.025,.053),(.0040,.0024,.0075),0,16,10);ears.ellipsoid((sign*.006,-.0270,.0538),(.0025,.00075,.0052),1,14,9)
  features.ellipsoid((sign*.0055,-.0325,.0450),(.0018,.0011,.0018),4,16,10);features.ellipsoid((sign*.0055-.00035,-.0334,.0456),(.00035,.00022,.00035),3,10,7)
 features.ellipsoid((0,-.0395,.0405),(.0021,.0014,.0014),4,18,10)
 # Restrained tail web supported by the relatively long hind limbs; no claimed flight mechanism.
 wings.sheet([(-.008,.019,.029),(-.023,.045,.017),(0,.065,.015),(.023,.045,.017),(.008,.019,.029)],.0009,1,(0,0,1))
 curve_tube(supports,[(0,.019,.030),(0,.042,.022),(0,.064,.015)],.0018,.00065,2,8,5)
 obj=fur.finish(c,True);clean_union(obj,3600,.00065)
 for part in [wings,supports,claws,features,ears]:
  obj=part.finish(c,True)
  import bmesh
  bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='onychonycteris');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='onychonycteris';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80 if i!=4 else .32) for i,color in enumerate(['#938171','#A08D7C','#816F5E','#C7B59D','#303730'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round06-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'terrestrial/flying early bat teaching concept; no marine, coexistence or exact flight-behavior claim','habitat_zh':'陆地/飞行早期蝙蝠教学概念；不主张海生、同域共存或精确飞行行为','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'origin':'Static spread-wing teaching display mounted at its lower model contact; pose is not a locomotion or flight-ready claim.','reconstruction_notes':{'en':'Short broad membranes and five wing-digit claw cues per side follow basic museum-supported morphology. Soft tissue, friendly face, palette, pose, nominal size and simplified supports are artistic, not a modern species or exact fossil restoration. No echolocation or flight mechanism is asserted; static, unrigged model.','zh':'短宽翼膜及每侧五个翼指爪提示参考博物馆支持的基础形态。软组织、友善面貌、配色、姿态、名义尺度及简化支撑为美术选择，非现代物种或精确化石复原。不主张回声定位或飞行机制；仅静态无骨骼模型。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Onychonycteris-inspired broad clawed-wing bat','zh':'受 Onychonycteris 启发的宽翼指爪早期蝙蝠'},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH17_COMPLETE',s)
if __name__=='__main__':main()
