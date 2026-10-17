#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only GLB byte accounting and in-memory precision estimates.
Never writes or mutates a candidate GLB; output reports go beside this script.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,math,struct,sys
P=Path(__file__).resolve().parent;ROOT=P.parent
REPO=next(x for x in P.parents if (x/'scripts/qa_glb.py').exists());sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import read_glb,accessor_values
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def quant_errors(normals,bits):
 maximum=2**(bits-1)-1;angles=[];length_errors=[]
 for n in normals:
  q=[round(x*maximum)/maximum for x in n];a=math.sqrt(sum(x*x for x in n));b=math.sqrt(sum(x*x for x in q));dot=sum(x*y for x,y in zip(n,q))/(a*b)
  angles.append(math.degrees(math.acos(max(-1,min(1,dot)))));length_errors.append(abs(b-1))
 angles.sort();return {'max_angle_deg':max(angles),'mean_angle_deg':sum(angles)/len(angles),'p99_angle_deg':angles[min(len(angles)-1,int(len(angles)*.99))],'max_decoded_unit_length_error':max(length_errors)}

def one(rev):
 p=ROOT/f'candidate-r{rev}';path=p/'conifer-tree.glb';doc,binary,raw=read_glb(path);before=H(path);meta=json.loads((p/'metadata.json').read_text());json_size=struct.unpack_from('<I',raw,12)[0]
 total={'POSITION':0,'NORMAL':0,'indices':0};parts=[];all_normals=[];all_keys=[]
 for mesh in doc['meshes']:
  for prim in mesh['primitives']:
   attributes=prim['attributes'];positions=accessor_values(doc,binary,attributes['POSITION']);normals=accessor_values(doc,binary,attributes['NORMAL']);indices=accessor_values(doc,binary,prim['indices']);keys=list(zip(positions,normals));ia=doc['accessors'][prim['indices']];index_bytes=len(indices)*{5121:1,5123:2,5125:4}[ia['componentType']]
   count=len(positions);total['POSITION']+=count*12;total['NORMAL']+=count*12;total['indices']+=index_bytes;all_normals.extend(normals);all_keys.extend(keys)
   parts.append({'mesh':mesh['name'],'material':doc['materials'][prim['material']]['name'],'vertices':count,'triangles':len(indices)//3,'attributes':list(attributes),'index_component_type':ia['componentType'],'position_bytes':count*12,'normal_bytes':count*12,'index_bytes':index_bytes,'unique_positions':len(set(positions)),'unique_position_normal_tuples':len(set(keys)),'duplicate_full_vertices':count-len(set(keys)),'unused_vertices':count-len({x[0] for x in indices}),'unique_normals':len(set(normals))})
 vertices=len(all_normals);source=meta['authored_source_vertices'];view_bytes=sum(x['byteLength'] for x in doc['bufferViews']);accounted=sum(total.values())
 result={'revision':rev,'sha256':before,'bytes':len(raw),'json_chunk_bytes':json_size,'container_header_bytes':28,'bin_bytes':len(binary),'buffer_view_bytes':view_bytes,'bin_padding_or_unreferenced_bytes':len(binary)-view_bytes,'attribute_or_index_bytes':total,'percent_of_total':{k:100*v/len(raw) for k,v in total.items()},'source_vertices':source,'export_vertices':vertices,'vertex_split_increment':vertices-source,'vertex_split_attribute_bytes':(vertices-source)*24,'triangles':sum(x['triangles'] for x in parts),'primitives':len(parts),'materials':len(doc['materials']),'images':len(doc.get('images',[])),'attributes':[x for x in sorted({k for mesh in doc['meshes'] for prim in mesh['primitives'] for k in prim['attributes']})],'duplicate_full_vertices_across_all_primitives':len(all_keys)-len(set(all_keys)),'unique_normals':len(set(all_normals)),'parts':parts}
 assert accounted==view_bytes and len(raw)==28+json_size+len(binary)
 if rev==19:
  result['normal_storage_estimates']={}
  for bits,stride in [(16,8),(8,4)]:
   saved=vertices*(12-stride);result['normal_storage_estimates'][str(bits)]={'vertex_stride_bytes':stride,'normal_payload_bytes':vertices*stride,'exact_payload_saving_bytes':saved,'file_estimate_before_small_schema_overhead':len(raw)-saved,'geometry_positions_changed':False,'precision':quant_errors(all_normals,bits)}
  def clean(x):
   if isinstance(x,dict):return {k:clean(v) for k,v in x.items() if k not in ['name','extras']}
   if isinstance(x,list):return [clean(y) for y in x]
   return x
  stripped=json.dumps(clean(doc),separators=(',',':'),ensure_ascii=False).encode();padded=(len(stripped)+3)//4*4
  result['all_name_extras_stripping_saving_upper_bound']=json_size-padded
  bounds=json.loads((p/'qa.json').read_text())['glb']['bounds_m'];maximum_extent=max(bounds['size'])
  result['position_quant16_optional_only']={'uniform_range_m':maximum_extent,'maximum_per_component_rounding_error_m':maximum_extent/(65535*2),'maximum_3d_rounding_error_m':maximum_extent/(65535*2)*math.sqrt(3),'saving_bytes_at_stride8':vertices*4,'warning':'Changes positions numerically; not a lossless or current recommendation.'}
 assert H(path)==before
 return result

rows=[one(x) for x in [12,15,19]]
for prior in rows[:2]:
 last=rows[2];last.setdefault('deltas',{})[str(prior['revision'])]={'bytes':last['bytes']-prior['bytes'],'source_vertex_attribute_delta':(last['source_vertices']-prior['source_vertices'])*24,'split_vertex_attribute_delta':(last['vertex_split_increment']-prior['vertex_split_increment'])*24,'index_delta':last['attribute_or_index_bytes']['indices']-prior['attribute_or_index_bytes']['indices'],'json_container_delta':last['json_chunk_bytes']-prior['json_chunk_bytes']}
output={'method':'Exact read-only accessor/buffer accounting; no candidate mutation. Normal quantization is simulated in memory, not yet an optimized artifact or rendering claim.','rows':rows}
(P/'byte-accounting.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps([{k:v for k,v in row.items() if k not in ['parts']} for row in rows],indent=2))
