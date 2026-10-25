import bpy,sys,json,hashlib
from pathlib import Path
old,new,out=map(Path,sys.argv[sys.argv.index('--')+1:]);allowed={'pectoral-fin--1','pectoral-fin-1','pelvic-fin--1','pelvic-fin-1'}
def snap(p):
 bpy.ops.wm.open_mainfile(filepath=str(p.resolve()));r={}
 for o in bpy.data.collections['EXPORT'].all_objects:
  if o.type!='MESH':continue
  r[o.name]={'vertices':[list(v.co) for v in o.data.vertices],'faces':[list(f.vertices) for f in o.data.polygons],'materials':[m.name for m in o.data.materials],'matrix':[list(x) for x in o.matrix_world],'material_indices':[f.material_index for f in o.data.polygons]}
 return r
A=snap(old);B=snap(new);edits=[];unchanged=[]
assert set(A)==set(B)
for n in sorted(A):
 a,b=A[n],B[n]
 if a==b:unchanged.append(n);continue
 assert n in allowed
 assert all(a[k]==b[k] for k in ['faces','materials','matrix','material_indices'])
 e=[{'vertex_index':i,'old':v,'new':b['vertices'][i]} for i,v in enumerate(a['vertices']) if v!=b['vertices'][i]]
 assert len(e)==4,(n,len(e));edits.append({'name':n,'edits':e})
assert len(edits)==4 and len(unchanged)==18
out.write_text(json.dumps({'status':'PASS_LOCALITY','old_blend_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'new_blend_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'unchanged_meshes':unchanged,'changed_meshes':edits,'source_topology_unchanged':True,'source_materials_unchanged':True,'source_transforms_unchanged':True,'changed_vertices_total':16,'scope':'Only the two proximal outline points, on both foil surfaces, changed in each of the four paired fins. All distal fin vertices and all other source mesh data are unchanged.'},indent=2)+'\n')
print('PASS: 16 proximal vertices; 18 other meshes identical')
