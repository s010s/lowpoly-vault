#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reopen actual source; world-space organ bounds, BVH junction and exposure proof."""
import argparse,datetime,hashlib,json,sys,collections
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--brief',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source);bpy.ops.wm.open_mainfile(filepath=str(src));contract=json.loads(bpy.data.texts['BATCH99_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[contract['object_name']];bpy.context.view_layer.update();v=[o.matrix_world@x.co for x in o.data.vertices];o.data.calc_loop_triangles();tri=[tuple(t.vertices) for t in o.data.loop_triangles];components=contract['components'];lookup={c['tag']:c for c in components};trees={};counts=collections.Counter();records=[];contacts=[];errors=[]
for c in components:
 ids=set(c['vertices']);faces=[t for t in tri if all(i in ids for i in t)];trees[c['tag']]=BVHTree.FromPolygons(v,faces,all_triangles=True);points=[v[i] for i in c['vertices']];sizes=[]
 for axis in c['axes']:
  d=o.matrix_world.to_3x3()@Vector(axis);d.normalize();z=[x.dot(d) for x in points];sizes.append(max(z)-min(z))
 rec=dict(tag=c['tag'],kind=c['kind'],vertices=len(points),triangles=len(faces),world_aabb_m={'min':[min(x[k] for x in points) for k in range(3)],'max':[max(x[k] for x in points) for k in range(3)]},oriented_length_m=sizes[0],oriented_width_m=sizes[1],oriented_thickness_m=sizes[2],length_width_ratio=sizes[0]/sizes[1] if sizes[1] else None,design=c['design']);records.append(rec);counts[c['kind']]+=1
brief=json.loads(Path(a.brief).read_text());rangechecks=[]
for rule in brief['hard_organ_ranges']:
 subset=[r for r in records if r['kind']==rule['kind']];lo,hi=rule['range'];fail=[r['tag'] for r in subset if not lo-1e-7<=r[rule['measure']]<=hi+1e-7];rangechecks.append(dict(rule=rule,observed_min=min(r[rule['measure']] for r in subset),observed_max=max(r[rule['measure']] for r in subset),count=len(subset),failures=fail));errors.extend('range:'+x for x in fail)
for c in components:
 if not c['parent']:continue
 if c['parent'] not in trees:errors.append('missing parent:'+c['tag']);continue
 tree=trees[c['parent']]
 def signed(idx):
  q,n,face,dist=tree.find_nearest(v[idx]);return (v[idx]-q).dot(n)
 ds=[signed(i) for i in c['base_vertices']];all_ds=[signed(i) for i in c['vertices']];embedded=bool(ds) and min(ds)<=1e-7;exposed=max(all_ds)>1e-7;rec=dict(child=c['tag'],parent=c['parent'],actual_base_vertices=c['base_vertices'],signed_base_surface_distances_m=ds,min_signed_base_distance_m=min(ds) if ds else None,base_intersects_parent=embedded,max_signed_component_distance_m=max(all_ds),exposed_vertex_count=sum(x>1e-7 for x in all_ds),component_vertex_count=len(all_ds),has_exposed_geometry=exposed,method='Actual reopened transformed mesh vertices; nearest parent triangle BVH outward normal signed distance. Negative is inside. Tangent <=1e-7m numerical tolerance. Not AABB/config point proof.');contacts.append(rec)
 if not embedded:errors.append('detached:'+c['tag'])
 if not exposed:errors.append('fully buried:'+c['tag'])
report=dict(schema_version=1,status='pass' if not errors else 'fail',source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),brief_sha256=hashlib.sha256(Path(a.brief).read_bytes()).hexdigest(),created_at_executor_clock=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_reopened=True,object_matrix_world=[list(row) for row in o.matrix_world],translation_only=contract['translation'],component_count=len(components),component_kind_counts=dict(counts),components=records,hard_range_checks=rangechecks,contact_checks=contacts,errors=errors,limitations='BVH signed nearest-normal test is local junction/exposure evidence, not complete interpenetration/visual acceptance. Actual signed distances may be zero at capped surface; exact render views remain required.')
Path(a.output).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'components':len(components),'errors':errors}))
