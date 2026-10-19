# SPDX-License-Identifier: MIT
"""Original concept-led batch51 semantic lofts. Run in Blender 4.3.2; one asset per call."""
import argparse,json,sys,math,random,hashlib
from pathlib import Path
from datetime import datetime,timezone
import bpy
from mathutils import Vector
REPO=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').is_file())
sys.path.insert(0,str(REPO/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset
TAU=math.tau
class Mesh:
 def __init__(self,name,col,mats):self.name=name;self.col=col;self.mats=mats;self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mat=0):
  off=len(self.v);self.v.extend(v);self.f.extend(tuple(i+off for i in face) for face in f);self.mi.extend([mat]*len(f))
 def finish(self):
  o=mesh_object(self.name,self.v,self.f,self.mats,self.col)
  for f,m in zip(o.data.polygons,self.mi):f.material_index=m
  return o
 def rings(self,rings,mat=0,caps=True):
  n=len(rings[0]);v=[p for r in rings for p in r];f=[]
  for k in range(len(rings)-1):
   for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
  if caps:f.extend([tuple(range(n-1,-1,-1)),tuple((len(rings)-1)*n+j for j in range(n))])
  self.add(v,f,mat)
 def ellipsoid(self,c,r,mat=0,n=20,rows=10):
  rings=[]
  for k in range(1,rows):
   a=math.pi*k/rows;rings.append([(c[0]+r[0]*math.sin(a)*math.cos(TAU*j/n),c[1]+r[1]*math.sin(a)*math.sin(TAU*j/n),c[2]+r[2]*math.cos(a)) for j in range(n)])
  v=[p for ring in rings for p in ring]+[(c[0],c[1],c[2]+r[2]),(c[0],c[1],c[2]-r[2])];f=[]
  for k in range(len(rings)-1):
   for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
  for j in range(n):f.extend([(len(v)-2,j,(j+1)%n),(len(v)-1,(len(rings)-1)*n+(j+1)%n,(len(rings)-1)*n+j)])
  self.add(v,f,mat)
 def tube(self,points,radii,mat=0,n=10):
  rings=[]
  for i,p in enumerate(points):
   tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)]);tangent.normalize();u=tangent.cross(Vector((1,0,0)))
   if u.length<.01:u=tangent.cross(Vector((0,1,0)))
   u.normalize();v=tangent.cross(u).normalized();rings.append([tuple(Vector(p)+radii[i]*(math.cos(TAU*j/n)*u+math.sin(TAU*j/n)*v)) for j in range(n)])
  self.rings(rings,mat)

def trilobite(col,m):
 head=Mesh('cephalon-shield-and-glabella',col,m)
 head.ellipsoid((0,-.016,.0068),(.0145,.012,.0068),0,32,12)
 head.ellipsoid((0,-.019,.010),(.0063,.0088,.005),1,24,12)
 head.ellipsoid((0,-.015,.0026),(.011,.009,.0026),0,24,8)
 head.finish()
 eyes=Mesh('small-attached-eyes',col,m)
 for s in [-1,1]:eyes.ellipsoid((s*.0103,-.020,.0104),(.0017,.0022,.0019),3,16,8)
 eyes.finish()
 armor=Mesh('ten-arched-thoracic-plates',col,m)
 # Complete closed transverse arched plates; tapered width and swept pleural ends.
 for k in range(10):
  y=-.007+k*.0032;w=.0126*(1-.045*k);h=.0074*(1-.04*k);rings=[]
  for dy,scale in [(-.0021,.86),(-.0014,1),(0,1.01),(.0014,.96),(.002,.78)]:
   ring=[]
   for j in range(32):
    a=TAU*j/32;x=w*scale*math.cos(a);z=.0038+max(0,math.sin(a))*h*scale+min(0,math.sin(a))*.0022
    # A true central axial ridge with quiet pleural wings.
    if math.sin(a)>0:z+=.0016*math.exp(-(x/(w*.36))**4)
    ring.append((x,y+dy+.0018*(abs(x)/w)**1.7,z))
   rings.append(ring)
  armor.rings(rings,0 if k%3 else 1)
 armor.finish()
 tail=Mesh('pygidial-shield',col,m);tail.ellipsoid((0,.026,.0038),(.007,.0068,.0038),0,24,10);tail.finish()
 sp=Mesh('swept-genal-and-pleural-spines',col,m)
 for s in [-1,1]:
  sp.tube([(s*.011,-.013,.005),(s*.018,-.008,.004),(s*.024,.003,.0025),(s*.026,.010,.001)], [.0024,.0016,.0009,.00012],0,10)
  for k in range(10):
   y=-.006+k*.0032;w=.0125*(1-.045*k);l=.0115*(1-.045*k)
   sp.tube([(s*w*.85,y,.005),(s*(w+l*.4),y+.002,.004),(s*(w+l*.9),y+.007,.002),(s*(w+l),y+.010,.001)], [.0016,.0012,.00065,.00009],0,8)
 sp.finish()
 horns=Mesh('paired-occipital-open-horns',col,m)
 for s in [-1,1]:
  pts=[];rad=[]
  for k in range(43):
   t=k/42;a=t*2.78;pts.append((s*(.0078+.002*math.sin(a)), -.012+.020*(1-math.cos(a)),.010+.025*math.sin(a)))
   rad.append(.0025*(1-t)**.8+.00010)
  horns.tube(pts,rad,0,12)
 horns.finish()

def floor_patch(col,m):
 mesh=Mesh('former-pool-floor',col,m);rings=[];n=48
 for scale,z in [(.14,.008),(.5,.0085),(.8,.010),(.91,.020),(1,.015),(1,0)]:
  rings.append([(.16*scale*(1+.075*math.sin(3*a)+.035*math.sin(7*a))*math.cos(a),.123*scale*(1+.07*math.cos(5*a))*math.sin(a),z+(.004*math.sin(3*a)+.003*math.cos(5*a))*scale if z else 0) for a in [TAU*j/n for j in range(n)]])
 mesh.rings(rings,0);mesh.finish()
 plates=Mesh('eighteen-solid-fractured-rafts',col,m)
 layout=[(-.10,-.045,.047,.026,-.22),(-.08,.035,.052,.030,.3),(-.035,-.05,.045,.032,.12),(-.015,.01,.052,.031,-.35),(.035,.05,.046,.028,.17),(.075,-.035,.045,.031,-.4),(.104,.020,.029,.022,.24),(.045,-.074,.028,.017,.4),(-.035,.073,.035,.016,-.12),(.002,-.025,.038,.024,.1),(-.115,.003,.023,.017,.55),(.075,.067,.028,.018,-.1),(-.079,-.078,.019,.014,.2),(.109,-.065,.020,.014,-.3),(-.003,.068,.024,.016,.8),(.050,.002,.025,.017,.5),(-.057,.012,.027,.019,-.6),(.004,-.080,.022,.014,.1)]
 for idx,(cx,cy,rx,ry,rot) in enumerate(layout):
  n=7+idx%3;shape=[(1+.19*math.sin(j*2.7+idx))*(.53 if j==2 and idx%3==0 else 1) for j in range(n)];z=.011+(idx%3)*.0022;tilt=.022*math.sin(idx*2)
  rings=[]
  for scale,dz in [(1,0),(1,.0014),(.91,.00185)]:
   r=[]
   for j in range(n):
    a=TAU*j/n;x=rx*math.cos(a)*shape[j]*scale;y=ry*math.sin(a)*shape[j]*scale
    r.append((cx+x*math.cos(rot)-y*math.sin(rot),cy+x*math.sin(rot)+y*math.cos(rot),z+dz+x*tilt+(.0006*math.sin(j*1.91+idx) if dz else 0)))
   rings.append(r)
  plates.rings(rings,1+(idx%3),caps=False)
  base=(len(plates.v)-3*n);plates.f.append(tuple(base+j for j in range(n-1,-1,-1)));plates.mi.append(1+(idx%3))
  center=len(plates.v);plates.v.append((cx,cy,z+.0022))
  for j in range(n):plates.f.append((base+2*n+j,base+2*n+(j+1)%n,center));plates.mi.append(1+(idx%3))
 plates.finish()

def perimeter(w,d,n=48):
 out=[]
 for j in range(n):
  a=TAU*j/n;c=math.cos(a);s=math.sin(a);r=min(w/max(abs(c),1e-8),d/max(abs(s),1e-8));out.append((r*c,r*s))
 return out

def ashbed(col,m):
 matrix=Mesh('continuous-layered-ash-matrix',col,m);n=48;xy=perimeter(.14,.10,n);layers=8;rings=[]
 for k in range(layers+1):
  z=.11*k/layers
  rings.append([(x*(.98+.02*math.sin(k*.7)),y*(.98+.02*math.sin(k*.7)),max(0,z+.0015*math.sin(j*.43+k*.5)) if k else 0) for j,(x,y) in enumerate(xy)])
 v=[p for r in rings for p in r];f=[];mi=[]
 for k in range(layers):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append([0,1,0,2,1,0,1,2][k])
 f+=[tuple(range(n-1,-1,-1)),tuple(layers*n+j for j in range(n))];mi+=[0,1];matrix.add(v,f);matrix.mi=mi;matrix.finish()
 grains=Mesh('embedded-rounded-ash-aggregates',col,m)
 pts=[(-.096,-.047,.008),(-.061,.040,.006),(-.017,-.025,.007),(.042,.049,.005),(.086,-.017,.006),(.111,.061,.004),(-.106,.065,.004),(.023,-.077,.004),(-.045,-.075,.005),(.074,.078,.004),(.110,-.064,.004),(-.008,.070,.004),(.045,.007,.003),(-.074,-.008,.003)]
 for i,(x,y,r) in enumerate(pts):grains.ellipsoid((x,y,.109-r*.25),(r,r*.95,r*.85),3,16,8)
 grains.finish()
 cuts=Mesh('three-exposed-concentric-ash-sections',col,m)
 # Small teaching-enlarged section discs, solid rings with radial color groups; embedded, not loose eggs.
 for axis,c,r in [('front',(-.072,-.0998,.060),.012),('front',(.063,-.0998,.036),.009),('right',(.1395,.033,.077),.011)]:
  n=36;vs=[];fs=[];mi=[]
  for rad in [0,.24,.50,.73,1]:
   for j in range(n):
    a=TAU*j/n;u=r*rad*math.cos(a);v=r*rad*math.sin(a)
    vs.append((c[0]+u,c[1]-.0003,c[2]+v) if axis=='front' else (c[0]+.0003,c[1]+u,c[2]+v))
  # use one central vertex and annular rings, avoid degenerate zero-radius ring
  vs=vs[n:]+[tuple((c[0],c[1]-.0003,c[2]) if axis=='front' else (c[0]+.0003,c[1],c[2]))]
  for j in range(n):fs.append((len(vs)-1,j,(j+1)%n));mi.append(3)
  for k in range(3):
   for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append([4,3,2][k])
  off=len(cuts.f);cuts.add(vs,fs);cuts.mi[off:]=mi
 o=cuts.finish()
 # These single-sided section inlays are intentional open discs against solid matrix; winding faces outward.

def conichnus(col,m):
 mesh=Mesh('sediment-with-continuous-conical-negative-cavity',col,m);n=64;xy=perimeter(.12,.10,n);rings=[]
 for z in [0,.004,.042,.087,.136,.14]:
  scale=.985 if z in [0,.14] else 1
  rings.append([(x*scale,y*scale,z+(.0007*math.sin(j*.39) if z>.004 else 0)) for j,(x,y) in enumerate(xy)])
 for r,z in [(.070,.140),(.042,.140),(.040,.135),(.031,.111),(.021,.080),(.010,.047),(.003,.031),(.0015,.028)]:rings.append([(r*math.cos(TAU*j/n),r*math.sin(TAU*j/n),z) for j in range(n)])
 v=[p for r in rings for p in r];f=[];mi=[]
 for k in range(len(rings)-1):
  for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(0 if k<2 else 1 if k<3 else 2)
 # bottom flat and tiny rounded basal cap, no through hole
 f.append(tuple(range(n-1,-1,-1)));mi.append(0)
 v.append((0,0,.0275));idx=len(v)-1;off=(len(rings)-1)*n
 for j in range(n):f.append((off+j,off+(j+1)%n,idx));mi.append(2)
 mesh.add(v,f);mesh.mi=mi;mesh.finish()

def main():
 p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(args.config.read_text());aid=c['asset_id'];col=setup_scene(aid,c['seed']);m=[make_material('region-'+str(i),v) for i,v in enumerate(c['design']['palette'])]
 {'dicranurus':trilobite,'calcite-raft-deposit':floor_patch,'accretionary-lapilli-bed':ashbed,'conichnus-conical-burrow':conichnus}[aid](col,m)
 ground_asset(col)
 b=json.loads((args.config.parent/'brief.json').read_text());refs=json.loads((args.config.parent/'references.json').read_text())
 # The shared helper requires a slug child: use an isolated temporary staging parent then move exact outputs.
 temp=args.output_dir/'export-staging';rec=export_asset(aid,b['subject']['inventory_name'],b['subject']['category'],col,metadata={'catalog_facets':b['catalog_facets'],'claim_scope':b['claim_scope'],'factual_classification':'stylized-inspired teaching art','sources':refs['sources'],'description':b['modeling_brief'],'generator':str(Path(__file__).relative_to(REPO)),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(args.config.read_bytes()).hexdigest(),'approval':'pending independent QA','hardware_gpu_verified':False,'parent_scene_verified':False},output_root=temp,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
 import shutil
 for f in (temp/aid).iterdir():shutil.move(str(f),str(out/f.name))
 shutil.rmtree(temp)
 md=json.loads((out/'metadata.json').read_text());md.update(glb=str((out/(aid+'.glb')).relative_to(REPO)),blend=str((out/(aid+'.blend')).relative_to(REPO)),preview=str((out/'proof/hero.png').relative_to(REPO)),preview_status='pending exact GLB render');(out/'metadata.json').write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n')
 print('BATCH51_BUILD_COMPLETED',aid,datetime.now(timezone.utc).isoformat())
if __name__=='__main__':main()
