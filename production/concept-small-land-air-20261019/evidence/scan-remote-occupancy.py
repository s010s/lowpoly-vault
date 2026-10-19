import subprocess,json,datetime,re
ids=['sapeornis','longirostravis','dunbaria','sphecoptera','messelornis','homoioptera','stenodictya','palaeotarbus','trigonotarbus','chimerarachne','meganeura']
refs=subprocess.check_output(['git','for-each-ref','--format=%(refname)','refs/remotes'],text=True).splitlines()
report={'scanned_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main_sha':subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),'refs':{},'matches':{i:[] for i in ids},'scope':'All fetched remote heads and PR head refs. Path scan plus task/claim/handoff/freeze text excluding inventory/planning taxonomy lists.'}
seen={}
for ref in refs:
 sha=subprocess.check_output(['git','rev-parse',ref],text=True).strip();report['refs'][ref]=sha
 if sha not in seen:
  paths=subprocess.check_output(['git','ls-tree','-r','--name-only',ref],text=True).splitlines()
  hits={i:[] for i in ids}
  for p in paths:
   for i in ids:
    if i in p.lower():hits[i].append({'path':p,'kind':'path'})
  records=[p for p in paths if p.startswith(('production/','qa/')) and any(t in p.lower() for t in ['claim.json','handoff.json','task-reg','task_reg','reservation','task.md','freeze.json'])]
  for p in records:
   data=subprocess.check_output(['git','show',ref+':'+p],text=True,errors='replace')
   for i in ids:
    if re.search(r'(?<![a-z-])'+re.escape(i)+r'(?![a-z-])',data.lower()):hits[i].append({'path':p,'kind':'task_record'})
  seen[sha]=hits
 for i,hits in seen[sha].items():
  if hits:report['matches'][i].append({'ref':ref,'sha':sha,'evidence':hits})
json.dump(report,open('/tmp/small-land-air-dedup.json','w'),indent=2)
for i,m in report['matches'].items():print(i,len(m),'refs',sum(len(x['evidence']) for x in m),'hits', [(x['ref'],[e['path'] for e in x['evidence'][:1]]) for x in m[:2]])
print('refs',len(refs),'unique_shas',len(seen))
