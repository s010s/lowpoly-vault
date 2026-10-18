# SPDX-License-Identifier: MIT
"""Compose exact-GLB diagnostic contact sheets and explicit recovery provenance."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,ast
R=Path(__file__).resolve().parents[1]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21)
for cat,a,rev in [('animals','juracimbrophlebia','r1'),('plants','asteroxylon','r2')]:
 d=R/'assets/prehistoric'/cat/a;q=R/'qa/small-fauna-v1'/a/'recovered-20261018'
 m=json.loads((d/'metadata.json').read_text());c=json.loads((q/'render-config.json').read_text())
 sheet=Image.new('RGB',(1088,682),'#eeeae2');draw=ImageDraw.Draw(sheet)
 draw.text((18,12),a+' / '+rev+' / exact-match GLB rebuilt 2026-10-18',font=big,fill='#263c34')
 draw.text((18,43),'Artistic interpretation | independent QA pending | GLB '+m['sha256']['glb'][:16],font=small,fill='#45554a')
 labels=['hero','front','right','rear','top','clay']
 for k,name in enumerate(labels):
  x=16+(k%4)*268;y=76+(k//4)*296
  im=Image.open(q/(name+'.png')).convert('RGB').resize((256,256),Image.Resampling.LANCZOS);sheet.paste(im,(x,y));draw.text((x+5,y+261),name.upper(),font=font,fill='#263c34')
 im=Image.open(q/'front.png').convert('RGB');di=ImageDraw.Draw(im)
 meters=.01 if a=='juracimbrophlebia' else .05;px=512*meters/c['camera']['orthographic_scale'];x0=30;y0=478
 di.line((x0,y0,x0+px,y0),fill='#263c34',width=4)
 for x in (x0,x0+px):di.line((x,y0-7,x,y0+7),fill='#263c34',width=3)
 di.text((x0,448),f'{meters*1000:.0f} mm',font=font,fill='#263c34')
 im.save(q/'scale.png');sheet.paste(im.resize((256,256),Image.Resampling.LANCZOS),(552,372));draw.text((557,633),'SCALE / FRONT',font=font,fill='#263c34')
 poster=Image.open(d/'preview-hero.png').convert('RGBA');bbox=poster.getbbox();trim=poster.crop(bbox)
 for size,xy in [(180,(825,377)),(80,(970,549))]:
  p=trim.copy();p.thumbnail((size,size));sheet.paste(p,xy,p)
 draw.text((825,633),'NORMAL VIEW: 180 / 80 px',font=small,fill='#263c34');sheet.save(q/'contact-sheet.png')
 report={'source_glb_sha256':m['sha256']['glb'],'six_rendered_views':labels,'scale_panel':'front view with accurate orthographic scale bar','scale_bar_m':meters,'scale_pixels_original_512':px,'scale_basis':'render-config.json camera.orthographic_scale','normal_view_projected_maxima_px':[180,80],'contact_sheet_sha256':hashlib.sha256((q/'contact-sheet.png').read_bytes()).hexdigest(),'poster_alpha_extrema':poster.getchannel('A').getextrema(),'poster_nonempty_alpha_bbox':bbox,'visual_approval':'independent review pending','provenance':'New evidence rendered from a regenerated GLB whose SHA256 matches the previously recorded original.'}
 (q/'contact-sheet.json').write_text(json.dumps(report,indent=2)+'\n')
 qa=json.loads((d/'qa.json').read_text());qa['recovery_comparison']=m['recovery'];qa['visual_review']={'status':'pending','maker_inspected':['hero'],'independent_review':'pending'};qa['previews']={'status':'rendered','source_glb_sha256':m['sha256']['glb'],'render_manifest':str((q/'render-manifest.json').relative_to(R)),'contact_sheet':str((q/'contact-sheet.png').relative_to(R)),'six_views':labels};qa['reviewed_warnings']=[{'warning':'Lowest Blender Z / glTF Y is negative','disposition':'Intentional body-center mounting pivot for the insect; this is a suspended static prop, not a ground-contact object.'}] if a=='juracimbrophlebia' else [];qa['threejs_runtime']={'status':'not_run','note':'Independent runtime QA remains pending.'};(d/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
 (d/'README.md').write_text(f'''# {a}: static artistic environment prop

This is an original stylized-inspired prop for an imaginative children's prehistoric world, not a strict scientific reconstruction. Color, pose, fine details and conservative restored parts are artistic. No rig or animation is included.

## Recovery provenance

The GLB was regenerated in Blender 4.3.2 from preserved source on 2026-10-18. Its SHA256 is **{m['sha256']['glb']}**, matching the previously recorded original GLB byte-for-byte. The editable .blend and rendered evidence are newly generated; their original-byte identity is not claimed.

The attached brief/reference package is **pilot-v002-recovered-20261018**, a disclosed reconstruction from planner commit `58e13487f6e8e2bdea2c7a6ee087e1a8e147275b`. It has new hashes and is not represented as the earlier brief's original bytes.

## Checks and limits

- {m['triangles']:,} exported triangles; {m['glb_bytes']:,} GLB bytes; four palette materials; five exported primitives
- Source/static GLB checks passed; the insect's negative lowest coordinate is its documented suspended mounting pivot
- Official Khronos validator: zero errors and zero warnings
- Six exact-export views plus transparent poster, calibrated scale panel and supported-size thumbnails are present
- Independent visual/basic-form review and target-runtime/scene QA remain pending; this is a candidate checkpoint, not a release approval

Generator: `scripts/models/build_small_insect_plant_pair.py`; final config: `production/insect-plant-build/{a}-{rev}.json`. Shared helper dependencies are retained at repository baseline `01c60dd85322932a967c4f2aa50045f2da1a25bd`.

Assets/previews: CC BY 4.0, attribution Leon Made This / s010s. Generator code: MIT. References were consulted only; no external artwork, model or texture is incorporated.
''')
for f in (R/'scripts').rglob('*.py'):ast.parse(f.read_text())
print('Contact sheets, candidate notes and syntax checks complete.')
