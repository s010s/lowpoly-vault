from pathlib import Path
import shutil,json,hashlib,datetime
b=Path('assets/candidates/continuous-small-life-round27-20261020/batch-68/lava-dome/r002');a=b/'attempts/01-regular-fracture-diagnostic';a.mkdir(parents=True)
(b/'quick-refinement-plan.json').write_text(json.dumps({'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Personally inspected quick hero/top: no block belt and summit covered, but fracture cells too uniformly low/flat.','bounded_change':'Vary local plate lift, tilt, edge shoulder width and partial breakage across surface; mixed large/small fracture regions and uneven summit height. Preserve continuous joined dome, scope, source, materials, dimensions role and locked renderer.'},indent=2)+'\n')
for n in ['generator.py','model.glb','source.blend','source-metrics.json','metrics.json','proof-quick','build.log','quick.log','build-dependencies.json']:
 if (b/n).exists():shutil.move(b/n,a/n)
s=(a/'generator.py').read_text().replace('while len(seeds)<96:', 'while len(seeds)<72:').replace(')>.12 for x,y in seeds', ')>.13 for x,y in seeds')
s=s.replace('return 43*math.sqrt', 'return 40*math.sqrt')
s=s.replace("lifts=[0,rng.uniform(.7,2.2),rng.uniform(.4,2.0)];rings=[]", "lift=rng.uniform(.5,5.5);lifts=[0,lift,rng.uniform(.3,5.2)];rings=[];inner=rng.uniform(.58,.82);shoulder=rng.uniform(.88,.97);tiltx=rng.uniform(-12,12);tilty=rng.uniform(-12,12)")
s=s.replace('enumerate([1,.90,.64])', 'enumerate([1,shoulder,inner])')
s=s.replace("z=h+lifts[j]*(.75+.25*math.sin(k*1.1+x*11-y*9))", "z=h+lifts[j]*(.72+.28*math.sin(k*1.1+x*11-y*9))+(xx-cx)*tiltx+(yy-cy)*tilty")
s=s.replace("height(cx,cy)+rng.uniform(.1,1.9)","height(cx,cy)+rng.uniform(.5,5.5)")
(b/'generator.py').write_text(s);d=json.loads((a/'build-dependencies.json').read_text());d['generator_sha256']=hashlib.sha256((b/'generator.py').read_bytes()).hexdigest();(b/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
