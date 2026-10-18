# SPDX-License-Identifier: MIT
"""Original batch05 geometry. Blender 4.3.2; deterministic; no external art input."""
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

def goniophyllum(c,m):
 shell=Part('rounded-square-cup-with-growth-contours',m);n=48;v=[]
 # Rounded square sections follow an expanding, gently curved pyramidal cup.
 profiles=[(0,.0035),(.004,.005),(.012,.009),(.022,.014),(.034,.020),(.047,.026),(.060,.030),(.071,.033),(.077,.034),(.080,.0338),(.080,.0307),(.075,.0303),(.066,.0258),(.054,.020),(.047,.010)]
 for j,(z,r) in enumerate(profiles):
  for k in range(n):
   a=2*pi*k/n;co=math.cos(a);si=math.sin(a);x=r*math.copysign(abs(co)**.36,co);y=r*math.copysign(abs(si)**.36,si)
   v.append((x+.003*(1-z/.08)**2,y,z+.0003*math.cos(4*a)*min(z/.02,1)))
 f=[tuple(reversed(range(n)))];mi=[0]
 for j in range(len(profiles)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j>=9 else 0)
 f.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(2);shell.add(v,f,mi);shell.finish(c,True)
 lids=Part('four-hinged-triangular-opercula',m)
 for side in range(4):
  angle=side*pi/2;u=Vector((math.cos(angle),math.sin(angle),0));w=Vector((-math.sin(angle),math.cos(angle),0));hinge=u*.0325+Vector((0,0,.079))
  # Each lid is a closed rounded triangular lens. Broad straight hinge, tapering tip.
  rows=12;cols=10;verts=[]
  for face in [1,-1]:
   for j in range(rows):
    t=j/rows;width=.030*(1-t)**.94
    for k in range(cols+1):
     q=2*k/cols-1
     p=hinge+u*(.021*t-.003*math.sin(pi*t))+w*width*q+Vector((0,0,.034*t+.0022*math.sin(pi*t)*(1-q*q)+face*.00065*(1-.6*t)))
     verts.append(tuple(p))
   verts.append(tuple(hinge+u*.021+Vector((0,0,.034+face*.00025))))
  layer=rows*(cols+1)+1;faces=[]
  for face in range(2):
   o=face*layer
   for j in range(rows-1):
    for k in range(cols):
     a=o+j*(cols+1)+k;faces.append((a,a+1,a+cols+2,a+cols+1) if face==0 else (a+cols+1,a+cols+2,a+1,a))
   for k in range(cols):
    a=o+(rows-1)*(cols+1)+k;faces.append((a,a+1,o+layer-1) if face==0 else (o+layer-1,a+1,a))
  boundary=list(range(cols+1))+[j*(cols+1)+cols for j in range(1,rows)]+[layer-1]+[j*(cols+1) for j in range(rows-1,0,-1)]
  for k,a in enumerate(boundary):b=boundary[(k+1)%len(boundary)];faces.append((a,a+layer,b+layer,b))
  lids.add(verts,faces,1)
  # Low-relief central rib supports the triangular lid shape without ornament overload.
  curve_tube(lids,[hinge+u*.001+Vector((0,0,.0014)),hinge+u*.009+Vector((0,0,.020)),hinge+u*.020+Vector((0,0,.033))],.0007,.00018,0,6,3)
 lids.finish(c,True)
 bands=Part('subtle-organic-growth-ridges',m)
 for z,r in [(.022,.014),(.047,.026),(.071,.033)]:
  pts=[]
  for k in range(49):
   a=2*pi*k/48;co=math.cos(a);si=math.sin(a);pts.append((r*math.copysign(abs(co)**.36,co)+.003*(1-z/.08)**2,r*math.copysign(abs(si)**.36,si),z+.0003*math.cos(4*a)))
  bands.tube(pts,[.00045]*len(pts),0,5)
 bands.finish(c,True)

def halysites(c,m):
 colony=Part('open-looping-chains-of-upright-corallites',m)
 # Five offset cells, deduplicated shared edges: genuine open chain walls.
 radius=.030;cells=[(0,0),(.045,.02598),(-.045,.02598),(0,.05196),(0,-.05196)]
 edges={}
 for cx,cy in cells:
  ps=[(cx+radius*math.cos(k*pi/3),cy+radius*math.sin(k*pi/3)) for k in range(6)]
  for k,a in enumerate(ps):
   b=ps[(k+1)%6];key=tuple(sorted((tuple(round(v,5) for v in a),tuple(round(v,5) for v in b))));edges[key]=(a,b)
 positions={}
 for a,b in edges.values():
  count=4
  for j in range(count+1):
   t=j/count;x=a[0]*(1-t)+b[0]*t;y=a[1]*(1-t)+b[1]*t;positions[(round(x,5),round(y,5))]=(x,y)
 for i,(xx,yy) in enumerate(positions.values()):
  x=xx+.005*math.sin(yy*33)+.002*math.sin(xx*61+yy*13);y=yy+.004*math.sin(xx*40-yy*17)
  # Gentle colony dome, not identical pickets; chain gaps remain through-open.
  h=.028+.015*math.exp(-((x/.08)**2+(y/.085)**2))+.006*math.sin(x*65+y*50)+.002*math.cos(x*130-y*90);r=.0049*(1+.04*math.sin(x*80-y*90));n=8;v=[]
  rings=[(0,r*.94),(.008,r), (h-.003,r*1.02),(h,r*.94),(h-.0005,r*.68),(h-.011,r*.59)]
  for j,(z,rr) in enumerate(rings):
   for k in range(n):
    a=2*pi*k/n;v.append((x+rr*math.cos(a)+.0010*(z/h)**2*math.sin(y*35),y+rr*math.sin(a),z+.0004*math.sin(a+x*50)*(z/h)))
  f=[tuple(reversed(range(n)))];mi=[0]
  for j in range(len(rings)-1):
   for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j==3 else 2 if j>=4 else 0)
  f.append(tuple((len(rings)-1)*n+k for k in range(n)));mi.append(2);colony.add(v,f,mi)
 colony.finish(c,True)

def marrella(c,m):
 head=Part('wedge-headshield-and-two-pairs-of-recurved-spines',m)
 head.ellipsoid((0,-.0105,.0047),(.0046,.005,.0027),0,24,12)
 for s in [-1,1]:
  # Two deliberate swept-back horns per side, broad at their shared shield roots.
  curve_tube(head,[(s*.003,-.012,.005),(s*.008,-.009,.0056),(s*.011,.000,.005),(s*.012,.010,.0035),(s*.010,.018,.0027)],.0015,.00010,0,10,5)
  curve_tube(head,[(s*.0015,-.008,.006),(s*.003,.000,.0075),(s*.0045,.011,.006),(s*.005,.020,.0045)],.0011,.00008,1,9,5)
 head.finish(c,True)
 body=Part('tapered-continuous-trunk-with-segment-rhythm',m)
 # A restrained connected trunk with 22 raised low bands, no oversized tailpiece.
 n=20;v=[];profiles=[]
 for j in range(23):
  t=j/22;y=-.007+j*.00118;width=.00275*(1-.75*t);h=.00185*(1-.7*t);z=.0041-.0014*t
  for offset,factor in [(-.00046,.91),(0,1.03),(.00046,.91)]:profiles.append((y+offset,width*factor,z,h*factor))
 for y,w,z,h in profiles:
  for k in range(n):a=k*2*pi/n;v.append((w*math.cos(a),y,z+h*math.sin(a)))
 f=[tuple(reversed(range(n)))];mi=[1]
 for j in range(len(profiles)-1):
  for k in range(n):f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(1 if j%3==0 else 0)
 f.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(0);body.add(v,f,mi);body.finish(c,True)
 limbs=Part('paired-walking-limbs-gill-paddles-and-antennae',m)
 for j in range(18):
  t=j/18;y=-.0068+j*.00135;w=.0027*(1-.72*t)
  for s in [-1,1]:
   curve_tube(limbs,[(s*w*.6,y,.0036),(s*(w+.0018),y+.0006,.0019),(s*(w+.0030),y+.0018,.0007),(s*(w+.0038),y+.0027,.0004)],.00036*(1-.5*t),.00007,2,6,2)
   # Gill blades broaden the middle scale and keep space beneath head horns.
   limbs.ellipsoid((s*(w+.0012),y+.0003,.0030),(.0013*(1-.5*t),.00045,.00035),1,8,4)
 for s in [-1,1]:
  curve_tube(limbs,[(s*.0015,-.014,.0045),(s*.0032,-.019,.004),(s*.0048,-.024,.0033),(s*.0065,-.027,.0025)],.00032,.00006,2,7,5)
  curve_tube(limbs,[(s*.003,-.013,.003),(s*.006,-.015,.0024),(s*.008,-.017,.002)],.00055,.00018,1,8,3)
 limbs.finish(c,True)

def proteroctopus(c,m):
 flesh=Part('soft-mantle-head-and-eight-arm-construction',m)
 flesh.ellipsoid((0,.020,.023),(.0175,.026,.019),0,32,20)
 flesh.ellipsoid((0,-.005,.0165),(.0135,.015,.012),0,28,16)
 arm_paths=[]
 for j in range(8):
  a=-pi/2+(j-3.5)*.49
  # Eight broad-rooted tapered arms fan from a common web, each tip curls calmly.
  start=Vector((.009*math.cos(a),-.013+.007*math.sin(a),.011))
  direct=Vector((math.cos(a),math.sin(a),0));side=Vector((-math.sin(a),math.cos(a),0));length=.033+.008*math.cos((j-3.5)*.7)
  pts=[start,start+direct*.011+Vector((0,0,-.004)),start+direct*(length*.73)+side*(.004*math.sin(j))+Vector((0,0,-.007)),start+direct*length+side*.006+Vector((0,0,-.007)),start+direct*(length+.002)+side*.011+Vector((0,0,-.004))]
  arm_paths.append(pts);curve_tube(flesh,pts,.0047,.00035,0,12,5)
 obj=flesh.finish(c,True)
 # Preserve editable construction outside EXPORT, then voxel-union the soft core.
 src=bpy.data.collections.new('SOURCE_CONSTRUCTION');bpy.context.scene.collection.children.link(src)
 backup=obj.copy();backup.data=obj.data.copy();src.objects.link(backup);backup.name='editable-original-mantle-and-eight-arms';backup.parent=None;backup.hide_render=True;backup.hide_set(True)
 bpy.context.view_layer.objects.active=obj;obj.select_set(True)
 mod=obj.modifiers.new('gentle-organic-union','REMESH');mod.mode='VOXEL';mod.voxel_size=.00068;mod.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 mod=obj.modifiers.new('soft-arm-root-transitions','SMOOTH');mod.factor=.65;mod.iterations=4;bpy.ops.object.modifier_apply(modifier=mod.name)
 obj.data.calc_loop_triangles();ratio=min(1,5600/len(obj.data.loop_triangles));mod=obj.modifiers.new('shape-aware-refined-lowpoly','DECIMATE');mod.ratio=ratio;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in obj.data.polygons:p.use_smooth=True
 fins=Part('paired-soft-mantle-fins',m)
 for s in [-1,1]:
  # Closed curved lens, rooted deeply in mantle, with tapered rounded leading edge.
  outlines=[(s*.012,.018,.027),(s*.019,.017,.026),(s*.028,.025,.028),(s*.031,.034,.031),(s*.027,.041,.031),(s*.018,.043,.030),(s*.009,.039,.028)]
  center=Vector((s*.019,.031,.031));n=len(outlines);v=[tuple(Vector(p)+Vector((0,0,.0007))) for p in outlines]+[tuple(Vector(p)-Vector((0,0,.0007))) for p in outlines]+[tuple(center+Vector((0,0,.0015))),tuple(center-Vector((0,0,.0006)))];f=[]
  for k in range(n):q=(k+1)%n;f.extend([(2*n,k,q),(2*n+1,n+q,n+k),(k,n+k,n+q,q)])
  fins.add(v,f,1)
 fins.finish(c,True)
 face=Part('small-lateral-eyes-and-underside-sucker-hints',m)
 for s in [-1,1]:
  face.ellipsoid((s*.0116,-.0105,.020),(.0025,.0032,.0030),1,20,10)
  face.ellipsoid((s*.0132,-.0111,.0202),(.00125,.0018,.00185),3,20,10)
  face.ellipsoid((s*.0140,-.0117,.0209),(.00035,.0005,.0005),2,12,6)
 # Restrained underside pads; no exact sucker count or arrangement claim.
 for pts in arm_paths:
  samples=catmull(pts,5)
  for index in [6,9,12,15]:
   p=Vector(samples[index]);face.ellipsoid(p+Vector((0,0,-.0013)),(.0010,.0011,.0005),2,10,5)
 face.finish(c,True)

PALETTES={'goniophyllum':['#BF8F7B','#DCC2A6','#876B61'],'halysites':['#A6B9AC','#D0D8BD','#6E8C84'],'marrella':['#8B9C9F','#B0BBB5','#718587'],'proteroctopus':['#C18E81','#D5A799','#E1C4B0','#334D52']}
NAMES={'goniophyllum':{'en':'Goniophyllum-inspired four-lidded coral','zh':'受 Goniophyllum 启发的四盖珊瑚'},'halysites':{'en':'Halysites-inspired chain coral','zh':'受 Halysites 启发的链珊瑚'},'marrella':{'en':'Marrella-inspired fork-spined arthropod','zh':'受 Marrella 启发的叉棘节肢动物'},'proteroctopus':{'en':'Finned eight-arm teaching prop inspired by Proteroctopus','zh':'受 Proteroctopus 启发的有鳍八腕教学道具'}}
DESCS={'goniophyllum':('A softly rounded pyramidal cup with four open triangular lids.','柔和方锥杯体与四片张开的三角盖。'),'halysites':('Upright linked tubes form five open looping chains with genuine negative space.','相连直立管壁构成五个通透环链，孔隙为真实几何。'),'marrella':('Swept paired head spines frame a gently tapered segmented trunk and small paired appendages.','成组后掠头棘围绕渐细分节躯干及成对小附肢。'),'proteroctopus':('Soft compact mantle, two fins and eight gently curling arms, with smoothly blended roots.','紧凑柔软外套膜、双鳍与八条轻卷腕，腕根柔和衔接。')}
def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',required=True,choices=PALETTES);p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s=a.asset;assert cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),col,roughness=.72) for i,col in enumerate(PALETTES[s])];globals()[s](c,m)
 # Ground contact on the actual lowest finished vertex; root remains identity.
 ground_asset(c,center_xy=False)
 meta={'description':dict(zip(['en','zh'],DESCS[s])),'generator':str(Path(__file__).relative_to(ROOT)),'config':str(a.config.resolve().relative_to(ROOT)),'claim_scope':'Original evidence-informed stylized-inspired static teaching prop; not a strict scientific reconstruction.','origin_detail':'Identity root at central placement axis; lowest finished geometry rests at Z=0; meters.','reconstruction_notes':{'en':'Palette, exact dimensions, open-lid/arm pose, counts of minor repeated parts and soft tissue are artistic choices. No copied media, mesh or texture. Cross-period catalogue; no coexistence claim.','zh':'配色、精确尺寸、开盖/腕姿势、细小重复结构数量及软组织均属美术选择。无第三方网格、图片或贴图；跨时代目录，不主张同域共存。'},'surface_profile':'original palette-only, no textures','sources':json.loads((ROOT/'production/continuous-small-life-round02-20261018/items'/s/'references.json').read_text())['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010','review_state':'candidate; parent-dispatched independent QA pending'}
 export_asset(s,NAMES[s],'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:
  out=a.output/s
  render_previews(c,out,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH05_COMPLETE',s)
if __name__=='__main__':main()
