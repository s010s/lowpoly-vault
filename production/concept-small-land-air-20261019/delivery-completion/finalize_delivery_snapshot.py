# SPDX-License-Identifier: MIT
"""Verify records and seal current hashes; no model or acceptance changes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
REPO=next(p for p in HERE.parents if (p/'scripts/validate_candidate.py').exists())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def files():return sorted(p for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.blend1','.blend2'))
source=json.loads((HERE/'baseline-files.json').read_text());baseline=source['files']
manifest=BASE/'freeze-manifest.json';exact=HERE/'exact-diff.json'
# Make the final snapshot's changed-record status explicit before running the check.
write(manifest,{'status':'pending-final-delivery-snapshot','source_commit':source['source_commit'],'original_manifest':'delivery-completion/original-records/freeze-manifest.json'})
subprocess.run([sys.executable,str(HERE/'verify_delivery_completion.py')],cwd=REPO,check=True)
changes=[];added=[];unchanged=0
for p in files():
 rel=p.relative_to(REPO).as_posix()
 if p in (manifest,exact):continue
 now={'bytes':p.stat().st_size,'sha256':digest(p)}
 if rel in baseline:
  if now==baseline[rel]:unchanged+=1
  else:changes.append({'path':rel,'before':baseline[rel],'after':now})
 else:added.append({'path':rel,**now})
write(exact,{'created_at':datetime.now(timezone.utc).isoformat(),'source_commit':source['source_commit'],'scope':'Exact record-only diff; every original file outside the allowlist must be unchanged. This report and freeze-manifest.json exclude their own hashes to avoid circularity; the final Git tree identifies both.','unchanged_original_files':unchanged,'modified_records':changes,'added_files':added,'snapshot_manifest_change':{'path':manifest.relative_to(REPO).as_posix(),'before':baseline[manifest.relative_to(REPO).as_posix()],'after_hash_authority':'Final commit tree; manifest hashes exact-diff.json, so exact-diff cannot hash the final manifest without a cycle.'}})
write(manifest,{'frozen_at':datetime.now(timezone.utc).isoformat(),'snapshot_kind':'delivery-record-completion','source_model_commit':source['source_commit'],'scope':'Current delivery snapshot; all files except this manifest. This is not a pre-model design freeze or acceptance. Original snapshot preserved in delivery-completion/original-records/freeze-manifest.json. Git commit SHA supplied after commit to avoid circular self-reference.','files':[{'path':p.relative_to(BASE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files() if p!=manifest]})
for entry in json.loads(manifest.read_text())['files']:
 p=BASE/entry['path'];assert digest(p)==entry['sha256'] and p.stat().st_size==entry['bytes']
print(json.dumps({'snapshot_files':len(json.loads(manifest.read_text())['files']),'changed_records_excluding_manifest':len(changes),'added_files_excluding_exact_diff':len(added),'unchanged_original_files':unchanged,'snapshot_sha256':digest(manifest)},indent=2))
