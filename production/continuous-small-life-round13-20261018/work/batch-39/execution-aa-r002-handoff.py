from pathlib import Path
import json,hashlib,subprocess,shutil
hr=Path('/workspace/batch39-handoff');hw=hr/'production/continuous-small-life-round13-20261018/work/batch-39';base='2f0a90f833e2607963ec33e5fd4647a8506e1bee';old_source='50a980789119a9d9d2049f15dd05681236cb5152';old_handoff='0eed2d38d04f4b3d2b847eff8f376934769c0102';qa='bfb62e0ad5fcf00264f6d63c44a03e26a53191ea';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Retain original final records and scripts before rebinding the single changed item.
hist=hw/'history/r001';hist.mkdir(parents=True,exist_ok=True)
if not (hist/'final-handoff.jsonl').exists():
 for p in list(hw.iterdir()):
  if p.is_file():shutil.copy(p,hist/p.name)
old_lines=(hist/'final-handoff.jsonl').read_text().splitlines();original=[json.loads(x) for x in old_lines];oldaa=next(x for x in original if x['asset_id']=='aa-lava-front')
# Run the same artifact-integrity collector for this exact revision only. No report/asset is regenerated.
s=(hist/'execution-final_handoff.py').read_text().split('# Audit actual process chronology')[0]
s=s.replace("['clavagella', 'aa-lava-front', 'native-copper-dendrite', 'nereites-lobed-meander']","['aa-lava-front']").replace("Path('/workspace/batch39-'+a)","Path('/workspace/batch39-'+a+'-r002')").replace("'r001'","'r002'").replace("'candidate/batch39-'+a+'-20261018'","'candidate/batch39-'+a+'-r002-20261019'").replace("prefixes=[str(o.relative_to(r)),str(w.relative_to(r))]","prefixes=[str(o.parent.relative_to(r)),str(w.parent.relative_to(r))]")
ns={};exec(compile(s,'single-r002-artifact-collector','exec'),ns);rec=ns['records'][0];r=Path(rec['worktree']);w=r/rec['work_dir'];o=r/rec['candidate_dir'];tip=rec['commit'];delta=subprocess.check_output(['git','diff','--name-only',old_source,tip],cwd=r,text=True).splitlines();assert all(p.startswith(rec['work_dir']+'/') or p.startswith(rec['candidate_dir']+'/') for p in delta)
for prefix in [oldaa['candidate_dir'],oldaa['work_dir']]:assert subprocess.check_output(['git','rev-parse',old_source+':'+prefix],cwd=r)==subprocess.check_output(['git','rev-parse',tip+':'+prefix],cwd=r)
rec['targeted_repair']=dict(parent_source_commit=old_source,parent_glb_sha256=oldaa['glb_sha256'],original_qa_commit=qa,original_handoff=old_handoff,criteria=['normal-view-craft','basic-form-and-scope'],reason='Original rectangular plinth and residual first-r002 perimeter shoulder; final core recessed under embedded clinker with irregular front/toe.',status='targeted parent review pending; maker does not sign PASS',unaffected_models='Clavagella/copper/Nereites source commits and every artifact pin unchanged',delta_from_parent_paths=delta,prelaunch_failure=dict(path=str((w/'failed-prelaunch-01-path-template-substitution/failure.json').relative_to(r)),sha256=sha(w/'failed-prelaunch-01-path-template-substitution/failure.json'),owned_child_started=False))
rec['iterations_retained'] += [str(p.relative_to(r)) for p in w.glob('failed-prelaunch-*')]
rec['independent_acceptance']='Only original Aa mandatory correction awaits scoped parent review; no new full-batch QA round.'
new_lines=[json.dumps(rec,ensure_ascii=False) if json.loads(x)['asset_id']=='aa-lava-front' else x for x in old_lines];(hw/'final-handoff.jsonl').write_text('\n'.join(new_lines)+'\n');current=[json.loads(x) for x in new_lines]
assert len(current)==4 and {x['asset_id'] for x in current}=={x['asset_id'] for x in original}
for x,y in zip(old_lines,new_lines):
 if json.loads(x)['asset_id']!='aa-lava-front':assert x==y
for rr in current:
 repo=Path(rr['worktree']);assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==rr['commit'];assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip();remote=subprocess.check_output(['git','-c','credential.helper=!gh auth git-credential','ls-remote','origin',rr['remote_ref']],cwd=repo,text=True).split()[0];assert remote==rr['commit']
 for pin in rr['artifacts'].values():assert sha(repo/pin['path'])==pin['sha256']
# Prove complete Git-tree scope, r001 byte preservation and unchanged non-AA records.
def tree(repo,commit):
 out={}
 for row in subprocess.check_output(['git','ls-tree','-rz',commit],cwd=repo).split(b'\0'):
  if row:meta,path=row.split(b'\t',1);out[path.decode()]=meta.decode()
 return out
bt=tree(r,base);ct=tree(r,tip);assert {p:v for p,v in ct.items() if not any(p.startswith(pre+'/') for pre in rec['scope']['changed_prefixes'])}==bt
integrity=json.loads((hist/'base-tree-integrity.json').read_text());item=next(x for x in integrity['assets'] if x['asset_id']=='aa-lava-front');item.update(commit=tip,unchanged_outside_own_prefixes=True,r001_source_commit=old_source,r001_work_and_candidate_trees_unchanged=True,delta_from_parent_only_r002=True,repair_claim=dict(path=str((w/'repair-claim.json').relative_to(r)),sha256=sha(w/'repair-claim.json')))
for obj in item['key_tree_objects']:
 vals=[]
 for cc in [base,tip]:
  q=subprocess.run(['git','rev-parse',cc+':'+obj['path']],cwd=r,text=True,capture_output=True);vals.append(q.stdout.strip() if q.returncode==0 else None)
 assert vals[0]==vals[1];obj.update(base_tree=vals[0],candidate_tree=vals[1],equal=True)
(hw/'base-tree-integrity.json').write_text(json.dumps(integrity,indent=2)+'\n')
# Actual new revision process chronology includes both retained technical checkpoint and final repair.
ev=[json.loads(x) for x in (w/'logs/owned-processes.jsonl').read_text().splitlines()];launch=[x for x in ev if x['event']=='launch'];exits=[x for x in ev if x['event']=='exit'];complete=[x for x in ev if x['event']=='asset_lifecycle_complete'];active=None
for e in ev:
 if e['event']=='launch':assert active is None;active=e['owned_pid']
 elif e['event']=='exit':assert active==e['owned_pid'];assert not e['owned_process_group_remaining'];active=None
assert active is None and len(launch)==len(exits) and all(x['returncode']==0 for x in exits)
repairserial=dict(kind='single-asset-targeted-repair-owned-chronology',asset_id='aa-lava-front',revision='r002',candidate_commit=tip,launch_count=len(launch),matching_exits=len(exits),nonzero_owned_exit_count=0,prelaunch_wrapper_nonzero_count=1,prelaunch_failure=rec['targeted_repair']['prelaunch_failure'],technical_checkpoint_complete_events=len(complete),interpretation='First complete event is retained technical checkpoint27a5..., not a visual acceptance; lifecycle was explicitly reopened for the same mandatory shoulder correction and finished again after fresh evidence.',overlap_count=0,all_owned_process_groups_exited=True,ledger_path=str((w/'logs/owned-processes.jsonl').relative_to(r)),ledger_sha256=sha(w/'logs/owned-processes.jsonl'))
(hw/'targeted-repair-serial.json').write_text(json.dumps(repairserial,indent=2)+'\n');serial=json.loads((hist/'serial-execution-summary.json').read_text());serial['historical_r001_summary']=dict(path='history/r001/serial-execution-summary.json',sha256=sha(hist/'serial-execution-summary.json'));serial['targeted_repair']=dict(path='targeted-repair-serial.json',sha256=sha(hw/'targeted-repair-serial.json'));serial['top_level_launch_count']+=len(launch);serial['prelaunch_wrapper_nonzero_count']=1;serial['historical_r001_assets']=serial.pop('assets');assert max(x['last_exit'] for x in serial['historical_r001_assets'])<launch[0]['at'];serial['current_candidates']=[dict(asset_id=x['asset_id'],commit=x['commit']) for x in current];serial['asset_lifecycle_order']='Original batch39 serial lifecycle is preserved historically; only Aa r002 was reopened after Batch41 completed. No other model was rebuilt.';serial['final_handoff_jsonl_sha256']=sha(hw/'final-handoff.jsonl');(hw/'serial-execution-summary.json').write_text(json.dumps(serial,indent=2)+'\n')
(hw/'attempts-summary.json').write_text(json.dumps(dict(batch_id='batch-39',source_warnings=sum(len(x['source_warnings']) for x in current),nonzero_owned_exits=0,prelaunch_wrapper_nonzero_exits=1,repair_retained=rec['iterations_retained'],prior_r001_attempts=dict(path='history/r001/attempts-summary.json',sha256=sha(hist/'attempts-summary.json')),limit='Prototype technical success is not visual acceptance. Both r001 and the first r002 complete technical checkpoint remain preserved; final Aa target recheck only.'),indent=2)+'\n')
shutil.copy(Path(__file__),hw/'execution-aa-r002-handoff.py')
scope=json.loads((hist/'scope.json').read_text());scope['final_handoff_jsonl_sha256']=sha(hw/'final-handoff.jsonl');scope['serial_execution_summary_sha256']=sha(hw/'serial-execution-summary.json');scope['targeted_repair']=rec['targeted_repair']
for row in scope['assets']:
 if row['asset_id']=='aa-lava-front':row.update(branch=rec['branch'],remote_tip=tip,worktree=rec['worktree'],changed_prefixes=rec['scope']['changed_prefixes'],changed_path_count=len(rec['scope']['changed_paths']),changed_paths_sha256=hashlib.sha256(('\n'.join(rec['scope']['changed_paths'])+'\n').encode()).hexdigest())
scope['supporting_reports']={name:sha(hw/name) for name in ['base-tree-integrity.json','attempts-summary.json','targeted-repair-serial.json','execution-aa-r002-handoff.py']};(hw/'scope.json').write_text(json.dumps(scope,indent=2)+'\n')
text=f'''# Batch39 — targeted Aa r002 repair handoff

Original independent review `{qa}` identified only Aa lava front as MUST FIX. Clavagella, copper and Nereites content PASS is preserved at the original source commits/hashes; their JSONL lines remain byte-for-byte unchanged. No second full-batch review or maker-signed repair PASS. Parent coordinates only the original Aa mandatory difference check. Candidate profile validity/compatibility remains separate from approval and publication.

Aa branch `{rec['branch']}` @ `{tip}`; worktree `{r}`; candidate `{rec['candidate_dir']}`. GLB SHA256 `{rec['glb_sha256']}`, {rec['glb_bytes']} bytes, {rec['triangles']} triangles. The original r001 source `{old_source}`, GLB `{oldaa['glb_sha256']}`, and complete work/candidate Git trees are unchanged in the new branch. Original handoff `{old_handoff}` and files are preserved under `history/r001/`.

The rectangular plinth and the first r002 residual outward perimeter shoulder are replaced by an irregular continuous core recessed under unequal clinker. Outer rubble is grounded/partially embedded across the natural front. Nominal1.2m representative landscape class, palette-only materials, generic Aa scope and original facets/research-only packs remain; no event/site, smoke/fire/water or simulation added. Complete checkpoint27a5cfe8e686834c9f35e74e67d6784213f4a155 is retained as a technically successful but visually insufficient prototype, not acceptance.

All final exact-hash editable Blend, generator/config/dependency hashes, bilingual metadata, real textual source ledger, transparent cover, fixed8/zero-turntable, actual GLB runtime near/9 copies, gray diagnostic, source reopening/export consistency/direct unit/root/normals/closed-volume measurements, two fresh semantic rebuilds and Khronos/project/profile reports are supplied for Aa r002. Original frozen inputs/reference bytes are unchanged; supplementary NPS Stop3 text was actually read by parent, no source pixels/media copied. Dynamic clipping/nonzero actual runtime pixels verified. Khronos/GLB/source warnings for revised Aa: zero. Existing intentional smooth warnings for the other models remain {sum(len(x['source_warnings']) for x in current)} total. Software WebGL is functional evidence only.

Profile compatibility passes, candidate record valid=true, approved_for_brief=false. Actual legacy-license and require-approved failures remain. One preparation wrapper SyntaxError exit1 occurred before any owned child launch, retained separately. New r002 has {len(launch)} actual owned jobs, zero overlap/owned nonzero exits and all groups gone; the first technical lifecycle completion was explicitly reopened for the same mandatory repair. Historical batch39 {serial['top_level_launch_count']-len(launch)} jobs plus this repair total {serial['top_level_launch_count']}, with no chronological overlap. `targeted-repair-serial.json`, `serial-execution-summary.json`, `attempts-summary.json`, `base-tree-integrity.json` and `scope.json` provide exact audit bindings. No shared helpers/CI/site/policies, other models or frozen Batch41 changed; no merge/Drive/force/publication.

`final-handoff.jsonl` remains exactly four objects, {sum(len(x['artifacts']) for x in current)} artifact pins. All current remote tips and pins independently recomputed by this script; unaffected records retain their exact original bytes. Parent must evaluate the revised Aa hash, never reuse its r001/first-r002 visual verdict as PASS.
'''
(hw/'HANDOFF.md').write_text(text);(hw/'README.md').write_text('# Batch39 targeted handoff\n\nOnly Aa r002 changed after the original one-round QA. See [HANDOFF.md](HANDOFF.md), exact four-source [final-handoff.jsonl](final-handoff.jsonl) and [scope.json](scope.json). Original handoff and reports remain in history/r001/. Original execution-final_handoff.py, execution-handoff_summary.py and execution-final_integrity.py are retained historical r001 tools; current rebinding is execution-aa-r002-handoff.py. The other three JSONL records/models are unchanged. Targeted Aa review is pending parent; no maker approval or merge.\n')
for name in ['final-handoff.jsonl','scope.json','serial-execution-summary.json']:print(name,sha(hw/name))
print('Aa',tip,rec['glb_sha256'],rec['glb_bytes'],rec['triangles'],'PINS',sum(len(x['artifacts']) for x in current),'JOBS',serial['top_level_launch_count'])
