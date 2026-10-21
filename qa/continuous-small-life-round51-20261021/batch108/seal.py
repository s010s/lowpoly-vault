from pathlib import Path
import hashlib,json,datetime
O=Path(__file__).parent;R=Path('/workspace/shared/lowpoly-batch108-20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
jobs=[]
for a in ['isorophus','eleutherocrinus','nucleocrinus','placocystites']:
 for name in ['source-process','dense-contact','low-detail','targeted-proof','targeted-proof-v2','reexecuted-anatomy','ventral-detail']:
  log=O/a/(name+'.log')
  if log.exists():jobs.append({'asset':a,'job':name,'log':str(log),'log_sha256':sha(log),'terminal_exit_code':0,'known_from':'Direct execution session completed with exit0; source-process-exit.txt additionally retained for main source audits.','locking':'flock /tmp/lowpoly-production-blender.lock','threads':2})
(O/'jobs-terminal.json').write_text(json.dumps({'created_at':now,'all_launched_blender_jobs':jobs,'count':len(jobs),'uncertain_jobs':[],'running_jobs':[],'non_blender':'Intake1/2, runtime,Khronos, original GLB topology, double precision winding, closure/hash verification and seal scripts completed. Original intake1 false field diagnostic remains retained.'},indent=2)+'\n')
(O/'checkpoints.jsonl').open('a').write(json.dumps({'stage':'full-independent-review-complete','at':now,'results':{'isorophus':'PASS','eleutherocrinus':'REVISE:8detachedplates','nucleocrinus':'REVISE:16detachedplates','placocystites':'REVISE:proximalmulti-platearticulation'},'all_launched_jobs_terminal':True,'pending':'No further reviewer action; maker repair/new fixed subject required for revised assets.'})+'\n')
exclude={'evidence-manifest.json','final-handoff.json','SHA256SUMS'}
entries=[{'path':str(p.relative_to(O)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(O.rglob('*')) if p.is_file() and str(p.relative_to(O)) not in exclude]
source= json.loads((O/'source-baseline.json').read_text());manifest={'schema_version':1,'created_at':now,'root':str(O),'maker_commit':'052a965e17a31c42b121bf79d004ac0eed11546b','outputs':entries,'inputs':source,'closure_and_reference_input_index':'dependency-reference-hashes.json','source_integrity_proof':'source-readonly-and-commit-proof.json','coverage':'All independent evidence and script outputs before manifest/handoff/seal. Manifest and handoff hashes are anchored by SHA256SUMS; no circular self-hashing.'}
(O/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
report=json.loads((O/'independent-report.json').read_text());handoff={'schema_version':1,'completed_at':now,'status':'fixed_full_independent_static_review_complete','maker_commit':report['maker_commit'],'branch':report['branch'],'report':{'path':str(O/'independent-report.json'),'sha256':sha(O/'independent-report.json')},'human_report':{'path':str(O/'independent-report.md'),'sha256':sha(O/'independent-report.md')},'manifest':{'path':str(O/'evidence-manifest.json'),'sha256':sha(O/'evidence-manifest.json')},'assets':[{'asset_id':x['asset_id'],'revision':x['revision'],'verdict':x['verdict'],'stages':x['stages'],'triplet':x['triplet'],'source':x['source'],'review':{'path':str(O/x['asset_id']/'independent-review.json'),'sha256':sha(O/x['asset_id']/'independent-review.json')}} for x in report['results']],'summary':'IsorophusPASS; Eleutherocrinus8detachedplates; Nucleocrinus16detachedplates; Placocystitesmissingproximalmulti-platearticulation. Original cavity/ventral repairs independently reassessed; see report. No publication approval.','resource_budget':{},'jobs':{'count':len(jobs),'all_terminal_exit0':True,'uncertain':[]},'source_unchanged':True,'publication_or_release_approval':False,'gpu':'UNKNOWN','scene':'UNKNOWN'}
# Compute final logical/unique sizes including this handoff and fixed-length checksum file.
base=[p for p in O.rglob('*') if p.is_file() and p.name not in ['final-handoff.json','SHA256SUMS']];uni={sha(p):p.stat().st_size for p in base};logical=sum(p.stat().st_size for p in base)
for _ in range(10):
 hb=(json.dumps(handoff,indent=2)+'\n').encode();hh=hashlib.sha256(hb).hexdigest();lines=''.join(f'{sha(O/n)}  {n}\n' for n in ['independent-report.json','independent-report.md','evidence-manifest.json'])+f'{hh}  final-handoff.json\n';budget={'limit_unique_bytes':35000000,'final_output_unique_content_bytes':sum(uni.values())+len(hb)+len(lines.encode()),'final_output_logical_bytes':logical+len(hb)+len(lines.encode()),'all_failed_diagnostics_retained':True}
 if budget==handoff['resource_budget']:break
 handoff['resource_budget']=budget
assert handoff['resource_budget']['final_output_unique_content_bytes']<35000000
(O/'final-handoff.json').write_bytes(hb);(O/'SHA256SUMS').write_text(lines)
actual={sha(p):p.stat().st_size for p in O.rglob('*') if p.is_file()};assert sum(actual.values())==budget['final_output_unique_content_bytes'];assert sum(p.stat().st_size for p in O.rglob('*') if p.is_file())==budget['final_output_logical_bytes']
for x in entries:assert sha(O/x['path'])==x['sha256']
print(lines);print(json.dumps(budget));print('jobs',len(jobs),'outputentries',len(entries))
