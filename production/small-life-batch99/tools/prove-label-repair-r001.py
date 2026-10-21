#!/usr/bin/env python3
"""Read-only exact source and exported per-component differential proof."""
import bpy,sys,json,pathlib,hashlib,collections,struct,os,datetime
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from qa_glb import read_glb,accessor_values,audit_glb
from asset_common import audit_source
from check_source_export import compare_source_audit
old,new,out=map(pathlib.Path,sys.argv[sys.argv.index('--')+1:]);a=old.stem
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def canonical(t):return min(tuple(t[i:]+t[:i]) for i in range(len(t)))
def topology(triangles):
    edges=collections.defaultdict(list);caps=collections.Counter();lo=min(v[1] for t in triangles for v in t);hi=max(v[1] for t in triangles for v in t)
    for ti,t in enumerate(triangles):
        for x,y in zip(t,t[1:]+t[:1]):edges[tuple(sorted((x,y)))].append((x,y,ti))
        n=(Vector(t[1])-Vector(t[0])).cross(Vector(t[2])-Vector(t[0]))
        if max(v[1] for v in t)-min(v[1] for v in t)<1e-9:
            side='front' if abs(t[0][1]-lo)<1e-8 else 'back';caps[side+('_outward' if (n.y<0)==(side=='front') else '_inward')]+=1
    adjacency=collections.defaultdict(set)
    for es in edges.values():
        for e in es:
            adjacency[e[2]].update(v[2] for v in es if v[2]!=e[2])
    unseen=set(range(len(triangles)));shells=[]
    while unseen:
        stack=[unseen.pop()];seen=set(stack)
        while stack:
            for j in adjacency[stack.pop()]&unseen:unseen.remove(j);seen.add(j);stack.append(j)
        ts=[triangles[j] for j in seen];origin=Vector(ts[0][0]);vol=sum((Vector(t[0])-origin).dot((Vector(t[1])-origin).cross(Vector(t[2])-origin))/6 for t in ts)
        shells.append({'triangles':len(ts),'signed_volume_m3':vol})
    return {'triangles':len(triangles),'unpaired_coordinate_edges':sum(len(es)!=2 for es in edges.values()),'same_direction_shared_coordinate_edges':sum(len(es)==2 and es[0][:2]!=tuple(reversed(es[1][:2])) for es in edges.values()),'cap_winding':dict(caps),'shells':shells,'all_shell_volumes_positive':all(s['signed_volume_m3']>0 for s in shells)}
def snapshot(src):
    bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
    con=json.loads(bpy.data.texts['BATCH99_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[con['object_name']];o.data.calc_loop_triangles();coords=[tuple(o.matrix_world@v.co) for v in o.data.vertices];components={};allids=[]
    for c in con['components']:
        ids=c['vertices'];iset=set(ids);allids+=ids;local={i:j for j,i in enumerate(ids)};polys=[p for p in o.data.polygons if set(p.vertices)<=iset];ts=[t for t in o.data.loop_triangles if set(t.vertices)<=iset];group=o.vertex_groups[c['tag']]
        actual={v.index for v in o.data.vertices if any(g.group==group.index and g.weight==1 for g in v.groups)}
        desc={'vertices':[coords[i] for i in ids],'polygons':[(tuple(local[i] for i in p.vertices),p.material_index,p.use_smooth,tuple(p.normal)) for p in polys],'triangles':[(tuple(local[i] for i in t.vertices),t.material_index) for t in ts],'contract':c}
        components[c['tag']]={'descriptor':desc,'sha256':sha(desc),'world_triangles':[tuple(coords[i] for i in t.vertices) for t in ts],'triangle_materials':[t.material_index for t in ts],'group_exact':actual==iset,'vertex_count':len(ids),'triangle_count':len(ts)}
        if c['tag']=='enlarged_label':
            indexedges=collections.Counter(tuple(sorted((x,y))) for t in ts for x,y in zip(tuple(t.vertices),tuple(t.vertices)[1:]+tuple(t.vertices)[:1]));components[c['tag']]['topology']=topology(components[c['tag']]['world_triangles']);components[c['tag']]['topology'].update(raw_index_boundary_edges=sum(n==1 for n in indexedges.values()),raw_index_nonmanifold_edges=sum(n>2 for n in indexedges.values()))
    col=next(c for c in bpy.data.collections if c.get('asset_root'));sa=audit_source(col,max_triangles=14000);ga=audit_glb(src.with_suffix('.glb'),max_triangles=14000,max_materials=6,max_primitives=30);compare=compare_source_audit(sa,ga,h(src),h(src.with_suffix('.glb')))
    doc,bin,raw=read_glb(src.with_suffix('.glb'));export=[]
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            v=accessor_values(doc,bin,p['attributes']['POSITION']);ix=[x[0] for x in accessor_values(doc,bin,p['indices'])];normals=accessor_values(doc,bin,p['attributes']['NORMAL'])
            for j in range(0,len(ix),3):
                ind=ix[j:j+3];t=tuple((v[i][0],-v[i][2],v[i][1]) for i in ind);export.append((t,p['material'],tuple(normals[i] for i in ind)))
    assignments=collections.defaultdict(list);tri_to_tags=collections.defaultdict(set)
    for tag,c in components.items():
        for t in c['world_triangles']:tri_to_tags[tuple(sorted(t))].add(tag)
    unmatched=[]
    for t,mat,norm in export:
        tags=tri_to_tags.get(tuple(sorted(t)),set())
        if len(tags)!=1:unmatched.append({'triangle':t,'matching_tags':sorted(tags)});continue
        tag=next(iter(tags));assignments[tag].append((canonical(list(zip(t,norm))),mat))
    for tag,c in components.items():c['glb_triangles']=sorted(assignments[tag]);c['glb_sha256']=sha(c['glb_triangles'])
    label_export=[t for t,mat,norm in export if tuple(sorted(t)) in {tuple(sorted(t)) for t in components['enlarged_label']['world_triangles']}]
    return {'source_sha256':h(src),'glb_sha256':h(src.with_suffix('.glb')),'object_matrix':[list(row) for row in o.matrix_world],'object_name':o.name,'materials':doc['materials'],'nodes':doc['nodes'],'scenes':doc['scenes'],'component_membership_complete':len(allids)==len(set(allids))==len(coords) and set(allids)==set(range(len(coords))),'source_export':compare,'glb_audit':ga,'components':components,'glb_unassigned_triangles':unmatched,'glb_label_topology':topology(label_export),'source_mutated':False}
before=snapshot(old);after=snapshot(new);comparisons=[]
for tag,c in before['components'].items():
    d=after['components'][tag];comparisons.append({'tag':tag,'is_label':tag=='enlarged_label','before_source_component_sha256':c['sha256'],'after_source_component_sha256':d['sha256'],'source_component_exact':c['descriptor']==d['descriptor'],'before_glb_component_sha256':c['glb_sha256'],'after_glb_component_sha256':d['glb_sha256'],'glb_component_exact':c['glb_triangles']==d['glb_triangles'],'before_vertices':c['vertex_count'],'after_vertices':d['vertex_count'],'before_triangles':c['triangle_count'],'after_triangles':d['triangle_count'],'after_group_exact':d['group_exact']})
report={'asset_id':a,'pid':os.getpid(),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_saved':False,'source_mutated':False,'method':'Exact float, polygon winding, material index, normal, contract and GLB triangle-plus-normal comparison per component. No weld or diagnostic normal recalculation. All exported triangles assigned by exact source coordinates.','before_source_sha256':before['source_sha256'],'after_source_sha256':after['source_sha256'],'before_glb_sha256':before['glb_sha256'],'after_glb_sha256':after['glb_sha256'],'nonlabel_components_all_exact':all(x['source_component_exact'] and x['glb_component_exact'] for x in comparisons if not x['is_label']),'object_transform_exact':before['object_matrix']==after['object_matrix'],'glb_nodes_and_scenes_exact':before['nodes']==after['nodes'] and before['scenes']==after['scenes'],'glb_materials_exact':before['materials']==after['materials'],'all_component_membership_exact':after['component_membership_complete'] and all(x['after_group_exact'] for x in comparisons),'before_glb_unassigned_triangles':before['glb_unassigned_triangles'],'after_glb_unassigned_triangles':after['glb_unassigned_triangles'],'components':comparisons,'before_source_label':before['components']['enlarged_label']['topology'],'after_source_label':after['components']['enlarged_label']['topology'],'before_glb_label':before['glb_label_topology'],'after_glb_label':after['glb_label_topology'],'source_export':after['source_export'],'glb_audit':after['glb_audit'],'label_coordinate_set_exact':set(v for t in before['components']['enlarged_label']['world_triangles'] for v in t)==set(v for t in after['components']['enlarged_label']['world_triangles'] for v in t)}
checks=[report[k] for k in ['nonlabel_components_all_exact','object_transform_exact','glb_nodes_and_scenes_exact','glb_materials_exact','all_component_membership_exact','label_coordinate_set_exact']]+[not report['before_glb_unassigned_triangles'],not report['after_glb_unassigned_triangles']]
for k in ['after_source_label','after_glb_label']:checks += [report[k]['unpaired_coordinate_edges']==0,report[k]['same_direction_shared_coordinate_edges']==0,report[k]['all_shell_volumes_positive'],not any(n for name,n in report[k]['cap_winding'].items() if name.endswith('_inward'))]
report['maker_differential_status']='pass' if all(checks) else 'fail';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['asset_id','maker_differential_status','nonlabel_components_all_exact','label_coordinate_set_exact']}));assert all(checks),'Bounded repair failed; no expanded geometry scope is permitted.'
