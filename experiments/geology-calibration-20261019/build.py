# SPDX-License-Identifier: MIT
"""Two isolated original calibration candidates. blender -b -t 2 --python build.py"""
import bpy,sys,math,json,random,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
SEED=20261019

def clip(poly,A,B,C):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  dp=A*p[0]+B*p[1]+C;dq=A*q[0]+B*q[1]+C
  if dp>=-1e-10:out.append(p)
  if (dp>=-1e-10)!=(dq>=-1e-10):
   t=dp/(dp-dq);out.append((p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t))
 clean=[]
 for p in out:
  if not clean or math.dist(p,clean[-1])>1e-7:clean.append(p)
 if len(clean)>1 and math.dist(clean[0],clean[-1])<1e-7:clean.pop()
 return clean

def sandstone(c):
 mats=[make_material('original-sandstone-'+str(i),col,.9) for i,col in enumerate(['#B3A184','#B9A88C','#AC987A','#C1AF92','#B5A184','#A7957D'])]
 # Natural broken profile, not a cuboid; unequal set boundaries, one dominant exposure.
 outline=[(-.40,0),(.31,0),(.39,.085),(.395,.19),(.33,.36),(.21,.485),(-.02,.515),(-.24,.465),(-.365,.345),(-.415,.145)]
 rng=random.Random(SEED)
 for g,(low,high,slope) in enumerate([((0,0),(.14,.065),.34),((.14,.065),(.365,-.055),-.27),((.365,-.055),(.60,0),.19)]):
  b=-.40;j=0
  while b<.85:
   spacing=rng.uniform(.017,.034);p=clip(outline,-low[1],1,-low[0]);p=clip(p,high[1],-1,high[0]);p=clip(p,-slope,1,-b);p=clip(p,slope,-1,b+spacing)
   if len(p)>=3:
    idx=rng.choices([0,1,2,3,4],[5,3,1,1,4])[0]
    original_poly=p
    for xlo,xhi in [(-.5,-.25),(-.25,-.05),(-.05,.17),(.17,.5)]:
     p=clip(clip(original_poly,1,0,-xlo),-1,0,xhi)
     if len(p)<3:continue
     # Each exposure patch is planar; shared layer edges cannot form fake crevices.
     n=len(p);verts=[]
     for ring in range(3):
      for x,z in p:
       breaks=[(-.5,-.11),(-.25,-.14),(-.05,-.155),(.17,-.145),(.5,-.10)]
       front=next(ya+(yb-ya)*(x-xa)/(xb-xa) for (xa,ya),(xb,yb) in zip(breaks,breaks[1:]) if xa-1e-8<=x<=xb+1e-8)+.008*z
       if ring==0:verts.append((x,front,z))
       elif ring==1:verts.append((x*.97+.008,.07,z*.98+.002))
       else:verts.append((x*.81-.025,.145+.035*math.cos(x*5+z*8),z*.87+.009))
     faces=[tuple(range(n)),tuple(reversed([2*n+k for k in range(n)]))]
     for r in range(2):
      for k in range(n):faces.append((r*n+k,(r+1)*n+k,(r+1)*n+(k+1)%n,r*n+(k+1)%n))
     o=mesh_object('set-%d-lamina-%02d'%(g+1,j),verts,faces,mats,c)
     for f in o.data.polygons:f.material_index=idx if f.index==0 else (idx if f.index==1 else 4)
   b+=spacing;j+=1

 # Consolidate semantic layer sets; retain loose lamina solids for editing.
 for g in range(1,4):
  bpy.ops.object.select_all(action='DESELECT')
  obs=[o for o in c.all_objects if o.type=='MESH' and o.name.startswith('set-'+str(g)+'-')]
  for o in obs:o.select_set(True)
  bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join()
  obs[0].name='crossbed-set-'+str(g)

def chimney(c):
 mats=[make_material(n,col,.9) for n,col in [('sulfide-ground','#77786A'),('pale-mineral-accretion','#AAA78B'),('inner-conduit','#4F544B'),('ochre-deposit','#8D866A')]]
 N=40;R=36;v=[];f=[];mi=[]
 def gauss(a,t,aa,tt,ww,hh):
  d=math.atan2(math.sin(a-aa),math.cos(a-aa));return math.exp(-(d/ww)**2-((t-tt)/hh)**2)
 # Retains original broad height/radius and wandering axis; deposits occupy
 # localized sectors at different heights rather than complete stacked rings.
 for inner in [False,True]:
  for j in range(R):
   u=j/(R-1);t=u+.008*math.sin(u*math.pi*5)*math.sin(u*math.pi)
   for k in range(N):
    a=2*math.pi*k/N;cx=.028*math.sin(t*4);cy=.016*math.sin(t*7)
    profile=.105+.130*(1-t)**1.7+.018*math.sin(t*math.pi*4+.6)*(1-.4*t)
    growth=.055*math.sin(3*a+t*3)+.032*math.sin(7*a-t*5)+.040*math.sin(a*4+.8)*math.exp(-((t-.35)/.23)**2)
    deposit=.027*gauss(a,t,-1.8,.29,.65,.15)+.021*gauss(a,t,.7,.57,.48,.20)+.016*gauss(a,t,2.7,.81,.8,.11)
    ribs=.007*math.sin(9*a+t*5)*(.35+.65*math.sin(t*9+a)**2)
    rad=(.026+.006*math.sin(t*5+a*2)) if inner else profile*(1+growth)+deposit+ribs+.004*math.sin(t*31+a*2)**3
    z=.85*t+(.014*math.sin(3*a+.4)+.007*math.sin(7*a))*t**9
    v.append((cx+rad*math.cos(a),cy+rad*math.sin(a),z))
 off=N*R
 for inner in [False,True]:
  for j in range(R-1):
   t=(j+.5)/(R-1)
   for k in range(N):
    a=2*math.pi*(k+.5)/N;q=(j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k)
    f.append(tuple(off+i for i in reversed(q)) if inner else q)
    field=math.sin(2.3*a+3*t)+.55*math.cos(5*a-12*t)+.35*math.sin(25*t+3*a)
    pale=gauss(a,t,-1.8,.29,.9,.22)+gauss(a,t,.7,.57,.7,.23)+gauss(a,t,2.7,.81,.7,.13)
    mi.append(2 if inner else (1 if pale>.57 and field>-.15 else 3 if field>.9 else 0))
 for k in range(N):
  q=(R-1)*N+k;b=(R-1)*N+(k+1)%N;f.append((q,b,off+b,off+q));mi.append(1)
  f.append((k,off+k,off+(k+1)%N,(k+1)%N));mi.append(0)
 o=mesh_object('continuous-sulfide-shell-and-open-conduit',v,f,mats,c)
 for p,m in zip(o.data.polygons,mi):p.material_index=m;p.use_smooth=(m==2)

for slug,fn in [('cross-bedded-sandstone',sandstone),('hydrothermal-chimney',chimney)]:
 c=setup_scene(slug,SEED);fn(c)
 export_asset(slug,{'en':slug+' calibration candidate','zh':'自然观感校准候选'},'geology',c,output_root=HERE,render=False,max_triangles=14000,max_materials=6,max_primitives=30,metadata={'candidate_status':'pending independent QA and user calibration; no production approval','generator':'build.py','reference_pixel_status':'blocked: direct downloads HTTP 403; web image routes returned only text ImageDisplayed markers, no inspectable pixels','purpose':'evidence-informed stylized natural scene prop; not site-specific reconstruction','textures':0})
