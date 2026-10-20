from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/small-life-batch77';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
notes={
'ernietta':'r001 all8 pixels personally inspected15:58:51Z: cavity and compressed outline visible but palisade too shallow and base too point-rounded. r002 strengthen actual integral rib relief and elongate basal seam, preserving original incomplete fossil scope.',
'loess-bluff':'r001 all8 personally inspected15:59:40Z: steep joints visible but side/back reads like regular cut bread slice, poor natural geological appearance. r002 taper ends, lower rear to a sloped irregular footprint, add coherent natural face breaks and stronger irregular gullied crest, no new scope.',
'rock-glacier':'r001 all8 personally inspected15:59:40Z: lobate angular tongue visible but arcuate ridges too subtle beneath uniformly domed surface. r002 strengthen three unequal arcuate ridge zones and reduce dome, retain connected unstructured rubble surface, no belts.',
'slump-folded-bed':'r001 all8 personally inspected16:00:08Z: contorted middle and bounding beds identifiable, but cuboid cut edges and almost planar roof look artificial. r002 irregular narrowing weathered ends/top and coherent differential erosion, unchanged bounded soft-sediment scope.'}
for slug,note in notes.items():
 old=W/'assets'/slug/'r001';b=old.parent/'r002';b.mkdir()
 for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json','premodel-schema-check.json','modeling-freeze.json','build-dependencies.json']:
  shutil.copyfile(old/n,b/n)
 (old/'maker-attempt-observation.json').write_text(json.dumps({'observed_at':now(),'glb_sha256':H(old/'model.glb'),'status':'needs_revision_not_final','notes':note,'prior_proof_retained':True},indent=2)+'\n')
 d={'asset_id':slug,'revision':'r002','original_modeling_freeze_sha256':H(old/'modeling-freeze.json'),'repair_frozen_at':now(),'scope_unchanged':True,'reason_and_geometry_plan':note,'original_brief_config_reference_files_byte_unchanged':True,'generator_changed_next':True}
 (b/'repair-freeze.json').write_text(json.dumps(d,indent=2)+'\n')
 s=(old/'generator.py').read_text()
 if slug=='ernietta':
  s=s.replace('(.027 if j<8 else .014)','(.073 if j<8 else .026)')
  s=s.replace('x=.04*rr*math.cos(t)*(1+.018*math.sin(5*t));y=.025*rr*math.sin(t)*(1+.025*math.cos(3*t))','x=.04*rr*math.cos(t)*(1+.018*math.sin(5*t));y=.025*rr*math.sin(t)*(1+.025*math.cos(3*t))\n   if j==0:x=.030*math.cos(t);y=.00065*math.sin(t)+.00025*math.sin(30*t)\n   if j==1:x=.032*math.cos(t);y=.006*math.sin(t)+.0004*math.sin(30*t)\n   if j==2:x=.035*math.cos(t)*(1+.025*rib);y=.015*math.sin(t)*(1+.04*rib)')
 elif slug=='loess-bluff':
  s=s.replace('(1.1,7.35),(2.1,6.45),(3.5,4.65)','(1.1,5.4),(2.1,2.2),(3.5,.16)')
  s=s.replace('crest=.35*math.sin(.53*x+1)+.22*math.sin(1.3*x-.4)-.45*g','crest=.62*math.sin(.53*x+1)+.37*math.sin(1.3*x-.4)+.18*math.sin(2.2*x+1.3)-.80*g')
  s=s.replace('yy=y+(g*(.8 if 3<j<9 else .3) if front else .1*math.sin(x*.7+j))','yy=y+(g*(1.05 if 3<j<9 else .3) if front else .1*math.sin(x*.7+j))\n   yy+=.16*math.sin(x*1.7+.3)+.08*math.sin(x*3.8+j*.4)')
  s=s.replace('xx=x+.035*math.sin(j*1.6+i*.7)*edge','endshape=.18+.82*(math.sin(math.pi*i/nx)**.30)\n   zz*=endshape\n   xx=x+.065*math.sin(j*1.6+i*.7)*edge')
 elif slug=='rock-glacier':
  s=s.replace('z=.45+3.5*shore**.38+1.6*(v+1)/2*shore**.2','z=1.0+1.45*shore**.24+.75*(v+1)/2*shore**.2')
  s=s.replace('(-13,1.7,.60,.2),(-4,1.1,.85,1.4),(5,1.9,.55,2.1),(13,1.4,.42,.8)','(-13,2.2,2.05,.2),(-4,1.9,2.65,1.4),(6,2.1,1.80,2.1),(14,1.7,1.25,.8)')
  s=s.replace('(rng.random()-.45)*.60','(rng.random()-.45)*.44')
 else:
  s=s.replace('xx=x+.12*amp*math.sin(phase+.6)+.04*math.sin(i*.91+h)*abs(x/4)**6','xx=x*(1-.055*h/4)+.12*amp*math.sin(phase+.6)+.14*math.sin(i*.43+h*2.3)*abs(x/4)**6')
  s=s.replace('erosion=.022*math.sin(j*1.13)+.015*math.sin(i*1.7+j*.7)','erosion=.055*math.sin(j*1.13)+.020*math.sin(i*.71+j*.7)')
  s=s.replace('yy=y+math.copysign(erosion,y)+.035*math.sin(x*2.7+j*.5)','yy=y*(1-.06*h/4)+math.copysign(erosion,y)+.075*math.sin(x*2.7+.5)+.03*math.sin(x*4.5)')
  s=s.replace('z=h+amp*fold+.035*math.sin(x*.9+y)*max(0,(h-3.3)/.7)','z=h+amp*fold+(.14*math.sin(x*2.3+y*.8)+.08*math.sin(x*4.2+.3))*max(0,(h-3.02)/.98)')
  s=s.replace("o=(len(records)-1)*n;fs.append(tuple(o+i for i in range(n)));ms.append('earth')","o=(len(records)-1)*n;cap=len(vs);vs.append((0,0,4.05))\n for i in range(n):fs.append((cap,o+i,o+(i+1)%n));ms.append('earth')")
 (b/'generator.py').write_text(s)
# Preserve original final-selection input, replace only derived current selection.
shutil.copyfile(W/'final-selection.json',W/'initial-selection-r001.json')
f=json.loads((W/'final-selection.json').read_text())
for x in f:x['revision']='r002';x['path']=x['path'].replace('/r001','/r002')
(W/'final-selection.json').write_text(json.dumps(f,indent=2)+'\n')
