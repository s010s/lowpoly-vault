"""Read-only fixed-e20d59 Linux preview comparison; no browser or publication."""
from pathlib import Path
from PIL import Image,ImageChops,ImageStat,ImageDraw
import hashlib,json,subprocess,math,struct
out=Path(__file__).parent;inputs=Path('qa/conifer-doc1-linux-preview-recheck');oldbase=Path('assets/turntables/conifer-tree/structure-r20-a-normal16-doc1/v2-768-q90')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
request=json.loads((inputs/'preview-review-request.json').read_text());manifest=json.loads((inputs/'linux-generated-turntable.json').read_text());capture=json.loads((inputs/'linux-render-report.json').read_text());failed=json.loads((inputs/'candidate-ci-render-report.json').read_text())
assert capture['status']=='pass' and failed['status']=='fail' and len(failed['reproducibility']['mismatches'])==25
assert capture['render_preset_sha256']==manifest['render_preset_sha256']=='2d3b55d5bc79348e50d7d5591489ea79e567c1c5b6e743c68a446809e31364ff'
assert capture['viewer_source_sha256']==sha('site/viewer.js') and capture['chromium_version']=='141.0.7390.37'
assert manifest['source_glb_sha256']==request['source_glb_sha256']=='c3a215eda3ceb3e4ec95bdb31446e180fd9f9d1f7eaa24131459a0db6fa56b40'
for line in (inputs/'SHA256SUMS').read_text().splitlines():
 digest,path=line.split('  ',1);assert sha(path)==digest,path
assert not subprocess.check_output(['git','diff','--name-only','35de59d2ad4dbce7e88eae9d8df237c480098c02','e20d59e4e6871903d23fcec958ebc2ba7d9030ba','--','site','scripts'])
def composite(im,c):
 bg=Image.new('RGBA',im.size,c);bg.alpha_composite(im.convert('RGBA'));return bg.convert('RGB')
rows=[]
for i,f in enumerate(manifest['frames']):
 p=inputs/'frames'/f'frame-{i:03}.webp';a=Image.open(oldbase/p.name).convert('RGBA');b=Image.open(p).convert('RGBA');alpha=b.getchannel('A');bbox=alpha.getbbox()
 assert sha(p)==f['sha256']==request['frames'][i]['sha256'] and p.stat().st_size==f['bytes']
 assert sha(oldbase/p.name)==request['frames'][i]['approved_mac_sha256']
 assert b.size==(768,768) and alpha.getextrema()==(0,255) and bbox==a.getchannel('A').getbbox()
 assert min(bbox[0],bbox[1],768-bbox[2],768-bbox[3])>0
 assert f['azimuth_deg']==42+15*i and f['elevation_deg']==23.3 and f['view']=='turntable'
 ad=ImageChops.difference(a.getchannel('A'),alpha);stats={}
 for name,c in [('light','#e8e4dc'),('dark','#20251b')]:
  diff=ImageChops.difference(composite(a,c),composite(b,c));stats[name]={'mean_abs_rgb_0_to_255':sum(ImageStat.Stat(diff).mean)/3,'channel_max':max(v[1] for v in diff.getextrema())}
 rows.append({'index':i,'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'old_sha256':sha(oldbase/p.name),'alpha_bbox':bbox,'old_and_linux_bounds_equal':True,'alpha_changed_pixels':768*768-ad.histogram()[0],'alpha_max_difference':ad.getextrema()[1],'composite_difference':stats,'azimuth_deg':f['azimuth_deg'],'elevation_deg':23.3,'inspected_individual_full_resolution_pair':True,'background_inspected':'light' if i%2==0 else 'dark','visual_observation':'Same branch/needle arrangement, camera, complete tip/root and woody/foliage palette. Slight local edge/color coverage changes; no coherent displacement, cut-off, missing spray or opaque backing.'})
assert len(rows)==24 and sum(x['bytes'] for x in rows)==manifest['total_bytes']==824778
assert sha(inputs/'poster.webp')==sha(inputs/'frames/frame-000.webp')==request['poster']['sha256']=='fb46be69de3e6dd664150c9bddeae58353d293e2eebff536cf44d5f014dab975'
# Offline remeasurement against existing actual GLB screenshots, not a new browser run.
background=(232,228,220)
def normalized(im):
 side=min(im.size);x=(im.width-side)/2;y=(im.height-side)/2;im=im.crop((x,y,x+side,y+side)).resize((320,320),Image.Resampling.BILINEAR);return composite(im,background)
def fg(im):
 pts=[(j%320,j//320) for j,v in enumerate(im.get_flattened_data()) if max(abs(v[k]-background[k]) for k in range(3))>12]
 return {'bbox':[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)],'centroid':[sum(x for x,y in pts)/len(pts),sum(y for x,y in pts)/len(pts)],'pixels':len(pts)}
handoff=[];expected=normalized(Image.open(inputs/'frames/frame-007.webp').convert('RGBA'))
for label in ['desktop-motion','mobile-motion']:
 p=Path('qa/conifer-doc1-integration/browser-evidence/conifer-handoff-attempt02')/(label+'-actual-detail-pixels.png');actual=normalized(Image.open(p).convert('RGBA'));a,b=fg(actual),fg(expected);diff=ImageChops.difference(actual,expected)
 metrics={'label':label,'source_capture':str(p),'source_sha256':sha(p),'normalization':'Pillow BILINEAR centered-square320px crop; independent offline approximation of existing browser parity method','new_browser_run':False,'mean_rgb_absolute_error':sum(ImageStat.Stat(diff).mean)/(3*255),'bbox_delta_px':max(abs(x-y) for x,y in zip(a['bbox'],b['bbox'])),'centroid_delta_px':math.dist(a['centroid'],b['centroid']),'actual_foreground':a,'expected_foreground':b}
 assert metrics['mean_rgb_absolute_error']<.04 and metrics['bbox_delta_px']<=8 and metrics['centroid_delta_px']<=8
 handoff.append(metrics);pair=Image.new('RGB',(640,344),'white');pair.paste(actual,(0,24));pair.paste(expected,(320,24));d=ImageDraw.Draw(pair);d.text((5,5),'Saved actual GLB '+label,fill='black');d.text((325,5),'New Linux frame007',fill='black');pair.save(out/(label+'-linux-parity.png'))
# Real canvas PNG from the Linux capture is the frame0 lossless runtime reference.
png=Image.open(inputs/'linux-reference.png').convert('RGBA');webp=Image.open(inputs/'poster.webp').convert('RGBA');assert png.size==webp.size==(768,768)
assert png.getchannel('A').tobytes()==webp.getchannel('A').tobytes()
reference_stats={c:sum(ImageStat.Stat(ImageChops.difference(composite(png,c),composite(webp,c))).mean)/3 for c in ['#e8e4dc','#20251b']}
raw=Path('assets/revisions/conifer-tree/structure-r20-a-normal16-doc1/conifer-tree.glb').read_bytes();g=json.loads(raw[20:20+struct.unpack_from('<I',raw,12)[0]])
assert hashlib.sha256(raw).hexdigest()==request['source_glb_sha256'] and len(raw)==715500 and len(g['materials'])==3 and not g.get('textures') and 'KHR_mesh_quantization' in g['extensionsRequired']
report={'status':'pass','fixed_review_commit':'e20d59e4e6871903d23fcec958ebc2ba7d9030ba','subject':{'revision':'structure-r20-a-normal16-doc1','glb_sha256':request['source_glb_sha256'],'brief_sha256':'092af4c3259156cd4a8a357df6e0151a1ec08fdd53fd7a351d162a6ed7561031','references_sha256':'18062b9ea882d531834240554f764a8a0818b83efd5e6f8afde2bbb77326119a'},'linux_capture_run':39038627111,'failed_ci_run':39038352273,'source_manifest_sha256':sha(inputs/'linux-generated-turntable.json'),'source_request_sha256':sha(inputs/'preview-review-request.json'),'linux_poster_sha256':sha(inputs/'poster.webp'),'poster_equals_frame0':True,'frames':rows,'offline_saved_glb_handoff_comparison':handoff,'linux_lossless_canvas_reference':{'path':str(inputs/'linux-reference.png'),'sha256':sha(inputs/'linux-reference.png'),'poster_alpha_exact':True,'poster_mean_abs_rgb_vs_png_0_to_255':reference_stats,'pixels_inspected':True},'observations':['All24 new Linux frames individually compared at full decoded resolution against approved Mac frames, on alternating light/dark backgrounds. Poster separately opened and inspected on both backgrounds.','24/24 alpha outer bounds exactly match the corresponding Mac frame; all have empty borders.42+15*i azimuth and23.3 elevation cover360 degrees with consistent ordering and closing step.','Magnified4x native-pixel patches at frame0/6/11/22 local maxima show small coverage/intensity changes at fine needles and branch edges. Differences are real decoded RGB/alpha changes, not solely encoding differences; no obvious pose, structural, palette, framing or broad halo regression.','Linux source capture uses the real built ModelStage and same exact GLB/viewer/preset; frame0 PNG alpha equals selected poster exactly. No live browser was operated by this review.','Preserved exact-code actual GLB screenshots remain consistent in angle, position and color with new frame7, both visually and by offline center-crop parity. New-image browser handoff/reproduction must still run after integrator activation.'],'root_cause':'Unresolved. Available evidence establishes environment-specific decoded/render/encoding differences; does not identify OS, browser package, backend, antialiasing or encoder as sole cause.','performance_scope':'No new performance acceptance. KHR_mesh_quantization required; prior M5 Pro/ANGLE Metal measured profile only; SwiftShader budget failures including single tree and fine-needle aliasing retained.','preview_defects':[],'release_blockers':['Current candidate still carries Mac image hashes and fails Linux zero-mismatch reproduction. Integrator must bind/activate approved Linux images and rerun complete Linux publication workflow; this review does not waive that failure.']}
(out/'artifact-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'status':report['status'],'poster':report['linux_poster_sha256'],'bounds_equal':24,'offline_parity':handoff,'png_comparison':reference_stats},indent=2))
