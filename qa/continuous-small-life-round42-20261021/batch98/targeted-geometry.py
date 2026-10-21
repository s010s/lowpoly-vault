import bpy,json,pathlib,hashlib,datetime,os,math,collections
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch98-20261020');B=W/'production/small-life-batch98';Q=pathlib.Path(__file__).parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
aid='agathis';src=B/aid/'r001/artifacts'/f'{aid}.blend';bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ct=json.loads(bpy.data.texts['BATCH98_COMPONENT_CONTRACT.json'].as_string());ob=bpy.data.objects[ct['object_name']];v=[ob.matrix_world@p.co for p in ob.data.vertices];ob.data.calc_loop_triangles();ts=[tuple(t.vertices) for t in ob.data.loop_triangles];owner={i:c['tag'] for c in ct['components'] for i in c['vertices']};tby=collections.defaultdict(list)
for i,t in enumerate(ts):tby[owner[t[0]]].append(i)
whole=BVHTree.FromPolygons(v,ts,all_triangles=True);directions=[]
for i in range(80):
 z=1-2*(i+.5)/80;a=i*math.pi*(3-math.sqrt(5));r=math.sqrt(1-z*z);directions.append(Vector((r*math.cos(a),r*math.sin(a),z)))
coretris=[ts[i] for i in tby['seed_cone_core']];planes=[]
for tr in coretris:
 a,b,c=[v[i] for i in tr];n=(b-a).cross(c-a).normalized();planes.append((a,n))
records=[]
for comp in ct['components']:
 if comp['kind'] not in ['cone_scale','seed_cone']:continue
 samples=[];ins=0;vis=0;witness=[]
 for ti in tby[comp['tag']]:
  a,b,c=[v[i] for i in ts[ti]]
  for u,w in [(1/3,1/3),(.8,.1),(.1,.8),(.1,.1),(.45,.1),(.1,.45),(.45,.45)]:
   p=a*u+b*w+c*(1-u-w);outside=max(float((p-q).dot(n)) for q,n in planes);inside=outside < -1e-7
   if comp['kind']=='cone_scale' and inside:ins+=1;continue
   visible=False
   for direction in directions:
    start=p+direction*.20;hit,normal,ix,dist=whole.ray_cast(start,-direction,.20001)
    if ix is not None and owner[ts[ix][0]]==comp['tag'] and (hit-p).length<2e-6:
     visible=True
     if len(witness)<2:witness.append({'triangle':ti,'point_m':list(p),'direction_to_viewer':list(direction),'hit_triangle':ix,'distance_to_sample_m':(hit-p).length})
     break
   vis+=int(visible)
  samples.append(ti)
 records.append({'tag':comp['tag'],'kind':comp['kind'],'samples':len(samples)*7,'samples_inside_convex_core_by_halfspaces':ins,'surface_samples_visible_from_external_rays':vis,'witnesses':witness,'vertices_world_m':[list(v[i]) for i in comp['vertices']]})
r={'asset_id':aid,'source_sha256':H(src),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'method':'Seven barycentric samples per actual transformed triangle. Core containment uses all outward convex-core face halfspaces with 1e-7m strict-inside threshold. Visibility casts from 0.2m outside cone toward each sample along 80 Fibonacci sphere directions and checks first-hit owner and sample proximity <=2e-6m. Positive samples establish exposed surface; zero samples do not mathematically prove total burial. No model/export edits.','components':records,'zero_visible_scale_samples':[r['tag'] for r in records if r['kind']=='cone_scale' and r['surface_samples_visible_from_external_rays']==0]}
(Q/aid/'targeted-cone-exposure.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='components'}));print([(r['tag'],r['samples_inside_convex_core_by_halfspaces'],r['surface_samples_visible_from_external_rays']) for r in records])
aid='voltzia';src=B/aid/'r001/artifacts'/f'{aid}.blend';bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ct=json.loads(bpy.data.texts['BATCH98_COMPONENT_CONTRACT.json'].as_string());ob=bpy.data.objects[ct['object_name']];v=[ob.matrix_world@p.co for p in ob.data.vertices];leaves=[]
for c in ct['components']:
 if c['kind']!='leaf':continue
 pts=[v[i] for i in c['vertices']];a,w,t=[Vector(x) for x in c['axes']];base=pts[0];coords=[[float((p-base).dot(axis)) for axis in (a,w,t)] for p in pts];mx=max(x[0] for x in coords);tips=[x for x in coords if mx-x[0]<1e-7];leaves.append({'tag':c['tag'],'vertex_count':len(pts),'coordinates_axial_width_thickness_m':coords,'terminal_vertex_count':len(tips),'terminal_width_m':max(x[1] for x in tips)-min(x[1] for x in tips)})
r={'asset_id':aid,'source_sha256':H(src),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'method':'Actual reopened transformed mesh vertices projected into frozen per-organ axes; no source rewrite or reexport. Six-vertex leaves use a planar four-corner pointed diamond outline and a top/bottom thickness vertex, without an axial bend station.','leaf_count':len(leaves),'single_point_tips':sum(x['terminal_vertex_count']==1 for x in leaves),'leaves':leaves}
(Q/aid/'targeted-leaf-outline.json').write_text(json.dumps(r,indent=2)+'\n');print(aid,r['leaf_count'],r['single_point_tips'])
