#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""NORMAL storage-only precision variant. No position/topology/material edits.
Requires KHR_mesh_quantization, handled by pinned GLTFLoader without a decoder.
Does not claim mathematical losslessness or independent visual approval.
"""
from pathlib import Path
import argparse,copy,hashlib,json,math,struct,sys
REPO=next(x for x in Path(__file__).resolve().parents if (x/'scripts/qa_glb.py').exists());sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import read_glb,accessor_values,audit_glb
H=lambda data:hashlib.sha256(data).hexdigest()
def pack(source,destination,report_path=None):
 source=Path(source);destination=Path(destination)
 if destination.exists():raise RuntimeError('Never overwrite an existing candidate GLB')
 doc,oldbin,raw=read_glb(source);out=copy.deepcopy(doc);normal_accessors={p['attributes']['NORMAL'] for m in doc['meshes'] for p in m['primitives']};normal_views={doc['accessors'][i]['bufferView']:i for i in normal_accessors}
 assert len(normal_views)==len(normal_accessors)
 buffer=bytearray();angles=[];length_errors=[]
 for index,view in enumerate(doc['bufferViews']):
  while len(buffer)%4:buffer.append(0)
  new_view=out['bufferViews'][index];new_view['byteOffset']=len(buffer)
  if index in normal_views:
   ai=normal_views[index];a=doc['accessors'][ai];assert a['componentType']==5126 and a['type']=='VEC3' and a.get('byteOffset',0)==0
   assert sum(1 for x in doc['accessors'] if x.get('bufferView')==index)==1
   values=accessor_values(doc,oldbin,ai)
   for n in values:
    q=tuple(max(-32767,min(32767,round(x*32767))) for x in n);buffer.extend(struct.pack('<hhhxx',*q));decoded=[x/32767 for x in q];length=math.sqrt(sum(x*x for x in decoded));original_length=math.sqrt(sum(x*x for x in n));cosine=sum(x*y for x,y in zip(n,decoded))/(length*original_length);angles.append(math.degrees(math.acos(max(-1,min(1,cosine)))));length_errors.append(abs(length-1))
   out['accessors'][ai]['componentType']=5122;out['accessors'][ai]['normalized']=True
   for bound,fn in [('min',min),('max',max)]:
    if bound in a:out['accessors'][ai][bound]=[fn(max(-32767,min(32767,round(row[k]*32767))) for row in values) for k in range(3)]
   new_view['byteStride']=8;new_view['byteLength']=len(values)*8
  else:
   begin=view.get('byteOffset',0);buffer.extend(oldbin[begin:begin+view['byteLength']]);new_view['byteLength']=view['byteLength']
 while len(buffer)%4:buffer.append(0)
 out['buffers'][0]['byteLength']=len(buffer)
 for field in ['extensionsUsed','extensionsRequired']:
  if 'KHR_mesh_quantization' not in out.setdefault(field,[]):out[field].append('KHR_mesh_quantization')
 encoded=json.dumps(out,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode();encoded+=b' '*((-len(encoded))%4)
 newraw=struct.pack('<4sII',b'glTF',2,28+len(encoded)+len(buffer))+struct.pack('<II',len(encoded),0x4e4f534a)+encoded+struct.pack('<II',len(buffer),0x004e4942)+buffer
 destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(newraw)
 newdoc,newbin,check=read_glb(destination);same_positions=True;same_indices=True
 for mi,mesh in enumerate(doc['meshes']):
  for pi,primitive in enumerate(mesh['primitives']):
   other=newdoc['meshes'][mi]['primitives'][pi];same_positions&=accessor_values(doc,oldbin,primitive['attributes']['POSITION'])==accessor_values(newdoc,newbin,other['attributes']['POSITION']);same_indices&=accessor_values(doc,oldbin,primitive['indices'])==accessor_values(newdoc,newbin,other['indices'])
 same_materials=doc['materials']==newdoc['materials'];same_nodes=doc.get('nodes')==newdoc.get('nodes') and doc.get('scenes')==newdoc.get('scenes');assert same_positions and same_indices and same_materials and same_nodes
 angles.sort();report={'check':'normal16_geometry_equivalence','status':'pass','source_glb_sha256':H(raw),'packed_glb_sha256':H(check),'source_bytes':len(raw),'packed_bytes':len(check),'saved_bytes':len(raw)-len(check),'saved_percent':100*(len(raw)-len(check))/len(raw),'positions_exact':same_positions,'indices_and_triangle_order_exact':same_indices,'materials_exact':same_materials,'nodes_and_scene_transforms_exact':same_nodes,'primitive_count':sum(len(x['primitives']) for x in doc['meshes']),'normal_values_changed':True,'mathematically_lossless':False,'normal_max_angular_error_deg':max(angles),'normal_mean_angular_error_deg':sum(angles)/len(angles),'normal_p99_angular_error_deg':angles[int(len(angles)*.99)],'normal_max_length_error':max(length_errors),'format':'KHR_mesh_quantization, normalized SHORT normals,8-byte stride; FLOAT32 positions unchanged','decoder_dependency':'No external decoder. Needs target loader support for the required extension; actual GPU evidence still required.','limitations':'Exact shape/topology/material/transform comparison and measured normal precision; not independent art approval or a GPU benchmark.'}
 if report_path:Path(report_path).write_text(json.dumps(report,indent=2)+'\n')
 assert source.read_bytes()==raw
 return report
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('source',type=Path);parser.add_argument('destination',type=Path);parser.add_argument('--report',type=Path);args=parser.parse_args();print(json.dumps(pack(args.source,args.destination,args.report),indent=2))
