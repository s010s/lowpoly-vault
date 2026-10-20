#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only verification of the selective batches 58/59 release payload."""
import hashlib,json,sys,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[2]
q=root/'qa/batches58-59-release-20261020'
def load(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_ref(ref):
 p=root/ref['path'];assert p.is_file(),str(p);assert digest(p)==ref['sha256'],str(p)
source=load(q/'source-bundle.json')
for f in source['files']:
 verify_ref(f);assert (root/f['path']).stat().st_size==f['bytes']
prep=load(q/'preparation.json');assert prep['selected_count']==7 and not prep['approval_claimed']
ids=[a['id'] for a in prep['selected_assets']];assert len(set(ids))==7 and 'erbenochile' not in ids
assert not (root/'assets/additions/erbenochile').exists()
assert not any('/erbenochile/' in str(p) for p in (root/'assets/candidates').rglob('*'))
sys.path.insert(0,str(root/'scripts'))
from qa_glb import audit_glb
assets=[];rebuilds=0
for a in prep['selected_assets']:
 for field in ['candidate','glb','blend','payload_glb','payload_blend','release_metadata','metrics','frozen_brief','references']:
  verify_ref(a[field])
 assert a['glb']['sha256']==a['payload_glb']['sha256'];assert a['blend']['sha256']==a['payload_blend']['sha256']
 c=load(root/a['candidate']['path']);assert c['approval']['status']=='pending'
 for ref in c['artifacts'].values():verify_ref(ref)
 for ref in c['evidence']:verify_ref(ref)
 md=load(root/a['release_metadata']['path']);assert md['sha256']['glb']==a['glb']['sha256']
 assert md['sha256']['preview'] is None and not (root/md['preview']).exists()
 assert md['preview_capture']['status']=='pending_actual_ModelStage_capture'
 assert not (root/md['preview_capture']['reserved_card_poster_path']).exists()
 assert md['name']['en'] and md['name']['zh'] and md['description']['en'] and md['description']['zh']
 audit=audit_glb(root/a['payload_glb']['path'],max_triangles=14000,max_materials=6,max_primitives=30)
 assert not audit['errors'],audit['errors']
 assert audit['sha256']==a['glb']['sha256']
 for key,actual in [('triangles',audit['scene_triangles']),('material_count',audit['materials']),('primitives',audit['scene_primitives_estimated_base_draw_calls']),('exported_position_accessor_vertices',audit['unique_position_accessor_vertices']),('glb_bytes',audit['bytes'])]:assert md[key]==actual,(a['id'],key)
 assert max(abs(x-y) for x,y in zip(md['dimensions'],audit['bounds_m']['size']))<1e-10
 if a['id']=='stalactite-group':assert audit['bounds_m']['min'][1]<-2 and audit['bounds_m']['max'][1]==0
 elif audit['warnings']:raise AssertionError((a['id'],audit['warnings']))
 base=Path(a['candidate']['path']).parent
 reports=['repro-final-1.report.json','repro-final-2.report.json'] if a['batch']==58 else ['rebuild-1.report.json','rebuild-2.report.json']
 for report in reports:
  r=load(root/base/report);assert r['status']==('pass_with_warnings' if a['id']=='stalactite-group' else 'pass') and r['byte_identical'] and r['semantic_match'];assert not r['errors']
  if a['id']=='stalactite-group':assert all('Lowest glTF Y is -2.289444 m; verify mounting/ground contract' in w for w in r['warnings'])
  assert r['glb_sha256']==a['glb']['sha256']==r['rebuilt_glb_sha256']
  for ref in r['build_run'].values():
   if isinstance(ref,dict) and 'path' in ref and 'sha256' in ref:verify_ref(ref)
  original_prefix='/tmp/lowpoly-batch'+str(a['batch'])+'-20261020/'
  rebuilt=root/r['rebuilt_glb_path'].removeprefix(original_prefix);assert digest(rebuilt)==a['glb']['sha256']
  rebuilds+=1
 assets.append({'id':a['id'],'revision':a['revision'],'glb_sha256':audit['sha256'],'triangles':audit['scene_triangles'],'bounds_glb_m':audit['bounds_m'],'warnings':audit['warnings'],'formal_approval':'pending_unchanged','preview':'pending_absent'})
assert rebuilds==14
manifest=q/'package-manifest.json'
manifest_checked=False
if manifest.exists():
 for f in load(manifest)['files']:
  verify_ref(f);assert (root/f['path']).stat().st_size==f['bytes']
 manifest_checked=True
print(json.dumps({'status':'pass','source_files_verified':len(source['files']),'selected_assets_verified':len(assets),'selected_queue_rebuild_records_verified':rebuilds,'package_manifest_verified':manifest_checked,'source_bytes':sum(f['bytes'] for f in source['files']),'assets':assets,'limits':'Read-only packaging integrity, static GLB measurements and existing rebuild evidence. No new Blender build, independent visual review, browser/GPU rendering, full catalog verification or publication.'},indent=2))
