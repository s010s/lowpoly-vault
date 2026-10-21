import bpy,json,pathlib,sys,os,datetime,math
from mathutils import Vector
W=pathlib.Path('/workspace/shared/lowpoly-batch103-20261021');O=pathlib.Path('/workspace/shared/lowpoly-batch103-independent-qa-20261021');a=sys.argv[sys.argv.index('--')+1];B=W/'production/small-life-batch103'/a/'r001';bpy.ops.wm.open_mainfile(filepath=str(B/'artifacts'/f'{a}.blend'),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ct=json.loads(bpy.data.texts['BATCH103_COMPONENT_CONTRACT.json'].as_string());o=bpy.data.objects[ct['object_name']];v=[o.matrix_world@x.co for x in o.data.vertices];cs=ct['components'];groups={c['tag']:c for c in cs};out={'asset':a,'pid':os.getpid(),'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_untouched':True};allsize=[max(q[k]for q in v)-min(q[k]for q in v)for k in range(3)];out['whole_size_m']=allsize
if a=='habelia':
 pts=[v[i]for c in cs if c['kind']in ['head_shield','trunk_tergite']for i in c['vertices']];body=max(q.y for q in pts)-min(q.y for q in pts);length=[]
 for name in ['telson_proximal','telson_distal']:
  pts=[v[i]for i in groups[name]['vertices']];length.append(max(q.y for q in pts)-min(q.y for q in pts))
 out.update(head_trunk_m=body,telson_component_spans_m=length,telson_to_body_ratio=sum(length)/body,proximal_to_distal_ratio=length[0]/length[1])
if a=='plenocaris':
 out['antennae']=[]
 for s in [-1,1]:
  c=groups[f'antenna{s}'];pts=[v[i]for i in c['vertices']];rings=[pts[k*6:(k+1)*6]for k in range(11)];centers=[sum(r,Vector())/6 for r in rings];radii=[sum((q-z).length for q in r)/6 for r,z in zip(rings,centers)];axis=(centers[-1]-centers[0]).normalized();line_dev=max(((z-centers[0])-axis*(z-centers[0]).dot(axis)).length for z in centers);linear_residual=max(abs(radii[k]-(radii[0]+(radii[-1]-radii[0])*k/10))for k in range(11));slopes=[(radii[k+1]-radii[k])/(centers[k+1]-centers[k]).length for k in range(10)]
  mats=set(p.material_index for p in o.data.polygons if set(p.vertices)<=set(c['vertices']));out['antennae'].append({'tag':c['tag'],'topological_intervals':10,'ring_centers_m':[list(q)for q in centers],'ring_radii_m':radii,'radius_slopes':slopes,'centerline_straight_residual_m':line_dev,'linear_taper_residual_m':linear_residual,'material_indices':list(mats),'observation':'Ten subdivisions of one straight linearly tapered tube, without joints, annular relief, bends or segment material distinction. This explains unsegmented appearance in exact final head detail.'})
if a=='nectocaris':
 c=groups['flared_mouth'];p=[v[i]for i in c['vertices']];centers=[sum(p[k*12:(k+1)*12],Vector())/12 for k in range(4)];out['mouth']={'opening_radius_m':sum((q-centers[2]).length for q in p[24:36])/12,'lumen_depth_m':(centers[2]-centers[3]).length}
 out['fins']=[]
 for s in [-1,1]:
  p=[v[i]for i in groups[f'fin{s}']['vertices']];zs=[p[i*3+1].z for i in range(29)];out['fins'].append({'tag':f'fin{s}','transverse_ridges':sum(zs[i]<zs[i-1] and zs[i]<zs[i+1]for i in range(1,28)),'lower_layer_center_z_m':zs})
(O/a/'feature-audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
