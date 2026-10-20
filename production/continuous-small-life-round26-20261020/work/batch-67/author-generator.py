from pathlib import Path
import json,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round26-20261020/work/batch-67';T=Path('/workspace/shared/lowpoly-batch65-20261020/production/continuous-small-life-round25-20261020/work/batch-65');s=(T/'generator.py').read_text();pre=s[:s.index('# ORIGINAL batch65')].replace('Original batch60 geometry','Original batch67 geometry');footer=s[s.index('ground_asset(col,center_xy=True)'):];body=r'''
# Original geometry authored AFTER the immutable batch67 freeze.
def marpolia():
 import random
 rng=random.Random(67);n=28
 rings=[]
 for z,scale in [(0,.88),(.0008,1),(.0017,.94)]:
  rings.append([(.022*scale*(1+.08*math.sin(i*2.1))*math.cos(i*math.tau/n),.016*scale*(1+.06*math.cos(i*1.7))*math.sin(i*math.tau/n),z+.00015*math.sin(i*2.7) if z else 0) for i in range(n)])
 loft('original_shale_flake',rings,'shale')
 # 52 representative main strands, each splits near basal quarter only.
 for i in range(52):
  t=i/51;a=-1.22+2.44*t;length=.022+rng.uniform(-.003,.003);base=(rng.uniform(-.0018,.0018),-.010+rng.uniform(-.0004,.0004),.00185)
  pts=[]
  for j in range(8):
   q=j/7;pts.append((base[0]+length*q*math.sin(a)+.00035*math.sin(q*7+i)*q,base[1]+length*q*math.cos(a),base[2]+.00012*math.sin(q*5+i)))
  tube('dense_slender_upper_unbranched_filaments',pts,[.000075*(1-.65*j/7) for j in range(8)],'filament' if i%3 else 'filamentlight',4)
  branch=pts[1];delta=(-1 if i%2 else 1)*.08
  pp=[branch]
  for j in range(1,7):
   q=j/6;pp.append((branch[0]+length*.78*q*math.sin(a+delta)+.00025*math.sin(q*5+i)*q,branch[1]+length*.78*q*math.cos(a+delta),branch[2]+.00013*math.sin(q*6+i)))
  tube('basal_quarter_secondary_fine_filaments',pp,[.000055*(1-.7*j/6) for j in range(7)],'filament',4)

def balanced():
 n=18
 def rock(name,profiles,mat):
  rings=[]
  for j,(z,rx,ry,xo) in enumerate(profiles):
   rings.append([(xo+rx*(1+.06*math.sin(i*2.9+j*.8))*math.cos(i*math.tau/n),ry*(1+.06*math.cos(i*2.4+j))*math.sin(i*math.tau/n),z+.045*math.sin(i*2.2+j) if z else 0) for i in range(n)])
  loft(name,rings,mat)
 rock('low_flared_eroded_footing',[(0,2.35,1.62,0),(.22,2.22,1.5,0),(.48,1.35,1.02,-.1)],'base')
 rock('attached_short_narrow_pedestal',[(.20,1.24,.95,-.12),(.65,.95,.75,-.05),(1.15,.62,.54,.02),(1.67,.48,.44,.08),(2.15,.67,.58,.02)],'pedestal')
 rock('broad_asymmetric_upper_boulder',[(1.96,.71,.61,.04),(2.23,1.50,1.05,.16),(2.85,2.02,1.37,.10),(3.56,1.87,1.27,-.02),(4.10,1.40,1.03,-.17),(4.32,.70,.58,-.26)],'rock')

def valley():
 xs=[-9,-7.4,-6.3,-5.6,-4.8,-4.4,-3.7,-2,0,2,3.7,4.4,4.8,5.6,6.3,7.4,9];zs=[7.65,7.9,6.9,5.6,2.7,1.5,1.05,.98,.96,.98,1.05,1.5,2.7,5.6,6.9,7.9,7.65];ny=20;nx=len(xs);vs=[];fs=[]
 for j in range(ny+1):
  y=-11.5+23*j/ny;offset=.22*math.sin(y*.27)
  for i,(x,z) in enumerate(zip(xs,zs)):vs.append((x+offset*(1-abs(x)/9),y,z+(.17*math.sin(y*.8+i*2.4) if abs(x)>4.4 else .035*math.sin(y*.5+i))))
 for j in range(ny):
  for i in range(nx-1):
   k=j*nx+i;fs.extend([(k,k+1,k+nx+1),(k,k+nx+1,k+nx)])
 perimeter=list(range(nx))+[j*nx+nx-1 for j in range(1,ny+1)]+[ny*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-1,0,-1)];o=len(vs)
 for k in perimeter:vs.append((vs[k][0],vs[k][1],0))
 for i,k in enumerate(perimeter):q=(i+1)%len(perimeter);fs.append((k,o+i,o+q,perimeter[q]))
 fs.append(tuple(o+i for i in range(len(perimeter)-1,-1,-1)));part('broad_floor_steep_parallel_walls_closed_cutaway',vs,fs,'rock')

def pavement():
 import random
 rng=random.Random(67)
 # Deterministic original 2D Voronoi cells, no scipy dependency.
 boundary=[(2.35*(1+.025*math.sin(i*2.5))*math.cos(i*math.tau/40),2.0*(1+.025*math.cos(i*1.7))*math.sin(i*math.tau/40)) for i in range(40)]
 loft('thin_closed_sandy_substrate',[[(x*.98,y*.98,0) for x,y in boundary],[(x,y,.13) for x,y in boundary]],'sand')
 sites=[]
 for j in range(12):
  for i in range(14):
   x=-2.35+(i+.5+rng.uniform(-.28,.28))*4.7/14;y=-2+(j+.5+rng.uniform(-.28,.28))*4/12
   if (x/2.45)**2+(y/2.1)**2<1.05:sites.append((x,y))
 def clip(poly,a,b,c):
  out=[]
  for i,p in enumerate(poly):
   q=poly[(i+1)%len(poly)];dp=a*p[0]+b*p[1]-c;dq=a*q[0]+b*q[1]-c
   if dp<=1e-10:out.append(p)
   if (dp<0)!=(dq<0):
    t=dp/(dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
  return out
 for k,(x,y) in enumerate(sites):
  poly=boundary[:]
  for l,(u,v) in enumerate(sites):
   if k==l:continue
   poly=clip(poly,u-x,v-y,(u*u+v*v-x*x-y*y)/2)
   if not poly:break
  if len(poly)<3:continue
  cx=sum(p[0] for p in poly)/len(poly);cy=sum(p[1] for p in poly)/len(poly);poly=[(cx+(p[0]-cx)*.97,cy+(p[1]-cy)*.97) for p in poly];h=.08+rng.random()*.10;n=len(poly)
  vs=[(u,v,.105) for u,v in poly]+[(cx+(u-cx)*.91,cy+(v-cy)*.91,.13+h*.7+rng.uniform(-.015,.015)) for u,v in poly]+[(cx+rng.uniform(-.025,.025),cy+rng.uniform(-.025,.025),.13+h)];fs=[tuple(range(n-1,-1,-1))]
  for i in range(n):q=(i+1)%n;fs.extend([(i,q,n+q,n+i),(n+i,n+q,2*n)])
  part('densely_fitted_original_angular_clasts',vs,fs,['clast','clastlight','clastdark'][k%3])

{'marpolia':marpolia,'balanced-rock':balanced,'u-shaped-glacial-valley':valley,'desert-pavement':pavement}[slug]()
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if slug=='marpolia' and mat=='shale':
  obj.data.materials.append(m['shaleedge'])
  for p in obj.data.polygons:p.material_index=1 if p.normal.z<.4 else 0
 if slug=='balanced-rock' and mat=='rock':
  obj.data.materials.append(m['rocklight'])
  for p in obj.data.polygons:p.material_index=1 if p.index%7 in [1,4] else 0
 if slug=='u-shaped-glacial-valley':
  for key in ['rocklight','floor','cut']:obj.data.materials.append(m[key])
  for p in obj.data.polygons:p.material_index=2 if p.center.z<1.2 and p.normal.z>.7 else 3 if abs(p.normal.y)>.85 or p.normal.z<-.9 else 1 if p.index%7==0 else 0
'''
(W/'generator.py').write_text(pre+body+footer)
for x in json.load(open(W/'final-selection.json')):
 b=R/x['path'];shutil.copy(W/'generator.py',b/'generator.py');(b/'authoring-start.json').write_text(json.dumps({'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Observed generator creation after frozen complete design. No geometry before this.'},indent=2)+'\n')
for n in ['blender-locked.sh','count-source-vertices.py','render-fixed8.py','runtime-parse.mjs','compose-sheets.py','run-lifecycle.py','render-delivery.py','package-candidates.py','close-dependencies.py']:
 t=(T/n).read_text().replace('round25','round26').replace('batch-65','batch-67').replace('batch65','batch67').replace("'seed':65","'seed':67")
 (W/n).write_text(t)
(W/'blender-locked.sh').chmod(0o755)
# Avoid preliminary render: delivery subject will be schema-checked before only final proof run.
p=W/'run-lifecycle.py';t=p.read_text();start=t.index(" if not (b/'proof-final/render-manifest.json').exists():");end=t.index("run(W,'runtime'",start);t=t[:start]+t[end:];p.write_text(t)
