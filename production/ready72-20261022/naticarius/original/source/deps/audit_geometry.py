# SPDX-License-Identifier: MIT
"""Read-only source geometry and exact artifact feature probes, not visual approval."""
import bpy,bmesh,sys,argparse,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--blend',required=True);p.add_argument('--glb',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=a.blend);C=bpy.data.collections['EXPORT'];parts=[];errors=[];allv=[]
for ob in C.all_objects:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data);volume=bm.calc_volume(signed=True)
 rec={'name':ob.name,'vertices':len(bm.verts),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':volume,'normal_winding':'positive_outward' if volume>0 else 'nonpositive','minimum_face_area_m2':min(f.calc_area() for f in bm.faces),'smooth_shading':'intentional for naturally smooth fossil shell'}
 if rec['nonmanifold_edges']:errors.append(ob.name+': nonmanifold source')
 if volume<=0:errors.append(ob.name+': nonpositive winding')
 bm.free();parts.append(rec);allv += [ob.matrix_world@v.co for v in ob.data.vertices]
body=bpy.data.objects['inflated-body-open-aperture-continuous-lining'];mesh=body.data;mesh.calc_loop_triangles();verts=[body.matrix_world@v.co for v in mesh.vertices];bvh=BVHTree.FromPolygons(verts,[t.vertices[:] for t in mesh.loop_triangles],all_triangles=True)
probes={}
for name,x,z in [('aperture-center',.0045,.0115),('closed-body-left',-.010,.0115),('umbilical-recess',-.0025,.0160),('columellar-shoulder',-.001,.0190)]:
 loc,normal,index,distance=bvh.ray_cast(Vector((x,-.05,z)),Vector((0,1,0)),.1)
 probes[name]={'origin_m':[x,-.05,z],'direction':[0,1,0],'hit_position_m':list(loc) if loc else None,'hit_normal':list(normal) if normal else None,'distance_m':distance,'triangle_index':index}
ys=[v.y for v in verts];front=min(ys);ap=probes['aperture-center']['hit_position_m'];depth=ap[1]-front if ap else None
if depth is None or depth<.006:errors.append('Aperture center is not recessed at least 6mm beyond the front lip plane')
report={'status':'PASS' if not errors else 'FAIL','scope':'Source closed-surface topology, positive aggregate winding and sampled real cavity depth. Not self-intersection union certification, scientific correctness or independent visual acceptance.','source_blend_sha256':hashlib.sha256(Path(a.blend).read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(Path(a.glb).read_bytes()).hexdigest(),'parts':parts,'probes':probes,'aperture_sample_recession_from_front_m':depth,'contains_preview_stage':any(o.type in ['CAMERA','LIGHT'] for o in bpy.context.scene.objects),'source_units':'meters','intentional_intersections':'Closed spire base embedded in body whorl. Distinct semantic meshes, not print-ready boolean union.','errors':errors}
if report['contains_preview_stage']:errors.append('Source contains preview camera/light')
Path(a.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if errors:raise RuntimeError('; '.join(errors))
