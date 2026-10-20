from pathlib import Path
import json,datetime,hashlib
R=Path.cwd();W=R/'production/continuous-small-life-round25-20261020/work/batch-65/breccia-repair-r003';B=R/'assets/candidates/continuous-small-life-round25-20261020/batch-65';a=B/'breccia-outcrop/r002';b=B/'breccia-outcrop/r003';P=W.parent
(b/'authoring-start.json').write_text(json.dumps({'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Observed immediately before revised generator authoring; follows repair freeze'})+'\n')
s=(a/'generator.py').read_text();old="""  vs=[tuple(c+u*x+v*y+normal*d) for d in [-depth*.65,depth*.35] for x,y in shape];fs=[tuple(range(count-1,-1,-1)),tuple(count+i for i in range(count))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)];part(name,vs,fs,mat)"""
assert old in s
s=s.replace(' def clast(name,c,u,v,depth,size,mat):',' records=[]\n def clast(name,c,u,v,depth,size,mat):')
s=s.replace(old,"""  records.append({'id':'clast-%03d'%len(records),'name':name,'center':c,'u':u,'v':v,'normal':normal,'depth':depth,'shape':[c+u*x+v*y for x,y in shape],'material':mat,'original_shape':[c+u*x+v*y for x,y in shape]})""")
insert='''
 # Actual coplanar overlap correction, only after original deterministic placements are collected.
 def signed_area(poly):return sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))/2 if len(poly)>2 else 0
 def polygon_overlap(A,B):
  u=A['u'];v=A['v'];o=A['center'];ap=[((p-o).dot(u),(p-o).dot(v)) for p in A['shape']];bp=[((p-o).dot(u),(p-o).dot(v)) for p in B['shape']];sign=1 if signed_area(bp)>0 else -1;q=ap
  for i,p in enumerate(bp):
   z=bp[(i+1)%len(bp)];out=[]
   if not q:break
   def value(x):return sign*((z[0]-p[0])*(x[1]-p[1])-(z[1]-p[1])*(x[0]-p[0]))
   for k,x in enumerate(q):
    y=q[(k+1)%len(q)];dx=value(x);dy=value(y);ix=dx>=-1e-12;iy=dy>=-1e-12
    if ix:out.append(x)
    if ix!=iy:
     t=dx/(dx-dy);out.append((x[0]+t*(y[0]-x[0]),x[1]+t*(y[1]-x[1])))
   q=out
  return abs(signed_area(q))
 def halfspace(poly,axis,mid,keep):
  out=[];margin=cfg['repair_parameters']['pair_boundary_margin_m']
  for i,p in enumerate(poly):
   q=poly[(i+1)%len(poly)];dp=keep*(p-mid).dot(axis)-margin;dq=keep*(q-mid).dot(axis)-margin;ip=dp>=0;iq=dq>=0
   if ip:out.append(p)
   if ip!=iq:
    t=dp/(dp-dq);out.append(p+(q-p)*t)
  return out
 corrections=[]
 for i,A in enumerate(records):
  for B in records[i+1:]:
   if len(A['shape'])<3 or len(B['shape'])<3:continue
   if abs(A['normal'].dot(B['normal']))<1-1e-6:continue
   separation=abs((B['center']-A['center']).dot(A['normal']))
   if separation>1e-5:continue
   overlap=polygon_overlap(A,B)
   if overlap<=1e-8:continue
   axis=B['center']-A['center'];axis-=A['normal']*axis.dot(A['normal'])
   assert axis.length>1e-8,'Coincident clast centers require explicit new decision'
   axis.normalize();mid=(A['center']+B['center'])*.5
   before=[len(A['shape']),len(B['shape'])];A['shape']=halfspace(A['shape'],axis,mid,-1);B['shape']=halfspace(B['shape'],axis,mid,1)
   corrections.append({'a':A['id'],'b':B['id'],'a_material':A['material'],'b_material':B['material'],'a_center':list(A['center']),'b_center':list(B['center']),'normal':list(A['normal']),'plane_separation_m':separation,'original_positive_overlap_area_m2':overlap,'vertices_before':before,'vertices_after':[len(A['shape']),len(B['shape'])],'method':'two-sided in-plane centroid-bisector clipping;0.1mm margin each side'})
 for r in records:
  shape=r['shape'];count=len(shape)
  if count<3:continue
  vs=[tuple(p+r['normal']*d) for d in [-r['depth']*.65,r['depth']*.35] for p in shape]
  fs=[tuple(range(count-1,-1,-1)),tuple(count+i for i in range(count))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
  part(r['name'],vs,fs,r['material'])
 (out/'geometry-repair-report.json').write_text(json.dumps({'asset_id':slug,'revision':cfg['revision'],'original_components':len(records),'corrected_actual_pairs':corrections,'unchanged_component_ids':[r['id'] for r in records if len(r['shape'])==len(r['original_shape']) and all((a-b).length<1e-9 for a,b in zip(r['shape'],r['original_shape']))],'limits':'Only actual coplanar overlapping footprint pairs clipped; no global offsets/material/render changes.'},indent=2)+'\\n')
'''
# Only breccia function changes. Preserve original host, placements, materials and export method.
s=s.replace('\ndef landslide():',insert+'\ndef landslide():');(b/'generator.py').write_text(s)
refs=json.load(open(a/'references.delivery-v001.json'));refs['packaging_rights_adapter']={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_references_sha256':hashlib.sha256((b/'references.json').read_bytes()).hexdigest(),'scope':'Targeted geometry repair delivery rights metadata; original scientific/design source ledger unchanged. New real proof subject binds this ledger.'};(b/'references.delivery-v001.json').write_text(json.dumps(refs,indent=2)+'\n')
# Reuse one-asset lifecycle only, no other candidate build/render paths.
for name in ['run-lifecycle.py','compose-sheets.py','package-candidates.py']:
 oldW=P/'stalagmite-repair-r003';t=(oldW/name).read_text().replace('stalagmite-repair-r003','breccia-repair-r003')
 if name=='run-lifecycle.py':t=t.replace("'source-metrics.json']})","'source-metrics.json','geometry-repair-report.json']})")
 if name=='package-candidates.py':
  start=t.index('notes={');end=t.index('summary=[]',start);t=t[:start]+"notes={'breccia-outcrop':'Targeted website-stage r003 repair under identical original target. Coplanar intersecting clast footprints on common host faces geometrically clipped into disjoint angular regions only at actual pair conflicts; source report records component IDs, coordinates, planes and overlap area. Embedding depth retained, no random offsets, material/alpha/camera/validator change. Original static acceptance of r002 remains historical and qualified by newly found website defect. Exact final eight512px views including clay personally inspected. New exact-GLB overlap comparison supplied. Independent targeted review pending.'}\n"+t[end:]
  t=t.replace("'base_main':'567f7a5271cca6271caba26c025bfaf39405a507'","'base_main':'b15cdab97b07f86dbc71e56fce9a44861631a20b'")
 (W/name).write_text(t)
