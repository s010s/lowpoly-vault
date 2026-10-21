import sys;sys.dont_write_bytecode=True
import pathlib,json,hashlib,subprocess,os
from PIL import Image
import numpy as np
W=pathlib.Path('/workspace/shared/lowpoly-batch100-20261021');B=W/'production/small-life-batch100';Q=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'scripts'))
from qa_glb import audit_glb
from check_reproducibility import compare_rebuild
from validate_candidate import validate_candidate
H=json.loads((B/'handoff.json').read_text());M=json.loads((B/'delivery-manifest.json').read_text());sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
files=[]
for d in M['files']:
 p=W/d['path'];files.append({'path':d['path'],'pass':p.stat().st_size==d['bytes'] and sha(p)==d['sha256']})
R={'manifest_pass':all(x['pass']for x in files),'file_count':len(files),'files':files,'assets':{}}
for i in H['items']:
 a=i['asset_id'];d=Q/a;d.mkdir(exist_ok=True);r=i['revision'];p=B/a/r;g=W/i['glb']['path'];b=json.loads((W/i['original_brief']['path']).read_text())
 audit=audit_glb(g,**{k:v for k,v in b['geometry_policy'].items() if k!='max_glb_bytes'});(d/'static-glb.json').write_text(json.dumps(audit,indent=2))
 cv=validate_candidate(p/'candidate.json',W,validation_profile='static-stylized-v1',profile_contract=p/'profile-contract.json');(d/'candidate-integrity.json').write_text(json.dumps(cv,indent=2))
 checks=[]
 for key,v in i.items():
  if isinstance(v,dict) and 'path'in v and 'sha256'in v:checks.append({'key':key,'path':v['path'],'pass':sha(W/v['path'])==v['sha256']})
 rb=[]
 for letter in ['a','b']:
  old=json.loads((p/f'qa/reproducibility-{letter}.report.json').read_text());req=p/f'qa/rebuild-{letter}-request.json';res=p/f'qa/rebuild-{letter}-result.json';exe=json.loads((p/f'qa/rebuild-{letter}-execution.json').read_text());raw=pathlib.Path(exe['argv'][exe['argv'].index('--output')+1]);result=json.loads(res.read_text());rc=compare_rebuild(g,old['rebuilt_glb_path'],W/i['generator']['path'],W/i['config']['path'],req,res,f'{a}/{a}.glb',W)
  rawchecks=[{'path':str(raw/k),'pass':(raw/k).exists() and sha(raw/k)==v['sha256'] and (raw/k).stat().st_size==v['bytes']}for k,v in result['outputs'].items()]
  rc['raw_outputs_checked']=rawchecks;rc['raw_execution_equals_delivery_copy']=json.loads((raw/'execution.json').read_text())==exe;rc['actual_blender_pid']=exe['pid'];rc['generator_config_match']=exe['generator_sha256']==i['generator']['sha256'] and exe['config_sha256']==i['config']['sha256'];rc['raw_output_path']=str(raw)
  (d/f'rebuild-{letter}-independent.json').write_text(json.dumps(rc,indent=2));rb.append(rc)
 frames=[];rm=json.loads((p/'views/render-manifest.json').read_text());sheet=Image.open(p/'views/contact-sheet.png').convert('RGBA');order=['hero','reversehero','front','side','rear','top','clay','silhouette']
 for j,v in enumerate(order):
  f=p/'views'/f'{v}.png';im=Image.open(f).convert('RGBA');arr=np.array(im);mask=np.min(arr[:,:,:3],axis=2)<170;y,x=np.where(mask);tile=sheet.crop((j%4*512,j//4*544,j%4*512+512,j//4*544+512));fr=next(z for z in rm['frames'] if z['id']==v)
  frames.append({'view':v,'path':str(f),'sha256':sha(f),'hash_bound':sha(f)==fr['sha256'],'dimensions':im.size,'lossless_sheet_tile_equal':np.array_equal(arr,np.array(tile)),'dark_geometry_pixel_bbox':[int(x.min()),int(y.min()),int(x.max()),int(y.max())],'edge_touch':bool(mask[0].any() or mask[-1].any() or mask[:,0].any() or mask[:,-1].any())})
 (d/'frame-binding-and-pixel-check.json').write_text(json.dumps({'frames':frames,'sheet_size':sheet.size,'method':'Exact RGBA comparison to lossless sheet tile at 512px image plus 32px label stride. Dark-pixel threshold only diagnoses framing, not feature exposure.'},indent=2))
 R['assets'][a]={'subject_checks':checks,'static_status':audit['status'],'candidate_valid':cv['valid'],'candidate_errors':cv['errors'],'two_distinct_actual_blender_pids':[x['actual_blender_pid']for x in rb],'rebuilds_pass':all(x['status']=='pass' and all(z['pass']for z in x['raw_outputs_checked']) and x['raw_execution_equals_delivery_copy'] and x['generator_config_match'] for x in rb),'frames_bound':all(x['hash_bound']for x in frames),'sheet_exact':all(x['lossless_sheet_tile_equal']for x in frames)}
(Q/'02-integrity-rebuild-frame-checkpoint.json').write_text(json.dumps(R,indent=2));print(json.dumps({k:v for k,v in R.items()if k!='files'},indent=2))
