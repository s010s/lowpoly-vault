# SPDX-License-Identifier: MIT
import subprocess,hashlib,json,pathlib,datetime
root=next(p for p in pathlib.Path(__file__).resolve().parents if (p/'scripts/asset_common.py').is_file()); base='352d81995b33fc1e7a95980184ab6641dd5738a5'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',base],cwd=root,text=True).splitlines()
assets=['phoenicopsis','cave-popcorn','curvolithus-trilobed-trail']
protected=[p for p in paths if any('/batch-52/'+a+'/' in p for a in assets) or any('/batch-52/'+a+'-' in p for a in assets) or '/batch-52/aturia/r001/' in p or '/batch-52/aturia/r002/' in p]
rows=[]
for p in protected:
 old=subprocess.check_output(['git','show',base+':'+p],cwd=root)
 new=(root/p).read_bytes()
 rows.append({'path':p,'sha256':hashlib.sha256(old).hexdigest(),'bytes':len(old),'unchanged':old==new})
r={'kind':'byte-identity-proof','base_commit':base,'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All tracked asset and work/evidence files for Phoenicopsis, Cave popcorn and Curvolithus; all Aturia r001/r002 files. Shared handoff changes only Aturia item.','checked_files':len(rows),'all_byte_identical':all(r['unchanged'] for r in rows),'files':rows}
(root/'production/continuous-small-life-round18-20261020/work/batch-52/aturia-r003-protected-files.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='files'}))
assert r['all_byte_identical']
