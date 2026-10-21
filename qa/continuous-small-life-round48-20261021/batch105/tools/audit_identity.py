import pathlib,json,hashlib,subprocess,os,collections,datetime,sys,math
R=pathlib.Path('/workspace/shared/lowpoly-batch105-20261021'); O=pathlib.Path('/workspace/shared/lowpoly-batch105-independent-qa-20261021');B=R/'production/small-life-batch105';H=json.loads((B/'maker-handoff.json').read_text()); C='9188a1ef90c7f61762e4bb4877ff9a8b4a5103dd'
sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from qa_glb import audit_glb,read_glb,accessor_values,IDENTITY,node_matrix,matmul,transform
from check_reproducibility import compare_rebuild
from PIL import Image
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def write(n,d):(O/'reports'/n).write_text(json.dumps(d,indent=2)+'\n')
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0',GIT_OPTIONAL_LOCKS='0')
def git(*a):return subprocess.check_output(['git','-c','protocol.allow=never','-C',str(R),*a],env=env)
errors=[];checks=[]
for fn in ['submission-manifest.json','original-freeze-manifest.json','dependency-closure-precommit.json']:
 d=json.loads((B/fn).read_text());results=[]
 for f in d['files']:
  p=R/f['path']; h=sha(p);blob=git('show',C+':'+f['path']);ok=h==f['sha256']==hashlib.sha256(blob).hexdigest() and ('bytes' not in f or len(blob)==f['bytes'])
  results.append({'path':f['path'],'sha256':h,'bytes':len(blob),'working_and_commit_match':ok})
  if not ok:errors.append(fn+':'+f['path'])
 checks.append({'manifest':fn,'sha256':sha(B/fn),'count':len(results),'bytes':sum(x['bytes'] for x in results),'files':results})
identity={'commit':git('rev-parse','HEAD').decode().strip(),'branch':git('branch','--show-current').decode().strip(),'parent':git('rev-parse','HEAD^').decode().strip(),'status_porcelain':git('status','--porcelain').decode(),'maker_handoff_sha256':sha(B/'maker-handoff.json'),'manifests':checks,'errors':errors,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
assert identity['commit']==C
write('identity.json',identity)
# Pure decoded original-GLB topology with exact coordinate-edge identity across normals/material seams.
def topology(p):
 doc,bin,_=read_glb(p);ts=[]
 def walk(i,m):
  n=doc['nodes'][i];m=matmul(m,node_matrix(n))
  if 'mesh' in n:
   for prim in doc['meshes'][n['mesh']]['primitives']:
    ps=[transform(m,v) for v in accessor_values(doc,bin,prim['attributes']['POSITION'])];ind=[v[0] for v in accessor_values(doc,bin,prim['indices'])] if 'indices' in prim else list(range(len(ps)))
    ts.extend(tuple(ps[x] for x in ind[k:k+3]) for k in range(0,len(ind),3))
  for j in n.get('children',[]):walk(j,m)
 for i in doc['scenes'][doc.get('scene',0)]['nodes']:walk(i,IDENTITY)
 edges=collections.defaultdict(list);adj=[set() for _ in ts]
 for i,t in enumerate(ts):
  for a,b in zip(t,t[1:]+t[:1]):edges[tuple(sorted((a,b)))].append((i,1 if a<b else -1))
 for refs in edges.values():
  for i,_ in refs:adj[i].update(j for j,_ in refs if i!=j)
 components=[];seen=set()
 for i in range(len(ts)):
  if i in seen:continue
  todo=[i];ids=set();seen.add(i)
  while todo:
   t=todo.pop();ids.add(t)
   for n in adj[t]:
    if n not in seen:seen.add(n);todo.append(n)
  es=[v for v in edges.values() if v[0][0] in ids]
  det=lambda a,b,c:a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0])
  r={'triangles':len(ids),'boundary_edges':sum(len(v)==1 for v in es),'nonmanifold_edges':sum(len(v)>2 for v in es),'same_direction_edges':sum(len(v)==2 and v[0][1]==v[1][1] for v in es),'signed_volume_m3':sum(det(*ts[t])/6 for t in ids)};r['pass']=r['signed_volume_m3']>0 and not any(r[k] for k in ['boundary_edges','nonmanifold_edges','same_direction_edges']);components.append(r)
 return {'glb_sha256':sha(p),'triangle_count':len(ts),'components':components,'pass':all(x['pass'] for x in components),'method':'Exact world-coordinate original triangles. No weld, repair, normal recalculation or input rewrite.'}
allassets=[]
for a in H['assets']:
 aid=a['asset_id'];d=B/aid/a['revision'];g=d/'artifacts'/f'{aid}.glb';audit=audit_glb(g,14000,6,30);write(aid+'-project.json',audit);write(aid+'-original-topology.json',topology(g));prov=[]
 for run in ['a','b']:
  q=d/'qa'/('rebuild-'+run);req=json.loads((q/'request.json').read_text());res=json.loads((q/'result.json').read_text());exe=json.loads((q/'execution.json').read_text());op=pathlib.Path(req['argv'][req['argv'].index('--output')+1]);reb=op/aid/(aid+'.glb')
  comp=compare_rebuild(g,reb,R/a['generator']['path'],d/'config.json',q/'request.json',q/'result.json',aid+'/'+aid+'.glb',root=R)
  actual=[]
  for name,e in res['outputs'].items():
   p=op/name;actual.append({'path':str(p),'sha256':sha(p),'matches_receipt':sha(p)==e['sha256'],'bytes':p.stat().st_size})
  good=all(x['matches_receipt'] for x in actual) and exe['generator_sha256']==a['generator']['sha256'] and exe['config_sha256']==a['config']['sha256'] and exe['parent_pid']==res['pid'] and req['created_at']<=res['started_at']<=exe['started_at_executor_clock']<=exe['finished_at_executor_clock']<=res['finished_at']
  prov.append({'run':run,'pid':exe['pid'],'execution_sha256':sha(q/'execution.json'),'actual_outputs':actual,'chronology_and_inputs_match':good,'semantic_comparison':comp,'full_argv':req['argv']})
 assert prov[0]['pid']!=prov[1]['pid']
 frames=[]
 for typ in ['views','details']:
  m=d/typ/'render-manifest.json'
  if not m.exists():continue
  man=json.loads(m.read_text());assert man['subject']==a['triplet'];cfg=json.loads((d/typ/'render-config.json').read_text())
  for f in man['frames']:
   p=d/typ/f['path'];im=Image.open(p);assert sha(p)==f['sha256'];assert im.size==(512,512)
   frames.append({'path':str(p.relative_to(R)),'sha256':sha(p),'dimensions':list(im.size)})
  if typ=='views':
   sheet=Image.open(d/typ/'contact-sheet.png').convert('RGB');eq=[]
   for i,f in enumerate(man['frames']):eq.append(sheet.crop(((i%4)*512,(i//4)*544,(i%4+1)*512,(i//4)*544+512)).tobytes()==Image.open(d/typ/f['path']).convert('RGB').tobytes())
   # Keep diagnostics if maker sheet has different documented caption padding.
   frames.append({'path':str((d/typ/'contact-sheet.png').relative_to(R)),'sha256':sha(d/typ/'contact-sheet.png'),'dimensions':list(sheet.size),'lossless_cell_pixels':eq})
 pins={k:v for k,v in a.items() if k in ['asset_id','revision','triplet','source','generator','config','candidate','profile_contract']}
 allassets.append({'pins':pins,'two_rebuild_provenance':prov,'render_identity':frames})
write('provenance-and-view-bindings.json',{'assets':allassets,'source_preserved':True})
print('identity',len(checks[0]['files']),len(checks[2]['files']),'errors',errors)
for a in H['assets']:
 aid=a['asset_id'];r=json.loads((O/'reports'/(aid+'-original-topology.json')).read_text());print(aid,r['pass'],r['triangle_count'],len(r['components']))
