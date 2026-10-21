import bpy,json,sys,pathlib,math,hashlib,datetime
from mathutils import Vector
from mathutils.bvhtree import BVHTree
O=pathlib.Path(__file__).parent;R=pathlib.Path('/workspace/shared/lowpoly-batch108-20261021');a=sys.argv[-1];rev='r003' if a=='placocystites' else 'r002';src=R/'production/batch-108'/a/rev/'artifacts'/f'{a}.blend';bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);ct=json.loads(bpy.data.texts['BATCH108_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];o.data.calc_loop_triangles();V=[o.matrix_world@v.co for v in o.data.vertices];T=[tuple(t.vertices) for t in o.data.loop_triangles];out=[]
if a=='placocystites':
 c=next(x for x in ct['components'] if x['tag']=='aulacophore');ids=c['vertices']
 for rn in range(0,22):
  ring=[V[i] for i in ids[rn*12:(rn+1)*12]];cc=sum(ring,Vector())/12;n=(ring[1]-ring[0]).cross(ring[2]-ring[1]).normalized();signed=[(ring[(i+1)%12]-ring[i]).cross(ring[(i+2)%12]-ring[(i+1)%12]).dot(n) for i in range(12)];out.append(dict(ring=rn,world_vertices=[list(v) for v in ring],all_same_sign=all(x>0 for x in signed) or all(x<0 for x in signed),signed_corner_cross_products=signed))
else:
 prior=json.loads((O/a/'dense-contact-diagnostic.json').read_text());targets=[x for x in prior['checks'] if x['witness'] is None and not x['other_intersecting_components']]
 for c in targets:
  ids=set(c['actual_vertices']);fs=[t for t in T if all(i in ids for i in t)];rest=[t for t in T if not all(i in ids for i in t)];own=BVHTree.FromPolygons(V,fs,all_triangles=True);tree=BVHTree.FromPolygons(V,rest,all_triangles=True);distances=[];signed=[]
  for i in ids:
   q,n,_,d=tree.find_nearest(V[i]);distances.append(d);signed.append((V[i]-q).dot(n))
  centroid=sum((V[i] for i in ids),Vector())/len(ids);q,n,_,d=tree.find_nearest(centroid)
  out.append(dict(component=c['component'],part=c['part'],original_vertices=sorted(ids),triangles=fs,intersections_with_entire_rest_scene=len(own.overlap(tree)),nearest_rest_surface_distances=distances,signed_nearest_rest_distances=signed,centroid_signed_nearest_surface=(centroid-q).dot(n),centroid=list(centroid),bounds={'min':[min(V[i][k] for i in ids) for k in range(3)],'max':[max(V[i][k] for i in ids) for k in range(3)]}))
r=dict(asset=a,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=out);(O/a/'targeted-proof.json').write_text(json.dumps(r,indent=2)+'\n');print(a,len(out),'targeted checks')
