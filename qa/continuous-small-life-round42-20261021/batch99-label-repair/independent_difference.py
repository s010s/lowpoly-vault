import sys
sys.dont_write_bytecode=True
import bpy,json,pathlib,hashlib,collections,os,datetime
from mathutils import Vector
Q=pathlib.Path(__file__).parent; W=pathlib.Path('/workspace/shared/lowpoly-batch99-label-repair-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch99-20261021');a=sys.argv[sys.argv.index('--')+1];old,new={'monetianthus':('r001','r002'),'proterocladus':('r002','r003')}[a]
sys.path.insert(0,str(W/'scripts'));from qa_glb import read_glb,accessor_values,audit_glb
from asset_common import audit_source
from check_source_export import compare_source_audit
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sha=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def canon(t):return min(t[i:]+t[:i] for i in range(len(t)))
def topology(triangles):
 edges=collections.defaultdict(list);cap=collections.Counter();adj=collections.defaultdict(set);ys=[v[1] for t in triangles for v in t];lo=min(ys);hi=max(ys)
 for i,t in enumerate(triangles):
  for x,y in zip(t,t[1:]+t[:1]):edges[tuple(sorted((x,y)))].append((x,y,i))
  if max(v[1] for v in t)-min(v[1] for v in t)<1e-9:
   side='front' if abs(t[0][1]-lo)<1e-8 else 'back'
   n=(Vector(t[1])-Vector(t[0])).cross(Vector(t[2])-Vector(t[0]));cap[side+('_outward' if (n.y<0)==(side=='front') else '_inward')]+=1
 for uses in edges.values():
  for x in uses:
   adj[x[2]].update(y[2] for y in uses if y[2]!=x[2])
 unseen=set(range(len(triangles)));shells=[]
 while unseen:
  stack=[unseen.pop()];component=set(stack)
  while stack:
   j=stack.pop()
   for k in adj[j]&unseen:unseen.remove(k);component.add(k);stack.append(k)
  origin=Vector(triangles[min(component)][0]);vol=0
  for j in component:
   p,q,r=[Vector(x)-origin for x in triangles[j]];vol+=p.dot(q.cross(r))/6
  shells.append({'triangles':len(component),'signed_volume_m3':vol})
 return {'triangles':len(triangles),'coordinate_boundary_or_nonmanifold_edges':sum(len(v)!=2 for v in edges.values()),'same_direction_coordinate_edges':sum(len(v)==2 and v[0][:2]!=tuple(reversed(v[1][:2])) for v in edges.values()),'caps':dict(cap),'shells':shells,'closed_consistently_oriented':all(len(v)==2 and v[0][:2]==tuple(reversed(v[1][:2])) for v in edges.values()),'classification':{'coordinate_grouping':'exact float tuple, no rounding or virtual weld','cap_plane_spread_lt_m':1e-9,'front_plane_proximity_lt_m':1e-8,'original_convention_unchanged':True}}
def value(v):
 if isinstance(v,(str,int,float,bool)) or v is None:return v
 try:return list(v)
 except TypeError:return str(v)
def materials():
 return {m.name:{'rgba':list(m.diffuse_color),'roughness':m.roughness,'metallic':m.metallic,'use_nodes':m.use_nodes,'backface_culling':m.use_backface_culling,'surface_render_method':m.surface_render_method,'nodes':[{'name':n.name,'type':n.bl_idname,'inputs':{s.identifier:value(s.default_value) for s in n.inputs if hasattr(s,'default_value')}} for n in m.node_tree.nodes] if m.use_nodes else [],'links':sorted((l.from_node.name,l.from_socket.identifier,l.to_node.name,l.to_socket.identifier) for l in m.node_tree.links) if m.use_nodes else []} for m in bpy.data.materials}
def snapshot(path,export=False):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);bpy.context.view_layer.update();contract=json.loads(bpy.data.texts['BATCH99_COMPONENT_CONTRACT.json'].as_string());obj=bpy.data.objects[contract['object_name']];mesh=obj.data;mesh.calc_loop_triangles();vs=[tuple(obj.matrix_world@v.co) for v in mesh.vertices];comps={};seen=[];match=collections.defaultdict(set)
 for c in contract['components']:
  ids=c['vertices'];iset=set(ids);seen+=ids;local={i:j for j,i in enumerate(ids)};ps=[p for p in mesh.polygons if set(p.vertices)<=iset];ts=[t for t in mesh.loop_triangles if set(t.vertices)<=iset];world=[tuple(vs[i] for i in t.vertices) for t in ts]
  descriptor={'contract':c,'vertices':[vs[i] for i in ids],'polygons':[(tuple(local[i] for i in p.vertices),p.material_index,p.use_smooth,tuple(p.normal),[tuple(mesh.corner_normals[j].vector) for j in p.loop_indices]) for p in ps],'triangles':[(tuple(local[i] for i in t.vertices),t.material_index) for t in ts]}
  group=obj.vertex_groups[c['tag']];actual={v.index for v in mesh.vertices if any(g.group==group.index and g.weight==1 for g in v.groups)}
  edges=collections.Counter(tuple(sorted((x,y))) for t in ts for x,y in zip(tuple(t.vertices),tuple(t.vertices)[1:]+tuple(t.vertices)[:1]))
  comps[c['tag']]={'descriptor':descriptor,'source_sha256':sha(descriptor),'triangles':world,'group_exact':actual==iset,'vertices':len(ids),'triangle_count':len(ts),'raw_index_boundary_edges':sum(n==1 for n in edges.values()),'raw_index_nonmanifold_edges':sum(n>2 for n in edges.values())}
  for t in world:match[tuple(sorted(t))].add(c['tag'])
 doc,blob,_=read_glb(path.with_suffix('.glb'));exported=collections.defaultdict(list);export_label=[];unmatched=[]
 for m in doc['meshes']:
  for p in m['primitives']:
   pos=accessor_values(doc,blob,p['attributes']['POSITION']);norm=accessor_values(doc,blob,p['attributes']['NORMAL']);ids=[x[0] for x in accessor_values(doc,blob,p['indices'])]
   for i in range(0,len(ids),3):
    inds=ids[i:i+3];t=tuple((pos[j][0],-pos[j][2],pos[j][1]) for j in inds);tags=match[tuple(sorted(t))]
    if len(tags)!=1:unmatched.append(t);continue
    tag=next(iter(tags));exported[tag].append((canon(tuple((t[k],tuple(norm[j])) for k,j in enumerate(inds))),p['material']))
    if tag=='enlarged_label':export_label.append(t)
 for tag in comps:comps[tag]['glb_triangles_with_normals']=sorted(exported[tag])
 colls=[c for c in bpy.data.collections if c.get('asset_root')];assert len(colls)==1;col=colls[0];sa=audit_source(col,max_triangles=14000);ga=audit_glb(path.with_suffix('.glb'),14000,6,30);se=compare_source_audit(sa,ga,h(path),h(path.with_suffix('.glb')))
 report={'source_hash':h(path),'glb_hash':h(path.with_suffix('.glb')),'components':comps,'membership_complete':len(seen)==len(set(seen))==len(vs) and set(seen)==set(range(len(vs))),'object_transform':[list(row) for row in obj.matrix_world],'materials':materials(),'glb_materials':doc['materials'],'glb_nodes':doc['nodes'],'glb_scenes':doc['scenes'],'source_label':topology(comps['enlarged_label']['triangles']),'glb_label':topology(export_label),'unmatched_glb_triangles':len(unmatched),'source_audit':sa,'glb_audit':ga,'source_export':se,'collection_objects':sorted((o.name,o.type) for o in col.all_objects),'source_scene':{'unit_scale':bpy.context.scene.unit_settings.scale_length,'cameras':[(o.name,[list(r) for r in o.matrix_world]) for o in bpy.data.objects if o.type=='CAMERA']}}
 if export:
  bpy.ops.object.select_all(action='DESELECT')
  for ob in col.all_objects:ob.select_set(True)
  bpy.context.view_layer.objects.active=bpy.data.objects.get(col.get('asset_root',''))
  output=Q/(a+'-fresh-full-collection.glb'); assert not output.exists()
  options=json.loads((path.parent/'metadata.json').read_text())['export_options'];options.update(filepath=str(output));bpy.ops.export_scene.gltf(**options)
  freshdoc,freshbin,freshraw=read_glb(output);report['fresh_full_collection_export']={'sha256':h(output),'byte_identical':output.read_bytes()==path.with_suffix('.glb').read_bytes(),'json_exact':freshdoc==doc,'bin_exact':freshbin==blob,'source_saved':False,'selected_all_collection_objects':True,'options':options}
 return report
before=snapshot(O/'production/small-life-batch99'/a/old/'artifacts'/(a+'.blend'));after=snapshot(W/'production/small-life-batch99'/a/new/'artifacts'/(a+'.blend'),True)
checks=[]
for tag,c in before['components'].items():
 d=after['components'][tag];checks.append({'tag':tag,'source_component_exact':c['descriptor']==d['descriptor'],'glb_component_positions_normals_winding_material_exact':c['glb_triangles_with_normals']==d['glb_triangles_with_normals'],'before_source_sha256':c['source_sha256'],'after_source_sha256':d['source_sha256'],'before_glb_component_sha256':sha(c['glb_triangles_with_normals']),'after_glb_component_sha256':sha(d['glb_triangles_with_normals']),'vertices_before':c['vertices'],'vertices_after':d['vertices'],'triangles_before':c['triangle_count'],'triangles_after':d['triangle_count'],'new_raw_index_boundary_edges':d['raw_index_boundary_edges'],'new_raw_index_nonmanifold_edges':d['raw_index_nonmanifold_edges'],'vertex_group_exact':d['group_exact']})
bl=before['components']['enlarged_label'];al=after['components']['enlarged_label'];report={k:after[k] for k in ['source_hash','glb_hash','source_audit','glb_audit','source_export','fresh_full_collection_export','source_label','glb_label','collection_objects','source_scene']};report.update(asset_id=a,old_revision=old,revision=new,pid=os.getpid(),blender_version=bpy.app.version_string,before_source_hash=before['source_hash'],before_glb_hash=before['glb_hash'],old_source_label=before['source_label'],old_glb_label=before['glb_label'],component_comparisons=checks,nonlabel_components_exact=all(c['source_component_exact'] and c['glb_component_positions_normals_winding_material_exact'] for c in checks if c['tag']!='enlarged_label'),old_raw_label_boundary_edges=bl['raw_index_boundary_edges'],new_raw_label_boundary_edges=al['raw_index_boundary_edges'],label_coordinate_set_exact=set(v for t in bl['triangles'] for v in t)==set(v for t in al['triangles'] for v in t),label_unoriented_triangles_exact=sorted(tuple(sorted(t)) for t in bl['triangles'])==sorted(tuple(sorted(t)) for t in al['triangles']),unmatched_glb_triangles=[before['unmatched_glb_triangles'],after['unmatched_glb_triangles']],membership_complete=before['membership_complete'] and after['membership_complete'],source_materials_before=before['materials'],source_materials_after=after['materials'],source_saved=False)
for k in ['object_transform','materials','glb_materials','glb_nodes','glb_scenes','source_scene','collection_objects']:report[k+'_exact']=before[k]==after[k]
assert report['nonlabel_components_exact'] and report['membership_complete'] and all(c['vertex_group_exact'] for c in checks)
assert all(report[k+'_exact'] for k in ['object_transform','materials','glb_materials','glb_nodes','glb_scenes','source_scene','collection_objects'])
assert report['label_coordinate_set_exact'] and report['label_unoriented_triangles_exact'] and report['unmatched_glb_triangles']==[0,0]
assert report['fresh_full_collection_export']['json_exact'] and report['fresh_full_collection_export']['bin_exact']
for target in ['source_label','glb_label']:
 assert report[target]['closed_consistently_oriented'] and len(report[target]['shells'])==8 and all(s['signed_volume_m3']>0 for s in report[target]['shells'])
 assert report[target]['caps']=={'front_outward':82,'back_outward':82} or report[target]['caps']=={'back_outward':82,'front_outward':82}
 assert report['old_'+target]['same_direction_coordinate_edges']==92 and report['old_'+target]['caps']['back_inward']==82
report['status']='pass';(Q/(a+'-independent-difference.json')).write_text(json.dumps(report,indent=2)+'\n')
with (Q/'recovery-progress.jsonl').open('a') as f:f.write(json.dumps({'stage':a+'_actual_source_glb_difference','status':'pass','at':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
print(a,'PASS exact non-label identity; repaired 8 outward closed shells; fresh full-collection export exact')
