# SPDX-License-Identifier: MIT
"""Original deterministic batch36 teaching geometry; Blender4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 # A cut wood-host block, not an additional whole log. Lengthwise grain is geometrical and restrained.
 outline=[(-.16,0,.016),(-.157,0,.106),(-.143,0,.132),(-.09,0,.137),(-.025,0,.133),(.043,0,.139),(.11,0,.132),(.151,0,.122),(.16,0,.101),(.156,0,.025),(.141,0,.008),(.075,0,.003),(-.04,0,0),(-.133,0,.004)]
 p=Part('Sectioned fossil wood host',m);p.sheet(outline,.112,0,(0,1,0));host=p.finish(c,False);bpy.context.view_layer.objects.active=host;host.select_set(True)
 bevel=host.modifiers.new('Soft original broken margins','BEVEL');bevel.width=.0022;bevel.segments=2;bpy.ops.object.modifier_apply(modifier=bevel.name);host.select_set(False)
 cavities=[]
 for index,(x,length,tilt) in enumerate([(-.113,.106,.010),(-.060,.098,-.011),(-.004,.111,.008),(.054,.100,.012),(.112,.083,-.010)]):
  # Vertical bore reaches the top surface through a narrow neck and ends in a larger rounded club below.
  n=28;pts=[];rad=[]
  for j in range(n+1):
   u=j/n;z=.162-length*u;xx=x+tilt*u+.002*math.sin(pi*u);pts.append((xx,-.052,z))
   # Neck, widening blind chamber, then closed rounded distal end.
   if u<.34:r=.0068
   elif u<.79:r=.0068+.0105*math.sin((u-.34)/.45*pi/2)
   else:r=.0173*math.sqrt(max(.012,1-((u-.79)/.215)**2))
   rad.append(r)
  p=Part('Boring cutter %d'%index,m);p.tube(pts,rad,0,20);cutter=p.finish(c,False);cavities.append((pts,rad))
  bpy.context.view_layer.objects.active=host;mod=host.modifiers.new('True club-ended cavity %d'%index,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
 # Two mineral/sediment infill casts remain within matching cavities, three cavities expose their walls.
 for index in (1,3):
  pts,rad=cavities[index];p=Part('Exposed matching club cast %d'%index,m)
  pp=[]
  for point in pts[8:]:pp.append((point[0],point[1]-.0015,point[2]))
  p.tube(pp,[r*.87 for r in rad[8:]],2,20);p.finish(c,True)
 # Original shallow longitudinal grain on the uncut back/side, bonded to host; no black hole decals.
 p=Part('Restrained longitudinal wood fibers',m)
 for k in range(7):
  z=.024+k*.013;pts=catmull([(-.151,.055,z),(-.08,.057,z+.002),(.025,.057,z-.001),(.146,.054,z+.001)],5);p.tube(pts,[.0011]*len(pts),1,5)
 for k,z in enumerate([.014,.022,.030,.037]):
  pts=catmull([(-.147+k*.003,-.0562,z),(-.081,-.0563,z+.0013),(.018,-.0563,z-.001),(.143-k*.008,-.0562,z+.001)],7)
  p.tube(pts,[.0001+.00075*math.sin(pi*j/(len(pts)-1))**.4 for j in range(len(pts))],1,5)
 p.finish(c,True)
 # Repair boolean numerical seams in original editable geometry, without skipping source QA.
 import bmesh
 bm=bmesh.new();bm.from_mesh(host.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00002)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00001)
 bmesh.ops.dissolve_limit(bm,angle_limit=.005,use_dissolve_boundaries=True,verts=list(bm.verts),edges=list(bm.edges),delimit={'MATERIAL'})
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(host.data);bm.free();host.data.update()
 # Recalculate booleans' surface normals, retaining a fully editable evaluated mesh in the source.
 bpy.context.view_layer.objects.active=host;host.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');host.select_set(False)
 obs=[o for o in c.objects if o.type=='MESH'];coords=[v.co for o in obs for v in o.data.vertices];scale=.32/(max(p.x for p in coords)-min(p.x for p in coords))
 for o in obs:
  for v in o.data.vertices:v.co*=scale

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='teredolites-wood-boring-cast');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='teredolites-wood-boring-cast';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#8e7560', '#9e8469', '#c3b393'])];generate(c,m);ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'references.json').read_text())
 inventory=json.loads((ROOT/'production/continuous-small-life-round12-20261018/items'/s/'inventory-record.json').read_text())
 meta={'catalog_facets':{k:inventory.get(k) for k in ['worlds','packs','category','subcategory','taxon_group','eras','biomes','tags','representation','reconstruction_type','scale_class']},'worlds':inventory['worlds'],'biomes':inventory['biomes'],'eras':inventory['eras'],'subcategory':inventory['subcategory'],'scale_class':inventory['scale_class'],'research_packs':inventory['packs'],'research_pack_status':'inventory research grouping only; not a published pack claim','inventory_production_gate':inventory['production_gate'],'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'Illustrative cut fossil-wood host','habitat_zh':'示意化石木宿主剖面','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; zero textures','representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'reconstruction_notes':{'en':'Sectional-structure teaching concept: five true club-ended blind borings in an original cut wood host, two matching mineral infill casts and three exposed cavities. Count, cut,0.32m span and colors are illustrative. No producer, tree species, exact fossil specimen or separate whole log is claimed.','zh':'结构剖面教学概念：原创剖切木质宿主内有五条真实棒端膨大盲孔，展示两条相应矿物铸填及三条空腔。数量、剖切、0.32米尺寸及颜色属示意，不指定制造者、树种或精确标本，不另计完整枯木。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 meta['trace_display']='sectional-structure'
 export_asset(s,{'en':'Teredolites wood-boring cast','zh':'Teredolites 木质钻孔铸型'},'traces',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH36_COMPLETE',s)
if __name__=='__main__':main()
