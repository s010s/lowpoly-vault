from pathlib import Path
import datetime,json,hashlib,shutil
R=Path.cwd();B=R/'assets/candidates/continuous-small-life-round26-20261020/batch-66';W=R/'production/continuous-small-life-round26-20261020/work/batch-66-repair-r002';old=(B/'louisella/r001/generator.py').read_text();prefix=old[:old.index('# Geometry authored')];tail=old[old.index('ground_asset(col,center_xy=True)'):]
body=r'''
# Isolatedr002 geometry authored AFTER frozen derived repair plan. Originalr001 untouched.
import random
rng=random.Random(cfg['seed'])
def louisella():
 n=20
 def center(t):return Vector((.014*math.sin(t*math.tau),-.15+.30*t,.018+.003*math.sin(t*math.tau)))
 def radius(t):
  if t>=.97:return .0075*math.sqrt(max(.004,1-((t-.97)/.03)**2))
  levels=[(0,.0015),(.08,.0024),(.16,.0045),(.24,.0048),(.28,.011),(.38,.013),(.43,.015),(.60,.0145),(.64,.012),(.85,.011),(.88,.0078),(.97,.0075)]
  for (a,r),(b,s) in zip(levels,levels[1:]):
   if a<=t<=b:return r+(s-r)*(t-a)/(b-a)
  return .0075
 def frame(t):
  tangent=(center(min(1,t+.001))-center(max(0,t-.001))).normalized();u=Vector((tangent.y,-tangent.x,0)).normalized();v=u.cross(tangent).normalized();return u,v
 rings=[]
 samples=[(.009,.00035),(0,.0008),(0,.0015)]
 for i in range(1,121):
  t=.97*i/120
  # Four distinct structural textures; smooth posterior is not a pointed annulated cone.
  amplitude=.105 if .41<t<.63 else .022 if t<.87 else 0
  rr=radius(t)*(1+amplitude*math.cos((t-.41)*math.tau/.0162));samples.append((t,rr))
 for j in range(1,13):
  t=.97+.03*j/12;samples.append((t,radius(t)))
 for t,r in samples:
  c=center(t);u,v=frame(t);rings.append([tuple(c+r*(u*math.cos(k*math.tau/n)+v*math.sin(k*math.tau/n))) for k in range(n)])
 loft('whole_body_spiny_anterior_coarse_annular_middle_papillate_zone_smooth_blunt_rear',rings,'body')
 # Dense short scalids on anterior trunk, sparse fine trunk rings toward papillate zone.
 for j in range(15):
  t=.29+j*.038;c=center(t);u,v=frame(t);r=radius(t)
  for k in range(10):
   a=k*math.tau/10+(j%2)*.2;d=u*math.cos(a)+v*math.sin(a);length=.0018 if t<.41 else .0009
   tube('short_trunk_spine_rings_rear_excluded',[tuple(c+d*(r-.0002)),tuple(c+d*(r+length))],[.00048,.00009],'spines',5)
 for j in range(7):
  t=.025+j*.028;c=center(t);u,v=frame(t)
  for k in range(8):
   a=k*math.tau/8+j*.3;d=u*math.cos(a)+v*math.sin(a);r=radius(t);tube('fine_proboscis_scalids',[tuple(c+d*(r-.0001)),tuple(c+d*(r+.00065))],[.00024,.00006],'spines',5)
 t=.125;c=center(t);u,v=frame(t)
 for k in range(25):
  a=k*math.tau/25;d=u*math.cos(a)+v*math.sin(a);tube('proboscis_exactly_25_long_midlength_scalids',[tuple(c+d*(radius(t)-.0001)),tuple(c+d*(radius(t)+.0042)+Vector((0,-.001,0)))],[.00045,.00008],'spines',5)
 # Widely separated genuinely cylindrical blunt papillae, NOT tiny pointed surface dots/legs.
 for j in range(22):
  t=.46+j*.0185;c=center(t);u,v=frame(t);r=radius(t)
  for side in [-1,1]:
   d=(v*.70+u*side*.714).normalized();start=c+d*(r-.0003);end=c+d*(r+.0048)
   tube('two_widely_separated_dorsal_longitudinal_blunt_papilla_rows',[tuple(start),tuple(start.lerp(end,.82)),tuple(end)],[.00145,.0014,.00115],'papilla',7)
 # Tiny posterior aperture at the center of a hemispherical rear, no projecting tail appendage.
 c=center(1);ellipsoid('small_posterior_aperture',tuple(c+Vector((0,.00004,0))),(.0005,.00010,.0005),'mouth',10,4)
def hoodoo():
 n=28;rings=[]
 # Continuous shaft taper, no periodic radius expansions at4global tier levels.
 # Local asymmetric shoulders occupy limited azimuth spans and unequal elevations.
 ledges=[(1.20,.42,.35,.80,.38),(3.72,.36,.31,3.25,.62),(6.18,.26,.23,5.20,.43)]
 def adiff(a,b):return (a-b+math.pi)%math.tau-math.pi
 for j in range(42):
  z=7.35*j/41;cx=.22*math.sin(z*.66)+.12*math.sin(z*1.5);cy=.16*math.sin(z*.8)
  # Broad eroded foot, unequal broad shoulders; neither encircles full shaft.
  base=.46+1.0*math.exp(-z/1.32)+.09*math.exp(-((z-4.6)/.8)**2)
  ring=[]
  for i in range(n):
   a=i*math.tau/n
   r=base*(1+.10*math.sin(a*3+z*.6)+.055*math.sin(a*7-z*.8))
   r+=.22*math.exp(-((z-2.25)/.63)**2)*math.exp(-(adiff(a,1.8)/1.0)**4)
   r+=.16*math.exp(-((z-5.1)/.92)**2)*math.exp(-(adiff(a,4.4)/.8)**4)
   for h,amp,width,az,span in ledges:
    local=math.exp(-(adiff(a,az)/span)**4)
    # Narrow projection plus soft undercut below, spatially local not a full rim.
    r+=local*(amp*math.exp(-((z-h)/width)**4)-amp*.32*math.exp(-((z-(h-.38))/(width*.8))**2))
   zz=z if j==0 else z+.065*math.sin(3*a+z*.4)
   ring.append((cx+r*math.cos(a),cy+r*.90*math.sin(a),zz))
  rings.append(ring)
 # Real coherent modest cap joined to shaft, not a detached broad boulder.
 for z,r in [(7.38,.65),(7.67,.67),(8.0,.55)]:
  cx=.22*math.sin(z*.66)+.12*math.sin(z*1.5);cy=.16*math.sin(z*.8)
  rings.append([(cx+r*(1+.10*math.sin(i*1.7))*math.cos(i*math.tau/n),cy+r*.90*(1+.1*math.sin(i*2.1))*math.sin(i*math.tau/n),z+.06*math.sin(i*1.3)) for i in range(n)])
 loft('irregular_tapered_erosional_pillar_with_three_interrupted_unequal_local_ledges',rings,'rock')
{'louisella':louisella,'hoodoo':hoodoo}[slug]()
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if mat=='body':
  for k in ['pale','neck','mouth']:obj.data.materials.append(m[k])
  obj.data.update()
  for p in obj.data.polygons:
   t=(p.center.y+.15)/.30;p.material_index=3 if t<.01 and p.center.y>-.1498 else 2 if .26<t<.41 else 1 if t>.87 or .41<t<.64 else 0
 elif slug=='hoodoo':
  for k in ['pale','rust','cap']:obj.data.materials.append(m[k])
  obj.data.update()
  for p in obj.data.polygons:
   x,y,z=p.center;a=math.atan2(y,x)
   # Broken mineral bands follow limited asymmetrical eroded patches, no4horizontal rings.
   pale=(abs(z-(1.25+.20*math.sin(a*2)))<.24 and math.cos(a-.35)>.35) or (abs(z-(3.8+.24*math.sin(a)))<.28 and math.cos(a-3.25)>.65) or (abs(z-(6.2+.13*math.sin(a*3)))<.18 and math.cos(a-5.2)>.72)
   p.material_index=3 if z>7.35 else 1 if pale else 2 if (2.7<z<3.35 and x>-.1) or (4.65<z<5.75 and y<.15) else 0
'''
for slug in ['louisella','hoodoo']:
 b=B/slug/'r002';(b/'generator.py').write_text(prefix+body+tail)
 deps=json.loads((B/slug/'r001/build-dependencies.json').read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();deps.update(generator_sha256=H(b/'generator.py'),config_sha256=H(b/'build-config.json'),repair_plan_sha256=H(b/'repair-plan.json'));(b/'build-dependencies.json').write_text(json.dumps(deps,indent=2)+'\n')
 (b/'chronology-clarification.json').write_text(json.dumps({'repair_plan_frozen_at':json.loads((b/'modeling-freeze.json').read_text())['frozen_at'],'repair_generator_completed_observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Bounded repair under original genuine concept/primary sources, not a new concept or changedscope. Original provider/authoring timestamp unknowns remain unchanged; actual new process intervals recorded separately.'},indent=2)+'\n')
print('REPAIR GENERATORS AUTHORED',datetime.datetime.now(datetime.timezone.utc).isoformat())
