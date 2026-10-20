#!/usr/bin/env python3
"""Verify batch-55 QA pins and fingerprint the actual bundle inputs."""
import argparse, hashlib, json, subprocess
from pathlib import Path

PINNED_CANDIDATE='b2341debdb31f73e0719d4aadbe832321db6008a'
ASSETS=[('vermicularia','r001'),('weichselia','r001'),('ventifact','r001'),('pentichnus-deep-dwelling-trace','r002')]
VIEWS=['hero','reversehero','front','side','rear','top','clay','silhouette']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[5]); ap.add_argument('--output',type=Path,default=Path(__file__).with_name('asset-binding.json')); a=ap.parse_args()
 root=a.repo.resolve(); scope_path=root/'production/continuous-small-life-round20-20261020/batch-55-QA-SCOPE.json'; handoff_path=root/'production/continuous-small-life-round20-20261020/work/batch-55/HANDOFF.md'; scope=json.loads(scope_path.read_text())
 if scope.get('expected_source_commit')!='1e43f9e2c79b6d2465d8eadf2169355cba3690c7': raise SystemExit('source commit pin mismatch')
 if scope.get('expected_asset_ids')!=[x for x,_ in ASSETS]: raise SystemExit('asset ID order/pin mismatch')
 base='assets/candidates/continuous-small-life-round20-20261020/batch-55/'; entries=[]
 for asset,rev in ASSETS:
  bundle=root/base/asset/rev; glb=bundle/f'{asset}.glb'; blend=bundle/f'{asset}.blend'; concept=bundle/'concept-original.png'; prompt=bundle/'concept-prompt.txt'; gen=json.loads((bundle/'concept-generation.json').read_text()); modeling=json.loads((bundle/'modeling-start.json').read_text()); manifest=json.loads((bundle/'proof/render-manifest.json').read_text()); frames=[]
  expected=scope['expected_glb_sha256_by_asset'][asset]; actual=sha(glb)
  if expected!=actual: raise SystemExit(f'{asset}: pinned GLB mismatch')
  if manifest.get('source_glb_sha256')!=actual or manifest.get('subject',{}).get('glb_sha256')!=actual: raise SystemExit(f'{asset}: proof manifest source GLB mismatch')
  for ident in VIEWS:
   fs=[f for f in manifest.get('frames',[]) if f.get('id')==ident]
   if len(fs)!=1: raise SystemExit(f'{asset}: required view {ident} missing/duplicate')
   f=fs[0]; path=bundle/'proof'/f['path']; actual_frame_sha=sha(path)
   if actual_frame_sha!=f['sha256'] or f['width']!=512 or f['height']!=512: raise SystemExit(f'{asset}: frame hash or size mismatch: {ident}')
   frames.append({'id':ident,'path':str(path.relative_to(root)),'sha256':actual_frame_sha,'width':f['width'],'height':f['height']})
  entries.append({'asset_id':asset,'revision':rev,'bundle':str(bundle.relative_to(root)),'glb':{'path':str(glb.relative_to(root)),'sha256':actual,'bytes':glb.stat().st_size,'expected_sha256':expected},'blend':{'path':str(blend.relative_to(root)),'sha256':sha(blend)},'generator':{'path':str((bundle/'generator.py').relative_to(root)),'sha256':sha(bundle/'generator.py')},'concept_original':{'path':str(concept.relative_to(root)),'sha256':sha(concept)},'concept_prompt':{'path':str(prompt.relative_to(root)),'sha256':sha(prompt)},'concept_generation_record':{'path':str((bundle/'concept-generation.json').relative_to(root)),'sha256':sha(bundle/'concept-generation.json'),'provider_generation_timestamp':gen.get('provider_generation_timestamp'),'provider_model':gen.get('provider_model'),'seed':gen.get('seed'),'output_received_observed_at':gen.get('output_received_observed_at')},'modeling_chronology':{'path':str((bundle/'modeling-start.json').relative_to(root)),'sha256':sha(bundle/'modeling-start.json'),'generator_authoring_started_at':modeling.get('generator_authoring_started_at'),'modeling_started_at':modeling.get('modeling_started_at'),'first_blender_geometry_started_at':modeling.get('first_blender_geometry_started_at')},'proof_manifest':{'path':str((bundle/'proof/render-manifest.json').relative_to(root)),'sha256':sha(bundle/'proof/render-manifest.json'),'contact_sheet_sha256':sha(bundle/'contact-sheet.png'),'frame_count':len(frames),'frames':frames},'candidate_record':{'task_id':json.loads((bundle/'candidate.json').read_text())['maker'].get('task_id'),'status':json.loads((bundle/'candidate.json').read_text()).get('approval',{}).get('status'),'stage_statuses':{k:v.get('status') for k,v in json.loads((bundle/'candidate.json').read_text()).get('stages',{}).items()}}})
 ancestry=subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor','1e43f9e2c79b6d2465d8eadf2169355cba3690c7',PINNED_CANDIDATE],check=False).returncode==0
 if not ancestry: raise SystemExit('model source commit not ancestor of candidate pin')
 report={'schema_version':1,'batch_id':'batch-55','candidate_branch':'candidate/small-life-batch55-concept-20261020','candidate_commit':PINNED_CANDIDATE,'model_source_commit':scope['expected_source_commit'],'source_commit_is_candidate_ancestor':ancestry,'handoff_sha256':sha(handoff_path),'qa_scope_sha256':sha(scope_path),'qa_scope_kind':scope.get('kind'),'inputs_immutable':True,'chronology_policy':'Provider generation timestamp and generator-authoring/modeling start remain null when not observed; no filesystem mtime is used.','view_ids_required':VIEWS,'assets':entries}
 a.output.write_text(json.dumps(report,indent=2)+'\n'); print(a.output)
if __name__=='__main__': main()
