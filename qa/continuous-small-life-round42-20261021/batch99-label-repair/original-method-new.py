import sys;sys.dont_write_bytecode=True
import sys,pathlib,json,collections,math,hashlib
W=pathlib.Path('/workspace/shared/lowpoly-batch99-label-repair-20261021');Q=pathlib.Path('/workspace/shared/lowpoly-batch99-label-independent-qa-20261021/original-method-new');sys.path.insert(0,str(W/'scripts'));from qa_glb import read_glb,accessor_values
for a,r in [('monetianthus','r002'),('proterocladus','r003')]:
 geo=json.loads((pathlib.Path('/workspace/shared/lowpoly-batch99-independent-qa-20261021')/(a+'-geometry.json')).read_text());label=next(c for c in geo['components'] if c['tag']=='enlarged_label');lo=label['bounds_world_m']['min'];hi=label['bounds_world_m']['max'];src=W/'production/small-life-batch99'/a/r/'artifacts'/(a+'.glb');doc,bin,raw=read_glb(src);ts=[];ix=[];edge=collections.defaultdict(list);caps=collections.Counter();vol=0
 for pi,p in enumerate(doc['meshes'][0]['primitives']):
  pos=accessor_values(doc,bin,p['attributes']['POSITION']);ids=[x[0] for x in accessor_values(doc,bin,p['indices'])]
  for off in range(0,len(ids),3):
   t=[pos[i] for i in ids[off:off+3]];bl=[(v[0],-v[2],v[1]) for v in t]
   if all(all(lo[k]-1e-8<=v[k]<=hi[k]+1e-8 for k in range(3)) for v in bl):
    ts.append(t);ix.append([pi,off//3]);
    for x,y in zip(t,t[1:]+t[:1]):edge[tuple(sorted((x,y)))].append((x,y,len(ts)-1))
    u=[t[1][k]-t[0][k] for k in range(3)];v=[t[2][k]-t[0][k] for k in range(3)];n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);
    if max(p[2] for p in t)-min(p[2] for p in t)<1e-9:
     side='front' if abs(t[0][2]+lo[1])<1e-8 else 'back';caps[side+('_outward' if (n[2]>0)==(side=='front') else '_inward')]+=1
    vol+=sum(t[0][k]*n[k] for k in range(3))/6
 assert len(ts)==label['triangles'],(a,len(ts),label['triangles'])
 unpaired=[{'edge':k,'uses':len(v)} for k,v in edge.items() if len(v)!=2];bad=[{'edge':k,'triangles':[ix[x[2]] for x in v]} for k,v in edge.items() if len(v)==2 and v[0][:2]!=tuple(reversed(v[1][:2]))]
 report={'asset_id':a,'glb_sha256':hashlib.sha256(raw).hexdigest(),'method':'Direct decode unchanged final GLB primitive indices and float positions; isolate exact label world AABB and require source label triangle count match; compare original directed coordinate edges. No welding, normal recalc, reexport or mesh edits.','label_triangle_count':len(ts),'source_label_triangle_count':label['triangles'],'unpaired_coordinate_edges':unpaired,'same_direction_shared_coordinate_edges':bad,'original_cap_winding':dict(caps),'signed_triangle_integral_m3_not_closed_volume':vol,'materials_double_sided':any(m.get('doubleSided',False) for m in doc['materials']),'source_mutated':False};(Q/(a+'-glb-label-orientation.json')).write_text(json.dumps(report,indent=2)+'\n');print(a,len(ts),'unpaired',len(unpaired),'same direction',len(bad),'cap',dict(caps),'vol',vol)
