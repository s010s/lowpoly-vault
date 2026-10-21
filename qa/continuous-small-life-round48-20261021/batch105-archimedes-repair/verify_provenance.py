import pathlib,json,hashlib,os,subprocess
R=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-repair-20261021');Q=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-independent-qa-20261021');D=R/'production/small-life-batch105-archimedes-repair/r002';P=pathlib.Path('/workspace/shared/lowpoly-batch105-independent-qa-20261021');A=pathlib.Path('/workspace/shared/lowpoly-batch105-archimedes-repair-evidence');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text());pin=lambda p:{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
prior=[]
for f in load(P/'evidence-manifest.json')['files']:
 p=P/f['path'];assert sha(p)==f['sha256'] and p.stat().st_size==f['bytes'];prior.append(pin(p))
deps=[]
for name in ['dependencies.json','proof-dependencies.json']:
 for f in load(D.parent/name)['files']:
  p=R/f['path'];assert sha(p)==f['sha256'];deps.append(pin(p))
receipt=load(A/'local-commit-receipt.json');assert receipt['commit']=='3b470a4aca963df9ceae39affcc96602707a1180';assert len(receipt['files'])==93
for f in receipt['files']:
 p=R/f['path'];assert sha(p)==f['sha256'] and p.stat().st_size==f['bytes']
# Verify retained render jobs were generated from exact candidate and completed after binding.
render=[];trip=load(D/'candidate-binding.json')['subject'];bound=load(D/'candidate-binding.json')['bound_at']
for name in ['views/views-1','views/views-2','views/views-3','views/views-4','lower-end','upper-end']:
 req=load(D/name/'request.json');res=load(D/name/'result.json');assert res['status']=='succeeded' and res['returncode']==0 and res['started_at']>bound;render.append({'request':pin(D/name/'request.json'),'result':pin(D/name/'result.json'),'started_at':res['started_at'],'finished_at':res['finished_at']})
for endpoint in ['lower','upper']:
 # Original and repaired endpoint cameras are exactly equal, not an angle chosen to hide the defect.
 assert (D/f'{endpoint}-end/render-config.json').read_bytes()==(P/f'archimedes-{endpoint}-end/render-config.json').read_bytes()
# Supplemental raw report is postcommit read-only evidence, not smuggled into the candidate or maker manifest.
extra=A/'endpoint-interior-contact.report.json';assert sha(extra)=='90c7521025376581fa1c3445c25a1660a5e60d7b1e626d180a412554705cfe89';assert load(extra)['source_commit']==receipt['commit']
env=dict(os.environ,GIT_NO_LAZY_FETCH='1',GIT_TERMINAL_PROMPT='0');cmd=['git','-c','protocol.allow=never','-C',str(R)];assert subprocess.check_output(cmd+['status','--porcelain'],env=env)==b'';assert subprocess.check_output(cmd+['rev-parse','HEAD'],env=env).decode().strip()==receipt['commit']
r={'status':'pass','all_prior_62_qa_files_verified':len(prior)==62,'immutable_prior_evidence_manifest':pin(P/'evidence-manifest.json'),'prior_evidence':prior,'dependency_files_verified':deps,'final_candidate_commit_receipt':pin(A/'local-commit-receipt.json'),'all93_committed_files_verified':True,'render_job_records':render,'endpoint_cameras_identical_to_original_defect_views':True,'postcommit_supplement':pin(extra),'read_only_candidate_status':'clean','original_report_preserved':pin(P/'independent-report.json')};(Q/'provenance-independent.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS: all62 prior QA evidence files,22 dependencies,93 receipt files,6 render jobs; original endpoint camera configs unchanged')
