# SPDX-License-Identifier: MIT
"""Original batch06 geometry; Blender 4.3.2. One asset, isolated output per call.
blender -b -t 2 --python-exit-code 1 --python PATH -- --config CONFIG --output DIR [--preview]
All dimensions below are normalized design coordinates and scaled by config.
No external geometry, image, texture, palette or reconstruction was incorporated.
"""
import argparse,sys,json,math,hashlib
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews
PI=math.pi
class Shape:
 def __init__(self,name,mats):self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  o=len(self.v);self.v.extend(v);self.f.extend([tuple(o+i for i in q) for q in f]);self.mi.extend(mi if isinstance(mi,list) else [mi]*len(f))
 def tube(self,points,radii,mi=0,n=12,caps=True):
  pts=list(map(Vector,points));v=[]
  # Stable transported local frames avoid rotations at bends.
  u=None
  for j,p in enumerate(pts):
   d=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized()
   if u is None:u=d.cross(Vector((0,1,0)))
   u=u-d*u.dot(d)
   if u.length<.001:u=d.cross(Vector((1,0,0)))
   u.normalize();w=d.cross(u).normalized()
   for k in range(n):v.append(tuple(p+radii[j]*(math.cos(2*PI*k/n)*u+math.sin(2*PI*k/n)*w)))
  f=[tuple(reversed(range(n)))] if caps else []
  for j in range(len(pts)-1):
   for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
  if caps:f.append(tuple((len(pts)-1)*n+k for k in range(n)))
  self.add(v,f,mi)
 def finish(self,c,smooth=True):
  o=mesh_object(self.name,self.v,self.f,self.mats,c)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i;p.use_smooth=smooth
  return o

def curve(points,radii,steps=4):
 pts=list(map(Vector,points));out=[];rs=[]
 for i in range(len(pts)-1):
  a,b,c,d=pts[max(i-1,0)],pts[i],pts[i+1],pts[min(i+2,len(pts)-1)]
  for j in range(steps):
   t=j/steps;out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t));rs.append(radii[i]*(1-t)+radii[i+1]*t)
 out.append(pts[-1]);rs.append(radii[-1]);return out,rs

def grow(s,points,radii,mi=0,n=12,steps=3):s.tube(*curve(points,radii,steps),mi=mi,n=n)
def apply(o,mod):
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name);o.select_set(False)
def fuse(o,voxel,ratio=.5):
 m=o.modifiers.new('Organic junction union','REMESH');m.mode='VOXEL';m.voxel_size=voxel;m.use_smooth_shade=True;apply(o,m)
 m=o.modifiers.new('Soft junction relaxation','SMOOTH');m.factor=1.0;m.iterations=3;apply(o,m)
 m=o.modifiers.new('Form-conscious planar economy','DECIMATE');m.ratio=ratio;apply(o,m)
 for p in o.data.polygons:p.use_smooth=True
 return o

def aulopora(c,m):
 s=Shape('creeping-tube-network',m)
 # Unequal lobes and directed branches, no substrate in export.
 main=[(-.48,-.02,.022),(-.29,-.055,.021),(-.10,-.015,.023),(.08,.025,.022),(.26,-.01,.023),(.44,.05,.022)]
 grow(s,main,[.021,.024,.025,.023,.019,.006],0,12,4)
 terminals=[]
 for i,(x,y,sgn,extent) in enumerate([(-.36,-.035,-1,.22),(-.23,-.04,1,.30),(-.08,-.01,-1,.32),(.07,.02,1,.27),(.23,0,-1,.24),(.34,.03,1,.20)]):
  end=Vector((x+.11*(1 if i%2 else -1),y+sgn*extent,.047))
  pts=[(x,y,.023),(x+.025,y+sgn*.08,.024),(end.x-.025,end.y-sgn*.055,.028),end]
  grow(s,pts,[.020,.017,.014,.012],0,12,4);terminals.append((end,sgn,i))
  q=Vector(pts[2]);side=Vector((-.08 if i%2 else .085,sgn*.04,0));branch=q+side;branch.z=.042
  grow(s,[Vector(pts[1]),q,branch],[.013,.012,.011],0,10,3);terminals.append((branch,-sgn,i+6))
 net=fuse(s.finish(c),.006,.16)
 # Each bell is a closed wall around a real blind cavity, with smooth upturned stem.
 cups=Shape('upturned-trumpet-cups-with-real-cavities',m)
 for end,sgn,i in terminals:
  h=.064+.012*math.sin(i*1.7);r=.027+.003*math.cos(i)
  center=[end+Vector((.005,sgn*.007,0)),end+Vector((.010,sgn*.012,.025)),end+Vector((.013,sgn*.017,h*.72)),end+Vector((.014,sgn*.020,h))]
  pts,rs=curve(center,[.012,.016,.023,r],3)
  # Return down the inner wall; top two rings form rounded lip.
  top=pts[-1];pts+= [top+Vector((0,0,.002)),top+Vector((0,0,-.004)),end+Vector((.012,sgn*.017,h*.50)),end+Vector((.009,sgn*.010,.023))]
  rs += [r-.003,r-.007,.012,.003]
  v=[];f=[tuple(reversed(range(16)))];mi=[0]
  for p,radius in zip(pts,rs):
   for k in range(16):v.append(tuple(p+Vector((radius*math.cos(2*PI*k/16),radius*math.sin(2*PI*k/16),0))))
  for j in range(len(pts)-1):
   for k in range(16):f.append((j*16+k,j*16+(k+1)%16,(j+1)*16+(k+1)%16,(j+1)*16+k));mi.append(1 if j>=len(pts)-4 else 0)
  f.append(tuple((len(pts)-1)*16+k for k in range(16)));mi.append(1);cups.add(v,f,mi)
 cups.finish(c)

def thamnopora(c,m):
 s=Shape('softly-fused-growing-fingers',m)
 paths=[([(0,0,.025),(-.025,.005,.23),(.025,.02,.48),(.015,.025,.73),(.06,.01,.96)],[.13,.115,.09,.075,.004]),
 ([(-.02,0,.22),(-.15,-.015,.38),(-.27,-.03,.56),(-.31,-.015,.73)],[.09,.083,.067,.003]),
 ([(0,.01,.42),(.17,.045,.53),(.27,.055,.72),(.25,.04,.88)],[.085,.078,.065,.004]),
 ([(-.16,-.01,.40),(-.20,.14,.53),(-.15,.20,.69)],[.065,.056,.003]),
 ([(.14,.04,.52),(.22,-.13,.60),(.32,-.18,.71)],[.067,.05,.003]),
 ([(.00,.02,.59),(-.08,.14,.75),(-.10,.16,.88)],[.06,.045,.003])]
 for pts,rs in paths:
  a,b=Vector(pts[-2]),Vector(pts[-1]);rr=rs[-2];pts=pts[:-1]+[a.lerp(b,.65),a.lerp(b,.90),b];rs=rs[:-1]+[rr*.82,rr*.46,rs[-1]];grow(s,pts,rs,0,16,4)
 body=fuse(s.finish(c),.012,.32)
 # Sparse oblique sockets drilled into the actual branch body, not painted dots.
 cutters=Shape('temporary-corallite-cutters',m)
 holes=[(-.017,0,.22,.108),(.003,.018,.36,.093),(.02,.02,.51,.083),(.016,.026,.65,.075),(.034,.02,.80,.065),
 (-.15,-.01,.41,.078),(-.23,-.027,.51,.065),(-.286,-.023,.64,.051),(.16,.043,.55,.070),(.24,.048,.69,.061),(.254,.041,.79,.045),(-.18,.16,.57,.045),(.26,-.15,.64,.04)]
 for i,(x,y,z,r) in enumerate(holes):
  for sign in [-1,1]:
   d=Vector((.20*math.sin(i*1.9),sign,.30)).normalized();p=Vector((x,y,z));a=p+d*(r-.026);b=p+d*(r+.025)
   cutters.tube([a,b],[.020 if i<6 else .017,.023 if i<6 else .020],1,12)
 cutter=cutters.finish(c);mod=body.modifiers.new('Readable outward corallite sockets','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;apply(body,mod);bpy.data.objects.remove(cutter,do_unlink=True)
 for p in body.data.polygons:p.use_smooth=True
 # Preserve crisp cavity rims while the broad fingers stay soft.
 bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.0008);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.0018);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(body.data);bm.free()

def hallucigenia(c,m):
 body=Shape('continuous-long-neck-and-trunk',m)
 pts=[(0,-.52,.22),(.005,-.49,.225),(.008,-.45,.22),(.01,-.39,.20),(.005,-.30,.18),(-.005,-.19,.178),(0,-.06,.18),(.006,.08,.18),(.003,.22,.17),(-.005,.34,.155),(-.012,.43,.145),(-.01,.48,.15)]
 rs=[.012,.037,.035,.026,.029,.052,.061,.062,.057,.045,.029,.004]
 grow(body,pts,rs,0,20,4);body.finish(c)
 legs=Shape('soft-curved-lobopods',m)
 for j in range(7):
  y=-.17+j*.092;z=.177-.028*(j/6)**2;r=.033*(1-.18*abs(j-3)/3)
  for side in [-1,1]:
   sweep=.020*math.sin(j*1.8+side*.7)
   grow(legs,[(side*.028,y,z),(side*.070,y+.010,z-.025),(side*.102,y+sweep,.073),(side*.119,y+sweep-.012,.024),(side*.142,y+sweep-.030,.015)],[r,r*.77,.017,.012,.007],1,10,4)
 # Three finer anterior pairs; simplify claws rather than enlarge them.
 for j in range(3):
  y=-.35+j*.055
  for side in [-1,1]:grow(legs,[(side*.016,y,.19),(side*.052,y-.025,.155),(side*.070,y-.064,.125)],[.014,.010,.003],1,9,4)
 legs.finish(c)
 spines=Shape('paired-tapered-dorsal-spines',m)
 for j in range(7):
  y=-.22+j*.094;h=.255+.060*math.sin(PI*(j+.5)/7);z=.198-.030*(j/6)**2
  for side in [-1,1]:grow(spines,[(side*.023,y,z),(side*.041,y+.007,z+.048),(side*.066,y+.014,z+h*.65),(side*.087,y+.010,z+h)],[.030,.022,.011,.0008],2,10,3)
 spines.finish(c,False)
 eyes=Shape('tiny-paired-eyes',m)
 for side in [-1,1]:
  grow(eyes,[(side*.024,-.488,.242),(side*.025,-.493,.244)],[.008,.003],3,10,2)
 eyes.finish(c)

def fenestella(c,m):
 # A slightly cupped fan, branching repeatedly outwards. True mesh windows.
 def pos(t,a):
  angle=a*(.44+.56*t);r=.075+.925*t
  return Vector((math.sin(angle)*r*.70,.065*math.cos(angle)*t*t+.020*math.sin(3*angle)*t,r*math.cos(angle)))
 s=Shape('branching-ribs-of-cupped-fan',m)
 grow(s,[(0,0,.005),(0,0,.055),(0,0,.16)],[.025,.023,.022],0,12,3)
 # Parent ribs fork at staggered growth levels; no stick-on rectangular panel.
 angles=[-.88,-.65,-.43,-.22,0,.23,.45,.67,.89]
 for j,a in enumerate(angles):
  start=.02 if j%2==0 else .21;end=1-.055*(.5+.5*math.sin(j*1.6));p=[pos(start+(end-start)*k/18,a) for k in range(19)]
  s.tube(p,[.0145*(1-k/28) for k in range(19)],0,8)
  if j<8:
   mid=(a+angles[j+1])/2;begin=.42+.025*math.sin(j);q=[pos(begin,a),pos(begin+.09,mid),pos(.75,mid),pos(.97-.035*math.cos(j),mid)]
   grow(s,q,[.0105,.010,.008,.004],0,8,3)
 s.finish(c)
 bars=Shape('short-crossbars-and-open-fenestrae',m)
 for row,t in enumerate([.22,.33,.44,.55,.66,.77,.88,.95]):
  aa=angles if t<.53 else sorted(angles+[(angles[j]+angles[j+1])/2 for j in range(8)])
  for j,(a,b) in enumerate(zip(aa,aa[1:])):
   # Crossbars follow cupped growth surface with a slight stagger; quiet lattice.
   tt=t+.008*math.sin(j*1.7+row);p=[pos(tt,a),pos(tt+.005,(a+b)/2),pos(tt,b)]
   grow(bars,p,[.0065,.006,.0065],1 if row%3==1 else 0,7,2)
 bars.finish(c)

BUILDERS={'aulopora':aulopora,'thamnopora':thamnopora,'hallucigenia':hallucigenia,'fenestella':fenestella}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--preview',action='store_true');a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());slug=cfg['asset_id'];c=setup_scene(slug,cfg['seed']);m=[make_material(slug+'-'+str(i),v) for i,v in enumerate(cfg['palette'])];BUILDERS[slug](c,m)
 # Bake all design-space coordinates into meters and floor-contact origin.
 objs=[o for o in c.all_objects if o.type=='MESH'];coords=[v.co for o in objs for v in o.data.vertices];axis=cfg['scale_axis'];extent=max(v[axis] for v in coords)-min(v[axis] for v in coords);factor=cfg['nominal_meters']/extent;low=min(v.z for v in coords);xs=[v.x for v in coords];ys=[v.y for v in coords];offset=Vector(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,low))
 for o in objs:
  for v in o.data.vertices:v.co=(v.co-offset)*factor
 bpy.context.view_layer.update()
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 record=export_asset(slug,cfg['name'],'animals',c,output_root=out.parent,render=False,max_triangles=14000,max_materials=6,max_primitives=30,metadata={'description':cfg['description'],'claim_scope':cfg['claim_scope'],'sources':cfg['sources'],'reconstruction_notes':cfg['uncertainties'],'generator':str(Path(__file__).relative_to(ROOT)),'config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'representation':'Original palette-only static teaching prop; no textures','nominal_scale':{'meters':cfg['nominal_meters'],'kind':'art-direction estimate, not fossil measurement'},'origin':'center of projected footprint at lowest intended floor contact; all mesh transforms identity','motion':'static only; no rig/animation claim','provenance':[{'creator':'Leon Made This / s010s','license':'CC-BY-4.0','scope':'All original geometry/materials/previews; no third-party media incorporated'}]})
 # export_asset creates parent/slug, so callers must supply a directory ending in slug.
 assert out.name==slug and Path(record['glb']).name==slug+'.glb'
 if a.preview:
  render_previews(c,out,views=('hero','reversehero','front','side','rear','top','clay','silhouette'),resolution=512,samples=8,transparent=True)
  import shutil;shutil.copy2(out/'preview-hero.png',out/'cover-transparent.png')
 print(json.dumps({'asset':slug,'bytes':record['glb_bytes'],'tris':record['triangles'],'sha256':record['sha256']['glb']}))
if __name__=='__main__':main()
