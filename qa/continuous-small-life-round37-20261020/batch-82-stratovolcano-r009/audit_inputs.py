import pathlib,json,hashlib,sys,subprocess,datetime,ast,math,copy
from PIL import Image,ImageChops
O=pathlib.Path('/workspace/shared/lowpoly-batch82-stratovolcano-r009-independent-qa-20261020');R=pathlib.Path('/workspace/shared/lowpoly-batch82-stratovolcano-repair-20261020');B=R/'production/batch82-stratovolcano-repair';P=B/'stratovolcano/r009';OLD=pathlib.Path('/workspace/shared/lowpoly-batch82-20261020');F=OLD/'production/small-life-batch82/assets/stratovolcano/r001';PREV=F.with_name('r006')
sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from check_reproducibility import compare_rebuild
from validate_candidate import validate_candidate
from qa_glb import audit_glb,read_glb,accessor_values
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
J=lambda p:json.loads(pathlib.Path(p).read_text())
def save(name,d): (O/name).write_text(json.dumps(d,indent=2)+'\n')
errors=[];checks=[]
def check(label,ok,details=None):
 checks.append({'check':label,'pass':bool(ok),'details':details})
 if not ok: errors.append(label)
h=J('/workspace/shared/lowpoly-batch82-stratovolcano-repair-handoff-20261020.json')
check('external handoff exact',sha('/workspace/shared/lowpoly-batch82-stratovolcano-repair-handoff-20261020.json')=='7690dc2ea15519443d0b081acac3bf1d866e5c48840550e6aef908677102c28f')
check('repo handoff exact',sha(B/'handoff.json')==h['handoff_sha256'])
git=lambda *a:subprocess.check_output(['git','-C',str(R),*a],text=True).strip()
check('immutable commit',git('rev-parse','HEAD')==h['local_commit'],git('rev-parse','HEAD'))
check('parent uploaded lean82',git('rev-parse','HEAD^')==h['base_parent'],git('rev-parse','HEAD^'))
check('clean source checkout',git('status','--porcelain')=='',git('status','--porcelain'))
roles={'glb':'model.glb','source':'source.blend','generator':'generator.py','config':'build-config.json','brief':'candidate-brief.json','references':'references.json','proof':'proof-final/render-manifest.json','sheet':'contact-sheet.png','repair_freeze':'repair-freeze.json'}
for k,f in roles.items():check('handoff '+k,sha(P/f)==h['hashes'][k],{'path':str(P/f),'actual':sha(P/f)})
freeze=J(F/'modeling-freeze.json')
for f,w in freeze['files'].items():check('original freeze '+f,sha(F/f)==w)
for inp in J(B/'original-byte-identity.json')['inputs']:check('original untouched '+inp['path'],sha(inp['path'])==inp['sha256'])
check('original QA snapshot',sha(B/'original-independent-qa.report.json')==h['original_qa_sha256'])
for f in ['brief.json','references.json','concept-original.png','concept-generation.json','concept-prompt.txt']:check('unchanged original '+f,sha(P/f)==sha(F/f))
check('original freeze copied intact',sha(P/'original-modeling-freeze.json')==sha(F/'modeling-freeze.json'))
der=J(P/'candidate-brief.json');orig=J(F/'brief.json');diff=[k for k in orig if orig[k]!=der[k]]
check('derived brief only delivery closure',diff==['required_deliverables'],diff)
check('derived atomic criteria unchanged',der['criteria']==orig['criteria'])
check('palette unchanged',J(P/'build-config.json')['palette']==J(PREV/'build-config.json')['palette'])
check('nominal scale unchanged',J(P/'build-config.json')['nominal_dimensions_blender_xyz_m']==J(F/'build-config.json')['nominal_dimensions_blender_xyz_m'])
check('renderer code identical',sha(B/'render-fixed8.py')==sha(OLD/'production/small-life-batch82/render-fixed8.py'))
dep=J(P/'build-dependencies.json')
for f,w in dep['files'].items():check('dependency '+f,sha(R/f)==w)
check('blender binary',sha(dep['blender']['path'])==dep['blender']['sha256'])
for k,v in [('three','three_package_sha256'),('gltf-validator','gltf_validator_package_sha256')]:check(k+' dependency',sha(pathlib.Path(dep['runtime_dependency']['read_only'])/k/'package.json')==dep['runtime_dependency'][v])
# Final subject fixed before actual render process, no timing inferred from filesystem.
pre=J(P/'preproof-binding.json');man=J(P/'proof-final/render-manifest.json');rc=J(P/'proof-final/render-config.json');life=[json.loads(x) for x in (B/'lifecycle.jsonl').read_text().splitlines()]
render=next(x for x in life if x['stage']=='proof-final-r009')
check('preproof before actual render',pre['fixed_at']<render['started_at']<man['created_at']<=render['ended_at'],{'binding':pre['fixed_at'],'process':render,'manifest_created':man['created_at']})
check('proof exact subject',all(man['subject'][k]==pre[k] for k in ['glb_sha256','brief_sha256','references_sha256']))
check('proof renderer config hash',sha(P/'proof-final/render-config.json')==man['config_sha256'])
check('renderer current helper binding',rc['renderer_sha256']==sha(B/'render-fixed8.py') and rc['helper_sha256']==sha(R/'scripts/asset_common.py'))
check('proof actual log renders',all('/proof-final/'+f['path'] in (B/'proof-final-r009.log').read_text() for f in man['frames']))
sheet=Image.open(P/'contact-sheet.png').convert('RGBA');sheetchecks=[]
for i,f in enumerate(man['frames']):
 im=Image.open(P/'proof-final'/f['path']).convert('RGBA');crop=sheet.crop(((i%4)*512,(i//4)*512,(i%4+1)*512,(i//4+1)*512));same=ImageChops.difference(im,crop).getbbox() is None
 check('proof '+f['id'],sha(P/'proof-final'/f['path'])==f['sha256'] and im.size==(512,512))
 sheetchecks.append({'view':f['id'],'exact_pixels':same});check('sheet '+f['id'],same)
check('eight views', [x['view'] for x in man['frames']]==orig['required_views'])
check('sheet dimensions',sheet.size==(2048,1024),sheet.size)
# Original eight frames still match original immutable QA evidence.
oldqa=J('/workspace/shared/lowpoly-batch82-independent-qa-20261020/independent-qa.report.json'); oldasset=next(x for x in oldqa['assets'] if x['asset_id']=='stratovolcano')
# field name is discovered instead of assuming report schema.
for value in oldasset.values():
 if isinstance(value,list):
  for ent in value:
   if isinstance(ent,dict) and ent.get('path','').startswith('production/') and ent.get('sha256'): check('original QA frame '+ent.get('view',''),sha(OLD/ent['path'])==ent['sha256'])
provenance=[]
for rf in sorted(B.glob('raw/rebuild-runs/build/**/result.json')):
 result=J(rf);request=J(rf.with_name('request.json'));record={'job_id':result['job_id'],'pid':result['pid'],'started_at':result['started_at'],'finished_at':result['finished_at'],'request':str(rf.with_name('request.json')),'request_sha256':sha(rf.with_name('request.json')),'result':str(rf),'result_sha256':sha(rf),'outputs':[]}
 for name,data in result['outputs'].items():
  f=rf.parent/'outputs'/name;ok=sha(f)==data['sha256'] and f.stat().st_size==data['bytes'];check(result['job_id']+' output '+name,ok);record['outputs'].append({'path':str(f),'sha256':sha(f),'bytes':f.stat().st_size})
 for name,data in request['identity']['inputs'].items():check(result['job_id']+' input '+name,sha(data['path'])==data['sha256'])
 check(result['job_id']+' chronology',request['created_at']<=result['started_at']<result['finished_at'] and result['wall_seconds']>0)
 check(result['job_id']+' actual stdout',h['hashes']['glb'] in rf.with_name('stdout.log').read_text() and 'Blender' in rf.with_name('stdout.log').read_text())
 report=compare_rebuild(P/'model.glb',rf.parent/'outputs/model.glb',P/'generator.py',P/'build-config.json',rf.with_name('request.json'),rf,'model.glb',R)
 check(result['job_id']+' independent comparison',report['status']=='pass' and report['byte_identical'] and report['semantic_match'],report['status']);save(result['job_id']+'-fresh-comparison.json',report);provenance.append(record)
check('two distinct real rebuilds',len(provenance)==2 and len({x['pid'] for x in provenance})==2 and set(x['pid'] for x in provenance)=={120,147})
for rev,status in [('r007','rejected'),('r008','not_selected')]:
 d=J(P.with_name(rev)/'attempt-disposition.json');check('preserved '+rev+' disposition',d['status']==status and sha(P.with_name(rev)/'model.glb')==d['glb_sha256'],d)
check('r007 remains over budget',(P.with_name('r007')/'model.glb').stat().st_size>orig['geometry_policy']['max_glb_bytes'])
profile=validate_candidate(P/'candidate.json',root=R,validation_profile='static-stylized-v1',profile_contract=P/'profile-contract.json');save('candidate-profile-fresh.json',profile);check('fresh project candidate validation',profile['valid'],profile)
save('provenance-audit.json',{'two_real_rebuilds':provenance,'limitation':'Retained request/result/logs are execution attestations, independently checked against exact actual outputs; not cryptographic process proof.'})
save('immutable-input-audit.json',{'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'errors':errors,'checks':checks,'originals_unchanged':True,'read_only_source':True})
print('CHECKS',len(checks),'ERRORS',errors)
