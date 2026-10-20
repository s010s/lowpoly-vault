# SPDX-License-Identifier: MIT
"""Read-only geometry metrics and same-fixed-frame projection silhouettes, not GPU evidence."""
from pathlib import Path
import json,sys,math,hashlib,datetime
from PIL import Image,ImageDraw
R=Path.cwd();W=R/'production/continuous-small-life-round25-20261020/work/batch-65/breccia-repair-r004';B=R/'assets/candidates/continuous-small-life-round25-20261020/batch-65/breccia-outcrop';sys.path.insert(0,str(R/'scripts'));from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,IDENTITY
D=lambda a,b:sum(x*y for x,y in zip(a,b))
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def norm(v):n=math.sqrt(D(v,v));return tuple(x/n for x in v)
def load(rev):
 p=B/rev/'model.glb';d,buf,raw=read_glb(p);world={}
 def visit(ni,parent):
  node=d['nodes'][ni];m=matmul(parent,node_matrix(node))
  if 'mesh'in node:world[node['mesh']]=m
  for ch in node.get('children',[]):visit(ch,m)
 for ni in d['scenes'][d.get('scene',0)]['nodes']:visit(ni,IDENTITY)
 tris=[];vols=[]
 for mi,m in enumerate(d['meshes']):
  volume=0
  for pr in m['primitives']:
   vs=[transform(world[mi],v) for v in accessor_values(d,buf,pr['attributes']['POSITION'])];ix=[q[0] for q in accessor_values(d,buf,pr['indices'])]
   for k in range(0,len(ix),3):
    tri=[vs[j] for j in ix[k:k+3]];tris.append(tri);volume+=D(tri[0],cross(tri[1],tri[2]))/6
  vols.append({'mesh':mi,'name':m.get('name'),'volume_m3':abs(volume)})
 return {'sha256':hashlib.sha256(raw).hexdigest(),'triangles':tris,'mesh_volumes':vols,'clast_sum_volume_m3':sum(x['volume_m3'] for x in vols if 'coherent' not in x['name']),'host_sum_volume_m3':sum(x['volume_m3'] for x in vols if 'coherent'in x['name'])}
a=load('r003');b=load('r004');directions={'front':(0,0,1),'side':(1,0,0),'rear':(0,0,-1),'top':(0,1,0),'hero':(math.sin(math.radians(35))*math.cos(math.radians(20)),math.sin(math.radians(20)),math.cos(math.radians(35))*math.cos(math.radians(20)))};rows=[]
for name,di in directions.items():
 di=norm(di);up=(0,0,1)if name=='top'else(0,1,0);u=norm(cross(up,di));v=norm(cross(di,u));project=lambda ts:[[(D(p,u),D(p,v))for p in t]for t in ts];ps=[project(x['triangles'])for x in [a,b]];allp=[p for q in ps for t in q for p in t];lo=[min(p[k]for p in allp)for k in range(2)];hi=[max(p[k]for p in allp)for k in range(2)];scale=460/max(hi[k]-lo[k]for k in range(2));center=[(lo[k]+hi[k])/2for k in range(2)];masks=[]
 for label,triangles in zip(['r003','r004'],ps):
  im=Image.new('1',(512,512));draw=ImageDraw.Draw(im)
  for t in triangles:draw.polygon([(round(256+(p[0]-center[0])*scale),round(256-(p[1]-center[1])*scale))for p in t],fill=1)
  masks.append(list(im.getdata()));im.save(W/('diagnostic-silhouette-'+name+'-'+label+'.png'))
 union=sum(bool(x or y)for x,y in zip(*masks));inter=sum(bool(x and y)for x,y in zip(*masks));changed=sum(x!=y for x,y in zip(*masks));rows.append({'view':name,'same_fixed_frame':True,'original_area_px':sum(masks[0]),'corrected_area_px':sum(masks[1]),'intersection_over_union':inter/union,'changed_union_fraction':changed/union,'limits':'Orthographic triangle-union raster diagnostic, not renderer/material/shadow or website evidence.'})
rep=json.load(open(B/'r004/geometry-repair-report.json'));m=rep['component_metrics'];out={'kind':'targeted_geometry_volume_and_silhouette_change','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original':{k:v for k,v in a.items()if k!='triangles'},'corrected':{k:v for k,v in b.items()if k!='triangles'},'retained_clast_summed_volume_fraction_vs_r003':b['clast_sum_volume_m3']/a['clast_sum_volume_m3'],'changed_components_vs_initial_120':120-len(rep['unchanged_component_ids']),'emitted_closed_solid_count':sum(x['emitted']for x in m),'minimum_individual_retained_volume_fraction_vs_original_initial_shape':min(x['retained_volume_fraction']for x in m),'components_retaining_under25percent_initial_volume':sum(x['retained_volume_fraction']<.25 for x in m),'actual_parallel_volume_conflict_pairs':len(rep['corrected_actual_pairs']),'maximum_corrected_center_plane_separation_m':max(x['plane_separation_m']for x in rep['corrected_actual_pairs']),'projection_silhouette_comparison':rows,'limits':'Summed separate clast volumes are not boolean-union volume, since original clasts interpenetrated. R003→r004 is exact-export comparison; per-component fractions in source report use original preclipping120shapes. Original120centers/materials/depths retained. No GPU/website clearance.'};(W/'geometry-change-quantification.json').write_text(json.dumps(out,indent=2)+'\n');print(out['retained_clast_summed_volume_fraction_vs_r003']);print([(x['view'],round(x['intersection_over_union'],5))for x in rows])
