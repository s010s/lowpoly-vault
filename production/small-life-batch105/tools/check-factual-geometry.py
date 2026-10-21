#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only exact source dimensions, biological angles and geometric row locations."""
import json,sys,hashlib,datetime,math,collections
from pathlib import Path
import bpy
from mathutils import Vector
src=Path(sys.argv[sys.argv.index('--')+1]);dest=Path(sys.argv[sys.argv.index('--')+2]);aid=src.stem;bpy.ops.wm.open_mainfile(filepath=str(src));ct=json.loads(bpy.data.texts['BATCH105_COMPONENT_CONTRACT.json'].as_string());obj=bpy.data.objects[ct['object_name']];vs=[obj.matrix_world@v.co for v in obj.data.vertices];comps={c['tag']:c for c in ct['components']};reports=[];errors=[];directions={};roots={}
for c in comps.values():
 axis=Vector(c['axes'][0]);pts=[vs[i] for i in c['vertices']];projs=[v.dot(axis) for v in pts];lo=min(projs);hi=max(projs);near0=[v for v in pts if v.dot(axis)-lo<1e-9];near1=[v for v in pts if hi-v.dot(axis)<1e-9];b=sum(near0,Vector())/len(near0);e=sum(near1,Vector())/len(near1);directions[c['tag']]=(e-b).normalized();roots[c['tag']]=b
if aid=='penniretepora':
 for c in comps.values():
  if c['kind']!='lateral_branch':continue
  angle=math.degrees(math.acos(max(-1,min(1,directions[c['tag']].dot(directions['main_branch'])))));ok=59<=angle<=82;reports.append({'kind':'actual_lateral_angle_degrees','component':c['tag'],'actual':angle,'source_range':[59,82],'pass':ok})
  if not ok:errors.append('angle:'+c['tag'])
 for side in [-1,1]:
  positions=sorted(roots[f'lateral_{side}_{i}'].dot(directions['main_branch']) for i in range(8));sp=[y-x for x,y in zip(positions,positions[1:])];ok=all(.00059<=x<=.00085 for x in sp);reports.append({'kind':'same_rank_center_spacing_m','side':side,'actual':sp,'source_range':[.00059,.00085],'pass':ok})
  if not ok:errors.append('spacing:'+str(side))
if aid in ['penniretepora','cystodictya']:
 faces=collections.defaultdict(list)
 for f in ct['integrated_features']:
  if f['kind']!='recessed_aperture':continue
  c=comps[f['component']];w=Vector(c['axes'][1]);center=sum((vs[i] for i in f['vertices'][:8]),Vector())/8;faces[(f['component'],f['side'])].append(center.dot(w))
 for key,coords in faces.items():
  vals=sorted(coords);clusters=[]
  for x in vals:
   if not clusters or abs(x-clusters[-1][-1])>1e-8:clusters.append([x])
   else:clusters[-1].append(x)
  actual=[sum(x)/len(x) for x in clusters];expected=2 if aid=='penniretepora' else 5;ok=len(actual)==expected;reports.append({'kind':'actual_geometric_longitudinal_aperture_rows','component':key[0],'face':key[1],'observed_row_coordinate_m':actual,'required_count':expected,'pass':ok})
  if not ok:errors.append('row:'+str(key))
if aid=='archimedes':
 count=sum(f['kind']=='open_fenestrule' for f in ct['integrated_features']);reports.append({'kind':'actual_topological_fenestrules','count':count,'pass':count==300,'note':'300 authored independent open cells, not a biological observed count.'})
report={'schema_version':1,'asset_id':aid,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'status':'pass' if not errors else 'fail','checks':reports,'errors':errors,'source_not_modified':True,'method':'Actual transformed source vertices. Branch axes derived from endpoint-plane vertex centroids; aperture rows independently clustered by actual rim-centroid projections, not just metadata row labels.'};dest.open('x').write(json.dumps(report,indent=2)+'\n');print(aid,report['status'],errors)
