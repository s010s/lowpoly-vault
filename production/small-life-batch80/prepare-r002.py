# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/small-life-batch80';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for slug in ['spriggina','pediment']:
 a=W/'assets'/slug/'r001';b=a.parent/'r002';b.mkdir()
 for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json']:shutil.copy(a/n,b/n)
 fix='Improve actual impressed fossil geometry: larger legible shallow negative relief and wider median ridge, more irregular broken slab boundary. Keep original source/scale/scope.' if slug=='spriggina' else 'Remove repeated diagonal material pattern and smooth unnatural ridge. Actual geometry uses unequal angular mountain peaks, coarser nonuniform bedrock facets and broad shallow continuous apron. No source/scope/scale change.'
 (b/'repair-freeze.json').write_text(json.dumps(dict(created_at=now(),revision='r002',original_revision='r001',original_generator_sha256=H(a/'generator.py'),reason=fix,original_brief_sha256=H(a/'brief.json'),original_references_sha256=H(a/'references.json'),repair_authored=False),indent=2)+'\n')
 t=(a/'generator.py').read_text()
 if slug=='spriggina':
  t=t.replace(".025*math.sin(8*v+1)*edgeu**4", ".055*math.sin(18*v+1)*edgeu**4+.025*math.cos(31*v)*edgeu**6")
  t=t.replace(".018*math.sin(11*u)*edgev**4", ".045*math.sin(19*u)*edgev**4")
  t=t.replace('z-=.00085*inside','z-=.00155*inside').replace('z-=.00036*groove','z-=.00048*groove').replace("z+=.00042*math.exp(-(x/.00045)**2)","z+=.0010*math.exp(-(x/.00070)**2)")
  t=t.replace("return 'impression' if z<.00475 else 'sandstone'", "return 'impression' if z<.00445 else 'sandstone'")
 else:
  t=t.replace("jag=.68+.23*math.sin(3*x/100+1)**2+.18*math.sin(x/15)**2", "jag=.50+.30*(1-abs(math.sin(x/25+.3)))+.36*(1-abs(math.sin(x/16+1.2)))")
  t=t.replace("z=apron-g*(math.sin(math.pi*v)**.7)+.20*math.sin(x*.11+y*.04)","z=apron-g*(math.sin(math.pi*v)**.7)+(.30 if v<.73 else 1.7)*math.sin(x*.13+y*.17)")
  t=t.replace("'weathered' if (i+j*3)%17<3 else 'bedrock'", "'weathered' if rng.random()<.08 else 'bedrock'")
  t=t.replace("58,52,p,mat", "38,36,p,mat")
 (b/'generator.py').write_text(t)
print('Repair freezes preceded changed generator authoring',now())
