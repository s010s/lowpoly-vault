# SPDX-License-Identifier: MIT
import argparse,json,math,sys,pathlib,random
import bpy
from mathutils import Vector
ROOT=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,link_object,ground_asset,export_asset

def loft(name,rings,n,mat,col):
 v=[]
 for z,rx,ry,cx,cy,amp in rings:
  for j in range(n):
   a=2*math.pi*j/n; f=1+amp*(.6*math.cos(7*a+.7*z)+.4*math.cos(11*a-2*z))
   v.append((cx+rx*f*math.cos(a),cy+ry*f*math.sin(a),z))
 f=[tuple(reversed(range(n)))]
 for k in range(len(rings)-1):
  for j in range(n):a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
 f.append(tuple((len(rings)-1)*n+j for j in range(n)))
 return mesh_object(name,v,f,mat,col)

def build(cfg,out):
 id=cfg['asset_id'];col=setup_scene(id,57);random.seed(57)
 mats=[make_material(n,c) for n,c in [('stone','#A88A65'),('fresh-break','#CDB58B'),('interior','#8B6A45'),('rim','#D7BC8A')]]
 if id=='cave-column':
  rings=[]
  for z,r in [(0,1.15),(.13,1.25),(.23,.91),(.38,.62),(.65,.48),(.95,.36),(1.25,.29),(1.6,.26),(1.95,.28),(2.25,.34),(2.55,.48),(2.78,.69),(2.9,1.15),(3.04,1.22),(3.15,1.02)]:
   rings.append((z,r,r*.77,.045*math.sin(z*2),.035*math.sin(z*3),.16 if .23<z<2.9 else .07))
  obj=loft('continuous-fluted-column-and-attachments',rings,48,mats,col)
  for p in obj.data.polygons:
   p.material_index=1 if p.center.z>100 else 0
  # assign structural light ridges by position after mesh update
  for p in obj.data.polygons:
   a=math.atan2(p.center.y,p.center.x);p.material_index=1 if math.cos(7*a)>.55 else 0
 elif id=='nidula-baltica':
  # Narrow vase, thick continuous wall, inner floor elevated to reveal peridiole.
  s=.05
  rings=[(0,.24*s,.24*s,0,0,.04),(.2*s,.28*s,.28*s,0,0,.04),(1.2*s,.42*s,.42*s,.02*s,0,.035),(2.2*s,.51*s,.51*s,.02*s,0,.035),(2.65*s,.6*s,.6*s,0,0,.035),(2.65*s,.51*s,.51*s,0,0,.035),(2.2*s,.43*s,.43*s,0,0,.02),(1.2*s,.33*s,.33*s,0,0,.02),(.65*s,.12*s,.12*s,0,0,0)]
  cup=loft('two-sided-narrow-vase-cup',rings,40,mats[:3],col)
  for p in cup.data.polygons:p.material_index=2 if p.index>4*40 else 0
  # original limited overlapping scale wedges, not asserted hidden anatomy
  v=[];f=[]
  for row in range(3):
   n=20;z=(2.12+row*.19)*s;r=(.50+row*.04)*s
   for j in range(n):
    a=2*math.pi*(j+.35*row)/n;rr=r+.015*s;w=.13;hh=(.24+.035*math.sin(j*2))*s
    coords=[]
    for da,rad,dz in [(-w,rr,-.10*s),(w,rr,-.10*s),(w*.75,rr+.09*s,hh*.7),(0,rr+.07*s,hh),(-w*.75,rr+.09*s,hh*.7),(0,rr-.025*s,.01*s)]:coords.append((rad*math.cos(a+da),rad*math.sin(a+da),z+dz))
    k=len(v);v+=coords;f += [tuple(k+i for i in face) for face in [(0,1,5),(1,2,5),(2,3,5),(3,4,5),(4,0,5),(0,4,3,2,1)]]
  mesh_object('overlapping-upturned-rim-scales',v,f,mats[3],col)
  bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=10,location=(0,-.002,.047))
  obj=bpy.context.object;obj.name='single-lenticular-peridiole';obj.scale=(.011,.0085,.0036);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);obj.data.materials.append(mats[1]);link_object(obj,col)
 elif id=='quatsinoporites':
  # Original broken fragment: one closed irregular boundary, boolean pore depths.
  poly=[(-.062,-.027),(-.043,-.044),(-.014,-.041),(.004,-.035),(.032,-.043),(.058,-.021),(.048,-.005),(.063,.017),(.036,.039),(.009,.034),(-.012,.045),(-.033,.029),(-.055,.022),(-.05,.005)]
  n=len(poly);v=[(x,y,z) for z in [0,.027] for x,y in poly];f=[tuple(reversed(range(n))),tuple(n+j for j in range(n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
  obj=mesh_object('abraded-fractured-pore-layer',v,f,mats,col)
  for p in obj.data.polygons:p.material_index=1 if p.index>1 else 0
  cutters=[]
  for row in range(7):
   for j in range(9):
    x=-.047+j*.0118+(row%2)*.0053;y=-.029+row*.010
    if (x/.052)**2+(y/.035)**2>1:continue
    rad=.0031+random.random()*.00125
    bpy.ops.mesh.primitive_cone_add(vertices=12,radius1=rad*.76,radius2=rad,depth=.025,location=(x,y,.023))
    c=bpy.context.object;c.scale.y=.85+random.random()*.35;cutters.append(c)
  bpy.ops.object.select_all(action='DESELECT')
  for c in cutters:c.select_set(True)
  bpy.context.view_layer.objects.active=cutters[0];bpy.ops.object.join();c=bpy.context.object
  bpy.context.view_layer.objects.active=obj;mod=obj.modifiers.new('structural-round-elliptical-pore-depth','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=c;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(c,do_unlink=True)
  for idx in reversed(range(len(obj.data.materials))):
   if obj.data.materials[idx] is None:obj.data.materials.pop(index=idx)
 elif id=='rusophycus-resting-excavation':
  n=59;v=[]
  for j in range(n):
   y=-.078+.156*j/(n-1)
   for i in range(n):
    x=-.09+.18*i/(n-1);dep=0;score=0
    for sign in [-1,1]:
     q=((x-sign*.025)/.028)**2+(y/.049)**2
     if q<1:
      dep=max(dep,.027*(1-q)**.6)
      # paired diagonal gouges recessed into each concave lobe floor
      phase=(y+sign*.45*(x-sign*.025))/.010
      groove=max(0,math.cos(2*math.pi*phase))**12
      score=max(score,.0027*groove*(1-q)**.5)
    z=.045-dep-score+.0005*math.sin(x*60)*math.cos(y*58)
    u=x/.09;vv=y/.078;cut=1-.12*abs(u*vv)**4;v.append((x*cut+.0014*math.sin(vv*8)*abs(u)**8,y*cut+.0015*math.cos(u*7)*abs(vv)**8,z))
  f=[]
  for j in range(n-1):
   for i in range(n-1):a=j*n+i;f.extend([(a,a+1,a+n+1),(a,a+n+1,a+n)])
  edge=list(range(n))+[j*n+n-1 for j in range(1,n)]+[n*(n-1)+i for i in range(n-2,-1,-1)]+[j*n for j in range(n-2,0,-1)]
  k=len(v)
  for a in edge:v.append((v[a][0],v[a][1],0))
  for j,a in enumerate(edge):b=edge[(j+1)%len(edge)];f.append((a,k+j,k+(j+1)%len(edge),b))
  f.append(tuple(reversed(range(k,len(v)))))
  obj=mesh_object('short-deep-bilobed-negative-and-scratch-fields',v,f,mats[:2],col)
  for p in obj.data.polygons:p.material_index=1 if p.center.z<.003 else 0
 ground_asset(col,center_xy=True)
 return export_asset(id,cfg['title'],cfg['category'],col,output_root=out.parent,render=False,diagnostics=False,max_triangles=14000,max_materials=6,max_primitives=30,metadata={'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'scale_note':cfg['scale_note'],'reconstruction_notes':cfg['scope'],'generator':'generator.py','export_texcoords':False})

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output-dir',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.load(open(a.config));out=pathlib.Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
 # helper appends asset_id; use staging parent, then move helper outputs to exact revision folder
 temp=out/'_export';rec=build(cfg,temp/cfg['asset_id'])
 for f in (temp/cfg['asset_id']).iterdir():f.rename(out/f.name)
 (temp/cfg['asset_id']).rmdir();temp.rmdir()
if __name__=='__main__':main()
