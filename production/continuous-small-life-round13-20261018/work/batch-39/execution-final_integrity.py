from pathlib import Path
import json,subprocess,hashlib,shutil
hr=Path('/workspace/batch39-handoff');w=hr/'production/continuous-small-life-round13-20261018/work/batch-39';base='2f0a90f833e2607963ec33e5fd4647a8506e1bee';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();recs=[json.loads(l) for l in (w/'final-handoff.jsonl').read_text().splitlines()]
def tree(repo,commit):
 d={}
 for line in subprocess.check_output(['git','ls-tree','-rz',commit],cwd=repo).split(b'\0'):
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
  assert vals[0]==vals[1];obj.append(dict(path=path,base_tree=vals[0],candidate_tree=vals[1],equal=True))
 cl=repo/r['work_dir']/'claim.json';claim=json.loads(cl.read_text());assert claim['base_commit']==base and claim['maker_model']=='GPT-6.1 Sol' and claim['reasoning_effort']=='medium'
 results.append(dict(asset_id=r['asset_id'],commit=r['commit'],base_file_count=len(b),unchanged_outside_own_prefixes=True,unchanged_manifest_sha256=hashlib.sha256(json.dumps(b,sort_keys=True).encode()).hexdigest(),key_tree_objects=obj,claim=dict(path=str(cl.relative_to(repo)),sha256=sha(cl),sparse_index_setup=claim['sparse_index_setup'])))
(w/'base-tree-integrity.json').write_text(json.dumps(dict(kind='git-tree-integrity-independent-of-sparse-working-view',base=base,status='pass',method='Recursive Git ls-tree compares every base path, object/blob ID and file mode outside exact own prefixes. Normal complete checkout populated full index before sparse selection; empty cached base diff and shared tree object equality were checked before each claim.',assets=results),indent=2)+'\n')
serial=json.loads((w/'serial-execution-summary.json').read_text());warnings=sum(len(r['source_warnings']) for r in recs);attempts=[dict(asset_id=r['asset_id'],retained=r['iterations_retained']) for r in recs]
(w/'attempts-summary.json').write_text(json.dumps(dict(batch_id='batch-39',source_warnings=warnings,nonzero_owned_exits=serial['nonzero_exit_count'],attempts=attempts,verdict_limit='Retained source drafts or failed attempts do not receive independent acceptance; final source/hash checks are separate.'),indent=2)+'\n')
assert serial['overlapping_top_level_owned_launches']==0 and serial['all_owned_process_groups_exited']
for name in ['HANDOFF.md','README.md']:
 with (w/name).open('a') as f:f.write(f"\nFinal integrity: {serial['top_level_launch_count']} actual owned top-level jobs, zero overlap, {serial['nonzero_exit_count']} actual nonzero exits, every owned process group exited. {warnings} source smooth-style prompts are individually dispositioned. base-tree-integrity.json compares every final Git base blob/mode outside own prefixes and explicit shared tree IDs; it is not a sparse working-view inference. Each normal complete checkout populated the index before sparse selection, with empty cached base diff checked before own claim files were added. Clavagella retains a source-only material-boundary prototype; actual geometric valve relief replaces serrated face-selected color edges, without a new soft-animal claim. Copper retains a source-only overclean ribbon-terminal draft; final widths and irregular flattened crystal ends were geometrically revised with fresh evidence. attempts-summary.json enumerates retained drafts/failures without turning them into independent PASS.\n")
for name in ['final_handoff.py','handoff_summary.py','final_integrity.py']:shutil.copy(Path('/workspace/batch39-control')/name,w/('execution-'+name))
scope=json.loads((w/'scope.json').read_text());scope['shared_changes_definition']='Final net Git diff from the specified base only. No shared base blob or file mode differs in any candidate.';scope['supporting_reports']={name:sha(w/name) for name in ['base-tree-integrity.json','attempts-summary.json','execution-final_handoff.py','execution-handoff_summary.py','execution-final_integrity.py']};(w/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
for r in recs:print(r['asset_id'],r['commit'],len(r['artifacts']),r['source_export'],r['profile_contract_status'],r['candidate_record_valid'],r['approved_for_brief'],r['legacy_errors'])
for name in ['final-handoff.jsonl','scope.json','serial-execution-summary.json']:print(name,sha(w/name))
print('JOBS',serial['top_level_launch_count'],'NONZERO',serial['nonzero_exit_count'],'WARNINGS',warnings)
