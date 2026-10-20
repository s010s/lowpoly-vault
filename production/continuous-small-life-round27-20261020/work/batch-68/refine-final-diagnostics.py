from pathlib import Path
import json,hashlib,datetime,shutil
R=Path.cwd();W=R/'production/continuous-small-life-round27-20261020/work/batch-68';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for slug in ['lava-dome','ice-wedge-polygon-ground']:
 b=R/'assets/candidates/continuous-small-life-round27-20261020/batch-68'/slug/'r001';a=b/'attempts/02-full-diagnostic-retained';a.mkdir(parents=True)
 plan={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_freeze_sha256':H(b/'modeling-freeze.json'),'original_brief_sha256':H(b/'brief.json'),'reason':'All eight actual512px views personally inspected; dome has mechanical band of blocks and overly smooth radial rind' if slug=='lava-dome' else 'All eight actual512px views personally inspected; crisp polygon shoulders still read as decorative tiling rather than hummocky terrain','scope_preserved':True,'bounded_design_realization_change':'Decouple exposed rind heights from angle, use irregular fractured angular blocks and nonaligned radial structure. Preserve bulbous craterless dome and frozen scale/palette.' if slug=='lava-dome' else 'Replace sharp cell prism rings with a single welded triangulated Voronoi-distance terrain heightfield. Preserve same irregular low-centered polygon subtype,45x40m soil module3m base plus0.7m raised hummocky shoulders and narrow connected grooves. Original implementation description retained, derived repair is explicit.','approval':False}
 (b/'diagnostic-repair-freeze.json').write_text(json.dumps(plan,indent=2)+'\n')
 for n in ['generator.py','model.glb','source.blend','metrics.json','source-metrics.json','source-final.report.json','source-vertex-counts.json','candidate-brief.json','build-dependencies.json','gltf-validator.report.json','runtime-parse.report.json','repro-final-1.report.json','repro-final-2.report.json','proof-final','proof-quick','preview.png','preproof-binding-check.json']:
  if (b/n).exists():shutil.move(b/n,a/n)
 s=(a/'generator.py').read_text()
 if slug=='lava-dome':
  s=s.replace("ir=1+.075*math.sin(i*2.3)+.055*math.cos(i*.72+j*.61);z=45*h*(1+.025*math.sin(i*.8))", "ir=1+.09*math.sin(i*2.3+j*1.1)+.075*math.cos(i*.72+j*1.57);z=45*h*(1+.04*math.sin(i*.8+j*1.6))")
  s=s.replace("a=j*2.399963;h=.15+.70*((j*.618)%1);rad=1", "a=j*2.399963+rng.uniform(-.2,.2);h=rng.uniform(.18,.92);rad=1")
  s=s.replace("rad*.99*math.cos(a)","rad*1.055*math.cos(a)").replace("rad*.99*math.sin(a)","rad*1.055*math.sin(a)")
  s=s.replace("for level in [0,1]:", "for level in [0,1]:").replace("rr=1+.12*math.sin(i*2.9+a)","rr=1+.24*math.sin(i*2.9+a+level*1.3)").replace("+(1.1 if level else 0)","+(s[0]*.23*math.sin(a) if level else 0)")
  s=s.replace("for j in range(44):", "for j in range(74):")
 else:
  start=s.index('def ice_ground():');end=s.index("\n{'thaumaptilon':",start)
  s=s[:start]+'''def ice_ground():
 seeds=[(-20,-16),(-3,-17),(17,-14),(-18,-1),(2,-5),(21,4),(-20,14),(-5,14),(9,11),(20,19)]
 nx=64;ny=56;vs=[];fs=[];mats=[];distances=[]
 for j in range(ny+1):
  y=-20+40*j/ny
  for i in range(nx+1):
   x=-22.5+45*i/nx
   # Low-frequency distortion of the contraction network gives natural nonstraight margins.
   xx=x+.72*math.sin(y*.24)+.25*math.sin(x*.4+y*.31);yy=y+.64*math.sin(x*.21)-.22*math.cos(y*.37-x*.16)
   ds=sorted(math.hypot(xx-a,yy-b) for a,b in seeds);edge=(ds[1]-ds[0])*.5
   ridge=math.exp(-((edge-.72)/.57)**2)
   h=3.02+.65*ridge+.035*math.sin(x*.9+y*.76)*ridge+.015*math.sin(x*.25-y*.24)
   # Narrow depressed contraction groove is still above or near low-center elevation.
   vs.append((x,y,h));distances.append(edge)
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;b=a+nx+1;faces=[(a,a+1,b+1),(a,b+1,b)] if (i+j)%2==0 else [(a,a+1,b),(a+1,b+1,b)]
   for f in faces:
    fs.append(f);e=sum(distances[k] for k in f)/3;mats.append('groove' if e<.27 else 'rim' if e<1.30 else 'center')
 perimeter=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 base=len(vs)
 for k in perimeter:x,y,z=vs[k];vs.append((x,y,0))
 for i,a in enumerate(perimeter):q=(i+1)%len(perimeter);fs.append((a,perimeter[q],base+q,base+i));mats.append('soil')
 fs.append(tuple(base+i for i in range(len(perimeter))));mats.append('soil')
 obj=mesh_object('single_welded_hummocky_low_centered_polygon_heightfield',vs,fs,[m[k] for k in cfg['palette']],col);keys=list(cfg['palette'])
 for p,k in zip(obj.data.polygons,mats):p.material_index=keys.index(k)
''' +s[end:]
 (b/'generator.py').write_text(s);d=json.loads((a/'build-dependencies.json').read_text());d['generator_sha256']=H(b/'generator.py');(b/'build-dependencies.json').write_text(json.dumps(d,indent=2)+'\n')
sel=json.loads((W/'final-selection.json').read_text());(W/'all-four-selection.json').write_text(json.dumps(sel,indent=2)+'\n');(W/'final-selection.json').write_text(json.dumps([x for x in sel if x['asset_id'] in ['lava-dome','ice-wedge-polygon-ground']],indent=2)+'\n')
s=(W/'run-lifecycle.py').read_text().replace("W/'rebuild-runs'", "W/'rebuild-runs-diagnostic-repair'")
(W/'run-lifecycle-diagnostic-repair.py').write_text(s)
