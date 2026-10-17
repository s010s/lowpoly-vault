#!/usr/bin/env python3
"""Verify/reassemble immutable recovery bundles and optionally import to a Git repository."""
import argparse, hashlib, json, pathlib, subprocess, sys

def sha256(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--directory',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent)
 p.add_argument('--repo',type=pathlib.Path,help='Optional existing repository with the required baseline; imports only new recovered/* refs.')
 args=p.parse_args(); directory=args.directory.resolve()
 index=json.loads((directory/'index.json').read_text())
 reports=[]
 for item in index['restore_order']:
  manifest_path=directory/item['manifest']; m=json.loads(manifest_path.read_text())
  target=directory/m['bundle_file']
  if not target.exists():
   tmp=target.with_suffix(target.suffix+'.assembling')
   try:
    with tmp.open('xb') as out:
     for part in m['bundle_parts']:
      f=directory/part['file']
      if f.stat().st_size!=part['bytes'] or sha256(f)!=part['sha256']: raise ValueError('Part integrity failed: '+str(f))
      with f.open('rb') as source:
       for b in iter(lambda:source.read(1024*1024),b''):out.write(b)
    if tmp.stat().st_size!=m['bundle_bytes'] or sha256(tmp)!=m['bundle_sha256']:raise ValueError('Assembled bundle integrity failed: '+str(tmp))
    tmp.rename(target)
   except BaseException:
    if tmp.exists():tmp.unlink()
    raise
  if target.stat().st_size!=m['bundle_bytes'] or sha256(target)!=m['bundle_sha256']:raise ValueError('Bundle integrity failed: '+str(target))
  report={'asset':m['asset'],'bundle':target.name,'sha256':m['bundle_sha256'],'checksum':'pass'}
  if args.repo:
   def git(*a):return subprocess.check_output(['git','-C',str(args.repo.resolve()),*a],stderr=subprocess.STDOUT)
   git('cat-file','-e',m['required_baseline_commit']+'^{commit}')
   git('bundle','verify',str(target))
   ref='refs/heads/recovered/'+m['asset']+'-'+m['source_tip'][:12]
   git('fetch','--no-tags',str(target),m['source_ref']+':'+ref)
   if git('rev-parse',ref).decode().strip()!=m['source_tip']:raise ValueError('Recovered ref mismatch')
   for c in m['commits']:git('cat-file','-e',c['commit']+'^{commit}')
   for blob,meta in m['blob_checksums'].items():
    b=git('cat-file','blob',blob)
    if len(b)!=meta['bytes'] or hashlib.sha256(b).hexdigest()!=meta['sha256']:raise ValueError('Recovered blob mismatch: '+blob)
   report.update({'import':'pass','ref':ref,'commits_verified':len(m['commits']),'changed_blob_checksums_verified':len(m['blob_checksums'])})
  reports.append(report);print(json.dumps(report))
 return reports
if __name__=='__main__':main()
