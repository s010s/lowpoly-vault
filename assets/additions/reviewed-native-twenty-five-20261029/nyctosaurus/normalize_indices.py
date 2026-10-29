"""Canonicalize only two diagnosed opaque eye triangle index streams. Never creates geometry."""
import json,struct,hashlib
from collections import Counter

def sha(b):return hashlib.sha256(b).hexdigest()
def cycle(t):return min(t,t[1:]+t[:1],t[2:]+t[:2])
def normalize(raw):
 assert struct.unpack_from('<4sII',raw)==(b'glTF',2,len(raw))
 jl,jt=struct.unpack_from('<I4s',raw,12);assert jt==b'JSON'
 bl,bt=struct.unpack_from('<I4s',raw,20+jl);assert bt==b'BIN\0';start=28+jl;assert start+bl==len(raw)
 d=json.loads(raw[20:20+jl]);assert not d.get('extensionsUsed') and not d.get('animations') and not d.get('skins')
 result=bytearray(raw);allowed=set();reports=[]
 for mi,name,ai,vi in [(10,'Sphere',41,42),(17,'Sphere.001',64,65)]:
  m=d['meshes'][mi];assert m['name']==name and len(m['primitives'])==1
  p=m['primitives'][0];assert p.get('mode',4)==4 and p['indices']==ai and not p.get('targets')
  mat=d['materials'][p['material']];assert mat.get('alphaMode','OPAQUE')=='OPAQUE' and not mat.get('extensions')
  a=d['accessors'][ai];v=d['bufferViews'][vi]
  assert a=={'bufferView':vi,'componentType':5123,'count':672,'type':'SCALAR'}
  assert v['buffer']==0 and v['byteLength']==1344 and v['target']==34963 and 'byteStride' not in v
  # The index view must be exclusively referenced by this index accessor, not any attribute/image.
  assert [i for i,x in enumerate(d['accessors']) if x.get('bufferView')==vi]==[ai]
  assert all(x.get('bufferView')!=vi for x in d.get('images',[]))
  lo=start+v['byteOffset'];hi=lo+v['byteLength'];assert hi<=len(raw)
  assert all(i!=vi and (w.get('buffer',0)!=0 or w.get('byteOffset',0)+w['byteLength']<=v['byteOffset'] or w.get('byteOffset',0)>=v['byteOffset']+v['byteLength']) for i,w in enumerate(d['bufferViews']) if i!=vi)
  indices=struct.unpack_from('<672H',raw,lo);tri=[tuple(indices[i:i+3]) for i in range(0,672,3)]
  canonical=sorted(cycle(t) for t in tri)
  assert Counter(cycle(t) for t in tri)==Counter(canonical)
  packed=struct.pack('<672H',*(x for t in canonical for x in t));result[lo:hi]=packed;allowed.update(range(lo,hi))
  reports.append({'mesh':mi,'name':name,'accessor':ai,'bufferView':vi,'triangle_count':224,'winding_preserved':True,'oriented_multiset_equal':True,'before_sha256':sha(raw[lo:hi]),'after_sha256':sha(packed)})
 changed=[i for i,(a,b) in enumerate(zip(raw,result)) if a!=b];assert all(i in allowed for i in changed)
 assert len(result)==len(raw) and result[:start]==raw[:start]
 return bytes(result),{'operation':'Cyclic-minimum oriented triangle triples, lexicographically sorted; only two opaque eye index streams','input_sha256':sha(raw),'output_sha256':sha(result),'changed_byte_count':len(changed),'json_and_nonindex_bytes_unchanged':True,'eyes':reports,'geometry_regenerated':False}
