from pathlib import Path
R=Path.cwd();W=R/'production/continuous-small-life-round27-20261020/work/batch-68/lava-r002-repair';old=R/'assets/candidates/continuous-small-life-round27-20261020/batch-68/lava-dome/r001/generator.py';b=old.parent.parent/'r002'
s=old.read_text();head=s[:s.index('# Original batch68 geometry')];tail=s[s.index('ground_asset(col,center_xy=True)'):]
geo='''# Original r002 continuous fractured extrusion, authored after immutable repair freeze.
import random
rng=random.Random(cfg['seed'])
def fractured_dome():
 # Coarse fracture regions distributed in plan across summit AND flanks, never in a latitude belt.
 seeds=[]
 while len(seeds)<96:
  p=(rng.uniform(-1,1),rng.uniform(-1,1))
  if p[0]*p[0]+p[1]*p[1]<1.03 and all(math.hypot(p[0]-x,p[1]-y)>.12 for x,y in seeds):seeds.append(p)
 outline=[]
 for i in range(48):
  a=i*math.tau/48;r=1+.035*math.sin(3*a+.4)+.022*math.sin(7*a)
  outline.append((r*math.cos(a),r*math.sin(a)))
 def clip(poly,A,B,C):
  out=[]
  for p,q in zip(poly,poly[1:]+poly[:1]):
   f=A*p[0]+B*p[1]-C;g=A*q[0]+B*q[1]-C
   if f<=1e-9:out.append(p)
   if (f<0)!=(g<0):
    t=f/(f-g);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return out
 def height(x,y):
  a=math.atan2(y,x);lim=1+.035*math.sin(3*a+.4)+.022*math.sin(7*a);r=math.hypot(x,y)/lim
  return 43*math.sqrt(max(0,1-min(1,r)**3.1))*(1+.018*math.sin(x*3+y*2))
 vertices=[];faces=[];materials=[];lookup={}
 def vert(x,y,z):
  p=(round(60*x,7),round(50*y,7),round(z,7))
  if p not in lookup:lookup[p]=len(vertices);vertices.append(p)
  return lookup[p]
 for k,(x,y) in enumerate(seeds):
  poly=outline[:]
  for j,(u,v) in enumerate(seeds):
   if k!=j:poly=clip(poly,2*(u-x),2*(v-y),u*u+v*v-x*x-y*y)
  if len(poly)<3:continue
  cx=sum(x for x,y in poly)/len(poly);cy=sum(y for x,y in poly)/len(poly);n=len(poly)
  # A joined seam, a narrow fractured shoulder and a broad irregular inclined rock plate.
  # Every region remains physically welded into the single extrusion surface.
  lifts=[0,rng.uniform(.7,2.2),rng.uniform(.4,2.0)];rings=[]
  for j,t in enumerate([1,.90,.64]):
   ring=[]
   for x,y in poly:
    xx=cx+(x-cx)*t;yy=cy+(y-cy)*t;h=height(xx,yy)
    if j==0:z=max(0,h-1.25)
    else:z=h+lifts[j]*(.75+.25*math.sin(k*1.1+x*11-y*9))
    ring.append(vert(xx,yy,z))
   rings.append(ring)
  mat='block' if (cx*.7+cy*.2)>.06 else 'core'
  for j in range(2):
   for i in range(n):q=(i+1)%n;faces.append((rings[j][i],rings[j][q],rings[j+1][q],rings[j+1][i]));materials.append('dark' if j==0 and k%5==0 else mat)
  c=vert(cx,cy,height(cx,cy)+rng.uniform(.1,1.9))
  for i in range(n):faces.append((rings[-1][i],rings[-1][(i+1)%n],c));materials.append(mat)
 # The exterior edge closes to a shallow irregular contact skirt and solid underside.
 edges={}
 for f in faces:
  for a,b in zip(f,f[1:]+f[:1]):key=tuple(sorted((a,b)));edges[key]=edges.get(key,0)+1
 boundary=[e for e,n in edges.items() if n==1];base=[]
 for a,b in boundary:
  x,y,z=vertices[a];u,v,w=vertices[b];aa=vert(x/60,y/50,-.6);bb=vert(u/60,v/50,-.6);faces.append((a,b,bb,aa));materials.append('rubble');base.extend([aa,bb])
 base=sorted(set(base),key=lambda i:math.atan2(vertices[i][1]/50,vertices[i][0]/60));faces.append(tuple(base));materials.append('core')
 obj=mesh_object('single_welded_bulbous_dome_coarse_fractured_summit_and_flanks',vertices,faces,[m[k] for k in cfg['palette']],col);keys=list(cfg['palette'])
 for p,k in zip(obj.data.polygons,materials):p.material_index=keys.index(k)
fractured_dome()
'''
(b/'generator.py').write_text(head+geo+tail);print(b/'generator.py')
