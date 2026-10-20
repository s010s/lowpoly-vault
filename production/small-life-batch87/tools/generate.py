#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original batch87 geometry authored after immutable original design freeze."""
import sys,json,math,os,datetime,hashlib,argparse
from pathlib import Path
import bpy
from math import sin,cos,pi,sqrt
HERE=Path(__file__).resolve();ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
from mathutils import Vector
class Mesh:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def add(self,v,f,mi=0):
  n=len(self.v);self.v+=v;self.f += [tuple(n+x for x in face) for face in f];self.mi += [mi]*len(f)
 def emit(self,name,m,col):
  o=mesh_object(name,self.v,self.f,m,col)
  for p,idx in zip(o.data.polygons,self.mi):p.material_index=idx
  return o

def solid_grid(name,rows,m,col,assign=None):
 n=len(rows);k=len(rows[0]);v=[tuple(v) for row in rows for v in row];f=[];mi=[]
 for i in range(n-1):
  for j in range(k-1):
   a=i*k+j;b=a+1;c=b+k;d=a+k
   for ff in ([(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)]):f.append(ff);mi.append(assign(i,j) if assign else 0)
 loop=list(range(k))+[i*k+k-1 for i in range(1,n)]+list(range((n-1)*k+k-2,(n-1)*k-1,-1))+[i*k for i in range(n-2,0,-1)]
 start=len(v);v += [(v[a][0],v[a][1],0) for a in loop];L=len(loop)
 for j,a in enumerate(loop):f.append((a,loop[(j+1)%L],start+(j+1)%L,start+j));mi.append(0)
 f.append(tuple(range(start,start+L))[::-1]);mi.append(0)
 o=mesh_object(name,v,f,m,col)
 for p,idx in zip(o.data.polygons,mi):p.material_index=idx
 return o

def tube(mesh,points,radii,sides,mat):
 v=[]
 for i,p in enumerate(points):
  p=Vector(p);t=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])).normalized();u=t.cross(Vector((0,0,1)))
  if u.length<.01:u=t.cross(Vector((0,1,0)))
  u.normalize();w=t.cross(u).normalized()
  for j in range(sides):v.append(tuple(p+radii[i]*(u*cos(2*pi*j/sides)+w*sin(2*pi*j/sides))))
 f=[tuple(range(sides))[::-1]]
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;b=i*sides+(j+1)%sides;f.append((a,b,b+sides,a+sides))
 f.append(tuple(range((len(points)-1)*sides,len(points)*sides)));mesh.add(v,f,mat)

def blade(mesh,a,z,length,width,rise,mat,base_radius=.055):
 # Closed lenticular blade with broad triangular base, narrow linear distal portion.
 ts=[0,.22,.52,.80,1];ws=[.48,1,.62,.28,.025];v=[]
 for t,w in zip(ts,ws):
  rr=base_radius+length*t;zz=z+rise*t-.07*length*sin(pi*t);cx=rr*cos(a);cy=rr*sin(a);th=.004*(1-.8*t)
  for side,dz in [(-1,0),(0,th),(1,0),(0,-th)]:v.append((cx-side*width*w*sin(a),cy+side*width*w*cos(a),zz+dz))
 f=[(3,2,1,0)]
 for i in range(4):
  for j in range(4):f.append((i*4+j,i*4+(j+1)%4,(i+1)*4+(j+1)%4,(i+1)*4+j))
 f.append((16,17,18,19));mesh.add(v,f,mat)

def pleuromeia(c,m,col):
 M=Mesh();N=20;rings=[(0.085,.075),(0.12,.105),(0.17,.11),(.22,.075),(.31,.070),(.50,.064),(.72,.057),(.94,.05),(1.18,.039)]
 original=rings; rings=[]
 for q in range(c['parameters']['stem_segments']+1):
  z=original[0][0]+(original[-1][0]-original[0][0])*q/c['parameters']['stem_segments']
  k=next((i for i in range(len(original)-1) if original[i][0]<=z<=original[i+1][0]),len(original)-2);a,b=original[k],original[k+1];t=(z-a[0])/(b[0]-a[0]);rings.append((z,a[1]+t*(b[1]-a[1])))
 v=[]
 for z,r in rings:
  for j in range(N):
   a=2*pi*j/N;lob=1+.32*cos(4*a+.35) if z<.22 else 1+.025*cos(5*a+z)
   v.append((r*lob*cos(a),r*lob*sin(a),z))
 f=[tuple(range(N))[::-1]]
 for i in range(len(rings)-1):
  for j in range(N):f.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
 f.append(tuple(range((len(rings)-1)*N,len(rings)*N)));M.add(v,f,0)
 # Sparse lower blades and a readable, continuous golden-angle crown, not whorls.
 for i in range(42):
  t=i/41;z=.23+.94*t;a=i*pi*(3-sqrt(5))+.3;length=.10+.20*sin(pi*(.16+.76*t))**1.3;length*=.94+.06*sin(i*1.7)
  if i<8:length*=.55
  blade(M,a,z,length,.023*(.6+.4*sin(pi*t)),.06+.09*t,1 if i%3 else 2,base_radius=.066-.026*t)
 # Cone axis and integral-looking overlapping thick oval sporophylls.
 tube(M,[(0,0,1.16),(0,0,1.23),(0,0,1.37),(0,0,1.45)],[.035,.055,.038,.002],12,1)
 for i in range(62):
  t=i/61;a=i*pi*(3-sqrt(5));z=1.18+.24*t;rad=.045*(sin(pi*(.12+.84*t))**.5)
  # oval obovate sporophyll, rather than spiky conifer bract
  n=10;v=[];base=Vector((.028*cos(a),.028*sin(a),z-.018));out=Vector((cos(a),sin(a),0));side=Vector((-sin(a),cos(a),0))
  for layer in [-1,1]:
   for j in range(n):
    b=2*pi*j/n;long=.5+.5*cos(b);p=base+out*(.012+rad*long)+side*(.021*sin(b)*(1-.25*t))+Vector((0,0,.045*long+layer*.003));v.append(tuple(p))
  ff=[tuple(range(n))[::-1],tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)];M.add(v,ff,1 if i%4 else 3)
 for i in range(24):
  a=2*pi*i/24+.08*sin(i);r=.065+.022*cos(4*a+.35);rr=.16+.025*sin(i*1.3)
  pts=[(r*cos(a),r*sin(a),.12),((r+.035)*cos(a+.04),(r+.035)*sin(a+.04),.068),(rr*cos(a+.07),rr*sin(a+.07),.018),((rr+.015)*cos(a+.1),(rr+.015)*sin(a+.1),.004)]
  tube(M,pts,[.008,.006,.003,.0015],5,4)
 # Root tips intentionally grounded at z0 via global translation of mesh.
 minz=min(p[2] for p in M.v);M.v=[(x,y,z-minz) for x,y,z in M.v]
 M.emit('unbranched-spiral-leaf-strobilus-rhizophore',m,col)

def glacier(c,m,col):
 # Four crack valleys, with intact continuous ice between; no stacked or coincident solids.
 profile=[(-27,0),(-23,0),(-20.2,0),(-19.0,0),(-18.2,1),(-17.5,.12),(-16.6,0),(-12,0),(-8.2,0),(-7.0,0),(-6.0,1),(-4.4,0),(-1,0),(2.5,0),(3.8,0),(4.6,1),(5.6,0),(11,0),(15,0),(16.7,0),(17.8,1),(19.2,0),(23,0),(27,0)]
 rows=[]
 for i,(y,depth) in enumerate(profile):
  row=[]
  for j in range(25):
   x=-18+36*j/24;xx=x*(1-.025*cos(y*.19));yy=y+(1.25*sin(x*.18+y*.31)+.55*sin(x*.49-y*.16))*(1-abs(y/27)**6);top=11.6+y*.04+.47*sin(x*.2+y*.12)+.17*cos(x*.61-y*.4);z=top-depth*(8.2+.65*sin(x*.21+y))
   row.append((xx,yy,z))
  rows.append(row)
 def idx(i,j):return 2 if profile[i][1] or profile[i+1][1] else 1 if i in (4,10,15,20) else 3 if i%7==0 else 0
 solid_grid('continuous-ice-with-four-v-fractures',rows,m,col,idx)

def spatter(c,m,col):
 N=64;v=[];faces=[];mi=[]
 # Continuous radial cross-section from inner vent floor to welded rim and out to broad foot.
 prof=[(.12,.18),(.45,.18),(.64,.32),(.69,1.0),(.81,1.85),(.91,2.25),(1.03,2.47),(1.30,2.40),(1.55,2.02),(1.9,1.53),(2.30,1.02),(2.72,.59),(3.15,.26),(3.70,.12)]
 centers=[.1,.65,1.5,2.04,2.9,3.7,4.18,5.1,5.65]
 for k,(r,z) in enumerate(prof):
  for j in range(N):
   a=2*pi*j/N;weld=0
   for ii,aa in enumerate(centers):
    da=(a-aa+.12*sin(k*.7+ii)+pi)%(2*pi)-pi;weld+=(.15+.08*sin(ii*1.2)**2)*math.exp(-(da/(.15+.07*sin(ii+2)**2))**2)*sin(pi*min(1,k/12))
   rr=r*(1+.10*sin(3*a+.4)+.065*cos(5*a-.3))+weld*(.8+sin(k*.8+.4)**2)
   # Strong continuous fused lobes, staggered in height and azimuth rather than rings of loose clasts.
   lumps=0
   for ii,aa in enumerate(centers):
    da=(a-aa-.10*sin(r*1.9+ii)+pi)%(2*pi)-pi
    for layer in range(2):
     rc=1.50+.65*sin(ii*1.31+layer*2.7)+.55*layer
     lumps+=(.38+.13*cos(ii*.9)**2)*math.exp(-(da/(.18+.05*cos(ii)**2))**2-((r-rc)/(.45+.12*sin(ii+layer)**2))**2)
   rr+=lumps*.48
   zz=z*(1+.12*sin(2*a+.6)+.06*cos(5*a)) + (.14*sin(k*1.4+3*a)+.1*cos(k*2.1-5*a))*sin(pi*k/13)+lumps*.80
   v.append((rr*cos(a),rr*sin(a),zz))
 faces.append(tuple(range(N))[::-1]);mi.append(3)
 for k in range(len(prof)-1):
  for j in range(N):
   a=k*N+j;b=k*N+(j+1)%N;c=b+N;d=a+N
   for ff in [(a,b,c),(a,c,d)]:faces.append(ff);mi.append(3 if k<3 else 1 if (sin(j*.49+k*1.3)+cos(j*.21-k*.8)>.9) else 0)
 bottom=len(v);v += [(v[(len(prof)-1)*N+j][0],v[(len(prof)-1)*N+j][1],0) for j in range(N)]
 for j in range(N):faces.append(((len(prof)-1)*N+j,(len(prof)-1)*N+(j+1)%N,bottom+(j+1)%N,bottom+j));mi.append(0)
 faces.append(tuple(range(bottom,bottom+N))[::-1]);mi.append(0)
 o=mesh_object('integral-welded-spatter-mound-and-vent',v,faces,m,col)
 for f,idx in zip(o.data.polygons,mi):f.material_index=idx

def travertine(c,m,col):
 # Single closed terrain surface. Each shelf floor is bounded by side rims and downstream lip.
 rows=[];regions=[];N=28
 for level in range(5):
  lengths=[2.6,3.4,3.1,4.4,4.5];L=lengths[level];y0=9-sum(lengths[:level]);floor=3.65-level*.70
  specs=[(0,.18),(.20,0),(L-.78,0),(L-.52,.18),(L-.32,.18),(L,-.52)]
  for k,(dy,dz) in enumerate(specs):
   if level>0 and k==0:continue
   row=[]
   for j in range(N+1):
    t=-1+2*j/N;side=abs(t);width=(2.25+2.5*(9-y0+dy)/18)*(1+.065*sin((y0-dy)*1.2));x=width*t+.38*sin((y0-dy)*.36)
    scallop=.33*cos(t*pi*2+.2*level)+.15*sin(t*pi*5+.6*level);y=y0-dy+scallop*(1 if level<4 or k<5 else .35)
    # geometric continuous enclosing side rims, flatter subdued pool floors
    edge=.20*max(0,(side-.78)/.22)
    z=floor+dz+edge
    if side>.83:z+=.035*sin(j*1.3+level*2+k*.9)
    if k in (3,4):z-=.15*math.exp(-((t-(.27 if level%2 else -.22))/.13)**2)
    row.append((x,y,z))
   rows.append(row);regions.append((level,k))
 def idx(i,j):
  level,k=regions[i];nlevel,nk=regions[i+1]
  if k==1 and nk==2 and j>=3 and j<N-3:return 3 if level%2 else 4
  if k in (3,4):return 2
  return 0 if j>2 and j<N-3 else 1
 solid_grid('linked-shallow-pools-carbonate-slope',rows,m,col,idx)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--output',required=True);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(Path(a.config).read_text());aid=cfg['asset_id'];out=Path(a.output);out.mkdir(parents=True,exist_ok=True);start=datetime.datetime.now(datetime.timezone.utc).isoformat();col=setup_scene(aid,cfg['seed']);m=[make_material(aid+'-region-'+str(i),s) for i,s in enumerate(cfg['palette_srgb'])]
 {'pleuromeia':pleuromeia,'glacier-crevasse-field':glacier,'spatter-cone':spatter,'travertine-terrace-pools':travertine}[aid](cfg,m,col);bpy.context.view_layer.update()
 export_asset(aid,aid,'plants' if aid=='pleuromeia' else 'terrain',col,metadata={'representation':'living-reconstruction' if aid=='pleuromeia' else 'geological-form','export_texcoords':False,'source_scope':'See immutable original-brief.json; original authored geometry.'},output_root=out,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 rec={'pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'started_at':start,'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_version':bpy.app.version_string,'generator_sha256':hashlib.sha256(HERE.read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(Path(a.config).read_bytes()).hexdigest()};(out/'execution.json').write_text(json.dumps(rec,indent=2)+'\n')
if __name__=='__main__':main()
