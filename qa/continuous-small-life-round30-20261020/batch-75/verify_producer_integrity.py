import hashlib, json, os, subprocess, sys, pathlib, time
W=pathlib.Path('/workspace/shared/lowpoly-batch75-20261020')
P=W/'production/continuous-small-life-round30-20261020/work/batch-75'
O=pathlib.Path('/workspace/shared/lowpoly-round30-qa75')
COMMIT='64a896d4a62893f7d0f6c8276438fb95e424e518'
BASE='54bbcd99bb3ec96e89cd2b24b7ec5017b8b4ef3c'

def git(*args, raw=False):
    return subprocess.check_output(['git','-C',str(W),*args],stderr=subprocess.STDOUT)
def sha(p):
    h=hashlib.sha256(); n=0
    with open(p,'rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b: break
            n+=len(b); h.update(b)
    return h.hexdigest(),n

def git_tree(commit):
    raw=git('ls-tree','-r','-z',commit,raw=True)
    out={}
    for ent in raw.split(b'\0'):
        if not ent: continue
        meta,path=ent.split(b'\t',1)
        mode,typ,oid=meta.split()
        out[path.decode('utf-8')]=oid.decode()
    return out

head=git('rev-parse','HEAD').decode().strip()
branch=git('branch','--show-current').decode().strip()
status=git('status','--porcelain=v1').decode().strip()
assert head==COMMIT,(head,COMMIT)
assert branch=='candidate/small-life-batch75-concept-20261020',branch
assert not status,status
manifest=json.load(open(P/'source-evidence-manifest.json'))
tree=git_tree(COMMIT)
entries=[]; failures=[]
for m in manifest['files']:
    rel=m['path']; local=W/rel
    oid=tree.get(rel)
    if not local.is_file() or oid is None:
        failures.append({'path':rel,'reason':'missing_worktree_or_commit_tree'}); continue
    data=local.read_bytes()
    git_oid=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    actual_sha=hashlib.sha256(data).hexdigest()
    if len(data)!=m['bytes'] or actual_sha!=m['sha256'] or git_oid!=oid:
        failures.append({'path':rel,'reason':'size_sha256_or_blob_mismatch','size':len(data),'sha256':actual_sha,'expected_sha256':m['sha256'],'git_blob':oid,'worktree_git_blob':git_oid})
    entries.append({'path':rel,'bytes':len(data),'sha256':actual_sha,'git_blob':oid})
assert len(manifest['files'])==747,len(manifest['files'])
# Inventory blob is checked directly at frozen base commit.
inv_rel='research/prehistoric-1000-v1/inventory.json'
inv_oid=git('rev-parse',f'{BASE}:{inv_rel}').decode().strip()
inv=git('cat-file','blob',inv_oid,raw=True)
inv_sha=hashlib.sha256(inv).hexdigest()
assert inv_oid=='ddc7fb07df224197bf15711a7f4cf5826b86ae67'
assert inv_sha=='b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c'
# Ensure exact final identities and preproof binding on candidate tree.
hand=json.load(open(P/'handoff.json'))
expected={
 'parvancorina':('r001','6d121aa830daae492b81ff6a4fd99dd491f74105c0273ecb034a907de2b4fd35'),
 'glacial-horn':('r002','dc476400091e3a9375de913d3684cceb8a8400ea9a4af18228516899bb5ed92b'),
 'eruptive-fissure':('r003','5c01f576cfdb26179b4002bebc0c27997f41e805cf2fb9d9075b022291f83caf'),
 'banded-gneiss-outcrop':('r003','ead8a0740aae860dce43f982ebb9a0ba72800b976a322c37ea18cef17630e638'),
}
assets=[]
for a in hand['assets']:
    aid=a['asset_id']; rev,glb=expected[aid]
    assert a['revision']==rev and a['hashes']['glb']==glb,(aid,a['revision'],a['hashes']['glb'])
    d=W/a['path']; pbind=json.load(open(d/'preproof-binding.json'))
    assert pbind['glb_sha256']==glb and pbind['original_freeze_unchanged'] is True
    for key,name in [('glb','model.glb'),('brief','candidate-brief.json'),('references','references.json'),('source','source.blend'),('generator','generator.py'),('config','build-config.json')]:
        h,n=sha(d/name)
        assert h==a['hashes'][key],(aid,key,h,a['hashes'][key])
    freeze=json.load(open(d/'modeling-freeze.json'))
    frozen_brief=freeze['files']['brief.json']
    assert sha(d/'brief.json')[0]==frozen_brief,(aid,'immutable frozen brief',sha(d/'brief.json')[0],frozen_brief)
    assets.append({'asset_id':aid,'revision':rev,'hashes':dict(a['hashes']),'preproof_binding':pbind,'bytes':{name:os.path.getsize(d/name) for name in ['model.glb','source.blend']}})
# Final images and sheet dimensions/bytes; exact individual 512 px PNGs.
from PIL import Image
views=['hero','reversehero','front','side','rear','top','clay','silhouette']
images=[]; img_failures=[]
for id, (rev,_) in expected.items():
    d=W/'production/continuous-small-life-round30-20261020/work/batch-75/assets'/id/rev
    for view in views:
        p=d/'proof-final'/f'{view}.png'
        try:
            im=Image.open(p)
            rec={'asset_id':id,'view':view,'path':str(p),'width':im.width,'height':im.height,'mode':im.mode,'sha256':sha(p)[0],'bytes':os.path.getsize(p)}
            if im.size!=(512,512): img_failures.append(rec)
            images.append(rec)
        except Exception as e: img_failures.append({'asset_id':id,'view':view,'error':str(e)})
    p=d/'contact-sheet.png'; im=Image.open(p)
    images.append({'asset_id':id,'view':'lossless_contact_sheet','path':str(p),'width':im.width,'height':im.height,'mode':im.mode,'sha256':sha(p)[0],'bytes':os.path.getsize(p)})
assert len(images)==36, len(images)
assert len(img_failures)==0,img_failures
assert not failures,failures
# Save a pre-QA snapshot of all manifest-bound producer files and key handoff files.
keys=[str(P/'handoff.json'),str(P/'source-evidence-manifest.json'),str(P/'tracked-manifest-check.json')]
key_hashes=[]
for f in keys:
    h,n=sha(f); key_hashes.append({'path':f,'sha256':h,'bytes':n})
result={
 'checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
 'repo':{'worktree':str(W),'commit':head,'branch':branch,'clean_worktree':True,'tree_entries':len(tree)},
 'source_inventory':{'commit':BASE,'path':inv_rel,'git_blob':inv_oid,'bytes':len(inv),'sha256':inv_sha,'expected_closure_sha256':'b4a14c3ba2e99705eb097ee371cabd82aa76950beef014c4ecc1913742d80f4c','verified':True},
 'producer_manifest':{'path':str(P/'source-evidence-manifest.json'),'entries_expected':747,'entries_checked':len(entries),'all_present_worktree_and_git':not failures,'excluded':manifest.get('excluded_self_and_handoff_files'),'files':entries},
 'key_files':key_hashes,
 'assets':assets,
 'final_images':images,
 'all_pass':True
}
out_path=O/os.environ.get('QA_OUT','integrity-pre.json')
if out_path.name=='integrity-post.json':
    pre=json.load(open(O/'integrity-pre.json'))
    before={r['path']:(r['bytes'],r['sha256'],r['git_blob']) for r in pre['producer_manifest']['files']}
    after={r['path']:(r['bytes'],r['sha256'],r['git_blob']) for r in entries}
    assert before==after and pre['repo']['commit']==head and pre['key_files']==key_hashes
    result['unchanged_since_pre_snapshot']=True
json.dump(result,open(out_path,'w'),indent=2,sort_keys=True)
print(json.dumps({k:v for k,v in result.items() if k not in ['producer_manifest','assets','final_images']},indent=2))
print('assets:',[(a['asset_id'],a['revision'],a['hashes']['glb']) for a in assets])
print('final images:',len(images),'(32 views + 4 sheets)')
