import json,math,datetime
from pathlib import Path
import numpy as np
# Reuse only this independent reviewer's freshly written geometry math.
from geometry_audit import prepare,classify
O=Path(__file__).parent
angles={'hero':(35,35),'reversehero':(215,35),'front':(0,0),'side':(90,0),'rear':(180,0),'top':(0,90),'lower_oblique':(45,-50),'lower_proximal':(-30,-60)}
D={k:np.array([math.sin(math.radians(a))*math.cos(math.radians(e)),-math.cos(math.radians(a))*math.cos(math.radians(e)),math.sin(math.radians(e))]) for k,(a,e) in angles.items()}
def audit(rev):
 m=json.loads((O/(rev+'-source-snapshot.json')).read_text())['meshes'][0];V,F,FI,T=prepare(m);allT=V[F];e1=allT[:,1]-allT[:,0];e2=allT[:,2]-allT[:,0];centers=allT.mean(axis=1);norm=np.cross(e1,e2);norm/=np.linalg.norm(norm,axis=1)[:,None];labels={int(i):g for g,idx in FI.items() for i in idx}
 def cast(points,d):
  p=np.cross(np.broadcast_to(d,e2.shape),e2);det=np.einsum('ij,ij->i',e1,p);valid=abs(det)>1e-24;inv=np.zeros_like(det);inv[valid]=1/det[valid];answers=[]
  for begin in range(0,len(points),48):
   origins=points[begin:begin+48];s=origins[:,None,:]-allT[None,:,0];u=np.einsum('kij,ij->ki',s,p)*inv;q=np.cross(s,e1);v=np.einsum('j,kij->ki',d,q)*inv;t=np.einsum('ij,kij->ki',e2,q)*inv;ok=valid&(u>=-1e-12)&(v>=-1e-12)&(u+v<=1+1e-12)&(t>1e-12);dist=np.where(ok,t,np.inf);idx=np.argmin(dist,axis=1);best=dist[np.arange(len(origins)),idx];answers.extend((float(dd),int(ii)) for dd,ii in zip(best,idx))
  return answers
 visibility={g:{} for g in FI};witnesses={g:[] for g in FI}
 for name,d in D.items():
  eligible=np.where(norm@d>0)[0];hit=cast(centers[eligible]+d*1e-10,d);clear=[int(i) for i,(dist,j) in zip(eligible,hit) if not math.isfinite(dist)]
  for g,idx in FI.items():
   vis=[i for i in clear if labels[i]==g];visibility[g][name]=len(vis)
   if vis and len(witnesses[g])<2:witnesses[g].append({'triangle_index':vis[0],'point_world_m':centers[vis[0]].tolist(),'direction':name})
 aps=[]
 for ap in m['apertures']:
  g=ap['component'];ring=V[[m['groups'][g][i] for i in ap['terminal_ring_local_indices']]];p=ring.mean(axis=0);d=np.array(ap['direction']);d/=np.linalg.norm(d);insidepoint=p-d*1e-10;occ=[k for k in T if classify(insidepoint,T[k])['strict']];depth,fi=cast(np.array([insidepoint]),-d)[0];hits=[]
  for name,dd in {'axis':d,**D}.items():
   if dd@d<=0:continue
   hit,j=cast(np.array([p+dd*1e-10]),dd)[0];hits.append({'direction':name,'open':not math.isfinite(hit),'first_component':labels[j] if math.isfinite(hit) else None,'distance_m':hit if math.isfinite(hit) else None})
  aps.append({'component':g,'actual_ring_center_world_m':p.tolist(),'center_metadata_error_m':float(np.linalg.norm(p-np.array(ap['center']))),'occupied_by_any_global_solid':occ,'actual_axis_recess_m':depth,'floor_component':labels[fi] if math.isfinite(depth) else None,'outward_rays':hits,'pass':not occ and math.isfinite(depth) and depth>0 and any(x['open'] for x in hits)})
 return {'revision':rev,'whole_scene_solid_count':len(T),'all_triangles':len(F),'component_exposure':[{'component':g,'visible_centroids_by_direction':visibility[g],'witnesses':witnesses[g],'pass':bool(witnesses[g])} for g in T],'apertures':aps,'failures':{'exposure':[g for g in T if not witnesses[g]],'apertures':[x['component'] for x in aps if not x['pass']]}}
a=audit('r004');b=audit('r005');same=all(x['visible_centroids_by_direction']==y['visible_centroids_by_direction'] for x,y in zip(a['component_exposure'],b['component_exposure']));r={'status':'PASS' if not any(a['failures'].values()) and not any(b['failures'].values()) else 'REVISE','old':a,'new':b,'whole_scene_exposure_counts_identical':same,'method':'Fresh float64 Moller-Trumbore ray intersections with every actual scene triangle; test all outward-facing triangle centroids in eight directions. Actual rim-center rays and inward floor against all global solids. No percentage, off-axis completeness, minimum depth, or infinite-axis-unblocked gate added. An axis may see a remote neighboring theca while a real exterior witness remains visible.'};(O/'global-exposure-and-recesses.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],'same counts',same,a['failures'],b['failures']);(O/'recovery-03-global-rays.json').write_text(json.dumps({'stage':'whole-scene-rays','status':r['status'],'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uncertain_jobs':[]},indent=2)+'\n')
