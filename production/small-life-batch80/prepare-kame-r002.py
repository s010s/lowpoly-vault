# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/small-life-batch80';a=W/'assets/kame-mound/r001';b=a.parent/'r002';b.mkdir();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json']:shutil.copy(a/n,b/n)
(b/'repair-freeze.json').write_text(json.dumps(dict(created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),revision='r002',original_revision='r001',reason='Actual final hero/top inspection found regular grid triangulation/color speckling and insufficient low shoulder. Repair real surface to nonuniform facets and clearer unequal off-axis shoulder; preserve sources, generic sediment scope and illustrative scale.',original_generator_sha256=H(a/'generator.py'),original_brief_sha256=H(a/'brief.json'),original_references_sha256=H(a/'references.json'),repair_authored=False),indent=2)+'\n')
t=(a/'generator.py').read_text().replace("vs.append(coords(i/nx,j/ny,i,j))","\n   u=i/nx;v=j/ny\n   if 0<i<nx:u+=(rng.random()-.5)*.72/nx\n   if 0<j<ny:v+=(rng.random()-.5)*.72/ny\n   vs.append(coords(u,v,i,j))")
t=t.replace("22*math.exp(-((x+8)/22)**2-((y-2)/21)**2)+9*math.exp(-((x-20)/14)**2-((y+10)/14)**2)","22*math.exp(-((x+9)/20)**2-((y-3)/20)**2)+14*math.exp(-((x-23)/10)**2-((y+10)/12)**2)")
t=t.replace("rng.random()<.19", "rng.random()<.075").replace("(rng.random()-.4)*.95", "(rng.random()-.4)*.65")
(b/'generator.py').write_text(t)
# Apply nonuniform facets to the pending pediment repair too, before any build.
p=W/'assets/pediment/r002/generator.py';q=p.read_text().replace("vs.append(coords(i/nx,j/ny,i,j))","\n   u=i/nx;v=j/ny\n   if 0<i<nx:u+=(rng.random()-.5)*.72/nx\n   if 0<j<ny:v+=(rng.random()-.5)*.72/ny\n   vs.append(coords(u,v,i,j))");p.write_text(q)
