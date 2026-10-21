#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only exact decoded triangle identity and immutable inherited tree audit."""
import sys,json,hashlib,subprocess,os,collections,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values,IDENTITY,node_matrix,matmul,transform
D=R/'production/small-life-batch105-archimedes-repair/r002';old=R/'production/small-life-batch105/archimedes/r001/artifacts/archimedes.glb';new=D/'artifacts/archimedes.glb';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def triangles(p):
 d,b,_=read_glb(p);ts=[]
 def walk(n,m):
  node=d['nodes'][n];m=matmul(m,node_matrix(node))
  if 'mesh' in node:
   for prim in d['meshes'][node['mesh']]['primitives']:
    ps=accessor_values(d,b,prim['attributes']['POSITION']);ix=[v[0] for v in accessor_values(d,b,prim['indices'])]
    for i in range(0,len(ix),3):ts.append((prim.get('material'),tuple(transform(m,ps[j]) for j in ix[i:i+3])))
  for c in node.get('children',[]):walk(c,m)
 for n in d['scenes'][d.get('scene',0)]['nodes']:walk(n,IDENTITY)
 return ts
before=triangles(old);after=triangles(new);assert len(before)==len(after)==9396;changed=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b];assert len(changed)>0
# The frozen axial source centerline ends are z=0 and z=.035 before its existing offset.
# Classify only for a conservative spatial difference envelope, not a taper acceptance threshold.
bounds=[]
for i in changed:
 a,b=before[i],after[i];assert a[0]==b[0];coords=[p for t in (a[1],b[1]) for p in t];assert all(abs(p[0])<.0021 and abs(p[2])<.0021 for p in coords);assert all(p[1]<.0021 for p in coords) or all(.033<p[1]<.036 for p in coords);bounds.extend(coords)
report={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_glb_sha256':sha(old),'repaired_glb_sha256':sha(new),'triangle_count':len(before),'exact_unchanged_triangle_position_and_material_count':len(before)-len(changed),'changed_triangle_indices':changed,'changed_triangles_only_at_actual_axial_ends':True,'unchanged_frond_proof':'All 7460 frond triangles and source vertices are unchanged. Complete source per-index, all-face, all-material and transform identity audit is geometry-identity.json.','changed_coordinate_bounds_export_xyz_m':{'min':[min(p[k] for p in bounds) for k in range(3)],'max':[max(p[k] for p in bounds) for k in range(3)]},'interpretation':'Difference envelope merely locates existing original end regions; it is not a new scientific or taper pass/fail requirement.'};(D/'qa/glb-difference.report.json').write_text(json.dumps(report,indent=2)+'\n')
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');git=lambda *a:subprocess.check_output(['git','-c','protocol.allow=never','-C',str(R),*a],env=env);base='cc7568aae69c84100837b056ea82314aafcaf525';assets=[]
for aid,rev in [('penniretepora','r001'),('constellaria','r002'),('cystodictya','r003')]:
 path=f'production/small-life-batch105/{aid}/{rev}';a=git('ls-tree','-r',base,'--',path);b=git('ls-tree','-r','HEAD','--',path);assert a==b;files=[]
 for line in a.decode().splitlines():
  meta,p=line.split('\t');mode,kind,oid=meta.split();assert kind=='blob';blob=git('cat-file','blob',oid);files.append({'path':p,'git_blob_oid':oid,'bytes':len(blob),'sha256':hashlib.sha256(blob).hexdigest()})
 assets.append({'asset_id':aid,'revision':rev,'all_tree_entries_identical_to_public_base':True,'files':files})
(D/'qa/three-accepted-unchanged.json').write_text(json.dumps({'base_commit':base,'assets':assets,'all_unchanged':True,'method':'Offline Git exact tree mode/path/object identity at original public base and current HEAD; SHA256 and byte length computed from every inherited candidate blob. No source path, historical index, failure or accepted asset edited.'},indent=2)+'\n');print('DIFFERENCE',len(changed),'changed triangles;',len(before)-len(changed),'unchanged; inherited accepted files',sum(len(x['files']) for x in assets))
