from pathlib import Path
import json,subprocess,hashlib,shutil
hr=Path('/workspace/batch28-handoff');w=hr/'production/continuous-small-life-round10-20261018/work/batch-28';base='da272109c96e3c38a7f2421dc2340c192a0153bb';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();recs=[json.loads(l) for l in (w/'final-handoff.jsonl').read_text().splitlines()]
def tree(repo,commit):
 out=subprocess.check_output(['git','ls-tree','-rz',commit],cwd=repo);d={}
 for line in out.split(b'\0'):
  if line:
   h,p=line.split(b'\t',1);d[p.decode()]=h.decode()
 return d
results=[]
for r in recs:
 repo=Path(r['worktree']);b=tree(repo,base);t=tree(repo,r['commit']);allowed=r['scope']['changed_prefixes'];filtered={p:v for p,v in t.items() if not any(p.startswith(a+'/') for a in allowed)};assert filtered==b
 obj=[]
 for path in ['scripts','schemas','skills','.github','src','public','site','production/policies']:
  vals=[]
  for c in [base,r['commit']]:
   q=subprocess.run(['git','rev-parse',c+':'+path],cwd=repo,capture_output=True,text=True);vals.append(q.stdout.strip() if q.returncode==0 else None)
  assert vals[0]==vals[1];obj.append({'path':path,'base_tree':vals[0],'candidate_tree':vals[1],'equal':True})
 results.append(dict(asset_id=r['asset_id'],commit=r['commit'],base_file_count=len(b),unchanged_outside_own_prefixes=True,unchanged_manifest_sha256=hashlib.sha256(json.dumps(b,sort_keys=True).encode()).hexdigest(),key_tree_objects=obj))
(w/'base-tree-integrity.json').write_text(json.dumps(dict(kind='git-tree-integrity-independent-of-sparse-working-view',base=base,status='pass',method='Recursive Git ls-tree compares every base path, blob/object ID and file mode outside the exact own prefixes, not sparse working-tree files. Final candidate objects are checked, mistaken prior claim history is retained separately.',assets=results),indent=2)+'\n')
shutil.copy('/workspace/batch28-control/worktree-setup-incident.json',w/'worktree-setup-incident.json')
recover=[]
for r in recs:
 rp=Path(r['worktree'])/r['work_dir']/'sparse-index-recovery.json'
 if rp.exists():
  x=json.loads(rp.read_text());recover.append(dict(asset_id=r['asset_id'],path=str(rp.relative_to(Path(r['worktree']))),sha256=sha(rp),original_claim=x['prior_claim_commit'],recovery_commit=x['recovery_commit'],final_commit=r['commit']))
(w/'recovery-lineage.json').write_text(json.dumps(dict(batch='batch-28',source_build_failures=2,source_warning_count=sum(len(r['source_warnings']) for r in recs),prototype_directories=[p for r in recs for p in r['iterations_retained'] if '/prototype-' in p],recoveries=recover),indent=2)+'\n')
for name in ['HANDOFF.md','README.md']:
 with (w/name).open('a') as f:f.write('\nWorkspace/setup lineage: worktree-setup-incident.json retains the initial full-checkout refusal and duplicate-branch probe. recovery-lineage.json pins mistaken no-checkout claim SHAs and ordinary FF restore commits for Sea-stack/Fulgurite; base-tree-integrity.json verifies every final Git base blob/mode outside own asset prefixes, including shared script/schema/skills/CI/site trees. Main and other branches were unchanged. The actual Sea missing-helper source launch and Fulgurite two-degenerate-triangle source rejection remain nonzero exits, separately from the Hurdia carapace-seating and Sea directional-erosion craft prototypes. Final chronology is56 owned jobs, zero overlap,2 nonzero, all groups exited; none of the failed attempts is called PASS. Seven source smooth-style warnings are individually dispositioned (2/4/0/1).\n')
for name in ['final_handoff.py','handoff_summary.py','final_integrity.py']:shutil.copy(Path('/workspace/batch28-control')/name,w/('execution-'+name))
scope=json.loads((w/'scope.json').read_text());scope['supporting_reports']={name:sha(w/name) for name in ['base-tree-integrity.json','worktree-setup-incident.json','recovery-lineage.json','execution-final_handoff.py','execution-handoff_summary.py','execution-final_integrity.py']};(w/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
serial=json.loads((w/'serial-execution-summary.json').read_text());assert serial['top_level_launch_count']==56 and serial['nonzero_exit_count']==2 and serial['overlapping_top_level_owned_launches']==0
assert sum(len(r['source_warnings']) for r in recs)==7
for r in recs:print(r['asset_id'],r['commit'],len(r['artifacts']),r['source_export'],r['profile_contract_status'],r['candidate_record_valid'],r['approved_for_brief'],r['legacy_errors'])
for name in ['final-handoff.jsonl','scope.json','serial-execution-summary.json']:print(name,sha(w/name))
