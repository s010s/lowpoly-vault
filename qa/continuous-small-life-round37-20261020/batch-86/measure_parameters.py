import bpy,sys,json,datetime,os,math
from pathlib import Path
from mathutils import Vector
r=Path('/workspace/shared/lowpoly-batch86-20261020');out=Path(__file__).parent;results=[]
for a in json.load(open(r/'production/batch86/handoff-assets.json')):
 p=r/a['path'];bpy.ops.wm.open_mainfile(filepath=str(p/'source.blend'),load_ui=False,use_scripts=False);entry={'asset_id':a['asset_id'],'pid':os.getpid(),'source_saved':False,'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'objects':[]}
 for o in bpy.data.collections['EXPORT'].all_objects:
  if o.type!='MESH':continue
  me=o.data;vs=[o.matrix_world@v.co for v in me.vertices];adj=[[] for v in vs]
  for e in me.edges:
   x,y=e.vertices;adj[x].append(y);adj[y].append(x)
  unseen=set(range(len(vs)));comps=[]
  while unseen:
   q=[unseen.pop()];c=[]
   while q:
    i=q.pop();c.append(i)
    for j in adj[i]:
     if j in unseen:unseen.remove(j);q.append(j)
   lo=[min(vs[i][k] for i in c) for k in range(3)];hi=[max(vs[i][k] for i in c) for k in range(3)]
   comps.append({'vertices':len(c),'min':lo,'max':hi,'size':[hi[k]-lo[k] for k in range(3)]})
  obj={'name':o.name,'component_count':len(comps),'components':comps}
  if a['asset_id']=='tower-karst':obj['tower_relief_above_plain_m']=max(v.z for v in vs)-12.0
  if a['asset_id']=='cinder-cone':
   # Use actual adjacent authored ring geometry, reporting median main flank elevation slope.
   slopes=[]
   for e in me.edges:
    v,w=[vs[i] for i in e.vertices];rv=math.hypot(v.x,v.y);rw=math.hypot(w.x,w.y)
    if 130<rv<300 and 130<rw<300 and abs(rv-rw)>10:
     slopes.append(math.degrees(math.atan2(abs(w.z-v.z),math.hypot(w.x-v.x,w.y-v.y))))
   slopes.sort();obj['main_flank_slope_median_degrees']=slopes[len(slopes)//2];obj['center_floor_m']=float(vs[0].z);obj['rim_high_m']=max(v.z for v in vs);obj['rim_floor_relief_m']=max(v.z for v in vs)-float(vs[0].z)
  if a['asset_id']=='zosterophyllum' and 'rhizome' in o.name:
   runners=[c for c in comps if c['vertices']==24];roots=[c for c in comps if c['vertices']==20]
   lo=[min(c['min'][k] for c in runners) for k in range(3)];hi=[max(c['max'][k] for c in runners) for k in range(3)]
   obj['rhizome_runner_count']=len(runners);obj['rhizome_runner_envelope_m']=[hi[k]-lo[k] for k in range(3)];obj['root_like_count']=len(roots);obj['root_vertical_lengths_m']=[c['size'][2] for c in roots]
  entry['objects'].append(obj)
 results.append(entry)
(out/'parameter-measurements.json').write_text(json.dumps(results,indent=2)+'\n')
print('Measured',[(e['asset_id'],[(o['name'],o.get('rhizome_runner_envelope_m'),o.get('tower_relief_above_plain_m')) for o in e['objects']]) for e in results])
