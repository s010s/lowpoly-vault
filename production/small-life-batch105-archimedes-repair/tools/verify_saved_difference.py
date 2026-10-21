#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fresh reopen of both saved sources; exact non-endpoint identity and genus audit."""
import bpy,json,hashlib,datetime,os,collections
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[3];D=R/'production/small-life-batch105-archimedes-repair/r002';O=R/'production/small-life-batch105/archimedes/r001';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();oldfile=O/'artifacts/archimedes.blend';newfile=D/'artifacts/archimedes.blend';pins=[sha(oldfile),sha(newfile)]
def read(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ct=json.loads(bpy.data.texts['BATCH105_COMPONENT_CONTRACT.json'].as_string());ob=bpy.data.objects[ct['object_name']];return {'vertices':[tuple(v.co) for v in ob.data.vertices],'faces':[tuple(p.vertices) for p in ob.data.polygons],'materials':[p.material_index for p in ob.data.polygons],'matrix':[list(r) for r in ob.matrix_world],'contract':ct}
a=read(oldfile);b=read(newfile);diff=[i for i,(x,y) in enumerate(zip(a['vertices'],b['vertices'])) if x!=y];assert len(diff)==65
for k in ['faces','materials','matrix','contract']:assert a[k]==b[k]
expected=json.loads((D/'qa/geometry-identity.json').read_text());assert diff==expected['modified_vertices'];frond=next(c for c in b['contract']['components'] if c['kind']=='perforated_frond');ids=set(frond['vertices']);assert not ids.intersection(diff);fs=[f for f in b['faces'] if set(f)<=ids];edges={tuple(sorted((x,y))) for f in fs for x,y in zip(f,f[1:]+f[:1])};chi=len(ids)-len(edges)+len(fs);assert chi==-598;g=(2-chi)//2;assert g==300
rings=[]
for row in expected['endpoint_ring_measurements']:
 ring=row['vertices'];ps=[Vector(b['vertices'][i]) for i in ring];ctr=sum(ps,Vector())/len(ps);rr=[(v-ctr).length for v in ps];rings.append({'ring_index':row['ring_index'],'source_vertex_count':len(ps),'radius_m_min':min(rr),'radius_m_max':max(rr),'center_m':list(ctr)})
assert [sha(oldfile),sha(newfile)]==pins
r={'schema_version':1,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender_pid':os.getpid(),'original_source_sha256':pins[0],'new_source_sha256':pins[1],'saved_sources_reopened':True,'source_or_geometry_modified':False,'changed_vertices':diff,'all_other_vertices_bitwise_equal':True,'all_faces_material_indices_transforms_semantic_contract_equal':True,'original_frond_vertices_and_faces_bitwise_equal':True,'actual_frond_topology':{'V':len(ids),'E':len(edges),'F':len(fs),'euler_characteristic':chi,'closed_orientable_genus':g,'note':'Original source winding test separately establishes closed outward surface. Genus300 plus exact frond identity corroborates300 actual through openings, not painted pores.'},'actual_saved_terminal_rings':rings,'status':'pass','note':'Numerics document the actual tapered ends; visual judgment remains based on original criterion and exact detail images, not a new taper ratio threshold.'};(D/'qa/saved-source-difference.report.json').write_text(json.dumps(r,indent=2)+'\n');print('SAVED_SOURCE_DIFFERENCE_PASS',len(diff),'changed vertices; genus',g)
