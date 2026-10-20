import bpy,sys,json,hashlib,math
from collections import defaultdict
args=sys.argv[sys.argv.index('--')+1:];out=args[0];paths=args[1:]
def h(obj):return hashlib.sha256(json.dumps(obj,separators=(',',':'),sort_keys=True).encode()).hexdigest()
def canonical_cycle(seq):
 vals=list(seq); candidates=[]
 for arr in (vals,list(reversed(vals))):
  for k in range(len(arr)): candidates.append(tuple(arr[k:]+arr[:k]))
 return min(candidates)
def components(path):
 bpy.ops.wm.open_mainfile(filepath=path);result={};total=0
 for ob in sorted([x for x in bpy.data.objects if x.type=='MESH' and x.name!='coherent_angular_matrix_outcrop'],key=lambda x:x.name):
  me=ob.data;n=len(me.vertices);parent=list(range(n))
  def find(x):
   while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
   return x
  def union(a,b):
   x,y=find(a),find(b)
   if x!=y:parent[y]=x
  for p in me.polygons:
   ids=list(p.vertices)
   for v in ids[1:]:union(ids[0],v)
  comps=defaultdict(lambda:{'verts':set(),'faces':[]})
  for p in me.polygons:
   root=find(p.vertices[0]); comps[root]['faces'].append(p)
   comps[root]['verts'].update(p.vertices)
  arr=[]
  for comp in comps.values():
   coords=[tuple(float(c) for c in me.vertices[i].co) for i in comp['verts']]
   coord_by_idx={i:tuple(float(c) for c in me.vertices[i].co) for i in comp['verts']}
   sorted_coords=sorted(coords);faces=[]
   for p in comp['faces']:
    cycle=[coord_by_idx[i] for i in p.vertices]
    faces.append((canonical_cycle(cycle),int(p.material_index)))
   faces.sort();coords_hash=h({'vertices':sorted_coords,'faces':faces})
   center=[sum(v[i] for v in coords)/len(coords) for i in range(3)]
   lo=[min(v[i] for v in coords) for i in range(3)];hi=[max(v[i] for v in coords) for i in range(3)]
   arr.append({'center':center,'bbox_min':lo,'bbox_max':hi,'vertices':len(coords),'polygons':len(comp['faces']),'triangles':sum(max(0,len(p.vertices)-2) for p in comp['faces']),'canonical_sha256':coords_hash})
  arr.sort(key=lambda a:(a['center'][0],a['center'][1],a['center'][2]))
  result[ob.name]=arr;total+=len(arr)
 return {'path':path,'objects':result,'fragment_components':total}
R=[components(p) for p in paths];changes=[];comp_counts=[]
for name in sorted(set(R[0]['objects'])|set(R[1]['objects'])):
 a=R[0]['objects'].get(name,[]);b=R[1]['objects'].get(name,[])
 pairs=[]
 # stable greedy nearest-center matching, within same aggregate object
 left=set(range(len(a)));right=set(range(len(b)))
 while left and right:
  best=min(((sum((a[i]['center'][k]-b[j]['center'][k])**2 for k in range(3)),i,j) for i in left for j in right),key=lambda x:x[0])
  dist,i,j=best;left.remove(i);right.remove(j)
  pairs.append({'old_index':i,'new_index':j,'center_distance_m':math.sqrt(dist),'same_canonical_geometry':a[i]['canonical_sha256']==b[j]['canonical_sha256'],'old_sha256':a[i]['canonical_sha256'],'new_sha256':b[j]['canonical_sha256']})
 changed=[p for p in pairs if not p['same_canonical_geometry']]
 if changed or left or right:changes.append({'object':name,'old_components':len(a),'new_components':len(b),'changed_count':len(changed),'unmatched_old':sorted(left),'unmatched_new':sorted(right),'matches':pairs})
 comp_counts.append({'object':name,'r002':len(a),'r003':len(b),'changed':len(changed)})
result={'read_only':True,'matching':'within each aggregate fragment mesh, minimum center-distance greedy match, then exact canonicalized vertex and polygon-coordinate/material-index hash comparison; clast identity inferred from preserved locations, not maker IDs.','r002':R[0],'r003':R[1],'comparison':{'fragment_component_counts':comp_counts,'r002_component_total':R[0]['fragment_components'],'r003_component_total':R[1]['fragment_components'],'changed_clast_count':sum(x['changed_count'] for x in changes),'aggregate_meshes_with_changed_components':[x['object'] for x in changes],'changes':changes}}
open(out,'w').write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['comparison'],indent=2)[:4500])
