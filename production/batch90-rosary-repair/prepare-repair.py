from pathlib import Path
import json,shutil,hashlib,datetime
R=Path(__file__).resolve().parents[2];P=Path(__file__).parent;S=Path('/workspace/shared/lowpoly-batch90-20261020/production/batch90');aid='rosary-shaped-chambered-burrow-hormosiroidea-type';O=S/'assets'/aid/'r001';B=P/'assets'/aid/'r002';B.mkdir(parents=True);F=P/'original-freeze';F.mkdir();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
for name in ['brief.json','references.json','build-config.json','modeling-freeze.json']:
 shutil.copyfile(O/name,F/name)
for name in ['brief.json','references.json','concept-original.png','concept-prompt.txt','concept-generation.json','LICENSES.md']:
 shutil.copyfile(O/name,B/name)
for name in ['render-fixed8.py','measure-geometry.py','runtime-parse.mjs','concept-evidence.template.json']:
 shutil.copyfile(S/name,P/name)
Q=Path('/workspace/shared/lowpoly-batch90-independent-qa-20261020');audit=[Q/'independent-review.json',Q/aid/'chamber-tail-exact-triangle-evidence.json']
record=dict(kind='append-only implementation decision before revised generator authoring',revision='r002',asset_id=aid,host_observed_at=now(),tool_clock_observed='2026-10-20T23:54:58Z',time_note='Host process timestamps and tool clock are distinct clocks; no mtime chronology inferred.',original_maker_commit='625b5f2cdd97623e216874fd981958852a3a910d',lean_parent='ee1eaa334f5e56a2716f30edb125e01cf193da6f',original_files={str(p):H(p) for p in [O/'generator.py',O/'model.glb',O/'source.blend',*[F/n for n in ['brief.json','references.json','build-config.json','modeling-freeze.json']],*audit]},scope='Only rosary-shaped-chambered-burrow-hormosiroidea-type r002. Original batch90, all failed evidence and other three assets read-only.',cause='Unconstrained triangulation bridges positive chamber samples through and beyond the base; floating radial evaluation also raises nominal ring points.',implementation='Use actual constrained inscribed 32-sided chamber base loops, replace ambiguous ring samples by exact neck-only boundary heights, and prohibit positive chamber vertices from joining exterior triangles. The 20nm inward construction guard is geometry inside the unchanged frozen range, not a pass tolerance. Preserve chamber centers/heights, S path, neck function, slab and renderer. Precise exported-triangle verification before final full proof. No new concept or factual scope.',inspected_pixels={'PRI76855':{'path':'/workspace/shared/lowpoly-batch90-evidence/reference-pixels/hormosiroidea.jpg','sha256':H(Path('/workspace/shared/lowpoly-batch90-evidence/reference-pixels/hormosiroidea.jpg')),'observation':'Shallow serial rounded chambers on irregular slab; quiet host and thin connectors, not isolated balls.'},'original_concept':{'sha256':H(B/'concept-original.png'),'observation':'All four panels inspected. Original rejection of giant ball height and noisy host retained.'}},source_text_review={'PRI-FEEDING':'First-party page re-read: PRI76855 Devonian Ludlowville, Tompkins County, approximate 10cm slab. Consult-only.', 'CAMBRIDGE':'Original description and remarks re-read: consecutive nodes, unbranched sinuous horizontal trace; subspherical versus heart-shaped and unresolved nomenclature. No maker species asserted.'})
(P/'implementation-record-v001.json').write_text(json.dumps(record,indent=2)+'\n')
cfg=json.loads((F/'build-config.json').read_text());cfg['revision']='r002';cfg['repair_record']='../../../implementation-record-v001.json';cfg['modeling_decisions']+=' Repair r002 constrains true chamber support inside the original radius range, without changing frozen design or acceptance criteria.';(B/'build-config.json').write_text(json.dumps(cfg,indent=2)+'\n')
s=(O/'generator.py').read_text();s=s.replace("poly=poly_outline(W,D);points=list(poly);segments=[]","poly=poly_outline(W,D);points=list(poly);segments=[];constraints=[];boundary_input=set();support_polygons=[]")
a=s.index(' if beads:\n  for q,br,bh in beads:');b=s.index(' for j in range(15):',a)
s=s[:a]+''' if beads:
  for q,br,bh in beads:
   points.append(q)
   for frac in [.35,.70,1.25]:
    for j in range(16):points.append((q[0]+br*frac*math.cos(math.tau*j/16),q[1]+br*frac*math.sin(math.tau*j/16)))
'''+s[b:]
a=s.index(' # Delaunay heightfield');b=s.index(' def height(q):',a)
s=s[:a]+''' # The chamber base loops are actual constrained topology, not merely labels.
 if beads:
  for q,br,bh in beads:
   support_polygons.append([(q[0]+(br-2e-8)*math.cos(math.tau*j/32),q[1]+(br-2e-8)*math.sin(math.tau*j/32)) for j in range(32)])
  def edge_distance(q,a,b):
   x,y=q;ax,ay=a;dx,dy=b[0]-ax,b[1]-ay;t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy)))
   return math.hypot(x-ax-t*dx,y-ay-t*dy)
  # Prevent merge epsilon from displacing or collapsing a support boundary.
  points=[q for q in points if all(edge_distance(q,a,ring[(j+1)%32])>3e-5 for ring in support_polygons for j,a in enumerate(ring))]
  for ring in support_polygons:
   ids=list(range(len(points),len(points)+32));points.extend(ring);boundary_input.update(ids);constraints.extend((ids[j],ids[(j+1)%32]) for j in range(32))
 vv,ee,ff,orig_v,*_=delaunay_2d_cdt([Vector(q) for q in points],constraints,[],0,.000015)
 boundary_output={i for i,orig in enumerate(orig_v) if any(j in boundary_input for j in orig)}
 def strictly_in(q,ring):
  return all((b[0]-a[0])*(q.y-a[1])-(b[1]-a[1])*(q.x-a[0])>0 for a,b in zip(ring,ring[1:]+ring[:1]))
'''+s[b:]
s=s.replace(' def height(q):',' def height(q,index):').replace('   for center,br,bh in beads:\n    dist=(q-Vector(center)).length\n    if dist<br:bump=max(bump,bh*math.sqrt(max(0,1-(dist/br)**2)))','   for (center,br,bh),ring in zip(beads,support_polygons):\n    dist=(q-Vector(center)).length\n    if index not in boundary_output and strictly_in(q,ring):bump=max(bump,bh*math.sqrt(max(0,1-(dist/br)**2)))').replace('vs=[(q.x,q.y,height(q)[0]) for q in vv]','vs=[(q.x,q.y,height(q,i)[0]) for i,q in enumerate(vv)]')
s=s.replace("semantic['chamber_count']=13","semantic['chamber_count']=13;semantic['support_repair']={'kind':'constrained inscribed32-gon with neck-only boundary heights','inward_construction_guard_m':2e-8,'support_polygon_sides':32,'not_an_acceptance_tolerance':True}")
(B/'generator.py').write_text(s)
(P/'recovery-progress.json').write_text(json.dumps({'stage':'prepared-before-first-build','at_host':now(),'asset':aid,'revision':'r002','immutable_implementation_record_sha256':H(P/'implementation-record-v001.json')},indent=2)+'\n')
print(B)
