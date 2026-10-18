from pathlib import Path
import json,hashlib,shutil,datetime
root=Path.cwd();out=root/'qa/conifer-doc1-linux-integration';accepted=root/'experiments/structural-refinement-2026-10-17/accepted/conifer-tree';record=accepted/'qa/doc1-linux-publication-preview-independent/candidate.reviewed.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(record)=='4ecdcbc679099789ab917f72e0cc6ffbb959a9b870e16698f325a2283c41ef27'
old=json.load(open('assets/manifest.json'));folder=Path('assets/revisions/conifer-tree/structure-r20-a-normal16-doc1');seq=Path('assets/turntables/conifer-tree/structure-r20-a-normal16-doc1/v2-768-q90');card=Path('assets/card-previews/conifer-tree-structure-r20-a-normal16-doc1-v2-768-q90.webp')
# Preserve the entire original unpublished Mac release image/metadata proposal as immutable QA evidence.
archive=out/'original-mac-proposal';archive.mkdir(parents=True,exist_ok=False)
for p in [folder/'release-metadata.json',folder/'preview.webp',seq/'turntable.json',card,Path('assets/manifest.json'),Path('assets/turntables/index.json')]+sorted(seq.glob('frame-*.webp')):
 dest=archive/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
review=accepted/'qa/doc1-linux-publication-preview-independent';r=json.load(open(record));evidence={x['id']:x for x in r['evidence']}
for i in range(24):
 e=evidence[f'linux-publication-frame-{i:03}'];src=accepted/e['path'];assert sha(src)==e['sha256'];shutil.copy2(src,seq/f'frame-{i:03}.webp')
poster=seq/'frame-000.webp';assert sha(poster)=='fb46be69de3e6dd664150c9bddeae58353d293e2eebff536cf44d5f014dab975'
shutil.copy2(poster,folder/'preview.webp');shutil.copy2(poster,card)
# Exact manifest from canonical Linux capture; frame paths already target the selected versioned routes.
shutil.copy2('qa/conifer-doc1-linux-preview-recheck/linux-generated-turntable.json',seq/'turntable.json');data=json.load(open(seq/'turntable.json'))
for f in data['frames']:assert sha(Path(f['path']))==f['sha256']
md=json.load(open(folder/'release-metadata.json'));md['sha256']['preview']=sha(poster);(folder/'release-metadata.json').write_text(json.dumps(md,ensure_ascii=False,indent=2)+'\n')
index=json.load(open('assets/turntables/index.json'))
for a in index['assets']:
 if a['id']=='conifer-tree':a['manifest_sha256']=sha(seq/'turntable.json')
for a in index['posters']:
 if a['id']=='conifer-tree':a['sha256']=sha(poster);a['bytes']=poster.stat().st_size
Path('assets/turntables/index.json').write_text(json.dumps(index,indent=2)+'\n')
desc=json.load(open('assets/releases/conifer-doc1-preview-reviewed-20261017.json'));desc['release_id']='conifer-doc1-linux-reviewed-20261017';desc['authorized_on']=datetime.datetime.now(datetime.timezone.utc).isoformat()
entry=next(x for x in desc['revisions'] if x['id']=='conifer-tree');entry['metadata']['sha256']=sha(folder/'release-metadata.json');entry['sha256']['preview']=sha(poster);entry['candidate']={'path':record.relative_to(accepted).as_posix(),'sha256':sha(record)}
p=Path('assets/releases')/(desc['release_id']+'.json');p.write_text(json.dumps(desc,ensure_ascii=False,indent=2)+'\n');pin={'path':str(p),'sha256':sha(p)};(out/'release-pin.json').write_text(json.dumps(pin,indent=2)+'\n')
(out/'activation-inputs.json').write_text(json.dumps({'independent_review_commit':'3b06230e66607f06f1980a035834ceb53755887e','candidate_sha256':sha(record),'poster_sha256':sha(poster),'canonical_capture_run':39038627111,'old_mac_proposal_preserved':str(archive.relative_to(root)),'model_and_blend_unchanged':True,'publication_gate_unchanged':True,'release_pin':pin},indent=2)+'\n')
print(json.dumps(pin))
