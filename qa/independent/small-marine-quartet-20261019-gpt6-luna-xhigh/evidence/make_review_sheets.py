#!/usr/bin/env python3
"""Make native-pixel 12-view review sheets; originals remain untouched and hash-bound."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path.cwd()
QA=Path('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence')
BASE=Path('production/concept-small-marine-quartet-20261019')
VIEWS=['concept-match','hero','reversehero','front','rear','left','right','top','bottom','clay','clayalt','wire']

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

assets=[]
for asset,revision in [('emeraldella','r002'),('burgessia','r002'),('tuzoia','r003'),('sanctacaris','r002')]:
    frozen=BASE/asset/revision
    independent=QA/'renders'/asset
    manifest=json.loads((independent/'render-manifest.json').read_text())
    frame_by_view={row['view']:row for row in manifest['frames']}
    source_rows=[]
    canvas=Image.new('RGB',(2048,1632),'#e8e4dc')
    draw=ImageDraw.Draw(canvas)
    for i,view in enumerate(VIEWS):
        if view=='concept-match':
            path=frozen/'proof/concept-match.png'
            frozen_manifest=json.loads((frozen/'proof/render-manifest.json').read_text())
            frame=next(row for row in frozen_manifest['frames'] if row['view']=='concept-match')
            expected=frame['sha256']
        else:
            path=independent/f'{view}.png'
            frame=frame_by_view[view]
            expected=frame['sha256']
        if sha(path)!=expected:raise SystemExit(f'{asset}/{view}: evidence frame hash mismatch')
        with Image.open(path) as source:
            if source.size!=(512,512):raise SystemExit(f'{asset}/{view}: unexpected frame size {source.size}')
            image=source.convert('RGB')
            x=(i%4)*512;y=(i//4)*544
            canvas.paste(image,(x,y+32))
            draw.text((x+8,y+8),f'{asset} {revision} / {view}',fill='#16232b')
        source_rows.append({'view':view,'path':path.as_posix(),'sha256':expected,'width':512,'height':512,'origin':'producer proof bound to selected GLB' if view=='concept-match' else 'fresh independent clean GLB import render'})
    output=QA/'renders'/f'{asset}-review-sheet.png'
    canvas.save(output,format='PNG',optimize=True)
    assets.append({'asset_id':asset,'revision':revision,'source_glb_sha256':manifest['subject']['glb_sha256'],'independent_render_manifest':(independent/'render-manifest.json').as_posix(),'independent_render_manifest_sha256':sha(independent/'render-manifest.json'),'views':source_rows,'review_sheet':output.as_posix(),'review_sheet_dimensions_px':list(canvas.size),'review_sheet_sha256':sha(output),'original_frames_rescaled_or_modified':False})

result={'schema_version':1,'kind':'independent_visual_review_sheets','method':'Each 512×512 source frame is pasted at native pixel dimensions with labels in a separate 32px row. The 11 fresh frames are from independently imported exact GLBs; concept-match is the original frame whose source manifest binds the same exact GLB. Sheets are navigation aids; the original frames remain available and unchanged.','view_order':VIEWS,'assets':assets}
manifest_path=QA/'review-sheet-manifest.json'
manifest_path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'pass','assets':len(assets),'output':manifest_path.as_posix()},indent=2))
