from pathlib import Path
import json,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round26-20261020/work/batch-67';P=W/'repair-pavement-r002';b=R/json.load(open(P/'final-selection.json'))[0]['path'];s=(b.parent/'r001/generator.py').read_text();a=s.index('def pavement():');z=s.index("\n{'marpolia':marpolia",a)
body=r'''def pavement():
 import random
 g=cfg['repair_geometry'];rng=random.Random(g['site_seed'])
 boundary=[(2.35*(1+.025*math.sin(i*2.5))*math.cos(i*math.tau/40),2.0*(1+.025*math.cos(i*1.7))*math.sin(i*math.tau/40)) for i in range(40)]
 loft('thin_closed_sandy_substrate',[[(x*.98,y*.98,0) for x,y in boundary],[(x,y,.13) for x,y in boundary]],'sand')
 sites=[]
 def add(x,y):
  if (x/2.45)**2+(y/2.1)**2>=1.02:return False
  if any((x-u)**2+(y-v)**2<g['minimum_site_distance']**2 for u,v in sites):return False
  sites.append((x,y));return True
 while len(sites)<g['base_sites']:add(rng.uniform(-2.4,2.4),rng.uniform(-2.05,2.05))
 # Dense pockets of small chips interrupt unequal large clasts; no regular grid.
 centers=[sites[i] for i in [3,9,17,22,29,35,44,51,60,67]]
 target=g['base_sites']+g['clustered_sites']
 while len(sites)<target:
  x,y=rng.choice(centers);add(x+rng.gauss(0,.30),y+rng.gauss(0,.30))
 def clip(poly,a,b,c):
  out=[]
  for i,p in enumerate(poly):
   q=poly[(i+1)%len(poly)];dp=a*p[0]+b*p[1]-c;dq=a*q[0]+b*q[1]-c
   if dp<=1e-10:out.append(p)
   if (dp<0)!=(dq<0):
    t=dp/(dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return out
 sizes=[]
 for k,(x,y) in enumerate(sites):
  poly=boundary[:]
  for l,(u,v) in enumerate(sites):
   if k==l:continue
   poly=clip(poly,u-x,v-y,(u*u+v*v-x*x-y*y)/2)
   if not poly:break
  if len(poly)<3:continue
  cx=sum(p[0] for p in poly)/len(poly);cy=sum(p[1] for p in poly)/len(poly)
  area=abs(sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))/2);sizes.append(area)
  # Asymmetric chips cut each cell edge at a different fraction; bottom footprint
  # remains close fitted while upper shoulders are uneven geological facets.
  chipped=[]
  for i,p in enumerate(poly):
   q=poly[(i+1)%len(poly)];t=rng.uniform(.25,.75)
   chipped.append((cx+(p[0]-cx)*.985,cy+(p[1]-cy)*.985))
   u=p[0]+t*(q[0]-p[0]);v=p[1]+t*(q[1]-p[1]);inset=rng.uniform(.94,.995)
   chipped.append((cx+(u-cx)*inset,cy+(v-cy)*inset))
  n=len(chipped);thickness=rng.uniform(*g['thickness_range'])*(min(1.2,max(.6,math.sqrt(area)/.32)))
  rim=[]
  for i,(u,v) in enumerate(chipped):
   inset=rng.uniform(*g['rim_inset_range']);rim.append((cx+(u-cx)*inset,cy+(v-cy)*inset,.135+thickness*rng.uniform(.35,.85)))
  # Offset crest not a repeating central pyramid; uneven rim sets asymmetric
  # wedge crowns and chipped bevels. Thickness is genuine vertex geometry.
  ax=rng.uniform(-.30,.30);ay=rng.uniform(-.30,.30);spanx=max(u for u,v in poly)-min(u for u,v in poly);spany=max(v for u,v in poly)-min(v for u,v in poly)
  vs=[(u,v,.105) for u,v in chipped]+rim+[(cx+ax*spanx,cy+ay*spany,.135+thickness)]
  fs=[tuple(range(n-1,-1,-1))]
  for i in range(n):q=(i+1)%n;fs.extend([(i,q,n+q,n+i),(n+i,n+q,2*n)])
  part('irregular_multiscale_chipped_clast_armor',vs,fs,['clast','clastlight','clastdark'][rng.randrange(3)])
 (out/'clast-layout-metrics.json').write_text(json.dumps({'clast_count':len(sizes),'planar_cell_area_m2':sorted(sizes),'max_to_min_area_ratio':max(sizes)/min(sizes),'non_grid_sites':sites,'note':'Original random multiscale clipped partitions provide dense lower footprints. Individually chipped angular outlines and uneven asymmetric crown vertices are actual geometry, not material or camera disguise.'},indent=2)+'\n')
'''
(b/'generator.py').write_text(s[:a]+body+s[z:]);(b/'authoring-start.json').write_text(json.dumps({'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'r002 generator authored after targeted repair freeze, original r001 immutable'},indent=2)+'\n')
for n in ['blender-locked.sh','count-source-vertices.py','render-fixed8.py','runtime-parse.mjs','compose-sheets.py','run-lifecycle.py','render-delivery.py','package-candidates.py','close-dependencies.py','prepare-delivery.py']:
 s=(W/n).read_text().replace("W=R/'production/continuous-small-life-round26-20261020/work/batch-67'","W=R/'production/continuous-small-life-round26-20261020/work/batch-67/repair-pavement-r002'")
 (P/n).write_text(s)
(P/'blender-locked.sh').chmod(0o755)
