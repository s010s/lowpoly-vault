#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Skolithos r002 minimal radius repair, authored after repair-freeze.json."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy
from mathutils import Vector
from math import sin,cos,pi
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  n=len(self.v);self.v+=v;self.f += [tuple(n+x for x in face) for face in f];self.mi += [mi]*len(f)
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

def skolithos(c,m,col):
 p=c['parameters'];M=Mesh();W,D,H=p['block_dimensions_m'];
 poly=[(-.05,-.035),(-.040,-.035),(-.040,-.015),(-.020,-.015),(-.020,-.008),(.012,-.008),(.012,-.019),(.041,-.019),(.041,-.035),(.05,-.035),(.05,.035),(-.05,.035)]
 extrude(M,poly,0,H,0);host=M.emit('sectioned-host-sandstone',m,col)
 positions=[(-.03,-.015,.0044),(-.003,-.008,.0035),(.028,-.019,.0048),(-.035,.020,.0032),(-.010,.018,.0042),(.016,.018,.0026),(.036,.023,.0036)]
 # New r002 geometry input repairs only the lower-end shaft and its matching hole.
 repair=c['repair'];assert repair['affected_zero_based_shaft_index']==5
 assert repair['filled_shaft_target_radius_m']>=p['shaft_radius_range_m'][0]
 assert repair['filled_shaft_target_radius_m']<=p['shaft_radius_range_m'][1]
 assert abs(repair['hole_radius_m']*.999-repair['filled_shaft_target_radius_m'])<1e-18
 x,y,_=positions[5];positions[5]=(x,y,repair['hole_radius_m'])
 for i,(x,y,r) in enumerate(positions):
  cutter=Mesh();tube(cutter,[(x,y,-.001),(x,y,H+.001)],[r,r],p['shaft_radial_segments'],0);o=cutter.emit('temporary-shaft-cutter',m,col)
  bpy.context.view_layer.objects.active=host;mod=host.modifiers.new('exact-shaft-negative','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=o;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(o,do_unlink=True)
  # Filled shaft is exact hole complement, no coplanar surface overlay: host top has real hole.
  shaft=Mesh();tube(shaft,[(x,y,0),(x,y,H+.0006)],[r*.999,r*.999],p['shaft_radial_segments'],2);shaft.emit('continuous-filled-vertical-shaft-%02d'%i,m,col)
 # Join all intact source meshes into one editable multi-material mesh; closed components kept.
 objs=[o for o in bpy.data.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=host;bpy.ops.object.join()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(args.config).read_text());aid=cfg['asset_id'];out=Path(args.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-palette-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])]
 {'skolithos-pipe-field':skolithos}[aid](cfg,m,col);bpy.context.view_layer.update()
 export_asset(aid,aid,'plants' if aid=='psilophyton' else 'traces',col,metadata={'representation':'living-reconstruction' if aid=='psilophyton' else 'trace-concept','export_texcoords':False,'source_scope':'Immutable original-brief.json; original geometry; no creator species for trace.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 r={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(args.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
