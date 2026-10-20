# SPDX-License-Identifier: MIT
from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round23-20261020/work/batch-60';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
selection=json.loads((W/'final-selection.json').read_text())
for x in selection:
 if x['asset_id'] not in ['collinsium','yardang']:continue
 old=R/x['path'];b=old.parent/'r002';b.mkdir(exist_ok=True)
 for n in ['concept-original.png','concept-prompt.txt','concept-generation.json','references.json','brief.md']:shutil.copy(old/n,b/n)
 note={'collinsium':'Maker self-review repair: shorten posterior lobopods toabout10mm versusabout27mm filtering limbs by lowering tubular body; filtering limbs extend forward more strongly rather than all limbs standing as equal stilts. Diagnostic count and whole-organism scope unchanged.','yardang':'Maker self-review repair: replace over-smooth cone-like transverse section with actual stepped, fluted rock cross-sections, asymmetrical longitudinal ridge and broken wind-eroded ledges. Retain blunt windward nose/tapered lee tail, no dune slipface. Muted stratification, geometry rather than colors must establish erosion.'}[x['asset_id']]
 brief=json.loads((old/'brief.json').read_text());brief['brief_version']='r002';brief['repair_note']=note;brief['created_at']=now();put(b/'brief.json',brief)
 cfg=json.loads((old/'build-config.json').read_text());cfg['revision']='r002';cfg['modeling_decisions']+=' '+note;put(b/'build-config.json',cfg)
 (b/'brief.md').write_text((old/'brief.md').read_text()+'\n\n## Premodel repair freeze r002\n'+note+'\n')
 put(b/'modeling-freeze.json',{'asset_id':x['asset_id'],'revision':'r002','frozen_at':now(),'status':'Focused repair decisions frozen before editing generator or rebuilding geometry','supersedes':str(old.relative_to(R)),'files':{n:H(b/n) for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json']}})
 s=(old/'generator.py').read_text()
 if x['asset_id']=='collinsium':
  s=s.replace('z=.020+.0022*math.sin(math.pi*t)','z=.012+.0015*math.sin(math.pi*t)')
  s=s.replace('(0,-.0393,.0185)','(0,-.0393,.0105)').replace('(0,-.0435,.0166)','(0,-.0435,.0086)').replace('-.0399,.0216','-.0399,.0136')
  s=s.replace('-.0423,.0189','-.0423,.0109').replace('-.0463,.018)','-.0463,.010)').replace('-.048,.0173','-.048,.0093')
  s=s.replace('y-.001,.014','y-.005,.010').replace('y-.0055,.007','y-.014,.0055').replace('y-.012,.0014','y-.025,.0014')
  s=s.replace('y+.0003,.013','y+.0003,.008').replace('y+.0005,.005','y+.0005,.0045')
  s=s.replace('(0,.036,.0204),(0,.040,.020),(0,.044,.0192)','(0,.036,.0124),(0,.040,.012),(0,.044,.0112)')
 if x['asset_id']=='yardang':
  a=s.index('def yardang():');e=s.index('def cirque():')
  f='''def yardang():
 # Sculpted asymmetric compact sediment ridge with real eroded ledges/flutes.
 half=[(.86,0),(.98,.08),(.87,.20),(.91,.28),(.71,.35),(.80,.43),(.69,.55),(.73,.62),(.50,.72),(.56,.81),(.28,.94),(0,1.0)]
 profile=half+[(-x,z) for x,z in reversed(half[:-1])];n=len(profile);rings=[]
 for j in range(41):
  t=j/40;y=-4+8*t
  width=1.40*(.38+.62*min(1,t/.08))*(1-.97*t)**.77
  height=2.5*(.66+.34*min(1,t/.10))*(1-.99*t)**.74
  ring=[]
  for k,(px,pz) in enumerate(profile):
   # Changes are coherent along erosion direction, not independently scattered noise.
   wave=1+.050*math.sin(t*13+k*.55)+.022*math.sin(t*29+k*.7)
   x=width*px*wave+.08*math.sin(t*5)*(1-t)
   z=height*pz*(1+.05*math.sin(t*17+k*.8))
   ring.append((x,y+.08*(1-t)*abs(px)*math.sin(k*.8),max(0,z)))
  rings.append(ring)
 loft('single_wind_eroded_stepped_and_longitudinally_fluted_ridge',rings,'sandstone')
'''
  s=s[:a]+f+s[e:]
  # Quieter layers do not distract from identifying carved geometry.
  s=s.replace("poly.material_index=1 if .65<z<.84 or 1.46<z<1.64 else 2 if .38<z<.48 or 1.12<z<1.24 else 0","poly.material_index=1 if .65<z<.80 or 1.46<z<1.57 else 2 if .38<z<.44 or 1.12<z<1.18 else 0")
 (b/'generator.py').write_text(s);put(b/'authoring-start.json',{'observed_at':now(),'generator_sha256':H(b/'generator.py'),'prior_freeze':'modeling-freeze.json'})
 (old/'rejected-maker-r001.md').write_text('Not selected for independentQA. '+note+'\nOriginal files retained unchanged as maker evidence; final revisionr002.\n')
 x['revision']='r002';x['path']=str(b.relative_to(R))
put(W/'final-selection.json',selection)
