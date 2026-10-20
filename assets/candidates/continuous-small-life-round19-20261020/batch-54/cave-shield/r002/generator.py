# SPDX-License-Identifier: MIT
"""Original batch 54 full-volume geometry. Run in Blender 4.3.2."""
import argparse,json,math,sys,pathlib
from mathutils import Vector
R=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(R/'scripts'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset
P=math.pi
args=sys.argv[sys.argv.index('--')+1:];pa=argparse.ArgumentParser();pa.add_argument('--config',required=True);pa.add_argument('--output-dir',required=True);a=pa.parse_args(args);cfg=json.loads(pathlib.Path(a.config).read_text());s=cfg['asset_id'];C=setup_scene(s,54)
cream=make_material('Calcite ivory','#DBBB88');ochre=make_material('Warm ochre','#B5804B');dark=make_material('Deep mineral shadow','#6C4932');stone=make_material('Sandstone','#A56E4E');seedmat=make_material('Fossil seed umber','#754B30')

def mesh(name,v,f,mat):return mesh_object(name,v,f,mat,C)
def tube(name,pts,rads,mat,n=12,rib=False,cavity=False):
 v=[];f=[];frames=[]
 for i,p in enumerate(pts):
  p=Vector(p);t=Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(i-1,0)]);t.normalize();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();w=t.cross(u).normalized();frames.append((p,t,u,w));rad=rads[i]*(1+.055*math.cos(i*P*.75) if rib else 1)
  for j in range(n):v.append(tuple(p+rad*(u*math.cos(2*P*j/n)+w*math.sin(2*P*j/n))))
 for i in range(len(pts)-1):
  for j in range(n):k=i*n+j;l=i*n+(j+1)%n;f.append((k,l,l+n,k+n))
 f.append(tuple(reversed(range(n))))
 if cavity:
  p,t,u,w=frames[-1];base=len(v);rad=rads[-1]
  for depth,rr in [(0,.78),(.018,.72),(.030,.55)]:
   for j in range(n):v.append(tuple(p-t*depth+rad*rr*(u*math.cos(2*P*j/n)+w*math.sin(2*P*j/n))))
  outer=(len(pts)-1)*n
  for j in range(n):k=(j+1)%n;f.append((outer+j,outer+k,base+k,base+j))
  for i in range(2):
   for j in range(n):k=(j+1)%n;f.append((base+i*n+j,base+i*n+k,base+(i+1)*n+k,base+(i+1)*n+j))
  f.append(tuple(base+2*n+j for j in range(n)))
 else:f.append(tuple((len(pts)-1)*n+j for j in range(n)))
 return mesh(name,v,f,mat)
def bez(p0,p1,p2,p3,n):
 return [tuple((1-t)**3*Vector(p0)+3*t*(1-t)**2*Vector(p1)+3*t*t*(1-t)*Vector(p2)+t**3*Vector(p3)) for t in [i/n for i in range(1,n+1)]]
def ellipsoid(name,center,rx,ry,rz,mat,spiral=False):
 # Rings avoid degenerate pole triangles. Spiral relief modulates actual radial coordinates.
 v=[(center[0],center[1]-ry,center[2])];f=[];n=24;m=24
 for i in range(1,m):
  t=P*i/m; y=-ry*math.cos(t); rr=math.sin(t)
  for j in range(n):
   ph=2*P*j/n; mod=1-.075*(.5+.5*math.cos(7*ph-5*t))**4 if spiral else 1
   v.append((center[0]+rx*rr*math.cos(ph)*mod,center[1]+y,center[2]+rz*rr*math.sin(ph)*mod))
 for j in range(n):f.append((0,1+(j+1)%n,1+j))
 for i in range(m-2):
  for j in range(n):k=1+i*n+j;l=1+i*n+(j+1)%n;f.append((k,l,l+n,k+n))
 end=len(v);v.append((center[0],center[1]+ry,center[2]));base=1+(m-2)*n
 for j in range(n):f.append((base+j,base+(j+1)%n,end))
 return mesh(name,v,f,mat)
def slab(name,x,y,h,mat):
 # Deliberate beveled slab with corner cuts.
 ring=[(-x*.44,-y*.5), (x*.40,-y*.5),(x*.5,-y*.39),(x*.48,y*.43),(x*.39,y*.5),(-x*.44,y*.48),(-x*.5,y*.35),(-x*.5,-y*.36)]
 v=[(a*.96,b*.96,0) for a,b in ring]+[(a,b,h*.75) for a,b in ring]+[(a*.95,b*.95,h) for a,b in ring];f=[]
 for i in range(2):
  for j in range(8):k=i*8+j;l=i*8+(j+1)%8;f.append((k,l,l+8,k+8))
 f += [tuple(reversed(range(8))),tuple(16+j for j in range(8))];return mesh(name,v,f,mat)
if s=='didymoceras':
 pts=[];rad=[]
 # Two separated, genuinely spatial whorls descending as tube thickens.
 for i in range(241):
  t=i/240;th=4*P*t;rr=.019+.044*t;pts.append((rr*math.cos(th),rr*math.sin(th),.29-.15*t));rad.append(.003+.010*t)
 p0=pts[-1];pts+=bez(p0,(.063,.034,.13),(.065,.043,.065),(.030,.043,.041),32);rad += [.013+.004*i/32 for i in range(1,33)]
 pts+=bez(pts[-1],(-.025,.043,.003),(-.099,.043,.029),(-.104,.043,.079),45);rad += [.017+.004*i/45 for i in range(1,46)]
 pts+=bez(pts[-1],(-.108,.043,.102),(-.104,.043,.120),(-.095,.043,.137),20);rad += [.021+.002*i/20 for i in range(1,21)]
 tube('Continuous open helix and hooked final chamber',pts,rad,cream,12,True,True)
elif s=='spirematospermum':
 # Thick open capsule shell: outer and inner surfaces joined around the true rim.
 N=48;M=32;v=[];f=[]
 for layer in range(2):
  for i in range(M+1):
   t=i/M;y=-.025+.05*t;profile=.12+.88*math.sin(P*t)**.72
   for j in range(N+1):
    ang=2.35+(2*P+.78-2.35)*j/N;rib=1+.045*math.cos(10*ang+1.2*t);rx=.0082*profile* (1 if layer==0 else .81);rz=.0067*profile*(1 if layer==0 else .76)
    v.append((rx*math.cos(ang)*rib,y, .007+rz*math.sin(ang)*rib))
 stride=(M+1)*(N+1)
 for layer in range(2):
  for i in range(M):
   for j in range(N):
    k=layer*stride+i*(N+1)+j;face=(k,k+1,k+N+2,k+N+1);f.append(face if layer==0 else tuple(reversed(face)))
 for i in range(M):
  for j in [0,N]:k=i*(N+1)+j;l=k+N+1;f.append((k,l,l+stride,k+stride))
 for i in [0,M]:
  for j in range(N):k=i*(N+1)+j;f.append((k,k+1,k+1+stride,k+stride))
 mesh('Ribbed capsule thick open wall',v,f,ochre)
 for i,y in enumerate([-.014,-.002,.010]):ellipsoid('Embedded spiral seed '+str(i+1),(0,y,.0085),.0038,.0057,.0044,seedmat,True)
 pts=[(0,.024,.007),(.0005,.030,.005),(.002,.036,.003)];tube('Curved basal stalk',pts,[.0015,.0012,.0009],dark,10)
elif s=='cave-shield':
 # Two closed rounded plates with shallow radial facets and continuous real sidewall.
 for idx,zc in enumerate([.29,.445]):
  n=48;nr=5;v=[];f=[]
  for layer in [0,1]:
   for ring in range(nr+1):
    rr=.035+.965*ring/nr
    for j in range(n):
     ang=2*P*j/n;shape=1+.027*math.cos(7*ang)+.016*math.sin(11*ang);x=.49*rr*math.cos(ang)*shape;y=.32*rr*math.sin(ang)*shape-.03
     z=zc+.07*y + (.032*(1-rr*rr)+.015 if layer==0 else -.028*(1-rr*rr)-.016);v.append((x,y,z))
  stride=(nr+1)*n
  for layer in [0,1]:
   for ring in range(nr):
    for j in range(n):k=layer*stride+ring*n+j;l=layer*stride+ring*n+(j+1)%n;f.append((k,l,l+n,k+n))
   f.append(tuple(layer*stride+j for j in range(n)))
  for j in range(n):k=nr*n+j;l=nr*n+(j+1)%n;f.append((k,l,l+stride,k+stride))
  mesh(('Lower' if idx==0 else 'Upper')+' calcite shield plate',v,f,cream)
 # compact supported rear-wall block, no decorative display pedestal
 v=[];n=10
 for z,rx,ry in [(0,.30,.13),(.22,.29,.12),(.49,.25,.11),(.64,.22,.09)]:
  for j in range(n):ang=2*P*j/n;v.append((rx*math.cos(ang),.34+ry*math.sin(ang),z+.015*math.cos(3*ang)))
 f=[tuple(reversed(range(n))),tuple(3*n+j for j in range(n))]
 for i in range(3):
  for j in range(n):k=i*n+j;l=i*n+(j+1)%n;f.append((k,l,l+n,k+n))
 mesh('Supporting cave wall attachment',v,f,stone)
elif s=='psammichnites-ribbon-trace':
 slab('Illustrative sandstone slab',.28,.38,.024,stone)
 # Unified broad ribbon cross-section. Median ridge and transverse crenulations are geometric.
 n=192; cross=[-1,-.82,-.53,-.20,0,.20,.53,.82,1];v=[];f=[]
 for layer in range(2):
  for i in range(n+1):
   t=i/n;y=-.155+.31*t;x=.052*math.sin(2*P*t-.6);dx=.052*2*P/.31*math.cos(2*P*t-.6);u=Vector((1,-dx,0)).normalized()
   taper=.58+.42*math.sin(P*t)**.25
   for c in cross:
    offset=c*.029*taper;p=Vector((x,y,0))+u*offset
    if layer==0:
     median=.0085*math.exp(-(c/.19)**2);body=.009*(1-c*c);ribs=.0035*(.5+.5*math.cos(2*P*34*t+1.2*c*c))**3*(1-abs(c)**3)*(1-math.exp(-(c/.22)**2));z=.0245+body+median+ribs
    else:z=.023
    v.append((p.x,p.y,z))
 stride=(n+1)*len(cross);w=len(cross)
 for layer in range(2):
  for i in range(n):
   for j in range(w-1):k=layer*stride+i*w+j;f.append((k,k+1,k+w+1,k+w))
 for i in range(n):
  for j in [0,w-1]:k=i*w+j;f.append((k,k+w,k+w+stride,k+stride))
 for i in [0,n]:
  for j in range(w-1):k=i*w+j;f.append((k,k+1,k+1+stride,k+stride))
 mesh('Raised ribbon median ridge and transverse divisions',v,f,ochre)
else:raise ValueError(s)
# Match the independently declared artistic envelope exactly; do not label it natural measurement.
bpy.context.view_layer.update()
verts=[v for o in C.all_objects if o.type=='MESH' for v in o.data.vertices]
low=[min(v.co[i] for v in verts) for i in range(3)];high=[max(v.co[i] for v in verts) for i in range(3)]
ratios=[cfg['nominal_design_envelope_blender_xyz_m'][i]/(high[i]-low[i]) for i in range(3)]
for v in verts:
 for i in range(3):v.co[i]*=ratios[i]
ground_asset(C,center_xy=True)
record=export_asset(s,s.replace('-',' ').title(),'geology' if s=='cave-shield' else 'traces' if s.endswith('trace') else 'plants' if s=='spirematospermum' else 'animals',C,metadata={'design_configuration':cfg,'reconstruction':'Stylized basic-form study, not scientific specimen facsimile.','surface_profile':'palette-only','generator':'generator.py'},output_root=pathlib.Path(a.output_dir),render=False,max_triangles=14000,max_materials=6,max_primitives=30)
print(json.dumps({'asset_id':s,'triangles':record['triangles'],'bytes':record['glb_bytes'],'bounds':record['blender_dimensions_m']}))
