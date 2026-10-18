# SPDX-License-Identifier: MIT
"""Execute and freeze maker checks only; independent acceptance stays pending."""
import sys,subprocess,json,hashlib,shutil,time
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'scripts/asset_common.py').is_file());P=ROOT/'production/continuous-small-life-20261018';BASE=ROOT/'assets/candidates/continuous-small-life-20261018/batch-02/r001'
sys.path.insert(0,str(HERE/'lib'));from qa_glb import audit_glb
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for s in sys.argv[1:]:
 p=BASE/s;logs=p/'logs';logs.mkdir(parents=True,exist_ok=True);frozen=HERE/'frozen'/s
 if not frozen.exists():
  frozen.mkdir(parents=True);shutil.copy2(HERE/'build_batch02.py',frozen/'build.py');shutil.copytree(HERE/'lib',frozen/'lib',ignore=shutil.ignore_patterns('__pycache__'))
 commands=[]
 def run(args,label):
  start=time.monotonic();r=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=300);(logs/(label+'.log')).write_bytes(r.stdout);commands.append({'command':args,'returncode':r.returncode,'wall_seconds':round(time.monotonic()-start,3),'log':'logs/'+label+'.log'});print(s,label,r.returncode,flush=True)
  if r.returncode:raise RuntimeError(label+' failed; see '+str(logs))
 gen=str(frozen/'build.py');blender=['blender','-b','-t','2','--python-exit-code','1','--python']
 run(blender+[gen,'--','--asset',s,'--no-preview'],'freeze-build')
 rebuild=Path('/tmp/batch02-rebuild')
 run(blender+[gen,'--','--asset',s,'--no-preview','--output',str(rebuild)],'rebuild')
 a=audit_glb(p/(s+'.glb'),14000,6,30);b=audit_glb(rebuild/s/(s+'.glb'),14000,6,30)
 re={'status':'pass' if a['semantic_sha256']==b['semantic_sha256'] and not a['errors'] and not b['errors'] else 'fail','original_sha256':a['sha256'],'rebuilt_sha256':b['sha256'],'original_semantic_sha256':a['semantic_sha256'],'rebuilt_semantic_sha256':b['semantic_sha256'],'separate_rebuild':True,'generator_sha256':sha(gen),'config_sha256':sha(P/'items'/s/'build-config.json'),'helper_sha256':sha(frozen/'lib/asset_common.py'),'checker_sha256':sha(frozen/'lib/qa_glb.py')}
 (p/'reproducibility.report.json').write_text(json.dumps(re,indent=2)+'\n');assert re['status']=='pass'
 run(blender+[str(HERE/'verify_blender.py'),'--',str(p)],'source-roundtrip')
 run(['node','scripts/validate_gltf.cjs',str(p)],'khronos')
 run(['node',str(HERE/'runtime.mjs'),s],'runtime')
 runtime=json.loads((p/'runtime/report.json').read_text());assert runtime['status']=='pass'
 for f in ['brief.json','build-config.json','references.json']:shutil.copy2(P/'items'/s/f,p/f)
 views=['hero','reversehero','front','side','rear','top','clay','silhouette'];out=Image.new('RGB',(1280,660),'#e8e4dc');d=ImageDraw.Draw(out)
 for i,n in enumerate(views):
  im=Image.open(p/f'preview-{n}.png').convert('RGBA');im.thumbnail((320,300));x=(i%4)*320+(320-im.width)//2;y=(i//4)*330;out.paste(im,(x,y),im);d.text(((i%4)*320+8,y+308),n,fill='#354044')
 out.save(p/'contact-sheet.jpg',quality=92)
 rtout=Image.new('RGB',(1280,660),'#e8e4dc');d=ImageDraw.Draw(rtout)
 for i,n in enumerate(['normal','near','reversehero','front','side','rear','top','scene']):
  im=Image.open(p/'runtime'/(n+'.png'));im.thumbnail((320,300));x=(i%4)*320+(320-im.width)//2;y=(i//4)*330;rtout.paste(im,(x,y));d.text(((i%4)*320+8,y+308),n,fill='#354044')
 rtout.save(p/'runtime/contact-sheet.jpg',quality=92)
 meta=json.loads((p/'metadata.json').read_text());q=json.loads((p/'qa.json').read_text());q['threejs_runtime']={'status':'pass','scope':runtime['scope'],'glb_sha256':a['sha256'],'report':'runtime/report.json'};q['previews']={'status':'rendered_maker_inspection_required','views':views,'source':'editable source','engine':'Cycles CPU','samples':16,'resolution':512,'transparent':True,'exact_glb_images':'runtime/'};q['visual_review']={'status':'independent_pending','maker_inspection':'separate maker-notes.json; does not establish independent QA'};q['numeric_tolerance_note']='Batch-local audit thresholds: triangle source area <1e-14 m²; GLB cross-product squared <1e-28 m⁴. Shared historical checker uses absolute area unsuitable for mm subjects. Exact zero and nonfinite faces remain errors. Khronos validation unchanged.';(p/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
 (p/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 files={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(p.rglob('*')) if f.is_file() and f.name not in ('candidate.json','checksums.sha256')}
 cand={'schema_version':1,'record_profile':'practical-fixed-eight-v1','asset_id':s,'revision':'r001','status':'candidate','acceptance':'pending_parent_dispatched_independent_QA','base_main':'643534830397824dfd46990485bd16ad66ecf9ce','branch':'candidate/small-life-batch-02-20261018','maker_model':'GPT-6.1 Sol medium','required_independent_reviewer':'GPT-6 Luna xhigh; parent dispatch','artifact':{'glb':s+'.glb','sha256':a['sha256'],'bytes':a['bytes'],'triangles':a['scene_triangles'],'position_vertices':a.get('unique_position_accessor_vertices'),'materials':a.get('materials'),'primitives':a.get('scene_primitives_estimated_base_draw_calls'),'bounds_m':a['bounds_m']},'source_metrics':q['source'],'generator':str(Path(gen).relative_to(ROOT)),'generator_sha256':sha(gen),'helper_sha256':sha(frozen/'lib/asset_common.py'),'checker_sha256':sha(frozen/'lib/qa_glb.py'),'brief_sha256':sha(p/'brief.json'),'config_sha256':sha(p/'build-config.json'),'references_sha256':sha(p/'references.json'),'maker_checks':{'technical':'pass','rebuild':'pass','source_reopen':'pass','runtime_parse':'pass','functional_software_render':'pass','nine_copy_scene':'pass'},'independent_review':{'visual':'pending','factual':'pending','specification':'pending'},'coverage':{'fixed_views':views,'turntable_frames':0,'exact_glb_views':'runtime/report.json'},'files':files,'remaining_blockers':['Independent review has not been dispatched by maker; parent owns acceptance and integration.']}
 (p/'candidate.json').write_text(json.dumps(cand,ensure_ascii=False,indent=2)+'\n');(p/'checksums.sha256').write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in files.items()));print(s,a['bytes'],a['scene_triangles'],a['sha256'],flush=True)
