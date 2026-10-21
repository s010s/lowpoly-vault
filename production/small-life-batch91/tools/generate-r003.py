#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Batch91 r003 coprolite radial-envelope repair; original freeze and r001 generator preserved."""
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
 p=c['parameters'];M=Mesh();H=p['trunk_top_height_m'];N=p['trunk_radial_segments'];path=[]
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
     direction=(sd*.36+spread*sign*.91+normal*.10).normalized();ep=lb+direction*ll;leaf(M,lb,ep,ll*p['leaf_width_to_length'],normal,2+(i+j+k+(sign+1)//2)%3,p['leaf_thickness_m'])
 # Three subtle closed oval scar nodules crossing the bark, not a scaly trunk texture.
 for j in range(p['branch_scar_count']):
  a=-1.3+j*2.5;z=.78+j*.23;r=p['trunk_base_diameter_m']/2*(1-.88*z/H);center=Vector((.055*sin(z/H*2),.028*sin(z/H*4),z))+Vector((cos(a),sin(a),0))*r*.98
  tangent=Vector((-sin(a),cos(a),0));normal=Vector((cos(a),sin(a),0));v=[]
  for s in [-1,1]:
   for k in range(8):ang=2*pi*k/8;v.append(center+tangent*.024*cos(ang)+Vector((0,0,.042*sin(ang)))+normal*(.003*s))
  f=[tuple(range(8))[::-1],tuple(range(8,16))]+[(k,(k+1)%8,(k+1)%8+8,k+8) for k in range(8)];M.add(v,f,1)
 lo=min(x[2] for x in M.v);hi=max(x[2] for x in M.v);scale=p['normalized_total_height_m']/(hi-lo);M.v=[(x*scale,y*scale,(z-lo)*scale) for x,y,z in M.v]
 M.emit('woody-tree-flattened-paddle-leafy-sprays',m,col)

def slab_poly(W,D):return [(-W*.48,-D*.38),(-W*.32,-D*.50),(W*.29,-D*.49),(W*.49,-D*.39),(W*.50,D*.31),(W*.34,D*.49),(-W*.29,D*.50),(-W*.49,D*.38)]

def cavity(host,col,m,poly,H,depth,floor_scale,tag):
 # Closed tapered cutter, bottom smaller than rim. Actual Boolean removes host material.
 n=len(poly);cx=sum(x for x,y in poly)/n;cy=sum(y for x,y in poly)/n;v=[]
 for scale,z in [(floor_scale,H-depth),(1.0,H),(1.01,H+.005)]:v.extend([(cx+(x-cx)*scale,cy+(y-cy)*scale,z) for x,y in poly])
 f=[tuple(range(n))[::-1]]
 for k in range(2):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 f.append(tuple(range(2*n,3*n)));C=Mesh();C.add(v,f,1);o=C.emit('temporary-cavity-'+tag,m,col)
 bpy.context.view_layer.objects.active=host;mod=host.modifiers.new('negative-impression-'+tag,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(o,do_unlink=True)

def tracks(c,m,col):
 p=c['parameters'];aid=c['asset_id'];W,D,H=p['slab_dimensions_m'];M=Mesh();extrude(M,slab_poly(W,D),0,H,0);host=M.emit('solid-sediment-with-six-negative-impressions',m,col);metadata=[]
 for i,(sg,y) in enumerate(zip(p['alternating_sides'],p['pair_y_m'])):
  x=sg*p['pes_center_x_abs_m'];angle=sg*.12
  def transform(shape,cx,cy):return [(cx+xx*cos(angle)-yy*sin(angle),cy+xx*sin(angle)+yy*cos(angle)) for xx,yy in shape]
  if aid.startswith('sauropod'):
   # Rounded subtriangular pes: broader anterior, narrower rounded heel.
   pl=p['pes_length_m'];pw=p['pes_width_m'];pes=[(-.25*pw,-.49*pl),(.14*pw,-.50*pl),(.43*pw,-.24*pl),(.50*pw,.12*pl),(.34*pw,.43*pl),(.06*pw,.50*pl),(-.30*pw,.40*pl),(-.50*pw,.08*pl),(-.45*pw,-.27*pl)]
   mw=p['manus_width_m'];ml=p['manus_length_m'];man=[(-.50*mw,-.22*ml),(-.43*mw,.23*ml),(-.20*mw,.48*ml),(.15*mw,.50*ml),(.43*mw,.29*ml),(.50*mw,-.18*ml),(.31*mw,-.37*ml),(.18*mw,-.13*ml),(-.03*mw,-.04*ml),(-.24*mw,-.13*ml),(-.40*mw,-.47*ml)];mx=x+sg*p['manus_extra_outward_m'];my=y+p['manus_forward_offset_m']
  else:
   pl=p['pes_length_m'];pw=p['pes_width_m'];pes=[(-.18*pw,-.50*pl),(.17*pw,-.50*pl),(.27*pw,-.38*pl),(.30*pw,-.09*pl),(.50*pw,.26*pl),(.31*pw,.47*pl),(-.18*pw,.50*pl),(-.48*pw,.29*pl),(-.29*pw,-.12*pl),(-.29*pw,-.38*pl)]
   # Outline has exactly 3 long/short fingers around a broad knuckle. The long digit points backwards/outwards.
   u=p['manus_extent_m'];man=[(-.07*u,-.08*u),(.10*u,-.16*u),(.42*u,-.66*u),(.50*u,-.64*u),(.30*u,-.09*u),(.52*u,.19*u),(.49*u,.27*u),(.17*u,.13*u),(.13*u,.38*u),(.05*u,.42*u),(-.02*u,.13*u),(-.11*u,.04*u)];man=[(xx*sg,yy) for xx,yy in man];mx=x+sg*p['manus_extra_outward_m'];my=y-p['manus_behind_offset_m']
  for role,shape,cx,cy in [('pes',pes,x,y),('manus',man,mx,my)]:
   poly=transform(shape,cx,cy);cavity(host,col,m,poly,H,p['impression_depth_m'],p['floor_shape_scale'],str(i)+'-'+role);metadata.append({'pair':i,'side':sg,'role':role,'outline_xy_m':poly})
 host['design_trace_pairs_json']=json.dumps(metadata);host['negative_relief_depth_m']=p['impression_depth_m'];host['factual_note']='Illustrative sequence, not specimen cast or identified producer.'


def coprolite(c,m,col):
 p=c['parameters'];M=Mesh();W,D,H=p['matrix_dimensions_m'];extrude(M,slab_poly(W,D),0,H,0);M.emit('subdued-irregular-matrix',m,col)
 L=p['body_length_m'];R=p['max_body_diameter_m']/2;N=p['body_axial_segments'];Q=p['body_radial_segments'];M=Mesh();v=[]
 for i in range(N+1):
  t=i/N;x=L*(t-.5);env=(p['blunt_end_radius_fraction']+(1-p['blunt_end_radius_fraction'])*sin(pi*.5*t/.35)) if t<.35 else (1-(1-p['tapered_end_radius_fraction'])*((t-.35)/.65)**1.6)
  for j in range(Q):
   a=2*pi*j/Q;phase=a-2*pi*p['broad_spiral_turns']*t;dist=math.atan2(sin(phase),cos(phase));sulcus=math.exp(-(dist/.37)**2);r=R*env*(1-p['relative_sulcus_depth']*sulcus);v.append((x,r*cos(a),p['body_center_z_m']+r*.92*sin(a)))
 # Explicit flat cap at blunt end and a near-point rounded taper with no loose coils.
 f=[tuple(range(Q))[::-1]];mi=[1]
 for i in range(N):
  for j in range(Q):
   a=i*Q+j;b=i*Q+(j+1)%Q;f.append((a,b,b+Q,a+Q));mi.append(1)
 f.append(tuple(range(N*Q,(N+1)*Q)));mi.append(2);M.v=v;M.f=f;M.mi=mi;M.emit('single-solid-three-turn-spiral-coprolite',m,col)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])]
 if aid=='archaeopteris':archaeopteris(cfg,m,col)
 elif aid=='spiral-coprolite':coprolite(cfg,m,col)
 else:tracks(cfg,m,col)
 bpy.context.view_layer.update();export_asset(aid,aid,'plants' if aid=='archaeopteris' else 'traces',col,metadata={'representation':'living-reconstruction' if aid=='archaeopteris' else 'trace-concept','export_texcoords':False,'source_scope':'Immutable original-brief.json. Original geometry, art scale, no trace-maker species assertion.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
