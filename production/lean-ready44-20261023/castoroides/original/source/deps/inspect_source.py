# SPDX-License-Identifier: MIT
"""Reopen source and bind mechanical checks to the exported GLB, not visual approval."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import audit_source

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 av=sys.argv[sys.argv.index('--')+1:];blend=Path(av[0]).resolve();glb=Path(av[1]).resolve();out=Path(av[2]).resolve()
 bpy.ops.wm.open_mainfile(filepath=str(blend));col=bpy.data.collections.get('EXPORT');q=audit_source(col,16000)
 meshes=[o for o in col.all_objects if o.type=='MESH'];foot={o.name:min((o.matrix_world@v.co).z for v in o.data.vertices) for o in meshes if o.name.startswith(('forefoot_','hindfoot_'))}
 teeth={}
 for side in ['L','R']:
  up=bpy.data.objects['upper_fluted_incisor_'+side];lo=bpy.data.objects['lower_fluted_incisor_'+side]
  def tree(ob):return BVHTree.FromPolygons([ob.matrix_world@v.co for v in ob.data.vertices],[tuple(f.vertices) for f in ob.data.polygons],all_triangles=False)
  teeth[side]={'upper_lower_triangle_overlap_count':len(tree(up).overlap(tree(lo))),'upper_vertices':len(up.data.vertices),'lower_vertices':len(lo.data.vertices)}
 external=[{'kind':'image','name':i.name} for i in bpy.data.images if i.source=='FILE' and not i.packed_file]
 external += [{'kind':'library','name':v.name} for v in bpy.data.libraries]
 r={'source_blend_sha256':sha(blend),'source_glb_sha256':sha(glb),'blender':bpy.app.version_string,'reopened_source_audit':q,'source_collections':[c.name for c in bpy.data.collections],'camera_count':sum(o.type=='CAMERA' for o in bpy.data.objects),'light_count':sum(o.type=='LIGHT' for o in bpy.data.objects),'external_file_dependencies':external,'foot_sole_min_z_m':foot,'incisor_pair_mesh_overlap':teeth,'all_anatomical_components_closed':all(part['boundary_edges']==part['nonmanifold_edges']==0 for part in q['parts']),'scope':'Reopened source and narrow tooth collision test only; intentional part intersections elsewhere are not a printable union claim.'}
 print('DETAILS',json.dumps({'foot':foot,'teeth':teeth}))
 assert not q['errors'] and not external and r['camera_count']==r['light_count']==0
 assert max(foot.values())<.002
 assert all(t['upper_lower_triangle_overlap_count']==0 for t in teeth.values())
 out.write_text(json.dumps(r,indent=2)+'\n');print('SOURCE_INSPECTION_OK')
if __name__=='__main__':main()
