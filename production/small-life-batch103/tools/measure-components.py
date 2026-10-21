#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""True transformed geometry, surface intersection, shared topology, dense global visibility."""
import argparse,datetime,hashlib,json,sys,collections,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--brief',required=True);p.add_argument('--output',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.source);bpy.ops.wm.open_mainfile(filepath=str(src));ct=json.loads(bpy.data.texts['BATCH103_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];bpy.context.view_layer.update();vs=[o.matrix_world@v.co for v in o.data.vertices];o.data.calc_loop_triangles();tris=[tuple(t.vertices) for t in o.data.loop_triangles];comps=ct['components'];lookup={c['tag']:c for c in comps};extent=max(max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3));eps=extent*1e-8;faces={};trees={};records=[];errors=[]
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
counts=collections.Counter(c['kind'] for c in comps)
expected={'habelia':{'trunk_tergite':12,'walking_leg':10,'posterior_exopod':14,'gnathobase':10,'cephalic_raptorial':10,'cephalic_exopod':10,'head_walking_leg':2,'reduced_anterior_appendage':2,'telson_proximal':1,'telson_distal':1,'head_tubercle':18},'alalcomenaeus':{'trunk_tergite':11,'walking_leg':22,'head_walking_leg':4,'great_appendage_peduncle':2,'great_appendage_claw':6,'great_appendage_flagellum':6,'lateral_eye':2,'median_eye':2,'spatulate_telson':1,'telson_spine':9},'plenocaris':{'carapace_valve':2,'abdominal_segment':13,'anterior_leg':6,'antenna':2,'antenna_spine':20,'caudal_ramulus':2},'nectocaris':{'trunk':1,'lateral_fin':2,'lateral_eye':2,'antenna':2,'flared_tubular_mouth':1}}[brief['asset_id']]
for k,n in expected.items():
 ok=counts[k]==n;extra.append({'kind':k,'required_count':n,'actual_nonempty_components':counts[k],'pass':ok})
 if not ok:errors.append('count:'+k)
size=[max(v[k] for v in vs)-min(v[k] for v in vs) for k in range(3)]
maximum={'alalcomenaeus':.060,'plenocaris':.017,'nectocaris':.072}.get(brief['asset_id'])
if maximum:
 ok=max(size)<=maximum;extra.append({'maximum_observed_size_m':maximum,'actual_total_largest_span_m':max(size),'pass':ok})
 if not ok:errors.append('maximum_size')
if brief['asset_id']=='habelia':
 rr=[r for r in records if r['kind'] in ['head_shield','trunk_tergite']];body=max(r['world_aabb_m']['max'][1] for r in rr)-min(r['world_aabb_m']['min'][1] for r in rr);telson=[r for r in records if r['kind'] in ['telson_proximal','telson_distal']];length=max(r['world_aabb_m']['max'][1] for r in telson)-min(r['world_aabb_m']['min'][1] for r in telson);extra.append({'actual_head_plus_trunk_m':body,'hard_range_m':[.0085,.034],'actual_telson_span_m':length,'telson_to_body_ratio':length/body,'qualitative_requirement':'subequal or slightly longer; inspect actual values, no invented tolerance'})
 if not .0085<=body<=.034:errors.append('habelia_body_length')
# Read-only audit of original component faces: no welding or normal recalculation.
topology=[]
for c in comps:
 fs=faces[c['tag']];ed=collections.defaultdict(list)
 for tri in fs:
  for aa,bb in zip(tri,tri[1:]+tri[:1]):ed[tuple(sorted((aa,bb)))].append(1 if aa<bb else -1)
 boundary=sum(len(x)==1 for x in ed.values());nonmanifold=sum(len(x)>2 for x in ed.values());same=sum(len(x)==2 and x[0]==x[1] for x in ed.values());volume=sum(vs[t[0]].dot(vs[t[1]].cross(vs[t[2]]))/6 for t in fs);ok=not(boundary or nonmanifold or same) and volume>0
 topology.append({'tag':c['tag'],'triangles':len(fs),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'same_direction_edges':same,'signed_volume_m3':volume,'original_closed_outward':ok})
 if not ok:errors.append('original_topology:'+c['tag'])
report={'schema_version':1,'status':'pass' if not errors else 'fail','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'brief_sha256':hashlib.sha256(Path(a.brief).read_bytes()).hexdigest(),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_reopened':True,'pid':__import__('os').getpid(),'object_matrix_world':[list(r) for r in o.matrix_world],'component_count':len(comps),'component_kind_counts':dict(collections.Counter(c['kind'] for c in comps)),'components':records,'contact_checks':contacts,'hard_range_checks':ranges,'additional_source_checks':extra,'original_component_topology':topology,'global_exposure':expo,'global_exposure_method':'Seven barycentric surface points per actual triangle plus vertices; rays in8 directions against all other relevant triangles. Shared tissue regions use unique source triangles. No arbitrary percentage acceptance threshold; small exposure still requires exact pixel readability.','numerical_ray_origin_epsilon_m':eps,'errors':errors,'limitations':'Surface intersection and sampled ray exposure are diagnostics, not independent approval. Required detail pixels and all eight actual final views must still be inspected.'};Path(a.output).open('x').write(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'counts':report['component_kind_counts'],'errors':errors,'lowest_exposure':sorted([(x['visible_fraction'],x['tag']) for x in expo])[:8]}))
