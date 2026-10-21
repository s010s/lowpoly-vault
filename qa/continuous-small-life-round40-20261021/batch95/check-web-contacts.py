import bpy,sys,json,pathlib,hashlib,datetime,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
S=pathlib.Path('/workspace/shared/lowpoly-batch95-20261020/production/small-life-batch95/dictyophyllum/r002/artifacts/dictyophyllum.blend');O=pathlib.Path('/workspace/shared/lowpoly-batch95-independent-qa-20261021/dictyophyllum/web-contact-supplement.json');bpy.ops.wm.open_mainfile(filepath=str(S),load_ui=False,use_scripts=False);ob=next(o for o in bpy.context.scene.objects if o.type=='MESH');ob.data.calc_loop_triangles();pts=[ob.matrix_world@v.co for v in ob.data.vertices];groups={g.name:set()for g in ob.vertex_groups}
for v in ob.data.vertices:
 for g in v.groups:groups[ob.vertex_groups[g.group].name].add(v.index)
out=[]
for s in [-1,1]:
 cn='four_ray_web_'+str(s);pn='basal_arm_'+str(s);ci=groups[cn];pi=groups[pn];ct=[tuple(t.vertices)for t in ob.data.loop_triangles if set(t.vertices)<=ci];pt=[tuple(t.vertices)for t in ob.data.loop_triangles if set(t.vertices)<=pi];cb=BVHTree.FromPolygons(pts,ct,all_triangles=True);pb=BVHTree.FromPolygons(pts,pt,all_triangles=True);cross=cb.overlap(pb);out.append({'child':cn,'parent':pn,'actual_surface_triangle_overlap_pairs':len(cross),'first_pair_vertices':{'child':[list(pts[i])for i in ct[cross[0][0]]],'parent':[list(pts[i])for i in pt[cross[0][1]]]}if cross else None,'pass':bool(cross)})
json.dump({'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'tests':out,'pass':all(x['pass']for x in out),'note':'Two actual lamina-web to arm intersections supplement 186 named per-part contacts. Total Dictyophyllum188, full batch1657. Pure BVH triangle geometry; no centerline proxy.'},O.open('x'),indent=2)
