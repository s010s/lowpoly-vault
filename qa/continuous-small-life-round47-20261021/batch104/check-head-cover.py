import bpy,sys,json,pathlib,hashlib,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree
Q=pathlib.Path(__file__).resolve().parent;I=json.loads((Q/'final-intake.json').read_text());W=pathlib.Path(I['worktree']);a=next(x for x in I['assets']if x['asset_id']=='arthropleura');src=W/a['source'];h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sha=h(src)
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);o=next(o for o in bpy.context.scene.objects if o.type=='MESH');m=o.data;m.calc_loop_triangles();v=[o.matrix_world@x.co for x in m.vertices];tr=[tuple(t.vertices)for t in m.loop_triangles]
def tree(name):
 gi=o.vertex_groups[name].index;ss={x.index for x in m.vertices if any(g.group==gi and g.weight>0 for g in x.groups)};return BVHTree.FromPolygons(v,[t for t in tr if set(t)<=ss],all_triangles=True),ss
head,ids=tree('flattened_head');collum,cids=tree('dorsal_unit_01');lo=[min(v[i][k]for i in ids)for k in range(3)];hi=[max(v[i][k]for i in ids)for k in range(3)];N=201;total=covered=0;front=[]
for i in range(N):
 for j in range(N):
  p=Vector((lo[0]+(hi[0]-lo[0])*(i+.5)/N,lo[1]+(hi[1]-lo[1])*(j+.5)/N,.1));hp,_,_,_=head.ray_cast(p,Vector((0,0,-1)),1)
  if hp is None:continue
  total+=1;cp,_,_,_=collum.ray_cast(p,Vector((0,0,-1)),1)
  if cp is not None and cp.z>hp.z:covered+=1
  elif len(front)<5:front.append(list(hp))
result={'asset_id':'arthropleura','revision':a['revision'],'source_sha256':sha,'glb_sha256':h(W/a['glb']),'pid':os.getpid(),'source_unchanged':h(src)==sha,'grid':N,'head_projected_hits':total,'head_covered_by_collum_hits':covered,'diagnostic_projected_covered_fraction':covered/total,'head_bounds_blender_m':{'min':lo,'max':hi},'collum_bounds_blender_m':{'min':[min(v[i][k]for i in cids)for k in range(3)],'max':[max(v[i][k]for i in cids)for k in range(3)]},'visible_head_sample_points':front,'method':'Actual unmodified transformed source triangle BVHs. Orthographic top projected grid: head hit is covered only when collum ray hit is vertically above it. Diagnostic comparison to original qualitative mostly-beneath requirement, not a new general exposure threshold.'}
(Q/'arthropleura/head-cover-diagnostic.json').open('x').write(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
