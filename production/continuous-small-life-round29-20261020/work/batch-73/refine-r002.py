# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round29-20261020/work/batch-73';p=W/'generator.py';t=p.read_text();t=t.replace('Original batch73 geometry authored after all four immutable15:01:31Z freezes.','Original batch73 r002 implementation repairs authored after15:07:20Z repair freezes; r001 retained.')
start=t.index('    v=abs(y)/width;');end=t.index('\n   vs.append((xx,yy,z))',start)
t=t[:start]+'''    v=abs(y)/width;best=-1.;bestk=0;bestlocal=0
    # Unequal compact lobate primary units, each with its OWN branching phase.
    for k in range(-13,14):
     root=k*.0096+.00035*math.sin(k*1.7);bend=.0038*math.sin(v*1.8)*(-1 if k>0 else 1)+.0004*math.sin(k*2.1)*v
     half=.0047*(1-.46*v*v)*(1+.06*math.sin(k*1.41));local=(x-root-bend)/half
     shape=max(0,1-local*local)**.65
     if shape>best:best=shape;bestk=k;bestlocal=local
    primary=max(0,best);k=bestk;local=bestlocal
    phase=v*(5.4+.63*math.sin(k*1.37))+.23*local+.08*math.sin(v*10+k)
    secondary=max(0,math.sin(math.pi*(phase%1)))**.8
    tertiary=.82+.18*max(0,math.sin(phase*math.pi*3+local*1.3))
    edge=min(1,(1-v)*15);z+=edge*(.0016*primary+.0010*primary*secondary*tertiary-.0008*(1-primary))
    if abs(y)<.0012:z=.0091+.00013*math.cos(x*100)''' +t[end:]
t=t.replace("xx=x+(.08*math.sin(y*2.2)+.04*math.cos(y*4.3))*abs(x/6)**8;yy=y*(.982+.018*math.sin(x*.72))", "xx=x+(.19*math.sin(y*1.7)+.10*math.cos(y*3.1))*abs(x/6)**8;yy=y*(.94+.04*math.sin(x*.58)+.02*math.cos(x*1.33))")
t=t.replace("z=1.05+.055*math.sin(x*.43)+.026*math.cos(y*.9+x*.14)","z=1.05+.075*math.sin(x*.43)+.035*math.cos(y*.9+x*.14)+.012*math.sin(x*2.1+y*3.1)\n   z-=.10*math.exp(-((x+1.2-.24*y)/.11)**2)\n   z-=.08*max(0,(abs(y)-3.5)/.5)")
t=t.replace(".12*math.sin(x*.44+k)",".22*math.sin(x*.44+k)")
a=t.index('def fumarole():');b=t.index('\ndef bif():',a)
t=t[:a]+'''def fumarole():
 nx=38;ny=16;vs=[];fs=[];ms=[];tags=[]
 for j in range(ny+1):
  for i in range(nx+1):
   x=-2+4*i/nx;end=max(0,1-(x/1.43)**2);w=.035+.23*end**.48;wl=w*(1+.23*math.sin(x*4+.7));wr=w*(1+.17*math.sin(x*5-1))
   outer=1.29+.08*math.sin(x*3.4)+.04*math.sin(x*8);center=.075*math.sin(x*2.8)+.035*math.sin(x*7)
   ys=[-outer,-1,-.68,-wl-.18,-wl-.065,-wl,-wl*.91,-wl*.55,0,wr*.55,wr*.91,wr,wr+.065,wr+.18,.68,1,outer]
   y=ys[j]+center;xx=x+(.10*math.sin(y*3.9)+.055*math.cos(y*8))*abs(x/2)**8
   z=.43+.037*math.sin(x*3.7+y*2)+.025*math.sin(x*8-y*5)+.015*math.cos(x*11+y*9)
   active=end>0
   if j in [7,8,9]:z=.075+.025*math.sin(x*4+y*5) if active else z-.045
   elif j in [6,10]:z=.19+.035*math.sin(x*7+j) if active else z-.055
   elif j in [5,11]:z-=.055 if active else .09
   crust=active and j in [3,4,5,11,12,13] and ((j<8 and math.sin(x*4+.4)>-.35) or (j>8 and math.sin(x*4-1)>.0))
   if crust:z+=.035+.035*(.5+.5*math.sin(i*2.2+j*1.7))
   # A branching ground crack extends diagonally off the crooked terminal slit.
   crack=abs(y-(.50+.65*(x-.6)))
   if x>.55 and j>10:z-=.085*math.exp(-(crack/.055)**2)
   vs.append((xx,y,z));tags.append('interior' if active and 6<=j<=10 else 'crust' if crust else 'rock')
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in ([(a,c,d),(a,d,b)] if (i+j)%2 else [(a,c,b),(b,c,d)]):
    fs.append(f);ncr=sum(tags[k]=='crust' for k in f);ni=sum(tags[k]=='interior' for k in f);mat='interior' if ni>=2 else ('ochre' if (i+j)%7==1 else 'crust') if ncr>=2 else 'rock';ms.append(mat)
 o=finish_grid('single_fractured_terrain_with_crooked_deep_fissure_and_rough_interrupted_crust',vs,fs,ms,nx,ny,'rock');o['scope']='Static generic mineral-encrusted vent, no chemistry/temperature claim'
''' +t[b:]
t=t.replace("rib=[-.003,.006,.001,-.004][q]*(.8+.2*math.sin(j*1.9))", "rib=[-.002,.005,.001,-.003][q]*(.65+.35*math.sin(j*1.9)**2)")
t=t.replace("taper=.91+.10*math.sin(math.pi*h)-.05*h", "taper=(.70+.31*math.sin(math.pi*h))*(1-.66*max(0,(h-.66)/.34)**1.15)")
t=t.replace("x=(.4*taper+rib)*xx*shape;y=(.2*taper+rib*.75)*yy*shape", "erosion=.007*math.sin(t*5+j*.43)+.004*math.sin(t*11-j*.27)\n    rib*=.7+.3*math.sin(t*3+j*.31)**2\n    notch=.020*math.exp(-((t-2.8)/.17)**2)*math.exp(-((h-.48)/.20)**2)\n    x=(.4*taper+rib+erosion-notch)*xx*shape;y=(.2*taper+rib*.75+erosion*.6-notch*.6)*yy*shape")
t=t.replace("z=z0+fold*math.sin(math.pi*h)+.010*math.sin(t*3+1)*h**5", "z=z0+fold*math.sin(math.pi*h)+.022*math.sin(t*3+1)*h**5+.0022*math.sin(t*7+j*.37)*math.sin(math.pi*h)")
a=t.index(' records.append((units-1,4))');b=t.index(' for j in range(len(records)-1):',a)
t=t[:a]+''' records.append((units-1,4))
 for i in range(n):
  t=i*math.tau/n;shape=1+.05*math.sin(t*5+.4)+.025*math.cos(t*9-1);xx=math.copysign(abs(math.cos(t))**.57,math.cos(t));yy=math.copysign(abs(math.sin(t))**.57,math.sin(t));vs.append((.4*.238*xx*shape,.2*.238*yy*shape,.65+.022*math.sin(t*3+1)))
''' +t[b:]
t=t.replace("fs.append(tuple(o+i for i in range(n)));ms.append('break');o=multi", "center=len(vs);vs.append((.012,-.008,.665))\n for i in range(n):fs.append((o+i,o+(i+1)%n,center));ms.append('break')\n o=multi")
p.write_text(t)
for x in json.loads((W/'final-selection.json').read_text()):
 b=R/x['path'];shutil.copy(p,b/'generator.py');files=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py'];(b/'build-dependencies.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seed':73,'blender':'4.3.2','three':'0.180.0','files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
print('r002 generator closure fixed',datetime.datetime.now(datetime.timezone.utc).isoformat())
