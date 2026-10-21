import bpy,sys,pathlib,json,math,struct,hashlib,os,datetime
from mathutils import Vector
b=pathlib.Path(sys.argv[sys.argv.index('--')+1]);bpy.ops.wm.open_mainfile(filepath=str(b/'source.blend'));sem=json.loads((b/'geometry-semantics.json').read_text());cfg=json.loads((b/'build-config.json').read_text());p=cfg['parameters'];path=[Vector(q) for q in sem['paths'][0]];T=p['slab_dimensions_m'][2];r=p['neck_radius_m'];h=p['neck_relief_height_m'];f32=lambda x:struct.unpack('f',struct.pack('f',x))[0];rows=[]
for o in bpy.data.collections['EXPORT'].all_objects:
 if o.type!='MESH':continue
 for vert in o.data.vertices:
  world=o.matrix_world@vert.co;x,y,z=world;q=Vector((x,y));best=1e9
  for a,bp in zip(path,path[1:]):
   v=bp-a;t=max(0,min(1,(q-a).dot(v)/v.length_squared));best=min(best,(q-a-v*t).length)
  neck=h*math.sqrt(max(0,1-(best/r)**2)) if best<r else 0
  baseline=f32(T+neck) if z>=f32(T) else z
  rows.append({'world_blender_xyz_m':list(world),'neck_only_baseline_z_m':baseline,'actual_chamber_increment_m':z-baseline,'nearest_neck_path_distance_m':best})
report={'source_sha256':hashlib.sha256((b/'source.blend').read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((b/'model.glb').read_bytes()).hexdigest(),'pid':os.getpid(),'host_observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Reopened actual source world vertices. Independently evaluate unchanged piecewise-linear97point neck field at actual vertex XY, using original Blender Vector arithmetic; convert baseline Z to exact float32 as exported. Actual geometry minus neck-only baseline is measured, not a chamber label. Export analyzer must map every source and GLB vertex exactly and bound every incident triangle.','rows':rows}
(b/'source-neck-baseline.json').write_text(json.dumps(report,indent=2)+'\n');print('BASELINE',len(rows),min(v['actual_chamber_increment_m'] for v in rows),sum(v['actual_chamber_increment_m']>0 for v in rows))
