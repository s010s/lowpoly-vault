from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round24-20261020/work/batch-62';B=R/'assets/candidates/continuous-small-life-round24-20261020/batch-62/dinomischus';old=B/'r001';b=B/'r002';b.mkdir(exist_ok=False)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['brief.json','brief.md','candidate-brief.json','references.json','modeling-freeze.json','concept-original.png','concept-prompt.txt','concept-generation.json']:shutil.copyfile(old/n,b/n)
c=json.loads((old/'build-config.json').read_text());c['revision']='r002';(b/'build-config.json').write_text(json.dumps(c,indent=2)+'\n')
s=(old/'generator.py').read_text();a=s.index(' rings=[[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z+');z=s.index(' for j in range(gp[\'bracts\']):',a)
s=s[:a]+''' # Single contiguous cup surface turns inward, avoiding coincident opposing caps.
 rings=[[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z+(.0024 if z>=.018 else 0)) for i in range(n)] for z,r in prof]
 rings += [[(r*math.cos(i*math.tau/n),r*math.sin(i*math.tau/n),z) for i in range(n)] for r,z in [(.0028,.02445),(.0018,.0242),(.0008,.0241)]]
 loft('bulb_stem_and_open_calyx_full_organism',rings,'body')
'''+s[z:]
# Raise opening discs onto shallow inner floor at their actual radii.
s=s.replace('(x,y,.02424)','(x,y,.02413)')
(b/'generator.py').write_text(s)
(b/'repair-freeze.json').write_text(json.dumps({'frozen_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repair':'Remove coincident shallow bowl cap/outer cap overlap causing black top; continuous outer to inner cup surface and two subtle opening discs. Same full-organism factual scope,20bracts, dimensions and palette.','parent_glb_sha256':H(old/'model.glb'),'brief_sha256':H(b/'candidate-brief.json'),'config_sha256':H(b/'build-config.json'),'generator_sha256':H(b/'generator.py')},indent=2)+'\n')
deps=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py',W/'render-fixed8.py'];(b/'build-dependencies.json').write_text(json.dumps({str(p.relative_to(R)):H(p) for p in deps},indent=2)+'\n')
x={'asset_id':'dinomischus','revision':'r002','path':str(b.relative_to(R))};(W/'repair-selection.json').write_text(json.dumps([x],indent=2)+'\n')
s=(W/'run-lifecycle.py').read_text().replace("W/'final-selection.json'","W/'repair-selection.json'").replace("'runtime'","'runtime-repair'").replace("'rebuild-jobs.json'","'repair-rebuild-jobs.json'").replace("'rebuild-runs'","'repair-rebuild-runs'").replace("'rebuild-queue'","'repair-rebuild-queue'").replace("'source-counts'","'source-counts-repair'");(W/'run-repair-lifecycle.py').write_text(s)
