# SPDX-License-Identifier: MIT
import sys,json,hashlib,collections,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,audit_glb
old,new,out=map(Path,sys.argv[1:]);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def decode(p):
 d,b,_=read_glb(p);tris=collections.Counter();identity=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]
 def visit(i,parent):
  n=d['nodes'][i];matrix=matmul(parent,node_matrix(n))
  if 'mesh' in n:
   for pr in d['meshes'][n['mesh']]['primitives']:
    vv=[tuple(transform(matrix,v)) for v in accessor_values(d,b,pr['attributes']['POSITION'])];nn=[tuple(x) for x in accessor_values(d,b,pr['attributes']['NORMAL'])];ii=[x[0] for x in accessor_values(d,b,pr['indices'])];mat=pr.get('material')
    for j in range(0,len(ii),3):
     t=tuple((vv[k],nn[k]) for k in ii[j:j+3]);cyc=[t,t[1:]+t[:1],t[2:]+t[:2]];tris[(mat,min(cyc))]+=1
  for ch in n.get('children',[]):visit(ch,matrix)
 for i in d['scenes'][d.get('scene',0)]['nodes']:visit(i,identity)
 return d,tris
a,at=decode(old);b,bt=decode(new);removed=list((at-bt).elements());added=list((bt-at).elements());plane=0.02516326867043972
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_glb_sha256':h(old),'repaired_glb_sha256':h(new),'original_triangles':sum(at.values()),'repaired_triangles':sum(bt.values()),'exact_position_normal_material_triangles_unchanged':sum((at&bt).values()),'removed_triangles':removed,'added_triangles':added,'all_changed_triangles_on_or_below_original_hidden_plane':all(v[0][1]<=plane for _,t in removed+added for v in t),'exposed_triangle_multiset_unchanged':collections.Counter({t:n for t,n in at.items() if any(v[0][1]>plane for v in t[1])})==collections.Counter({t:n for t,n in bt.items() if any(v[0][1]>plane for v in t[1])}),'materials_identical':a['materials']==b['materials'],'nodes_identical':a['nodes']==b['nodes'],'scene_identical':a['scenes']==b['scenes'],'source_joint_plane_blender_z_equals_gltf_y_m':plane,'method':'Exact decoded world positions, original stored normals, material IDs and oriented triangle multisets; no welding, geometry repair, normal recalculation or coordinate rounding.'};r['status']='pass' if r['all_changed_triangles_on_or_below_original_hidden_plane'] and all(r[k] for k in ['exposed_triangle_multiset_unchanged','materials_identical','nodes_identical','scene_identical']) else 'fail';out.write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k not in ['removed_triangles','added_triangles']})
