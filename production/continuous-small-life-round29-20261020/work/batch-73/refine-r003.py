from pathlib import Path
import json,hashlib,shutil,datetime
R=Path.cwd();W=R/'production/continuous-small-life-round29-20261020/work/batch-73';p=W/'generator.py';t=p.read_text();t=t.replace('r002 implementation repairs authored after15:07:20Z repair freezes; r001 retained.','r003 targeted geology implementation after15:11:12Z freezes; previous attempts retained.')
t=t.replace("grooves=[(-3.20,.075,.10),(-2.72,.19,.23),(-1.88,.12,.16),(-1.08,.25,.29),(-.28,.10,.12),(.54,.16,.21),(1.43,.23,.26),(2.31,.10,.15),(3.08,.15,.19)]", "grooves=[(-3.45,.045,.07),(-3.18,.055,.10),(-2.65,.21,.26),(-.95,.055,.09),(-.74,.045,.06),(.48,.26,.29),(1.85,.05,.08),(2.04,.055,.11),(3.28,.16,.22)]")
t=t.replace("(.19*math.sin(y*1.7)+.10*math.cos(y*3.1))", "(.30*math.sin(y*1.7)+.16*math.cos(y*3.1))")
t=t.replace("rib*=.7+.3*math.sin(t*3+j*.31)**2", "rib*=.30+.70*math.sin(t*3+j*.31)**4\n    erosion+=.012*math.sin(t*8+h*5)+.007*math.sin(t*13-h*7)\n    for tt,depth in [(1.2,.012),(2.7,.019),(4.45,.014),(5.8,.011)]:\n     erosion-=depth*math.exp(-((t-tt-.09*math.sin(h*8))/.065)**2)*math.sin(math.pi*h)**.5")
p.write_text(t)
for x in json.loads((W/'final-selection.json').read_text()):
 if x['revision']!='r003':continue
 b=R/x['path'];shutil.copy(p,b/'generator.py');files=[b/'generator.py',b/'build-config.json',R/'scripts/asset_common.py',R/'scripts/qa_glb.py'];(b/'build-dependencies.json').write_text(json.dumps({'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seed':73,'blender':'4.3.2','three':'0.180.0','files':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}},indent=2)+'\n')
print('r003 closure fixed')
