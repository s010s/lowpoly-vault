# SPDX-License-Identifier: MIT
"""Package actual evidence without granting independent approval."""
import hashlib,json,shutil,sys
from pathlib import Path
from PIL import Image
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
W=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import audit_glb
ATTEMPTS={'calceola':'attempt-03','favosites':'attempt-02','opabinia':'attempt-01','choia':'attempt-02'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def file(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def main():
    access=json.loads((W/'preflight.json').read_text())['reference_access_this_turn']
    summary=[]
    for s,a in ATTEMPTS.items():
        d=ROOT/'assets/candidates/continuous-small-life-round02-20261018/batch-04'/s/'r001'/a
        work=W/s/'r001';plan=ROOT/'production/continuous-small-life-round02-20261018/items'/s
        q=json.loads((d/'qa.json').read_text());g=audit_glb(d/(s+'.glb'),14000,6,30)
        source=json.loads((d/'technical/source-export.json').read_text())
        rt=json.loads((W/'runtime-attempt-02'/(s+'.json')).read_text())
        runtime=rt['loaded'][0]
        dims=g['bounds_m']['size']
        errors=list(g['errors'])+list(source['errors'])
        for letter in ('a','b'):
            rebuild=json.loads((d/'technical'/('rebuild-'+letter+'.json')).read_text())
            if rebuild['errors'] or not rebuild['semantic_match'] or rebuild['glb_sha256']!=g['sha256']:errors.append('Rebuild '+letter+' mismatch')
        if runtime['glb_sha256']!=g['sha256'] or rt['errors'] or rt['failed']:errors.append('Runtime binding/errors')
        if runtime['triangles']!=g['scene_triangles'] or runtime['vertices']!=g['unique_position_accessor_vertices']:errors.append('Loader geometry count mismatch')
        for side in ('min','max'):
            if max(abs(runtime['bounds'][side][i]-g['bounds_m'][side][i]) for i in range(3))>1e-6:errors.append('Loader bounds mismatch')
        if q['khronos_validator']['num_errors'] or q['khronos_validator']['num_warnings']:errors.append('Khronos issues require review')
        if g['bytes']>1000000:errors.append('GLB byte ceiling')
        frames=json.loads((d/'views/manifest.json').read_text())
        if frames['glb_sha256']!=g['sha256'] or frames['turntable_frames']!=0:errors.append('View source/count mismatch')
        required=['hero','reversehero','front','side','rear','top','clay','silhouette']
        if [f['view'] for f in frames['frames']]!=required:errors.append('Required fixed views differ')
        for f in frames['frames']:
            if sha(d/'views'/f['path'])!=f['sha256']:errors.append('Stale frame '+f['path'])
        hero=d/'views/preview-hero.png';image=Image.open(hero)
        if image.mode!='RGBA' or image.getchannel('A').getextrema()!=(0,255):errors.append('Transparent hero alpha missing')
        shutil.copyfile(hero,d/'preview-hero.png')
        # Metadata is packaging; the delivered Blend and GLB bytes remain unchanged.
        meta=json.loads((d/'metadata.json').read_text())
        meta.update(attempt=a,preview=str((d/'preview-hero.png').relative_to(ROOT)),exporter=g['generator'],threejs='0.180.0',independent_acceptance='pending parent-dispatched Luna xhigh QA',reference_access_this_run=access[s],geometry_metrics={'authored_vertices':sum(p['vertices'] for p in q['source']['parts']),'evaluated_vertices':sum(p['vertices'] for p in source['source_audit']['parts']),'exported_position_vertices':g['unique_position_accessor_vertices'],'triangles':g['scene_triangles'],'materials':g['materials'],'primitives':g['scene_primitives_estimated_base_draw_calls'],'bytes':g['bytes']},texture_metrics={'count':0,'encoded_bytes':0,'decoded_bytes':0},dimensions_measured_glb_m=dims,nominal_scale_note='Art direction, not fossil measurements; placement and measured model bounds are separate.',dependency_sha256={str(p.relative_to(ROOT)):sha(p) for p in [W/'build_batch04.py',ROOT/'production/small-fauna-trio-v2/build_trio.py',ROOT/'scripts/asset_common.py',ROOT/'scripts/qa_glb.py',work/(a+'-config.json')]},provenance={'geometry':'original procedural construction; existing MIT Part utility reused from this repository','materials':'original palette only; no external image, texture, mesh or scan','code_license':'MIT','asset_license':'CC-BY-4.0','attribution':'Leon Made This / s010s'},runtime_evidence=file(W/'runtime-attempt-02'/(s+'.json')),source_warnings_review={'smooth_normals':'Intentional organic smoothing on closed meshes; reviewed in clay, color and actual GLB views.','mounting':'Opabinia lowest glTF Y=0.005m is intentional free-swimming mount; its root remains identity at the documented body-centreline mounting pivot.' if s=='opabinia' else 'Grounded meshes have lowest authored Z=0 and corresponding exported glTF Y=0.'})
        save(d/'metadata.json',meta)
        brief=json.loads((plan/'brief.json').read_text())
        artifacts={'glb':file(d/(s+'.glb')),'source':file(d/(s+'.blend')),'generator':file(W/'build_batch04.py'),'config':file(work/(a+'-config.json')),'brief':file(plan/'brief.json'),'references':file(plan/'references.json'),'metadata':file(d/'metadata.json'),'cover':file(d/'preview-hero.png'),'view_manifest':file(d/'views/manifest.json'),'runtime':file(W/'runtime-attempt-02'/(s+'.json'))}
        stages={}
        for stage in ('technical','visual','factual','specification','runtime_parse','gpu','scene'):
            stages[stage]={'status':'unknown','reviewer':None,'subject':None,'evidence':[],'inspected_references':[],'criteria':[{'id':x['id'],'status':'unknown','evidence':[],'note':'Pending parent-dispatched independent QA; maker evidence is available.'} for x in brief['criteria'] if x['stage']==stage],'note':'Pending independent acceptance; maker reports are linked separately.'}
        cand={'schema_version':1,'asset_id':s,'revision':'r001','attempt':a,'maker':{'id':'GPT-6.1-Sol-medium-batch04','task_id':'01a15047-91cd-7261-916c-9690e749200e'},'artifacts':artifacts,'supersedes':None,'textures':[],'evidence':[],'stages':stages,'blockers':['Independent visual/factual/specification acceptance pending parent dispatch.'],'approval':{'status':'pending'},'frozen_plan_commit':'bc73f5b5c2b085f538ee0f076f087f1603498dcb','parent_claim_commit':'7060ae0e5ee2c0a4c164ab1439c253d46159b561','contract_note':'Exact user-selected round02 frozen brief retained unchanged. Historical validate_candidate.py expects 2+ turntable frames and additional views; this task explicitly requires zero turntable and eight fixed views. Its result is retained, never rewritten as PASS.'}
        save(work/'candidate.json',cand)
        checks={'schema_version':1,'scope':'batch04 maker automated checks only; does not grant independent visual/factual/spec approval','asset_id':s,'attempt':a,'glb_sha256':g['sha256'],'status':'fail' if errors else 'pass','errors':errors,'khronos':q['khronos_validator'],'source_export':file(d/'technical/source-export.json'),'rebuilds':[file(d/'technical'/('rebuild-'+x+'.json')) for x in ('a','b')],'runtime':file(W/'runtime-attempt-02'/(s+'.json')),'root_units_axes':'identity EXPORT root, metric 1.0; source/export and loader bounds compared','source_boundary_edges':sum(p['boundary_edges'] for p in q['source']['parts']),'source_nonmanifold_edges':sum(p['nonmanifold_edges'] for p in q['source']['parts']),'warnings_review':meta['source_warnings_review'],'limits':{'triangles':14000,'bytes':1000000,'materials':6,'primitives':30,'textures':0},'source_counts':meta['geometry_metrics'],'actual_bounds_glb_m':g['bounds_m']}
        save(d/'technical/maker-checks.json',checks)
        assert not errors,errors
        summary.append({'asset_id':s,'attempt':a,'bundle':d.relative_to(ROOT).as_posix(),'candidate_record':str((work/'candidate.json').relative_to(ROOT)),'glb_sha256':g['sha256'],'bytes':g['bytes'],'triangles':g['scene_triangles'],'source_vertices':meta['geometry_metrics']['authored_vertices'],'exported_vertices':g['unique_position_accessor_vertices'],'materials':g['materials'],'primitives':g['scene_primitives_estimated_base_draw_calls'],'blender_bounds_m':q['source']['bounds_blender_m'],'checks':file(d/'technical/maker-checks.json')})
    scene=json.loads((W/'runtime-attempt-02/scene.json').read_text())
    assert scene['instances']==12 and not scene['errors'] and not scene['failed']
    assert all(v['triangles']==3*sum(s['triangles'] for s in summary)+2 and v['calls']==3*sum(s['primitives'] for s in summary)+1 for v in scene['views'])
    save(W/'delivery-index.json',{'schema_version':1,'status':'candidate-awaiting-parent-independent-QA','assets':summary,'scene':{'instances':12,'preserved_metre_scale':True,'offsets_only_no_normalization':True,'calls':scene['views'][0]['calls'],'triangles':scene['views'][0]['triangles'],'renderer':scene['renderer'],'report':file(W/'runtime-attempt-02/scene.json'),'limitation':'Functional software WebGL scene only; no physical GPU performance or cross-period coexistence claim.'}})
    # Bind every runtime original screenshot, including ordinary and near views.
    save(W/'runtime-attempt-02/hashes.json',{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted((W/'runtime-attempt-02').iterdir()) if p.is_file() and p.name!='hashes.json'})
if __name__=='__main__':main()
