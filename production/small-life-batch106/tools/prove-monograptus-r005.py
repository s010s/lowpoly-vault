# SPDX-License-Identifier: MIT
"""Read-only source difference, actual solid winding, and strict embedding proof."""
import bpy,sys,json,hashlib,math,datetime,os,collections
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
old,new,out=map(Path,sys.argv[sys.argv.index('--')+1:]);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(p):
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ob=next(o for o in bpy.context.scene.objects if o.type=='MESH');me=ob.data;me.calc_loop_triangles();v=[list(ob.matrix_world@x.co) for x in me.vertices];g={x.name:[i.index for i in me.vertices if any(a.group==x.index for a in i.groups)] for x in ob.vertex_groups};tris={tag:[list(t.vertices) for t in me.loop_triangles if set(t.vertices)<=set(ids)] for tag,ids in g.items()}
 return {'v':v,'f':[list(p.vertices) for p in me.polygons],'mi':[p.material_index for p in me.polygons],'smooth':[p.use_smooth for p in me.polygons],'g':g,'t':tris,'matrix':[list(r) for r in ob.matrix_world],'objects':{o.name:{'type':o.type,'matrix':[list(r) for r in o.matrix_world],'props':{k:o[k] for k in o.keys()}} for o in bpy.context.scene.objects},'materials':[(m.name,tuple(m.diffuse_color),m.get('palette_srgb'),[(n.name,[(i.name,str(i.default_value)) for i in n.inputs if hasattr(i,'default_value')]) for n in m.node_tree.nodes]) for m in me.materials],'contacts':json.loads(ob.get('contact_design','[]')),'apertures':json.loads(ob.get('aperture_design','[]'))}
a=snapshot(old);b=snapshot(new);plane=max(a['v'][i][2] for i in a['g']['stipe']);changed_v=[i for i,v in enumerate(a['v']) if v!=b['v'][i]];changed_f=[i for i,f in enumerate(a['f']) if f!=b['f'][i]];assert not changed_v and len(changed_f)==1
# Generalized winding number uses float64 actual world-space triangles. A point
# with nonzero boundary clearance and winding magnitude one is strictly inside.
trees={k:BVHTree.FromPolygons([Vector(x) for x in b['v']],tt,all_triangles=True) for k,tt in b['t'].items()}
def classify(p,tag):
 tt=np.array([[b['v'][i] for i in t] for t in b['t'][tag]],dtype=np.float64)-np.array(p);x,y,z=tt[:,0],tt[:,1],tt[:,2];nx=np.linalg.norm(x,axis=1);ny=np.linalg.norm(y,axis=1);nz=np.linalg.norm(z,axis=1);num=np.einsum('ij,ij->i',x,np.cross(y,z));den=nx*ny*nz+np.einsum('ij,ij->i',x,y)*nz+np.einsum('ij,ij->i',y,z)*nx+np.einsum('ij,ij->i',z,x)*ny;w=float(np.arctan2(num,den).sum()/(2*math.pi));near=trees[tag].find_nearest(Vector(p));d=float(near[3]);return {'winding_number':w,'nearest_boundary_distance_m':d,'strictly_inside':abs(abs(w)-1)<1e-6 and d>1e-11,'numerical_note':'1e-11 m rejects surface-classification uncertainty; it is not an anatomical penetration threshold.'}
center=np.mean([b['v'][i] for i in a['g']['nema'][:6]],axis=0);newcap=np.mean([b['v'][i] for i in range(len(a['v']),len(b['v']))],axis=0);p=((center+newcap)/2).tolist();joint={'point_world_blender_m':p,'stipe':classify(p,'stipe'),'nema':classify(p,'nema')};assert joint['stipe']['strictly_inside'] and joint['nema']['strictly_inside']
# All newly added geometry is contained by the true original stipe. Convex
# parent terminal cell is unchanged, and all new ring vertices are strict inside.
ringtests=[{'vertex_index':i,'world':b['v'][i],'stipe':classify(b['v'][i],'stipe')} for i in range(len(a['v']),len(b['v']))];assert all(x['stipe']['strictly_inside'] for x in ringtests)
# Reclassify each declared physical-contact witness using a second solid method.
qa=json.loads((out.parent/'world-components-and-contacts.json').read_text());contact=[]
for rel in qa['physical_contact_tests']:
 hits=[]
 for key,target in [('witnesses',rel['parent']),('reverse_parent_inside_child_witnesses',rel['child'])]:
  for w in rel[key]:
   c=classify(w['world'],target)
   if c['strictly_inside']:hits.append({'world':w['world'],'strict_inside_component':target,**c})
 contact.append({'child':rel['child'],'parent':rel['parent'],'witnesses':hits,'pass':bool(hits)})
unchanged={k:{'source_vertices_identical':a['g'][k]==b['g'][k] and all(a['v'][i]==b['v'][i] for i in a['g'][k]),'source_triangles_identical':a['t'][k]==b['t'][k]} for k in a['g'] if k!='nema'}
r={'status':'pass' if all(x['pass'] for x in contact) and all(all(x.values()) for x in unchanged.values()) else 'fail','created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'original_source_sha256':h(old),'repaired_source_sha256':h(new),'original_plane_world_z_m':plane,'old_separating_plane_proves_zero_volume':max(a['v'][i][2] for i in a['g']['stipe'])==min(a['v'][i][2] for i in a['g']['nema']),'modified_original_vertex_indices':changed_v,'modified_original_polygon_indices':changed_f,'old_cap_polygon':a['f'][changed_f[0]],'new_cap_polygon':b['f'][changed_f[0]],'new_vertices':len(b['v'])-len(a['v']),'new_polygons':len(b['f'])-len(a['f']),'unchanged_non_nema_components':unchanged,'original_face_material_indices_unchanged':a['mi']==b['mi'][:len(a['mi'])],'original_smoothing_unchanged':a['smooth']==b['smooth'][:len(a['smooth'])],'materials_unchanged':a['materials']==b['materials'],'transforms_unchanged':a['matrix']==b['matrix'],'objects_and_properties_unchanged':a['objects']==b['objects'],'aperture_metadata_unchanged':a['apertures']==b['apertures'],'contact_design_unchanged':a['contacts']==b['contacts'],'shared_strict_interior_point':joint,'positive_volume_ball_radius_lower_bound_m':min(joint[x]['nearest_boundary_distance_m'] for x in ['stipe','nema'])/2,'added_ring_vertices_strictly_inside_stipe':ringtests,'all_declared_contacts_independent_winding_witnesses':contact,'limits':'Actual transformed geometry, not AABB-only. Boundary-distance ball is a measured sufficient volume certificate, not a minimum-depth criterion. Strict topology and exact exposed-GLB triangle identity are separate checks.'};assert all(r[k] for k in ['materials_unchanged','transforms_unchanged','objects_and_properties_unchanged','aperture_metadata_unchanged','contact_design_unchanged']);out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'],joint)
