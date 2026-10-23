#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Huayangosaurus, Blender 4.3.2, meters, head -Y.
Usage: blender -b -t 2 --factory-startup --python-exit-code 1 --python source/generate.py -- --output /tmp/build
The generator reads only its adjacent params.json and vendored deps. Render-only diagnostics are separate.
"""
from pathlib import Path
import sys, json, math, argparse, hashlib
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
P=json.loads((HERE/'params.json').read_text())
COL=setup_scene(P['asset_id'],P['seed'])
M=[make_material(n,c) for n,c in P['palette']]
class Assembly:
 def __init__(self,name):self.name=name;self.v=[];self.f=[];self.m=[];self.groups=[]
 def add(self,name,v,f,mi=0):
  off=len(self.v);self.v.extend(v);self.f.extend([tuple(off+i for i in face) for face in f]);self.m.extend(mi if isinstance(mi,list) else [mi]*len(f));self.groups.append((name,off,len(v)))
 def finish(self):
  v=[(x,y+P['footprint_center_offset_y_m'],z) for x,y,z in self.v]
  ob=mesh_object(self.name,v,self.f,M,COL)
  for poly,idx in zip(ob.data.polygons,self.m):poly.material_index=idx
  for name,off,count in self.groups:ob.vertex_groups.new(name=name).add(list(range(off,off+count)),1,'REPLACE')
  ob['semantic_components']=json.dumps([g[0] for g in self.groups]);return ob
skin=Assembly('skin-continuous-trunk-and-articulated-limbs');armor=Assembly('paired-small-plates-and-shoulder-spines');horn=Assembly('terminal-spines-and-pedal-nails');features=Assembly('eyes-nostrils-and-closed-mouth')
def loft_y(group,name,rings,n=16,mat=0,belly=False):
 v=[]
 for y,x,z,rx,rz in rings:
  for j in range(n):
   a=2*math.pi*j/n;v.append((x+rx*math.cos(a),y,z+rz*math.sin(a)))
 f=[tuple(reversed(range(n)))];mi=[mat]
 for i in range(len(rings)-1):
  for j in range(n):
   f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j));mi.append(1 if belly and math.sin((j+.5)*2*math.pi/n)<-.55 else mat)
 f.append(tuple((len(rings)-1)*n+j for j in range(n)));mi.append(mat);group.add(name,v,f,mi)
def loft_z(group,name,rings,n=10,mat=0):
 v=[]
 for x,y,z,rx,ry in rings:
  for j in range(n):
   a=2*math.pi*j/n;v.append((x+rx*math.cos(a),y+ry*math.sin(a),z))
 f=[tuple(reversed(range(n)))]
 for i in range(len(rings)-1):
  for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
 f.append(tuple((len(rings)-1)*n+j for j in range(n)));group.add(name,v,f,mat)
def ellipsoid(group,name,c,r,mat,n=10,levels=5):
 v=[(c[0],c[1],c[2]-r[2])]
 for k in range(1,levels):
  p=-math.pi/2+math.pi*k/levels
  for j in range(n):
   a=2*math.pi*j/n;v.append((c[0]+r[0]*math.cos(p)*math.cos(a),c[1]+r[1]*math.cos(p)*math.sin(a),c[2]+r[2]*math.sin(p)))
 v.append((c[0],c[1],c[2]+r[2]));f=[]
 for j in range(n):f.append((0,1+(j+1)%n,1+j))
 for k in range(levels-2):
  for j in range(n):f.append((1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j))
 for j in range(n):f.append((len(v)-1,1+(levels-2)*n+j,1+(levels-2)*n+(j+1)%n))
 group.add(name,v,f,mat)
def spike(group,name,points,radii,mat=3,n=8):
 axis=(Vector(points[-1])-Vector(points[0])).normalized();u=axis.cross(Vector((0,0,1)))
 if u.length<.1:u=axis.cross(Vector((0,1,0)))
 u.normalize();w=axis.cross(u).normalized();v=[]
 for p,r in zip(points[:-1],radii[:-1]):
  for j in range(n):v.append(tuple(Vector(p)+r*(u*math.cos(2*math.pi*j/n)+w*math.sin(2*math.pi*j/n))))
 v.append(tuple(points[-1]));f=[tuple(reversed(range(n)))]
 for k in range(len(points)-2):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 off=(len(points)-2)*n
 for j in range(n):f.append((off+j,off+(j+1)%n,len(v)-1))
 group.add(name,v,f,mat)
# Profile-driven axial surface: broad abbreviated head, descending neck, barrel trunk and long tapering tail.
profiles=[(-1.9,.09,.69,.07),(-1.78,.185,.705,.115),(-1.61,.215,.77,.15),(-1.44,.19,.79,.165),(-1.28,.145,.815,.15),(-1.13,.17,.87,.20),(-.95,.27,.98,.295),(-.75,.38,1.035,.38),(-.45,.46,1.08,.445),(-.1,.49,1.105,.475),(.25,.48,1.11,.47),(.55,.42,1.075,.45),(.78,.33,1.0,.385),(1.0,.24,.875,.29),(1.25,.18,.755,.205),(1.55,.13,.66,.135),(1.85,.095,.60,.095),(2.15,.067,.545,.067),(2.4,.036,.49,.036),(2.6,.005,.445,.005)]
loft_y(skin,'continuous-head-neck-trunk-tail',[(y,0,z,rx,rz) for y,rx,z,rz in profiles],16,0,True)
# Near-equal effective limb lengths. Elbow and hock contours are lofted, not sphere stacks.
for s in (-1,1):
 side='left' if s<0 else 'right'
 loft_z(skin,side+'-forelimb',[(s*.29,-.72,1.10,.19,.21),(s*.37,-.70,.88,.17,.18),(s*.405,-.58,.63,.115,.13),(s*.415,-.66,.40,.092,.105),(s*.415,-.75,.17,.087,.09),(s*.415,-.78,.095,.10,.12)],10)
 loft_z(skin,side+'-hindlimb',[(s*.29,.47,1.17,.235,.27),(s*.36,.45,.89,.22,.24),(s*.41,.34,.66,.155,.17),(s*.425,.50,.44,.105,.115),(s*.43,.54,.18,.092,.105),(s*.43,.50,.09,.11,.13)],10)
 # Forefoot low five-lobed arc, hindfoot three weightbearing toes. Claws are simplified keratin, not an exact osteological claim.
 for fore,base_y in [(True,-.80),(False,.50)]:
  footname=side+('-forefoot' if fore else '-hindfoot');x=s*(.415 if fore else .43)
  loft_z(skin,footname,[(x,base_y,0,.135,.16),(x,base_y,.085,.15,.18),(x,base_y+.015,.17,.105,.115)],10)
  toes=5 if fore else 3
  for t in range(toes):
   dx=(t-(toes-1)/2)*(.049 if fore else .075)
   cy=base_y-.11+abs(dx)*.28
   ellipsoid(skin,f'{footname}-digit-{t+1}',(x+dx,cy,.058),(.039 if fore else .052,.115,.058),0,8,4)
   if not fore or t in (1,2):
    spike(horn,f'{footname}-nail-{t+1}',[(x+dx,cy-.055,.05),(x+dx,cy-.125,.035),(x+dx,cy-.162,.025)],[.029,.022,0],3,6)
# Twelve homologous pairs, deliberately small and narrow rather than giant alternating diamonds.
plate_specs=[(-1.16,.115,1.02,.10,.09),(-.96,.13,1.21,.14,.11),(-.72,.15,1.38,.23,.145),(-.43,.17,1.50,.30,.17),(-.10,.18,1.565,.345,.185),(.23,.18,1.56,.355,.19),(.55,.165,1.49,.32,.175),(.83,.14,1.33,.27,.15),(1.10,.115,1.10,.22,.125),(1.36,.09,.87,.17,.105),(1.60,.07,.77,.13,.09),(1.80,.055,.68,.095,.075)]
for i,(y,x,z,h,wid) in enumerate(plate_specs):
 for s in (-1,1):
  # Faceted lenticular triangular blade; thick ridge, sharp but nonzero tip.
  cx=s*x;th=.026 if i<8 else .016
  outline=[(y-wid,z-.055),(y+wid,z-.045),(y+wid*.38,z+h*.56),(y-wid*.14,z+h),(y-wid*.60,z+h*.52)]
  v=[(cx+s*.015,yy,zz) for yy,zz in outline]+[(cx+th,y,z+h*.36),(cx-th,y,z+h*.36)]
  f=[]
  for j in range(5):f.extend([(5,j,(j+1)%5),(6,(j+1)%5,j)])
  armor.add(f'paired-dorsal-plate-{i+1:02d}-'+('left' if s<0 else 'right'),v,f,2)
# One parascapular spine per side, rooted at shoulders, not hips.
for s in (-1,1):
 spike(armor,'parascapular-shoulder-spine-'+str(s),[(s*.28,-.72,1.07),(s*.50,-.69,1.09),(s*.77,-.54,1.02),(s*.98,-.39,.99)],[.10,.087,.045,0],2,8)
 # Two pairs of distal tail spikes, conspicuous in dorsal and perspective views.
 for i,(y,l,z) in enumerate([(1.96,.48,.59),(2.30,.39,.51)]):
  spike(horn,f'terminal-tail-spine-{i+1}-'+str(s),[(s*.055,y,z),(s*.20,y+.025,z+.035),(s*l,y+.19,z+.105)],[.069,.045,0],3,8)
 # Recessed lateral eyes under brow and closed oral commissure.
 ellipsoid(features,'eye-socket-'+str(s),(s*.194,-1.61,.841),(.025,.048,.039),4,10,5)
 ellipsoid(features,'amber-iris-'+str(s),(s*.214,-1.622,.845),(.012,.021,.023),5,10,5)
 ellipsoid(features,'pupil-'+str(s),(s*.225,-1.626,.845),(.006,.009,.014),4,8,4)
 ellipsoid(features,'nostril-'+str(s),(s*.147,-1.805,.758),(.011,.027,.014),4,8,4)
 # Fine closed mouth seam, not an open toothless beak.
 seam=[(-1.88,s*.105,.675,.005,.005),(-1.78,s*.175,.657,.006,.006),(-1.62,s*.195,.651,.006,.006),(-1.47,s*.174,.676,.004,.004)]
 loft_y(features,'closed-mouth-line-'+str(s),seam,6,4)
for g in (skin,armor,horn,features):g.finish()
root=bpy.data.objects[COL['asset_root']];root['reconstruction']='Huayangosaurus taibaii, muted living reconstruction; paired plates and spine pose are interpretive.'
root['plate_pairs']=12;root['shoulder_spines']=2;root['terminal_tail_spines']=4
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);args=a.parse_args(argv)
args.output.mkdir(parents=True,exist_ok=True)
record=export_asset(P['asset_id'],{'en':'Huayangosaurus','zh':'华阳龙'},'animals',COL,metadata={'generator':'source/generate.py','representation':'living-reconstruction','export_texcoords':False},output_root=args.output/'canonical',render=False,max_triangles=P['max_triangles'],max_materials=P['max_materials'],max_primitives=P['max_primitives'])
src=args.output/'canonical'/P['asset_id']
import shutil
shutil.copy2(src/(P['asset_id']+'.glb'),args.output/'model.glb');shutil.copy2(src/(P['asset_id']+'.blend'),args.output/'model.blend')
qa=json.loads((src/'qa.json').read_text());(args.output/'technical.json').write_text(json.dumps(qa,indent=2)+'\n')
record['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();record['params_sha256']=hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()
record['exporter_version']=list(__import__('io_scene_gltf2').bl_info['version'])
(args.output/'build.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
print('BUILD_COMPLETE',args.output,qa['source']['triangles'],qa['glb']['semantic_sha256'])
