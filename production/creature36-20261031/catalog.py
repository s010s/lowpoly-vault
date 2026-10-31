"""Install a same-ID overlay. Untargeted manifest/poster bytes stay unchanged."""
import pathlib,json,copy,importlib.util,hashlib,shutil
ROOT=pathlib.Path(__file__).resolve().parents[2]; RELEASE='creature36-20261031';FOLDER=ROOT/'production'/RELEASE
spec=importlib.util.spec_from_file_location('prior',ROOT/'production/meshy-refined-five-20261030/prepare-final-catalog.py');prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
def sha(b):return hashlib.sha256(b).hexdigest()
CAVEATS={
'megatherium':('Hind-claw reconstruction remains approximate; unsuitable for exact foot closeups.','后足爪部复原仍有差异，不用于精确足部特写。'),
'toxodon':('Small outer-ankle projections may read as folds or extra digits; their identity is uncertain.','踝外侧小突起可能读作皮褶或额外趾，其性质仍不确定。'),
'glyptodon':('Front-digit arrangement differs from the earlier anatomical brief.','前足趾式与原解剖简报存在差异。'),
'diplocaulus':('Front-foot detail differs from the approved four-visible-digit art design.','前足细节与批准的四个可见趾美术设计存在差异。'),
'cynognathus':('Front feet retain extra digit-like rays.','前足保留额外的趾状分支。'),
'chalicotherium':('Hind feet retain four claw-bearing rays rather than the three in the earlier brief.','后足保留四个带爪趾状分支，与原简报的三个存在差异。'),
'metoposaurus':('Foot separation and digit detail remain approximate.','足趾分离和细节仍是近似表达。'),
'castoroides':('Toe detail is retained; local repair trials were reverted after reducing neighboring-toe quality.','趾部细节保持原版；局部试修影响邻趾轮廓，已回退。'),
'deinocheirus':('Hand/foot digits remain approximate; earlier local repair did not improve the display.','手足趾式仍是近似表达；此前局部修补未改善展示。'),
'parasaurolophus':('Forehands are modestly compacted; four front lobes remain. This is a visual adjustment.','前掌做了轻量收拢，仍保留四个前端分叶，属于观感调整。'),
'inostrancevia':('Duplicate inner long sabers are retracted; short residual roots and lip irregularities remain at close range.','重复内侧长剑齿已收回；近景仍有短牙根和唇部不规则。'),
'quetzalcoatlus':('Duplicate tall wing rods are tapered and shortened; small folded projections remain. Full wing anatomy was not rebuilt.','重复高耸翼杆已渐缩收短，仍有小型折叠状突起，未重建完整翼部解剖。'),
'mosasaurus':('Dental details are approximate and unsuitable for faithful dental closeups.','牙列细节为近似表达，不用于精确牙列特写。'),
'tylosaurus':('Dental details are approximate and unsuitable for faithful dental closeups.','牙列细节为近似表达，不用于精确牙列特写。'),
}
def main():
    lp=FOLDER/'integration-ledger.json';ledger=json.loads(lp.read_text());pairs={r['id']:r for r in json.loads((FOLDER/'evidence/source-reopen.json').read_text())['models']}
    mp=ROOT/'assets/manifest.json';mt=mp.read_text();manifest=json.loads(mt);old={r['id']:r for r in manifest['assets']};rows={};posters={};files=[]
    assert len(ledger['models'])==36 and len(set(r['id'] for r in ledger['models']))==36
    for r in ledger['models']:
        id=r['id'];a=copy.deepcopy(old[id]);pair=pairs[id];assert pair['glb_sha256']==r['glb_sha256'] and pair['reopened']
        for key in ('approval_provenance','production_release','production_posters','production_acceptance_adapter','production_provenance','qa','card_preview','turntable','wheelSpec','generator','generator_config','generator_sha256','generator_dependencies','config_sha256','revision_provenance','successor_provenance','frozen_scientific_scope','source_publication_status','reconstruction_notes','acceptance_scope','scientific_scope','credits'):
            a.pop(key,None)
        if id=='gastornis':a['name']={'en':'Diatryma gigantea','zh':'Diatryma gigantea（始新世巨鸟）'}
        name=a['name']['en'];en,zh=CAVEATS.get(id,('Fine anatomy, soft tissues, pose and colour remain artistic interpretations.','细部解剖、软组织、姿态与配色属于艺术解释。'))
        if id=='gastornis':en='Diatryma gigantea is the adopted identity; the historical Gastornis stable URL is retained. '+en;zh='采用 Diatryma gigantea 分类，保留历史目录链接。'+zh
        a['description']={'en':f'{name}-inspired whole-animal display prop, developed from an external Meshy base with Blender refinement. {en} Dimensions are illustrative authored asset scale, not verified life size or specimen measurements.','zh':f'{a["name"]["zh"]}启发的完整活体展示道具，由外部 Meshy 底模经 Blender 精修。{zh}尺寸为美术设定，不是经验证的动物或标本实测尺寸。'}
        directory=f'assets/revisions/{RELEASE}/{id}';a.update(glb=r['glb'],blend=pair['blend'],preview=directory+'/preview.png',revision=RELEASE,dimensions=r['bounds']['dimensions'],bounds_glb_m={'min':r['bounds']['min'],'max':r['bounds']['max']},triangles=r['bounds']['triangles'],primitives=r['bounds']['primitives'],material_count=r['bounds']['material_count'],units='m',quality_status='user_accepted_general_display_with_limits',scale_scope=r['scale_scope'])
        a['scientific_scope']={'scope':'Whole-animal artistic display; not exact specimen reconstruction.','artistic_interpretation':'Colour, pose, soft tissues and fine anatomy are artistic. '+en,'measurement_scope':r['scale_scope'],'limits':'Historical anatomy findings remain applicable. General-display acceptance does not establish exact anatomy, animation suitability, physical-device performance or scientific certification.'}
        a['acceptance_scope']='User authorized general-display integration on 2026-10-31. Historical PASS_WITH_LIMITS or anatomy HOLD is retained in the integration ledger; later pragmatic review admitted nine unchanged and three locally modified models. Source review applies to its own hash; fresh integration checks cover scale, grounding, browser delivery and captured presentation.'
        a['revision_provenance']={'author':a.get('author',manifest.get('author','Leon Made This / s010s')),'source_url':'https://github.com/s010s/lowpoly-vault','changes':'Adopt accepted final candidate; add uniform authored scale, Y-axis orientation and grounded origin. Binary geometry, UV, material and embedded image bytes remain unchanged. Editable source is a clean import of this final GLB.','original_author':old[id].get('author','Leon Made This / s010s'),'original_source_url':old[id].get('source_url','https://github.com/s010s/lowpoly-vault'),'original_glb_sha256':old[id]['sha256']['glb'],'previous_glb_path':old[id]['glb'],'previous_blend_path':old[id]['blend'],'previous_preview_path':old[id]['preview'],'external_provider':'Meshy','accepted_candidate_glb_sha256':r['source_glb_sha256']}
        a['integration_ledger']=str(lp.relative_to(ROOT));a['file_sizes']={'glb':r['glb_bytes'],'blend':pair['blend_bytes']};a['glb_bytes']=r['glb_bytes'];a['blend_bytes']=pair['blend_bytes'];a['sha256']={'glb':r['glb_sha256'],'blend':pair['blend_sha256']}
        a['model_network_payload']={'glb_bytes':r['glb_bytes'],'external_texture_bytes':0,'total_model_bytes':r['glb_bytes'],'embedded_images':r['bounds']['embedded_images'],'scope':'Model payload only. Excludes shared JS, poster images and optional Blend/ZIP downloads; not GPU memory.'}
        rows[id]=a
        for role in ('wheel','detail'):
            src=ROOT/f'qa/model-image-capture/{id}/{role}.png';b=src.read_bytes();dest=f'gallery/revisions/{RELEASE}/{id}/{role}.png';p=ROOT/'site/public'/dest;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_bytes(b);files.append({'path':dest,'sha256':sha(b),'bytes':len(b)})
            if role=='detail':shutil.copyfile(src,ROOT/a['preview']);a['sha256']['preview']=sha(b)
        posters[id]={'source_glb_sha256':r['glb_sha256'],'render_route':'webgl-manual-v1','detailPresentation':{'revision':2,'minimum_margin':0.025,'screen_shift':0.06,'raster_size':1536},'wheel':f'gallery/revisions/{RELEASE}/{id}/wheel.png','detail':f'gallery/revisions/{RELEASE}/{id}/detail.png'}
    spans,_=prior.items(mt,prior.members(mt)['assets'][0]);result=prior.edits(mt,[(a,b,prior.rendered(rows[v['id']],mt,a)) for a,b,v in spans if v['id'] in rows]);newspans,_=prior.items(result,prior.members(result)['assets'][0]);assert [x[2]['id'] for x in spans]==[x[2]['id'] for x in newspans]
    untouched=0
    for oldspan,newspan in zip(spans,newspans):
        if oldspan[2]['id'] not in rows:assert mt[oldspan[0]:oldspan[1]]==result[newspan[0]:newspan[1]];untouched+=1
    assert untouched==716
    rp=ROOT/'site/public/gallery/resources.json';resources=prior.preserve_resources(rp.read_text(),posters,files)
    assert not any(word in json.dumps(rows) for word in ['drive.google','/workspace/','task_id'])
    mp.write_text(result);rp.write_text(resources)
    (FOLDER/'evidence/catalog-overlay.json').write_text(json.dumps(dict(total_ids=752,replaced_ids=list(rows),untouched_manifest_rows=untouched,untouched_row_bytes=True,historical_resources_preserved=True,new_posters=len(files)),indent=2)+'\n')
if __name__=='__main__':main()
