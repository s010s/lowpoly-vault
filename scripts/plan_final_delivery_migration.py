"""Read-only fixed52/22-group PR42-style migration plan. Never deletes/rebinds.
Requires a successful instrumented actual collector read-set and exact verified
archive coverage. No direct read-set absence or claimed hash is deletion authority.
"""
import argparse,json,pathlib,hashlib
p=argparse.ArgumentParser();p.add_argument('--root',type=pathlib.Path,required=True);p.add_argument('--read-set',type=pathlib.Path,required=True);p.add_argument('--inventory',type=pathlib.Path,required=True);p.add_argument('--coverage',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest()
reads=json.loads(a.read_set.read_bytes());assert reads['complete'] and reads['model_count']==52
assert reads['source_sha256']==sha((a.root/'site/fifty-two-release.mjs').read_bytes())
direct={r['path'] for r in reads['reads'] if r['kind']!='bundle_membership'}
inventory={r['path']:r for r in json.loads(a.inventory.read_bytes())}
# Public-safe normalized rows only, prepared from independently readback-verified manifests.
coverage=json.loads(a.coverage.read_bytes());covered={(r['path'],r['sha256']):r for r in coverage['files']};assert coverage['readback_verified'] is True
allowed={'process_json_requires_pin_review','process_log_or_text','asset_non_delivery_image_pin_review','process_image_requires_pin_review'}
deletes=[];remaining=[];groups=[]
for i in range(1,23):
 path=f'assets/releases/next52-g{i:02d}-20261021.json';raw=(a.root/path).read_bytes();desc=json.loads(raw);rem=[]
 for pin in desc['files']:
  q=pin['path'];reason=None
  if q in direct:reason='REQUIRED_ACTUAL_COLLECTOR_READ'
  elif inventory.get(q,{}).get('category') not in allowed:reason='RETAIN_FINAL_OR_SOURCE_OR_UNCLASSIFIED'
  elif (q,pin['sha256']) not in covered:reason='ARCHIVE_EXACT_BYTES_NOT_VERIFIED'
  if reason:remaining.append({'path':q,'sha256':pin['sha256'],'reason':reason})
  else:
   # Also establish live bytes match the descriptor; no unchecked archival claim.
   b=(a.root/q).read_bytes();assert sha(b)==pin['sha256']
   row={'path':q,'sha256':pin['sha256'],'bytes':len(b),'archive_member_manifest_sha256':covered[(q,pin['sha256'])]['member_manifest_sha256']};deletes.append(row);rem.append(row)
 groups.append({'descriptor':path,'old_descriptor_sha256':sha(raw),'source_bundle':desc['source_bundle'],'remove_members':rem,'rebind_required_if_nonempty':['public restoration index','source_bundle.files','descriptor.files + source_bundle hash','accepted-fifty-two-release literal descriptor/release','accepted-bounded-batches descriptor/source bundle','registry batch descriptor pin'], 'apply':False})
result={'mode':'DRY_RUN_ONLY_NO_DELETION_OR_REBIND','scope':'fixed52 new22groups only; old295 canonical constant unchanged','read_set_sha256':sha(a.read_set.read_bytes()),'archive_coverage_sha256':sha(a.coverage.read_bytes()),'groups':groups,'proposed_deletions':deletes,'remaining':remaining,'safe_removable_unique_count':len({r['path'] for r in deletes}),'remaining_unique_count':len({r['path'] for r in remaining}),'post_migration_required':['Independent exact deletion/rebinding review','Full new-policy CI baseline','Ordinary commit; no history rewriting'],'contract_note':'Bundle membership hash reads must be removed only through reviewed PR42 rebinding; direct semantic reads remain required.'}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['mode','safe_removable_unique_count','remaining_unique_count']}))
