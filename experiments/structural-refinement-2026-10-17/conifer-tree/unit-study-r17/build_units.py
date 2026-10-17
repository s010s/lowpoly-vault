#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Two foliage representations on immutable r12 wood excerpts, never a full tree.
Local bounded modeling study. Thin leaf surfaces are explicitly double-sided,
opaque, and texture-free. No thickness shell or ridge-fan cap is generated.
"""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
P=Path(__file__).resolve().parent
REPO=next(x for x in P.parents if (x/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
import asset_common as ac

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

def feather_lobe(mesh,sp,mat):
 """16 narrow linear silhouette tabs (2 tri each) + curved spine (6 tri) =38 tri.
 These tabs intentionally omit per-leaf camber. Their bases visibly meet the spine;
 they are open double-sided surfaces, not a manifold volume or thick 'fingers'.
 """
 span=(sp(1)-sp(0)).length;side,n=frame(sp(1)-sp(0));rachis(mesh,sp,span,side,mat)
 for k in range(8):
  t=.085+k*.108;tangent=(sp(t+.02)-sp(t-.02)).normalized()
  length=span*(.15+.13*math.sin(math.pi*t))*(1-.42*t)
  for sign in [-1,1]:
   base=sp(t+(.014 if sign>0 else 0));d=(tangent*.37+side*sign*.93+n*.05).normalized();cross=d.cross(n).normalized();width=length*.14
   end=base+d*length-n*length*.10
   mesh.add([base-cross*width*.42,base+cross*width*.42,end+cross*width*.07,end-cross*width*.07],[(0,1,2,3)],mat)

def double_feather(mesh,sp,mat):
 """Two short subordinate feathers + original rachis, 82 tri total per spray.
 Extra silhouette edges replace closed shell faces; this is a representation
 choice, not botanical proof of this exact two-fan grouping.
 """
 span=(sp(1)-sp(0)).length;side,n=frame(sp(1)-sp(0));rachis(mesh,sp,span,side,mat)
 for t,ll,sign in [(.12,.83,1),(.37,.65,-1)]:
  base=sp(t);tangent=(sp(t+.02)-sp(t-.02)).normalized()
  d=(tangent*.95+side*sign*.22+n*sign*.27).normalized()
  def lobe(u,base=base,d=d,ll=ll):return base+d*span*ll*u+n*span*ll*(.07*math.sin(math.pi*u)-.09*u*u)
  feather_lobe(mesh,lobe,mat)

def inherit_wood(source,upper):
 bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
 obj=next(o for o in bpy.data.objects if o.type=='MESH' and 'woody' in o.name)
 verts=[tuple(obj.matrix_world@x.co) for x in obj.data.vertices]
 names={g.index:g.name for g in obj.vertex_groups};selected=set()
 for x in obj.data.vertices:
  groups=[names[g.group] for g in x.groups]
  if (any(g.startswith(('tier5-bough','tier6-bough')) for g in groups) or ('main-leader' in groups and verts[x.index][2]>=4.95)) if upper else 'tier5-bough1' in groups:selected.add(x.index)
 faces=[(f.index,tuple(f.vertices)) for f in obj.data.polygons if all(i in selected for i in f.vertices)]
 used=sorted({i for _,face in faces for i in face});remap={old:new for new,old in enumerate(used)}
 return {'vertices':[verts[i] for i in used],'faces':[tuple(remap[i] for i in face) for _,face in faces],'original_vertex_indices':used,'original_face_indices':[i for i,_ in faces],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}

def shoots(config,upper):
 result=[]
 for tier in [4,5] if upper else [4]:
  row=config['tiers'][tier];z,L=row['height'],row['length']
  angles=row['angles'] if upper else row['angles'][:1]
  for j,degrees in enumerate(angles):
   a=math.radians(degrees);d=radial(a);side=radial(a+math.pi/2);length=L*[1.02,.91,1.07,.96,1.04][(j+tier)%5]
   start=axis(z+.065*math.sin(j*1.9+tier));droop=.05
   def bp(t):return start+d*length*t+side*(.07*math.sin(t*math.pi)*(1 if j%2 else -1))+v((0,0,-droop*math.sin(t*math.pi)+(.10+.035*tier)*t*t))
   layout=[(.33,-1),(.54,1),(.75,-1),(.94,.12)]
   for k,(t,lateral) in enumerate(layout):
    attachment=bp(t);terminal=k==len(layout)-1
    direction=(d*(1 if terminal else .63)+side*lateral*(.08 if terminal else .78)).normalized();ll=max(length*(.39+.055*math.sin(math.pi*t))*config['shoot_length_multiplier'],.20);lift=[-.12,.05,-.04,.14][k]
    def sp(u,attachment=attachment,direction=direction,ll=ll,d=d,lift=lift):return attachment+direction*ll*u+d*.020*u*u+v((0,0,ll*(-.16*math.sin(math.pi*u)+lift*u+.13*u*u)))
    result.append((f'tier{tier+1}-bough{j+1}-shoot{k+1}',sp,0 if tier==4 else 1))
 if upper:
  for i,(z,degrees,ll) in enumerate([(6.46,22,.28),(6.52,135,.25),(6.60,255,.23),(6.67,68,.20),(6.73,185,.17),(6.80,300,.14),(6.88,30,.13)]):
   d=(radial(math.radians(degrees))*.34+v((0,0,.93))).normalized();base=axis(z)
   def sp(t,base=base,d=d,ll=ll):return base+d*ll*t
   result.append((f'leader-shoot-{i}',sp,1))
 return result

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.output_dir.resolve()
 if out.exists() and any(out.iterdir()):raise RuntimeError('Fresh output directory required')
 out.mkdir(parents=True,exist_ok=True);config=json.loads((P/'study-config.json').read_text());source=P.parent/'candidate-r12/conifer-tree.blend';wood={k:inherit_wood(source,k=='upper') for k in ['unit','upper']};records=[]
 for variant in ['a-ribbon','b-feather']:
  for scope in ['unit','upper']:
   slug='conifer-'+scope;col=ac.setup_scene(slug,config['seed']);bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
   bark=ac.make_material('bark_warm',config['palette']['bark_warm'],roughness=.92)
   leaves=[ac.make_material(name,config['palette'][name],roughness=.92,double_sided=True) for name in ['needles_mid','young_growth']]
   w=wood[scope];ac.mesh_object('Unchanged r12 wood excerpt',w['vertices'],w['faces'],bark,col)
   mesh=Mesh();axes=shoots(config,scope=='upper')
   for label,sp,mat in axes:(ribbon_fan if variant=='a-ribbon' else double_feather)(mesh,sp,mat)
   obj=mesh.finish('Original thin needle surfaces | '+variant,leaves,col)
   meta={'description':{'en':'Local foliage representation study on unchanged wood excerpt; no whole-tree acceptance.','zh':'不改木骨架的局部针叶表示试验，非整树候选。'},'profile':'opaque double-sided thin needle surfaces, palette-only, no textures','scientific_status':'Modern foliage analogue only; artistic grouping and scale, no extinct-species reconstruction','provenance':'Original geometry. References consulted only, no external images or geometry incorporated.','generator':str(P.relative_to(REPO)/'build_units.py'),'variant':variant,'scope':scope,'semantic_counts':{'inherited_spray_axes':len(axes),'triangles_per_spray':106 if variant=='a-ribbon' else 82},'topology_notes':'Intentional open leaf surfaces with double-sided opaque material. Cut upper trunk is an exact open excerpt at the preexisting trunk ring near z=5; no caps added or wood vertices changed. No ground normalization; original meter-space coordinates preserved.'}
   result=ac.export_asset(slug,{'en':'Conifer local representation study','zh':'针叶局部表示试验'},'plants',col,meta,output_root=out/variant,render=False,max_triangles=6000,max_materials=3,max_primitives=3)
   assert (out/variant/slug/(slug+'.glb')).stat().st_size<=config['budgets']['max_glb_bytes']
   actual=[list(x.co) for x in next(o for o in col.all_objects if o.type=='MESH' and 'wood excerpt' in o.name).data.vertices]
   assert actual==[list(x) for x in w['vertices']], 'Inherited wood was changed'
   records.append({'variant':variant,'scope':scope,'triangles':result['triangles'],'bytes':result['glb_bytes'],'materials':json.loads((out/variant/slug/'qa.json').read_text())['glb']['materials'],'primitives':json.loads((out/variant/slug/'qa.json').read_text())['glb']['unique_mesh_primitives'],'sprays':len(axes),'foliage_triangles':sum(len(f)-2 for f in mesh.f),'wood_vertices':len(w['vertices']),'wood_triangles':sum(len(f)-2 for f in w['faces']),'wood_exact_vertex_equality':True,'wood_original_vertex_indices':w['original_vertex_indices'],'wood_original_face_indices':w['original_face_indices'],'source_blend_sha256':w['source_sha256'],'glb_sha256':result['sha256']['glb']})
 (out/'study-measurements.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps([{k:v for k,v in r.items() if not k.endswith('indices')} for r in records],indent=2))
if __name__=='__main__':main()
