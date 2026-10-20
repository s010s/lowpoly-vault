import bpy,bmesh,json,hashlib,os
from pathlib import Path
p=Path(bpy.data.filepath)
rows=[]
for ob in sorted((o for o in bpy.context.scene.objects if o.type=='MESH'),key=lambda x:x.name):
 bm=bmesh.new(); bm.from_mesh(ob.data)
 # graph components over authored mesh vertices/edges
 unseen=set(bm.verts); comps=[]
 while unseen:
  seed=unseen.pop(); stack=[seed]; comp=[seed]
  while stack:
   v=stack.pop()
   for e in v.link_edges:
    w=e.other_vert(v)
    if w in unseen: unseen.remove(w);stack.append(w);comp.append(w)
  ce={e for v in comp for e in v.link_edges}
  cfaces={f for v in comp for f in v.link_faces}
  comps.append({'vertices':len(comp),'edges':len(ce),'faces':len(cfaces),'boundary_edges':sum(e.is_boundary for e in ce),'nonmanifold_nonboundary_edges':sum(not e.is_manifold and not e.is_boundary for e in ce)})
 rows.append({'object':ob.name,'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'triangles':sum(len(f.verts)-2 for f in bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_nonboundary_edges':sum(not e.is_manifold and not e.is_boundary for e in bm.edges),'loose_vertices':sum(len(v.link_edges)==0 for v in bm.verts),'components':len(comps),'all_components_closed':all(x['boundary_edges']==0 and x['nonmanifold_nonboundary_edges']==0 for x in comps)})
 bm.free()
report={'source_file':str(p),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'mesh_objects':rows,'triangles_total':sum(r['triangles'] for r in rows),'boundary_edges_total':sum(r['boundary_edges'] for r in rows),'nonmanifold_edges_total':sum(r['nonmanifold_nonboundary_edges'] for r in rows),'loose_vertices_total':sum(r['loose_vertices'] for r in rows),'all_components_closed':all(r['all_components_closed'] for r in rows)}
Path('/tmp/lowpoly-round23-qa61/'+p.parent.parent.name+'-source-reopen.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['source_sha256','triangles_total','boundary_edges_total','nonmanifold_edges_total','loose_vertices_total','all_components_closed']}));print(json.dumps(rows))
