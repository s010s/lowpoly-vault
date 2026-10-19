# SPDX-License-Identifier: MIT
"""Read-only validation of records/models; writes only its new verification reports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, math, subprocess, sys
HERE=Path(__file__).resolve().parent; BASE=HERE.parent
REPO=next(p for p in HERE.parents if (p/'scripts/validate_candidate.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import audit_glb,read_glb
from validate_candidate import validate_candidate
from validate_concept_evidence import validate as validate_concept

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def check_desc(d):assert digest(REPO/d['path'])==d['sha256'],d
pins=load(HERE/'baseline-files.json'); handoff=load(BASE/'handoff.json')
allowed={str((BASE/name).relative_to(REPO)) for name in ('HANDOFF.md','handoff.json','freeze-manifest.json')}
allowed|={str((BASE/a/'r001/output'/a/'metadata.json').relative_to(REPO)) for a in ['sapeornis','longirostravis','dunbaria','chimerarachne']}
changed=[];unchanged=[]
for path,old in pins['files'].items():
 p=REPO/path;assert p.is_file(),path
 if digest(p)!=old['sha256']:
  assert path in allowed, 'Unexpected original-file change: '+path
  changed.append(path)
 else: unchanged.append(path)
actual_changes=subprocess.check_output(['git','diff','--name-only',pins['source_commit']],cwd=REPO,text=True).splitlines()
assert all(path in allowed for path in actual_changes),actual_changes
for n in ('HANDOFF.md','handoff.json','freeze-manifest.json'):
 assert digest(HERE/'original-records'/n)==pins['files'][(BASE/n).relative_to(REPO).as_posix()]['sha256']
results=[]
for item in handoff['assets']:
 a=item['asset_id'];assert item['revision']=='r001'; d=BASE/a/'r001'; output=d/'output'/a;glb=output/(a+'.glb');blend=output/(a+'.blend')
 m=load(output/'metadata.json');c=load(d/'candidate.json');config=load(d/'build-config.json')
 assert digest(HERE/'original-records'/(a+'-metadata.json'))==pins['files'][(output/'metadata.json').relative_to(REPO).as_posix()]['sha256']
 audit=audit_glb(glb,max_triangles=config['max_triangles'],max_materials=config['max_materials'],max_primitives=config['max_primitives']);doc,_,raw=read_glb(glb)
 assert not audit['errors'];assert m['dimensions_m']==m['dimensions']==audit['bounds_m']['size']
 assert len(m['dimensions_m'])==3 and all(math.isfinite(v) and v>0 for v in m['dimensions_m'])
 assert m['triangles']==audit['scene_triangles'];assert m['primitives']==audit['scene_primitives_estimated_base_draw_calls']
 assert m['material_count']==audit['materials'];assert m['textures']==len(doc.get('textures',[]))==0;assert m['images']==len(doc.get('images',[]))==0
 assert m['bytes']==m['glb_bytes']==len(raw);assert m['file_bytes']=={'glb':len(raw),'blend':blend.stat().st_size}
 assert m['origin']==config['mount_origin'];assert m['axis']['up']=='+Y' and m['axis']['forward']=='+Z'
 for key in ('glb','blend','preview','generator','candidate_record'):assert (REPO/m[key]).is_file(),(a,key)
 assert digest(REPO/m['preview'])==m['preview_sha256'];assert digest(REPO/m['generator'])==m['generator_sha256']
 assert m['generator']==(BASE/('generator-r001.py' if a=='sapeornis' else 'generator.py')).relative_to(REPO).as_posix()
 for entry in [*c['artifacts'].values(),*c['technical_evidence'].values()]:check_desc(entry)
 assert c['approval']['status']=='pending';assert all(s['status']=='unknown' and s['reviewer'] is None and s['reviewed_at'] is None for s in c['stages'].values())
 v=validate_candidate(d/'candidate.json',REPO);assert v['valid'] and not v['approved_for_brief'] and not v['errors']
 run=subprocess.run([sys.executable,'scripts/validate_candidate.py',str(d/'candidate.json'),'--root',str(REPO),'--require-approved','--json'],cwd=REPO,text=True,capture_output=True)
 assert run.returncode==1; denied=json.loads(run.stdout);assert denied['valid'] and not denied['approved_for_brief'] and not denied['errors']
 write(HERE/'evidence'/(a+'-require-approved-expected-failure.json'),{'command':'scripts/validate_candidate.py --require-approved --json','exit_code':run.returncode,'expected_exit_code':1,'interpretation':'Correct fail-closed rejection of formal approval; the record itself is valid.','result':denied})
 cv=validate_concept(d/'concept-evidence.json',BASE);assert cv['valid'] and cv['evidence_complete'],cv
 write(HERE/'evidence'/(a+'-concept-integrity.json'),cv)
 source=load(HERE/'evidence'/(a+'-source.json'));assert source['model_bytes_unchanged'] and not source['source_export']['errors']
 assert source['hashes_after']=={glb.name:digest(glb),blend.name:digest(blend)}
 kh=load(HERE/'evidence'/(a+'-khronos.json'));assert kh['glb_sha256']==digest(glb) and kh['report']['issues']['numErrors']==kh['report']['issues']['numWarnings']==0
 manifest=load(BASE/item['proof']['path']);assert len(manifest['frames'])==11
 assert manifest['source_glb_sha256']==manifest['subject']['glb_sha256']==digest(glb)
 assert manifest['subject']['brief_sha256']==digest(d/'brief.json') and manifest['subject']['references_sha256']==digest(d/'references.json')
 for frame in manifest['frames']:assert digest((BASE/item['proof']['path']).parent/frame['path'])==frame['sha256']
 registration=load(d/'candidate-brief.json');assert registration['preproduction_freeze_claim'] is False and registration['original_evidence_coverage']['turntable_frames']==0
 for key in ('metadata','candidate','candidate_validation','delivery_preview'):
  info=item[key];assert digest(BASE/info['path'])==info['sha256']
 results.append({'asset_id':a,'revision':'r001','candidate_record_valid':True,'candidate_formally_approved':False,'require_approved_exit':run.returncode,'model_and_original_evidence_unchanged':True,'actual_measurements_match':True,'preview_exists_and_hash_matches':True,'generator_exists_and_hash_matches':True,'original_concept_evidence_still_complete':True,'khronos_errors':0,'khronos_warnings':0,'source_export_status':source['source_export']['status'],'glb_sha256':digest(glb),'blend_sha256':digest(blend)})
qa=load(HERE/'qa-provenance.json')
for f in qa['files']:
 raw=subprocess.check_output(['git','show',qa['qa_commit']+':'+f['original_path']],cwd=REPO);check_desc(f)
 assert hashlib.sha256(raw).hexdigest()==f['sha256']
assert handoff['rejected_revision']['asset_id']=='sapeornis' and handoff['rejected_revision']['revision']=='r002'
report={'checked_at':datetime.now(timezone.utc).isoformat(),'status':'pass','source_commit':pins['source_commit'],'scope':'Delivery record integrity only; not independent/formal acceptance, hardware acceptance, release or publication.','unchanged_original_file_count':len(unchanged),'permitted_changed_original_records':changed,'all_model_generator_design_report_and_image_bytes_unchanged':True,'all_formal_stages':'unknown; no reviewer or acceptance time invented','items':results}
write(HERE/'self-check.json',report)
print(json.dumps(report,indent=2))
