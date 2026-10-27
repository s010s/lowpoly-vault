# SPDX-License-Identifier: MIT
"""Original Paradoxides davidis davidis surface patch model; design units millimetres.
All dorsal patches share actual edge vertices. Neutral underside is an unsegmented
technical closure, not preserved ventral anatomy. No scan or source pixels used.
"""
import math
from collections import Counter

def build_geometry():
 V=[];F=[];T=[];G={};connections=[]
 def vert(p,group):
  i=len(V);V.append(tuple(float(x) for x in p));G.setdefault(group,set()).add(i);return i
 def face(ids,tag):
  assert len(set(ids))==len(ids)
  if len(ids)==3:F.append(tuple(ids));T.append(tag)
  else:
   a,b,c,d=ids;F.extend([(a,b,c),(a,c,d)]);T.extend([tag,tag])
 def bridge(a,b,tag):
  assert len(a)==len(b)
  for i in range(len(a)-1):face((a[i],a[i+1],b[i+1],b[i]),tag)
 def mark(ids,group):G.setdefault(group,set()).update(ids)
 xf=[-1,-.8,-.5,0,.5,.8,1]
 trows=[0,.24,.70,1]
 pitch=5.2;ystart=-58
 def corewidth(y):return 18-10*max(0,min(1,(y-ystart)/(20*pitch)))**1.15
 def coreheight(xratio,y,t):
  i=max(0,min(20,(y-ystart)/pitch));edge=6.6-1.6*i/20
  arch=(11.4-4.6*i/20)*(max(0,1-xratio*xratio)**.72)
  ridge=(2.1-.5*i/20)*math.sin(math.pi*t)**1.1
  return edge+arch+ridge
 # Broad semicircular cephalon, swollen anterior glabella, paired curved eye lobes.
 cols=[-65,-60,-55,-50,-45,-40,-36,-32,-28,-24,-21,-18,-14.4,-9,0,9,14.4,18,21,24,28,32,36,40,45,50,55,60,65]
 rowspec=[(-119,10),(-117,19),(-114,28),(-110,36),(-106,43),(-102,48),(-98,52),(-94,56),(-90,59),(-86,61),(-82,62.5),(-78,63.5),(-74,64),(-70,64.5),(-66,65),(-58,65)]
 def headheight(x,y,w):
  base=2.6+5.8*max(0,1-(x/w)**2)**.65
  bulb=15*math.exp(-((y+103)/18)**2)*math.exp(-(x/24)**4)
  stem=7*math.exp(-((y+78)/14)**4)*math.exp(-(x/18)**4)
  groove=sum(1.5*math.exp(-((y-a)/1.2)**2)*math.exp(-(x/19)**6) for a in [-88,-80,-73])
  # Sessile crescent ridge follows an arc rather than a globular eye primitive.
  eye_x=25.5+7.2*math.sin(math.pi*max(0,min(1,(y+103)/34)))
  eye=3.7*math.exp(-((abs(x)-eye_x)/2.5)**2)*math.exp(-((y+87)/14)**6)
  # Subdued cranidial furrow immediately beside the axial lobe.
  axial_furrow=1.4*math.exp(-((abs(x)-22)/1.7)**2)*math.exp(-((y+84)/20)**6)
  return max(1.9,base+bulb+stem-groove+eye-axial_furrow)
 head=[]
 for r,(y,w) in enumerate(rowspec):
  row=[]
  actual_cols=[cx*w/65 for cx in cols]
  if -106<=y<=-70:
   eye_x=25.5+7.2*math.sin(math.pi*max(0,min(1,(y+103)/34)))
   e=eye_x-4
   pos=[0,e*.22,e*.40,e*.58,e*.74,e*.88,e,eye_x-2,eye_x,eye_x+2,eye_x+4,(eye_x+4+w)/2,w*.88,w*.95,w]
   assert pos==sorted(pos),(y,pos)
   actual_cols=[-x for x in pos[:0:-1]]+pos
  for x in actual_cols:
   yy=y;z=headheight(x,yy,w)
   if r==len(rowspec)-1:
    yy=ystart-5*max(0,(abs(x)-18)/47)
    if abs(x)<=18+1e-8:z=coreheight(x/18,ystart,0)
    else:z=6.6-3.8*(abs(x)-18)/47
   row.append(vert((x,yy,z),'cephalon'))
  head.append(row)
  if r:bridge(head[r-1],row,'head')
 apex=vert((0,-120,2.5),'cephalon')
 for i in range(len(cols)-1):face((apex,head[0][i+1],head[0][i]),'head')
 # Genal spines branch from the real posterior head edge.
 for side in [-1,1]:
  selected=[i for i,c in enumerate(cols) if (50<=c<=65 if side>0 else -65<=c<=-50)]
  first=[head[-1][i] for i in selected];seq=first
  group='genal-spine-'+('L' if side<0 else 'R');mark(first,group)
  specs=[(-47,59.5,5.6,3.0),(-26,62,3.6,2.6),(-5,62,1.8,2.0)]
  for y,center,half,z in specs:
   row=[]
   for j in range(len(seq)):
    q=-1+2*j/(len(seq)-1);x=(side*center)+q*half
    row.append(vert((x,y,z+1.3*(1-q*q)),group))
   bridge(seq,row,'head');seq=row
  tip=vert((side*60.5,13,1.45),group)
  for j in range(len(seq)-1):face((seq[j],seq[j+1],tip),'head')
  connections.append({'part':group,'shared_dorsal_root_vertices':first,'method':'Same indexed head-edge vertices, no overlapping separate object.'})
 # Exactly20 thoracic tergites, actual connected raised axial strips and pleural wings.
 firstcore=[head[-1][cols.index(x)] for x in [-18,-14.4,-9,0,9,14.4,18]]
 previous=firstcore;segment_edges=[]
 widths=[43,44.5,45,45.3,45.5,45.5,45.2,44.8,44.2,43.6,42.8,41.7,40.3,38.6,36.5,33.8,30.5,27,22,18]
 sweeps=[8,8,8,8,8,9,9,10,10,11,12,13,15,18,22,27,32,39,48,75]
 for i in range(20):
  group=f'thoracic-tergite-{i+1:02d}';core=[previous];mark(previous,group)
  for t in trows[1:]:
   y=ystart+(i+t)*pitch;w=corewidth(y)
   row=[vert((q*w,y,coreheight(q,y,t)),group) for q in xf]
   bridge(core[-1],row,'axis');core.append(row)
  previous=core[-1];segment_edges.append([core[0][0],core[0][-1],core[-1][0],core[-1][-1]])
  for side in [-1,1]:
   edge=[r[-1 if side>0 else 0] for r in core];seq=edge;mark(edge,group)
   if i<19:
    # Curved, low-arched leaf. Gap increases gently outward, not detached bars.
    for u in [.22,.45,.66,.84,.95]:
     row=[]
     for t,idx in zip(trows,edge):
      x0,y0,z0=V[idx];x=abs(x0)+(widths[i]-abs(x0))*u
      center=ystart+(i+.5)*pitch+sweeps[i]*(u**1.75)
      y=center+(t-.5)*pitch*(1-.20*u)
      z=(6.6-1.6*i/20)*(1-u)+1.55*u+(2.8-.7*i/20)*math.sin(math.pi*t)*math.sin(math.pi*(.10+.90*u))
      row.append(vert((side*x,y,z),group))
     bridge(seq,row,'pleura');seq=row
    tip=vert((side*widths[i],ystart+(i+.5)*pitch+sweeps[i]+1,1.15),group)
    for j in range(len(seq)-1):face((seq[j],seq[j+1],tip),'pleura')
   else:
    # Final thoracic pair: long sabre blades bend toward the axis, no median telson.
    for y,x,half,z in [(54,10.6,1.8,4.7),(69,12.5,1.7,3.6),(88,13.5,1.4,2.7),(106,11.2,.8,1.9)]:
     row=[]
     for t in trows:
      # Cross-section transverse to the longitudinal blade; root is rotated continuously.
      q=2*t-1;row.append(vert((side*(x-q*half),y+q*1.0,z+1.0*(1-q*q)),group))
     bridge(seq,row,'pleura');seq=row
    tip=vert((side*8,120,1.15),group)
    for j in range(len(seq)-1):face((seq[j],seq[j+1],tip),'pleura')
   connections.append({'part':group+('-L-pleura' if side<0 else '-R-pleura'),'shared_dorsal_root_vertices':edge,'method':'Exact shared edge indices with its axial tergite.'})
 # Small narrow pygidium follows last axial edge; never a broad terminal shield.
 seq=previous;mark(seq,'pygidium')
 for y,w,z in [(49,7.5,9.6),(53,6.3,7.0),(57,3.6,3.2)]:
  row=[vert((q*w,y,2.4+(z-2.4)*(1-q*q)**.7),'pygidium') for q in xf]
  bridge(seq,row,'axis');seq=row
 tip=vert((0,59,1.7),'pygidium')
 for j in range(len(seq)-1):face((seq[j],seq[j+1],tip),'axis')
 # Ensure each top triangle winds +Z; topology is surface patches, not Boolean overlap.
 for k,f in enumerate(F):
  a,b,c=[V[j] for j in f];area=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
  if area<0:F[k]=f[::-1]
  assert abs(area)>1e-8,(k,f,'degenerate projected face')
 top_n=len(V);top_f=len(F);edgecounts=Counter(tuple(sorted((a,b))) for f in F for a,b in zip(f,f[1:]+f[:1]));assert max(edgecounts.values())<=2
 directed=[(a,b) for f in F for a,b in zip(f,f[1:]+f[:1]) if edgecounts[tuple(sorted((a,b)))]==1]
 # No underside segmentation: neutral nearly planar closure tracks the anatomical perimeter.
 V.extend((x,y,0.0) for x,y,z in V[:top_n])
 G['technical-art-underside-NOT-anatomy']=set(range(top_n,len(V)))
 for f in list(F):F.append(tuple(i+top_n for i in f[::-1]));T.append('closure')
 for a,b in directed:face((a,a+top_n,b+top_n,b),'closure')
 for k,ids in list(G.items()):
  if k!='technical-art-underside-NOT-anatomy':G[k]=set(ids)|{i+top_n for i in ids}
 # Global footprint center, zero technical underside datum. No individual part scaling.
 ys=[v[1] for v in V];offset=(min(ys)+max(ys))/2
 V=[(x,y-offset,z) for x,y,z in V]
 return V,F,T,{k:sorted(ids) for k,ids in G.items()},{'connections':connections,'thoracic_tergites':20,'top_surface_vertices':top_n,'top_surface_triangles':top_f,'boundary_edges_closed':len(directed),'construction':'One continuous indexed dorsal surface with neutral duplicate-plan closure and boundary walls. No separate overlapping parts.','underside':'Technical artistic closure only, not ventral anatomy or a display base.','offset_y_mm':-offset}

if __name__=='__main__':
 v,f,t,g,m=build_geometry();print(len(v),len(f),len(g),m['boundary_edges_closed'])
