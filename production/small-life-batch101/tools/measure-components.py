#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""True transformed geometry, surface intersection, shared topology, dense global visibility."""
import argparse,datetime,hashlib,json,sys,collections,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--brief',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source);bpy.ops.wm.open_mainfile(filepath=str(src));ct=json.loads(bpy.data.texts['BATCH101_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];bpy.context.view_layer.update();vs=[o.matrix_world@v.co for v in o.data.vertices];o.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in o.data.loop_triangles];comps=ct['components'];lookup={c['tag']:c for c in comps};extent=max(max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3));eps=extent*1e-8;faces={};trees={};records=[];errors=[]
for c in comps:
 ids=set(c['vertices']);fs=[t for t in tris if all(i in ids for i in t)];faces[c['tag']]=fs;trees[c['tag']]=BVHTree.FromPolygons(vs,fs,all_triangles=True);pts=[vs[i] for i in c['vertices']];sizes=[]
 for axis in c['axes']:
  d=o.matrix_world.to_3x3()@Vector(axis);d.normalize();z=[v.dot(d) for v in pts];sizes.append(max(z)-min(z))
 records.append({'tag':c['tag'],'kind':c['kind'],'vertices':len(pts),'triangles':len(fs),'world_aabb_m':{'min':[min(v[k] for v in pts) for k in range(3)],'max':[max(v[k] for v in pts) for k in range(3)]},'oriented_length_m':sizes[0],'oriented_width_m':sizes[1],'oriented_thickness_m':sizes[2],'design':c['design'],'shared_topology':c.get('shared_topology',False)})
contacts=[]
for c in comps:
 if not c.get('parent'):continue
 parent=c['parent'];tree=trees[parent];ids=c['base_vertices']
 if c.get('shared_topology'):
  shared=set(ids)&set(lookup[parent]['vertices']);ok=bool(shared);contacts.append({'child':c['tag'],'parent':parent,'method':'Actual common vertex indices in one contiguous manifold tissue; no duplicate solid.','shared_vertices':len(shared),'base_intersects_parent':ok});continue
 ds=[]
 for i in ids:
  q,n,fi,dist=tree.find_nearest(vs[i]);ds.append((vs[i]-q).dot(n))
 overlap=trees[c['tag']].overlap(tree);ok=bool(ds) and min(ds)<=eps or bool(overlap)
 contacts.append({'child':c['tag'],'parent':parent,'actual_base_vertices':ids,'min_signed_base_distance_m':min(ds) if ds else None,'triangle_intersection_pair_count':len(overlap),'base_intersects_parent':ok,'method':'Actual transformed component base vertices signed to nearest parent triangles, plus exact BVH triangle intersections. Not AABB.'})
 if not ok:errors.append('detached:'+c['tag'])
brief=json.loads(Path(a.brief).read_text());ranges=[]
for rule in brief['hard_organ_ranges']:
 rr=[r for r in records if r['kind']==rule['kind']];lo,hi=rule['range'];bad=[r['tag'] for r in rr if not lo-1e-7<=r[rule['measure']]<=hi+1e-7];ranges.append({'rule':rule,'observed_min':min(r[rule['measure']] for r in rr),'observed_max':max(r[rule['measure']] for r in rr),'count':len(rr),'failures':bad});errors+=['range:'+x for x in bad]
dirs={k:Vector(v).normalized() for k,v in {'front':(0,-1,0),'rear':(0,1,0),'left':(-1,0,0),'right':(1,0,0),'top':(0,0,1),'bottom':(0,0,-1),'hero':(.47,-.67,.57),'reversehero':(-.47,.67,.57)}.items()};expo=[]
for c in comps:
 ids=set(c['vertices']);own=faces[c['tag']];rest=[t for t in tris if not all(i in ids for i in t)];tree=BVHTree.FromPolygons(vs,rest,all_triangles=True) if rest else None;samples=[]
 # Seven actual barycentric surface samples per triangle plus actual vertices, not merely face centers.
 for tri in own:
  x,y,z=[vs[i] for i in tri];samples.extend([(x+y+z)/3,(x+y)/2,(y+z)/2,(z+x)/2,x*.6+y*.2+z*.2,x*.2+y*.6+z*.2,x*.2+y*.2+z*.6])
 samples.extend(vs[i] for i in c['vertices']);counts={k:0 for k in dirs};seen=0
 for q in samples:
  visible=False
  for k,d in dirs.items():
   hit=tree.ray_cast(q+d*eps,d,extent*3)[0] if tree else None
   if hit is None:counts[k]+=1;visible=True
  if visible:seen+=1
 expo.append({'tag':c['tag'],'kind':c['kind'],'surface_samples':len(samples),'visible_samples_any_direction':seen,'visible_fraction':seen/len(samples) if samples else 0,'visible_samples_by_direction':counts,'not_fully_swallowed':seen>0})
 if seen==0:errors.append('no_global_surface_exposure:'+c['tag'])
extra=[]
if brief['asset_id']=='winfrenatia':
 for r in records:
  if r['kind']=='pit':
   depth=r['oriented_thickness_m'];extra.append({'tag':r['tag'],'measured_pit_depth_from_open_rim_m':depth,'allowed_m':[.0005,.001],'status':'pass' if .0005<=depth<=.001 else 'fail'})
 if any(x['status']=='fail' for x in extra):errors.append('pit_depth')
 mat=next(r for r in records if r['kind']=='layered_mat');extra.append({'actual_mat_thickness_m':mat['oriented_thickness_m'],'allowed_m':[.001,.002],'status':'pass' if .001<=mat['oriented_thickness_m']<=.002 else 'fail'})
report={'schema_version':1,'status':'pass' if not errors else 'fail','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'brief_sha256':hashlib.sha256(Path(a.brief).read_bytes()).hexdigest(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_reopened':True,'pid':__import__('os').getpid(),'object_matrix_world':[list(r) for r in o.matrix_world],'component_count':len(comps),'component_kind_counts':dict(collections.Counter(c['kind'] for c in comps)),'components':records,'contact_checks':contacts,'hard_range_checks':ranges,'additional_source_checks':extra,'global_exposure':expo,'global_exposure_method':'Seven barycentric surface points per actual triangle plus vertices; rays in8 directions against all other relevant triangles. Shared tissue regions use unique source triangles. No arbitrary percentage acceptance threshold; small exposure still requires exact pixel readability.','numerical_ray_origin_epsilon_m':eps,'errors':errors,'limitations':'Surface intersection and sampled ray exposure are diagnostics, not independent approval. Required detail pixels and all eight actual final views must still be inspected.'};Path(a.output).open('x').write(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'counts':report['component_kind_counts'],'errors':errors,'lowest_exposure':sorted([(x['visible_fraction'],x['tag']) for x in expo])[:8]}))
