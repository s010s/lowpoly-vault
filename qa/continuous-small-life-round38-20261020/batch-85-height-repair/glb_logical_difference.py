import json,sys,datetime
from collections import Counter
from pathlib import Path
O=Path(__file__).parent;R=Path('/workspace/shared/lowpoly-batch85-height-repair-20261020');OLD=Path('/workspace/shared/lowpoly-batch85-20261020');sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values
H=json.load(open(R/'production/small-life-batch85-height-repair/maker-handoff.json'))
for item in H['items']:
 aid=item['asset_id'];a,b,_=read_glb(OLD/'production/small-life-batch85'/aid/item['previous_revision']/'artifacts'/(aid+'.glb'));c,d,_=read_glb(R/item['artifacts']['glb']['path']);parts=[]
 def triangles(doc,bin,p):
  v=accessor_values(doc,bin,p['attributes']['POSITION']);ind=[x[0] for x in accessor_values(doc,bin,p['indices'])];out=[]
  for i in range(0,len(ind),3):
   t=tuple((v[j][0],v[j][2],v[j][1]==0) for j in ind[i:i+3]);out.append(min(t,t[1:]+t[:1],t[2:]+t[:2]))
  return Counter(out)
 for ma,mc in zip(a['meshes'],c['meshes']):
  for pa,pc in zip(ma['primitives'],mc['primitives']):parts.append({'mesh':ma['name'],'material_index':pa.get('material'),'oriented_coordinate_triangle_multiset_identical':triangles(a,b,pa)==triangles(c,d,pc)})
 ok=all(x['oriented_coordinate_triangle_multiset_identical'] for x in parts);rec={'asset_id':aid,'glb_sha256':item['artifacts']['glb']['sha256'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Compare oriented triangle coordinate multisets using exact GLB x,z and bottom/top identity; source .blend full vertex-index/polygon identities separately prove vertical-side identity. Raw index differences are flat-normal export duplicate-vertex allocation, not surface connectivity changes.','prior_raw_index_diagnostic':'glb-difference.json','parts':parts,'status':'pass' if ok else 'fail'};(O/aid/'glb-logical-difference.json').write_text(json.dumps(rec,indent=2)+'\n');print(aid,ok)
