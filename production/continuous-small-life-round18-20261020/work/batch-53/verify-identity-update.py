# SPDX-License-Identifier: MIT
"""Verify the parent-confirmed identity-only update against the saved maker commit."""
from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[4];W=Path(__file__).resolve().parent;O=R/'assets/candidates/continuous-small-life-round18-20261020/batch-53';old='b204a43a5c816f9c0c76683b5ee8a4451e9050a8';task='01a156a2-8680-7691-b35e-25e9eecee03b';turn='01a156a2-9163-72a1-ac93-9a657d275a35';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
allowed={'candidate.json','profile-contract.json','project-checker.report.json','profile-checker.report.json','profile-approved-checker.report.json','preflight-contract.report.json','HANDOFF.md','checksums.sha256'}
count=0
for p in O.rglob('*'):
 if not p.is_file() or p.name in allowed:continue
 rel=str(p.relative_to(R));assert p.read_bytes()==subprocess.check_output(['git','show',old+':'+rel],cwd=R),rel;count+=1
for s in ['hypoturrilites','iodes-brownii','welded-ignimbrite-outcrop','halopoa-furrowed-burrow']:
 o=O/s/'r001';c=json.loads((o/'candidate.json').read_text());before=json.loads(subprocess.check_output(['git','show',old+':'+str((o/'candidate.json').relative_to(R))],cwd=R));assert c['artifacts']==before['artifacts'];assert c['stages']==before['stages']
 assert c['maker']['task_id']==c['maker']['thread_id']==task and c['maker']['turn_id']==turn;assert c['approval']==before['approval']=={'status':'pending'}
 q=json.loads((o/'profile-checker.report.json').read_text());assert q['valid'] and not q['approved_for_brief'] and q['profile_contract_status']=='pass' and not q['errors']
 q=json.loads((o/'profile-approved-checker.report.json').read_text());assert q['valid'] and not q['approved_for_brief'] and q['approval_blockers']
 q=json.loads((o/'concept-checker.report.json').read_text());assert q['valid'] and not q['evidence_complete'];assert q['blockers']==['concept_generated_at: unknown; do not reconstruct times from file mtimes']
 f=json.loads((o/'modeling-freeze.json').read_text());assert all(sha(o/name)==h for name,h in f['files'].items())
 for row in (o/'checksums.sha256').read_text().splitlines():h,name=row.split('  ',1);assert sha(o/name)==h
 print(s,'identity bound; static profile valid; approval pending; artifact hashes unchanged')
print(count,'protected candidate files byte-identical to',old)
