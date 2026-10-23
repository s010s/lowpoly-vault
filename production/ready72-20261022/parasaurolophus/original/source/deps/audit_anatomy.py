#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Asset-specific source geometry probes; not visual/factual certification."""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
A=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(); p.add_argument('blend',type=Path); p.add_argument('glb',type=Path); p.add_argument('--output',type=Path,required=True); a=p.parse_args(A)
bpy.ops.wm.open_mainfile(filepath=str(a.blend.resolve()))
P=json.loads((Path(__file__).resolve().parents[1]/'params.json').read_text()); shift=P['footprint_origin_y_translation_m']
o=bpy.data.objects['Parasaurolophus-editable-anatomy']; m=o.data; m.calc_loop_triangles()
verts=[v.co.copy() for v in m.vertices]; groups={}
for g in o.vertex_groups:
    ids={v.index for v in m.vertices if any(w.group==g.index for w in v.groups)}
    ts=[tuple(t.vertices) for t in m.loop_triangles if set(t.vertices).issubset(ids)]
    volume=sum(verts[t[0]].dot(verts[t[1]].cross(verts[t[2]]))/6 for t in ts)
    edges={}
    for t in ts:
        for k in range(3):
            e=tuple(sorted((t[k],t[(k+1)%3]))); edges[e]=edges.get(e,0)+1
    groups[g.name]={'vertices':len(ids),'triangles':len(ts),'signed_volume_m3':volume,'boundary_edges':sum(c==1 for c in edges.values()),'nonmanifold_edges':sum(c>2 for c in edges.values()),'bounds':{'min':[min(verts[i][k] for i in ids) for k in range(3)],'max':[max(verts[i][k] for i in ids) for k in range(3)]},'_ids':ids,'_triangles':ts}
checks=[]
def check(name,ok,detail): checks.append({'name':name,'status':'pass' if ok else 'fail','detail':detail})
check('all_anatomical_components_closed_outward',all(q['signed_volume_m3']>0 and q['boundary_edges']==q['nonmanifold_edges']==0 for q in groups.values()),'Per-component signed-volume and triangle-edge incidence; does not certify union or intersection appearance.')
check('source_scene_export_only',all(x.type in {'MESH','EMPTY'} for x in bpy.context.scene.objects) and 'EXPORT' in bpy.data.collections,'No source camera, light, floor or preview-helper object.')
root=bpy.data.objects['parasaurolophus']; check('root_identity',all(abs(root.matrix_world[i][j]-(1 if i==j else 0))<1e-8 for i in range(4) for j in range(4)),[list(row) for row in root.matrix_world])
lo=[min(v[k] for v in verts) for k in range(3)]; hi=[max(v[k] for v in verts) for k in range(3)]
check('nine_metre_approximate_target',abs(hi[1]-lo[1]-9)<1e-5,{'posed_bounds_blender_m':{'min':lo,'max':hi},'scope':'Genus-level artistic scale, not measured complete ROM768.'})
feet={n:q['bounds']['min'][2] for n,q in groups.items() if n.endswith('-hind-foot-pad') or n.endswith('-fore-hand-mitten')}
check('four_contact_pads_at_floor',len(feet)==4 and all(abs(z)<1e-6 for z in feet.values()),feet)
contact=[verts[i] for n,q in groups.items() if n in feet for i in q['_ids'] if abs(verts[i].z)<1e-6]
center=[sum(v[k] for v in contact)/len(contact) for k in range(2)]
check('root_at_contact_centroid',all(abs(c)<1e-6 for c in center),{'four_pad_contact_centroid_xy_m':center})
body=groups['ribcage-hip-and-comparatively-reconstructed-tail']; tail=[verts[i] for i in body['_ids'] if verts[i].y>=1.32+shift]
check('tail_clear_of_floor',min(v.z for v in tail)>1.5,{'lowest_reconstructed_tail_m':min(v.z for v in tail)})
crest=groups['diagnostic-backward-tubular-cranial-crest']; neck=groups['neck-healthy-living-contour']
targettris=body['_triangles']+neck['_triangles']; tree=BVHTree.FromPolygons(verts,targettris,all_triangles=True)
free=[verts[i] for i in crest['_ids'] if verts[i].y>-2.22+shift]
dist=min(tree.find_nearest(v)[3] for v in free)
free_tris=[t for t in crest['_triangles'] if all(verts[i].y>-2.22+shift for i in t)]
intersections=BVHTree.FromPolygons(verts,free_tris,all_triangles=True).overlap(tree)
check('free_crest_clear_of_neck_and_back',dist>.01 and len(intersections)==0,{'minimum_vertex_to_neck_or_trunk_surface_m':dist,'triangle_intersection_pairs':len(intersections),'criterion':'No sampled free-crest/neck-trunk triangle intersections, positive vertex-surface clearance above 0.01 m numerical margin.','excluded_root':'Crest vertices before the authored -2.22 m section include intentional cranial attachment; remaining sample is lowpoly vertex/surface distance, not exhaustive triangle clearance.'})
check('long_backward_tube_extent',crest['bounds']['max'][1]-crest['bounds']['min'][1]>1.5,crest['bounds'])
check('no_extra_unrequested_scene_objects',set(bpy.data.objects)=={root,o},[x.name for x in bpy.data.objects])
for q in groups.values(): del q['_ids']; del q['_triangles']
r={'kind':'asset-specific-source-geometry','asset_id':'parasaurolophus','revision':'r001','source_blend_sha256':hashlib.sha256(a.blend.read_bytes()).hexdigest(),'source_glb_sha256':hashlib.sha256(a.glb.read_bytes()).hexdigest(),'status':'pass' if all(q['status']=='pass' for q in checks) else 'fail','checks':checks,'components':groups,'limitations':['Separate closed anatomical volumes intentionally overlap at joints, cheeks and small facial details. Not a Boolean union or printable solid.','Edge incidence and signed volume do not prove absence of self-intersection. Independent pixel inspection remains required.','No internal airway, inferred skin colour, or exact missing tail/hindlimb anatomy is asserted.']}
a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps({'status':r['status'],'checks':checks}))
if r['status']!='pass': sys.exit(1)
