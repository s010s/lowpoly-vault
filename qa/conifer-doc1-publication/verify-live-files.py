"""Read-only exact-file checks for the explicitly authorized three-asset release."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, urllib.request, zipfile, io

COMMIT = '01c60dd85322932a967c4f2aa50045f2da1a25bd'
BASE = 'https://s010s.github.io/lowpoly-vault/'
ROOT = Path.cwd()
DIST = ROOT / 'dist'
OUT = ROOT / 'qa/release-conifer-doc1-live/live-files.json'
sha = lambda data: hashlib.sha256(data).hexdigest()
manifest = json.loads((DIST / 'assets/manifest.json').read_text())
approval = json.loads((ROOT / 'assets/initial-publication.json').read_text())
originals = {item['id']:item for item in approval['assets']}
assert set(manifest['publication']['approved_asset_ids']) == {'natural-arch','fern-cluster','conifer-tree'}
targets = {}
unchanged = []
for asset in manifest['assets']:
    if asset['id'] not in {'natural-arch','fern-cluster','conifer-tree'}:
        for key in ['glb','blend','preview']:
            assert asset[key] == originals[asset['id']][key]
            assert asset['sha256'][key] == originals[asset['id']]['sha256'][key]
        unchanged.append(asset['id'])
    for key in ['glb','blend','preview','card_preview']:
        path = asset[key]
        targets[path] = {'path':path,'expected_sha256':sha((DIST/path).read_bytes()),'asset_id':asset['id'],'kind':key}
    for key in ['bundle','credits']:
        path = asset['downloads'][key]
        targets[path] = {'path':path,'expected_sha256':sha((DIST/path).read_bytes()),'asset_id':asset['id'],'kind':key}
    if asset['id'] in {'natural-arch','fern-cluster','conifer-tree'}:
        path = asset['turntable']['manifest']
        targets[path] = {'path':path,'expected_sha256':sha((DIST/path).read_bytes()),'asset_id':asset['id'],'kind':'turntable_manifest'}
        data = json.loads((DIST/path).read_text())
        for frame in data['frames']:
            targets[frame['path']] = {'path':frame['path'],'expected_sha256':frame['sha256'],'asset_id':asset['id'],'kind':'turntable_frame'}
for item in DIST.rglob('*'):
    if item.is_file() and item.name != 'index.html':
        path = item.relative_to(DIST).as_posix()
        targets.setdefault(path, {'path':path,'expected_sha256':sha(item.read_bytes()),'kind':'deployed_file'})
route_count = 0
for page in DIST.rglob('index.html'):
    relative = page.relative_to(DIST)
    route = relative.parent.as_posix()
    route = '' if route == '.' else route + '/'
    targets['route:'+route] = {'path':route,'expected_sha256':sha(page.read_bytes()),'kind':'bilingual_html_route'}
    route_count += 1
assert route_count == 26
path = 'assets/manifest.json'
targets[path] = {'path':path,'expected_sha256':sha((DIST/path).read_bytes()),'kind':'manifest'}

def check(item):
    url = BASE + item['path'] + '?verify=' + COMMIT
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({'https':'http://127.0.0.1:10808'}))
    request = urllib.request.Request(url,headers={'Cache-Control':'no-cache','User-Agent':'LowpolyVault-ReleaseVerification'})
    try:
        with opener.open(request,timeout=40) as response:
            raw = response.read()
            result = {**item,'url':url,'http_status':response.status,'bytes':len(raw),'actual_sha256':sha(raw)}
            result['pass'] = response.status == 200 and result['actual_sha256'] == item['expected_sha256']
            if item['path'].endswith('.zip'):
                with zipfile.ZipFile(io.BytesIO(raw)) as archive:
                    result['zip_crc_valid'] = archive.testzip() is None
                    result['zip_entries'] = {n:sha(archive.read(n)) for n in archive.namelist()}
                    result['pass'] = result['pass'] and result['zip_crc_valid']
            return result
    except Exception as exc:
        return {**item,'url':url,'pass':False,'error':str(exc)}

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(check, targets.values()))
report = {'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deployed_commit':COMMIT,'base_url':BASE,
          'expected_manifest_sha256':sha((DIST/'assets/manifest.json').read_bytes()),'bilingual_route_count':route_count,
          'approved_asset_ids':manifest['publication']['approved_asset_ids'],'unchanged_original_asset_ids':sorted(unchanged),
          'checked_files_and_routes':len(results),'results':results,'status':'pass' if all(r['pass'] for r in results) else 'fail'}
OUT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in report if k!='results'},indent=2))
for failure in [r for r in results if not r['pass']]: print(json.dumps(failure))
raise SystemExit(0 if report['status']=='pass' else 1)
