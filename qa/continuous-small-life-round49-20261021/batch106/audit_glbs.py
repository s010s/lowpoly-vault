import sys,json,hashlib,datetime,collections,math
from pathlib import Path
sys.dont_write_bytecode=True
R=Path('/workspace/shared/lowpoly-batch106-20261021');B=R/'production/small-life-batch106';O=Path(__file__).parent
sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,audit_glb,semantic_digest,IDENTITY
from validate_candidate import validate_candidate
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def triangles(p):
 d,b,_=read_glb(p);out=[]
 def walk(i,parent):
  n=d['nodes'][i];m=matmul(parent,node_matrix(n))
  if 'mesh' in n:
   for pr in d['meshes'][n['mesh']]['primitives']:
    assert pr.get('mode',4)==4
    vv=[transform(m,v) for v in accessor_values(d,b,pr['attributes']['POSITION'])];ix=[v[0] for v in accessor_values(d,b,pr['indices'])] if 'indices' in pr else list(range(len(vv)))
    for j in range(0,len(ix),3):out.append(tuple(vv[x] for x in ix[j:j+3]))
  for ch in n.get('children',[]):walk(ch,m)
 for i in d['scenes'][d.get('scene',0)]['nodes']:walk(i,IDENTITY)
 return out
cross=lambda a,b:(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]);dot=lambda a,b:sum(x*y for x,y in zip(a,b));sub=lambda a,b:tuple(x-y for x,y in zip(a,b))
results=[]
for aid,rev in [('didymograptus','r004'),('monograptus','r004'),('diplograptus','r009'),('dictyonema','r005')]:
 p=B/aid/rev;glb=p/'artifacts'/(aid+'.glb');raw=triangles(glb);edges=collections.defaultdict(list);areas=[];vols=[]
 for i,t in enumerate(raw):
  a,b,c=t;areas.append(dot(cross(sub(b,a),sub(c,a)),cross(sub(b,a),sub(c,a))));vols.append(dot(a,cross(b,c))/6)
  for u,v in zip(t,t[1:]+t[:1]):edges[tuple(sorted((u,v)))].append((u,v,i))
 adj=collections.defaultdict(set)
 for e in edges.values():
  for u in e:
   for v in e:adj[u[2]].add(v[2])
 left=set(range(len(raw)));islands=[]
 while left:
  s=next(iter(left));left.remove(s);piece={s};todo=[s]
  while todo:
   for i in adj[todo.pop()]:
    if i in left:left.remove(i);piece.add(i);todo.append(i)
  islands.append({'triangles':len(piece),'signed_volume':sum(vols[i] for i in piece)})
 top={'triangles':len(raw),'nonmanifold_edges':sum(len(e)!=2 for e in edges.values()),'same_direction_edges':sum(len(e)==2 and e[0][:2]==e[1][:2] for e in edges.values()),'zero_area_triangles':sum(x==0 for x in areas),'closed_islands':islands,'exact_source_triangle_order_unchanged':True,'method':'Original GLB exact decoded coordinates identify geometric seams only. No coordinate rounding, spatial weld, vertex move, triangle reordering, winding repair or normal changes. Island adjacency and positive signed volume independently recomputed.'}
 top['pass']=not(top['nonmanifold_edges'] or top['same_direction_edges'] or top['zero_area_triangles']) and all(i['signed_volume']>0 for i in islands)
 audit=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30)
 c=json.loads((p/'candidate.json').read_text());cr=validate_candidate(str((p/'candidate.json').relative_to(R)),R,None,'static-stylized-v1',str((p/'profile-contract.json').relative_to(R)))
 re=O/aid/(aid+'-source-reexport.glb');td,tb,_=read_glb(glb);rd,rb,_=read_glb(re);retri=triangles(re)
 # Exact sorted oriented position triples; cyclic rotation equivalent, winding reversal is not.
 canon=lambda t:min(t,t[1:]+t[:1],t[2:]+t[:2])
 equal=collections.Counter(canon(t) for t in raw)==collections.Counter(canon(t) for t in retri)
 reexport={'exact_oriented_triangle_multiset_equal':equal,'project_semantic_equal':semantic_digest(td,tb)==semantic_digest(rd,rb),'original_semantic_sha256':semantic_digest(td,tb),'reexport_semantic_sha256':semantic_digest(rd,rb),'original_materials':td.get('materials'),'reexport_materials':rd.get('materials'),'source_untouched':True}
 chains=[]
 for lab in ['a','b']:
  req=json.loads((p/f'qa/rebuild-{lab}-request.json').read_text());res=json.loads((p/f'qa/rebuild-{lab}-result.json').read_text());exe=json.loads((p/f'qa/rebuild-{lab}-execution.json').read_text());out=Path(exe['argv'][exe['argv'].index('--output')+1]);fp=hashlib.sha256(json.dumps(req['identity'],sort_keys=True,separators=(',',':')).encode()).hexdigest();errs=[]
  if req['fingerprint']!=fp or res['fingerprint']!=fp:errs.append('fingerprint')
  if res['status']!='succeeded' or res['returncode']!=0:errs.append('result')
  if not(req['created_at']<=exe['started_at']<=exe['finished_at']<=res['finished_at']):errs.append('chronology')
  for name,v in req['identity']['inputs'].items():
   if h(Path(v['path']))!=v['sha256']:errs.append('input '+name)
  for name,v in res['outputs'].items():
   op=out/name
   if not op.exists() or h(op)!=v['sha256'] or op.stat().st_size!=v['bytes']:errs.append('output '+name)
  reb=out/aid/(aid+'.glb');rbd,rbb,_=read_glb(reb);match=semantic_digest(rbd,rbb)==semantic_digest(td,tb)
  if not match:errs.append('semantic')
  if exe['generator_sha256']!=c['artifacts']['generator']['sha256'] or exe['config_sha256']!=c['artifacts']['config']['sha256']:errs.append('exact generator/config')
  if (glb.stat().st_dev,glb.stat().st_ino)==(reb.stat().st_dev,reb.stat().st_ino):errs.append('not separately retained')
  chains.append({'job':lab,'output_directory':str(out),'generator_pid':exe['pid'],'queue_pid':res['pid'],'started_at':exe['started_at'],'finished_at':exe['finished_at'],'request_sha256':h(p/f'qa/rebuild-{lab}-request.json'),'execution_sha256':h(p/f'qa/rebuild-{lab}-execution.json'),'result_sha256':h(p/f'qa/rebuild-{lab}-result.json'),'glb_sha256':h(reb),'separate_inode':reb.stat().st_ino,'semantic_match':match,'errors':errs})
 assert chains[0]['generator_pid']!=chains[1]['generator_pid']
 result={'asset_id':aid,'revision':rev,'glb_sha256':h(glb),'project':audit,'candidate':cr,'topology':top,'source_reexport':reexport,'retained_rebuild_chains':chains,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (O/aid/'independent-technical.json').write_text(json.dumps(result,indent=2));print(aid,'project',audit['errors'],'candidate',cr['valid'],cr['errors'],'topology',top['pass'],'reexport',equal,reexport['project_semantic_equal'],'rebuild errors',[x['errors'] for x in chains]);results.append(result)
