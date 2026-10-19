from pathlib import Path
import json,hashlib,shutil,sys
root=Path(__file__).resolve().parents[3]
source='production/concept-small-marine-quartet-20261019';qa='qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh';scope='concept-quartets-20261019';pack='prehistoric-'+scope
read=lambda p:json.loads((root/p).read_text())
def pin(p):return {'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()}
def write(p,d):
 f=root/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
text={
'emeraldella':('Emeraldella-inspired crawler','Emeraldella 启发爬行小动物','Seafoam eyeless head, eleven tapered trunk plates, curved antennae and a long tail spine. Fine limbs, posture and palette are artistic simplifications; no specimen-level reconstruction claim.','海沫绿色无眼头盾、十一片逐渐收窄的躯干甲片、弯曲触角与长尾刺。细部附肢、姿态和配色为艺术简化，不作标本级复原主张。'),
'burgessia':('Burgessia-inspired shield crawler','Burgessia 启发盾甲小动物','Warm ochre domed shield, swept antennae and a slender posterior spine. Opaque shell and simplified appendages retain the broad fossil-inspired form; internal organs and fine limb anatomy are not reconstructed.','暖赭色拱形背甲、后掠触角与细长尾刺。不透明甲壳和简化附肢保留化石启发的整体形态，不复原内部器官或精细附肢解剖。'),
 'tuzoia':('Tuzoia-inspired bivalved swimmer','Tuzoia 启发双瓣甲游泳小动物','Rose-colored paired valves, a projecting head and simplified soft limbs. A genus-inspired composite with artistic valve depth, ornament and palette; not a species-exact or specimen-level reconstruction.','玫瑰色双瓣甲、伸出的头部与简化软体附肢。综合该属形态的艺术造型；甲壳厚度、纹饰与配色为创作处理，非精确物种或标本级复原。'),
'sanctacaris':('Sanctacaris-inspired marine crawler','Sanctacaris 启发海洋爬行小动物','Blue-gray shield with swept head wings, paired frontal appendages and a segmented trunk. Fine bristles, joint counts and grasping teeth are simplified; colors and blunt tips are artistic choices.','蓝灰色头盾带后掠侧翼、成对前附肢与分节躯干。细刚毛、关节数量和捕捉齿均作简化；配色和钝端为艺术处理。')}
additions=[]
for ident,rev in [('emeraldella','r002'),('burgessia','r002'),('tuzoia','r003'),('sanctacaris','r002')]:
 p=f'{source}/{ident}/{rev}';folder=f'assets/additions/{ident}/{scope}';a=read(p+'/metadata.json');brief=read(p+'/brief.json');refs=read(p+'/references.json')
 keys=['id','category','triangles','dimensions','license','author','schema_version','collection','units','axes','origin','blender_version','blender_unit_scale','blender_dimensions_m','bounds_glb_m','generator_seed','export_options','materials','glb_bytes','generator','surface_profile']
 a={k:a[k] for k in keys if k in a};a.update(name=dict(zip(['en','zh'],text[ident][:2])),description=dict(zip(['en','zh'],text[ident][2:])),scientific_scope={'en':'Evidence-informed stylized scene prop; formal production and physical-device acceptance remain unverified.','zh':'基于事实参考的风格化场景道具；正式生产验收及实体设备验收仍未核实。'},worlds=['prehistoric'],packs=[pack],surface_profile='palette-only',source_revision=rev,source_category='animals',source_url=f'https://github.com/s010s/lowpoly-vault/tree/1c1b5fd0f466feb95457a8c96ed58ed8f219201f/{p}',sources=refs['sources'],mount_origin=brief['budgets']['mount_origin'])
 (root/folder).mkdir(parents=True,exist_ok=True)
 for key in ['glb','blend']:
  a[key]=f'{folder}/{ident}.{key}';shutil.copyfile(root/f'{p}/{ident}.{key}',root/a[key])
 a['preview']=f'{folder}/preview-hero.png'
 capture=root/'qa/quartets-release-20261019/card-capture/references'/f'{ident}.png'
 if not capture.exists():raise SystemExit('Waiting for pinned capture '+str(capture))
 shutil.copyfile(capture,root/a['preview']);a['sha256']={k:pin(a[k])['sha256'] for k in ['glb','blend','preview']};write(folder+'/release-metadata.json',a)
 additions.append({'id':ident,'group':'marine','revision':rev,'source_commit':'1c1b5fd0f466feb95457a8c96ed58ed8f219201f','review_commit':'45b1411119a624461f84452adfcd0cd83838a074','original_review_freeze':'7c3cc658c1d10fa595e3ef7d27c6f0b17a842dd1','review':pin(qa+'/review.json'),'metadata':pin(folder+'/release-metadata.json'),'source_metadata':pin(p+'/metadata.json'),'candidate':pin(p+'/candidate.json'),'candidate_validation':pin(p+'/candidate-validation.json'),'artifacts':{**{k:pin(f'{p}/{ident}.{k}') for k in ['glb','blend']},**{k:pin(p+'/'+file) for k,file in [('brief','brief.json'),('references','references.json'),('config','build-config.json')]},'generator':pin(read(p+'/metadata.json')['generator'])},'technical':{k:pin(p+'/'+file) for k,file in [('source_export','source-export.report.json'),('rebuild_1','reproducibility-1.json'),('rebuild_2','reproducibility-2.json'),('runtime_parse','threejs-parse.report.json'),('khronos','gltf-validator.report.json')]},'proof':pin(p+'/proof/render-manifest.json'),'runtime':pin(qa+'/evidence/webgl/runtime-report.json'),'limits':brief['budgets'],'sha256':a['sha256'],'capture':{'report':pin('qa/quartets-release-20261019/card-capture/render-report.json'),'index':pin('qa/quartets-release-20261019/card-capture/assets/turntables/index.json'),'reference':pin('qa/quartets-release-20261019/card-capture/references/'+ident+'.png')}})
files=[]
for prefix,commit in [(source,'1c1b5fd0f466feb95457a8c96ed58ed8f219201f'),(qa,'45b1411119a624461f84452adfcd0cd83838a074')]:
 for path in sorted((root/prefix).rglob('*')):
  if path.is_file():files.append({**pin(str(path.relative_to(root))),'source_commit':commit})
for path in sorted((root/'qa/quartets-release-20261019/integration-audit').rglob('*')):
 if path.is_file():files.append({**pin(str(path.relative_to(root))),'origin':'fresh integration verification'})
for path in sorted((root/'qa/quartets-release-20261019/card-capture').rglob('*')):
 if path.is_file():files.append({**pin(str(path.relative_to(root))),'origin':'pinned Chromium capture-only CI'})
write('qa/quartets-release-20261019/source-bundle.json',{'version':1,'scope':'Immutable source and independent limited review; candidate approval remains pending','files':files})
d={'version':1,'scope':scope,'authorization':'owner_authorized_publish_independent_qa_passed_batches','acceptance_scope':'independent_qa_accepted_stylized_prop','formal_profile_acceptance':'BLOCKED','hardware_gpu_verified':False,'target_scene_verified':False,'base_descriptor':pin('assets/releases/concept-seven-20261019.json'),'publication_policy':pin('production/policies/qa-passed-batch-publication-20261018.json'),'source_bundle':pin('qa/quartets-release-20261019/source-bundle.json'),'integration_audit':pin('qa/quartets-release-20261019/integration-audit/marine-delivery-integrity.json') if (root/'qa/quartets-release-20261019/integration-audit/marine-delivery-integrity.json').exists() else None,'excluded_ids':['ctenoimbricata'],'additions':additions}
write('assets/releases/'+scope+'.json',d);(root/'site/accepted-concept-quartets-release.mjs').write_text('/** Exact independently reviewed candidate pins; bounded website publication only. */\nexport const CONCEPT_QUARTETS_RELEASE = '+json.dumps(d,ensure_ascii=False,indent=2)+';\n')
