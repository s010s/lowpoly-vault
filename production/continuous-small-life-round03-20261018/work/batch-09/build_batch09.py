# SPDX-License-Identifier: MIT
"""Original batch09 geometry. Blender 4.3.2; deterministic; no external art input."""
import sys,math,json,argparse,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews,ground_asset
pi=math.pi
class Part:
 def __init__(self,name,mats): self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  off=len(self.v);self.v.extend(v);self.f.extend([tuple(off+i for i in face) for face in f]);self.mi.extend(mi if isinstance(mi,list) else [mi]*len(f))
 def finish(self,c,smooth=False):
  o=mesh_object(self.name,self.v,self.f,self.mats,c)
  for p,i in zip(o.data.polygons,self.mi):p.material_index=i;p.use_smooth=smooth
  return o
 def tube(self,points,radii,mi=0,n=6):
  pts=[Vector(p) for p in points];v=[]
  for i,p in enumerate(pts):
   d=pts[min(i+1,len(pts)-1)]-pts[max(0,i-1)];d.normalize();u=d.cross(Vector((0,0,1)))
   if u.length<.01:u=d.cross(Vector((0,1,0)))
   u.normalize();w=d.cross(u).normalized()
   for k in range(n):v.append(tuple(p+radii[i]*(u*math.cos(2*pi*k/n)+w*math.sin(2*pi*k/n))))
  f=[tuple(reversed(range(n)))]
  for i in range(len(pts)-1):
   for k in range(n): f.append((i*n+k,i*n+(k+1)%n,(i+1)*n+(k+1)%n,(i+1)*n+k))
  f.append(tuple((len(pts)-1)*n+k for k in range(n)));self.add(v,f,mi)
 def ellipsoid(self,center,scale,mi=0,n=12,rings=7):
  # Nondegenerate poles and latitude strips.
  v=[(center[0],center[1],center[2]+scale[2])]
  for j in range(1,rings):
   a=pi*j/rings
   for k in range(n):
    b=2*pi*k/n;v.append((center[0]+scale[0]*math.sin(a)*math.cos(b),center[1]+scale[1]*math.sin(a)*math.sin(b),center[2]+scale[2]*math.cos(a)))
  bot=len(v);v.append((center[0],center[1],center[2]-scale[2]));f=[]
  for k in range(n):f.append((0,1+k,1+(k+1)%n))
  for j in range(rings-2):
   for k in range(n): a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b))
  for k in range(n):f.append((bot,1+(rings-2)*n+(k+1)%n,1+(rings-2)*n+k))
  self.add(v,f,mi)
 def sheet(self,outline,thickness,mi=0,axis=(1,0,0)):
  a=Vector(axis)*thickness/2;v=[tuple(Vector(p)+a) for p in outline]+[tuple(Vector(p)-a) for p in outline];n=len(outline)
  # A tail fork is concave: use proper polygon tessellation, never center fans.
  from mathutils.geometry import tessellate_polygon
  poly=[Vector(p) for p in outline];triangles=tessellate_polygon([poly]);f=[]
  for tri in triangles:
   ids=[t if isinstance(t,int) else next(i for i,p in enumerate(poly) if (p-t).length<1e-8) for t in tri]
   f.extend([tuple(ids),tuple(n+i for i in reversed(ids))])
  for k in range(n):j=(k+1)%n;f.append((k,n+k,n+j,j))
  self.add(v,f,mi)


def catmull(points,steps=4):
 ps=[Vector(p) for p in points];out=[]
 for i in range(len(ps)-1):
  a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(len(ps)-1,i+2)]
  for k in range(steps):
   t=k/steps;out.append(tuple(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)))
 out.append(tuple(ps[-1]));return out

def curve_tube(part,pts,r0,r1,mi=0,n=10,steps=4):
 p=catmull(pts,steps);part.tube(p,[r0*(1-j/(len(p)-1))**1.1+r1*j/(len(p)-1) for j in range(len(p))],mi,n)


def preserve_construction(obj,label):
 c=bpy.data.collections.get('SOURCE_CONSTRUCTION')
 if not c:c=bpy.data.collections.new('SOURCE_CONSTRUCTION');bpy.context.scene.collection.children.link(c)
 copy=obj.copy();copy.data=obj.data.copy();c.objects.link(copy);copy.name=label;copy.parent=None;copy.hide_render=True;copy.hide_set(True)

def organic_union(obj,voxel,target):
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 mod=obj.modifiers.new('organic-branch-union','REMESH');mod.mode='VOXEL';mod.voxel_size=voxel;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=obj.modifiers.new('soft-growth-connections','SMOOTH');mod.factor=.55;mod.iterations=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 obj.data.calc_loop_triangles();mod=obj.modifiers.new('retained-primary-shape','DECIMATE');mod.ratio=min(1,target/len(obj.data.loop_triangles));bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in obj.data.polygons:p.use_smooth=True

def thecosmilia(c,m):
 core=Part('naturally-forked-thick-branch-corallum',m)
 curve_tube(core,[(0,0,.004),(.003,.002,.035),(-.001,0,.074),(.002,.001,.11)],.016,.011,0,16,5)
 terminals=[(-.043,-.025,.157,.015),(.037,-.030,.177,.016),(-.035,.027,.194,.0145),(.039,.031,.151,.0165),(.005,-.006,.202,.015),(-.006,.048,.166,.013)]
 for j,(x,y,z,r) in enumerate(terminals):
  start=Vector((.001,0,.049 if j%2==0 else .075));mid=Vector((x*.48,y*.48,(start.z+z-.032)*.50));pre=Vector((x*.96,y*.96,z-.047));tip=Vector((x,y,z-.032))
  pts=catmull([start,mid,pre,tip],5);radii=[.0115+(r*.76-.0115)*(k/(len(pts)-1))+.0004*math.sin(pi*k/(len(pts)-1)) for k in range(len(pts))];core.tube(pts,radii,0,20)
 obj=core.finish(c,True);preserve_construction(obj,'editable-six-branch-solid-before-cup-cuts');organic_union(obj,.0012,4200)
 # Closed cup shells overlap the branch neck below their floors; no fragile boolean cuts.
 cups=Part('six-deep-thick-walled-terminal-cups',m);n=40
 for x,y,z,r in terminals:
  profiles=[(z-.049,r*.63),(z-.037,r*.80),(z-.022,r*.98),(z-.005,r*1.02),(z,r*.98),(z-.0007,r*.76),(z-.009,r*.69),(z-.020,r*.40),(z-.025,r*.24)]
  v=[]
  for zz,rr in profiles:
   for k in range(n):
    a=2*pi*k/n;v.append((x+rr*math.cos(a),y+rr*math.sin(a),zz+.00035*math.sin(5*a+x*10)*max(0,(zz-(z-.02))/.02)))
  f=[tuple(reversed(range(n)))]
  for j in range(len(profiles)-1):
   for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
  f.append(tuple((len(profiles)-1)*n+k for k in range(n)));cups.add(v,f,0)
 cup_object=cups.finish(c,True)
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);cup_object.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.join()
 organic_union(obj,.00075,6500)
 # Wedge-like radial septa taper into depth, rather than spokes floating above cups.
 septa=Part('simplified-unequal-radial-cup-septa',m)
 for x,y,z,r in terminals:
  for k in range(14):
   a=2*pi*k/14;u=Vector((math.cos(a),math.sin(a),0));w=Vector((-math.sin(a),math.cos(a),0));ri=r*(.20 if k%2==0 else .36);ro=r*.76;ctr=Vector((x,y,0));p=[ctr+u*ro+Vector((0,0,z-.0020)),ctr+u*ri+Vector((0,0,z-.019)),ctr+u*(ri*.85)+Vector((0,0,z-.023)),ctr+u*(ro*.88)+Vector((0,0,z-.010))]
   septa.sheet(p,.00065,1,axis=w)
 septa.finish(c,True)
 # Sparse low longitudinal ribs, tied to branch growth, stop below the terminal cup.
 ribs=Part('restrained-longitudinal-corallite-costae',m)
 for j,(x,y,z,r) in enumerate(terminals):
  for k in range(5):
   a=2*pi*k/5+.3*j;u=Vector((math.cos(a),math.sin(a),0));pts=[Vector((x,y,z-.027))+u*r*.90,Vector((x,y,z-.017))+u*r*.99,Vector((x,y,z-.004))+u*r*.99];curve_tube(ribs,pts,.00048,.00025,0,5,3)
 ribs.finish(c,True)

def meandrina(c,m):
 # Winding valley centerlines are authored in plan; the whole mound is one relief mesh.
 paths=[
 [(-.074,-.041),(-.050,-.052),(-.026,-.051),(-.014,-.034),(-.036,-.024),(-.053,-.014),(-.045,.003),(-.021,.012),(-.020,.035),(-.044,.044),(-.050,.060)],
 [(-.024,-.072),(-.003,-.063),(.004,-.044),(-.005,-.025),(.007,-.008),(.024,-.004),(.028,.018),(.013,.033),(.020,.055),(.041,.061)],
 [(.029,-.065),(.052,-.054),(.060,-.037),(.042,-.026),(.041,-.012),(.058,.000),(.064,.024),(.049,.034),(.052,.046)],
 [(-.080,-.003),(-.068,.009),(-.071,.031),(-.060,.044)],
 [(-.004,.077),(-.006,.055),(-.003,.041)],
 [(.080,-.013),(.069,-.010),(.061,-.019)],
 [(-.011,-.034),(.008,-.028),(.019,-.037),(.022,-.052)]
 ]
 segments=[]
 for path in paths:
  ps=catmull([(x,y,0) for x,y in path],6)
  for a,b in zip(ps,ps[1:]):
   dx=b[0]-a[0];dy=b[1]-a[1];segments.append((a[0],a[1],dx,dy,dx*dx+dy*dy))
 def distance(x,y):
  best=1
  for ax,ay,dx,dy,den in segments:
   t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/den));dd=(x-ax-t*dx)**2+(y-ay-t*dy)**2
   if dd<best:best=dd
  return math.sqrt(best)
 n=128;rings=40;v=[];dists=[]
 def pos(r,a):
  x=.09*r*math.cos(a);y=.079*r*math.sin(a);d=distance(x,y)
  # Paired walls rise on each side of each dark recessed valley, in real geometry.
  relief=(.0080*math.exp(-((d-.0055)/.0030)**2)-.0055*math.exp(-(d/.0028)**2))*min(1,(1-r)*12)
  z=.007+.048*max(0,1-r*r)**.65+relief+.0016*math.sin(x*22+y*11)*(1-r)
  return (x,y,z),d
 p,d=pos(0,0);v.append(p);dists.append(d)
 for j in range(1,rings+1):
  r=j/rings
  for k in range(n):p,d=pos(r,k*2*pi/n);v.append(p);dists.append(d)
 f=[]
 for k in range(n):f.append((0,1+k,1+(k+1)%n))
 for j in range(rings-1):
  for k in range(n):a=1+j*n+k;b=1+j*n+(k+1)%n;f.append((a,a+n,b+n,b))
 base=len(v);v.append((0,0,0));dists.append(1)
 for k in range(n):
  idx=1+(rings-1)*n+k;nextidx=1+(rings-1)*n+(k+1)%n;f.append((base,nextidx,idx))
 part=Part('continuous-mound-with-sculpted-meandering-valleys',m);mi=[]
 for face in f:
  d=sum(dists[i] for i in face)/len(face);mi.append(0)
 part.add(v,f,mi);obj=part.finish(c,True)
 uv=obj.data.uv_layers.new(name='Original-planar-pigment')
 for poly in obj.data.polygons:
  for li in poly.loop_indices:
   co=obj.data.vertices[obj.data.loops[li].vertex_index].co;uv.data[li].uv=(co.x/.18+.5,co.y/.158+.5)
 # One small original low-contrast pigment map makes continuous valleys readable;
 # geometry, rather than the image, provides the actual relief and silhouette.
 import numpy as np
 size=256;xx,yy=np.meshgrid((np.arange(size)+.5)/size*.18-.09,(np.arange(size)+.5)/size*.158-.079);dd=np.full((size,size),1.)
 for ax,ay,dx,dy,den in segments:
  t=np.clip(((xx-ax)*dx+(yy-ay)*dy)/den,0,1);dd=np.minimum(dd,(xx-ax-t*dx)**2+(yy-ay-t*dy)**2)
 dd=np.sqrt(dd);valley=np.exp(-(dd/.0028)**2);crest=np.exp(-((dd-.0055)/.0030)**2);pixels=np.ones((size,size,4),dtype=np.float32)
 for i,base in enumerate([.70,.72,.64]):pixels[:,:,i]=base-.16*valley+.035*crest
 image=bpy.data.images.new('meandrina-original-valley-pigment',width=size,height=size,alpha=True);image.colorspace_settings.name='sRGB';image.pixels.foreach_set(pixels.ravel());image.update();image.filepath_raw=str(OUT_DIR/'meandrina-original-valley-pigment.png');image.file_format='PNG';image.save();image.pack()
 node=m[0].node_tree.nodes.new('ShaderNodeTexImage');node.image=image;node.interpolation='Linear';shader=next(n for n in m[0].node_tree.nodes if n.type=='BSDF_PRINCIPLED');m[0].node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])


def leptomitus(c,m):
 tube=Part('elongate-wrinkled-continuous-tube-and-rounded-base',m);n=96;v=[]
 outer=[(0,.0020),(.004,.0075),(.011,.0105)]
 for j in range(1,38):
  t=j/37;outer.append((.011+.189*t,.0117*(1+.12*math.sin(pi*t)+.055*math.sin(5*pi*t+.5))))
 inner=[(.200,.0085),(.195,.0087),(.187,.0085),(.178,.0084),(.166,.0078),(.158,.0044)]
 profiles=outer+inner
 for j,(z,r) in enumerate(profiles):
  t=z/.2;cx=.0045*math.sin(t*2.7)+.0015*t;cy=.0025*math.sin(t*4)
  for k in range(n):
   a=2*pi*k/n;fold=(.00060*math.cos(12*a+.20*math.sin(pi*t))+.00025*math.sin(19*a+.4)+.00018*math.cos(7*a))*(min(t*12,1) if j<len(outer) else .25);rr=r+fold
   zz=z+(.0009*math.sin(5*a+.4)+.0003*math.cos(11*a))*max(0,(t-.88)/.12)
   v.append((cx+rr*math.cos(a),cy+rr*math.sin(a),zz))
 bottom=len(v);v.append((0,0,0));f=[(bottom,(k+1)%n,k) for k in range(n)];mi=[0]*n
 for j in range(len(profiles)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j==len(outer)-1 else 2 if j>=len(outer) else 0)
 zz,rr=profiles[-1];t=zz/.2;floor=len(v);v.append((.0045*math.sin(t*2.7)+.0015*t,.0025*math.sin(t*4),zz))
 for k in range(n):f.append((floor,(len(profiles)-1)*n+k,(len(profiles)-1)*n+(k+1)%n));mi.append(2)
 tube.add(v,f,mi);tube.finish(c,True)


def buthograptus(c,m):
 # A shallow original teaching relief, cropped across the central axis at BOTH ends.
 # No complete crown, root, holdfast, leaf veins or reconstructed living stance.
 axis=Part('cropped-central-thallus-axis',m);axispts=catmull([(-.006,-.050,.0016),(-.003,-.023,.0019),(.003,.007,.0020),(.009,.039,.0018),(.011,.052,.0016)],6)
 def flat_tube(part,points,widths,depths,mi):
  pts=[Vector(p) for p in points];v=[];n=10
  for j,p in enumerate(pts):
   d=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized();u=Vector((-d.y,d.x,0)).normalized()
   for k in range(n):a=k*2*pi/n;v.append(tuple(p+u*widths[j]*math.cos(a)+Vector((0,0,depths[j]*math.sin(a)))))
  f=[tuple(reversed(range(n)))]+[(j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k) for j in range(len(pts)-1) for k in range(n)]+[tuple((len(pts)-1)*n+k for k in range(n))];part.add(v,f,mi)
 flat_tube(axis,axispts,[.0017-.0004*j/(len(axispts)-1) for j in range(len(axispts))],[.00075]*len(axispts),0);axis.finish(c,True)
 sides=Part('up-curved-tapered-laterals-of-preserved-fragment',m)
 for j in range(11):
  y=-.042+j*.0084;x=-.006+(y+.05)*.17
  for side in [-1,1]:
   if j==0 and side==1:continue
   length=.026+.009*math.sin(j*.41+.8)+(.002 if side==1 else -.002);dy=.011+.004*math.cos(j*.5)
   points=catmull([(x,y,.0018),(x+side*length*.35,y+.002,.0021),(x+side*length*.78,y+dy*.55,.0019),(x+side*length,y+dy,.00155)],5)
   widths=[.00135*(1-t/(len(points)-1))**.75+.00013 for t in range(len(points))];depths=[.00055*(1-t/(len(points)-1))+.00018 for t in range(len(points))];flat_tube(sides,points,widths,depths,0)
 sides.finish(c,True)
 for o in c.all_objects:
  if o.type=='MESH':
   for vertex in o.data.vertices:vertex.co.z-=.0015
 # A quiet original slab makes the preserved-fragment presentation explicit.
 # It is a teaching support, not a replica of the cited specimen's rock.
 slab=Part('original-shallow-specimen-support-slab',m);outline=[(-.056,-.059),(-.033,-.067),(.021,-.065),(.052,-.049),(.058,-.005),(.051,.047),(.025,.064),(-.027,.066),(-.053,.048),(-.060,.011)]
 n=len(outline);v=[(x,y,0) for x,y in outline]+[(x*.97,y*.97,-.004) for x,y in outline];f=[tuple(range(n)),tuple(reversed([n+k for k in range(n)]))]+[(k,n+k,n+(k+1)%n,(k+1)%n) for k in range(n)];slab.add(v,f,1);slab.finish(c,False)

PALETTES={'thecosmilia':['#B79A83','#DFCEB1','#8B7566'],'meandrina':['#B7B8A0','#DDD6B9','#8B9E95'],'leptomitus':['#94AAA8','#C1C9B4','#637F7C'],'buthograptus':['#6F7867','#C9BA9E']}
NAMES={'thecosmilia':{'en':'Thecosmilia-inspired branch-tube coral','zh':'受 Thecosmilia 启发的枝管珊瑚'},'meandrina':{'en':'Meandrina-inspired maze-ridge coral','zh':'受 Meandrina 启发的迷宫脊珊瑚'},'leptomitus':{'en':'Leptomitus-inspired wrinkled tube sponge','zh':'受 Leptomitus 启发的褶纹管海绵'},'buthograptus':{'en':'Buthograptus-inspired preserved algal thallus fragment','zh':'受 Buthograptus 启发的保存藻体片段'}}
DESCS={'thecosmilia':('Six naturally forked thick branches end in deep, separated septate cups.','六条自然分叉厚枝的末端为分离的深隔壁杯。'),'meandrina':('A low rounded mound with continuous sculpted winding valleys and paired raised walls.','低圆丘体上以真实几何塑造连续曲折沟谷及成对隆起壁。'),'leptomitus':('A quiet slender continuous sponge tube with a rounded base and restrained longitudinal folds.','安静纤长的连续海绵管体，带圆钝基部与克制纵向褶纹。'),'buthograptus':('An open comb-like preserved thallus fragment in shallow relief on an original teaching slab; not a complete organism.','原创教学板上开放梳状浅浮雕藻体片段，并非完整生物复原。')}
def main():
 global OUT_DIR
 p=argparse.ArgumentParser();p.add_argument('--asset',required=True,choices=PALETTES);p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s=a.asset;assert cfg['asset_id']==s
 OUT_DIR=a.output/s;OUT_DIR.mkdir(parents=True,exist_ok=True)
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),col,roughness=.78) for i,col in enumerate(PALETTES[s])];globals()[s](c,m);ground_asset(c,center_xy=False)
 meta={'description':dict(zip(['en','zh'],DESCS[s])),'generator':str(Path(__file__).relative_to(ROOT)),'config':str(a.config.resolve().relative_to(ROOT)),'claim_scope':('Preserved shallow thallus structural fragment only; no complete living organism, roots, holdfast or marine vegetation claim.' if s=='buthograptus' else 'Original stylized-inspired static teaching prop; no strict scientific reconstruction.'),'representation':cfg['representation'],'reconstruction_type':cfg['reconstruction_type'],'origin_detail':'Identity root at central placement axis; finished base at Z=0 in meters.','reconstruction_notes':{'en':'Nominal size, palette, pose and counts of fine repeated structures are artistic choices. No third-party media, mesh or texture incorporated; cross-period teaching catalogue only.','zh':'名义尺寸、配色、姿态及微小重复结构数量为美术选择。无第三方媒体、网格或贴图；仅作跨时代教学目录。'},'export_texcoords':s=='meandrina','surface_profile':'original geometry relief; Meandrina uses one original 256px valley-pigment map, other subjects palette-only','sources':json.loads((ROOT/'production/continuous-small-life-round03-20261018/items'/s/'references.json').read_text())['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010','review_state':'candidate; parent-dispatched independent QA pending'}
 export_asset(s,NAMES[s],'plants' if s=='buthograptus' else 'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH09_COMPLETE',s)
if __name__=='__main__':main()
