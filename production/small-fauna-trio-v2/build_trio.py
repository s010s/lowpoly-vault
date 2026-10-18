# SPDX-License-Identifier: MIT
"""Original stylized static fauna. Run with Blender 4.3.2 -b --python-exit-code 1.
-- --asset diplomystus|burgessomedusa|kalligramma [--output /absolute/parent] [--no-preview]
No external models, textures or source art incorporated. Seed 18.
"""
import sys, math, json, argparse
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews
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

def painted_material(mat,name,width,height,painter):
 image=bpy.data.images.new(name,width=width,height=height,alpha=True)
 pixels=[]
 for y in range(height):
  for x in range(width):pixels.extend((*painter((x+.5)/width,(y+.5)/height),1))
 # Image float values here are sRGB because this image is explicitly tagged sRGB.
 image.colorspace_settings.name='sRGB';image.pixels.foreach_set(pixels);image.update();image.filepath_raw=str(TEXTURE_DIR/(name+'.png'));image.file_format='PNG';image.save();image.pack()
 node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;node.interpolation='Linear';shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');mat.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])
 return image

def fish_pigment(u,v):
 h=math.sin(v*2*pi);back=(.31,.44,.48);side=(.60,.70,.70);belly=(.82,.84,.78)
 if h>0:t=h**1.4;a,b=side,back
 else:t=(-h)**1.3;a,b=side,belly
 color=[a[i]*(1-t)+b[i]*t for i in range(3)]
 # Low contrast original scale rhythm, suppressed on the head and peduncle.
 envelope=max(0,min(1,(u-.16)*6))*max(0,min(1,(.88-u)*9))
 scale=.012*math.cos(u*2*pi*30+math.sin(v*2*pi*13))*(.5+.5*math.cos(v*2*pi*15))*envelope
 return [max(0,min(1,c+scale)) for c in color]

def wing_pigment(u,v):
 base=(.68,.62,.47);edge=max(0,(abs(v-.5)*2-.72)/.28);taper=.07*edge+.025*math.cos(u*pi)
 # Irregular muted ocellus: pigment only, no raised concentric disks.
 dx=(u-.59)/.070;dy=(v-.50)/.18;r=math.sqrt(dx*dx+dy*dy)*(1+.045*math.sin(u*80+v*50));spot=max(0,min(1,(1-r)*6));halo=max(0,1-abs(r-1.12)*4)*.030
 grain=.006*math.sin(u*190+math.sin(v*70))*math.sin(v*143)
 return [max(0,min(1,base[i]-taper+halo+grain-spot*(.20 if i<2 else .14))) for i in range(3)]

def fish(c,m):
 body=Part('continuous-head-and-tapered-body',m)
 profiles=[(-.128,.001,.017,.002),(-.125,.0035,.014,.0045),(-.119,.008,.009,.012),(-.108,.012,.003,.022),(-.092,.0145,0,.029),(-.072,.0155,-.001,.033),(-.050,.015,-.002,.034),(-.025,.0138,-.003,.031),(.001,.0115,-.003,.024),(.025,.0085,-.002,.017),(.047,.006,-.001,.010),(.065,.004,0,.006),(.080,.003,0,.004),(.088,.0025,0,.0035)]
 n=28;v=[]
 for y,w,z,h in profiles:
  for k in range(n):
   a=2*pi*k/n;v.append((w*math.cos(a),y,z+h*math.sin(a)))
 f=[tuple(reversed(range(n)))];mi=[1]
 for j in range(len(profiles)-1):
  for k in range(n):
   f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));q=math.sin(2*pi*(k+.5)/n);mi.append(0 if q>.72 else 1 if q>-.40 else 2)
 f.append(tuple((len(profiles)-1)*n+k for k in range(n)));mi.append(1);body.add(v,f,[0]*len(f));body_obj=body.finish(c,True)
 uv=body_obj.data.uv_layers.new(name='UVMap')
 for polygon in body_obj.data.polygons:
  ks=[body_obj.data.loops[i].vertex_index%n for i in polygon.loop_indices]
  for li in polygon.loop_indices:
   vi=body_obj.data.loops[li].vertex_index;j,k=divmod(vi,n);vv=k/n
   if max(ks)-min(ks)>n/2 and k==0:vv=1
   uv.data[li].uv=(j/(len(profiles)-1),vv)
 body_mat=m[0].copy();body_mat.name='diplomystus-body-pigment';body_obj.data.materials.clear();body_obj.data.materials.append(body_mat)
 painted_material(body_mat,'diplomystus-silver-pigment',256,128,fish_pigment)
 fins=Part('curved-fins-with-fine-ray-structure',m)
 # Thin closed membrane with curved interior vertices, smoothly rounded outlines.
 def membrane(poly,axis=(1,0,0),bend=.0010):
  from mathutils.geometry import tessellate_polygon
  poly=[Vector(p) for p in poly];n=len(poly);normal=Vector(axis);v=[];f=[];tris=tessellate_polygon([poly]);ids=[[t if isinstance(t,int) else next(i for i,p in enumerate(poly) if (p-t).length<1e-8) for t in tr] for tr in tris]
  for side in [1,-1]:
   for q in poly:v.append(tuple(q+normal*side*.00033))
  for tri in ids:
   center=sum((poly[i] for i in tri),Vector())/3;idx=len(v);v.extend([tuple(center+normal*(bend+.00033)),tuple(center+normal*(bend-.00033))])
   for k in range(3):a,b=tri[k],tri[(k+1)%3];f.extend([(idx,a,b),(idx+1,n+b,n+a)])
  for k in range(n):j=(k+1)%n;f.append((k,n+k,n+j,j))
  fins.add(v,f,3)
 dorsal=[(0,-.038,.025),(0,-.028,.042),(0,-.019,.054),(0,-.012,.056),(0,-.006,.052),(0,.002,.039),(0,.014,.026),(0,.024,.012)]
 anal=[(0,-.010,-.025),(0,.002,-.039),(0,.014,-.037),(0,.033,-.024),(0,.055,-.005)]
 tail=[(.001,.078,.003),(.002,.100,.018),(.004,.121,.030),(.005,.132,.033),(.005,.134,.029),(.003,.121,.015),(.001,.109,0),(0,.123,-.016),(-.001,.134,-.029),(-.001,.132,-.033),(-.001,.119,-.029),(0,.098,-.014),(0,.078,-.003)]
 for poly in [dorsal,anal,tail]:membrane(poly)
 for side in [-1,1]:
  membrane([(side*.013,-.091,-.006),(side*.022,-.077,-.013),(side*.030,-.057,-.022),(side*.027,-.049,-.024),(side*.021,-.054,-.018),(side*.013,-.070,-.012)],axis=(0,0,1),bend=.001)
  membrane([(side*.008,-.021,-.026),(side*.016,-.008,-.035),(side*.018,.004,-.036),(side*.014,.009,-.030),(side*.008,-.002,-.025)],axis=(0,0,1),bend=.0007)
  for yy,zz in [(-.025,.043),(-.018,.051),(-.011,.052),(-.004,.043),(.004,.033)]:
   fins.tube([(side*.0008,-.032,.029),(side*.0017,(yy-.032)/2,zz*.82),(side*.0008,yy,zz)],[.00026,.00024,.00013],1,5)
  for yy,zz in [(.129,.029),(.123,.023),(.117,.015),(.117,-.015),(.123,-.023),(.129,-.029)]:
   fins.tube([(side*.001,.082,0),(side*.002,.101,zz*.4),(side*.001,yy,zz)],[.00028,.00023,.00010],1,5)
 fins.finish(c,True)
 face=Part('subtle-eyes-gill-cover-and-lifted-mouth',m)
 for side in [-1,1]:
  face.ellipsoid((side*.0107,-.111,.0105),(.0012,.0036,.0036),1,20,9)
  face.ellipsoid((side*.0116,-.111,.0107),(.0007,.0026,.0026),4,20,9)
  face.ellipsoid((side*.0121,-.112,.0115),(.00022,.00065,.00065),2,10,5)
  face.tube([(side*.0124,-.097,.020),(side*.0147,-.090,.010),(side*.0147,-.087,-.002),(side*.011,-.089,-.016)],[.00028,.00036,.00033,.00018],0,6)
  face.tube([(side*.0065,-.121,.007),(side*.003,-.127,.013),(side*.001,-.129,.016)],[.00040,.00034,.00019],4,7)
 for j in range(14):
  y=-.085+j*.0035;z=.029+(.0013 if j>3 else -.001)
  face.sheet([(-.0009,y,z),(0,y-.001,z+.0017),(.0009,y,z),(0,y+.0011,z-.0006)],.0005,0,axis=(0,1,0))
 face.finish(c,True)

def jelly(c,m):
 shell=Part('softly-contracted-hollow-bell',m);n=48
 rings=[(.004,.040),(.009,.044),(.024,.046),(.048,.0455),(.075,.041),(.101,.0335),(.122,.024),(.135,.012),(.139,.003),(.135,.0025),(.130,.010),(.117,.020),(.097,.0295),(.073,.0365),(.047,.041),(.023,.0418),(.009,.0405),(.004,.0365)]
 v=[]
 for j,(z,r) in enumerate(rings):
  for k in range(n):
   a=2*pi*k/n;co=math.cos(a);si=math.sin(a)
   # Rounded square plan and four shallow corner folds, slightly contracted oral rim.
   ripple=(.00065*math.cos(8*a)+.00035*math.sin(3*a))*(1-z/.15)**2
   shift=.006*(z/.14)**2
   v.append((shift+(r+ripple)*math.copysign(abs(co)**.79,co), (r+ripple)*math.copysign(abs(si)**.79,si),z+.0012*math.cos(4*a)*(1-z/.14)**3))
 f=[];mi=[]
 for j in range(len(rings)-1):
  if j==8:continue
  for k in range(n):
   f.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k));mi.append(2 if j in [0,16] else 1 if j>8 else 0)
 f.extend([tuple(8*n+k for k in range(n)),tuple(reversed([9*n+k for k in range(n)]))]);mi.extend([0,1])
 for k in range(n):f.append(((len(rings)-1)*n+k,(len(rings)-1)*n+(k+1)%n,(k+1)%n,k));mi.append(2)
 shell.add(v,f,mi);shell.finish(c,True)
 fringe=Part('short-gently-splayed-tentacle-fringe',m)
 for k in range(96):
  a=2*pi*k/96;co=math.cos(a);si=math.sin(a);r=.0379;x=r*math.copysign(abs(co)**.79,co);y=r*math.copysign(abs(si)**.79,si);length=.015+.003*(.5+.5*math.cos(4*a));d=Vector((co,si,0));p=Vector((x,y,.006+.0012*math.cos(4*a)));sway=Vector((.0018*math.sin(3*a),.0012*math.cos(2*a),0))
  fringe.tube([p,p+d*.001+Vector((0,0,-.005)),p+d*.003+sway+Vector((0,0,-length*.7)),p+d*.004+sway*1.2+Vector((0,0,-length))],[.00105,.001,.00075,.00018],3,n=6)
 fringe.finish(c,True)
 folds=Part('four-inner-bell-folds',m)
 for a in [pi/4,3*pi/4,5*pi/4,7*pi/4]:
  folds.tube([(.013*math.cos(a)+.004,.013*math.sin(a),.123),(.031*math.cos(a)+.002,.031*math.sin(a),.068),(.036*math.cos(a),.036*math.sin(a),.013)],[.0025,.0018,.0011],2,n=8)
 folds.finish(c,True)
 # A quiet swimming tilt is an artistic pose; bake geometry, keep identity root.
 from mathutils import Matrix
 rot=Matrix.Rotation(math.radians(-9),4,'Y')@Matrix.Rotation(math.radians(5),4,'X')
 for o in c.objects:
  if o.type=='MESH':
   for vertex in o.data.vertices:vertex.co=rot@vertex.co

def insect(c,m):
 wings=Part('four-volumetric-rounded-wings',m);veins=Part('branched-wing-veins',m);spots=Part('four-inlaid-eye-spots',m)
 # Parametric tapered root, rounded distal edge. Each wing a closed lens.
 for s in [-1,1]:
  for fore in [True,False]:
   root=Vector((s*.002,-.006 if fore else .004,.004 if fore else .0025))
   u=Vector((s*(.052 if fore else .041),-.027 if fore else .030,.011 if fore else .008))
   perp=Vector((s*(.011 if fore else -.012),.021 if fore else .018,-.001))
   def pos(t,q,z=0):return root+u*t+perp*(math.sin(pi*t)**.72)*q+Vector((0,0,z+.0025*math.sin(pi*t)))
   # Elliptical outline around root/tip, each pair connected in order.
   outline=[pos(0,0)]
   for j in range(1,13):outline.append(pos(j/13,-1))
   outline.append(pos(1,0))
   for j in range(12,0,-1):outline.append(pos(j/13,1))
   # layered fill with a curved middle ridge rather than a flat playing card.
   n=len(outline);center=pos(.52,0);v=[tuple(p+Vector((0,0,.00035))) for p in outline]+[tuple(p-Vector((0,0,.00035))) for p in outline]+[tuple(center+Vector((0,0,.0011))),tuple(center-Vector((0,0,.0006)))];f=[];mi=[]
   for k in range(n):j=(k+1)%n;f.extend([(2*n,k,j),(2*n+1,n+j,n+k),(k,n+k,n+j,j)]);mi.extend([0,0,0])
   wings.add(v,f,mi)
   # Sparse primary and cross-vein rhythm, readable at normal prop size.
   for q in [-.7,0,.7]:
    pts=[pos(t,q,.00105) for t in [.04,.25,.50,.74,.94]];veins.tube(pts,[.00019,.00018,.00016,.00012,.00007],2,5)
   for t in [.20,.32,.45,.58,.70,.82]:
    for q in [-1,1]:veins.tube([pos(t,0,.00110),pos(t+.06,q*.48,.00105),pos(min(t+.10,.96),q*.95,.0007)],[.00012,.00010,.000055],2,5)
   # Restrained original pigment marking; no bright target-like concentric rings.
   p=pos(.59,0,.0017)
   for rr,z,mat in [(.0053,0,1),(.0039,.00010,0),(.0025,.00018,3)]:
    vs=[tuple(p+Vector((0,0,z)))]+[tuple(p+Vector((rr*math.cos(2*pi*k/20),rr*.92*math.sin(2*pi*k/20),z))) for k in range(20)]
    spots.add(vs,[(0,1+k,1+(k+1)%20) for k in range(20)],mat)
 wing_obj=wings.finish(c,True);veins.finish(c,True)
 uv=wing_obj.data.uv_layers.new(name='UVMap');chunk=54
 for polygon in wing_obj.data.polygons:
  for li in polygon.loop_indices:
   vi=wing_obj.data.loops[li].vertex_index%chunk
   if vi>=52:coord=(.52,.5)
   else:
    k=vi%26
    if k==0:coord=(0,.5)
    elif k<=12:coord=(k/13,.5-.5*math.sin(pi*k/13)**.72)
    elif k==13:coord=(1,.5)
    else:coord=((26-k)/13,.5+.5*math.sin(pi*(26-k)/13)**.72)
   uv.data[li].uv=coord
 painted_material(m[0],'kalligramma-wing-pigment',256,256,wing_pigment)
 body=Part('head-thorax-and-segmented-abdomen',m)
 body.ellipsoid((0,-.004,.0045),(.0048,.008,.0047),2,12,8)
 body.ellipsoid((0,-.014,.0048),(.0037,.0038,.0037),2,12,7)
 for j in range(7):body.ellipsoid((0,.005+j*.0035,.0025-j*.00015),(.0033-j*.00030,.0030,.0028-j*.00023),2,14,8)
 for s in [-1,1]:body.ellipsoid((s*.0028,-.0155,.0055),(.0017,.0018,.0018),3,10,6)
 body.finish(c,True)
 limbs=Part('six-legs-two-antennae-and-proboscis',m)
 for s in [-1,1]:
  for j in range(3):
   y=-.009+j*.005
   limbs.tube([(s*.0025,y,.003),(s*.008,y+(-.005+j*.004),-.002),(s*.012,y+(-.008+j*.007),-.007),(s*.015,y+(-.011+j*.010),-.007)],[.00065,.00050,.00035,.00018],2,6)
  limbs.tube([(s*.0015,-.016,.007),(s*.003,-.023,.010),(s*.006,-.030,.0105),(s*.008,-.033,.0095)],[.00036,.00027,.00020,.00010],2,6)
 limbs.tube([(0,-.017,.003),(0,-.025,.001),(0,-.034,-.002),(0,-.037,-.004)],[.00048,.00040,.00029,.00015],2,7)
 limbs.finish(c,True)

def main():
 global TEXTURE_DIR
 p=argparse.ArgumentParser();p.add_argument('--asset',required=True,choices=['diplomystus','burgessomedusa','kalligramma']);p.add_argument('--output',type=Path,default=ROOT/'assets/candidates/small-fauna-trio-v2');p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);s=a.asset;TEXTURE_DIR=a.output/s;TEXTURE_DIR.mkdir(parents=True,exist_ok=True);c=setup_scene(s,18)
 palettes={'diplomystus':['#637E85','#97AFB2','#C7D2CB','#8CA5A6','#263D43'],'burgessomedusa':['#ABC6C5','#8FAFAE','#CBDDD4','#8FB5B0'],'kalligramma':['#B4A07C','#8C7C62','#716652','#665F4B']}
 mats=[make_material(s+'-'+str(i),color,roughness=.52 if s=='diplomystus' else .80) for i,color in enumerate(palettes[s])]
 if s=='burgessomedusa':
  for mat in mats[:2]:
   shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');shader.inputs['Transmission Weight'].default_value=.38;shader.inputs['IOR'].default_value=1.34;shader.inputs['Roughness'].default_value=.30

 {'diplomystus':fish,'burgessomedusa':jelly,'kalligramma':insect}[s](c,mats)
 meta={'description':{'en':'Original child-friendly stylized concept inspired by '+s+'. Artistic palette, pose, scale and simplified detail; static, not a scientific reconstruction.','zh':'原创儿童友好史前启发造型；颜色、姿态、尺寸和简化细节属于艺术选择。静态模型，非严格科学复原。'},'generator':'production/small-fauna-trio-v2/build_trio.py','revision':'v002','status':'candidate','mounting_point':'body/bell centerline at local origin; free-swimming/flying static specimen, not ground contact','textures':'original packed pigment map for fish/wing; no third-party images','export_texcoords':True,'claim_scope':'named-taxon-inspired stylized art','sources':json.loads((ROOT/'production/small-fauna-trio-v2'/s/'references.json').read_text())['sources']}
 export_asset(s,{'en':'Stylized '+s.capitalize(),'zh':{'diplomystus':'古鱼 Diplomystus','burgessomedusa':'箱钟水母 Burgessomedusa','kalligramma':'宽翅蝶蛉 Kalligramma'}[s]},'animals',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=24)
 if not a.no_preview:render_previews(c,a.output/s,views=('hero','reversehero','front','side','rear','top','clay','silhouette'),resolution=640,samples=32,transparent=True)
if __name__=='__main__':main()
