#!/usr/bin/env python3
"""Validate the delivered research inventory. Standard-library only; no network."""
from pathlib import Path
import csv,json,re,collections,hashlib
D=Path(__file__).resolve().parent
read=lambda name:json.loads((D/name).read_text(encoding='utf-8'))
j=read('inventory.json');a=j['assets'];sources=read('sources.json');reg=read('registry.json')
assert j['schema_version']==2 and j['inventory_status']=='research-planning'
assert len(a)==1000
ids=[x['id'] for x in a];assert len(set(ids))==1000
expected={'horsetail-cluster':('Jointed horsetail cluster','木贼群落'),'cycad':('Cycad rosette','苏铁形植株'),'lepidodendron':('Carboniferous lycopsid concept','石炭纪鳞木'),'fern-cluster':('Ground fern cluster','地被蕨丛'),'conifer-tree':('Mesozoic conifer concept','针叶乔木'),'natural-arch':('Natural Arch','天然石拱'),'stratified-cliff':('Stratified Cliff','层理岩崖'),'three-toed-track':('Three-toed Track Slab','三趾足迹泥板'),'dinosaur-nest':('Dinosaur Nest','恐龙卵窝'),'uprooted-log':('Uprooted seed-tree log','连根倒木')}
existing={x['id']:x for x in a if x['status']=='existing-candidate'}
assert set(existing)==set(expected)
for k,names in expected.items():assert (existing[k]['name']['en'],existing[k]['name']['zh'])==names
assert sum(x['status']=='planned' for x in a)==990
src={s['id']:s for s in sources};assert len(src)==len(sources)
for s in sources:
 assert re.match(r'https?://',s['url']),s['id']
 assert s['verification'] in {'opened','search-result'},s['id']
 assert s.get('supports') and s.get('limitations')
allowed={k:{x['id'] for x in reg[k]} for k in ['worlds','categories','eras','biomes','tags','packs']}
subs={(x['category'],x['id']) for x in reg['subcategories']}
for x in a:
 assert x['schema_version']==2 and re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',x['id'])
 for k in ['name','description','distinctness','modeling_brief','scientific_scope']:
  assert all(isinstance(x[k].get(l),str) and x[k][l].strip() for l in ['en','zh']),(x['id'],k)
 assert x['category'] in allowed['categories'] and (x['category'],x['subcategory']) in subs
 for k in ['worlds','eras','biomes','tags','packs']:assert set(x[k])<=allowed[k],(x['id'],k)
 assert x['source_ids'] and set(x['source_ids'])<=set(src),x['id']
 assert [s['id'] for s in x['sources']]==x['source_ids']
 assert all(s['url']==src[s['id']]['url'] for s in x['sources'])
 assert x['reconstruction_type'] in {'whole-organism','specimen','artistic-concept'}
 if x['status']=='planned':assert x['specifications'] is None
 if x['evidence_level']=='candidate':assert x['priority']=='hold' and x['production_gate']!='reference-ready'
 if x['evidence_level']=='group-supported':assert x['production_gate']!='reference-ready'
for p in reg['packs']:
 assert p['asset_ids']==[x['id'] for x in a if p['id'] in x['packs']]
with (D/'inventory.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==1000 and [x['id'] for x in rows]==ids
for x,y in zip(a,rows):
 for k in ['name','description','distinctness','modeling_brief','scientific_scope']:
  for l in ['en','zh']:assert y[k+'_'+l]==x[k][l],(x['id'],k,l)
 for k in ['worlds','packs','tags','eras','biomes','aliases','source_ids','specifications']:assert json.loads(y[k+'_json'])==x[k],(x['id'],k)
 for k in ['category','subcategory','status','representation','reconstruction_type','evidence_level','confidence','priority','production_wave','production_gate','complexity','scale_class','research_domain']:assert y[k]==x[k],(x['id'],k)
 assert json.loads(y['source_urls_json'])==[s['url'] for s in x['sources']]
with (D/'sources.csv').open(encoding='utf-8-sig',newline='') as f:sr=list(csv.DictReader(f))
assert len(sr)==len(sources) and [s['id'] for s in sr]==[s['id'] for s in sources]
for x,y in zip(sources,sr):
 for k in y:assert y[k]==str(x.get(k) or ''),(x['id'],k)
for k in ['status','research_domain','category','evidence_level','confidence','priority','production_gate','production_wave','reconstruction_type','representation']:
 assert dict(collections.Counter(x[k] for x in a))==j['counts'][k],k
assert len(sources)==j['counts']['source_entries']
assert len({s['url'] for s in sources})==j['counts']['unique_source_urls']
assert read('counts.json')==j['counts']
assert set(src)=={s for x in a for s in x['source_ids']}
# Checksum verification is optional while the bundle is being assembled.
if (D/'checksums.sha256').exists():
 for line in (D/'checksums.sha256').read_text().splitlines():
  digest,name=line.split('  ',1)
  assert hashlib.sha256((D/name).read_bytes()).hexdigest()==digest,name
print(json.dumps({'validated':True,'total':1000,'existing':10,'new':990,'sources':len(sources),'csv_round_trip':True,'registry_resolved':True,'scientific_certification':False},ensure_ascii=False,indent=2))
