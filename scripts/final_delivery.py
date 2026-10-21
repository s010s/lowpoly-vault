"""Fixed offline content consumer. No publication authority or archive credentials."""
import hashlib,json,pathlib,tempfile,importlib.util,subprocess,os
from final_delivery_fixed import REVIEWED_CONTENT,PUBLICATION_ACCEPTED_ENTRIES
from final_delivery_relations import validate_candidate
HERE=pathlib.Path(__file__).resolve().parent
SOURCE=str(HERE/'qa_glb.py')
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(v,msg):
 if not v:raise ValueError(msg)
def authenticate_content(name,raw):
 need(name in REVIEWED_CONTENT,'unlisted fixed content entry')
 entry=REVIEWED_CONTENT[name];need(sha(raw)==entry['summary_sha256'],'summary differs from independently reviewed fixed content')
 s=json.loads(raw);validate_candidate(s)
 need(s['provenance']==entry['provenance'],'source/review provenance differs')
 actual={a['id']:{'revision':a['revision'],'artifacts':a['artifacts'],'original_QA':a['independent_review']['original_report']} for a in s['assets']}
 need(actual==entry['assets'],'exact artifact/revision/QA set differs')
 need(s.get('original_quality_context',{}).get('top_level_pins',{})==entry['original_quality_context_pins'],'original review bindings differ')
 need(s['archive']==entry['archive'],'primary archive bindings differ')
 need([{k:a[k] for k in ['archive_sha256','member_manifest_sha256']} for a in s['supplementary_archives']]==entry['supplementary_archives'],'supplement manifests differ')
 need(s['offline_static_eligible_ids']==entry['offline_static_eligible_ids'],'eligible set differs')
 return s

def recompute_native(asset,glb_bytes):
 """Independent actual-byte comparison, also separately adversarially tested."""
 p=asset['artifacts']['glb'];need(isinstance(glb_bytes,bytes),'actual GLB bytes required')
 need(sha(glb_bytes)==p['sha256'] and len(glb_bytes)==p['bytes'],'actual final GLB differs')
 need(sha(pathlib.Path(SOURCE).read_bytes())==asset['native_measurement_comparison']['validator_sha256'],'native verifier changed')
 spec=importlib.util.spec_from_file_location('unchanged_native_glb',SOURCE);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 budget=asset['frozen_native_gate']['budget'];need(budget=={'max_triangles':14000,'max_materials':6,'max_primitives':30},'unreviewed frozen budget')
 with tempfile.NamedTemporaryFile(suffix='.glb') as f:
  f.write(glb_bytes);f.flush();result=mod.audit_glb(f.name,max_triangles=budget['max_triangles'],max_materials=budget['max_materials'],max_primitives=budget['max_primitives'])
 need(result['status']=='pass','actual final native static gate failed')
 producer=asset['native_measurement_comparison'];original=asset['independent_review']['measurements']
 for native,key,reported in [('scene_triangles','triangles','triangles'),('materials','materials','materials'),('bytes','glb_bytes','glb_bytes')]:
  need(result[native]==original[key]==producer[reported],'actual native '+key+' differs from original QA or summary')
 original_bounds=original.get('gltf_bounds_m',original.get('bounds_gltf_m'))
 for key in ['min','max']:need(result['bounds_m'][key]==original_bounds[key]==producer['bounds_m'][key],'actual native bounds differ')
 need(result['semantic_sha256']==producer['semantic_sha256'],'actual native semantic digest differs')
 if 'primitives' in original:need(result['scene_primitives_estimated_base_draw_calls']==original['primitives'],'actual primitives differ')
 return {'status':'ACTUAL_BYTES_STATIC_GLB_VERIFIED_NOT_FULL_QA','glb_sha256':sha(glb_bytes),'bytes':len(glb_bytes),'triangles':result['scene_triangles'],'materials':result['materials'],'bounds_m':result['bounds_m'],'semantic_sha256':result['semantic_sha256']}

def inspect_final_candidate(name,raw,asset_id,glb_bytes,blend_bytes):
 summary=authenticate_content(name,raw);need(asset_id in summary['offline_static_eligible_ids'],'not independently offline eligible')
 a=next(x for x in summary['assets'] if x['id']==asset_id);source=a['artifacts']['source']
 need(isinstance(blend_bytes,bytes) and sha(blend_bytes)==source['sha256'] and len(blend_bytes)==source['bytes'],'actual final Blend differs')
 native=recompute_native(a,glb_bytes)
 return {'id':asset_id,'scope':'OFFLINE_CONTENT_AND_STATIC_GLB_ONLY','native':native,'blend_sha256':sha(blend_bytes),'publication_ready':False,'pending':['Current final presentation assets and independent review','Other required native/source/geometry gates','Website/scene/GPU and remote CI/publication authorization']}

def authorize_publication(*args,**kwargs):
 need(bool(PUBLICATION_ACCEPTED_ENTRIES),'production publication accepted-set remains empty')
 raise ValueError('local prototype cannot publish')

def inspect_candidate_inputs(name,raw,asset_id,actual_inputs):
 """Complete seven-role retained-input path; callers supply bytes, never metrics."""
 summary=authenticate_content(name,raw);need(asset_id in summary['offline_static_eligible_ids'],'not offline eligible')
 asset=next(a for a in summary['assets'] if a['id']==asset_id)
 need(isinstance(actual_inputs,dict) and set(actual_inputs)==set(asset['artifacts']),'missing or extra retained artifact role')
 for role,pin in asset['artifacts'].items():
  b=actual_inputs[role];need(isinstance(b,bytes) and len(b)==pin['bytes'] and sha(b)==pin['sha256'],'actual '+role+' bytes differ from fixed review')
 result=inspect_final_candidate(name,raw,asset_id,actual_inputs['glb'],actual_inputs['source'])
 result['all_retained_artifact_roles_read_and_hashed']=sorted(actual_inputs)
 return result

def read_retained(root,path):
 """No symlink traversal, arbitrary absolute path or external archive reads."""
 root=pathlib.Path(root).resolve()
 need(isinstance(path,str) and path and not path.startswith('/') and all(p not in ('','.','..') for p in path.split('/')),'unsafe retained path')
 full=root/path
 need(full.resolve()==full and full.is_file(),'retained file missing or symlinked: '+path)
 return full.read_bytes()

def collect_final_delivery(root):
 from final_delivery_fixed import DELIVERY_PATHS,RESTORATION_INDICES,DELIVERY_SUPPORT_PINS,INDEPENDENT_CONSUMER_REVIEW_SHA256
 results=[];inputs=[]
 for pin in DELIVERY_SUPPORT_PINS:
  need(sha(read_retained(root,pin['path']))==pin['sha256'],'delivery metadata/license/support differs')
  inputs.append(pin)
 for name,entry in REVIEWED_CONTENT.items():
  path='qa/final-delivery-20261021/'+name+'-summary.candidate.json'
  raw=read_retained(root,path);summary=authenticate_content(name,raw)
  restoration=RESTORATION_INDICES[name];b=read_retained(root,restoration['path'])
  need(sha(b)==restoration['sha256'],'restoration index differs from reviewed bytes')
  inputs += [{'path':path,'sha256':sha(raw)},restoration]
  for aid in entry['offline_static_eligible_ids']:
   roles=DELIVERY_PATHS[aid];actual={role:read_retained(root,path) for role,path in roles.items()}
   result=inspect_candidate_inputs(name,raw,aid,actual)
   result['final_paths']=roles;results.append(result)
   inputs.extend({'path':roles[role],'sha256':sha(b)} for role,b in actual.items())
 return {'contract':'final-delivery-offline-v1','independent_contract_review_sha256':INDEPENDENT_CONSUMER_REVIEW_SHA256,'candidates':results,'inputs':inputs,'publication_ready_ids':[],
 'historical_png_policy':'Historical PNG/full-report bodies restored from archives for audit, not reread by every release CI; exact independently reviewed summary is protected content.',
 'pending':['Final canonical preview/card/gallery and independent exact-subject review','Remaining current native/source gates','Catalog integration, remote full CI and separate publication authorization']}

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=pathlib.Path,default=HERE.parent);args=parser.parse_args()
 print(json.dumps(collect_final_delivery(args.root),sort_keys=True))
