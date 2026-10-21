import bpy,json,sys,pathlib,hashlib,datetime,collections,math
from mathutils import Vector
W=pathlib.Path('/workspace/shared/lowpoly-batch101-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch101-independent-qa-20261021');aid=sys.argv[sys.argv.index('--')+1];rev='r002'if aid=='protospongia'else'r001';B=W/'production/small-life-batch101'/aid/rev;src=B/'artifacts'/f'{aid}.blend';bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);ct=json.loads(bpy.data.texts['BATCH101_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];o.data.calc_loop_triangles();v=[o.matrix_world@p.co for p in o.data.vertices];tt=[tuple(t.vertices)for t in o.data.loop_triangles];out=[]
for c in ct['components']:
 ids=set(c['vertices']);fs=[t for t in tt if set(t)<=ids];edges=collections.defaultdict(list);adj=collections.defaultdict(set)
 for f in fs:
  for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted([a,b]))].append((a,b));adj[a].add(b);adj[b].add(a)
 left=set(ids);n=0
 while left:
  todo=[min(left)];seen=set()
  while todo:
   i=todo.pop()
   if i in seen:continue
   seen.add(i);todo.extend(adj[i]-seen)
  left-=seen;n+=1
 rec={'tag':c['tag'],'kind':c['kind'],'vertex_connected_components':n,'edge_closed':all(len(e)==2 for e in edges.values()),'shared_tissue_region':c.get('shared_topology',False)}
 if c['kind']=='leaf':
  vv=[v[i]for i in c['vertices']];N=len(vv)//2;outline=vv[:N];base=(outline[0]+outline[-1])/2;ax=[(o.matrix_world.to_3x3()@Vector(d)).normalized()for d in c['axes']];local=[((p-base).dot(ax[1]),(p-base).dot(ax[0]))for p in outline];rr=[math.hypot(x,y)for x,y in local];peaks=[i for i in range(1,N-1)if rr[i]>rr[i-1] and rr[i]>rr[i+1]];rec['radial_margin_lobe_tip_count']=len(peaks);rec['lobe_tip_coordinates_in_leaf_plane_m']=[local[i]for i in peaks]
 out.append(rec)
r={'asset_id':aid,'revision':rev,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_unit_system':bpy.context.scene.unit_settings.system,'source_unit_scale_length':bpy.context.scene.unit_settings.scale_length,'all_non_tissue_components_closed_connected':all(x['vertex_connected_components']==1 and x['edge_closed']for x in out if not x['shared_tissue_region']),'components':out};(O/aid/'feature-audit.json').write_text(json.dumps(r,indent=2)+'\n');print(aid,r['all_non_tissue_components_closed_connected'],[(x['tag'],x.get('radial_margin_lobe_tip_count'))for x in out if x['kind']=='leaf'])
