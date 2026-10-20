# SPDX-License-Identifier: MIT
from pathlib import Path
import json,shutil,hashlib,datetime
w=Path('production/small-life-batch79');p=w/'generator.py';s=p.read_text()
s=s.replace("x=-.075+.15*i/nx;u=x/.0575;v=y/.065;r=math.sqrt(u*u+v*v)","ux=-1+2*i/nx;vy=y/.09;x=.075*ux*math.sqrt(1-.45*vy*vy);yp=y*math.sqrt(1-.45*ux*ux);u=x/.0575;v=yp/.065;r=math.sqrt(u*u+v*v)")
s=s.replace("phase=(y+.010*(abs(u)**1.4)*math.sin(y*14)+(.00045 if x>seamx else 0))/.0039","phase=(yp+.017*(abs(u)**1.4)*math.sin(yp*14)+(.00065 if x>seamx else 0))/.0039")
s=s.replace("amu=max(0,min(1,(.058-y)/.012))","amu=max(0,min(1,(.057-yp)/.020))")
s=s.replace("mask*(-.00065+.00105*ribs*amu+.00028*(1-r*r))","mask*(-.0008+.0026*ribs*amu+.00038*(1-r*r))")
s=s.replace("seam=.0004*math.exp(-((x-seamx)/.0012)**2)","seam=.00115*math.exp(-((x-seamx)/.0018)**2)")
s=s.replace("yy=y+.0016*math.sin(x*98-.2)*(abs(y/.09)**8)","yy=yp+.0016*math.sin(x*98-.2)*(abs(y/.09)**8)")
s=s.replace("xx=x+.07*math.sin(i*1.37+j*.68)*math.sin(math.pi*i/nx);yy=y+.06*math.sin(i*.93+j*1.47)*math.sin(math.pi*j/ny)","xx=x+rng.uniform(-.085,.085)*math.sin(math.pi*i/nx);yy=y+rng.uniform(-.12,.12)*math.sin(math.pi*j/ny)")
s=s.replace("grain=.035*math.sin(i*7.31+j*4.67)+.025*math.cos(i*3.2-j*5.7)","grain=rng.uniform(-.052,.052)")
s=s.replace("if z<.8 and (i*17+j*31)%19<3:mat='gravel'","if z<.8 and rng.random()<.025:mat='gravel'")
s=s.replace("z+=1.0*math.sin(t*7+r*25)*r*(1-r)+.7*math.sin(13*t-r*21)*r*(1-r)","z+=10*math.sin(t*7+r*25)*r*(1-r)+7*math.sin(13*t-r*21)*r*(1-r)")
s=s.replace("fval=math.sin(t*3+.7+r*4)+.6*math.sin(t*7-r*3)","cx,cy,_=vs[a];fval=math.sin(cx*.006+math.sin(cy*.007))+.6*math.sin(cy*.009+cx*.003)")
start=s.index('def schist():');end=s.index("{'dickinsonia':fossil",start)
s=s[:start]+'''def schist():
 n=144;nz=31;vs=[];fs=[];ms=[]
 for j in range(nz):
  q=j/(nz-1);radius=(1-.96*q**3.0)
  for i in range(n):
   t=math.tau*i/n;ang=t+.006*math.sin(i*3.71+j*.81)*math.sin(math.pi*q)
   shape=1+.09*math.sin(3*t+.4)+.04*math.sin(7*t+1.2)
   x=1.6*radius*shape*math.cos(ang);y=.9*radius*shape*math.sin(ang)
   z=2.08*q+(.10*math.sin(t*3+.5)+.07*math.sin(7*t))*math.sin(math.pi*q)
   # Unequal steep foliation and localized joint offsets through whole rock skin.
   coord=x+.29*z+.08*math.sin(z*3.3+x*.8)+.055*math.sin(x*4.2)
   phase=coord*7.6+.36*math.sin(coord*4.7)+.13*math.sin(z*5.1+coord)
   f=phase-math.floor(phase);flake=f/.82 if f<.82 else (1-f)/.18
   amp=(.020+.027*(.5+.5*math.sin(z*5.2+math.floor(phase)*1.7)))*math.sin(math.pi*q)**.4
   rough=.025*math.sin(x*5.3+z*2.7)+.012*math.sin(y*7.4-z*4.1)
   delta=amp*(flake-.35)+rough*math.sin(math.pi*q)
   x+=math.cos(ang)*delta;y+=math.sin(ang)*delta
   vs.append((x,y,max(0,z)))
 for j in range(nz-1):
  for i in range(n):
   a=j*n+i;b=j*n+(i+1)%n;c=a+n;d=b+n
   mat='mica' if rng.random()<.10 else 'schist'
   if rng.random()<.035:mat='fracture'
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append(mat)
 base=len(vs);vs.append((0,0,0));top=len(vs);vs.append((0,0,2.13))
 for i in range(n):
  k=(i+1)%n;fs.append((base,k,i));ms.append('schist');fs.append((top,(nz-1)*n+i,(nz-1)*n+k));ms.append('schist')
 ob=multi('original_irregular_coherent_schist_outcrop_full_surface_wavy_flaky_foliation',vs,fs,ms);ob['scope']='Generic physically foliated mica schist, no exact locality/age. Unequal flakes are integral geometry.'
''' + s[end:]
p.write_text(s)
a=json.loads((w/'final-selection.json').read_text());(w/'selection-before-r003.json').write_text(json.dumps(a,indent=2)+'\n')
keep=['brief.json','brief.md','references.json','build-config.json','modeling-freeze.json','premodel-schema-check.json','concept-original.png','concept-prompt.txt','concept-generation.json','build-dependencies.json']
for x in a:
 old=Path(x['path']);new=old.parent/'r003';new.mkdir()
 for n in keep:shutil.copyfile(old/n,new/n)
 (new/'generator.py').write_text(s);d=json.loads((new/'build-dependencies.json').read_text());d['generator_sha256']=hashlib.sha256((new/'generator.py').read_bytes()).hexdigest();(new/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
 reasons={'dickinsonia':'Original8 frame inspection: hero/clay mould ribs and seam too weak and matrix overly square. Increase actual rib/seam relief within original low-relief fossil scope, broaden anterior smooth region, round stone footprint. No camera/render changes.','arroyo-wash':'Original8 frame inspection: periodic diagonal terrain ripple and regularly patterned gravel colors read too mechanical. Replace periodic relief sampling with seeded irregular geometry jitter and much sparser randomized gray gravel accents. Dry incision unchanged.','shield-volcano':'Original8 frame inspection: radial material wedges and overly featureless broad mass. Replace origin-radial patch function by Cartesian irregular cooled-flow regions and add restrained integral uneven relief. Low-angle silhouette and small shallow depression unchanged.','schist-outcrop':'Original8 frame inspection: equal barcode front ridges and ruled sheet top/sides fail original physically natural foliation intent. Reconstruct whole outcrop as irregular closed crown mass with unequal wavy steep foliation/flaky relief on complete skin, no flat ruled top or unchanged rectangle shell. No camera/material hiding.'}
 (new/'repair-freeze.json').write_text(json.dumps({'revision':'r003','frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_frozen_design_unchanged':True,'reason':reasons[x['asset_id']],'generator_sha256':hashlib.sha256((new/'generator.py').read_bytes()).hexdigest(),'source_revision':x['revision']},indent=2)+'\n');x['revision']='r003';x['path']=str(new)
(w/'final-selection.json').write_text(json.dumps(a,indent=2)+'\n')
