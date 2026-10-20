import bpy,sys,json,hashlib,datetime,os
from pathlib import Path
old,new,out,aid=map(str,sys.argv[sys.argv.index('--')+1:]);sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();before=[sha(old),sha(new)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(p):
 bpy.ops.wm.open_mainfile(filepath=p,load_ui=False,use_scripts=False);bpy.context.view_layer.update();d={}
 for o in bpy.data.collections['EXPORT'].all_objects:
  if o.type=='MESH':d[o.name]={'vertices':[list(v.co) for v in o.data.vertices],'polygons':[list(p.vertices) for p in o.data.polygons],'materials':[p.material_index for p in o.data.polygons],'material_names':[m.name for m in o.data.materials],'matrix':[list(x) for x in o.matrix_world]}
 return d
A=read(old);B=read(new);assert A.keys()==B.keys();report={'asset_id':aid,'started_at':start,'old_sha256':before[0],'new_sha256':before[1],'pid':os.getpid(),'parts':[]};issues=[]
for n,a in A.items():
 b=B[n];assert len(a['vertices'])==len(b['vertices']);changed=[i for i,(v,w) in enumerate(zip(a['vertices'],b['vertices'])) if v!=w];xy=all(v[:2]==w[:2] for v,w in zip(a['vertices'],b['vertices']));other=all(a[k]==b[k] for k in ['polygons','materials','material_names','matrix']);rec={'name':n,'vertices':len(a['vertices']),'changed_vertex_indices':changed,'xy_identical':xy,'topology_materials_transform_identical':other,'old_max_z':max(v[2] for v in a['vertices']),'new_max_z':max(v[2] for v in b['vertices'])}
 if not xy or not other:issues.append(n+' unplanned planar/topology/material/transform change')
 if aid=='piedmont-glacier':
  if n!='east-mountain-shoulder' and changed:issues.append(n+' unexpected change')
  if n=='east-mountain-shoulder':
   rec['max_expected_scaling_error']=max(abs(w[2]-(52+(v[2]-52)*.98 if v[2]>52 else v[2])) for v,w in zip(a['vertices'],b['vertices']));assert rec['max_expected_scaling_error']<.0001
 if aid=='lava-channel':
  expected=[i*13+9 for i in range(33)];rec['changed_exactly_33_right_crest_column9']=changed==expected;rec['delta_range']=[min(b['vertices'][i][2]-a['vertices'][i][2] for i in changed),max(b['vertices'][i][2]-a['vertices'][i][2] for i in changed)];assert changed==expected
 if aid=='karst-polje':
  rec['changed_exactly_upper_rings4_5']=changed==list(range(225,337));rec['floor_169_vertices_unchanged']=a['vertices'][:169]==b['vertices'][:169];assert changed==list(range(225,337));assert rec['floor_169_vertices_unchanged']
 report['parts'].append(rec)
report.update({'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_files_unchanged':before==[sha(old),sha(new)],'issues':issues,'status':'pass' if not issues else 'fail'});Path(out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not issues
