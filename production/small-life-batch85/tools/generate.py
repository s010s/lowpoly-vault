#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original deterministic geometry, authored after batch85 original freeze."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy
HERE=Path(__file__).resolve(); ROOT=HERE.parents[3]; sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
from math import sin,cos,pi,sqrt

def solid_grid(name,rows,mats,col,assign=None,bottom=0):
 n=len(rows);m=len(rows[0]);verts=[tuple(v) for row in rows for v in row];faces=[];mi=[]
 for i in range(n-1):
  for j in range(m-1):
   a=i*m+j;b=a+1;c=a+m+1;d=a+m
   fs=[(a,b,c),(a,c,d)] if (i+j)%2==0 else [(a,b,d),(b,c,d)]
   for f in fs:faces.append(f);mi.append(assign(i,j) if assign else 0)
 loop=list(range(m))+[i*m+m-1 for i in range(1,n)]+list(range((n-1)*m+m-2,(n-1)*m-1,-1))+[i*m for i in range(n-2,0,-1)]
 k=len(verts);verts.extend([(verts[a][0],verts[a][1],bottom) for a in loop]);L=len(loop)
 for q,a in enumerate(loop):faces.append((a,loop[(q+1)%L],k+(q+1)%L,k+q));mi.append(0)
 faces.append(tuple(range(k,k+L))[::-1]);mi.append(0)
 o=mesh_object(name,verts,faces,mats,col)
 for f,a in zip(o.data.polygons,mi):f.material_index=a
 return o

def slab(name,outline,height,mats,col):
 n=len(outline);v=[(x,y,height) for x,y in outline]+[(x,y,0) for x,y in outline];f=[tuple(range(n)),tuple(range(n,2*n))[::-1]]
 f += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 return mesh_object(name,v,f,mats,col)

def namacalathus(c,m,col):
 # Connected shell midsurface, omitted oval patches become actual lumen openings.
 N=60; rings=[(0,.00125),(.004,.00120),(.009,.00113),(.014,.00115),(.016,.0021),(.018,.0045),(.0195,.0067)]
 rings += [(.021+k*.00065,.010*sqrt(max(.03,1-((.021+k*.00065-.026)/.010)**2))) for k in range(20)]
 rings += [(.034,.0072),(.035,.0062)]
 v=[]
 for z,r in rings:
  for j in range(N):
   a=2*pi*j/N;rf=r*(1+.018*sin(3*a+.3)+.012*cos(5*a+z*100));v.append((rf*cos(a),rf*sin(a),z))
 f=[]
 for i in range(len(rings)-1):
  z=(rings[i][0]+rings[i+1][0])/2
  for j in range(N):
   a=2*pi*(j+.5)/N;nearest=round(a/(pi/3))%6;da=(a-nearest*pi/3+pi)%(2*pi)-pi;cz=.0263+.00035*sin(nearest*2.2);hz=.00325*(1+.06*cos(nearest));wa=.31*(1+.04*sin(nearest*1.3))
   if (da/wa)**2+((z-cz)/hz)**2<1:continue
   f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
 # Conform true lumen boundary vertices to elliptical curves before thickening.
 edgeuses={}
 for face in f:
  for a,b in zip(face,face[1:]+face[:1]):edgeuses.setdefault(tuple(sorted((a,b))),0);edgeuses[tuple(sorted((a,b)))]+=1
 boundary=set(i for e,count in edgeuses.items() if count==1 for i in e if .020<v[i][2]<.032)
 for sector in range(6):
  group=[];cz=.0263+.00035*sin(sector*2.2);hz=.00325*(1+.06*cos(sector));wa=.31*(1+.04*sin(sector*1.3))
  for idx in boundary:
   x,y,z=v[idx];aa=math.atan2(y,x)%(2*pi)
   if round(aa/(pi/3))%6!=sector:continue
   da=(aa-sector*pi/3+pi)%(2*pi)-pi;phi=math.atan2((z-cz)/hz,da/wa);group.append((phi,idx))
  group.sort();phase=group[0][0]
  for k,(_,idx) in enumerate(group):
   phi=phase+2*pi*k/len(group);aa=sector*pi/3+wa*cos(phi);zz=cz+hz*sin(phi)
   rr=.010*sqrt(max(.03,1-((zz-.026)/.010)**2))*(1+.018*sin(3*aa+.3)+.012*cos(5*aa+zz*100));v[idx]=(rr*cos(aa),rr*sin(aa),zz)
 # Inner layer follows outer surface with radial thickness. Stem is genuinely hollow.
 L=len(v);inner=[]
 for x,y,z in v:
  r=math.hypot(x,y);t=.00028 if z<.016 else c['parameters']['shell_thickness_m'];factor=max(.15,(r-t)/r);inner.append((x*factor,y*factor,z))
 edges={}
 for face in f:
  for a,b in zip(face,face[1:]+face[:1]):key=tuple(sorted((a,b)));edges.setdefault(key,[]).append((a,b))
 faces=list(f)+[tuple(a+L for a in face[::-1]) for face in f]
 for e,uses in edges.items():
  if len(uses)==1:a,b=uses[0];faces.append((a,b,b+L,a+L))
 used=sorted(set(i for face in faces for i in face)); remap={old:new for new,old in enumerate(used)}
 o=mesh_object('windowed-cup-continuous-hollow-stalk',[(v+inner)[i] for i in used],[tuple(remap[i] for i in face) for face in faces],m,col)
 for p in o.data.polygons:
  z=p.center.z;p.material_index=0
 # Materials remain structural rather than random face noise.
 o['restoration']='Hidden stalk and unseen shell restored; genus-level skeletal form, not an exact fossil cast.'

def piedmont(c,m,col):
 outline=[(-520,800),(500,800),(590,500),(635,0),(610,-500),(430,-790),(0,-830),(-450,-760),(-620,-430),(-650,50),(-610,500)]
 slab('foreland-substrate',outline,55,[m[4]],col)
 profiles=[(790,125,180),(680,130,168),(560,135,154),(440,145,145),(320,165,136),(220,210,126),(120,310,115),(0,420,105),(-140,515,94),(-300,550,84),(-440,515,72),(-550,450,61),(-640,340,50),(-705,210,40),(-740,70,34)]
 rows=[]
 for i,(y,w,h) in enumerate(profiles):
  xcen=18*sin(y/270)
  row=[]
  for j in range(19):
   t=-1+2*j/18;x=xcen+w*t;yy=y+(5*sin(j*1.6+i*.7) if i>7 else 0);z=55+h*(.30+.70*(1-t*t)) + (3*sin(i*1.2+j*.8) if abs(t)>.6 else 1.8*sin(i+j))
   row.append((x,yy,z))
  rows.append(row)
 def ice_mat(i,j):
  if j==1 and i>=5:return 5
  if j==16 and i>=7:return 3
  return 1 if j in (0,17) else 2 if (i<4 or (i>6 and j in range(6,12))) else 0
 solid_grid('continuous-throat-spreading-lobe',rows,m,col,ice_mat,bottom=50)
 for side in [-1,1]:
  rows=[]
  for i in range(12):
   t=i/11;y=800-880*t;inner=145+100*t;outer=540+40*sin(t*pi);peak=330-150*t+50*sin(t*4*pi+.5*side)
   row=[]
   for j in range(7):
    q=j/6;x=side*(inner+(outer-inner)*q);ridge=[0,.48,.96,.72,.56,.25,0] if side<0 else [0,.32,.68,1,.66,.30,0];z=52+peak*ridge[j]*(.90+.10*sin(i*1.7+j*.8))
    row.append((x,y,z))
   rows.append(row)
  solid_grid(('west' if side<0 else 'east')+'-mountain-shoulder',rows,[m[3],m[4],m[5]],col,lambda i,j: 2 if j in (2,3) else 0,bottom=40)

def lava(c,m,col):
 rows=[]; offsets=[-24,-21,-17,-12,-8,-6.5,0,6.5,8,12,17,21,24]
 for i in range(33):
  t=(i+(0 if i in (0,32) else .25*sin(i*2.4)))/32;y=60-120*t;center=9*sin(2*pi*t-.4);row=[]
  for j,x in enumerate(offsets):
   z=[2,5,10.5,11,7,3.5,3,3.4,7.8,12,10,5,2][j]
   if j in (2,3,8,9,10):z+=1.3*sin(i*.73+j*.6)+.8*cos(i*1.39-j)+.5*sin(i*2.34+j)
   elif j in (5,6,7):z+=.32*sin(i*1.4+j)+.14*cos(i*2.17-j)
   else:z+=.45*sin(i*.8+j)
   row.append((center+x*(1+.025*sin(i*.9)),y,z))
  rows.append(row)
 def mi(i,j):return 2 if j in (5,6) else 1 if j in (4,7) or (j==2 and i in range(7,13)) else 0
 solid_grid('cooled-floor-and-welded-levee-terrain',rows,m,col,mi,bottom=0)

def polje(c,m,col):
 N=56;rad=[.2,.45,.70,.78,.85,.94,1];v=[(0,0,45)];faces=[];mi=[]
 for k,r in enumerate(rad):
  for j in range(N):
   a=2*pi*j/N;s=1+.055*sin(3*a+.2)+.045*cos(5*a);rr=r*(1+(.045*sin(5*a+.3)+.025*cos(9*a))*(1 if k<5 else .4));x=550*rr*cos(a)*s;y=1050*rr*sin(a)*s
   rim=216+31*sin(3*a+.7)+19*cos(7*a)+12*sin(13*a)
   z=45 if k<3 else 73+.14*rim+15*sin(11*a) if k==3 else rim*(.80+.18*sin(5*a)**2) if k==4 else rim*(.61+.25*cos(4*a+.2)**2) if k==5 else .29*rim
   v.append((x,y,z))
 for j in range(N):faces.append((0,1+j,1+(j+1)%N));mi.append(0)
 for k in range(len(rad)-1):
  for j in range(N):
   a=1+k*N+j;b=1+k*N+(j+1)%N;cc=b+N;d=a+N
   faces.extend([(a,b,cc),(a,cc,d)]);mat=0 if k<2 else 4 if k==2 else 3 if k==4 and j in list(range(4,10))+list(range(27,33))+list(range(44,49)) else 1 if k in (3,4) else 2;mi.extend([mat,mat])
 start=1+(len(rad)-1)*N;bottom=len(v);v.extend([(v[start+j][0],v[start+j][1],0) for j in range(N)])
 for j in range(N):faces.append((start+j,start+(j+1)%N,bottom+(j+1)%N,bottom+j));mi.append(2)
 faces.append(tuple(range(bottom,bottom+N))[::-1]);mi.append(2)
 o=mesh_object('enclosed-carbonate-slopes-flat-sediment-basin',v,faces,m,col)
 for p,a in zip(o.data.polygons,mi):p.material_index=a

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(Path(a.config).read_text());aid=c['asset_id'];out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,c['seed']);m=[make_material(aid+'-region-'+str(i),color) for i,color in enumerate(c['palette_srgb'])]
 {'namacalathus':namacalathus,'piedmont-glacier':piedmont,'lava-channel':lava,'karst-polje':polje}[aid](c,m,col)
 bpy.context.view_layer.update()
 export_asset(aid,aid,'animals' if aid=='namacalathus' else 'terrain',col,metadata={'representation':'fossil-form' if aid=='namacalathus' else 'geological-form','export_texcoords':False,'source_scope':'See frozen original-brief.json; geometry original.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 rec={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()}
 (out/'execution.json').write_text(json.dumps(rec,indent=2)+'\n')
if __name__=='__main__':main()
