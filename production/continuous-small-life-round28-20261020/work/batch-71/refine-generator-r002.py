from pathlib import Path
R=Path.cwd();W=R/'production/continuous-small-life-round28-20261020/work/batch-71';p=W/'generator.py';s=p.read_text();(W/'generator-r001.py').write_text(s)
s=s.replace('n=128;nr=20','n=112;nr=20')
s=s.replace("t=i*math.tau/n;r=.075*j/nr*(1+.007*math.sin(t*5)+.004*math.sin(t*11));x,y=r*math.cos(t),r*math.sin(t);z=upper(x,y) if surface==0 else lower(x,y)","""t=i*math.tau/n;q=(-t)%math.tau;gutcenter=.034+.0035*math.sin(q*.7);gutwidth=.0058 if q<3.9 else .0028
    rr=[.0045,.009,.0135,.018,.0225,.0265,gutcenter-gutwidth,gutcenter,gutcenter+gutwidth,.047,.051,.055,.059,.063,.066,.0685,.071,.073,.074,.075]
    r=rr[j-1]*(1+.007*math.sin(t*5)+.004*math.sin(t*11));x,y=r*math.cos(t),r*math.sin(t);z=upper(x,y) if surface==0 else lower(x,y)""")
s=s.replace("if surf==0 and projection(x,y):mat='projection'\n     elif surf==0 and i%5==0:mat='rays'", "if surf==0 and j in [6,7] and .22<(-math.atan2(y,x))%math.tau<5.92:mat='projection'")
s=s.replace("if .22<q<5.50:","if .22<q<5.92:")
# Natural irregular coherent bedrock replacement.
a=s.index('def roche():');b=s.index('\ndef maar():',a)
s=s[:a]+'''def roche():
 xs=[-18,-16.5,-14,-11,-8,-5.5,-2,1,4,6.8,8.3,9.1,9.8,11.4,14.1,18];heights=[.45,.9,1.65,2.6,3.8,4.6,5.7,6.6,7.1,7.45,7.2,5.8,2.8,.9,.65,.45];ny=24;vs=[];fs=[];mats=[]
 for j,(x,h) in enumerate(zip(xs,heights)):
  for i in range(ny+1):
   v=-1+2*i/ny
   if i not in [0,ny]:v+=rng.uniform(-.022,.022)
   y=v*12*(.97+.03*math.sin(j*.8));f=math.sin(i*math.pi/ny);xx=x+(.50*math.sin(i*1.71+j*.9)+rng.uniform(-.22,.22))*f
   if 7<x<12:xx+=1.0*math.sin(y*.61)+.45*math.sin(y*1.35)
   cross=max(0,1-v*v)**.66;z=.4+h*cross*(1+.035*math.sin(y*.5+x*.2)+.02*math.sin(y*1.0-x*.13))
   if x<8 and abs(v)<.85:
    for g,depth in [(-7.4,.12),(-4.6,.20),(-1.3,.13),(2.8,.19),(5.9,.10)]:z-=depth*math.exp(-((y-g-.15*math.sin(x*.4))/.40)**2)*math.sin((x+18)*math.pi/29)**2
   if 7<x<12:
    z+=(.32*math.sin(i*1.91+j*.7)+rng.uniform(-.21,.21))*cross
    z-=.8*math.exp(-((y+3.1)/.6)**2)*cross
   vs.append((xx,y,z))
 for j in range(len(xs)-1):
  for i in range(ny):
   a=j*(ny+1)+i;b=a+1;c=a+ny+1;d=c+1
   for f in ([(a,c,b),(b,c,d)] if rng.random()<.5 else [(a,c,d),(a,d,b)]):fs.append(f);mats.append('fracture' if xs[j]>=7.5 else 'bedrock')
 boundary=list(range(ny+1))+[j*(ny+1)+ny for j in range(1,len(xs))]+[(len(xs)-1)*(ny+1)+i for i in range(ny-1,-1,-1)]+[j*(ny+1) for j in range(len(xs)-2,0,-1)];bottom=len(vs)
 vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],bottom+q,bottom+i));mats.append('ground')
 fs.append(tuple(bottom+i for i in range(len(boundary)-1,-1,-1)));mats.append('ground');multi('coherent_bedrock_stoss_and_irregularly_plucked_lee',vs,fs,mats)
''' +s[b:]
a=s.index('def maar():');b=s.index('\ndef terrace():',a)
s=s[:a]+'''def maar():
 # Uneven Cartesian triangulation avoids repeated radial belts and circular puck framing.
 nx=48;ny=44;vs=[];fs=[];mats=[];rr=[]
 for j in range(ny+1):
  for i in range(nx+1):
   x=-60+120*i/nx;y=-55+110*j/ny
   if i not in [0,nx]:x+=rng.uniform(-.65,.65)
   if j not in [0,ny]:y+=rng.uniform(-.65,.65)
   t=math.atan2(y/45,x/51);r=math.hypot(x/51,y/45)*(1+.035*math.sin(t*3+.4)+.027*math.sin(t*7-1))
   if r<.30:z=6+.30*(r/.30)**2
   elif r<.69:z=6.30+15.1*((r-.30)/.39)**1.15
   elif r<.81:z=21.4+.58*math.sin((r-.69)/.12*math.pi)
   elif r<1.15:z=21.4-1.4*((r-.81)/.34)
   else:z=20
   z+=.16*math.sin(x*.23+y*.06)*math.sin(y*.19-x*.04)
   if .32<r<.70:z+=(.5*math.sin(t*7+r*5)+.26*math.sin(t*17-1.2)+.19*math.cos(t*11+.2))*math.sin((r-.32)/.38*math.pi)
   # Slight original irregular cutaway outline, no named-site replication.
   xx=x+(1.0*math.sin(y*.18)+.5*math.cos(y*.39))*abs(x/60)**8;yy=y+(.8*math.sin(x*.14)+.4*math.cos(x*.31))*abs(y/55)**8
   vs.append((xx,yy,z));rr.append(r)
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+1;c=a+nx+1;d=c+1
   for f in ([(a,c,d),(a,d,b)] if rng.random()<.5 else [(a,c,b),(b,c,d)]):
    r=sum(rr[k] for k in f)/3;x=sum(vs[k][0] for k in f)/3;y=sum(vs[k][1] for k in f)/3;patch=math.sin(x*.18+y*.08)+.55*math.sin(x*.28-y*.17)
    mat='floor' if r<.32 else ('wallshade' if patch>.5 else 'wall') if r<.69 else 'ejecta' if r<1.05+.045*patch else 'country';fs.append(f);mats.append(mat)
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)];bot=len(vs);vs.extend([(vs[a][0],vs[a][1],0) for a in boundary])
 for i,a in enumerate(boundary):q=(i+1)%len(boundary);fs.append((a,boundary[q],bot+q,bot+i));mats.append('country')
 fs.append(tuple(bot+i for i in range(len(boundary)-1,-1,-1)));mats.append('country');o=multi('country_ground_cutaway_with_excavated_maar_and_low_apron',vs,fs,mats);o['country_surface_z_m']=20.;o['crater_floor_z_m']=6.;o['rim_nominal_z_m']=22.
''' +s[b:]
s=s.replace("c=2.1*math.sin(y/16)","c=2.1*math.sin(y/16)")
s=s.replace("f=math.sin(math.pi*(x+40)/80);xx=x+c*f+.38*math.sin(y*.31+i*.7)*f;zz=z+(.12*math.sin(y*.33+x*.18) if z>3 else .025*math.sin(y*.31));vs.append((xx,y,zz))", """f=math.sin(math.pi*(x+40)/80);bankweight=math.exp(-((abs(x)-14.6)/6)**2)
   scallop=(1.9*math.sin(y*.21+(1 if x>0 else 0))+.65*math.sin(y*.53+(.5 if x>0 else 2)))*bankweight
   xx=x+c*f+scallop;zz=z+(.12*math.sin(y*.33+x*.18) if z>3 else .025*math.sin(y*.31))
   if 3<z<10.9:zz-=.9*math.exp(-((y-(8 if x<0 else -15))/2.2)**2)*math.sin((z-3)/8*math.pi)
   vs.append((xx,y,zz))""")
s=s.replace("mats.append('shade' if i%9<3 else 'sediment')", "mats.append('sediment')")
s=s.replace('Original batch71 geometry authored after complete immutable14:30:50Z freezes.','Original batch71 r002 refinements authored after immutable14:36:03Z repair freezes; r001 retained.')
p.write_text(s)
# Render new exact final GLBs at clear illustrative oblique angle. Canonical orthogonal views unchanged.
p=W/'render-fixed8.py';s=p.read_text();s=s.replace('if args.glb.parent.parent.name == "hanging-valley":','if args.glb.parent.parent.name in ["eldonia","roche-moutonnee","maar-crater","river-terrace"]:').replace('DIRECTIONS.update(hero=(325,25),reversehero=(145,25),clay=(325,25),silhouette=(325,25))','DIRECTIONS.update(hero=(35,32),reversehero=(215,32),clay=(35,32),silhouette=(35,32))');p.write_text(s)
import json,shutil
for x in json.loads((W/'final-selection.json').read_text()):shutil.copy(W/'generator.py',R/x['path']/'generator.py')
