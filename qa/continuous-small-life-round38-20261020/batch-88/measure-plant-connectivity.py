import json,numpy as np
from pathlib import Path
Q=Path('/workspace/shared/lowpoly-batch88-independent-qa-20261020/baragwanathia');obj=json.load(open(Q/'mesh-measure-input.json'))
a=next(v for k,v in obj.items() if '_axis_' in k);v=np.array(a['vertices']);axes=[]
for i in range(7):
 rings=v[i*192:(i+1)*192].reshape(24,8,3);centers=rings.mean(axis=1);rads=np.linalg.norm(rings-centers[:,None,:],axis=2).mean(axis=1);axes.append((centers,rads))
def dist(p,ax):
 c,r=ax;vv=c[1:]-c[:-1];t=np.clip(np.sum((p-c[:-1])*vv,axis=1)/np.sum(vv*vv,axis=1),0,1);dd=np.linalg.norm(p-(c[:-1]+vv*t[:,None]),axis=1)-(r[:-1]+(r[1:]-r[:-1])*t);idx=np.argmin(dd);return float(dd[idx]),int(idx)
links=[]
for i,(c,r) in enumerate(axes):
 for j in range(i):
  # Actual end ring centers are inside the other measured polygonal tube envelope.
  clearance,k=dist(c[0],axes[j]);
  if clearance<0:links.append({'axis':i,'parent_candidate':j,'base_center_inside_radius_envelope_m':clearance,'parent_segment':k})
leaf=[]
for name,o in obj.items():
 if '_leaf' not in name:continue
 vv=np.array(o['vertices'])
 for i in range(0,len(vv),10):
  candidates=[dist(vv[i],ax)[0] for ax in axes];leaf.append(min(candidates))
report={'method':'Actual source axis rings independently averaged; each leaf base tested against nearest measured piecewise centerline/radius envelope. This is geometric attachment evidence, not a Boolean union or exhaustive intersection proof.','axis_count':7,'axis_base_links':links,'leaf_count':len(leaf),'leaf_base_clearance_to_axis_envelope_m':{'min':min(leaf),'max':max(leaf)},'leaf_bases_inside_envelopes':sum(x<=0 for x in leaf),'source_axis_components_are_closed_but_not_welded':True}
(Q/'connectivity-measurements.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
