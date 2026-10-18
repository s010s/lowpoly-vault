# SPDX-License-Identifier: MIT
"""Bind the completed v2 candidate/evidence bytes without asserting user approval."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'production/small-fauna-trio-v2';ASSETS=ROOT/'assets/candidates/small-fauna-trio-v2';QA=ROOT/'qa/small-fauna-trio-v2'
QA.mkdir(parents=True,exist_ok=True)
def write(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def entry(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
for slug in ['diplomystus','burgessomedusa','kalligramma']:
 d=BASE/slug;a=ASSETS/slug
 refs=json.loads((d/'references.json').read_text());refs['schema_version']=1;write(d/'references.json',refs)
 brief=json.loads((d/'brief.json').read_text());brief['texture_policy']={'max_textures':1,'max_dimension':256,'max_total_bytes':65536,'max_decoded_bytes':524288};brief['artistic_choices']=list(dict.fromkeys(brief['artistic_choices']+['Original low-contrast pigment maps for fish and lacewing; mild portable transmission for jelly bell.']));write(d/'brief.json',brief)
 config=json.loads((d/'build-config.json').read_text());config['profile']='original pigment-mapped static mesh; jelly portable transmission';write(d/'build-config.json',config)
 files={role:entry(p) for role,p in {'glb':a/(slug+'.glb'),'source':a/(slug+'.blend'),'generator':BASE/'build_trio.py','config':d/'build-config.json','brief':d/'brief.json','references':d/'references.json','helper':ROOT/'scripts/asset_common.py'}.items()}
 freeze={'schema_version':1,'asset_id':slug,'revision':'v002','kind':'versioned-execution-brief-supplement','files':files,'source_contract':'meters; identity root at documented free-swimming/flying centerline; Blender Z-up/-Y-forward, GLB Y-up/+Z-forward','view_envelope_px':[80,240,480],'user_acceptance':'pending','publication_authorized':False,'supersedes_art_direction':'v001 rejected by user','claim_scope':'Stylized named-taxon-inspired static prop; no scientific reconstruction or animation-ready claim'}
 write(d/'freeze.json',freeze)
 textures=[entry(p) for p in a.glob('*pigment.png')]
 metadata=json.loads((a/'metadata.json').read_text());metadata['status']='candidate-awaiting-user-visual-review';metadata['textures']=textures;metadata['origin']='free-swimming/flying centerline; identity root';metadata['reconstruction_notes']='Colors, detailed proportions/pose, 96 jelly tentacles and vein/pigment simplification are artistic choices; consult source ledger for access limits.';metadata['preview']=(a/('preview-top.png' if slug=='kalligramma' else 'preview-hero.png')).relative_to(ROOT).as_posix();write(a/'metadata.json',metadata)
 qa=json.loads((a/'qa.json').read_text());qa['threejs_runtime']=json.loads((QA/'browser'/(slug+'.json')).read_text());qa['visual_review']={'status':'pending_user_acceptance','note':'Independent basic-form review is separate from user aesthetic acceptance. v001 user rejection is preserved.'};qa['warning_disposition']={'smooth_normals':'intentional refined low-poly bodies/organic appendages','negative_min_height':'free-swimming/flying mounting point, no ground-contact claim','thin_surfaces':'fish fin membranes and insect wings are closed; pigment maps replace old open eye-spot discs','transmission':'jelly uses portable KHR_materials_transmission; exact browser functional rendering verified, no physical GPU/performance claim'};write(a/'qa.json',qa)
 images=[entry(p) for p in sorted(a.glob('preview-*.png'))]+[entry(p) for p in sorted((QA/'browser').glob(slug+'-*.png'))]
 for p in a.glob('preview-*.png'):
  im=Image.open(p);assert im.mode=='RGBA'
  if 'silhouette' not in p.name:assert im.getchannel('A').getextrema()[0]==0
 write(QA/(slug+'-view-manifest.json'),{'asset_id':slug,'glb_sha256':files['glb']['sha256'],'frames':images,'turntable_frames':0,'source_render':'Blender4.3.2 Cycles CPU,640px32samples,Standard/None; transparent RGBA','browser_render':'Three.js0.180.0,software SwiftShader WebGL2; fixed views and80/160/240px plus480px inspection'})
 write(d/'candidate.json',{'schema_version':1,'asset_id':slug,'revision':'v002','maker':{'id':'cloud-maker','task_id':'small-fauna-trio-v2'},'artifacts':{k:{'path':v['path'],'sha256':v['sha256']} for k,v in files.items()},'textures':textures,'status':'candidate-awaiting-user-visual-review','approval':{'status':'pending'},'technical_evidence':{'khronos':entry(a/'gltf-validator.report.json'),'source_export':entry(QA/'final-validation-r2'/(slug+'-source-export.json')),'reproducibility':entry(QA/'final-validation-r2'/(slug+'-reproducibility.json')),'browser':entry(QA/'browser'/(slug+'.json')),'views':entry(QA/(slug+'-view-manifest.json'))},'blockers':[],'formal_gate_limitation':'Historical validate_candidate.py requires >=2 turntable frames and production full diagnostic coverage; user specifically requests zero sequence frames and practical bounded review. It is not reported as a passing approval gate.'})
# Clean presentation contact sheets, same neutral background as diagnostic browser.
for slug in ['diplomystus','burgessomedusa','kalligramma']:
 paths=sorted((ASSETS/slug).glob('preview-*.png'));canvas=Image.new('RGB',(1280,710),'#e8e4dc');draw=ImageDraw.Draw(canvas)
 for k,p in enumerate(paths):
  im=Image.open(p);im.thumbnail((320,320));x=k%4*320;y=k//4*355;canvas.paste(im,(x+(320-im.width)//2,y+(320-im.height)//2),im);draw.text((x+8,y+325),p.stem,fill='#30434b')
 canvas.save(QA/(slug+'-contact-sheet.jpg'),quality=92)
canvas=Image.new('RGB',(1200,870),'#e8e4dc');draw=ImageDraw.Draw(canvas)
for row,version in enumerate(['v1','v2']):
 for col,slug in enumerate(['diplomystus','burgessomedusa','kalligramma']):
  p=ROOT/('assets/candidates/small-fauna-trio-'+version)/slug/('preview-top.png' if slug=='kalligramma' else 'preview-hero.png');im=Image.open(p);im.thumbnail((385,385));x=col*400;y=row*435;canvas.paste(im,(x+7,y+5),im);draw.text((x+12,y+405),slug+' '+version+(' (rejected)' if row==0 else ' (candidate)'),fill='#30434b')
canvas.save(QA/'before-after.jpg',quality=95)
print('Frozen3 candidates and exact file/view bindings; user acceptance pending.')
