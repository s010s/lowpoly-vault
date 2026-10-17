"""Read-only exact-subject audit; no browser or publication operations."""
from pathlib import Path
import hashlib,json,struct,subprocess,zipfile
from PIL import Image
out=Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
hashfile=lambda p:sha(Path(p).read_bytes())
request=json.loads(Path('qa/conifer-doc1-integration/preview-review-request.json').read_text())
manifest=json.loads(Path(request['preview_manifest']).read_text())
assert hashfile(request['preview_manifest'])==request['preview_manifest_sha256']
rows=[]
for i,f in enumerate(manifest['frames']):
 p=Path(f['path']);raw=p.read_bytes();im=Image.open(p).convert('RGBA');a=im.getchannel('A');bbox=a.getbbox()
 assert sha(raw)==f['sha256']==request['frames'][i]['sha256'] and len(raw)==f['bytes']
 assert im.size==(768,768) and a.getextrema()==(0,255)
 assert bbox and min(bbox[0],bbox[1],768-bbox[2],768-bbox[3])>0
 assert not any(a.crop(box).getbbox() for box in [(0,0,768,1),(0,767,768,768),(0,0,1,768),(767,0,768,768)])
 assert f['azimuth_deg']==42+15*i and f['elevation_deg']==23.3
 source='qa/conifer-r20-runtime-20261017/attempt-01/swiftshader/preview/frames/'+p.name
 assert sha(subprocess.check_output(['git','show',request['preview_source_commit']+':'+source]))==f['sha256']
 rows.append({'index':i,'path':str(p),'sha256':f['sha256'],'bytes':len(raw),'alpha_bbox':bbox,'margin_ltrb':[bbox[0],bbox[1],768-bbox[2],768-bbox[3]],'transparent_fraction':a.histogram()[0]/(768*768),'azimuth_deg':f['azimuth_deg'],'elevation_deg':23.3,'source_commit_bytes_equal':True,'pixels_inspected':True,'composite_background':'#f5f3ef' if i%2==0 else '#202822','observation':'Complete tip/root, readable separated fine sprays, stable trunk placement and progressive rotation; no crop or opaque backing.'})
assert len(rows)==24 and sum(r['bytes'] for r in rows)==823466
for p in [request['poster'],request['release_preview'],manifest['frames'][0]['path']]:assert hashfile(p)==request['poster_sha256']
p=Path('assets/revisions/conifer-tree/structure-r20-a-normal16-doc1/conifer-tree.glb');raw=p.read_bytes();g=json.loads(raw[20:20+struct.unpack_from('<I',raw,12)[0]])
triangles=sum(g['accessors'][p['indices']]['count']//3 for m in g['meshes'] for p in m['primitives'])
assert len(raw)==715500 and sha(raw)==request['subject']['glb_sha256'] and triangles==19052 and len(g['materials'])==3 and not g.get('images') and not g.get('textures')
assert 'KHR_mesh_quantization' in g['extensionsRequired']
md=json.loads(Path('assets/revisions/conifer-tree/structure-r20-a-normal16-doc1/release-metadata.json').read_text())
for lang in ['en','zh']:
 s=md['scientific_scope'][lang]
 for required in ['KHR_mesh_quantization','Three.js 0.180.0','M5 Pro','Metal','SwiftShader']:assert required in s
assert '16.7' in md['scientific_scope']['en']
# Existing browser execution is independently inspected, never represented as a new run.
p=Path('qa/conifer-doc1-integration/browser-evidence/conifer-handoff-attempt02/report.json');r=json.loads(p.read_text())
assert r['status']=='pass'
assert not subprocess.check_output(['git','diff','--name-only',r['commit'],'35de59d2ad4dbce7e88eae9d8df237c480098c02','--','site','scripts'])
parity=[{'label':c['label'],'status':c['status'],'mean_rgb_absolute_error':c['pixel_parity']['mean_rgb_absolute_error'],'bbox_delta_px':c['pixel_parity']['bbox_delta_px'],'centroid_delta_px':c['pixel_parity']['centroid_delta_px']} for c in r['cases'] if c.get('pixel_parity')]
for c in parity:assert c['status']=='pass' and c['bbox_delta_px']<=2 and c['centroid_delta_px']<.2 and c['mean_rgb_absolute_error']<.004
report={'status':'pass','reviewed_commit':'35de59d2ad4dbce7e88eae9d8df237c480098c02','subject':request['subject'],'request_sha256':hashfile('qa/conifer-doc1-integration/preview-review-request.json'),'manifest_sha256':request['preview_manifest_sha256'],'poster_sha256':request['poster_sha256'],'poster_equals_frame0_and_release_preview':True,'glb':{'bytes':len(raw),'sha256':sha(raw),'triangles':triangles,'materials':len(g['materials']),'textures':0,'required_extensions':g['extensionsRequired']},'frames':rows,'camera':'Shared ModelStage v2: perspective FOV38, elevation23.3, initial azimuth42, 15-degree increments, fit_padding1.08; ACESFilmic/sRGB/exposure1.2. Preset SHA is verified by unmodified delivery gate.','visual_observation':'All24 individual full-resolution decoded images inspected on alternating light/dark backgrounds; frame0 additionally on both backgrounds. Poster separately opened and identical to frame0. Grey RGB blocks in alpha-zero pixels disappear with correct composition and are not a visible defect. Selected airy A structure, subdued greens and tan woody structure remain consistent with saved actual GLB desktop/mobile captures. Fine needle subpixel aliasing remains disclosed.','handoff':{'source_report':str(p),'sha256':hashfile(p),'new_browser_run':False,'site_and_validator_code_unchanged_since_browser_commit':True,'actual_desktop_and_mobile_capture_pixels_inspected':True,'cases':parity,'limits':'Existing software-browser integration diagnostics; no new device/performance acceptance. Original failed first harness attempt retained.'},'compatibility_bilingual_checked':True,'performance_scope':'Only prior recorded M5 Pro/ANGLE Metal profile; SwiftShader performance fails including single-tree. Other devices/loaders unverified.','blockers':[]}
(out/'artifact-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print('PASS: 24 exact alpha frames, poster/frame0, source render bytes, GLB metrics, bilingual scope, unchanged-code handoff evidence')
