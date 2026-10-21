from pathlib import Path
import json,hashlib,struct
Q=Path(__file__).resolve().parent;I=json.loads((Q/'final-intake.json').read_text());W=Path(I['worktree']);H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
notes={
'kerygmachela':[
'Complete body retained, paired curved spinose appendages, oval lateral flap envelope and single median tail; no clipping.',
'Rear three-quarter separates long single tail from flaps; axial tubercle rows and paired underside legs readable.',
'Anterior lobe, paired appendages, low dark ventrolateral eye regions and rostral spines visible; no extra globular eyes.',
'Short legs sit below flaps; flattened soft trunk and long median tail are not a crustacean plate stack.',
'Tail base is one median solid; paired limbs below broad flaps, no paired-tail invention.',
'Eleven repeated paired flaps and eleven four-cue axial rows are countable; oval envelope broadest anterior-middle.',
'Relief and appended structures remain legible without palette; no material-only anatomical substitute.',
'Single tail and two frontal appendages remain distinct; open spaces between spines and silhouette breaks retained.'],
'pambdelurion':[
'Thick annulated trunk, broad lateral flaps and stout legs; oral structure restrained below head instead of conceptual forward horn.',
'Two short terminal lobes are distinct from Kerygmachela tail; no added eyes.',
'Six cephalic spines arranged in two groups, paired flexible frontal appendages, ventral oral disk with fine rim cues.',
'Eleven short legs per side beneath flaps; dorsal annulations are geometric; small ventral oral projection visible.',
'Paired short posterior lobes and broad trunk are visible, not one elongate tail.',
'Eleven paired flaps, soft cigar-like trunk and paired three-tip appendages readable.',
'Annulations, cephalic spines, flaps and oral position remain clear independent of palette.',
'Opening between frontal appendages and fine three-tip terminal silhouettes survive.'],
'aegirocassis':[
'Elongate central carapace and two levels of lateral flaps; long filter structures visible below anterior shield.',
'Blunt terminal body and dorsal band cues; no tail fan; distinct second flap level.',
'Paired lateral shields and dorsal/ventral flap planes are visible; filters narrow in this projection.',
'Carapace reaches forward roughly trunk length; ten upper/lower flap stations and blunt terminal region. Support article count is not resolved here.',
'Dorsal blade cues and two flap planes clear; no unexpected eyes or fan at posterior.',
'Ten dorsal band stations and central carapace ridge; bilateral shield outline. Filter supports naturally hidden in dorsal view.',
'Large shape and thin filter geometry are real surfaces, not material-only cards.',
'Full flap array and filter rods have open silhouettes; small support segmentation still not demonstrable.'],
'arthropleura':[
'Trilobed plated trunk, narrow wingless collum, short numerous legs, club eyes and7-bulge antennae. Head conspicuously exposed ahead of collum.',
'Posterior plate decrease and terminal region visible; repeated lateral wings and legs separate.',
'Flat head, narrow collum arch, two club-tipped stalks and alternating limb article regions visible.',
'Low elongated24-unit trunk and repeated legs; head projects well ahead of collar.',
'Paired lateral paratergites and low central core; no spurious terminal leg pair.',
'24 dorsal units and narrowing posterior body; head is mostly visible anterior to collum, not mostly covered as frozen brief requires.',
'Relief is geometry; low tubercles still present but understated; anterior head-cover discrepancy remains.',
'Many short legs and antenna bulges readable; broad head projection ahead of collar remains.']}
details={'kerygmachela':'Underside detail confirms two low elongated eye lobes under appendage bases, paired rostral spines and small central ventral mouth. Not extra globular concept eyes.','pambdelurion':'Underside detail confirms shallow oral disk with radial triangular rim cues, six cephalic spines and distal3-tip appendages. About16 is declared simplification, not invariant plate count.','aegirocassis':'Detail permits five long endites per side and fine spaced setal cues; supports look continuous and seven anatomical articles cannot be counted confidently. Additional independent exact-GLB side closeup requested, no model change.','arthropleura':'Underside detail resolves seven physical bulges per antenna with narrow necks and leg material regions. Club eyes are separate from antennae. This does not repair the head being mostly outside the collum in top/hero.'}
assets=[]
for it in I['assets']:
 a=it['asset_id'];manifest=json.loads((W/it['views']/'render-manifest.json').read_text());viewnames=['hero','reversehero','front','side','rear','top','clay','silhouette'];frames=[]
 for name,note in zip(viewnames,notes[a]):
  p=W/it['views']/(name+'.png');sha=H(p);entry=next(x for x in manifest['frames']if x['id']==name);assert sha==entry['sha256'];dims=struct.unpack('>II',p.read_bytes()[16:24]);assert dims==(512,512)
  frames.append({'view':name,'path':str(p),'sha256':sha,'dimensions':dims,'personally_viewed':True,'observation':note})
 sheet=W/it['views']/'contact-sheet.png';detail=W/it['detail']/'detail.png';assets.append({'asset_id':a,'revision':it['revision'],'glb_sha256':it['glb_sha256'],'frames':frames,'sheet':{'path':str(sheet),'sha256':H(sheet),'personally_viewed':True,'not_a_substitute_for_individual_frames':True},'detail':{'path':str(detail),'sha256':H(detail),'personally_viewed':True,'observation':details[a]},'visual_status':'PASS'if a in ['kerygmachela','pambdelurion']else'PENDING_ADDITIONAL_MORPHOLOGY_DIAGNOSTIC','concept_and_primary_references':'See unchanged reference-preflight-checkpoint.json, independently viewed before final intake.'})
r={'source_commit':I['source_commit'],'authoritative_session_utc_window':'2026-10-21T03:51:00Z/2026-10-21T03:54:00Z','personally_viewed_final_individual_frames':32,'personally_viewed_final_lossless_sheets':4,'personally_viewed_final_details':4,'not_hardware_or_scene_test':True,'assets':assets}
(Q/'individual-frame-inspection.json').open('x').write(json.dumps(r,indent=2)+'\n')
print('Recorded32 individual frames +4 sheets +4 details, with exact hashes and independent observations.')
