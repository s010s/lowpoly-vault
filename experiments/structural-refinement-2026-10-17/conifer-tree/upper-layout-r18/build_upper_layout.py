#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One bounded upper-crown arrangement using immutable r17 A leaf geometry.
No whole-tree output. Only fine attachment, length, pitch and local overlap change.
Original woody excerpt is read from immutable r12; no main trunk/bough edits.
"""
import argparse,hashlib,importlib.util,inspect,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
P=Path(__file__).resolve().parent
REPO=next(x for x in P.parents if (x/'scripts/asset_common.py').exists())
FROZEN=P.parent/'unit-study-r17/build_units.py'
spec=importlib.util.spec_from_file_location('frozen_r17',FROZEN);r17=importlib.util.module_from_spec(spec);spec.loader.exec_module(r17)
ac=r17.ac;v=r17.v;axis=r17.axis;radial=r17.radial
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def support(mesh,sp,span):
 """A tiny tapering fine twig, eight triangles; support cost reported separately."""
 points=[sp(0),sp(.44)];d=(points[1]-points[0]).normalized();side,n=r17.frame(d);verts=[]
 for point,radius in zip(points,[min(.007,span*.012),min(.0025,span*.004)]):
  for j in range(3):
   a=math.tau*j/3;verts.append(point+radius*(side*math.cos(a)+n*math.sin(a)))
 mesh.add(verts,[(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)],0)

def arranged_axes(config):
 out=[]
 for tier in [4,5]:
  row=config['tiers'][tier];z,L=row['height'],row['length'];layout=config['layout']['lower_bough_clusters' if tier==4 else 'higher_bough_clusters']
  for j,degrees in enumerate(row['angles']):
   a=math.radians(degrees);d=radial(a);side=radial(a+math.pi/2);length=L*[1.02,.91,1.07,.96,1.04][(j+tier)%5]
   start=axis(z+.065*math.sin(j*1.9+tier))
   def bp(t):return start+d*length*t+side*(.07*math.sin(t*math.pi)*(1 if j%2 else -1))+v((0,0,-.05*math.sin(t*math.pi)+(.10+.035*tier)*t*t))
   for k,item in enumerate(layout):
    base=bp(item['t']);heading=a+math.radians(item['heading']);pitch=math.radians(item['pitch']);direction=radial(heading)*math.cos(pitch)+v((0,0,math.sin(pitch)));ll=length*item['length_ratio']
    def sp(t,base=base,direction=direction,ll=ll):return base+direction*ll*t+v((0,0,ll*(.035*math.sin(math.pi*t)-.10*t*t)))
    out.append({'id':f'tier{tier+1}-bough{j+1}-spray{k+1}','sp':sp,'material':0 if tier==4 else 1,'attachment':list(base),'direction':list(direction),'length':ll,'cluster':f'tier{tier+1}-bough{j+1}-cluster{k//2+1}','layout':item,'added':tier==5 and k>=4})
 for i,item in enumerate(config['layout']['leader_cluster']):
  base=axis(item['z']);pitch=math.radians(item['pitch']);direction=radial(math.radians(item['angle']))*math.cos(pitch)+v((0,0,math.sin(pitch)));ll=item['length']
  def sp(t,base=base,direction=direction,ll=ll):return base+direction*ll*t+v((0,0,ll*(.035*math.sin(math.pi*t)-.10*t*t)))
  out.append({'id':f'leader-spray-{i+1}','sp':sp,'material':1,'attachment':list(base),'direction':list(direction),'length':ll,'cluster':f'leader-cluster-{i//3+1}','layout':item,'added':i>=7})
 return out

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);dest=args.output_dir.resolve()
 if dest.exists() and any(dest.iterdir()):raise RuntimeError('Output must be fresh; no iteration overwrite')
 dest.mkdir(parents=True,exist_ok=True);config=json.loads((P/'layout-config.json').read_text());wood=r17.inherit_wood(P.parent/'candidate-r12/conifer-tree.blend',True);axes=arranged_axes(config)
 assert len(axes)==43 and sum(x['added'] for x in axes)==8
 col=ac.setup_scene('conifer-upper',config['seed']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
 bark=ac.make_material('bark_warm',config['palette']['bark_warm'],roughness=.92)
 leaves=[ac.make_material(name,config['palette'][name],roughness=.92,double_sided=True) for name in ['needles_mid','young_growth']]
 wm=r17.Mesh();wm.add(wood['vertices'],wood['faces'],0);fol=r17.Mesh()
 placements=[]
 for row in axes:
  before=sum(len(f)-2 for f in fol.f);r17.ribbon_fan(fol,row['sp'],row['material']);after=sum(len(f)-2 for f in fol.f);assert after-before==106
  support(wm,row['sp'],(row['sp'](1)-row['sp'](0)).length)
  placements.append({k:value for k,value in row.items() if k!='sp'})
 woody=ac.mesh_object('Unchanged main wood prefix plus fine supports',wm.v,wm.f,bark,col);fol.finish('Frozen r17 A needle strips in local overlapping clusters',leaves,col)
 assert [list(x.co) for x in woody.data.vertices[:len(wood['vertices'])]]==[list(x) for x in wood['vertices']]
 frozen_leaf_sha=hashlib.sha256(inspect.getsource(r17.ribbon_fan).encode()).hexdigest();total_fol=sum(len(f)-2 for f in fol.f);assert total_fol==4558 and (len(axes)-35)*106<=848
 meta={'description':{'en':'Bounded upper-crown layout test using frozen r17 A needle surfaces; not a whole-tree candidate.','zh':'冻结r17 A叶形的有界上冠排布试验，非整树候选。'},'profile':'opaque double-sided open needle surfaces, palette-only, no textures','scientific_status':'evidence-informed stylized concept; grouping and layout are artistic, no extinct-species reconstruction','provenance':'Original geometry; r17 leaf constructor reused unchanged; original woody excerpt retained exactly. No external image or model incorporated.','generator':str(P.relative_to(REPO)/'build_upper_layout.py'),'frozen_leaf_constructor_sha256':frozen_leaf_sha,'semantic_counts':{'original_sprays':35,'added_sprays':8,'total_sprays':43,'foliage_triangles':4558,'added_foliage_triangles':848,'fine_support_triangles':344,'original_wood_triangles':732},'topology_notes':'Original r12 main wood vertices and face index prefix unchanged; fine support twigs appended, eight triangles per spray. Open cut trunk and double-sided open leaf surfaces intentional. No ground normalization or whole-tree integration.','artistic_choices':['Paired local spray clusters use upward and drooping support axes to bridge upper tiers.','Six added sprays reinforce three short upper boughs; two added sprays support the terminal crown.','Leaf count, widths, per-leaf camber, terminals, normals and palette remain frozen from r17 A. Only whole-spray attachment, length, direction and path change.']}
 result=ac.export_asset('conifer-upper',{'en':'Upper-crown bounded layout test','zh':'上冠有界排布试验'},'plants',col,meta,output_root=dest,render=False,max_triangles=6000,max_materials=3,max_primitives=3)
 assert result['glb_bytes']<=config['budgets']['max_glb_bytes']
 report={'revision':'upper-layout-r18','approval':'pending_independent_direction_review','whole_tree_changed':False,'source_main_wood_blend_sha256':wood['source_sha256'],'original_wood_vertex_count':len(wood['vertices']),'original_wood_triangles':732,'original_main_wood_prefix_exactly_equal':True,'r17_source_sha256':H(FROZEN),'r17_A_leaf_constructor_sha256':frozen_leaf_sha,'geometry_policy':'No leaf-constructor edits; 35 existing sprays rearranged plus exactly eight; support cost separate.','triangles':result['triangles'],'glb_bytes':result['glb_bytes'],'glb_sha256':result['sha256']['glb'],'counts':meta['semantic_counts'],'placements':placements}
 (dest/'layout-measurements.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='placements'},indent=2))
if __name__=='__main__':main()
