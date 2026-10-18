# SPDX-License-Identifier: MIT
"""Original deterministic batch19 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 for mat in m[:2]:
  for node in mat.node_tree.nodes:
   if node.type=='BSDF_PRINCIPLED':node.inputs['Roughness'].default_value=.32
 matrix=Part('irregular-natural-matrix-rooting-the-crystal-cluster',m);n=18;v=[];f=[];mi=[]
 for z,r in [(0,.76),(.010,1),(.026,.91),(.039,.58)]:
  for k in range(n):
   a=k*2*pi/n;rr=r*(1+.07*math.cos(3*a+.3)+.025*math.sin(5*a));v.append((.086*rr*math.cos(a),.063*rr*math.sin(a),z+.002*math.sin(3*a)*(z/.039)))
 for j in range(3):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(2 if (j+k)%4 else 3)
 bottom=len(v);v.append((0,0,0));top=len(v);v.append((-.003,0,.040))
 for k in range(n):f.extend([(bottom,(k+1)%n,k),(top,3*n+k,3*n+(k+1)%n)]);mi.extend([2,3])
 matrix.add(v,f,mi);matrix.finish(c,False)
 quartz=Part('unequal-six-sided-prisms-with-pointed-terminations',m)
 specs=[((-.010,.006,.020),.019,.170,(-.08,.07,1),.15),((.021,.011,.018),.016,.120,(.22,.05,1),.38),((-.035,-.010,.016),.013,.107,(-.32,-.08,1),.04),((.005,-.029,.016),.012,.079,(.05,-.28,1),.54),((.045,-.005,.015),.011,.072,(.32,-.04,1),.28),((-.014,.036,.017),.010,.087,(-.10,.25,1),.75),((.027,.033,.015),.009,.052,(.20,.27,1),.02),((-.046,.018,.014),.009,.058,(-.35,.12,1),.45),((-.030,-.035,.013),.008,.047,(-.19,-.26,1),.84)]
 for j,(base,radius,height,axis,rotation) in enumerate(specs):
  base=Vector(base);axis=Vector(axis).normalized();u=axis.cross(Vector((0,1,0))).normalized();ww=axis.cross(u).normalized();v=[]
  shoulder=height-radius*1.45
  for h,r in [(0,radius*.97),(shoulder,radius)]:
   for k in range(6):a=2*pi*k/6+rotation;v.append(tuple(base+axis*h+(u*math.cos(a)+ww*math.sin(a))*r))
  tip=len(v);v.append(tuple(base+axis*height));f=[tuple(reversed(range(6)))];mi=[j%2]
  for k in range(6):f.extend([(k,(k+1)%6,6+(k+1)%6,6+k),(6+k,6+(k+1)%6,tip)]);mi.extend([j%2,j%2])
  quartz.add(v,f,mi)
 obj=quartz.finish(c,False);bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 mod=obj.modifiers.new('restrained-crystal-edge-light-catch','BEVEL');mod.width=.00045;mod.segments=1;mod.limit_method='ANGLE';mod.angle_limit=.38;bpy.ops.object.modifier_apply(modifier=mod.name)
 for face in obj.data.polygons:face.use_smooth=False

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='quartz-prism-cluster');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='quartz-prism-cluster';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#D2D9D0', '#BAC7C2', '#999686', '#ADA694'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round07-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'mineral-growth teaching cluster on original matrix; no exact mine, chemistry or age claim','habitat_zh':'原创基质上的矿物生长教学晶簇；不主张精确矿区、化学测定或年代','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Original unequal six-sided prisms with pointed terminations, varied inclination and thickness, rooted within an irregular matrix. Solid opaque portable materials with restrained roughness; no complex transparent overlaps, industrial array or reference specimen copy. Nominal size, crystal count, colors and small edge rounding are artistic. Low byte count follows planar crystal geometry; no filler tessellation.','zh':'原创不等大六方柱与尖端，粗细及倾向变化，并嵌生于不规则基质。采用克制粗糙度的不透明便携材质，不靠复杂透明重叠、工业阵列或复制标本。名义尺寸、晶数、配色及轻微棱缘圆厚为美术选择。平面晶体几何文件较小，不填充无用细分。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Quartz six-sided prism cluster on natural matrix','zh':'天然基质上的六方尖端石英柱晶簇'},'geology',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH19_COMPLETE',s)
if __name__=='__main__':main()
