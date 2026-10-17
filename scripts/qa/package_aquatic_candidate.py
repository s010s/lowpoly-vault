# SPDX-License-Identifier: MIT
"""Package maker evidence without asserting independent visual approval."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
ROOT=Path(__file__).resolve().parents[2]
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
for slug in ('bothriolepis','waptia'):
 d=ROOT/'assets/prehistoric/fauna'/slug; views=d/'views-r001-final'; brief=json.loads((d/'execution-brief.json').read_text()); meta=json.loads((d/'metadata.json').read_text()); qa=json.loads((d/'qa.json').read_text())
 # The seventh sheet panel uses an exact imported-GLB image at supported sizes.
 image=Image.open(views/'hero.webp').convert('RGB')
 background=Image.new('RGB',image.size,'#E8E4DC'); mask=ImageChops.difference(image,background).convert('L').point(lambda x:255 if x>6 else 0); image=image.crop(mask.getbbox())
 scale=Image.new('RGB',(1024,500),'#E8E4DC'); draw=ImageDraw.Draw(scale)
 font=ImageFont.truetype(FONT,20)
 draw.text((24,20),'Supported view envelope • exact GLB render',fill='#35413A',font=font)
 x=24
 for size in (80,160,240,360):
  thumb=image.copy(); thumb.thumbnail((size,size),Image.Resampling.LANCZOS); scale.paste(thumb,(x,95+(360-thumb.height)//2)); draw.text((x,465),f'{size} px',fill='#35413A',font=font); x+=size+32
 scale.save(d/'qa-supported-scale.webp',quality=92,method=6)
 sheet=Image.new('RGB',(1536,1120),'#E8E4DC'); ds=ImageDraw.Draw(sheet); title=ImageFont.truetype(FONT,29); label=ImageFont.truetype(FONT,20)
 ds.text((24,20),f'{meta["name"]["en"]} • r001 • candidate, independent review pending',fill='#35413A',font=title)
 for i,name in enumerate(('hero','front','right','rear','top','clay')):
  x=(i%3)*512; y=64+(i//3)*512
  im=Image.open(views/f'{name}.webp').convert('RGB').resize((460,460),Image.Resampling.LANCZOS); sheet.paste(im,(x+26,y+28)); ds.text((x+24,y+4),name.upper(),fill='#35413A',font=label)
 sheet.save(d/'qa-contact-sheet.webp',quality=92,method=6)
 # All approval fields remain pending. Technical evidence is present for a
 # reviewer to verify; machine tests cannot approve visual craft or identity.
 candidate=json.loads((ROOT/'schemas/templates/candidate.template.json').read_text())
 candidate.update(asset_id=slug,revision='r001',maker={'id':'model-small-aquatic-pair','task_id':'/root/model_small_aquatic_pair'})
 candidate['artifacts']={k:rec(p) for k,p in {'glb':d/f'{slug}.glb','source':d/f'{slug}.blend','brief':d/'execution-brief.json','references':d/'references.json','generator':ROOT/'scripts/models/small_fauna/build_aquatic_pair.py','config':d/'build-config.json'}.items()}
 for stage,record in candidate['stages'].items():
  record['criteria']=[{'id':c['id'],'status':'unknown','evidence':[],'note':'Pending independent review / designated runtime evidence.'} for c in brief['criteria'] if c['stage']==stage]
 candidate['approval']={'status':'pending'}; candidate['blockers']=[]
 subject={'revision':'r001','glb_sha256':sha(d/f'{slug}.glb'),'brief_sha256':sha(d/'execution-brief.json'),'references_sha256':sha(d/'references.json')}
 candidate['evidence']=[{'id':'exact-glb-six-views','stage':'visual','kind':'render_manifest','subject':subject,**rec(views/'render-manifest.json')}]
 candidate['stages']['visual']['evidence']=['exact-glb-six-views']
 (d/'candidate.json').write_text(json.dumps(candidate,indent=2,ensure_ascii=False)+'\n')
 reports={name:json.loads((d/name).read_text()) for name in ('source-export.report.json','glb-roundtrip.report.json','reproducibility.report.json','gltf-validator.report.json')}
 metrics={'schema_version':1,'asset_id':slug,'revision':'r001','subject_glb_sha256':sha(d/f'{slug}.glb'),'status':'machine_checks_complete_independent_review_pending','triangles':qa['glb']['scene_triangles'],'source_vertices':sum(p['vertices'] for p in qa['source']['parts']),'export_position_vertices':qa['glb']['unique_position_accessor_vertices'],'materials':qa['glb'].get('materials'),'primitives':qa['glb']['scene_primitives_estimated_base_draw_calls'],'glb_bytes':(d/f'{slug}.glb').stat().st_size,'blend_bytes':(d/f'{slug}.blend').stat().st_size,'dimensions_glb_m':meta['dimensions'],'nominal_body_length_m':meta['nominal_body_length_m'],'texture_bytes':0,'animation_clips':0,'rigged':False,'checks':{'source_export':reports['source-export.report.json']['status'],'clean_reimport':reports['glb-roundtrip.report.json']['status'],'reproducibility':reports['reproducibility.report.json']['status'],'rebuild_byte_identical':reports['reproducibility.report.json']['byte_identical'],'khronos_errors':reports['gltf-validator.report.json']['issues']['numErrors'],'khronos_warnings':reports['gltf-validator.report.json']['issues']['numWarnings']},'warning_disposition':[{'warning':'Negative lowest vertical coordinate / verify mount','disposition':'Expected: the frozen aquatic brief specifies a suspended body-center mounting origin, not ground contact. The identity root stays at the declared body center.'}],'independent_visual_factual_specification':'pending','target_threejs_runtime':'pending','scene_test':'pending','artistic_scope':'Static artistic interpretation for an imaginative children’s prehistoric world; neither strict scientific reconstruction nor animation-ready model.'}
 (d/'technical-summary.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False)+'\n')
 readme=f'''# {meta['name']['en']} · static artistic interpretation\n\nOriginal low-poly prop for an imaginative children's prehistoric world. Inspired by {brief['subject']['taxon']}; color, fine details and pose are artistic. This is not a strict scientific reconstruction.\n\n- Editable source: `{slug}.blend`\n- Standalone web asset: `{slug}.glb`\n- Generator: `scripts/models/small_fauna/build_aquatic_pair.py` and its adjacent geometry helper\n- Rebuild parameters/material palette: `build-config.json`\n- Transparent source thumbnail: `preview-hero.png`\n- Six exact-GLB diagnostic views and hashed manifest: `views-r001-final/`\n- Contact sheet: `qa-contact-sheet.webp`; supported-size inspection: `qa-supported-scale.webp`\n- Frozen art brief/reference ledger: `brief.json`, `references.json`, `freeze.json`; `execution-brief.json` adds exact deliverable hashes without changing the art brief\n\nMeasured export: {metrics['triangles']:,} triangles, {metrics['primitives']} primitives, 4 opaque palette materials, {metrics['glb_bytes']:,} bytes. Nominal body length {meta['nominal_body_length_m']} m. Asset coordinates are meters, glTF +Y up / +Z forward. The identity root is the declared suspended body-center mounting point; the asset is not ground-aligned.\n\nSource/export count and bounds, clean GLB reimport, official Khronos format validation and a separately executed deterministic rebuild have completed. See `technical-summary.json` and the individual reports. Independent art/specification approval, actual target graphics runtime and repeated-scene review remain pending. The source image is not evidence of WebGL rendering. No rig or animation is included.\n\nGeometry and palette are original. Cited institutional/scientific references were consulted only; no third-party model, scan, image or texture is incorporated. Assets and rendered images: CC-BY-4.0, Leon Made This / s010s. Generator code: MIT. See the repository LICENSE and LICENSES directory.\n'''
 (d/'README.md').write_text(readme)
 print(slug,metrics)
