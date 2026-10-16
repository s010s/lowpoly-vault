# SPDX-License-Identifier: MIT
"""Encode and measure the original 256px preview experiment. No runtime changes.

python scripts/experiments/measure_preview_turntable_v3.py

Decode timings are Pillow/libwebp CPU proxies, explicitly NOT browser timings.
"""
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path
import gzip
import hashlib
import json
import platform
import statistics
import struct
import sys
import time

import PIL
from PIL import Image, ImageDraw, ImageFont, features

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'experiments/preview-turntable-v3'
ASSETS = {'dinosaur-nest': 'traces', 'lepidodendron': 'plants', 'natural-arch': 'geology'}
BG = {'light': '#F2EFE7', 'dark': '#24292A'}
QUALITY = 82
ITERATIONS = 40

def stats(samples):
    s = sorted(samples)
    return {'median_ms': round(statistics.median(s),4),
            'p95_ms': round(s[int((len(s)-1)*.95)],4),
            'min_ms': round(min(s),4), 'max_ms': round(max(s),4), 'samples_ms': [round(x,4) for x in samples]}

def decode(paths):
    data = [p.read_bytes() for p in paths]
    samples = []
    for i in range(5+ITERATIONS):
        start = time.perf_counter_ns()
        for b in data:
            with Image.open(BytesIO(b)) as im:
                im.load()
                rgba = im.convert('RGBA')
                raw = rgba.tobytes()
                if len(raw) != rgba.width*rgba.height*4:
                    raise RuntimeError('Unexpected decode size')
        elapsed = (time.perf_counter_ns()-start)/1e6
        if i >= 5:
            samples.append(elapsed)
    return stats(samples)

def over(im, color):
    return Image.alpha_composite(Image.new('RGBA', im.size, color),im).convert('RGB')

def encode(im, path):
    im.save(path, 'WEBP', quality=QUALITY, method=6, exact=True, alpha_quality=100)

def info(path):
    with Image.open(path) as im:
        return {'path': str(path.relative_to(ROOT)), 'encoded_bytes': path.stat().st_size,
                'width': im.width, 'height': im.height,
                'decoded_rgba_bytes': im.width*im.height*4,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def pixel_delta(original, lossy, background):
    a = over(original,background); b = over(lossy,background)
    diffs = [abs(x-y) for x,y in zip(a.tobytes(),b.tobytes())]
    return {'mean_absolute_channel_error_0_255': round(sum(diffs)/len(diffs),3),
            'max_absolute_channel_error': max(diffs)}

def glb_info(path):
    b = path.read_bytes()
    length, typ = struct.unpack_from('<II', b, 12)
    if typ != 0x4e4f534a:
        raise RuntimeError('Missing GLB JSON')
    doc = json.loads(b[20:20+length])
    attrs = set(); indices = set()
    for mesh in doc.get('meshes',[]):
        for prim in mesh['primitives']:
            attrs.update(prim['attributes'].values())
            if 'indices' in prim: indices.add(prim['indices'])
    component = {5120:1,5121:1,5122:2,5123:2,5125:4,5126:4}
    elements = {'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
    packed = sum(doc['accessors'][i]['count']*component[doc['accessors'][i]['componentType']]*elements[doc['accessors'][i]['type']] for i in attrs|indices)
    result = {'path': str(path.relative_to(ROOT)), 'actual_file_bytes': len(b),
              'gzip_level9_bytes': len(gzip.compress(b,compresslevel=9,mtime=0)),
              'compressed_transfer_note': 'Optional transport estimate only; actual host response encoding was not tested.',
              'packed_attribute_and_index_bytes_lower_bound': packed,
              'textures': len(doc.get('textures',[])),
              'draw_primitives': sum(len(m['primitives']) for m in doc.get('meshes',[])),
              'gpu_and_js_heap': 'Not measured. Packed geometry is not total GPU/JS memory; renderer, materials, canvas buffers and loader overhead excluded.'}
    try:
        import brotli
        result['brotli_quality11_bytes'] = len(brotli.compress(b,quality=11))
    except ImportError:
        result['brotli_quality11_bytes'] = None
    return result

font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font = ImageFont.truetype(font_path,17)
small = ImageFont.truetype(font_path,13)

def contact(columns, rows, name, title):
    w, h = len(columns)*276+24, len(rows)*300+90
    result = Image.new('RGB',(w,h),'#ECEAE4')
    d = ImageDraw.Draw(result)
    d.text((16,12),title,font=font,fill='#24292A')
    for ci,label in enumerate(columns):
        d.text((24+ci*276,44),label,font=small,fill='#343A3B')
    for ri,(slug,ims) in enumerate(rows):
        y = 76+ri*300
        for ci,im in enumerate(ims):
            result.paste(im.convert('RGB').resize((256,256),Image.Resampling.LANCZOS),(24+ci*276,y))
        d.text((24,y+261),slug,font=small,fill='#343A3B')
    result.save(OUT/name)

if '--add-clean' in sys.argv:
    report = json.loads((OUT/'measurements.json').read_text())
    clean_rows = []
    for record in report['assets']:
        slug = record['asset']; out = OUT/slug
        frames = [Image.open(out/'png-clean'/f'{i:02d}.png').convert('RGBA') for i in range(16)]
        (out/'frames-clean').mkdir(exist_ok=True)
        sheet = Image.new('RGBA',(1024,1024),(0,0,0,0))
        for i,im in enumerate(frames):
            encode(im,out/'frames-clean'/f'{i:02d}.webp')
            sheet.paste(im,((i%4)*256,(i//4)*256))
        encode(sheet,out/'sheet-clean.webp')
        sheet.save(out/'sheet-clean.png',optimize=True)
        (out/'hero-clean.webp').write_bytes((out/'frames-clean/00.webp').read_bytes())
        paths = [out/'frames-clean'/f'{i:02d}.webp' for i in range(16)]
        record['variants']['clean'] = {
            'static':info(out/'hero-clean.webp'), 'sheet':info(out/'sheet-clean.webp'),
            'frames':{'count':16,'total_encoded_bytes':sum(p.stat().st_size for p in paths),
                      'smallest_frame_bytes':min(p.stat().st_size for p in paths),
                      'largest_frame_bytes':max(p.stat().st_size for p in paths),
                      'single_decoded_rgba_bytes':256*256*4,'all_decoded_rgba_bytes':16*256*256*4,
                      'files':[info(p) for p in paths]},
            'cpu_proxy_decode':{'static':decode([out/'hero-clean.webp']),
                                'sheet':decode([out/'sheet-clean.webp']),
                                'all_frames_sequential':decode(paths)}}
        record['clean_frame_alpha_bboxes'] = [im.getchannel('A').getbbox() for im in frames]
        clean_rows.append((slug,[over(frames[i],BG['light']) for i in (0,4,8,12)]))
        print(slug,'clean static',record['variants']['clean']['static']['encoded_bytes'],
              'clean sheet',record['variants']['clean']['sheet']['encoded_bytes'],flush=True)
    report['clean_cutout_added_utc'] = datetime.now(timezone.utc).isoformat()
    (OUT/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
    contact(['Frame 00 / -55 deg','Frame 04 / 35 deg','Frame 08 / 125 deg','Frame 12 / 215 deg'],
            clean_rows,'clean-cutout-turntable-contact.png','No-floor cutouts: the same camera/light rig, all original geometry unchanged')
    raise SystemExit(0)

results = []
alpha_rows = []; direction_rows = []
for slug,category in ASSETS.items():
    out = OUT/slug
    frames = [Image.open(out/'png-shadow'/f'{i:02d}.png').convert('RGBA') for i in range(16)]
    for name in ('frames-shadow','frames-light','frames-dark'):
        (out/name).mkdir(exist_ok=True)
    sheets = {name: Image.new('RGBA' if name == 'shadow' else 'RGB',(1024,1024), (0,0,0,0) if name == 'shadow' else BG[name]) for name in ('shadow','light','dark')}
    for i,im in enumerate(frames):
        for name in sheets:
            variant = im if name == 'shadow' else over(im,BG[name])
            encode(variant,out/f'frames-{name}'/f'{i:02d}.webp')
            sheets[name].paste(variant,((i%4)*256,(i//4)*256))
    for name,im in sheets.items():
        encode(im,out/f'sheet-{name}.webp')
        im.save(out/f'sheet-{name}.png',optimize=True)
    for name in sheets:
        (out/f'hero-{name}.webp').write_bytes((out/f'frames-{name}/00.webp').read_bytes())
    clean = Image.open(out/'hero-clean.png').convert('RGBA')
    encode(clean,out/'hero-clean.webp')
    for name,color in BG.items():
        over(frames[0],color).save(out/f'hero-composite-{name}.png',optimize=True)
        over(clean,color).save(out/f'hero-clean-{name}.png',optimize=True)

    old = Image.open(ROOT/f'assets/prehistoric/{category}/{slug}/preview-hero.png').convert('RGB')
    old.resize((256,256),Image.Resampling.LANCZOS).save(out/'original-hero-256.webp','WEBP',quality=QUALITY,method=6)
    variants = {}
    for name in sheets:
        frame_paths = [out/f'frames-{name}'/f'{i:02d}.webp' for i in range(16)]
        variants[name] = {'static': info(out/f'hero-{name}.webp'),
                          'sheet': info(out/f'sheet-{name}.webp'),
                          'frames': {'count': 16, 'total_encoded_bytes': sum(p.stat().st_size for p in frame_paths),
                                     'smallest_frame_bytes': min(p.stat().st_size for p in frame_paths),
                                     'largest_frame_bytes': max(p.stat().st_size for p in frame_paths),
                                     'single_decoded_rgba_bytes': 256*256*4,
                                     'all_decoded_rgba_bytes': 16*256*256*4,
                                     'files': [info(p) for p in frame_paths]},
                          'cpu_proxy_decode': {'static': decode([out/f'hero-{name}.webp']),
                                               'sheet': decode([out/f'sheet-{name}.webp']),
                                               'all_frames_sequential': decode(frame_paths)}}
    rendered = json.loads((out/'render-report.json').read_text())
    partial_alpha = [a for a in frames[0].getchannel('A').tobytes() if 0<a<255]
    clean_alpha = clean.getchannel('A')
    shadow_alpha = frames[0].getchannel('A')
    outside = [sa for sa,ca in zip(shadow_alpha.tobytes(),clean_alpha.tobytes()) if ca == 0]
    decoded = Image.open(out/'hero-shadow.webp').convert('RGBA')
    record = {'asset': slug, 'glb': glb_info(ROOT/f'assets/prehistoric/{category}/{slug}/{slug}.glb'),
              'variants': variants,
              'source_png_bytes_total': sum((out/'png-shadow'/f'{i:02d}.png').stat().st_size for i in range(16)),
              'original_hero_png_bytes': (ROOT/f'assets/prehistoric/{category}/{slug}/preview-hero.png').stat().st_size,
              'original_hero_optimized_256': info(out/'original-hero-256.webp'),
              'alpha_check': {'partial_alpha_pixels': len(partial_alpha),
                              'nonzero_alpha_pixels_outside_clean_object': sum(a>0 for a in outside),
                              'outside_object_max_alpha_0_255': max(outside),
                              'webp_alpha_identical': decoded.getchannel('A').tobytes() == frames[0].getchannel('A').tobytes(),
                              'lossy_rgb_over_light': pixel_delta(frames[0],decoded,BG['light']),
                              'lossy_rgb_over_dark': pixel_delta(frames[0],decoded,BG['dark']),
                              'all_frame_alpha_bboxes': [im.getchannel('A').getbbox() for im in frames]},
              'camera': rendered['camera'], 'render_seconds': sum(t['seconds'] for t in rendered['render']['timings'])}
    results.append(record)
    alpha_rows.append((slug,[over(clean,BG['light']),over(frames[0],BG['light']),over(frames[0],BG['dark']),over(clean,BG['dark']),Image.open(out/'hero-physical-dark.png')]))
    direction_rows.append((slug,[old,over(frames[0],BG['light']),over(frames[4],BG['light']),over(frames[8],BG['light'])]))
    print(slug, 'static',variants['light']['static']['encoded_bytes'], 'sheet',variants['light']['sheet']['encoded_bytes'], 'frames',variants['light']['frames']['total_encoded_bytes'],'glb',record['glb']['actual_file_bytes'],flush=True)

report = {'experiment': 'preview-turntable-v3', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
          'scope': 'Three original representative assets only. No production runtime integration.',
          'conditions': {'platform': platform.platform(), 'python': platform.python_version(),
                         'pillow': PIL.__version__, 'libwebp': features.version('webp'),
                         'cpu': next((l.split(':',1)[1].strip() for l in Path('/proc/cpuinfo').read_text().splitlines() if l.startswith('model name')),'unknown'),
                         'encoding': {'format':'WebP', 'quality':QUALITY, 'method':6,'alpha_quality':100,'exact':True},
                         'decode': 'Pillow/libwebp CPU proxy: in-memory encoded bytes, open + load + RGBA conversion + tobytes; 5 warmups, 40 measured repetitions, no I/O in timing; sequential frames.',
                         'decoded_memory': 'Mathematical RGBA8 pixel budget, not observed resident or GPU memory. Native decoder/driver/DOM caches may retain more or fewer buffers.',
                         'browser_measurement': 'Not obtained: packaged Playwright browser missing; installed Chromium failed with socket EPERM. Elevated supported retry failed at sandbox setup (read-only sessions path). No bypass attempted.',
                         'browser_gpu_upload_fps_and_mobile_decode': 'NOT MEASURED'},
          'assets': results}
(OUT/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
contact(['Clean cutout / light','Shadow RGBA / light','Same RGBA / dark','Clean cutout / dark','Actual dark floor'],alpha_rows,'alpha-shadow-comparison.png','Alpha and shadow: baked catcher vs theme and physical-floor checks')
contact(['Existing source hero','Unified frame 00','Unified frame 04','Unified frame 08'],direction_rows,'art-direction-comparison.png','Original geometry, shared framing/lighting rules, per-asset projected fit')
print('MEASUREMENTS_COMPLETE',OUT/'measurements.json',flush=True)
