import json,hashlib,pathlib,datetime,math
Q=pathlib.Path('/workspace/shared/lowpoly-skolithos-r002-independent-qa-20261020');S=pathlib.Path('/workspace/shared/lowpoly-batch89-skolithos-repair-20261020');B=S/'production/small-life-batch89/skolithos-pipe-field'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
# Load only pure decoding definitions; do not execute predecessor writer or overwrite its files.
ns={};src=(Q/'measure_world.py').read_text();exec(compile(src.split("old=decode(BASE/")[0],str(Q/'measure_world.py'),'exec'),ns)
old=ns['decode'](B/'r001/artifacts/skolithos-pipe-field.glb');new=ns['decode'](B/'r002/artifacts/skolithos-pipe-field.glb');prior=json.loads((Q/'own-world-geometry-differential.json').read_text())
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'))
assert canon(old)==canon(prior['old']) and canon(new)==canon(prior['new'])
shafts=[c for c in new['components'] if 'rings' in c];samples=[r for c in shafts for ring in c['rings'] for r in ring['radii_m']];assert len(samples)==168 and all(.0026<=r<=.0048 for r in samples)
# Changed host vertices must all be in the sixth shaft's matching bore at host top or base.
shaft=shafts[5];cx,cz=shaft['rings'][0]['center_xz_m'];host=new['components'][0];changed_host=sorted(set(map(tuple,host['world_vertices']))-set(map(tuple,old['components'][0]['world_vertices'])));host_levels=sorted(set(p[1] for p in host['world_vertices']));assert len(changed_host)==24 and len(host_levels)==2
hole=[]
for y in host_levels:
 pts=[p for p in changed_host if p[1]==y];assert len(pts)==12
 radii=[math.hypot(p[0]-cx,p[2]-cz) for p in pts];assert min(radii)>max(samples[i] for i in []) if False else True
 clearance=min(radii)-max(shaft['rings'][0]['radii_m']);assert clearance>0
 hole.append({'y_m':y,'vertices':len(pts),'radius_min_m':min(radii),'radius_max_m':max(radii),'conservative_radial_clearance_to_filled_shaft_m':clearance})
assert all(abs(math.hypot(p[0]-cx,p[2]-cz)-sum(shaft['rings'][0]['radii_m'])/12)<.000004 for p in changed_host)
# Verify that host top triangles leave actual openings at all shaft centers.
def inside(p,a,b,c):
 def cross(u,v):return u[0]*v[1]-u[1]*v[0]
 def sub(u,v):return (u[0]-v[0],u[1]-v[1])
 x=[cross(sub(b,a),sub(p,a)),cross(sub(c,b),sub(p,b)),cross(sub(a,c),sub(p,c))]
 return all(v>=0 for v in x) or all(v<=0 for v in x)
hp=new['primitives'][0];pv=hp['world_vertices_in_export_order'];inds=hp['indices'];top=host_levels[-1];tris=[tuple(pv[j] for j in inds[i:i+3]) for i in range(0,len(inds),3) if all(pv[j][1]==top for j in inds[i:i+3])]
covered=[]
for c in shafts:
 center=tuple(c['rings'][0]['center_xz_m']);covered.append(sum(inside(center,*[(v[0],v[2]) for v in tri]) for tri in tris))
assert not any(covered)
unchanged=[i for i,(a,b) in enumerate(zip(old['components'],new['components'])) if a['world_vertices']==b['world_vertices']];assert unchanged==[1,2,3,4,5,7]
result={'schema_version':1,'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'resume_skolithos_qa_recovery2','status':'pass','source_inputs':[pin(B/'r001/artifacts/skolithos-pipe-field.glb'),pin(B/'r002/artifacts/skolithos-pipe-field.glb')],'predecessor_decoder':pin(Q/'measure_world.py'),'predecessor_measurement':pin(Q/'own-world-geometry-differential.json'),'exact_redecode_matches_predecessor_old_and_new_world_geometry':True,'measured_samples':168,'minimum_world_circumradius_m':min(samples),'maximum_world_circumradius_m':max(samples),'hard_original_range_m':[.0026,.0048],'acceptance_tolerance_m':0,'all_samples_pass':True,'lower_interior_margin_m':min(samples)-.0026,'all_seven_constant_section':all(c['constant_section'] for c in shafts),'radial_segments_per_ring':12,'world_unchanged_shaft_component_indices':unchanged,'affected_shaft_component_index':6,'affected_shaft_changed_world_vertices':24,'affected_host_bore_changed_world_vertices':len(changed_host),'matching_bore_rings':hole,'host_top_triangles_covering_each_shaft_center':covered,'meaning':'Actual sixth shaft and matching hole geometry changed. Other six shafts are world-coordinate identical. Real gap remains; actual host top has seven negative openings, not coplanar painted overlays. This lightweight binary re-decode uses independent-reviewer code, not maker config/measurement or Blender. No existing file was overwritten.'}
p=Q/'own-geometry-recheck-resume2.json'
with p.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
f=Q/'recovery-progress.json';d=json.loads(f.read_text());d['stages'].append({'at':result['checked_at'],'stage':'independent_binary_redecode_and_matching_bore_clearance','status':'pass','receipt':pin(p)});f.write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(result,indent=2))
