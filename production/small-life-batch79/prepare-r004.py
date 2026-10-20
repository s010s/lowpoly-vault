# SPDX-License-Identifier: MIT
from pathlib import Path
import json,shutil,hashlib,datetime
w=Path('production/small-life-batch79');s=(w/'generator.py').read_text();start=s.index('def fossil():');end=s.index('def wash():',start)
s=s[:start]+'''def fossil():
 nx=28;ny=140;vs=[];fs=[];ms=[]
 # Rows follow ribs exactly so ridges are actual coherent geometry, not grid aliasing.
 for j in range(1,ny):
  v=-1+2*j/ny;yb=.065*v;width=.0575*math.sqrt(1-v*v)
  for i in range(nx+1):
   u=-1+2*i/nx;x=width*u;y=yb+.006*u*u*v+.00055*math.tanh(x/.002)
   mask=(max(0,1-u*u))**.35;amu=max(0,min(1,(.055-yb)/.018))
   rib=(.5+.5*math.cos(math.tau*j/4))**.8
   z=.008+mask*(-.0006+.0022*rib*amu+.00025*(1-v*v))-.0010*math.exp(-(x/.0018)**2)*amu
   vs.append((x,y,z))
 rows=ny-1
 for j in range(rows-1):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in [(a,b,d),(a,d,c)]:fs.append(f);ms.append('fossil')
 south=len(vs);vs.append((0,-.065,.008));north=len(vs);vs.append((0,.065,.008))
 for i in range(nx):
  fs.append((south,i+1,i));ms.append('fossil');a=(rows-1)*(nx+1)+i;fs.append((north,a,a+1));ms.append('fossil')
 boundary=[south]+[j*(nx+1)+nx for j in range(rows)]+[north]+[j*(nx+1) for j in range(rows-1,-1,-1)]
 outer=len(vs)
 for k in boundary:
  x,y,z=vs[k];t=math.atan2(y/.065,x/.0575);rad=1+.035*math.sin(5*t+.4)+.018*math.sin(9*t)
  vs.append((.075*rad*math.cos(t),.09*rad*math.sin(t),.008+.00025*math.sin(t*4+.2)))
 n=len(boundary)
 for i,a in enumerate(boundary):q=(i+1)%n;fs.append((a,boundary[q],outer+q,outer+i));ms.append('matrix')
 bottom=len(vs);vs.extend([(vs[outer+i][0],vs[outer+i][1],0) for i in range(n)])
 for i in range(n):q=(i+1)%n;fs.append((outer+i,outer+q,bottom+q,bottom+i));ms.append('edge')
 center=len(vs);vs.append((0,0,0))
 for i in range(n):fs.append((center,bottom+(i+1)%n,bottom+i));ms.append('edge')
 ob=multi('continuous_rib_aligned_Dickinsonia_fossil_mould_SAM_P47720_informed_matrix',vs,fs,ms);ob['scope']='Original broad oval fossil mould study;35 simplified serial ribs per side. Not living exterior or specimen facsimile.'

''' +s[end:]
start=s.index('def schist():');end=s.index("{'dickinsonia':fossil",start)
s=s[:start]+'''def schist():
 # Irregular unequal foliation-controlled cross sections form one connected solid.
 n=24;stations=[];u=-1.6;layer=0
 while u<1.6:
  width=rng.uniform(.045,.14);end=min(1.6,u+width)
  stations.extend([(u,layer,.0),(max(u+.008,end-.010),layer,1.)]);u=end;layer+=1
 stations.append((1.6,layer,0.))
 vs=[];fs=[];ms=[]
 for j,(u,layer,flange) in enumerate(stations):
  endtaper=.70+.30*math.sin(math.pi*(u+1.6)/3.2)**.45
  for k in range(n):
   t=math.tau*k/n;cy=math.cos(t);sz=math.sin(t)
   y=.78*math.copysign(abs(cy)**.68,cy);z=.99+1.00*math.copysign(abs(sz)**.70,sz)
   # Unequal plate breaks and wavy edges, no perfect periodic barcode or ruled roof.
   shape=endtaper*(1+.065*math.sin(t*3+layer*1.79)+.025*math.sin(t*7+layer*.7))
   ledge=(.035+.045*(.5+.5*math.sin(layer*2.3+t*.7)))*flange
   y=y*shape+math.copysign(ledge,y);z=.99+(z-.99)*shape+ledge*max(0,sz)
   x=u-.22*(z-.99)+.035*math.sin(z*3.8)
   vs.append((x,y,max(.0,z-.16)))
 rings=len(stations)
 for j in range(rings-1):
  for k in range(n):
   q=(k+1)%n;a=j*n+k;b=j*n+q;c=a+n;d=b+n
   for f in [(a,b,d),(a,d,c)]:
    fs.append(f);v=rng.random();ms.append('mica' if v<.035 else 'fracture' if v>.985 else 'schist')
 for row in [0,rings-1]:
  center=len(vs);u=stations[row][0];vs.append((u+.035*math.sin(.99*3.8),0,.83))
  for k in range(n):fs.append((center,row*n+k,row*n+(k+1)%n));ms.append('schist')
 ob=multi('irregular_schist_unequal_wavy_steep_foliation_controlled_full_volume_plate_fracture',vs,fs,ms);ob['scope']='Generic schist outcrop; unequal physical plate-like fractures on all surfaces, not banded gneiss or painted stripe.'

''' +s[end:]
(w/'generator-r004.py').write_text(s)
a=json.loads((w/'final-selection.json').read_text());(w/'selection-before-r004.json').write_text(json.dumps(a,indent=2)+'\n')
keep=['brief.json','brief.md','references.json','build-config.json','modeling-freeze.json','premodel-schema-check.json','concept-original.png','concept-prompt.txt','concept-generation.json','build-dependencies.json']
for x in a:
 if x['asset_id'] not in ['dickinsonia','schist-outcrop']:continue
 old=Path(x['path']);new=old.parent/'r004';new.mkdir()
 for n in keep:shutil.copyfile(old/n,new/n)
 (new/'generator.py').write_text(s);d=json.loads((new/'build-dependencies.json').read_text());d['generator_sha256']=hashlib.sha256((new/'generator.py').read_bytes()).hexdigest();(new/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
 reason='Rib-aligned actual surface topology removes previous grid moire/aliasing while retaining original low-relief mould scope,35 simplified ribs per side, broad undivided anterior and integral matrix. Earlier hero remained weak; no camera/renderer changes.' if x['asset_id']=='dickinsonia' else 'Earlier original r003 inspected hero/top/clay still mound-like with insufficient schist fracture. Replace radial crown with unequal wavy steep foliation-controlled closed rock cross sections and physical ledges across full volume, not material/camera hiding. Original source scope retained.'
 (new/'repair-freeze.json').write_text(json.dumps({'revision':'r004','frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_frozen_design_unchanged':True,'reason':reason,'generator_sha256':hashlib.sha256((new/'generator.py').read_bytes()).hexdigest(),'source_revision':x['revision']},indent=2)+'\n');x['revision']='r004';x['path']=str(new)
(w/'final-selection.json').write_text(json.dumps(a,indent=2)+'\n')
