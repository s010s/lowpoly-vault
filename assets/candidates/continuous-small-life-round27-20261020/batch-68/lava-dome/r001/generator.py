# SPDX-License-Identifier: MIT
"""Original batch68 geometry; deterministic Blender4.3.2, palette-only. No reference meshes."""
import bpy,sys,json,math,argparse,pathlib,datetime,hashlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
from asset_common import setup_scene,mesh_object,make_material,audit_source,ground_asset
from qa_glb import audit_glb
P=argparse.ArgumentParser();P.add_argument('--config',required=True);P.add_argument('--output',required=True);a=P.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(pathlib.Path(a.config).read_text());out=pathlib.Path(a.output);out.mkdir(parents=True,exist_ok=True)
slug=cfg['asset_id'];col=setup_scene(slug,cfg['seed']);m={k:make_material(k,v) for k,v in cfg['palette'].items()};groups={}
def part(name,vs,fs,mat):
 v,f=groups.setdefault((name,mat),([],[]));n=len(v);v.extend(vs);f.extend([tuple(n+i for i in face) for face in fs])
def loft(name,rings,mat):
 n=len(rings[0]);vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))]
 for j in range(len(rings)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));part(name,vs,fs,mat)
def tube(name,points,radii,mat,n=6):
 rings=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.95 else Vector((1,0,0));u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
  rings.append([tuple(Vector(p)+radii[i]*(u*math.cos(j*math.tau/n)+w*math.sin(j*math.tau/n))) for j in range(n)])
 loft(name,rings,mat)
def ellipsoid(name,c,r,mat,n=12,k=6):
 rings=[]
 for j in range(k+1):
  t=-math.pi/2+.15+(math.pi-.30)*j/k
  rings.append([(c[0]+r[0]*math.cos(t)*math.cos(i*math.tau/n),c[1]+r[1]*math.cos(t)*math.sin(i*math.tau/n),c[2]+r[2]*math.sin(t)) for i in range(n)])
 loft(name,rings,mat)


# Original batch68 geometry authored only after immutable freezes at2026-10-20T13:59:28Z.
import random
rng=random.Random(cfg['seed'])
def thaumaptilon():
 def width(t):return .025*math.sin(math.pi*t)**.56*(.92+.12*t)
 def cy(t):return .0018*math.sin(t*math.pi)
 rings=[]
 for i in range(53):
  t=.005+.99*i/52;z=.027+.183*t;w=width(t);th=.0016*(.55+.45*math.sin(math.pi*t))
  rings.append([(w*math.cos(k*math.tau/12),cy(t)+th*math.sin(k*math.tau/12),z) for k in range(12)])
 loft('continuous_common_base_frond_lamina',rings,'frond')
 tube('central_axis_and_short_blunt_attachment',[(0,0,.004),(0,0,.025),(0,.001,.10),(0,0,.210)],[.0028,.0020,.0015,.0005],'axis',8)
 ellipsoid('blunt_basal_attachment',(0,0,.005),(.004,.003,.005),'frond',10,4)
 for side in [-1,1]:
  for j in range(18):
   z=.034+j*.0085;endz=z+.019;te=min(.98,(endz-.027)/.183);w=width(te)*(.95-.035*math.sin(j*1.4))
   # Continuous sheet underneath all oblique structures, no free fern leaflets.
   for face in [-1,1]:
    points=[]
    for q in range(4):
     u=q/3;zz=z+(endz-z)*u;tt=(zz-.027)/.183;points.append((side*w*u,cy(tt)+face*(.0016*math.sqrt(max(.01,1-(w*u/max(.0001,width(tt)))**2))+.0001),zz))
    tube(('front' if face<0 else 'rear')+'_oblique_connected_lateral_relief',points,[.00065,.0008,.00065,.00025],'ridge' if face<0 else 'frond',6)
 # Irregular front-only low pustules, not neat combs or asserted zooids.
 for j in range(29):
  t=rng.uniform(.13,.87);x=rng.uniform(-.77,.77)*width(t);y=cy(t)-.0016*math.sqrt(1-(x/width(t))**2)
  ellipsoid('front_only_uncertain_pustules',(x,y-.0001,.027+.183*t),(.00065,.00037,.0006),'pustule',6,3)

def fin():
 nx=32;nz=8;vs=[];fs=[];mats=[]
 for face in [-1,1]:
  for j in range(nz+1):
   t=j/nz
   for i in range(nx+1):
    x=-8+16*i/nx;crest=9+.7*math.sin(i*.49)+.3*math.sin(i*1.7);z=t*crest
    half=.65+.22*(1-t)**4+.10*math.sin(i*.71)+.05*math.sin(i*1.9+j*.5)
    vs.append((x,face*half,z))
 stride=(nx+1)*(nz+1)
 for face in range(2):
  for j in range(nz):
   for i in range(nx):
    a=face*stride+j*(nx+1)+i;b=a+nx+1;fs.append((a,a+1,b+1,b));z=(vs[a][2]+vs[b][2])/2;mats.append('pale' if 3.2<z<4.8 else 'rust' if z>7.2 else 'rock')
 perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,nz+1)]+[nz*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(nz-1,0,-1)]
 for k,a in enumerate(perimeter):b=perimeter[(k+1)%len(perimeter)];fs.append((a,b,b+stride,a+stride));mats.append('foot' if vs[a][2]<.01 else 'rock')
 obj=mesh_object('single_thin_joint_bounded_sandstone_wall',vs,fs,[m[k] for k in cfg['palette']],col);keys=list(cfg['palette'])
 for p,k in zip(obj.data.polygons,mats):p.material_index=keys.index(k)

def lava_dome():
 n=40;rings=[];levels=[(0,1),(.07,.97),(.23,.88),(.51,.80),(.77,.68),(.95,.48),(1,.25)]
 for j,(h,r) in enumerate(levels):
  ring=[]
  for i in range(n):
   a=i*math.tau/n;ir=1+.09*math.sin(i*2.3+j*1.1)+.075*math.cos(i*.72+j*1.57);z=45*h*(1+.04*math.sin(i*.8+j*1.6))
   ring.append((60*r*ir*math.cos(a)+2*h,50*r*ir*math.sin(a),z))
  rings.append(ring)
 loft('steep_bulbous_extrusion_coherent_solid',rings,'core')
 def block(name,c,s,mat,a):
  # Angular flat-face fractured rock unit, deliberately not rounded boulder.
  pts=[]
  for level in [0,1]:
   for i in range(5):
    t=a+i*math.tau/5;rr=1+.24*math.sin(i*2.9+a+level*1.3)
    pts.append((c[0]+s[0]*rr*math.cos(t)+(s[0]*.23*math.sin(a) if level else 0),c[1]+s[1]*rr*math.sin(t),c[2]+s[2]*(level-.5)*(1+.1*math.sin(i+a))))
  loft(name,[pts[:5],pts[5:]],mat)
 for j in range(74):
  a=j*2.399963+rng.uniform(-.2,.2);h=rng.uniform(.18,.92);rad=1
  for (za,ra),(zb,rb) in zip(levels,levels[1:]):
   if za<=h<=zb:rad=ra+(rb-ra)*(h-za)/(zb-za);break
  c=(60*rad*1.055*math.cos(a),50*rad*1.055*math.sin(a),45*h)
  block('embedded_brecciated_angular_rind',c,(rng.uniform(5,9),rng.uniform(5,8),rng.uniform(7,14)),['block','dark','core'][j%3],a)
 for j in range(36):
  a=j*math.tau/36;rad=1+.025*math.sin(j*1.5);c=(57*rad*math.cos(a),47*rad*math.sin(a),rng.uniform(1,2.4));block('subordinate_basal_rubble',c,(rng.uniform(2,4),rng.uniform(2,3.5),rng.uniform(2,4)), 'rubble' if j%4==0 else 'block',a)

def ice_ground():
 seeds=[(-18,-13),(-5,-15),(10,-13),(20,-9),(-17,0),(-2,-1),(13,2),(-13,15),(1,14),(18,16)]
 def clip(poly,A,B,C):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   f=A*p[0]+B*p[1]-C;g=A*q[0]+B*q[1]-C
   if f<=1e-8:out.append(p)
   if (f<0)!=(g<0):
    t=f/(f-g);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return out
 cells=[]
 for k,(x,y) in enumerate(seeds):
  poly=[(-22.5,-20),(22.5,-20),(22.5,20),(-22.5,20)]
  for l,(u,v) in enumerate(seeds):
   if l!=k:poly=clip(poly,2*(u-x),2*(v-y),u*u+v*v-x*x-y*y)
  cells.append(poly)
 vs=[];fs=[];mat=[];lookup={}
 def vert(p):
  key=tuple(round(v,7) for v in p)
  if key not in lookup:lookup[key]=len(vs);vs.append(tuple(p))
  return lookup[key]
 for k,poly in enumerate(cells):
  cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly);boundary=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   for j in range(3):t=j/3;boundary.append((p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t))
  n=len(boundary);rings=[]
  for t in [1,.94,.82,.55]:
   ring=[]
   for x,y in boundary:
    xx=cx+(x-cx)*t;yy=cy+(y-cy)*t
    h=3.20 if t==1 else 3.66+.045*math.sin(xx*.9+yy*.6) if t==.94 else 3.55+.035*math.sin(xx*.7-yy*.8) if t==.82 else 3.08+.025*math.sin(xx*.3+yy*.4)
    ring.append(vert((xx,yy,h)))
   rings.append(ring)
  for j in range(3):
   for i in range(n):q=(i+1)%n;fs.append((rings[j][i],rings[j][q],rings[j+1][q],rings[j+1][i]));mat.append('groove' if j==0 else 'rim' if j==1 else 'center')
  center=vert((cx,cy,3.02+.02*math.sin(k)))
  for i in range(n):fs.append((rings[-1][i],rings[-1][(i+1)%n],center));mat.append('center')
 # Close external terrain perimeter only, shared inner boundaries remain welded.
 counts={}
 for f in fs:
  for a,b in zip(f,f[1:]+f[:1]):key=tuple(sorted((a,b)));counts[key]=counts.get(key,0)+1
 edges=[e for e,n in counts.items() if n==1]
 bottom=[]
 for a,b in edges:
  aa=vert((vs[a][0],vs[a][1],0));bb=vert((vs[b][0],vs[b][1],0));fs.append((a,b,bb,aa));mat.append('soil');bottom.extend([aa,bb])
 # order planar underside around rectangle center.
 bottom=sorted(set(bottom),key=lambda i:math.atan2(vs[i][1],vs[i][0]));fs.append(tuple(bottom));mat.append('soil')
 obj=mesh_object('continuous_low_centered_polygon_terrain_with_raised_rims',vs,fs,[m[k] for k in cfg['palette']],col);keys=list(cfg['palette'])
 for p,k in zip(obj.data.polygons,mat):p.material_index=keys.index(k)

{'thaumaptilon':thaumaptilon,'sandstone-fin':fin,'lava-dome':lava_dome,'ice-wedge-polygon-ground':ice_ground}[slug]()
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset(col,center_xy=True);source=audit_source(col,14000);assert not source['errors'],source
(out/'source-metrics.json').write_text(json.dumps(source,indent=2)+'\n');bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(out/'source.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in col.all_objects:obj.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
bpy.ops.export_scene.gltf(**opts);qa=audit_glb(out/'model.glb',14000,6,30);assert not qa['errors'],qa;assert qa['bytes']<=1000000,qa['bytes']
(out/'metrics.json').write_text(json.dumps({'source':source,'glb':qa,'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'measured_blender_xyz_m':source['bounds_blender_m']['size'],'measured_glb_xyz_m':qa['bounds_m']['size'],'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'three_version':'0.180.0','author':'Leon Made This / s010s','asset_license':'CC-BY-4.0','code_license':'MIT'},indent=2)+'\n');print('BUILT',slug,qa['sha256'],qa['scene_triangles'],qa['bytes'])
