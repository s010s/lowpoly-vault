import json,math,collections,datetime,hashlib
from pathlib import Path
import numpy as np
O=Path(__file__).parent
A=json.loads((O/'r004-source-snapshot.json').read_text());B=json.loads((O/'r005-source-snapshot.json').read_text());a=A['meshes'][0];b=B['meshes'][0]
changed_v=[i for i,v in enumerate(a['vertices']) if v!=b['vertices'][i]];changed_f=[i for i,v in enumerate(a['faces']) if v!=b['faces'][i]];n=len(a['vertices']);plane=max(a['world_vertices'][i][2] for i in a['groups']['stipe'])
ident={'original_vertices_retained_exact':not changed_v,'original_vertex_weights_retained':a['weights']==b['weights'][:n],'changed_original_faces':changed_f,'added_vertices':len(b['vertices'])-n,'added_faces':len(b['faces'])-len(a['faces']),'all_original_face_materials_retained':a['face_materials']==b['face_materials'][:len(a['faces'])],'all_original_smoothing_retained':a['smoothing']==b['smoothing'][:len(a['faces'])],'materials_identical':a['materials']==b['materials'],'transforms_identical':a['matrix_world']==b['matrix_world'],'objects_properties_collections_units_identical':all(A[k]==B[k] for k in ['objects','collections','units']),'contacts_apertures_identical':a['contacts']==b['contacts'] and a['apertures']==b['apertures'],'non_nema_groups_identical':all(a['groups'][g]==b['groups'][g] for g in a['groups'] if g!='nema'),'old_triangles':len(a['triangles']),'new_triangles':len(b['triangles']),'original_plane_z_m':plane,'new_bounds_unchanged':np.array_equal(np.min(a['world_vertices'],axis=0),np.min(b['world_vertices'],axis=0)) and np.array_equal(np.max(a['world_vertices'],axis=0),np.max(b['world_vertices'],axis=0))}
assert not changed_v and changed_f==[1448] and ident['added_vertices']==6 and ident['added_faces']==6
assert all(v for k,v in ident.items() if isinstance(v,bool))
# Independent double precision point-triangle distance: closest projected point when
# barycentric coordinates are in the triangle, otherwise the three edge segments.
def distance(p,T):
 x,y,z=T[:,0],T[:,1],T[:,2];u=y-x;v=z-x;w=p-x;normal=np.cross(u,v);nn=np.einsum('ij,ij->i',normal,normal);nd=np.einsum('ij,ij->i',w,normal);proj=p-(nd/nn)[:,None]*normal;ww=proj-x
 uu=np.einsum('ij,ij->i',u,u);uv=np.einsum('ij,ij->i',u,v);vv=np.einsum('ij,ij->i',v,v);wu=np.einsum('ij,ij->i',ww,u);wv=np.einsum('ij,ij->i',ww,v);den=uu*vv-uv*uv;s=(vv*wu-uv*wv)/den;t=(uu*wv-uv*wu)/den
 d2=np.where((s>=0)&(t>=0)&(s+t<=1),nd*nd/nn,np.inf)
 for f,e in [(x,y),(y,z),(z,x)]:
  ed=e-f;lam=np.clip(np.einsum('ij,ij->i',p-f,ed)/np.einsum('ij,ij->i',ed,ed),0,1);d2=np.minimum(d2,np.sum((p-f-lam[:,None]*ed)**2,axis=1))
 return float(np.sqrt(d2.min()))
def classify(p,T):
 p=np.asarray(p,dtype=np.float64);d=distance(p,T)
 if d<=1e-12:return {'strict':False,'boundary_distance_m':d,'winding':None,'classification':'boundary-or-numerically-unresolved'}
 x,y,z=(T-p).transpose(1,0,2);nx=np.linalg.norm(x,axis=1);ny=np.linalg.norm(y,axis=1);nz=np.linalg.norm(z,axis=1);num=np.einsum('ij,ij->i',x,np.cross(y,z));den=nx*ny*nz+np.einsum('ij,ij->i',x,y)*nz+np.einsum('ij,ij->i',y,z)*nx+np.einsum('ij,ij->i',z,x)*ny;w=float(np.sum(np.arctan2(num,den))/(2*np.pi));return {'strict':abs(w-1)<1e-7,'boundary_distance_m':d,'winding':w}
def prepare(m):
 V=np.array(m['world_vertices'],dtype=np.float64);F=np.array(m['triangles']);G={k:set(v) for k,v in m['groups'].items()};FI={g:np.array([i for i,f in enumerate(F) if set(f)<=ids]) for g,ids in G.items()};T={g:V[F[ix]] for g,ix in FI.items()};return V,F,FI,T

def solid_checks(m):
 V,F,FI,T=prepare(m);top=[];contacts=[]
 for g,ix in FI.items():
  ff=F[ix];edges=collections.defaultdict(list);adj=collections.defaultdict(set)
  for f in ff:
   for i,j in zip(f,np.roll(f,-1)):edges[tuple(sorted((int(i),int(j))))].append((int(i),int(j)));adj[int(i)].add(int(j));adj[int(j)].add(int(i))
  unseen=set(m['groups'][g]);islands=[]
  while unseen:
   seed=unseen.pop();todo=[seed];part={seed}
   while todo:
    for j in adj[todo.pop()]&unseen:unseen.remove(j);part.add(j);todo.append(j)
   tt=V[[f for f in ff if f[0] in part]];vol=float(np.sum(np.einsum('ij,ij->i',tt[:,0],np.cross(tt[:,1],tt[:,2])))/6);islands.append({'vertices':len(part),'triangles':len(tt),'signed_volume_m3':vol})
  deg=int(np.sum(np.linalg.norm(np.cross(T[g][:,1]-T[g][:,0],T[g][:,2]-T[g][:,0]),axis=1)==0));bad=sum(len(x)!=2 for x in edges.values());same=sum(len(x)==2 and x[0]==x[1] for x in edges.values());top.append({'component':g,'islands':islands,'nonmanifold_edges':bad,'same_direction_edges':same,'degenerate_triangles':deg,'pass':not(bad or same or deg) and all(x['signed_volume_m3']>0 for x in islands)})
 for rel in m['contacts']:
  ch,pa=rel['child'],rel['parent'];witness=None
  for source,target in [(ch,pa),(pa,ch)]:
   tt=T[source];norm=np.cross(tt[:,1]-tt[:,0],tt[:,2]-tt[:,0]);norm/=np.linalg.norm(norm,axis=1)[:,None]
   for center,normal in zip(tt.mean(axis=1),norm):
    test=classify(center,T[target])
    if not test['strict']:continue
    for ratio in [0.25,0.05,0.01]:
     q=center-normal*min(test['boundary_distance_m']*ratio,1e-7);cq=classify(q,T[ch]);pq=classify(q,T[pa])
     if cq['strict'] and pq['strict']:
      witness={'point_world_m':q.tolist(),'child':cq,'parent':pq,'shared_open_ball_radius_m':min(cq['boundary_distance_m'],pq['boundary_distance_m'])/2};break
    if witness:break
   if witness:break
  contacts.append({**rel,'shared_interior_witness':witness,'pass':witness is not None})
 return {'topology':top,'contacts':contacts,'failures':{'topology':[x['component'] for x in top if not x['pass']],'contacts':[x['child'] for x in contacts if not x['pass']]}}
old=solid_checks(a);new=solid_checks(b);V,F,FI,T=prepare(b)
base=np.array([a['world_vertices'][i] for i in a['groups']['nema'][:6]]);extra=V[n:];p=(base.mean(axis=0)+extra.mean(axis=0))/2
joint={'point_world_m':p.tolist(),'stipe':classify(p,T['stipe']),'nema':classify(p,T['nema'])};joint['shared_open_ball_radius_m']=min(joint[k]['boundary_distance_m'] for k in ['stipe','nema'])/2
newring=[{'index':n+i,'point_world_m':q.tolist(),**classify(q,T['stipe'])} for i,q in enumerate(extra)]
# Verify the original terminal stipe cell is convex and that the added six quads
# and basal cap fit inside its supporting planes. This proves the entire faces,
# not just their vertices or AABB, remain hidden in the original true solid.
from scipy.spatial import ConvexHull
terminal_ids=a['groups']['stipe'][-16:];cell=np.array([a['world_vertices'][i] for i in terminal_ids]);hull=ConvexHull(cell);testpoints=np.concatenate([base,extra]);planes=testpoints@hull.equations[:,:3].T+hull.equations[:,3]
contain={'original_terminal_stipe_cell_vertex_ids':terminal_ids,'convex_hull_volume_m3':float(hull.volume),'maximum_signed_plane_distance_m':float(planes.max()),'all_added_geometry_inside_or_on_original_terminal_cell':bool(np.all(planes<=1e-12)),'new_ring_strict_parent_interior':all(x['strict'] for x in newring),'method':'Actual stipe terminal cell is the final two equal octagonal rings joined by straight side faces; convex supporting halfspaces contain every vertex of each added planar face, so each entire face is contained. Original retained upper ring is on the original cap plane.'}
assert old['failures']=={'topology':[],'contacts':['nema']};assert new['failures']=={'topology':[],'contacts':[]};assert joint['stipe']['strict'] and joint['nema']['strict'];assert contain['all_added_geometry_inside_or_on_original_terminal_cell'] and contain['new_ring_strict_parent_interior']
r={'status':'PASS','identity':ident,'old_r004':old,'new_r005':new,'original_exact_halfspaces':{'plane_z_m':plane,'stipe_vertices_above':sum(a['world_vertices'][i][2]>plane for i in a['groups']['stipe']),'nema_vertices_below':sum(a['world_vertices'][i][2]<plane for i in a['groups']['nema']),'zero_positive_volume':max(a['world_vertices'][i][2] for i in a['groups']['stipe'])==min(a['world_vertices'][i][2] for i in a['groups']['nema'])},'new_shared_interior':joint,'hidden_new_ring':newring,'hidden_full_faces':contain,'numerics':'Float64 source coordinates and centroids, true point-triangle distance and generalized signed solid angle. 1e-12 m boundary uncertainty band is numerical classification protection, not an anatomical penetration requirement. Shared positive-clearance interior ball proves positive overlap volume; no minimum depth/percentage introduced.'}
(O/'geometry-and-difference.json').write_text(json.dumps(r,indent=2)+'\n');(O/'recovery-02-source-and-solid.json').write_text(json.dumps({'stage':'fresh-source-and-solid','status':'PASS','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'uncertain_jobs':[]},indent=2)+'\n');print('PASS',joint,old['failures'],new['failures'])
