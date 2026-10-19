# SPDX-License-Identifier: MIT
"""Read-only delivery check. No approval, model export, or source save."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,subprocess,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parent
REPO=next(p for p in HERE.parents if (p/'scripts/validate_candidate.py').exists());sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import audit_glb,read_glb
from validate_candidate import validate_candidate
from validate_concept_evidence import validate as validate_concept

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_commit='7c3cc658c1d10fa595e3ef7d27c6f0b17a842dd1'
selected=json.load(open(BASE/'selected-models.json'))['selected'];result=[]
for item in selected:
 slug=item['id'];d=BASE/slug/item['revision'];glb=d/(slug+'.glb');blend=d/(slug+'.blend')
 stable=[glb,blend,d/'brief.json',d/'brief.md',d/'references.json',d/'build-config.json',d/'source-metadata.json',d/'source-qa.json',d/'qa.json',d/'gltf-validator.report.json',d/'proof/render-manifest.json',d/'proof/render-config.json']
 stable.extend(BASE/n for n in ['generator.py','generator-r002.py','generator-r003.py','concept-original.png','concept-generation.json','concept-prompt.txt'])
 for file in stable:
  old=subprocess.check_output(['git','show',source_commit+':'+file.relative_to(REPO).as_posix()],cwd=REPO)
  assert digest(file)==hashlib.sha256(old).hexdigest(),file
 m=json.load(open(d/'metadata.json'));doc,_,raw=read_glb(glb);audit=audit_glb(glb,max_triangles=16000,max_materials=7,max_primitives=220)
 assert not audit['errors'];assert m['dimensions_m']==audit['bounds_m']['size'];assert len(m['dimensions_m'])==3 and all(math.isfinite(v) and v>0 for v in m['dimensions_m'])
 assert m['bytes']==m['glb_bytes']==len(raw)==glb.stat().st_size;assert m['file_bytes']=={'glb':len(raw),'blend':blend.stat().st_size}
 assert m['axis']['up']=='+Y' and m['axis']['forward']=='+Z' and m['axis']['source_up']=='+Z' and m['axis']['source_forward']=='-Y'
 assert m['primitives']==audit['scene_primitives_estimated_base_draw_calls'];assert m['textures']==len(doc.get('textures',[]))==0;assert m['images']==len(doc.get('images',[]))==0
 for key in ['dimensions_m','axis','primitives','textures','bytes']:assert item[key]==m[key]
 c=json.load(open(d/'candidate.json'));assert c['approval']['status']=='pending';assert all(s['status']=='unknown' and s['reviewer'] is None and s['reviewed_at'] is None for s in c['stages'].values())
 for descriptor in [*c['artifacts'].values(),*c['technical_evidence'].values()]:assert digest(REPO/descriptor['path'])==descriptor['sha256']
 v=validate_candidate(d/'candidate.json',REPO);assert v['valid'] and not v['approved_for_brief'] and not v['errors']
 cv=validate_concept(d/'concept-evidence.json',BASE);assert cv['valid'] and cv['evidence_complete']
 registration=json.load(open(d/'candidate-brief.json'));brief=json.load(open(d/'brief.json'));assert registration['original_evidence_coverage']['turntable_frames']==brief['turntable_frames']==0;assert registration['preproduction_freeze_claim'] is False
 source=json.load(open(HERE/'evidence'/(slug+'-source.json')));assert source['model_bytes_unchanged'] and source['source_export']['status']=='pass'
 assert source['hashes_after'][glb.name]==digest(glb) and source['hashes_after'][blend.name]==digest(blend)
 result.append({'asset_id':slug,'revision':item['revision'],'model_and_original_design_evidence_unchanged':True,'measured_metadata_matches_actual_glb_and_blend':True,'candidate_record_valid':True,'candidate_formally_approved':False,'original_concept_evidence_still_complete':True,'formal_stages':'all unknown; no reviewer or time invented','glb_sha256':digest(glb),'blend_sha256':digest(blend)})
qa=json.load(open(HERE/'qa-provenance.json'));original=subprocess.check_output(['git','show',qa['qa_commit']+':'+qa['original_path']],cwd=REPO);assert hashlib.sha256(original).hexdigest()==digest(HERE/'independent-review-source.md')==qa['sha256']
report={'checked_at':datetime.now(timezone.utc).isoformat(),'scope':'metadata, candidate structure and exact unchanged model/artifact hashes only; no independent approval, hardware or publication verdict','status':'pass','items':result}
(HERE/'self-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
