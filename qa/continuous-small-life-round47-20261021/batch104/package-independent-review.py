from pathlib import Path
import json,hashlib
Q=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'path':str(p.relative_to(Q)),'sha256':H(p),'bytes':p.stat().st_size}
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
# Correct the draft's anticipated clock label before the immutable package is sealed.
f=Q/'final-readback-integrity.json';d=json.loads(f.read_text());d.pop('session_utc');d['session_utc_window']='2026-10-21T04:05:44Z/2026-10-21T04:05:50Z';d['timestamp_scope']='Observed session reminder bounds around actual readback, not a claim of an exact per-file timestamp.';write(f,d)
f=Q/'independent-report.json';d=json.loads(f.read_text());d['review_finalized_session_utc']='2026-10-21T04:06:04Z';d['final_readback']={'path':str(Q/'final-readback-integrity.json'),'sha256':H(Q/'final-readback-integrity.json'),'bytes':(Q/'final-readback-integrity.json').stat().st_size};write(f,d)
files=[pin(p)for p in sorted(Q.rglob('*'))if p.is_file() and p.name not in ['own-manifest.json','handoff.json','package-verification.json']]
manifest={'schema_version':1,'kind':'independent_QA_immutable_evidence_manifest','source_commit':d['source_commit'],'scope':'All own evidence and checker files. Handoff and this manifest excluded to avoid cycles. Original maker/source pins are preserved in included intake and report evidence.','files':files,'file_count':len(files),'bytes':sum(x['bytes']for x in files),'budget_bytes':35000000,'original_failure_records_retained':True}
assert manifest['bytes']<35000000
(Q/'own-manifest.json').open('x').write(json.dumps(manifest,indent=2)+'\n')
hand={'schema_version':1,'source_commit':d['source_commit'],'source_parent':d['parent_commit'],'status':d['report_status'],'report':pin(Q/'independent-report.json'),'readable_report':pin(Q/'INDEPENDENT-REPORT.md'),'own_manifest':pin(Q/'own-manifest.json'),'original_preflight':pin(Q/'reference-preflight-checkpoint.json'),'intake_readback':pin(Q/'final-readback-integrity.json'),'static_five_stage_pass':['kerygmachela/r006','pambdelurion/r006'],'static_five_stage_fail':['aegirocassis/r008:A104-1','arthropleura/r009:A104-2'],'complete_seven_stage_pass_count':0,'gpu':'UNKNOWN','scene':'UNKNOWN','website':'NOT_TESTED','publication':'NOT_PERFORMED','approval_modified':False,'source_tree_modified':False,'new_revisions_require_new_intake':True,'batch_accepted':False}
(Q/'handoff.json').open('x').write(json.dumps(hand,indent=2)+'\n')
# Actual readback of every sealed entry and control pins.
for e in manifest['files']:assert H(Q/e['path'])==e['sha256'] and (Q/e['path']).stat().st_size==e['bytes']
for k in ['report','readable_report','own_manifest','original_preflight','intake_readback']:assert H(Q/hand[k]['path'])==hand[k]['sha256']
verification={'all_manifest_entries_verified':True,'file_count':manifest['file_count'],'payload_bytes':manifest['bytes'],'manifest':pin(Q/'own-manifest.json'),'handoff':pin(Q/'handoff.json'),'complete_directory_bytes_before_verification':sum(p.stat().st_size for p in Q.rglob('*')if p.is_file()),'separate_control_receipt_not_in_manifest':True}
(Q/'package-verification.json').open('x').write(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification,indent=2))
