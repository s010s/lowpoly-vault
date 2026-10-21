import numpy as np,json,pathlib,datetime,hashlib
O=pathlib.Path(__file__).parent
for a in ['eleutherocrinus','nucleocrinus']:
 z=np.load(O/a/'source-triangles.npz');V=z['vertices'];T=z['triangles'];prior=json.loads((O/a/'targeted-proof-v2.json').read_text());out=[]
 for rec in prior['checks']:
  ids=rec['original_vertices'];rest=T[~np.all(np.isin(T,ids),axis=1)];tri=V[rest];checks=[]
  for p in [V[ids].mean(axis=0),*V[ids]]:
   v=tri-p;norm=np.linalg.norm(v,axis=2);num=np.einsum('ij,ij->i',v[:,0],np.cross(v[:,1],v[:,2]));den=norm[:,0]*norm[:,1]*norm[:,2]+np.einsum('ij,ij->i',v[:,0],v[:,1])*norm[:,2]+np.einsum('ij,ij->i',v[:,1],v[:,2])*norm[:,0]+np.einsum('ij,ij->i',v[:,2],v[:,0])*norm[:,1];w=np.sum(2*np.arctan2(num,den))/(4*np.pi);checks.append(float(w))
  out.append(dict(component=rec['component'],part=rec['part'],vertices=ids,rest_triangles=len(rest),crossing_pairs=rec['intersections_with_entire_rest_scene'],winding_numbers_centroid_then_all_vertices=checks,minimum_vertex_surface_distance_m=min(rec['nearest_rest_surface_distances']),all_outside=all(abs(w)<1e-8 for w in checks),notes='Double precision signed solid angle sum over all other original closed outward solids. Inside contributions add, rather than odd/even cancelling overlaps. Combined with zero candidate/rest triangle crossings, this distinguishes disjoint pieces from wholly contained pieces. 1e-8 is dimensionless floating summation diagnostic, not anatomical gap threshold.'))
 r=dict(asset=a,created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),geometry_npz_sha256=hashlib.sha256((O/a/'source-triangles.npz').read_bytes()).hexdigest(),checks=out);(O/a/'solid-angle-proof.json').write_text(json.dumps(r,indent=2)+'\n');print(a,[(x['component'],x['part'],x['all_outside'],x['minimum_vertex_surface_distance_m'],max(abs(w) for w in x['winding_numbers_centroid_then_all_vertices'])) for x in out])
