#!/usr/bin/env python3
import hashlib,json,datetime
from pathlib import Path
ROOT=Path('/workspace/shared/lowpoly-batch74-20261020')
QA=Path('/workspace/shared/lowpoly-round30-qa74')
W=ROOT/'production/continuous-small-life-round30-20261020/work/batch-74'
CONS=Path('/workspace/shared/batch74-consult-only')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files={}
def add(p,role,group):
 p=Path(p)
 if p.is_file(): files[str(p)]={'path':str(p),'sha256':h(p),'bytes':p.stat().st_size,'role':role,'group':group}
for p in (ROOT/'production/continuous-small-life-round30-20261020').rglob('*'):
 if p.is_file(): add(p,'producer package file','complete 539-file frozen batch package')
# Actual consulted pixels/text snapshots are external to Git; source/pixel rights remain with their owners.
for name,role in [('tribrachidium.jpg','fossil reference pixels'),('arete.jpg','NPS Garden Wall reference pixels'),('splay-fig3.png','Copernicus Fig. 3 reference pixels'),('coal-fig18.png','DOE/GSA Fig. 18 reference pixels'),('coal-doe.pdf','consult-only primary PDF'),('splay.pdf','consult-only primary PDF'),('splay-text.txt','primary article text extract'),('splay-xml.txt','primary article XML extract'),('splay.html','primary article HTML snapshot')]:
 add(CONS/name,role,'consult-only source material outside Git')
# Include every generated QA raw output, execution script, independent report, and immutable-manifest input.
for p in QA.rglob('*'):
 if p.is_file() and p.name not in ('raw-file-manifest.json','independent-report.json'):
  add(p,'independent QA evidence','new QA run output or script')
# Explicitly capture source references read online; no unverified provider timestamp or approval claim.
source_urls=[
 {'asset_id':'tribrachidium','url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC4681345/','title':'Rahman et al. 2015 primary morphology and fossil figures'},
 {'asset_id':'arete-ridge','url':'https://www.nps.gov/articles/nunataksareteshorns.htm','title':'National Park Service landform descriptions and Garden Wall photo'},
 {'asset_id':'crevasse-splay','url':'https://nhess.copernicus.org/articles/17/1505/2017/','title':'Izumida et al. 2017 primary paper and Fig. 3'},
 {'asset_id':'coal-seam-outcrop','url':'https://www.netl.doe.gov/sites/default/files/2018-02/fe0000888-final-report.pdf','title':'DOE/GSA final report, p. 37 and Fig. 18'}]
obj={'schema_version':1,'kind':'independent_batch74_qa_raw_file_manifest','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file_count':len(files),'files':list(sorted(files.values(),key=lambda x:x['path'])),'consulted_primary_web_sources':source_urls,'excluded_to_avoid_circular_hashing':['/workspace/shared/lowpoly-round30-qa74/raw-file-manifest.json','/workspace/shared/lowpoly-round30-qa74/independent-report.json'],'notes':['This manifest hashes all 539 files in the frozen batch production package, all consult-only primary documents/pixels named above, and every QA evidence/script file present at manifest-write time.','The report is excluded because it references this manifest hash; the manifest itself is excluded from its own hash closure.','Third-party consult-only pixels and primary PDFs are referenced but not copied into the candidate Git worktree.']}
p=QA/'raw-file-manifest.json';p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'path':str(p),'sha256':h(p),'bytes':p.stat().st_size,'file_count':len(files),'production_files':sum(1 for x in files.values() if x['group']=='complete 539-file frozen batch package'),'qa_files':sum(1 for x in files.values() if x['group']=='new QA run output or script'),'consult_files':sum(1 for x in files.values() if x['group']=='consult-only source material outside Git')},indent=2))
