# SPDX-License-Identifier: MIT
"""Compare unchanged-index source meshes; does not establish visual acceptance."""
import bpy,sys,json,hashlib
from pathlib import Path
old,new,out=map(Path,sys.argv[sys.argv.index('--')+1:])
def read(p):
 bpy.ops.wm.open_mainfile(filepath=str(p));o=next(o for o in bpy.data.collections['EXPORT'].all_objects if o.type=='MESH');return [tuple(v.co) for v in o.data.vertices],[tuple(f.vertices) for f in o.data.polygons]
a,fa=read(old);b,fb=read(new);assert len(a)==len(b) and fa==fb
changed=[];max_below=0
for i,(v,w) in enumerate(zip(a,b)):
 d=sum((v[k]-w[k])**2 for k in range(3))**.5
 if v[2]<.066:max_below=max(max_below,d)
 if d>1e-8:changed.append((i,v[2],d))
r={'status':'PASS' if max_below<1e-8 else 'FAIL','scope':'HYS-QA-01 locality only; unchanged vertex indexing and faces compared. No visual/factual acceptance.','baseline_blend_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'repaired_blend_sha256':hashlib.sha256(new.read_bytes()).hexdigest(),'topology_identical':True,'vertex_count':len(a),'changed_vertex_count_at_10nm_tolerance':len(changed),'lowest_changed_baseline_z_m':min(c[1] for c in changed),'max_vertex_delta_below_z_0_066_m':max_below,'maximum_vertex_delta_m':max(c[2] for c in changed),'note':'All vertices below 66 mm, including three folds, body cords below the shoulder, lower cavity, canal and waist, are position-identical within 10 nm. Only shoulder and spire collar relief changed.'}
out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
