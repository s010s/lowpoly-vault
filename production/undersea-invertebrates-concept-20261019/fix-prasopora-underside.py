from pathlib import Path
import json,shutil
B=Path('production/undersea-invertebrates-concept-20261019');A=Path('assets/candidates/undersea-invertebrates-concept-20261019');old=A/'prasopora/r002';d=A/'prasopora/r003';d.mkdir(exist_ok=True)
for f in ['brief.md','references.json','build-config.json']:shutil.copy2(old/f,d/f)
s=(old/'generator.py').read_text();a=s.index(' rr=[(0,.026');z=s.index('\n return mats\n\ndef strophomena',a)
s=s[:a]+''' # Real closed radially corrugated underside. No planar cap hiding the folds.
 profile=[(.00045,.00015,0,0)]
 for rad in [.004,.006,.0072,.008,.0088,.010,.0128,.014,.0152,.017,.0188,.020,.0212,.023,.024,.025,.026]:
  depth=.00050-.00042*sum(math.exp(-((rad-r)/.00070)**2) for r in [.008,.014,.020,.025])
  profile.append((depth,rad,0,0))
 profile.extend([(.00035,.028,0,0),(.00070,.0296,0,0),(.0016,.0305,0,0),(.0028,.0303,0,0),(.0032,.0299,0,0),(.003,.00015,0,0)])
 loft('Closed epitheca with visible concentric lower folds',profile,48,mats[2])'''+s[z:]
(d/'generator.py').write_text(s);cfg=json.loads((d/'build-config.json').read_text());cfg['revision']='r003';(d/'build-config.json').write_text(json.dumps(cfg,indent=2)+'\n');(d/'brief.md').write_text((d/'brief.md').read_text()+'\nr003 follows actual 512px bottom-frame inspection: r002 cap hid concentric folds. Replace cap and separate fold loops with one closed radially corrugated epitheca underside. Pore dome unchanged.\n')
j=json.loads((B/'refined-build-jobs.json').read_text());j['jobs']=[q for q in j['jobs'] if q['asset_id']=='prasopora']
for q in j['jobs']:q['revision']='r003';q['job_id']='underside-repair';q['inputs']={k:v.replace('/r002/','/r003/') for k,v in q['inputs'].items()}
(B/'underside-build-jobs.json').write_text(json.dumps(j,indent=2)+'\n')
