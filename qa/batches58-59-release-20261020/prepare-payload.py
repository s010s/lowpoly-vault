import json, hashlib, subprocess, shutil, os, sys
from pathlib import Path
from collections import deque
OUT=Path('/tmp/lowpoly-batches58-59-release-payload-20261020')
Q=Path('qa/batches58-59-release-20261020')
SPECS={58:{'root':Path('/tmp/lowpoly-batch58-20261020'),'model':'9bb7eb242a2c7ee35868ca57789c93c06c4bcbb8','qa':'48f08fa3e2d6bb9a06526efd7142c4fc35184d86','ids':{'calamophyton':'r001','perspicaris':'r002','barchan-dune':'r001','current-ripple-surface':'r001'},'report':'independent-qa.md'},59:{'root':Path('/tmp/lowpoly-batch59-20261020'),'model':'330bc4aa669a1647c632a32622ce4318fd8d1b59','qa':'289cca9359cdd3595f7015f894a00675a004c422','ids':{'glacial-erratic':'r002','gypsum-cave-flower':'r002','stalactite-group':'r002'},'report':'QA-report.md'}}
assert not OUT.exists(), 'Do not overwrite an existing payload'
OUT.mkdir(parents=True)
def sha(x): return hashlib.sha256(x).hexdigest()
def readj(p):return json.loads(p.read_text())
def writej(p,d):p=OUT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def git(r,*args):return subprocess.check_output(['git','-C',str(r),*args])
def tree(r,commit):
 result={}
 for line in git(r,'ls-tree','-r','-z',commit).split(b'\0'):
  if not line:continue
  head,path=line.split(b'\t',1);mode,kind,oid=head.decode().split();
  if kind=='blob':result[path.decode()]=(oid,mode)
 return result
source_files={};model_trees={};qa_trees={};closure_notes=[];asset_records=[];custodies=[]
def copy_pinned(n,rel,commit,tree_map,reason):
 s=SPECS[n]; rel=str(rel);assert rel in tree_map,(n,rel,'not tracked at pin')
 oid,mode=tree_map[rel];assert mode!='120000',(rel,'symlink unsupported')
 expected=git(s['root'],'cat-file','blob',oid); materialized=(s['root']/rel).is_file(); data=(s['root']/rel).read_bytes() if materialized else expected
 assert data==expected,(rel,'worktree differs from pinned blob')
 dest=OUT/rel;digest=sha(data)
 if rel in source_files:
  assert source_files[rel]['sha256']==digest,(rel,'cross-batch conflict')
  origin={'batch':n,'source_commit':commit,'git_blob':oid}
  if origin not in source_files[rel]['origins']:source_files[rel]['origins'].append(origin)
  return
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 assert sha(dest.read_bytes())==digest
 source_files[rel]={'path':rel,'bytes':len(data),'sha256':digest,'source_commit':commit,'git_blob':oid,'origins':[{'batch':n,'source_commit':commit,'git_blob':oid}],'role':reason,'copy_method':'plain_copy_verified_against_git_blob' if materialized else 'materialized_directly_from_pinned_git_blob'}
def allstrings(x):
 if isinstance(x,str):yield x
 elif isinstance(x,list):
  for v in x:yield from allstrings(v)
 elif isinstance(x,dict):
  for k,v in x.items():
   yield k;yield from allstrings(v)
for n,s in SPECS.items():
 r=s['root'];mt=tree(r,s['model']);qt=tree(r,s['qa']);model_trees[n]=mt;qa_trees[n]=qt
 assert git(r,'merge-base','--is-ancestor',s['model'],s['qa'])==b''
 changed=git(r,'diff','--name-only',s['model'],s['qa']).decode().splitlines()
 assert all(p.startswith(f'qa/batch{n}-independent-20261020/') for p in changed), changed
 prefixes=[f'assets/candidates/continuous-small-life-round22-20261020/batch-{n}/{id}/{rev}/' for id,rev in s['ids'].items()]
 wanted={p for p in mt if any(p.startswith(pre) for pre in prefixes)}
 # Small pinned runtime/validation sources, contracts and licenses; no app/catalog or installation.
 helpers=['asset_common.py','qa_glb.py','check_source_export.py','check_reproducibility.py','run_asset_queue.py','validate_gltf.cjs','validate_candidate.py','candidate_profile.py','validate_concept_evidence.py','render_candidate_views.py']
 wanted.update('scripts/'+p for p in helpers)
 wanted.update(p for p in mt if p.startswith('schemas/'))
 wanted.update(['LICENSE','LICENSES/CC-BY-4.0.txt','LICENSES/MIT.txt','ATTRIBUTION.md','package.json','package-lock.json','production/policies/qa-passed-batch-publication-20261018.json'])
 work=f'production/continuous-small-life-round22-20261020/work/batch-{n}'
 context=['HANDOFF.md','handoff.json','final-selection.json','claim.json','KNOWN-LIMITS.md','build-dependencies.json','rebuild-jobs.json','rebuild-r002-queue.json']
 wanted.update(work+'/'+p for p in context if work+'/'+p in mt)
 # Preserve all actual executions referenced by the final authoritative rebuild reports.
 for ident,rev in s['ids'].items():
  base=f'assets/candidates/continuous-small-life-round22-20261020/batch-{n}/{ident}/{rev}'
  for report in (['repro-final-1.report.json','repro-final-2.report.json'] if n==58 else ['rebuild-1.report.json','rebuild-2.report.json']):
   d=readj(r/base/report);attempt=str(Path(d['build_run']['request']['path']).parent)
   wanted.update(p for p in mt if p.startswith(attempt+'/'))
   run_root=attempt.split('/build/')[0]
   wanted.update(p for p in mt if p.startswith(run_root+'/runs/') and p.endswith('.json'))
 # Follow file pointers only inside the seven selected revisions, their work records and pinned helpers.
 # Batch context / QA may mention excluded or historical revisions; those are not active release dependencies.
 queue=deque(sorted(wanted));seen=set()
 while queue:
  rel=queue.popleft()
  if rel in seen:continue
  seen.add(rel)
  if rel not in mt:raise ValueError(('Missing pinned source',rel))
  copy_pinned(n,rel,s['model'],mt,'selected_candidate_and_source_closure')
  if not rel.endswith('.json') or rel.startswith('schemas/') or rel.endswith(('handoff.json','final-selection.json','claim.json')):continue
  try:d=readj(r/rel)
  except Exception:continue
  for val in allstrings(d):
   if len(val)>600 or '\n' in val or val.startswith(('http:','https:')):continue
   candidates=[]
   if val.startswith(str(r)+'/'):candidates=[val[len(str(r))+1:]]
   elif not val.startswith('/'):candidates=[val,str(Path(rel).parent/val)]
   for ref in candidates:
    ref=os.path.normpath(ref)
    if ref not in mt:continue
    if ref.startswith('assets/candidates/') and not any(ref.startswith(pre) for pre in prefixes):
     closure_notes.append({'from':rel,'reference':ref,'status':'historical_or_excluded_revision_not_release_payload'});continue
    if '/erbenochile/' in ref:continue
    if ref.startswith(('assets/candidates/','production/continuous-small-life-round22-20261020/work/','production/policies/','scripts/','schemas/')) or ref in ['package.json','package-lock.json']:
     if ref not in seen:queue.append(ref)
 qroot=f'qa/batch{n}-independent-20261020';cust=readj(r/qroot/'evidence-custody.json')
 assert cust['source_commit']==s['model'];assert set(cust['accepted_bounded_ids'])==set(s['ids'])
 for item in cust['files']:
  data=(r/qroot/item['path']).read_bytes();assert sha(data)==item['sha256'];assert len(data)==item['bytes']
 for rel in sorted(qt):
  if rel.startswith(qroot+'/'):copy_pinned(n,rel,s['qa'],qt,'complete_independent_qa_evidence')
 custodies.append({'batch':n,'model_commit':s['model'],'qa_commit':s['qa'],'qa_only_diff_verified':True,'custody_report':qroot+'/evidence-custody.json','custody_files_verified':len(cust['files']),'qa_files_copied':sum(p.startswith(qroot+'/') for p in qt),'accepted_bounded_ids':list(s['ids']),'formal_approval':False,'remote_backup':{'status':'verified','verification_method':'coordinator reported ordinary push and exact ls-remote match','verified_by':'/root/coordinate_new_model_batches','independently_network_rechecked_by_payload_worker':False,'branch':f'candidate/small-life-batch{n}-concept-20261020','commit':s['qa']}})
print('Copied frozen source closure',len(source_files),'files',sum(x['bytes'] for x in source_files.values()),'bytes',flush=True)
writej(Q/'source-bundle.json',{'version':1,'scope':'Complete seven selected candidate revision directories, pinned helper/contracts/licenses, referenced selected build evidence, and complete batch independent-QA records. Context can mention excluded assets; none is selected for additions.','copy_method':'plain verified copies; no hard links','files':sorted(source_files.values(),key=lambda x:x['path'])})
writej(Q/'source-inventory.json',{'version':1,'source_files':len(source_files),'source_bytes':sum(x['bytes'] for x in source_files.values()),'batches':custodies,'external_historical_references':closure_notes,'historical_absolute_paths':'Original absolute paths are retained unchanged. Resolve /tmp/lowpoly-batch58-20261020/ and /tmp/lowpoly-batch59-20261020/ prefixes to this payload root for inspection; package copies do not claim those original executor locations.','excluded_exports':'No Erbenochile .glb/.blend or candidate directory is included. Full QA retains its evidence and blocked disposition.'})
TEXT={
'calamophyton':('Calamophyton form study','Calamophyton 形态研究','plants','An evidence-informed stylized Calamophyton exterior with a narrow upright trunk, leafless digitate sprays and retained branch bases. Not a measured specimen or an internal-anatomy reconstruction; branch arrangement, colour and display size are artistic.','依据参考资料制作的 Calamophyton 风格化外部形态，保留细长直立主干、无叶指状分枝与枝基痕迹。并非实测标本或内部解剖复原；分枝布置、颜色和展示尺度为艺术设定。'),
'perspicaris':('Perspicaris form study','Perspicaris 形态研究','animals','A genus-level stylized whole-animal reconstruction with paired carapace valves, stalked eyes, antennae, ten flap-bearing thoracic stations, seven exposed abdominal segments and a forked tail. Not an exact specimen or species diagnosis; soft parts, colour, pose and size are illustrative.','属级风格化整体现生形态复原，呈现成对甲瓣、眼柄、触角、十个带游泳瓣的胸部节位、七个外露腹节与分叉尾端。并非特定标本复刻或物种鉴定；软体结构、颜色、姿态和尺度均为示意。'),
'barchan-dune':('Barchan dune','新月形沙丘','geology','A generic crescent-shaped dune with two unequal horns, a gentle windward rise and a steeper inner lee face. A stylized teaching prop, not a reconstruction of a particular dune, locality, period or measured landscape.','通用新月形沙丘，具有长短不一的双角、缓和迎风坡与较陡的内侧背风坡。属于风格化教学道具，不对应特定沙丘、地点、年代或实测地形。'),
'current-ripple-surface':('Current-ripple surface','流水波痕表面','geology','A closed cutaway slab with eight gently sinuous, near-parallel current-ripple ridges and asymmetric gentle-stoss/steep-lee profiles. Relief and dimensions are exaggerated teaching choices, not a flow simulation or a claim about a named site, age or sediment grain size.','封闭剖切薄板上呈现八条近乎平行、轻微弯曲的流水波痕，剖面为缓迎流坡与陡背流坡。起伏与尺寸为教学效果作了夸张，不是水流模拟，也不主张特定地点、年代或沉积颗粒大小。'),
'glacial-erratic':('Glacial erratic','冰川漂砾','geology','A generic stylized erratic-like boulder on contrasting bedrock, with an asymmetric faceted outline and an artistic pale vein. Illustrates the geological form only; it does not assert a particular boulder, proven transport history, glacier, locality, age or real-world scale.','反差色基岩上放置通用风格化漂砾状巨石，采用不对称多面轮廓与艺术化浅色矿脉。仅示意地质形态，不指认特定巨石，不主张已证实的搬运史、冰川、地点、年代或真实尺度。'),
'gypsum-cave-flower':('Gypsum cave flower','石膏洞花','geology','Six unequal flattened curling ribbons emerge from a common rocky attachment in a stylized gypsum cave-flower form. The broad ribbons simplify crystalline growth; this is not a botanical flower, a fine-crystal replica or a named-site, age or measured-scale reconstruction.','六条长短不一的扁平卷曲带从共同岩质附着处伸出，形成风格化石膏洞花。宽带结构简化了晶体生长形态；并非植物花朵、精细晶体复刻，也不对应特定地点、年代或实测尺度。'),
'stalactite-group':('Stalactite group','钟乳石组','geology','Five downward-tapering stalactites hang from an irregular ceiling patch, with one longer offset pendant and four shorter ones. The origin is the upper ceiling attachment, not the floor. A generic stylized calcite form, not a whole cave or a named-site, age or measured-scale reconstruction.','五根向下渐细的钟乳石悬挂于不规则洞顶片：一根较长且偏置，其余四根较短。原点位于洞顶上方附着点，而非地面。属于通用风格化方解石形态，并非整座洞穴或特定地点、年代、实测尺度的复原。')}
def file_ref(rel):
 p=OUT/rel;return {'path':str(rel),'sha256':sha(p.read_bytes())}
selection=[];mappings=[];capture=[];licenses=[];review_reports=[]
for n,s in SPECS.items():
 h=readj(OUT/f'production/continuous-small-life-round22-20261020/work/batch-{n}/handoff.json');hand={a['asset_id']:a for a in h.get('assets',h.get('items',[]))}
 qroot=f'qa/batch{n}-independent-20261020';report=file_ref(f'{qroot}/{s["report"]}');report.update({'source_commit':s['model'],'qa_commit':s['qa'],'reviewer_task':next(x for x in custodies if x['batch']==n).get('reviewer_task',readj(OUT/qroot/'evidence-custody.json')['reviewer_task'])});review_reports.append(report)
 for ident,rev in s['ids'].items():
  base=Path(f'assets/candidates/continuous-small-life-round22-20261020/batch-{n}/{ident}/{rev}');c=readj(OUT/base/'candidate.json');m=readj(OUT/base/'metrics.json');b=readj(OUT/base/'brief.json');cfg=readj(OUT/base/'build-config.json');refs=readj(OUT/base/'references.json');hh=hand[ident]
  assert c['approval']['status']=='pending'
  for role,a in c['artifacts'].items():assert sha((OUT/a['path']).read_bytes())==a['sha256'],(ident,role)
  assert c['artifacts']['glb']['sha256']==hh['glb_sha256'];assert c['artifacts']['source']['sha256']==hh['source_sha256']
  if n==58:
   bounds=m['glb']['bounds_m'];bd=m['measured_blender_xyz_m'];tri=m['glb']['scene_triangles'];materials=m['glb']['materials'];primitives=m['glb']['scene_primitives_estimated_base_draw_calls'];pos=m['glb']['unique_position_accessor_vertices'];verts=readj(OUT/base/'source-vertex-counts.json');authored=verts['authored_vertices'];evaluated=verts['evaluated_vertices'];nominal=m['nominal_dimensions_blender_xyz_m'];export=m['export_options'];version=m['blender_version'];seed=cfg['seed'];source_metadata=None
  else:
   om=readj(OUT/base/'metadata.json');bounds=om['bounds_glb_m'];bd=m['measured_dimensions_blender_xyz_m'];tri=m['triangles'];materials=m['materials'];primitives=m['primitives'];pos=m['exported_position_accessor_vertices'];authored=m['authored_source_vertices'];evaluated=None;nominal=m['nominal_dimensions_blender_xyz_m'];export=om['export_options'];version=om['blender_version'];seed=cfg['seed'];source_metadata=file_ref(base/'metadata.json')
  nameen,namezh,cat,en,zh=TEXT[ident];add=Path(f'assets/additions/{ident}/batch{n}-20261020');(OUT/add).mkdir(parents=True,exist_ok=True)
  for role,suffix in [('glb','glb'),('source','blend')]:
   data=(OUT/c['artifacts'][role]['path']).read_bytes();(OUT/add/f'{ident}.{suffix}').write_bytes(data);assert sha(data)==c['artifacts'][role]['sha256']
  glbrel=str(add/f'{ident}.glb');blendrel=str(add/f'{ident}.blend');preview=str(add/f'{ident}.png');poster=f'assets/card-previews/{ident}-v2-768-q90.webp'
  scope={'en':'Bounded stylized teaching/form study only. File-space metres and nominal dimensions are artistic display choices, not measurements of a real specimen or site. No locality or geological age is asserted.','zh':'仅限风格化教学或形态研究。文件坐标中的米制尺寸与标称尺寸均为艺术展示设定，并非真实标本或地点的实测值；不主张具体地点或地质年代。'}
  md={'schema_version':1,'id':ident,'name':{'en':nameen,'zh':namezh},'category':cat,'collection':'prehistoric','worlds':['prehistoric'],'packs':[f'prehistoric-batch{n}-20261020'],'description':{'en':en,'zh':zh},'scientific_scope':scope,'units':'meters','dimension_semantics':'measured exported file-space bounds, not real-world specimen/locality measurements','axes':{'glb_up':'+Y','glb_forward':'+Z','blender_up':'+Z','blender_forward':'-Y'},'dimensions':bounds['size'],'blender_dimensions_m':bd,'bounds_glb_m':bounds,'nominal_dimensions_blender_xyz_m':nominal,'origin':b.get('origin','ground contact center; see immutable source contract'),'triangles':tri,'material_count':materials,'primitives':primitives,'authored_source_vertices':authored,'evaluated_source_vertices':evaluated,'exported_position_accessor_vertices':pos,'glb_bytes':(OUT/glbrel).stat().st_size,'texture_count':0,'license':'CC-BY-4.0','author':'Leon Made This / s010s','blender_version':version,'three_version':'0.180.0','generator_seed':seed,'export_options':export,'glb':glbrel,'blend':blendrel,'preview':preview,'sha256':{'glb':c['artifacts']['glb']['sha256'],'blend':c['artifacts']['source']['sha256'],'preview':None},'preview_capture':{'status':'pending_actual_ModelStage_capture','reserved_png_path':preview,'reserved_card_poster_path':poster,'reservation_note':'v2/768/q90 follows reference method only; confirm current trusted main preset before capture. No CPU proof/concept image is promoted.'},'source_url':f'https://github.com/s010s/lowpoly-vault/tree/{s["model"]}/{base}','source_identity':{'batch':n,'revision':rev,'model_commit':s['model'],'qa_commit':s['qa'],'candidate':file_ref(base/'candidate.json')},'metadata_provenance':'Derived release metadata. Original source, candidate, brief and reports are byte-unchanged. Not source-authored metadata or a formal acceptance record.'}
  if ident=='stalactite-group':md['origin']='ceiling attachment top center: Blender z=0 / glTF y=0; body extends below origin';md['mounting_note']={'en':'Preserve ceiling mounting. Do not silently ground-normalize this asset; negative glTF Y is expected.','zh':'保留洞顶悬挂原点，不要自动归一到地面；glTF Y 轴负向延伸符合设计。'}
  writej(add/'release-metadata.json',md)
  attrib=f'{nameen} / {namezh}\nOriginal model and editable source: Leon Made This / s010s.\nLicense: Creative Commons Attribution 4.0 International (CC BY 4.0).\nhttps://creativecommons.org/licenses/by/4.0/\nSource: {md["source_url"]}\nRevision: {rev}; model commit {s["model"]}.\nRelease preparation changes: artifact paths and bilingual metadata only; GLB and Blender source bytes unchanged.\nGenerator and executable helper code: MIT. Third-party references are consulted-only and retain their own rights; no third-party reference images, scans, textures or mesh data incorporated.\nScope: {en}\n范围：{zh}\nPreview capture is pending; candidate proof/concept images are not approved website posters.\n'
  (OUT/add/'ATTRIBUTION.txt').write_text(attrib)
  rec={'id':ident,'revision':rev,'batch':n,'source_commit':s['model'],'qa_commit':s['qa'],'candidate':file_ref(base/'candidate.json'),'glb':file_ref(c['artifacts']['glb']['path']),'blend':file_ref(c['artifacts']['source']['path']),'payload_glb':file_ref(glbrel),'payload_blend':file_ref(blendrel),'release_metadata':file_ref(add/'release-metadata.json'),'source_metadata':source_metadata,'metrics':file_ref(base/'metrics.json'),'frozen_brief':file_ref(base/'brief.json'),'candidate_artifact_brief':c['artifacts']['brief'],'references':file_ref(base/'references.json'),'independent_qa_report':report,'bounded_disposition':'ACCEPT','formal_acceptance':'UNAPPROVED_PENDING_UNCHANGED','preview_capture':'pending','physical_gpu':'not_run','target_scene':'not_run','provider_generation_time':'unknown','modeling_start_time':readj(OUT/base/'concept-evidence.json')['chronology'].get('modeling_started_at'),'counts':{'triangles':tri,'materials':materials,'primitives':primitives,'authored_source_vertices':authored,'evaluated_source_vertices':evaluated,'exported_position_accessor_vertices':pos},'measured_blender_xyz_m':bd,'measured_gltf_xyz_m':bounds['size']}
  selection.append(rec)
  mapping={'id':ident,'release_metadata':rec['release_metadata'],'original_candidate':rec['candidate'],'original_metrics':rec['metrics'],'original_metadata':source_metadata,'original_brief':rec['frozen_brief'],'candidate_artifact_brief':rec['candidate_artifact_brief'],'original_references':rec['references'],'independent_qa':report,'field_mapping':{'name/description/scientific_scope':'Bilingual release-authored labels and restricted claims derived from frozen brief and independent bounded QA; no invented translated taxon common name, locality, age, or physical specimen size.','category':'Release taxonomy: plants/animals/geology. Glacial erratic source terrain is mapped to existing website geology category. No age claim follows from organizational prehistoric collection.','glb/blend/sha256':'Exact candidate.artifacts pins copied byte-identically to additions.','dimensions/bounds_glb_m':'Measured glTF X,Y,Z; metrics.glb.bounds_m (58) or source metadata bounds_glb_m plus source-export report (59).','blender_dimensions_m':'Measured Blender X,Y,Z from metrics; not nominal envelope.','nominal_dimensions_blender_xyz_m':'Unchanged illustrative nominal target, separately labeled.','counts':'58 metrics plus source-vertex-counts; 59 original metrics. Batch59 evaluated vertex count remains null because a separate explicit authored-vs-evaluated count is not supplied in metadata.','preview/sha256.preview':'Reserved path; image not created and hash null until exact ModelStage capture and review.','origin':'Frozen brief source contract. Stalactites explicitly ceiling-mounted with expected negative glTF Y.','source identity':'Pinned model commit and separately supplied final QA commit; no formal stage fields promoted.'},'original_metadata_stale_paths':n==59,'stale_path_handling':'Batch59 original metadata points to removed temporary _export paths; retained unmodified in source evidence, not used as payload artifact authority. Candidate.artifacts is authoritative.' if n==59 else None}
  if ident=='current-ripple-surface':mapping['wording_reconciliation']='Original claim_scope prose says seven ridges, but frozen feature range is seven to nine, concept_decisions explicitly says eight, generator ridge=8, and independent QA observes eight. Release copy states eight; original brief is untouched.'
  if ident=='perspicaris':mapping['dimension_reconciliation']='Actual long axis is 0.055883741 m, not the 0.045 m illustrative nominal target. Both are retained with distinct semantics; neither is a specimen-size claim.'
  mappings.append(mapping)
  capture.append({'id':ident,'glb':rec['payload_glb'],'metadata':rec['release_metadata'],'reserved_preview':preview,'reserved_card_poster':poster,'source_model_commit':s['model'],'qa_commit':s['qa'],'mounting':md['origin']})
  licenses.append({'id':ident,'art_license':'CC-BY-4.0','software_license':'MIT','attribution':'Leon Made This / s010s','attribution_file':file_ref(add/'ATTRIBUTION.txt'),'references_ledger':rec['references'],'third_party_incorporation':'consulted-only references; no third-party assets incorporated','changes':'bilingual release metadata and path remapping; model/source bytes unchanged'})
writej(Q/'metadata-mapping.json',{'version':1,'source_authored_metadata_claimed':False,'scope':'Derived website payload metadata only; candidate/source/brief/stages untouched. No formal approval inferred.','assets':mappings})
writej(Q/'license-attribution.json',{'version':1,'license_files':[file_ref('LICENSE'),file_ref('LICENSES/CC-BY-4.0.txt'),file_ref('LICENSES/MIT.txt'),file_ref('ATTRIBUTION.md')],'assets':licenses})
exclusions=[{'id':'erbenochile','revision':'r003','source_commit':SPECS[59]['model'],'qa_commit':SPECS[59]['qa'],'glb_sha256':'ec7b7fb8e84b2298a17d5ee42f0074ce97aab38eaac98a21579edc6eee59645f','disposition':'BLOCKED_EXCLUDED','reason_en':'Dorsal-shell-only teaching reconstruction does not satisfy the original whole-organism inventory scope. Primary Fortey & Chatterton (2003) Fig. 1(A–E) anatomy pixels were unavailable for eye/visor review. These are independent blockers.','reason_zh':'当前仅为背甲教学复原，未满足原始整只生物范围；Fortey 与 Chatterton（2003）图1(A–E)的原始解剖图像未能供眼部与眼罩形态审查。这是两项相互独立的阻塞。','required_resolution':'Separate explicit shell-only scope authorization plus actual figure-pixel review, or a new whole-organism reconstruction against primary anatomy evidence. Figure access alone cannot resolve scope mismatch.','release_assets_present':False,'review_evidence_retained':True}]
writej(Q/'exclusions.json',{'version':1,'excluded':exclusions,'no_export_or_preview_reserved_for_excluded_ids':True})
gates=[{'id':'trusted-main-baseline','status':'pending','requirement':'Root verifies current main commit, actual release count, uniqueness and exact permitted release policy. 209 is an expected historical baseline, not established by this package.'},{'id':'bounded-release-disposition','status':'pending_root_record','requirement':'Record separate seven-ID bounded publication disposition under current policy without rewriting formal candidate acceptance or unrun GPU/scene stages.'},{'id':'modelstage-capture','status':'not_run','requirement':'Use current trusted main ModelStage/render preset and pinned Chromium on exactly these seven GLBs; preserve source hashes, viewer/preset hash, renderer identity and dimensions. Capture reference PNG and card WebP; do not use CPU proof/concept images.'},{'id':'preview-independent-review','status':'not_run','requirement':'Inspect actual captured pixels for silhouette, materials, clipping, background and card/detail continuity; verify image digests and exact source GLB identity. Stalactites must remain ceiling-mounted.'},{'id':'gallery-detail-wheel','status':'not_run','requirement':'Verify seven cards and detail GLB first paint, wheel/orbit, desktop/mobile, return/close, preview fallback and no GPU-count inflation; produce actual evidence on selected final integration baseline.'},{'id':'release-integration-ci','status':'not_run','requirement':'Serial root integration only: incremental collector/manifest/allowlist updates, current release checks and CI for exact final commit. No collector or manifest has been changed here.'},{'id':'merge-deploy-verification','status':'not_run','requirement':'Only root under existing user authorization: verify expected remote commit, successful deployment, actual catalog inclusion and exact live download hashes before saying live.'}]
formal={'candidate_approval':'pending/unapproved, original records unchanged','physical_gpu':'not_run','populated_scene':'not_run','concept_provider_timestamp':'unknown for all seven','batch59_modeling_started_at':'unknown','note':'Software ModelStage capture when later run does not establish a physical hardware GPU pass. Bounded release policy is not formal production acceptance.'}
writej(Q/'capture-inputs.json',{'version':1,'publication_authority':False,'selected_ids':[x['id'] for x in selection],'assets':capture,'renderer':'existing current pinned ModelStage via site/render-web-previews.mjs','capture_status':'not_run','images_present':False,'gallery_detail_wheel':'deferred_until_trusted_main_baseline','reserved_preset':'v2/768/q90 reference method, must be checked against actual current main before capture','baseline_commit':None,'baseline_release_count':None,'physical_gpu':'not_run','target_scene':'not_run'})
writej(Q/'preparation.json',{'version':1,'publication_authority':False,'status':'prepared_source_and_payload_not_release_ready','selected_assets':selection,'selected_count':7,'review_reports':review_reports,'exclusions':exclusions,'source_custody':custodies,'approval_claimed':False,'formal_gate_status':formal,'required_gates':gates,'trusted_main_baseline':{'status':'not_verified','commit':None,'release_count':None,'expected_count_not_authoritative':209},'collector_manifest_site_ci_changes':False,'capture_or_deployment_performed':False})
writej(Q/'remaining-gates.json',{'version':1,'release_gates':gates,'formal_candidate_gates':formal,'no_new_workflow_triggered':True})
VERIFY='''#!/usr/bin/env python3
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
'''
(OUT/Q/'verify-package.py').write_text(VERIFY)
validation=[]
for a in selection:
 base=Path(a['candidate']['path']).parent
 cmd=[sys.executable,str(OUT/'scripts/validate_candidate.py'),a['candidate']['path'],'--root',str(OUT),'--profile','static-stylized-v1','--profile-contract',str(base/'profile-contract.json'),'--json']
 result=subprocess.run(cmd,cwd=OUT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 try:d=json.loads(result.stdout)
 except Exception:raise RuntimeError((a['id'],result.returncode,result.stdout,result.stderr))
 writej(Q/'validation'/f'{a["id"]}-candidate.json',d)
 assert result.returncode==0 and d['valid'] and not d['approved_for_brief'],(a['id'],d)
 validation.append({'id':a['id'],'integrity_valid':True,'profile_compatible':True,'approved_for_brief':False,'returncode':result.returncode,'result':file_ref(Q/'validation'/f'{a["id"]}-candidate.json')})
writej(Q/'candidate-integrity-checks.json',{'status':'pass','scope':'Read-only relocated selected candidate/profile integrity; not formal approval','assets':validation})
res=subprocess.run([sys.executable,str(OUT/Q/'verify-package.py')],cwd=OUT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
assert res.returncode==0,(res.stdout,res.stderr)
writej(Q/'packaging-verification.json',json.loads(res.stdout))
(OUT/'README.md').write_text('''# Seven-model release payload: batches 58 and 59\n\nPrepared in dot-owned /tmp only. This is a selective payload, not a checkout, release manifest, formal approval, publication or live-site claim. No source candidate, brief, report, collector, site, CI or main branch was changed. No install, Blender rebuild, capture workflow, push, merge or deployment was run for this preparation.\n\nSelected: calamophyton r001; perspicaris r002; barchan-dune r001; current-ripple-surface r001; glacial-erratic r002; gypsum-cave-flower r002; stalactite-group r002.\n\nErbenochile r003 is excluded. The shell-only/whole-organism scope mismatch and unavailable primary figure pixels are independent blockers. Its complete independent-QA context remains in the QA evidence, not in release additions or model exports.\n\n## Entry points\n\n- qa/batches58-59-release-20261020/preparation.json: seven exact identities, statuses and remaining gates.\n- qa/batches58-59-release-20261020/source-bundle.json: every original copied file, SHA-256, Git blob and source commit.\n- qa/batches58-59-release-20261020/package-manifest.json: all packaged files except the manifest itself and SHA256SUMS.\n- qa/batches58-59-release-20261020/metadata-mapping.json: derived bilingual release wording and source mappings.\n- qa/batches58-59-release-20261020/capture-inputs.json: seven hash-pinned inputs and reserved preview paths. No preview pixels are present under additions/card-previews.\n- qa/batches58-59-release-20261020/exclusions.json and remaining-gates.json.\n- assets/additions/<id>/batch58-20261020 or batch59-20261020: selected byte-identical GLB/Blend plus release-metadata.json and ATTRIBUTION.txt.\n\n## Verification\n\nRun from this payload root:\n\n    python qa/batches58-59-release-20261020/verify-package.py\n    sha256sum -c SHA256SUMS\n\nVerification is read-only and requires no package installation. It rechecks original-file hashes, selected source/export pins, relocated candidate dependencies, static GLB counts/bounds and 14 already-recorded queue rebuilds. It does not execute generators or confer visual/factual/runtime approval.\n\nAll source files are plain copies verified against their immutable Git blobs, not hard links. Sparse-checkout omissions such as license texts are materialized directly from their pinned blobs. Original absolute execution paths remain untouched in historical records; the source-inventory.json documents how to locate copied counterparts. Shared batch records can refer to historical or excluded assets outside this selected closure; only the seven selected model/rebuild dependency chains are release dependencies.\n\n## Scope safeguards\n\nIndependent reviews accept bounded stylized scope only. Original candidate approvals remain pending; physical GPU and populated-scene checks remain unrun. Image-provider generation timestamps remain unknown, as does batch59 modeling-start time. File-space metre dimensions are not measured specimen or locality claims. Stalactites retain their ceiling origin and negative glTF Y extent.\n\nThe expected 209 baseline is not verified here. Root must establish actual current main/IDs/count before serial integration. Exact current ModelStage capture and independent pixel review, gallery/detail/wheel checks, release CI, and merge/deployment verification remain pending. CPU proof images and ImageGen concepts are evidence only, never approved website posters. Existing pinned capture method may use software rendering; it is not physical GPU proof.\n\nModels/source art/metadata: CC BY 4.0, Leon Made This / s010s. Executable code: MIT. Reference ledgers distinguish consulted sources from incorporated art. Per-model attribution accompanies the additions.\n''')
# Preserve the exact preparation recipe for reproducibility, but it must not overwrite an existing output.
(OUT/Q/'prepare-payload.py').write_bytes(Path(__file__).read_bytes())
files=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.relative_to(OUT).as_posix() not in [str(Q/'package-manifest.json'),'SHA256SUMS']:
  files.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
writej(Q/'package-manifest.json',{'version':1,'scope':'Local selective seven-model release payload, not released','selected_ids':[a['id'] for a in selection],'file_count':len(files),'total_bytes':sum(f['bytes'] for f in files),'excluded_self_and_checksum_file':True,'files':files})
(OUT/'SHA256SUMS').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(OUT)}\n' for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
# Seal the final integrity result, then regenerate non-self-referential checksums.
finalcheck=subprocess.run([sys.executable,str(OUT/Q/'verify-package.py')],cwd=OUT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
assert finalcheck.returncode==0,(finalcheck.stdout,finalcheck.stderr)
writej(Q/'packaging-verification.json',json.loads(finalcheck.stdout))
files=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.relative_to(OUT).as_posix() not in [str(Q/'package-manifest.json'),'SHA256SUMS']:
  files.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
writej(Q/'package-manifest.json',{'version':1,'scope':'Local selective seven-model release payload, not released','selected_ids':[a['id'] for a in selection],'file_count':len(files),'total_bytes':sum(f['bytes'] for f in files),'excluded_self_and_checksum_file':True,'files':files})
(OUT/'SHA256SUMS').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(OUT)}\n' for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
print(json.dumps({'output':str(OUT),'source_files':len(source_files),'package_files':len(files)+2,'package_bytes':sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),'manifest':str(Q/'package-manifest.json'),'manifest_sha256':sha((OUT/Q/'package-manifest.json').read_bytes()),'selected_ids':[a['id'] for a in selection]},indent=2))
