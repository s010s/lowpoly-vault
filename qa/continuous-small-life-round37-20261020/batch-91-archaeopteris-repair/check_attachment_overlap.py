import pathlib,runpy,json,datetime,numpy as np
O=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-independent-qa-20261021')
# Load reviewed definitions without executing/replacing successful geometry report.
s=(O/'audit_geometry-v2.py').read_text();cut=s.index('summary={k:');ns={};exec(s[:cut],ns)
winding=ns['winding'];v=ns['v'];comps=ns['comps'];by={c['first']:c for c in comps};supp=[]
for entry in ns['attachment_fails']:
 c=by[entry['first']];hosts=ns['limbs'] if entry['kind']=='spray_to_limb' else [ns['trunk']];rows=[]
 for host in hosts:
  ws=[winding(v[i],host) for i in c['ids']];inside=[i for i,w in zip(c['ids'],ws) if abs(w-1)<1e-5]
  if inside:rows.append({'host_first':host['first'],'inside_vertex_ids':inside,'max_winding':max(ws)})
 supp.append({'base_center_test':entry,'component_has_vertices_inside_actual_host_volume':bool(rows),'overlaps':rows})
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'A base center outside an intersecting host is not a disconnected component. For each such case inspect actual vertices within actual host closed geometry. No universal full-base-center containment rule is imposed.','cases':supp,'all_actual_attachments_have_geometric_overlap':all(x['component_has_vertices_inside_actual_host_volume'] for x in supp)}
(O/'attachment-overlap.report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
g=json.load(open(O/'geometry.report.json'))
for i,x in enumerate(g['leaves']):
 if not x['nominal_within_single_storage_interval']:print('OUTLIER_INDEX',i,'i/k/j/sign',i//48,(i%48)//12,(i%12)//2,-1 if i%2==0 else 1)
