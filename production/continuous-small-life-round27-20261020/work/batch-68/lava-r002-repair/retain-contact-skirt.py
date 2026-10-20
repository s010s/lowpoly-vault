from pathlib import Path
import shutil,json,hashlib,datetime
b=Path('assets/candidates/continuous-small-life-round27-20261020/batch-68/lava-dome/r002');a=b/'attempts/02-coherent-rind-before-contact-skirt';a.mkdir(parents=True)
(b/'contact-skirt-refinement.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'All eight512px diagnostics show original QA ring and bare summit removed. Preserve original brief secondary basal-rubble requirement using a few subordinate rooted fragments at contact, not a circumferential belt.','change':'Small angular low fragment clusters in three unequal basal sectors, attached into footprint, outside main summit/flank coarse relief. No change to scope/palette/camera/renderer.'},indent=2)+'\n')
for n in ['generator.py','model.glb','source.blend','source-metrics.json','metrics.json','source-final.report.json','source-vertex-counts.json','candidate-brief.json','build-dependencies.json','gltf-validator.report.json','runtime-parse.report.json','repro-final-1.report.json','repro-final-2.report.json','proof-final','proof-quick','preview.png','preproof-binding-check.json','build.log','quick.log','format.log','source-reopen.log','source-vertex-counts.log','proof-final.log','repro-final-1.log','repro-final-2.log']:
 if (b/n).exists():shutil.move(b/n,a/n)
s=(a/'generator.py').read_text();s=s.replace('fractured_dome()\nground_asset', '''fractured_dome()
# Subordinate rooted basal fragments in unequal contact sectors, never a mid-height belt.
for k,a in enumerate([-.25,-.13,.04,.17,.30,2.1,2.24,2.45,4.0,4.13,4.30]):
 r=1+.035*math.sin(3*a+.4)+.022*math.sin(7*a);cx=60*r*.99*math.cos(a);cy=50*r*.99*math.sin(a);n=5;rings=[]
 for level in [0,1]:
  ring=[]
  for j in range(n):
   q=a+j*math.tau/n;rr=1+.18*math.sin(j*2.1+k+level)
   ring.append((cx+(2.8+.6*math.sin(k))*rr*math.cos(q),cy+(2.3+.5*math.cos(k*1.3))*rr*math.sin(q),-.5 if level==0 else 1.0+1.2*(.5+.5*math.sin(k*1.8+j*.7))))
  rings.append(ring)
 loft('subordinate_rooted_contact_fragment_clusters',rings,'rubble' if k%4==0 else 'core')
for (name,mat),(vs,fs) in groups.items():mesh_object(name,vs,fs,m[mat],col)
ground_asset''')
(b/'generator.py').write_text(s);d=json.loads((a/'build-dependencies.json').read_text());d['generator_sha256']=hashlib.sha256((b/'generator.py').read_bytes()).hexdigest();(b/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
W=Path('production/continuous-small-life-round27-20261020/work/batch-68/lava-r002-repair');p=W/'run-lifecycle-final.py';s=(W/'run-lifecycle.py').read_text().replace("W/'rebuild-runs'", "W/'rebuild-runs-final'").replace("W/'rebuild-runs/build'", "W/'rebuild-runs-final/build'");p.write_text(s)
