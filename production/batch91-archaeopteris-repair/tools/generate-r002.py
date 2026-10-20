#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch91 original geometry, authored only after immutable original freeze."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from math import sin,cos,pi
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  n=len(self.v);self.v.extend([tuple(x) for x in v]);self.f.extend([tuple(n+x for x in face) for face in f]);self.mi.extend([mi]*len(f))
 def emit(self,name,m,col):
  o=mesh_object(name,self.v,self.f,m,col)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i
  return o

def tube(M,points,radii,sides,mat):
 v=[]
 for i,pp in enumerate(points):
  p=Vector(pp);t=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])).normalized();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();w=t.cross(u).normalized()
  for j in range(sides):v.append(tuple(p+radii[i]*(u*cos(2*pi*j/sides)+w*sin(2*pi*j/sides))))
 f=[tuple(range(sides))[::-1]]
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 f.append(tuple(range((len(points)-1)*sides,len(points)*sides)));M.add(v,f,mat)

def extrude(M,poly,z0,z1,mat):
 n=len(poly);v=[(x,y,z) for z in (z0,z1) for x,y in poly];f=[tuple(range(n))[::-1],tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)];M.add(v,f,mat)

def leaf(M,base,tip,width,normal,mat,thick):
 b=Vector(base);e=Vector(tip);axis=e-b;n=Vector(normal).normalized();side=n.cross(axis).normalized();L=axis.length
 # Broad paddle blade, not a needle. Closed biconvex six-edge blade.
 coords=[b,b+axis*.28+side*width*.40,b+axis*.74+side*width*.50,e,b+axis*.74-side*width*.50,b+axis*.28-side*width*.40]
 v=coords+[b+axis*.57+n*thick*.5,b+axis*.57-n*thick*.5];f=[]
 for j in range(6):f.extend([(j,(j+1)%6,6),((j+1)%6,j,7)])
 M.add(v,f,mat)

def archaeopteris(c,m,col):
 p=c['parameters'];M=Mesh();leaf_records=[];H=p['trunk_top_height_m'];N=p['trunk_radial_segments'];path=[]
 for i in range(12):
  t=i/11;path.append((.055*sin(t*2.0),.028*sin(t*4),H*t))
 radii=[p['trunk_base_diameter_m']/2*(1-.88*(i/11)) for i in range(12)];radii[0]*=1.33;tube(M,path,radii,N,0)
 for j in range(p['root_count']):
  a=2*pi*j/p['root_count']+.11*sin(j*1.7);r=p['root_radius_m']*(.84+.14*sin(j*2.2));tube(M,[(0,0,.22),(r*.32*cos(a),r*.32*sin(a),.14),(r*.73*cos(a),r*.73*sin(a),.044),(r*cos(a),r*sin(a),.008)],[.075,.057,.025,.006],6,0)
 for i in range(p['structural_limb_count']):
  a=i*2.399963+.13*sin(i*2.3);z=1.40+i*.133;start=Vector((.055*sin(z/H*2),.028*sin(z/H*4),z));d=Vector((cos(a),sin(a),0));side=Vector((-sin(a),cos(a),0));L=1.05-.024*i;end=start+d*L+Vector((0,0,.51+.018*i));mid=start+d*L*.50+Vector((0,0,.23+.008*i));tube(M,[start,mid,end],[.065*(1-i*.035),.036*(1-i*.027),.013],p['branch_radial_segments'],0)
  for k in range(p['sprays_per_limb']):
   t=.42+.17*k;q=start.lerp(end,t);sg=-1 if k%2 else 1;sd=(d*.62+side*sg*.70+Vector((0,0,.20))).normalized();length=.53-.025*k;tip=q+sd*length;normal=sd.cross(side).normalized()
   if normal.z<0:normal=-normal
   tube(M,[q,q.lerp(tip,.50),tip],[.010,.006,.002],5,1)
   for j in range(p['leaf_pairs_per_spray']):
    tt=.16+j*.135;lb=q.lerp(tip,tt);ll=p['leaf_length_range_m'][1]-(p['leaf_length_range_m'][1]-p['leaf_length_range_m'][0])*(j/5);spread=normal.cross(sd).normalized()
    for sign in [-1,1]:
     direction=(sd*.36+spread*sign*.91+normal*.10).normalized();ep=lb+direction*ll;first=len(M.v);leaf(M,lb,ep,ll*p['leaf_width_to_length'],normal,2+(i+j+k+(sign+1)//2)%3,p['leaf_thickness_m']);leaf_records.append((first,tuple(lb),ll))
 # Three subtle closed oval scar nodules crossing the bark, not a scaly trunk texture.
 for j in range(p['branch_scar_count']):
  a=-1.3+j*2.5;z=.78+j*.23;r=p['trunk_base_diameter_m']/2*(1-.88*z/H);center=Vector((.055*sin(z/H*2),.028*sin(z/H*4),z))+Vector((cos(a),sin(a),0))*r*.98
  tangent=Vector((-sin(a),cos(a),0));normal=Vector((cos(a),sin(a),0));v=[]
  for s in [-1,1]:
   for k in range(8):ang=2*pi*k/8;v.append(center+tangent*.024*cos(ang)+Vector((0,0,.042*sin(ang)))+normal*(.003*s))
  f=[tuple(range(8))[::-1],tuple(range(8,16))]+[(k,(k+1)%8,(k+1)%8+8,k+8) for k in range(8)];M.add(v,f,1)
 # r002: actual leaf offsets keep meter dimensions; only attachment skeleton is normalized.
 lo=min(x[2] for x in M.v);old_hi=max(x[2] for x in M.v);old_scale=p['normalized_total_height_m']/(old_hi-lo)
 local={}
 for first,base,ll in leaf_records:
  for j in range(8):local[first+j]=(base,tuple(M.v[first+j][k]-base[k] for k in range(3)))
 envelope=[]
 for index,v in enumerate(M.v):
  base,offset=local.get(index,(v,(0.,0.,0.)));a=base[2]-lo;b=offset[2]
  if a>0:envelope.append((p['normalized_total_height_m']-b)/a)
 scale=min(envelope)
 corrected=[]
 for index,v in enumerate(M.v):
  base,offset=local.get(index,(v,(0.,0.,0.)));corrected.append((base[0]*scale+offset[0],base[1]*scale+offset[1],(base[2]-lo)*scale+offset[2]))
 M.v=corrected
 assert abs(max(v[2] for v in M.v)-p['normalized_total_height_m'])<1e-10 and abs(min(v[2] for v in M.v))<1e-10
 bpy.context.scene['repair_normalization']=json.dumps({'old_scale':old_scale,'skeleton_scale':scale,'relative_skeleton_scale_change':scale/old_scale-1,'leaf_local_dimensions_scaled':False,'leaf_count':len(leaf_records)})
 M.emit('woody-tree-flattened-paddle-leafy-sprays',m,col)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])]
 assert aid=='archaeopteris';archaeopteris(cfg,m,col)
 bpy.context.view_layer.update();export_asset(aid,aid,'plants' if aid=='archaeopteris' else 'traces',col,metadata={'representation':'living-reconstruction' if aid=='archaeopteris' else 'trace-concept','export_texcoords':False,'source_scope':'Immutable original-brief.json. Original geometry, art scale, no trace-maker species assertion.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
