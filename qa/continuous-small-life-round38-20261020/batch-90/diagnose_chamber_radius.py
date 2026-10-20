exec(open('/workspace/shared/lowpoly-batch90-independent-qa-20261020/measure_glb_relief.py').read().split("for aid in ")[0])
aid='rosary-shaped-chambered-burrow-hormosiroidea-type'
script=open('/workspace/shared/lowpoly-batch90-independent-qa-20261020/measure_glb_relief.py').read();setup=script.split("for aid in ")[1].split("\n",1)[1].split(' pts=np.unique')[0];exec('\n'.join(line[1:] for line in setup.splitlines()))
rows=[]
for i in range(13):
 t=i/12;x=-.04+.08*t;y=.009*math.sin(math.tau*t-.4);n=np.array([-.009*math.tau*math.cos(math.tau*t-.4),.08]);n/=np.linalg.norm(n);row={'lobe':i,'threshold_semibreadths':{}}
 for eps in [1e-8,1e-7,1e-6,1e-5,2e-5,8e-5]:
  rr=[]
  for sign in [-1,1]:
   lo,hi=.0015,.004
   for _ in range(24):
    mid=(lo+hi)/2
    if z(x+sign*n[0]*mid,y+sign*n[1]*mid)>T+eps:lo=mid
    else:hi=mid
   rr.append((lo+hi)/2)
  row['threshold_semibreadths'][str(eps)]=rr
 row['excess_at_3_2mm_relief']=[z(x+sg*n[0]*.0032,y+sg*n[1]*.0032)-T for sg in [-1,1]];rows.append(row)
report={'asset_id':aid,'method':'Independent exact GLB triangle interpolation, radial normal section through all13 frozen centers. Threshold sweep isolates microscopic triangulation ramps from lobe body. Thresholds are diagnostics, not new acceptance limits.','rows':rows}
(O/aid/'chamber-radius-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
for row in rows:print(row['lobe'],row['threshold_semibreadths'],row['excess_at_3_2mm_relief'])
