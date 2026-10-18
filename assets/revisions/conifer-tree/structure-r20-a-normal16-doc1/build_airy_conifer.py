#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Full conifer r19: user-selected separated, feathery airy A style.
Deterministic, standalone generator with frozen A constructor and recorded r12
wood snapshot. No B core surfaces; no implicit production/visual approval.
"""
import argparse,hashlib,inspect,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
P=Path(__file__).resolve().parent
REPO=next(x for x in P.parents if (x/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
import asset_common as ac
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def v(p):return Vector(p)


def radial(a):return v((math.cos(a),math.sin(a),0))


def axis(z):return v((.045*math.sin(z*.75),.025*math.sin(z*.51),z))


def frame(d):
 d=d.normalized();u=d.cross(v((0,0,1)) if abs(d.z)<.9 else v((0,1,0))).normalized();n=u.cross(d).normalized()
 if n.z<0:u=-u;n=-n
 return u,n


class Mesh:
 def __init__(self):self.v=[];self.f=[];self.m=[]
 def add(self,verts,faces,mat):
  off=len(self.v);self.v.extend([tuple(x) for x in verts]);self.f.extend([tuple(off+i for i in face) for face in faces]);self.m.extend([mat]*len(faces))
 def finish(self,name,mats,col):
  obj=ac.mesh_object(name,self.v,self.f,mats,col)
  for face,mi in zip(obj.data.polygons,self.m):face.material_index=mi
  # Smooth along the two gently bowed panels; there is no raised center ridge.
  for face in obj.data.polygons:face.use_smooth=True
  return obj


def strip(mesh,points,widths,side,mat):
 verts=[]
 for point,width in zip(points,widths):verts.extend([point-side*width/2,point+side*width/2])
 faces=[(2*k,2*k+1,2*k+3,2*k+2) for k in range(len(points)-1)]
 mesh.add(verts,faces,mat)


def rachis(mesh,sp,span,side,mat):
 ts=[0,.34,.68,1.03]
 strip(mesh,[sp(t) for t in ts],[span*.012,span*.009,span*.006,span*.002],side,mat)


def ribbon_fan(mesh,sp,mat):
 """One feather: 24 curved narrow leaves + small terminal + curved rachis =106 tri."""
 span=(sp(1)-sp(0)).length;side,n=frame(sp(1)-sp(0));rachis(mesh,sp,span,side,mat)
 for k in range(12):
  t=.075+k*.072;length=span*(.12+.14*math.sin(math.pi*t))*(1-.40*t)
  tangent=(sp(t+.02)-sp(t-.02)).normalized()
  for sign in [-1,1]:
   base=sp(t+(.012 if sign>0 else 0));pitch=.22*math.sin(k*.65)+sign*.13
   lat=(side*math.cos(pitch)+n*math.sin(pitch)).normalized()
   d=(tangent*.34+lat*sign*.94).normalized();cross=d.cross(n).normalized()
   points=[base+d*length*u+n*length*(.11*math.sin(math.pi*u)-.16*u*u) for u in [0,.55,1]]
   width=length*.15
   strip(mesh,points,[width*.60,width,width*.12],cross,mat)
 # A short, narrow forward terminal continues the feather axis without a spear.
 base=sp(.91);d=(sp(1.02)-base).normalized();length=span*.16
 strip(mesh,[base,base+d*length*.55+n*length*.06,base+d*length-n*length*.08],[span*.012,span*.022,span*.003],side,mat)


def support(mesh,sp,span):
 """A tiny tapering fine twig, eight triangles; support cost reported separately."""
 points=[sp(0),sp(.44)];d=(points[1]-points[0]).normalized();side,n=frame(d);verts=[]
 for point,radius in zip(points,[min(.007,span*.012),min(.0025,span*.004)]):
  for j in range(3):
   a=math.tau*j/3;verts.append(point+radius*(side*math.cos(a)+n*math.sin(a)))
 mesh.add(verts,[tuple(reversed(f)) for f in [(2,1,0),(3,4,5),(0,1,4,3),(1,2,5,4),(2,0,3,5)]],0)


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


def lower_axes(config):
 out=[]
 for tier in range(4):
  row=config['tiers'][tier];z,L=row['height'],row['length'];layout=config['lower_layouts']['seven' if tier<2 else 'five']
  for j,degrees in enumerate(row['angles']):
   if tier==0 and j==1:continue # existing broken bough and its sky window retained
   a=math.radians(degrees);d=radial(a);side=radial(a+math.pi/2);length=L*[1.02,.91,1.07,.96,1.04][(j+tier)%5];start=axis(z+.065*math.sin(j*1.9+tier));droop=.20 if tier<2 else .13
   def bp(t):return start+d*length*t+side*(.07*math.sin(t*math.pi)*(1 if j%2 else -1))+v((0,0,-droop*math.sin(t*math.pi)+(.10+.035*tier)*t*t))
   for k,item in enumerate(layout):
    base=bp(item['t']);heading=a+math.radians(item['heading']);pitch=math.radians(item['pitch']);direction=radial(heading)*math.cos(pitch)+v((0,0,math.sin(pitch)));ll=length*(.39+.055*math.sin(math.pi*item['t']))*config['shoot_length_multiplier']
    def sp(t,base=base,direction=direction,ll=ll):return base+direction*ll*t+v((0,0,ll*(.035*math.sin(math.pi*t)-.10*t*t)))
    out.append({'id':f'tier{tier+1}-bough{j+1}-spray{k+1}','sp':sp,'material':0,'attachment':list(base),'direction':list(direction),'length':ll,'cluster':f'tier{tier+1}-bough{j+1}-cluster{k//2+1}','added':False,'support':False})
 return out

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--config',type=Path,default=P/'build-config.json');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.output_dir.resolve()
 if out.exists() and any(out.iterdir()):raise RuntimeError('Fresh output directory required')
 out.mkdir(parents=True,exist_ok=True);config=json.loads(args.config.read_text());wood=json.loads((P/'woody-source.json').read_text())
 constructor_hash=hashlib.sha256(inspect.getsource(ribbon_fan).encode()).hexdigest();assert constructor_hash==config['frozen_A_leaf_constructor_sha256']
 axes=lower_axes(config);assert len(axes)==106
 upper=arranged_axes(config)
 for item in upper:item['support']=True
 axes+=upper;assert len(upper)==43 and len(axes)==149 and sum(x['added'] for x in axes)==8
 col=ac.setup_scene('conifer-tree',config['seed']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
 bark=ac.make_material('bark_warm',config['palette']['bark_warm'],roughness=.92)
 leaves=[ac.make_material(name,config['palette'][name],roughness=.92,double_sided=True) for name in ['needles_mid','young_growth']]
 wm=Mesh();wm.add(wood['vertices'],wood['faces'],0);fol=Mesh();fol_parts=[];support_parts=[];placements=[]
 for row in axes:
  start=len(fol.v);before=sum(len(f)-2 for f in fol.f);ribbon_fan(fol,row['sp'],row['material']);assert sum(len(f)-2 for f in fol.f)-before==106;fol_parts.append((row['id'],start,len(fol.v)))
  if row['support']:
   first=len(wm.v);support(wm,row['sp'],(row['sp'](1)-row['sp'](0)).length);support_parts.append((row['id'],first,len(wm.v)))
  placements.append({key:value for key,value in row.items() if key!='sp'})
 woody=ac.mesh_object('Conifer | unchanged r12 main wood and small upper twig supports',wm.v,wm.f,bark,col,recalculate_normals=False)
 for name,indices in wood['vertex_groups'].items():woody.vertex_groups.new(name=name).add(indices,1,'REPLACE')
 for label,a,b in support_parts:woody.vertex_groups.new(name='fine-support-'+label).add(list(range(a,b)),1,'REPLACE')
 foliage=fol.finish('Conifer | user-selected separated feather-needle A',leaves,col)
 for label,a,b in fol_parts:foliage.vertex_groups.new(name=label).add(list(range(a,b)),1,'REPLACE')
 assert [list(x.co) for x in woody.data.vertices[:len(wood['vertices'])]]==wood['vertices']
 original_face_prefix=[list(face.vertices) for face in woody.data.polygons[:len(wood['faces'])]];face_equal=original_face_prefix==wood['faces'];assert face_equal
 meta={'description':{'en':'An airy seven-meter conifer concept with rounded tapering main boughs, separated narrow feather-like needle sprays, shallow local overlap and natural crown sky windows.','zh':'轻透的七米针叶乔木概念：圆顺渐细主枝、分离羽状细针叶束、局部浅搭接与自然天窗。'},'profile':'static opaque palette-only; double-sided open thin leaf strips; no textures','scientific_status':'evidence-informed stylized conifer architectural concept; no identified extinct species reconstruction','generator':str((P/'build_airy_conifer.py').relative_to(REPO)),'generator_sha256':H(P/'build_airy_conifer.py'),'source_wood_snapshot_sha256':H(P/'woody-source.json'),'frozen_A_leaf_constructor_sha256':constructor_hash,'seed':config['seed'],'provenance':'Original geometry. r12 wood coordinates and faces retained exactly, r17 A constructor retained unchanged. References consulted only; no external mesh or imagery incorporated.','artistic_choices':['The user explicitly selected separated, feathery, airy A rather than B connected feather-core surfaces. Natural sparsity and sky windows are intended style, not a density defect by itself.','Paired local lower-crown attachments and inherited r18 upper arrangement produce irregular layered foliage. The existing broken lower bough remains.','Individual-like needle count, enlarged groups, colors, seven-meter scale and precise branch arrangement are artistic abstractions, not measured fossil anatomy.'],'topology_notes':'Main wood remains closed flat-shaded geometry with original collars. Upper fine supports are8 triangles per spray. Leaves are intentionally open double-sided opaque strips, with two gently bent panels and shared normals. No thick green tube, ridge-filled hard blade or connected B core. Organic twig/branch contacts are intentionally buried intersections.','semantic_counts':{'main_boughs':26,'lower_sprays':106,'upper_sprays':43,'total_sprays':149,'added_upper_sprays':8,'foliage_triangles':15794,'upper_support_triangles':344,'original_wood_triangles':2914},'authored_source_vertices':len(wm.v)+len(fol.v),'source_vertex_count_convention':'Sum of authored unique mesh vertices, no modifiers or instances.','target_runtime':'Three.js0.180.0; exact GPU and composed-scene evidence pending separate gate.'}
 result=ac.export_asset('conifer-tree',{'en':'Airy feather-needle conifer concept','zh':'轻透羽状针叶乔木'},'plants',col,meta,output_root=out,render=False,max_triangles=config['budgets']['max_triangles'],max_materials=3,max_primitives=3)
 assert result['glb_bytes']<=config['budgets']['max_glb_bytes']
 report={'revision':config['revision'],'status':'candidate_pending_independent_review','art_approved':False,'triangles':result['triangles'],'glb_bytes':result['glb_bytes'],'glb_sha256':result['sha256']['glb'],'counts':meta['semantic_counts'],'source_vertices':meta['authored_source_vertices'],'main_wood_vertex_prefix_exact':True,'main_wood_polygon_prefix_exact':face_equal,'frozen_A_leaf_constructor_sha256':constructor_hash,'source_wood_snapshot_sha256':H(P/'woody-source.json'),'placements':placements}
 (out/'build-measurements.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({key:value for key,value in report.items() if key!='placements'},indent=2))
if __name__=='__main__':main()
