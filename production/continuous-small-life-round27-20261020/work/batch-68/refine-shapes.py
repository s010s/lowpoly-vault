from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round27-20261020/work/batch-68';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for slug in ['lava-dome','ice-wedge-polygon-ground']:
 b=R/'assets/candidates/continuous-small-life-round27-20261020/batch-68'/slug/'r001';a=b/'attempts/01-quick-shape';a.mkdir(parents=True)
 (b/'visual-refinement-plan.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_freeze_sha256':H(b/'modeling-freeze.json'),'reason':'Quick maker pixels show dome rind too hidden and slopes too conical' if slug=='lava-dome' else 'Quick maker pixels show overly even polygon spacing and narrow angular rim geometry','bounded_change':'Expose angular blocks on dome shoulders and widen high shoulder mass without crater; preserve frozen scale/scope/palette' if slug=='lava-dome' else 'Use more unequal irregular cell positions and wider hummocky elevated shoulders, same low-centered3.7m soil module/scope/palette','approval':False},indent=2)+'\n')
 for n in ['generator.py','model.glb','source.blend','metrics.json','source-metrics.json','build-dependencies.json','proof-quick']:
  if (b/n).exists():shutil.move(b/n,a/n)
 s=(a/'generator.py').read_text()
 if slug=='lava-dome':
  s=s.replace("(.23,.85),(.51,.75),(.77,.56),(.95,.34),(1,.13)","(.23,.88),(.51,.80),(.77,.68),(.95,.48),(1,.25)")
  s=s.replace("a=j*2.399963;h=.15+.68*((j*.618)%1);rad=(1-h**1.8)**.6", "a=j*2.399963;h=.15+.70*((j*.618)%1);rad=1\n  for (za,ra),(zb,rb) in zip(levels,levels[1:]):\n   if za<=h<=zb:rad=ra+(rb-ra)*(h-za)/(zb-za);break")
  s=s.replace("60*rad*.83*math.cos(a),50*rad*.83*math.sin(a)","60*rad*.99*math.cos(a),50*rad*.99*math.sin(a)")
  s=s.replace("(rng.uniform(4,8),rng.uniform(4,7),rng.uniform(6,13))", "(rng.uniform(5,9),rng.uniform(5,8),rng.uniform(7,14))")
 else:
  s=s.replace("seeds=[(-18,-13),(-5,-15),(10,-13),(20,-9),(-17,0),(-2,-1),(13,2),(-13,15),(1,14),(18,16)]", "seeds=[(-20,-16),(-3,-17),(17,-14),(-18,-1),(2,-5),(21,4),(-20,14),(-5,14),(9,11),(20,19)]")
  s=s.replace("for t in [1,.94,.82,.55]", "for t in [1,.92,.72,.48]").replace("if t==.94", "if t==.92").replace("if t==.82", "if t==.72")
 (b/'generator.py').write_text(s);d=json.loads((a/'build-dependencies.json').read_text());d['generator_sha256']=H(b/'generator.py');(b/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
