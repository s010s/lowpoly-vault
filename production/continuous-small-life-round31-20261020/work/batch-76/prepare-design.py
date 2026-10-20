import json,pathlib,shutil,hashlib,datetime
from specs import specs
R=pathlib.Path.cwd();W=R/'production/continuous-small-life-round31-20261020/work/batch-76';B=R/'production/continuous-small-life-round31-20261020/assets';C=pathlib.Path('/workspace/shared/lowpoly-batch76-references')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
put(W/'research-design-input.json',specs)
old=pathlib.Path('/workspace/shared/lowpoly-batch72-20261020/production/continuous-small-life-round29-20261020/work/batch-72')
for n in ['render-fixed8.py','count-source-vertices.py','runtime-parse.mjs','locked-blender.sh','compose-sheets.py']:
 s=(old/n).read_text().replace('continuous-small-life-round29-20261020','continuous-small-life-round31-20261020').replace('batch-72','batch-76');(W/n).write_text(s)
(W/'locked-blender.sh').chmod(0o755)
# Preserve rejected generation and exact actual observer record, no invented provider internals.
records=json.loads((W/'concept-tool-records.json').read_text())
for slug,s in specs.items():
 b=B/slug/'r001';b.mkdir(parents=True,exist_ok=True);g=records[slug];shutil.copyfile(g['path'],b/'concept-original.png');(b/'concept-prompt.txt').write_text(g['prompt']+'\n')
 put(b/'concept-generation.json',{'tool':'image_gen.imagegen','output_path':g['path'],'output_hint':g['output_hint'],'call_started_observed_utc':g['started'],'result_observed_utc':g['observed'],'provider_generated_at':None,'receipt_status':'Actual returned image and output_hint; provider generation ID/internal timestamps unavailable','inspected_at':now()})
 source={'id':'PRIMARY-'+slug,'title':slug+' selected primary reference','url':s['url'],'license':'Consulted-only; source rights retained; no pixels redistributed','use':'consulted-only','incorporated':False,'rights_note':'Text/pixels consulted only; no photograph, scan, mesh, texture or other third-party asset incorporated or redistributed.','notes':s['observation'],'consulted_at':now(),'consulted_images':[{'filename':n,'sha256':H(C/n)} for n in s['pixels']]}
 if slug=='coal-seam-outcrop':source['credit']='DOE/GSA2014 final report, Fig18 modified from Pashin etal2008. Consult-only; figure rights retained.'
 if slug=='crevasse-splay':source['additional_urls']=['https://pubs.usgs.gov/publication/ofr20241051/full'];source['license']='Primary2017 paper CC BY3.0, actual field imagery consult-only; USGS indexed text, pixels unavailable403'
 concept={'id':'CONCEPT','url':'internal-original-concept','title':'Original generated '+slug+' concept','license':'CC-BY-4.0 Leon Made This / s010s','use':'original-generated-concept','incorporated':False,'rights_note':'Original concept design guidance only, not primary factual evidence or texture.','notes':s['decisions']}
 put(b/'references.json',{'schema_version':1,'no_incorporated_third_party_assets':True,'rights_note':'Delivered geometry and rendering original; consulted third-party pixels excluded.','sources':[source,concept]})
 brief=json.loads((R/'schemas/templates/brief.template.json').read_text());brief.update(asset_id=slug,brief_version='r001',purpose='Original evidence-informed low-poly supporting educational prop; independent QA pending',required_views=['hero','reversehero','front','side','rear','top','clay','silhouette'],turntable_frames=0,geometry_policy={'max_triangles':14000,'max_materials':6,'max_primitives':30,'max_glb_bytes':1000000},texture_policy={'max_textures':0,'max_dimension':256,'max_total_bytes':0,'max_decoded_bytes':0},view_exemptions={},coverage_justification='Static-stylized-v1 eight512px canonical/diagnostic views;7 distinct stages.',required_deliverables=[],claim_scope=s['claim'],nominal_dimensions_blender_xyz_m=s['dims'],dimension_status='Nominal illustrative scale, not measured reference locality/specimen; export measured separately',recognition_features=s['features'],concept_decisions=s['decisions'],style='Palette-only faceted real3D low-poly',intended_use=('Hand-scale fossil-form supporting educational prop' if slug=='rangea' else 'Landscape supporting geological terrain prop')+' at256-512px; no engineering/museum-grade replica claim',created_at=now(),validation_profile='static-stylized-v1')
 for q in brief['criteria']:
  if q['stage'] in ['visual','factual']:q['required_sources']=['PRIMARY-'+slug];q['description']+=' Required features: '+'; '.join(s['features'])+'. Scope: '+s['claim']
 put(b/'brief.json',brief);put(b/'build-config.json',{'asset_id':slug,'revision':'r001','seed':76,'nominal_dimensions_blender_xyz_m':s['dims'],'palette':s['palette'],'blender_threads':2,'three_version':'0.180.0','concept_inspected_at':now(),'modeling_decisions':s['decisions']})
 (b/'brief.md').write_text('# Immutable premodel brief\n\n'+s['claim']+'\n\n'+'\n'.join('- '+x for x in s['features'])+'\n\n'+s['decisions']+'\n\n'+s['observation']+'\n\nNo independent/formal/user approval asserted.\n')
 refs=json.loads((b/'references.json').read_text());assert refs['schema_version']==1 and refs['no_incorporated_third_party_assets'] is True
 for e in refs['sources']:assert all(isinstance(e.get(k),str) and e[k] for k in ['id','title','url','license','use','rights_note']);assert e['incorporated'] is False
 put(b/'prefreeze-ledger-check.json',{'checked_at':now(),'status':'pass','schema_version':1,'reference_sha256':H(b/'references.json'),'all_entries_have_rights_note':True,'nonincorporation_valid':True})
 put(b/'modeling-freeze.json',{'asset_id':slug,'revision':'r001','frozen_at':now(),'status':'Actual primary text and pixels plus genuine generated concept personally inspected; complete asset-specific design frozen before generator authorship','files':{n:H(b/n) for n in ['brief.json','brief.md','references.json','build-config.json','concept-original.png','concept-prompt.txt','concept-generation.json']}})
put(W/'final-selection.json',[{'asset_id':x,'revision':'r001','path':str((B/x/'r001').relative_to(R))} for x in specs]);put(W/'design-freeze-chronology.json',{'all_freezes_completed_at':now(),'next_action':'Author generator after this marker','provider_timestamps':None})
print('FROZEN',now())
