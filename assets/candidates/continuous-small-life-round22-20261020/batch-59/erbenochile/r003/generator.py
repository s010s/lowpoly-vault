# SPDX-License-Identifier: MIT
import argparse,json,math,sys,pathlib,random
import bpy
from mathutils import Vector
ROOT=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists());sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset

def loft(name,rings,n,mats,col):
 v=[]
 for k,(z,rx,ry,cx,cy) in enumerate(rings):
  for j in range(n):
   a=2*math.pi*j/n; v.append((cx+rx*math.cos(a),cy+ry*math.sin(a),z))
 f=[tuple(reversed(range(n)))]
 for k in range(len(rings)-1):
  for j in range(n):a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
 f.append(tuple((len(rings)-1)*n+j for j in range(n)))
 return mesh_object(name,v,f,mats,col)

def tube(name,points,radii,mat,col,n=8):
 v=[]
 for i,p in enumerate(points):
  tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]);tangent.normalize();ref=Vector((0,0,1))
  if abs(tangent.dot(ref))>.95:ref=Vector((0,1,0))
  u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
  for j in range(n):
   q=Vector(p)+radii[i]*(math.cos(2*math.pi*j/n)*u+math.sin(2*math.pi*j/n)*w);v.append(tuple(q))
 f=[tuple(reversed(range(n)))]
 for i in range(len(points)-1):
  for j in range(n):a=i*n+j;b=i*n+(j+1)%n;f.append((a,b,b+n,a+n))
 f.append(tuple((len(points)-1)*n+j for j in range(n)));return mesh_object(name,v,f,mat,col)

def ellipsoid(name,center,dims,mat,col,n=24,m=10):
 rings=[]
 for i in range(m+1):
  t=-math.pi/2+(math.pi-.04)*(i/m)+.02;z=center[2]+dims[2]*math.sin(t);r=math.cos(t);rings.append((z,dims[0]*r,dims[1]*r,center[0],center[1]))
 return loft(name,rings,n,mat,col)

def build(cfg,out):
 a=cfg['asset_id'];col=setup_scene(a,cfg['seed']);random.seed(cfg['seed'])
 if a=='stalactite-group':
  stone=make_material('ceiling-dark-warm','#625B4D');cal=make_material('calcite-ivory','#DBC59C');light=make_material('calcite-growth-crest','#E9D7B7')
  slab=loft('rough-ceiling-attachment',[(-.20,1.27,.65,.03,0),(-.10,1.43,.77,0,0),(0,1.33,.66,-.03,0)],18,stone,col)
  for v in slab.data.vertices:
   an=math.atan2(v.co.y,v.co.x);v.co.x*=1+.08*math.sin(5*an);v.co.y*=1+.07*math.cos(3*an);v.co.z+=.055*math.sin(an*3)+.022*math.cos(an*5)
  for i,(x,y,L,r) in enumerate([(-.92,-.12,.9,.21),(-.49,.24,1.24,.22),(.08,-.18,2.1,.37),(.62,.22,1.35,.26),(1.00,-.19,.82,.20)]):
   rings=[]
   for k in range(15):
    t=k/14;rr=max(.004,r*(1-t)**.80*(1+.065*math.sin(t*38+i)));rings.append((-.12-L*t,rr,rr*.83,x+.05*math.sin(t*2+i)*t,y+.04*t*t))
   o=loft('rooted-pendant-%02d'%i,list(reversed(rings)),16,[cal,light],col)
   for p in o.data.polygons:p.material_index=1 if p.index//16 in [9,11,13] else 0
 elif a=='gypsum-cave-flower':
  stone=make_material('attachment-rock','#70685A');iv=make_material('gypsum-ivory','#EBDFCB');ridge=make_material('gypsum-longitudinal-crest','#F4EBDD')
  ellipsoid('small-common-rock-attachment',(0,0,.015),(.020,.018,.012),stone,col,11,5)
  base=bpy.data.objects['small-common-rock-attachment']
  for ve in base.data.vertices:
   an=math.atan2(ve.co.y,ve.co.x);ve.co.x*=1+.20*math.sin(3*an+.6);ve.co.y*=1+.12*math.cos(5*an);ve.co.z+=.0015*math.cos(4*an)
  for i,(ang,L,curl,width) in enumerate([(.08,.145,4.6,.018),(.91,.120,4.0,.014),(2.19,.152,4.9,.019),(3.44,.105,3.8,.012),(4.10,.134,4.5,.016),(5.48,.115,4.2,.013)]):
   v=[];steps=24
   # closed flattened rectangular crystal ribbon, longitudinal profile crests in width
   cross=[(-1,-1),(-1,1),(-.28,1.15),(.32,1.12),(1,1),(1,-1)]
   for k in range(steps):
    t=k/(steps-1);th=.15+curl*t;rad=L/curl;rr=rad*(1-math.cos(th));zz=.020+rad*math.sin(th)+(.018+.006*(i%3))*t
    tangent=Vector((math.cos(ang)*math.sin(th),math.sin(ang)*math.sin(th),math.cos(th)+(.018+.006*(i%3))/(rad*curl))).normalized();side=Vector((-math.sin(ang),math.cos(ang),0));norm=tangent.cross(side).normalized();c=Vector((rr*math.cos(ang+.18*t*math.sin(i)),rr*math.sin(ang+.18*t*math.sin(i)),zz));w=width*(.65+.35*math.sin(math.pi*t))*.5;thick=.0016*(1-.25*t)
    for u,z in cross:v.append(tuple(c+side*u*w+norm*z*thick))
   n=len(cross);f=[tuple(reversed(range(n)))]
   for k in range(steps-1):
    for j in range(n):q=k*n+j;qq=k*n+(j+1)%n;f.append((q,qq,qq+n,q+n))
   f.append(tuple((steps-1)*n+j for j in range(n)));o=mesh_object('curled-crystal-ribbon-%02d'%i,v,f,[iv,ridge],col)
   for p in o.data.polygons:p.material_index=1 if p.index%n in [2,3] else 0
 elif a=='glacial-erratic':
  och=make_material('contrasting-ochre-bedrock','#A88B5E');edge=make_material('bedrock-fracture','#C2A576');rock=make_material('transported-bluegray-boulder','#77818A');vein=make_material('pale-mineral-vein','#C5C4B8')
  o=loft('irregular-stratified-bedrock',[(0,1.62,1.32,0,0),(.13,1.75,1.43,0,0),(.25,1.63,1.32,.03,-.03),(.34,1.58,1.27,0,-.02)],22,[och,edge],col)
  for v in o.data.vertices:
   an=math.atan2(v.co.y,v.co.x);v.co.x*=1+.07*math.sin(5*an+.4);v.co.y*=1+.05*math.cos(7*an);v.co.z+=.036*math.sin(an*3)+.018*math.cos(an*5)
  for p in o.data.polygons:p.material_index=1 if p.index//22==1 else 0
  o=loft('single-asymmetric-erratic-with-integral-vein',[(.31,.69,.65,.08,0),(.47,1.02,.89,.05,0),(.83,1.25,1.00,.02,.02),(1.32,1.20,.96,-.05,.04),(1.45,1.14,.92,-.10,.06),(1.55,1.1,.88,-.12,.08),(2.00,.90,.73,-.24,.16),(2.46,.52,.48,-.44,.24),(2.65,.12,.14,-.52,.20)],11,[rock,vein],col)
  for v in o.data.vertices:
   an=math.atan2(v.co.y,v.co.x);v.co.x*=1+.16*math.sin(3*an+.3);v.co.y*=1+.12*math.cos(4*an+.7);v.co.z+=.065*math.sin(2*an+.7)*(v.co.z-.31)/2.34;v.co.x=min(v.co.x,1.02-.12*v.co.z)
  for p in o.data.polygons:p.material_index=1 if 1.45<p.center.z<1.55 else 0
 else:
  shell=make_material('shell-warm-charcoal','#49453B');ridge=make_material('axial-crest','#766650');eye=make_material('eye-turret-dark','#302F2B');rim=make_material('eye-upper-rim','#A38A61')
  # Units meters. Anterior -Y, tail +Y. Closed shells intentionally omit uncertain soft tissues.
  head=ellipsoid('vaulted-cephalon',(0,-.022,.006),(.020,.014,.006),shell,col,32,12)
  ellipsoid('central-glabella',(0,-.025,.010),(.0065,.010,.004),ridge,col,20,8)
  for sign in [-1,1]:
   x=sign*.011;y=-.027
   loft(('left' if sign<0 else 'right')+'-eye-turret',[(.008,.0035,.0035,x,y),(.017,.0035,.0035,x,y),(.018,.0044,.0044,x,y),(.019,.0044,.0044,x,y),(.0195,.0036,.0036,x,y)],20,[eye,rim],col)
   ob=bpy.data.objects[('left' if sign<0 else 'right')+'-eye-turret']
   for p in ob.data.polygons:p.material_index=1 if p.center.z>.0175 else 0
   tube('swept-genal-spine-'+str(sign),[(sign*.017,-.021,.006),(sign*.022,-.010,.004),(sign*.023,.007,.0025),(sign*.022,.018,.0015)],[.0022,.0017,.0009,.0001],shell,col)
  # Continuous vaulted thoracic shell underneath raised ribs, avoiding a floating skeletal comb.
  v=[];n=20;sections=[(-.014,.015,.0038),(-.007,.016,.0041),(.003,.014,.0040),(.014,.011,.0037),(.025,.007,.0027),(.031,.0038,.0016)]
  for yy,ww,hh in sections:
   for j in range(n):
    an=2*math.pi*j/n;v.append((ww*math.cos(an),yy,.0046+hh*math.sin(an)))
  f=[tuple(reversed(range(n)))]
  for i in range(len(sections)-1):
   for j in range(n):q=i*n+j;qq=i*n+(j+1)%n;f.append((q,qq,qq+n,q+n))
  f.append(tuple((len(sections)-1)*n+j for j in range(n)));mesh_object('continuous-vaulted-thoracic-shell',v,f,shell,col)
  for i in range(11):
   t=i/10;y=-.010+i*.0035;width=.017*(1-.57*t);z=.0055-.0018*t
   # Original arched transverse pleura: closed elliptical section with tapering swept tips.
   xs=[-1,-.86,-.55,-.32,-.24,0,.24,.32,.55,.86,1];v=[];n=10
   for j,xx in enumerate(xs):
    rad=max(.00010,.00125*(1-abs(xx)**4));arch=.0016+.0032*math.exp(-(xx/.30)**4);yc=y+.0047*abs(xx)**2;zc=z+arch
    for k in range(n):
     an=2*math.pi*k/n;v.append((xx*width,yc+rad*math.cos(an),zc+rad*1.35*math.sin(an)))
   f=[tuple(reversed(range(n)))]
   for j in range(len(xs)-1):
    for k in range(n):q=j*n+k;qq=j*n+(k+1)%n;f.append((q,qq,qq+n,q+n))
   f.append(tuple((len(xs)-1)*n+k for k in range(n)));ob=mesh_object('articulated-rib-%02d'%i,v,f,[shell,ridge],col)
   for p in ob.data.polygons:p.material_index=1 if abs(p.center.x)<width*.26 else 0
  bpy.ops.object.select_all(action='DESELECT')
  ribs=[ob for ob in col.objects if ob.name.startswith('articulated-rib-')]
  for ob in ribs:ob.select_set(True)
  bpy.context.view_layer.objects.active=ribs[0];bpy.ops.object.join();bpy.context.object.name='eleven-editable-rib-sections'
  ellipsoid('small-tapering-pygidium',(0,.029,.0028),(.006,.008,.0026),shell,col,20,8)
 if a!='stalactite-group':ground_asset(col,center_xy=True)
 else:
  # True mounting origin at upper attachment center, root remains identity.
  maxz=max((o.matrix_world@v.co).z for o in col.objects if o.type=='MESH' for v in o.data.vertices)
  for ob in col.objects:
   if ob.type=='MESH':ob.location.z-=maxz
 return export_asset(a,cfg['title'],cfg['category'],col,output_root=out.parent,render=False,diagnostics=False,max_triangles=14000,max_materials=6,max_primitives=30,metadata={'nominal_dimensions_blender_xyz_m':cfg['nominal_dimensions_blender_xyz_m'],'scale_note':cfg['scale_note'],'reconstruction_notes':cfg['scope'],'generator':'generator.py','export_texcoords':False})

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output-dir',required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.load(open(args.config));out=pathlib.Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=True);temp=out/'_export';build(cfg,temp/cfg['asset_id'])
 for f in (temp/cfg['asset_id']).iterdir():f.rename(out/f.name)
 (temp/cfg['asset_id']).rmdir();temp.rmdir()
if __name__=='__main__':main()
