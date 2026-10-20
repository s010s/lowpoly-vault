import pathlib,json,hashlib,subprocess
Q=pathlib.Path('/workspace/shared/lowpoly-round32-qa78');R=pathlib.Path('/workspace/shared/lowpoly-batch78-20261020');REF=pathlib.Path('/workspace/shared/lowpoly-batch78-references');H=R/'production/continuous-small-life-round32-20261020/work/batch-78/HANDOFF.json';C=R/'production/continuous-small-life-round32-20261020/work/batch-78/tracked-closure.json';
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
owned=[];total=0
for p in sorted(Q.rglob('*')):
 if not p.is_file() or p.name=='OWNED_MANIFEST.json':continue
 data=p.read_bytes();total+=len(data);owned.append({'path':str(p.relative_to(Q)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
handoff=json.loads(H.read_text()); all_refs=[]
for a in handoff['assets']:
 d=R/a['path']; refs=json.loads((d/'references.json').read_text())
 for s in refs.get('sources',[]):
  for im in s.get('consulted_images',[]):
   p=REF/im['filename']; all_refs.append({'path':str(p),'filename':p.name,'sha256':h(p) if p.exists() else None,'rights':'consulted-only; source rights retained; not incorporated or redistributed','declared_sha256':im['sha256']})
producer_inputs=[]
for p in [H,C,R/'production/continuous-small-life-round32-20261020/work/batch-78/design-freeze-chronology.json',R/'production/continuous-small-life-round32-20261020/work/batch-78/verification-final.json']:
 producer_inputs.append({'path':str(p),'sha256':h(p),'use':'read-only producer/maker evidence; not acceptance by itself'})
for a in handoff['assets']:
 producer_inputs.append({'path':str(R/a['path']),'asset_id':a['asset_id'],'revision':a['revision'],'glb_sha256':h(R/a['path']/'model.glb'),'use':'read-only candidate and producer evidence'})
manifest={'kind':'QA-owned artifact manifest','schema_version':1,'source_commit':'aeee367763cf731cd7564a550e4d3be3d2684ce7','qa_output_root':str(Q),'qa_owned_files_count':len(owned),'qa_owned_files_bytes':total,'qa_owned_files':owned,'consult_only_inputs':{'pinned_producer_source':{'path':str(R),'commit':'aeee367763cf731cd7564a550e4d3be3d2684ce7','tracked_closure_count':660,'tracked_closure_bytes':67269722,'tracked_closure_sha256':h(C),'use':'Read-only source, briefs, candidates, producer records and original attempts. No mutations.'},'producer_evidence':producer_inputs,'primary_reference_pixels':{'path':str(REF),'items':all_refs,'use':'Consulted-only source pixels, not incorporated or redistributed; kept outside QA-owned files.'}},'manifest_self_hash':'Not included to avoid a self-referential hash; compute SHA-256 of this file after writing.'}
p=Q/'OWNED_MANIFEST.json';p.write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'manifest':str(p),'manifest_sha256':h(p),'qa_owned_files_count':len(owned),'qa_owned_files_bytes':total,'assets':[(a['asset_id'],a['revision'],a['hashes']['glb']) for a in handoff['assets']],'final_reports':{str(x.relative_to(Q)):h(x) for x in [Q/'reports/static-dispositions.json',Q/'reports/asset-evidence.json',Q/'reports/postcheck-manifest.json',Q/'semantic-jobs/independent-semantic-rebuilds.json']}} ,indent=2))
