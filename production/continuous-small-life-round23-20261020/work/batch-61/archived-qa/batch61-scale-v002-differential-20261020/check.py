import json, hashlib, pathlib, subprocess, sys
from collections import Counter
REPO=pathlib.Path('/tmp/lowpoly-batch61-20261020')
OUT=pathlib.Path('/tmp/lowpoly-round23-qa61-scale-v002')
BASE='faa9090270732d1c770a807607fe5e34db8908eb'
OLD_HEAD='f1737e4f00dfc5c1817084ecb31763320ec2a163'
NEW_HEAD='c15ccbb5bc0fa0890fad5b68856eb653645e571d'
work='production/continuous-small-life-round23-20261020/work/batch-61/metadata-scale-v002'
assets={
'daemonelix-helical-burrow': {'rev':'r002','old_brief':'2fcfd328842918ca9e1bc75bbb542692960c9a1f0644eb678bd8cca5a5056896','new_brief':'721ad77bfd1600cadda06b178a571f439c957c00f19ba1263d307f9e40449ac4','old_candidate':'70af6d4c57a4335632e364b1ff5380bdaeebc431d949c963443320be96570a67','glb':'c415fbe405e75ac182bb39512ea33b43f81d574723263f04378422fb0221aa82','source':'802c13dc3117cadd7748201ca2dc5fce4b3a50cc60ab5791e0042ba463ea6248','refs':'9f76d189a6c74522a08af4c200898e30591f3cd7960bf3e44212b912a52ac075','generator':'4776e0b89f0f1049df60983fa8c82d78018cdd08c5471e4dcbb0de2bafd1a70f','config':'15b9358a2862c867b2d9cc4fa83c4a4ce9fd8437a319d8b0ff7c3c94d15f6cf3','frozen':'7ea2a8eb5d48a96ac7ed975c4cbd2ff796d422608fd5a18262732027c4303262','corrected':'Illustrative exposed fossil-burrow cast teaching-asset envelope only. Declared nominal Blender XYZ envelope is 1.7 x 1.0 x 2.0 metres; actual mesh bounds are reported separately. Not a measured fossil-burrow specimen dimension.'},
'mesa': {'rev':'r002','old_brief':'4bf4e45bce74a19ba20ef2d8f658d08358c702ad0bb449055732434489f346cf','new_brief':'63de5d1f262ba10b471dba0587139685a141ca2105c5efdf77c8eee5a69798cd','old_candidate':'95e78e305ee143611877cf993594b3f6d3553055418f98f8f60bdd8e1163027d','glb':'399e9fb78b225cd808563598485888ea343b568e8bc2cac8b427939fc94f1cad','source':'716288207373eb8d1b4ff123bc9bebda485d1b015d3e85f09b5c5b94f053f57d','refs':'ad88334969361d198442598087096ab275a8c2e3aa672c85233dbb8c85e37df4','generator':'4776e0b89f0f1049df60983fa8c82d78018cdd08c5471e4dcbb0de2bafd1a70f','config':'f3b3fde69b10ad042f18c52091675ddc28ba3f83eabfc91247149aa728d69b65','frozen':'bfa454dc1f79702ff23ed7a58359673bd40cd9ce725bc390897042069e5d167e','corrected':'Illustrative broad flat-capped geological-form teaching-asset envelope only. Declared nominal Blender XYZ envelope is 600 x 450 x 180 metres; actual mesh bounds are reported separately. Not a measured specimen or named-site dimension.'},
'drumlin': {'rev':'r002','old_brief':'12ddf48322e3b644df06d7df62a15a4272ed1a7bd5df680fe6e8ed2ed169ad6a','new_brief':'106e2bbd77cd9e7c69be89311af1aebb4dad808b1e25a40da0a98e3fded3da43','old_candidate':'d0399bf4f325b36bb044fb3ea915817cf324e3b3f046113d6f2fcc24d5c0dff0','glb':'317dee38ec731d1939985a61fd431238a188b5be34dfcc717dafe23dc4bd7534','source':'ee0abc1e2a6860fb6624c0bf150f4c29f0287ab306539c5a2ad75e6d241a8fea','refs':'1c33853bc5d0e7f7c0dc858458b2df334d3acfe89996c2a98dd84ca62591659e','generator':'4776e0b89f0f1049df60983fa8c82d78018cdd08c5471e4dcbb0de2bafd1a70f','config':'e48252f277d3ab3499026d1b970a8657b71639531ac44779824dea7b65adaba2','frozen':'221c2e543ae506e718d7ea4602254ffe4ddfb05ddebcf9850048b6ad667ada40','corrected':'Illustrative low rounded elongated glacial-landform teaching-asset envelope only. Declared nominal Blender XYZ envelope is 150 x 450 x 35 metres; actual mesh bounds are reported separately. Not a measured specimen or named-site dimension.'}}

def sha_b(b):return hashlib.sha256(b).hexdigest()
def sha_file(p):return sha_b(p.read_bytes())
def git(*args,check=True):return subprocess.run(['git','-C',str(REPO),*args],check=check,stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.decode().strip()
def gitblob(rev,path):return subprocess.run(['git','-C',str(REPO),'show',f'{rev}:{path}'],check=True,stdout=subprocess.PIPE).stdout
def jread(p):return json.loads(p.read_text())
def deep_diff(a,b,path=''):
 if type(a)!=type(b):return [path or '/']
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append(f'{path}/{k}')
   else:out+=deep_diff(a[k],b[k],f'{path}/{k}')
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [path+'/length']
  return sum((deep_diff(x,y,f'{path}/{i}') for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [path]

assert git('rev-parse','HEAD')==NEW_HEAD
assert git('status','--porcelain')==''
changed=git('diff','--name-status',f'{BASE}..{NEW_HEAD}').splitlines()
assert len(changed)==26
assert all(line.startswith('A\t') for line in changed)
assert git('rev-parse','HEAD^')==BASE
handoffpath=f'{work}/handoff-scale-v002.json'
handoff_blob=gitblob(NEW_HEAD,handoffpath)
handoff=json.loads(handoff_blob)
assert sha_b(handoff_blob)=='0a25dc54235bcaa822ab534b58e3f7d5f039aa182b347fc7059f4efec5ffbe17'
assert handoff['baseline_commit']==BASE and handoff['original_model_head']==OLD_HEAD
assert handoff['payload_commit']=='b2ff8314140e2539c825d573fef2152584120059'
assert handoff['kind']=='focused-metadata-repair-handoff'
# validate all original byte pins from preservation manifest at baseline and current commit/worktree
pres=json.loads(gitblob(NEW_HEAD,f'{work}/preserved-original-files.json'))
preserved=pres['sha256']
assert pres['baseline_commit']==BASE
pres_fail=[]
for path,expected in preserved.items():
 old=gitblob(BASE,path)
 now=gitblob(NEW_HEAD,path)
 if sha_b(old)!=expected or sha_b(now)!=expected:pres_fail.append(path)
assert not pres_fail, pres_fail[:20]
# original QA explicitly matches archive pins
for slot in ('original_qa','original_qa_results'):
 item=handoff[slot]; b=gitblob(NEW_HEAD,item['path']); assert sha_b(b)==item['sha256']
# Source model HEAD is immutable as source of four pins, and candidate files were unaffected between original model and QA archive.
assets_root='assets/candidates/continuous-small-life-round23-20261020/batch-61'
models=[]
for name,info in assets.items():
 p=f'{assets_root}/{name}/{info["rev"]}'
 for fn,expected in [('model.glb',info['glb']),('source.blend',info['source'])]:
  assert sha_b(gitblob(OLD_HEAD,f'{p}/{fn}'))==expected
  assert sha_b(gitblob(BASE,f'{p}/{fn}'))==expected
  assert sha_b(gitblob(NEW_HEAD,f'{p}/{fn}'))==expected
 oldp=f'{p}/candidate-brief.json'; newp=f'{p}/candidate-brief-scale-v002.json'
 oldbytes=gitblob(BASE,oldp); newbytes=gitblob(NEW_HEAD,newp)
 assert sha_b(oldbytes)==info['old_brief'] and sha_b(newbytes)==info['new_brief']
 oldbrief=json.loads(oldbytes); newbrief=json.loads(newbytes)
 assert deep_diff(oldbrief,newbrief)==['/scale_note']
 assert oldbrief['scale_note']=='Illustrative nominal envelope; actual measured bounds reported separately. Animal body nominal17mm excludes antenna; pose appendages extend bounds.'
 assert newbrief['scale_note']==info['corrected']
 assert newbrief['nominal_dimensions_blender_xyz_m']==oldbrief['nominal_dimensions_blender_xyz_m']
 assert newbrief['purpose']==oldbrief['purpose'] and newbrief['claim_scope']==oldbrief['claim_scope']
 assert newbrief['packaging_adapter']['frozen_design_brief_sha256']==info['frozen']
 assert sha_b(gitblob(NEW_HEAD,f'{p}/brief.json'))==info['frozen']
 assert json.loads(gitblob(NEW_HEAD,f'{p}/modeling-freeze.json'))['brief_sha256']==info['frozen'] # original modeling freeze binds original design brief
 correction=json.loads(gitblob(NEW_HEAD,f'{p}/scale-note-correction-v002.json'))
 assert correction['changed_json_pointer']=='/scale_note'
 assert correction['original_delivery_brief']['sha256']==info['old_brief']
 assert correction['original_frozen_brief']['sha256']==info['frozen']
 assert correction['original_modeling_freeze']['sha256']==sha_b(gitblob(BASE,f'{p}/modeling-freeze.json'))
 assert correction['original_value']==oldbrief['scale_note'] and correction['corrected_value']==newbrief['scale_note']
 assert correction['corrected_delivery_brief']['sha256']==info['new_brief']
 assert correction['declared_nominal_blender_xyz_envelope_m']==newbrief['nominal_dimensions_blender_xyz_m']
 assert 'measured fossil/site dimensions' in correction['dimension_distinction']
 assert 'no new ImageGen, rebuild, rerender or runtime test' in correction['dependency_impact']
 # explicit retained all geometry/build/refs and original render manifest pins in correction
 for k,fn,expect in [('glb','model.glb',info['glb']),('source','source.blend',info['source']),('generator','generator.py',info['generator']),('config','build-config.json',info['config']),('references','references.json',info['refs'])]:
  assert correction['unchanged_artifacts'][k]['sha256']==expect
  assert sha_b(gitblob(NEW_HEAD,f'{p}/{fn}'))==expect
 oldcand_bytes=gitblob(BASE,f'{p}/candidate.json'); newcand_bytes=gitblob(NEW_HEAD,f'{p}/candidate-scale-v002.json')
 assert sha_b(oldcand_bytes)==info['old_candidate']
 oldcand=json.loads(oldcand_bytes); cand=json.loads(newcand_bytes)
 assert cand['metadata_revision']=='scale-note-v002'
 assert cand['metadata_predecessor']['sha256']==info['old_candidate']
 assert cand['metadata_correction']['sha256']==correction['corrected_delivery_brief']['sha256'] if False else True # pin is correction record below
 corr_rel=f'{p}/scale-note-correction-v002.json'; assert cand['metadata_correction']['path']==corr_rel and cand['metadata_correction']['sha256']==sha_b(gitblob(NEW_HEAD,corr_rel))
 assert cand['artifacts']['glb']['sha256']==info['glb'] and cand['artifacts']['source']['sha256']==info['source']
 assert cand['artifacts']['brief']['path']==newp and cand['artifacts']['brief']['sha256']==info['new_brief']
 assert cand['artifacts']['references']['sha256']==info['refs'] and cand['artifacts']['generator']['sha256']==info['generator'] and cand['artifacts']['config']['sha256']==info['config']
 assert all(s['status']=='unknown' for s in cand['stages'].values())
 assert cand['approval']['status']=='pending'
 assert any(b['id']=='pending-metadata-differential' and b['status']=='open' for b in cand['blockers'])
 assert any(b['id']=='pending-runtime-render' and b['status']=='open' for b in cand['blockers'])
 profile=json.loads(gitblob(NEW_HEAD,f'{p}/profile-contract-scale-v002.json'))
 assert profile['validation_profile']=='static-stylized-v1' and profile['rule_version']=='2026-10-18.1'
 assert profile['candidate']['path']==f'{p}/candidate-scale-v002.json' and profile['candidate']['sha256']==sha_b(newcand_bytes)
 assert profile['publication_authority']=='separate'
 validation=json.loads(gitblob(NEW_HEAD,f'{p}/candidate-validation-scale-v002.json'))
 assert validation['valid'] is True and validation['approved_for_brief'] is False and validation['approval_status']=='pending'
 assert validation['subject']['glb_sha256']==info['glb'] and validation['subject']['brief_sha256']==info['new_brief'] and validation['subject']['references_sha256']==info['refs']
 assert validation['profile_contract_status']=='pass'
 assert validation['profile_contract']['path']==f'{p}/profile-contract-scale-v002.json' and validation['profile_contract']['sha256']==sha_b(gitblob(NEW_HEAD,f'{p}/profile-contract-scale-v002.json'))
 # carried render manifest: old subject and exact frame records/times/config/GLB preserved, no rerender claim
 ompath=f'{p}/proof-final/render-manifest.json'; nmpath=f'{p}/proof-final/render-manifest-scale-v002.json'
 oldmanifest=json.loads(gitblob(BASE,ompath)); newmanifest=json.loads(gitblob(NEW_HEAD,nmpath))
 carr=newmanifest['evidence_carry_forward']
 assert carr['kind']=='metadata-only-evidence-adapter-not-a-new-render'
 assert carr['original_render_manifest']['sha256']==sha_b(gitblob(BASE,ompath))
 assert carr['original_render_subject']['brief_sha256']==info['old_brief']
 assert carr['original_render_subject']['glb_sha256']==info['glb']
 assert 'does not claim original rendering tested the later correction' in carr['changed_statement']
 assert carr['requires_differential_specification_review'] is True
 assert newmanifest['created_at']==oldmanifest['created_at']
 assert {k:v for k,v in newmanifest['subject'].items() if k!='brief_sha256'}=={k:v for k,v in oldmanifest['subject'].items() if k!='brief_sha256'}
 top_subject_changed_brief=(oldmanifest['subject']['brief_sha256'],newmanifest['subject']['brief_sha256'])
 assert newmanifest['subject']['brief_sha256']==info['new_brief'] and oldmanifest['subject']['brief_sha256']==info['old_brief']
 assert newmanifest['source_glb_sha256']==oldmanifest['source_glb_sha256']==info['glb']
 assert newmanifest['config_sha256']==oldmanifest['config_sha256']
 assert newmanifest['render_config']==oldmanifest['render_config']
 assert newmanifest['frames']==oldmanifest['frames']
 for fr in oldmanifest['frames']:
  pixpath=f'{p}/proof-final/{fr["path"]}'
  assert sha_b(gitblob(BASE,pixpath))==fr['sha256']
  assert sha_b(gitblob(NEW_HEAD,pixpath))==fr['sha256']
 # evidence record itself explicitly references carry-forward manifest; new brief hash doesn't erase original manifest subject.
 ev=cand['evidence'][0]
 assert ev['path']==nmpath and ev['sha256']==sha_b(gitblob(NEW_HEAD,nmpath))
 assert ev['subject']['brief_sha256']==info['new_brief'] and ev['subject']['glb_sha256']==info['glb']
 models.append({'asset_id':name,'geometry_revision':info['rev'],'metadata_revision':'scale-note-v002','old_brief_sha256':info['old_brief'],'corrected_brief_sha256':info['new_brief'],'carry_forward_manifest_top_level_brief_sha256':info['new_brief'],'original_render_subject_brief_sha256':info['old_brief'],'remaining_defect':'top-level render subject claims corrected v002 brief hash although original images were rendered for old brief; preserve old subject and bind v002 separately','old_candidate_sha256':info['old_candidate'],'corrected_note':newbrief['scale_note'],'nominal_dimensions_blender_xyz_m':newbrief['nominal_dimensions_blender_xyz_m'],'original_frozen_brief_sha256':info['frozen'],'glb_sha256':info['glb'],'source_blend_sha256':info['source'],'refs_sha256':info['refs'],'generator_sha256':info['generator'],'config_sha256':info['config'],'candidate_record_valid':True,'approved_for_brief':False,'approval':'pending','visual_manifest':'original subject retained only in evidence_carry_forward; top-level subject incorrectly uses corrected brief hash; exact old timestamps/frame hashes retained; no rerender disclosed','candidate_statuses':'all unknown pending independent review'})
# Pseudopulex artifacts and historical QA report remain exactly same in original result
pseu=f'{assets_root}/pseudopulex/r003'
pseu_pins={'model.glb':'75f6799431a7bf6037881c78d12e7cf731670fcb2fdea82b66576dadc8cdf99c','source.blend':'e572b15e3efffc4331f3b865c4fe74fb37d29632893b459904cc87fc233b8415','candidate-brief.json':'3ee0ecc2d4a18b634c4d94eddea7fa985ce458c91538749388d230695f8fbe67'}
for fn,h in pseu_pins.items():
 assert sha_b(gitblob(OLD_HEAD,f'{pseu}/{fn}'))==h==sha_b(gitblob(BASE,f'{pseu}/{fn}'))==sha_b(gitblob(NEW_HEAD,f'{pseu}/{fn}'))
# global selection points unmodified Pseudopulex metadata and new candidate paths for only three.
selection=json.loads(gitblob(NEW_HEAD,f'{work}/final-selection-scale-v002.json'))
assert len(selection)==4
assert selection[0]['asset_id']=='pseudopulex' and selection[0]['metadata_repair']=='not affected; no file touched'
for row in selection[1:]:
 n=row['asset_id']; p=f'{assets_root}/{n}/r002'
 assert row['candidate_record']==f'{p}/candidate-scale-v002.json' and row['delivery_brief']==f'{p}/candidate-brief-scale-v002.json'
# additive Git diff and preservation manifest coverage
result={
 'schema_version':1,'kind':'batch61_scale_metadata_differential_review','review_date_utc':'2026-10-20','review_commit':NEW_HEAD,'baseline_commit':BASE,'original_model_head':OLD_HEAD,'worktree_clean':True,
 'outcome':'Scale-note content correction is adequate, but three carry-forward render manifests still bind corrected v002 brief hash as top-level subject, not the original rendered brief. Keep all three BLOCKED until that subject binding is made unambiguously historical. No full QA or formal approval.',
 'diff':{'additions':len(changed),'modified':0,'deleted':0,'all_original_hashes_verified':len(preserved),'original_hash_failures':0,'all_original_model_and_QA_files_preserved':True},
 'handoff_sha256':sha_b(handoff_blob),'original_qa_files_preserved':True,'metadata_record_checks':'pass','brief_differential':'exactly /scale_note differs for each corrected delivery brief','candidate_profile_binding':'all three new candidate/profile/validation records bind corrected brief and unchanged exact asset pins; candidate record gates valid but not approved and stages remain unknown/pending','remaining_defect':'Each new render manifest proof-final/render-manifest-scale-v002.json changed top-level subject.brief_sha256 to the v002 corrected brief hash. That is not the old render subject; old hash survives only at evidence_carry_forward.original_render_subject. Corrected brief must be bound separately while original subject remains exact. This is a scope blocker, not a geometry or image-quality issue.','render_evidence':'all three carry-forward manifests preserve timestamps, frame hashes, config and original subject under evidence_carry_forward.original_render_subject, and disclose no rerender. DEFECT: top-level subject.brief_sha256 is changed from original v001 hash to corrected v002 hash, so manifest does not retain exact original subject and may imply the old pixels were rendered against v002.','pseudopulex':'unchanged at exact original GLB, Blend and delivery brief hashes; prior ACCEPT_BOUNDED finding is carried forward without re-review','assets':models,
 'limitations':['This was only a metadata differential, not a new visual/technical/factual or runtime rerun. Earlier positive checks carry forward only because the original files and pinned GLBs/Blends match baseline.','GPU, composed scene and formal user/publication approval remain unknown/not run.','Original source_binding_note is inherited historical v001 packaging prose; the carry-forward manifest discloses no rerender. However, its top-level subject.brief_sha256 is rewritten to v002, which must be corrected before the evidence can be treated as an unambiguous historical carry-forward.']
}
(OUT/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
log=[
 f'HEAD={NEW_HEAD}',f'BASELINE={BASE}',f'ORIGINAL_MODEL_HEAD={OLD_HEAD}',f'WORKTREE_CLEAN=true',f'GIT_DIFF_ADDITIONS={len(changed)} MODIFIED=0 DELETED=0',f'PRESERVED_BASELINE_FILES_CHECKED={len(preserved)} FAILURES=0',f'HANDOFF_SHA256={sha_b(handoff_blob)}',f'ORIGINAL_QA_SHA256={handoff["original_qa"]["sha256"]}',f'ORIGINAL_QA_RESULTS_SHA256={handoff["original_qa_results"]["sha256"]}',f'ASSET_DIFFERENTIAL_CHECKS=3 PASS',f'PSEUDO_PULEX_PIN_CHECKS=3 PASS',f'FINAL_SELECTION_CHECK=PASS',
 'Render proof: each carry-forward manifest exactly retains original subject and frame list including file hashes, dimensions, camera angles, timestamps, plus original GLB/config hashes; explicit evidence_carry_forward says this is not a new render and not validation of corrected dimensions.'
]
(OUT/'checks.log').write_text('\n'.join(log)+'\n')
print(json.dumps({'result':result['outcome'],'preserved_files':len(preserved),'assets':[a['asset_id'] for a in models]},indent=2))
