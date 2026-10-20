# SPDX-License-Identifier: MIT
from pathlib import Path
import json,shutil,datetime,hashlib
R=Path.cwd();W=R/'production/continuous-small-life-round23-20261020/work/batch-61';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();old=json.loads((W/'final-selection.json').read_text());shutil.copyfile(W/'final-selection.json',W/'initial-selection.json');final=[]
repairs={
'pseudopulex':'Remove proud separate abdominal collars visible in r001 top/clay. Integrate eight shallow color-band regions directly in one closed abdominal shell, preserving original shape and setae. No scope, morphology or dimensions change.',
'daemonelix-helical-burrow':'Eliminate visible dark seam between capped helix and lower tunnel. Build chamber, tunnel, helix and neck as one continuous closed transported tube with shared rings. No hollow bore, coil-count or representation change.',
'mesa':'Remove rectangular attached buttress prisms which read as straps in r001 front/clay. Author integrated radial talus flutes and irregular erosion bays in a single closed layered mesa body. Preserve broad flat cap, stepped steep sides and original nominal envelope.',
'drumlin':'Replace piecewise height law with smooth normalized asymmetric beta profile to remove side-view cusp. Preserve broad rounded end, long low tapered end, convex cross-section, scale and no ice-direction claim.'}
#Freeze revised config/unchanged claims BEFORE authoring revised generator.
for x in old:
 b0=R/x['path'];b=b0.parent/'r002';b.mkdir()
 for n in ['brief.json','brief.md','references.json','concept-original.png','concept-prompt.txt','concept-generation.json']:shutil.copyfile(b0/n,b/n)
 cfg=json.loads((b0/'build-config.json').read_text());cfg['revision']='r002';cfg['repair_decision']=repairs[x['asset_id']];(b/'build-config.json').write_text(json.dumps(cfg,indent=2)+'\n')
 (b/'modeling-freeze.json').write_text(json.dumps({'schema_version':1,'frozen_at':now(),'status':'targeted repair under unchanged original premodel claim/design freeze','original_freeze_path':str((b0/'modeling-freeze.json').relative_to(R)),'original_freeze_sha256':H(b0/'modeling-freeze.json'),'brief_sha256':H(b/'brief.json'),'config_sha256':H(b/'build-config.json'),'references_sha256':H(b/'references.json'),'repair':repairs[x['asset_id']],'no_scope_narrowing':True},indent=2)+'\n')
 final.append({'asset_id':x['asset_id'],'revision':'r002','path':str(b.relative_to(R))})
s=(W/'generator.py').read_text()
start=s.index('n=20;ys=');end=s.index(" ellipsoid('compact_wingless_thorax'",start)
s=s[:start]+'''n=20;ys=[-.0035,-.0028,-.0014,.0002,.0018,.0034,.005,.0065,.0078,.0092];ws=[.00155,.0020,.00240,.0026,.00262,.00252,.00228,.00185,.00115,.00016];hs=[.00072,.00098,.00114,.00122,.00124,.00117,.00108,.00085,.00053,.00015]
 #Integrated surface material bands replace separate oversized collars.
 bands=[-.0032+j*.00148 for j in range(1,8)];stations=sorted(ys+[v for y in bands for v in [y-.00007,y+.00007]]);rings=[]
 def interp(y,values):
  for k in range(len(ys)-1):
   if ys[k]<=y<=ys[k+1]:t=(y-ys[k])/(ys[k+1]-ys[k]);return values[k]*(1-t)+values[k+1]*t
  return values[-1]
 for y in stations:
  w=interp(y,ws);h=interp(y,hs);rings.append([(w*math.cos(i*math.tau/n),y,.0032+h*math.sin(i*math.tau/n)) for i in range(n)])
 vs=[p for ring in rings for p in ring];fs=[tuple(range(n-1,-1,-1))];mi=[0]
 for j in range(len(rings)-1):
  mid=(stations[j]+stations[j+1])/2;band=1 if any(abs(mid-y)<.00007 for y in bands) else 0
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i));mi.append(band)
 fs.append(tuple((len(rings)-1)*n+i for i in range(n)));mi.append(0);obj=mesh_object('continuous_broad_abdomen_with_integral_suggested_bands',vs,fs,[m['abdomen'],m['ochre']],col)
 for p,i in zip(obj.data.polygons,mi):p.material_index=i
'''+s[end:]
s=s.replace(" tube('solid_continuous_four_and_half_turn_burrow_cast',points,radii,'cast',12)"," #Terminal chamber and helix share one continuous ring sequence, no joining caps.")
s=s.replace(" tube('continuous_lower_tunnel_and_expanded_terminal_chamber',lower,[0,.14,.17,.155,.10,.10,.10],'cast-light',14)"," tube('one_closed_chamber_tunnel_helix_and_neck',lower[:-1]+points,[0,.14,.17,.155,.10,.10]+radii,'cast',12)")
start=s.index(" n=gp['mesa_perimeter_steps'];levels=");end=s.index('\ndef drumlin():',start)
s=s[:start]+''' n=gp['mesa_perimeter_steps'];levels=gp['mesa_levels_m'];scale=[1,.97,.88,.85,.84,.85,.83,.83];rings=[]
 #All buttresses are now integral talus flutes, not attached rectangular prisms.
 for k,(z,sc) in enumerate(zip(levels,scale)):
  ring=[]
  for j in range(n):
   th=j*math.tau/n;outline=1+.075*math.sin(th*3+.4)+.042*math.sin(th*7+.2)+.028*math.cos(th*11)
   notch=max(0,math.sin(th*5+.4))**8;upper=outline-.085*notch
   flute=(.060*math.sin(th*9+.7)+.030*math.cos(th*13))*(1-k/7)
   r=upper+flute
   ring.append((300*sc*r*math.cos(th),225*sc*r*math.sin(th),z if k in [0,7] else z+1.5*math.sin(th*5+.8)))
  rings.append(ring)
 vs=[p for row in rings for p in row];fs=[tuple(range(n-1,-1,-1))];mats=['talus']
 for k in range(len(rings)-1):
  mat=['talus','talus','sandstone','pale','sandstone','upper','cap'][k]
  for j in range(n):
   aa=k*n+j;bb=k*n+(j+1)%n;cc=bb+n;dd=aa+n
   #Staggered triangulated scarp/talus faces make coherent broad facets.
   fs.extend([(aa,bb,dd),(bb,cc,dd)] if (j+k)%2 else [(aa,bb,cc),(aa,cc,dd)]);mats.extend([mat,mat])
 center=len(vs);vs.append((-15,8,180))
 for j in range(n):fs.append(((len(rings)-1)*n+j,(len(rings)-1)*n+(j+1)%n,center));mats.append('cap')
 matnames=list(dict.fromkeys(mats));obj=mesh_object('single_closed_broad_capped_mesa_integrated_scarps_and_talus',vs,fs,[m[mat] for mat in matnames],col)
 for poly,mat in zip(obj.data.polygons,mats):poly.material_index=matnames.index(mat)
'''+s[end:]
s=s.replace("width=75*(math.sin(math.pi*t)**.58)*(1.18-.60*t);h=35*((t/.24)**.72 if t<.24 else ((1-t)/.76)**1.55)","width=75*(math.sin(math.pi*t)**.58)*(1.18-.60*t)/.908;peak=.75/3.15;h=35*(t**.75*(1-t)**2.4)/(peak**.75*(1-peak)**2.4)")
(W/'generator-r002.py').write_text(s)
for x in final:
 b=R/x['path'];(b/'generator.py').write_text(s);d=json.loads((b/'brief.json').read_text());d['packaging_adapter']={'created_at':now(),'frozen_design_brief_sha256':H(b/'brief.json'),'note':'Original design and claims unchanged. r002 targeted geometry repairs documented in modeling-freeze. Artifact-role adapter only.'};d['required_deliverables']=[{'role':k,'path':str((b/n).relative_to(R)),'sha256':H(b/n)} for k,n in [('generator','generator.py'),('config','build-config.json')]];(b/'candidate-brief.json').write_text(json.dumps(d,indent=2)+'\n');(b/'build-dependencies.json').write_text(json.dumps({str(p.relative_to(R)):H(p) for p in [b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py',W/'render-fixed8.py']},indent=2)+'\n')
(W/'final-selection.json').write_text(json.dumps(final,indent=2)+'\n')
#New isolated queue/evidence destinations. Never overwrite initial runs.
s=(W/'run-lifecycle.py').read_text().replace("'rebuild-jobs.json'","'rebuild-r002-jobs.json'").replace("'rebuild-runs'","'rebuild-r002-runs'").replace("'rebuild-queue'","'rebuild-r002-queue'").replace("'runtime'","'runtime-r002'")
(W/'run-r002-lifecycle.py').write_text(s)
print('r002 repair briefs/configs frozen; revised generator authored',now())
