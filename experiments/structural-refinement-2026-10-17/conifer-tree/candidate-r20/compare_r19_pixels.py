#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only same-camera comparison; never modifies source or candidate PNGs."""
from pathlib import Path
from PIL import Image
import hashlib,json,math
P=Path(__file__).resolve().parent;OLD=P.parent/'candidate-r19';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for directory,baseline,views in [('detail512','pilot512',['hero035','hero125','hero215','hero305','detail','detailclay','clay']),('native128','pilot128',['hero035','hero125','hero215','hero305','front','rear','left','right','silhouette'])]:
 for view in views:
  source=OLD/'evidence'/baseline/(view+'.png');candidate=P/'evidence'/directory/(view+'.png');a=Image.open(source).convert('RGB');b=Image.open(candidate).convert('RGB');assert a.size==b.size
  aa=a.tobytes();bb=b.tobytes();diff=[abs(x-y) for x,y in zip(aa,bb)];count=sum(any(diff[i:i+3]) for i in range(0,len(diff),3))
  rows.append({'view':view,'source_path':str(source.relative_to(P.parent)),'source_sha256':H(source),'candidate_path':str(candidate.relative_to(P)),'candidate_sha256':H(candidate),'resolution':list(a.size),'max_channel_difference_8bit':max(diff),'mean_abs_channel_difference':sum(diff)/len(diff),'rmse_channel_difference':math.sqrt(sum(x*x for x in diff)/len(diff)),'changed_pixels':count,'changed_pixel_fraction':count/(a.width*a.height),'exact_pixels':aa==bb})
report={'check':'r19_r20_matched_pixel_comparison','source_glb_sha256':H(OLD/'conifer-tree.glb'),'candidate_glb_sha256':H(P/'conifer-tree.glb'),'same_camera_lighting_samples_resolution':True,'frame_count':len(rows),'views':rows,'observations':['All exact FLOAT32 positions, indices, materials and transforms are separately compared.','Images are not all pixel-identical; every actual difference is retained.','Silhouette equality, small channel differences and maker visual inspection are supporting evidence, not independent perceptual approval.'],'limitations':'Actual CPU Cycles reimports, not target Three.js GPU or populated-scene performance.'}
output=P/'pixel-comparison.report.json'
if output.exists():raise RuntimeError('Use fresh report path')
output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps([{k:r[k] for k in ['view','resolution','max_channel_difference_8bit','changed_pixels','changed_pixel_fraction','exact_pixels']} for r in rows],indent=2))
