"""Adversarial production seven-role consumer tests; no archived PNG/report reads."""
import json,copy,pathlib,tempfile
from final_delivery import *
from final_delivery_fixed import DELIVERY_PATHS
ROOT=HERE.parent
samples={n:read_retained(ROOT,'qa/final-delivery-20261021/'+n+'-summary.candidate.json') for n in REVIEWED_CONTENT}
results=[]
def reject(name,fn):
 try:fn()
 except ValueError as e:results.append({'case':name,'result':'REJECTED','reason':str(e)})
 else:raise AssertionError('accepted '+name)
old=[('wrong GLB',lambda s:s['assets'][0]['artifacts']['glb'].__setitem__('sha256','0'*64)),('missing stage',lambda s:s['assets'][0]['independent_review']['subject_projection']['stages'].pop('gpu')),('UNKNOWN promoted',lambda s:s['assets'][0]['independent_review']['subject_projection']['stages'].__setitem__('gpu','PASS')),('wrong source',lambda s:s['provenance'].__setitem__('original_source_commit','0'*40)),('wrong archive manifest',lambda s:s['archive'].__setitem__('member_manifest_sha256','0'*64)),('wrong report hash',lambda s:s['assets'][0]['independent_review']['original_report'].__setitem__('sha256','0'*64)),('claimed approval',lambda s:s.__setitem__('publication_approved',True)),('missing view',lambda s:s['assets'][0]['historical_views']['frames'].pop())]
independent=[('delete quality fields except stages',lambda x:x['assets'][0]['independent_review'].__setitem__('subject_projection',{'stages':x['assets'][0]['independent_review']['subject_projection']['stages']})),('999999 budget',lambda x:x['assets'][0].__setitem__('frozen_native_gate',{'budget':{'max_triangles':999999}})),('null archive/provenance/report',lambda x:(x.__setitem__('archive',None),x.__setitem__('provenance',None),x['assets'][0]['independent_review'].__setitem__('original_report',None))),('duplicate ID',lambda x:x['assets'].append(copy.deepcopy(x['assets'][0]))),('asset accepted=true',lambda x:x['assets'][0].__setitem__('accepted',True)),('Cup eligible',lambda x:x['offline_static_eligible_ids'].append('cupressocrinites')),('null historical views',lambda x:x['assets'][0].__setitem__('historical_views',None)),('new GLB old report',lambda x:x['assets'][0]['artifacts']['glb'].__setitem__('sha256','0'*64)),('empty measurements',lambda x:x['assets'][0]['independent_review'].__setitem__('measurements',{})),('erase blockers',lambda x:x.__setitem__('release_blockers',[]))]

for name,raw in samples.items():
 base=authenticate_content(name,raw)
 for title,mutate in old+(independent if name=='batch109' else []):
  x=copy.deepcopy(base);mutate(x)
  reject(title,lambda:authenticate_content(name,json.dumps(x).encode()))
 for aid in base['offline_static_eligible_ids']:
  actual={k:read_retained(ROOT,p) for k,p in DELIVERY_PATHS[aid].items()}
  inspect_candidate_inputs(name,raw,aid,actual)
  for role in actual:
   bad=dict(actual);bad[role]=bytes([actual[role][0]^1])+actual[role][1:]
   reject(aid+' corrupted '+role,lambda:inspect_candidate_inputs(name,raw,aid,bad))
  reject(aid+' missing role',lambda:inspect_candidate_inputs(name,raw,aid,{k:v for k,v in actual.items() if k!='references'}))
  reject(aid+' extra producer metrics',lambda:inspect_candidate_inputs(name,raw,aid,{**actual,'producer_metrics':b'{}'}))
 reject(name+' publication',lambda:authorize_publication())
base=json.loads(samples['batch109']);asset=base['assets'][0];glb=read_retained(ROOT,DELIVERY_PATHS[asset['id']]['glb'])
x=copy.deepcopy(asset);x['native_measurement_comparison']['triangles']=1;x['independent_review']['measurements']['triangles']=1
reject('synchronized native QA triangle forgery, actual GLB unchanged',lambda:recompute_native(x,glb))
x=copy.deepcopy(asset);x['native_measurement_comparison']['semantic_sha256']='0'*64
reject('false semantic digest actual GLB',lambda:recompute_native(x,glb))
for title,mutate in [
 ('section UTF8',lambda s:s['assets'][0]['scientific_visual_finding'].__setitem__('verbatim_original_section','fake')),
 ('bounds disagreement',lambda s:s['assets'][0]['native_measurement_comparison']['bounds_m']['min'].__setitem__(0,-999)),
 ('nonfinite',lambda s:s['assets'][0]['native_measurement_comparison'].__setitem__('triangles',float('nan'))),
 ('negative dimensional size',lambda s:s['assets'][0]['anatomy_gate_projection']['transformed_components']['groups'][0]['actual_world_size_m_min'].__setitem__(0,-1)),
 ('reversed dimensional extrema',lambda s:s['assets'][0]['anatomy_gate_projection']['transformed_components']['groups'][0]['actual_world_size_m_min'].__setitem__(0,999))]:
 x=copy.deepcopy(base);mutate(x);reject(title,lambda:validate_candidate(x))
reject('unknown fixed entry',lambda:authenticate_content('self-approved',samples['batch109']))
reject('Cup REVISE',lambda:inspect_candidate_inputs('batch109',samples['batch109'],'cupressocrinites',{}))
reject('path escape',lambda:read_retained(ROOT,'../package.json'))
with tempfile.TemporaryDirectory() as td:
 p=pathlib.Path(td);(p/'link').symlink_to(ROOT/'package.json');reject('symlink',lambda:read_retained(p,'link'))
report=collect_final_delivery(ROOT)
assert len(report['candidates'])==5 and report['publication_ready_ids']==[]
print(json.dumps({'positive_real_seven_role_candidates':5,'negative_count':len(results),'negatives':results,'publication_ready_ids':[]}))
