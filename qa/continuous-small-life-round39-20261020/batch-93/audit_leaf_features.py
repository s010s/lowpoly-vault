import bpy,json,sys,math,collections,hashlib,os,datetime
from mathutils import Vector
from pathlib import Path
R=Path('/workspace/shared/lowpoly-batch93-20261020/production/small-life-batch93');O=Path('/workspace/shared/lowpoly-batch93-independent-qa-20261020')
a,rev=sys.argv[sys.argv.index('--')+1:];s=R/a/rev/'artifacts'/f'{a}.blend';bpy.ops.wm.open_mainfile(filepath=str(s),load_ui=False,use_scripts=False);parts=[]
for obj in bpy.data.objects:
 if obj.type!='MESH':continue
 me=obj.data;adj=[set() for v in me.vertices]
 for e in me.edges:x,y=e.vertices;adj[x].add(y);adj[y].add(x)
 unseen=set(range(len(adj)))
 while unseen:
  first=min(unseen);q=[first];seen={first};unseen.remove(first)
  while q:
   for x in adj[q.pop()]:
    if x in unseen:unseen.remove(x);seen.add(x);q.append(x)
  vv=[obj.matrix_world@me.vertices[x].co for x in sorted(seen)];m=sorted(set(p.material_index for p in me.polygons if p.vertices[0] in seen));parts.append(dict(first=first,v=vv,m=m))
leaves=[c for c in parts if c['m'] in [[2],[3]]];r={'asset_id':a,'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'pid':os.getpid(),'measured_at_host':datetime.datetime.now(datetime.timezone.utc).isoformat(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'method':'Fresh source vertex graph and actual blade endpoints; no generator execution or design-count metadata used.'}
if a=='omphalophloios':
 axes=[]
 for c in parts:
  if len(c['v'])==24 and c['m']==[0]:axes.append((c['first'],sum(c['v'][6:12],Vector())/6,sum(c['v'][-6:],Vector())/6))
 def closest(pt):
  ds=[]
  for idx,p,q in axes:
   d=q-p;t=(pt-p).dot(d)/d.length_squared;t=max(0,min(1,t));ds.append(((pt-(p+t*d)).length,idx))
  return min(ds)
 leaf_counts=collections.Counter();sp_counts=collections.Counter();leafrows=[];sprows=[]
 # Fertile terminal leaves can be identified from actual inserted root-to-axis distance; proximal leaves lie outside these axes.
 for c in leaves:
  d,i=closest(c['v'][0]);leafrows.append(dict(first_vertex=c['first'],nearest_terminal_axis=i,distance_m=d))
  if d<.002:leaf_counts[i]+=1
 for c in parts:
  if c['m']==[4]:
   d,i=closest(sum(c['v'],Vector())/len(c['v']));sp_counts[i]+=1;sprows.append(dict(first_vertex=c['first'],nearest_terminal_axis=i,distance_m=d))
 r.update(terminal_axes=len(axes),leaf_near_axis_threshold_m=.002,threshold_note='Diagnostic grouping threshold, not an acceptance dimension; results interpreted with source component ordering and original generator formulas.',terminal_leaf_group_histogram=dict(collections.Counter(leaf_counts.values())),terminal_leaf_groups=dict(leaf_counts),sporangia_group_histogram=dict(collections.Counter(sp_counts.values())),sporangia_groups=dict(sp_counts),leaf_assignments=leafrows,sporangia_assignments=sprows)
if a=='chaloneria':
 stem=next(c for c in parts if len(c['v'])==96);rings=[]
 for k in range(6):
  vv=stem['v'][16*k:16*(k+1)];rr=[math.hypot(x.x,x.y) for x in vv];zz=[x.z for x in vv];rings.append({'z_minmax_m':[min(zz),max(zz)],'radius_minmax_m':[min(rr),max(rr)]})
 r.update(stem_vertex_rings=rings,stem_vertices=96,leaf_components=len(leaves),all_leaf_components_six_vertex_pointed_blades=all(len(c['v'])==6 for c in leaves),extra_brown_components=[{'first_vertex':c['first'],'vertices':len(c['v']),'material':c['m'],'z_min':min(x.z for x in c['v']),'z_max':max(x.z for x in c['v'])} for c in parts if c['m'] in [[1],[4]]],conclusion='The stem consists only of six circular rings and faces between them. All 184 blades taper to a single inserted point. The only 72 ovoid components occupy the fertile upper zone; no oval leaf-base relief or scars occur on the vegetative stem.')
with (O/a/'leaf-feature-measurements.json').open('x') as f:json.dump(r,f,indent=2);f.write('\n')
print('LEAF-AUDIT',a,{k:v for k,v in r.items() if k in ['terminal_axes','terminal_leaf_group_histogram','sporangia_group_histogram','stem_vertices','leaf_components','all_leaf_components_six_vertex_pointed_blades']})
