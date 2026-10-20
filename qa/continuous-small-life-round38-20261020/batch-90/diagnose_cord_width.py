import json,sys,math,pathlib,hashlib,numpy as np
R=pathlib.Path('/workspace/shared/lowpoly-batch90-20261020');O=pathlib.Path('/workspace/shared/lowpoly-batch90-independent-qa-20261020');sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values
script=open(O/'measure_glb_relief.py').read();aid='lumbricaria-thread-like-coprolite';setup=script.split('for aid in ')[1].split('\n',1)[1].split(' pts=np.unique')[0];exec('\n'.join(line[1:] for line in setup.splitlines()))
paths=json.load(open(R/'production/batch90/assets'/aid/'r001/geometry-semantics.json'))['paths'];rows=[]
for pi,vi in [(0,2),(0,106),(1,2),(1,106),(2,2),(2,71)]:
 path=np.array(paths[pi]);q=path[vi];t=path[vi+1]-path[vi-1];n=np.array([-t[1],t[0]]);n/=np.linalg.norm(n);row={'path':pi,'vertex':vi,'center_xy':q.tolist(),'threshold_semibreadths':{}}
 for eps in [1e-8,1e-7,1e-6,1e-5,8e-5]:
  rr=[]
  for sg in [-1,1]:
   lo,hi=.0002,.003
   for _ in range(24):
    mid=(lo+hi)/2
    if z(q[0]+sg*n[0]*mid,q[1]+sg*n[1]*mid)>T+eps:lo=mid
    else:hi=mid
   rr.append((lo+hi)/2)
  row['threshold_semibreadths'][str(eps)]=rr
 row['relief_at_nominal_1_3mm']=[z(q[0]+sg*n[0]*.0013,q[1]+sg*n[1]*.0013)-T for sg in [-1,1]];rows.append(row)
(O/aid/'cord-width-diagnostic.json').write_text(json.dumps({'method':'Actual exported mesh transverse sections on six trailing-end source path positions; not new acceptance thresholds. Some sample positions may lie near crossings.','rows':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))
