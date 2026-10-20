#!/usr/bin/env python3
"""Recompute Batch 55 pinned GLB budgets and eight-view manifest hashes."""
import argparse, hashlib, json, sys
from pathlib import Path
BASE='assets/candidates/continuous-small-life-round20-20261020/batch-55'
IDS=[('vermicularia','r001'),('weichselia','r001'),('ventifact','r001'),('pentichnus-deep-dwelling-trace','r002')]
VIEWS=['hero','reversehero','front','side','rear','top','clay','silhouette']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[5]);p.add_argument('--output',type=Path);a=p.parse_args();root=a.repo.resolve();sys.path.insert(0,str(root/'scripts'));from qa_glb import audit_glb,read_glb
 scope=json.loads((root/'production/continuous-small-life-round20-20261020/batch-55-QA-SCOPE.json').read_text());results=[]
 for asset,rev in IDS:
  bundle=root/BASE/asset/rev; glb=bundle/f'{asset}.glb'; expected=scope['expected_glb_sha256_by_asset'][asset]; actual=sha(glb)
  if actual!=expected: raise SystemExit(f'{asset}: pinned GLB SHA mismatch')
  audit=audit_glb(glb,max_triangles=14000,max_materials=6,max_primitives=30);doc,_,_=read_glb(glb)
  manifest=json.loads((bundle/'proof/render-manifest.json').read_text()); frames=[]
  for ident in VIEWS:
   matched=[x for x in manifest.get('frames',[]) if x.get('id')==ident]
   if len(matched)!=1: raise SystemExit(f'{asset}: missing/duplicate frame {ident}')
   f=matched[0]; img=bundle/'proof'/f['path']; digest=sha(img)
   if digest!=f['sha256'] or img.stat().st_size!=f.get('bytes',f.get('byte_length')) or (f['width'],f['height'])!=(512,512):raise SystemExit(f'{asset}: proof frame integrity failed: {ident}')
   frames.append({'id':ident,'path':str(img.relative_to(root)),'sha256':digest,'bytes':img.stat().st_size,'width':f['width'],'height':f['height']})
  item={'asset_id':asset,'revision':rev,'glb_sha256_expected':expected,'glb_sha256_actual':actual,'hash_match':True,'bytes':audit['bytes'],'audit':audit,'texture_count':len(doc.get('textures',[])),'image_count':len(doc.get('images',[])),'node_count':len(doc.get('nodes',[])),'camera_count':sum(n.get('camera') is not None for n in doc.get('nodes',[])),'extensions_used':doc.get('extensionsUsed',[]),'manifest_glb_sha256':manifest.get('source_glb_sha256'),'manifest_view_ids':[x['id'] for x in manifest['frames']],'required_views':VIEWS,'proof_frame_hashes':{x['id']:x['sha256'] for x in frames},'proof_frames':frames,'all_required_proof_frames_present':True}
  if item['bytes']>1000000 or audit['status']!='pass' or item['texture_count']!=0 or item['image_count']!=0 or item['camera_count']!=0: raise SystemExit(f'{asset}: static profile gate failed')
  results.append(item)
 out={'schema_version':1,'scope_source_commit':scope['expected_source_commit'],'candidate_commit':'b2341debdb31f73e0719d4aadbe832321db6008a','static_profile':'static-stylized-v1','limits':{'triangles':14000,'materials':6,'primitives':30,'glb_bytes':1000000,'textures':0},'assets':results}
 encoded=json.dumps(out,indent=2)+'\n'
 if a.output:a.output.write_text(encoded)
 print(encoded,end='')
if __name__=='__main__':main()
