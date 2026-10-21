import pathlib,sys,json,math,hashlib,datetime
W=pathlib.Path('/workspace/shared/lowpoly-batch97-20261020');B=W/'production/small-life-batch97';O=pathlib.Path(__file__).parent;sys.path.insert(0,str(W/'scripts'));from qa_glb import read_glb,accessor_values,node_matrix,matmul,transform,IDENTITY
results=[]
for aid,rev in [('ginkgo','r002'),('dicranophyllum','r003'),('noeggerathia','r002'),('bjuvia','r001')]:
 d=B/aid/rev;p=d/'artifacts'/f'{aid}.glb';doc,binary,raw=read_glb(p);pts=[]
 def visit(i,parent):
  n=doc['nodes'][i];m=matmul(parent,node_matrix(n))
  if 'mesh' in n:
   for primitive in doc['meshes'][n['mesh']]['primitives']:
    for p in accessor_values(doc,binary,primitive['attributes']['POSITION']):
     q=transform(m,p);pts.append((q[0],-q[2],q[1]))
  for c in n.get('children',[]):visit(c,m)
 for n in doc['scenes'][doc.get('scene',0)]['nodes']:visit(n,IDENTITY)
 cfg=json.loads((d/'views/render-config.json').read_text());man=json.loads((d/'views/render-manifest.json').read_text());target=cfg['target_blender_m'];scale=cfg['orthographic_scale'];records=[]
 for frame in man['frames']:
  az,el=[math.radians(q) for q in frame['angle_degrees']];right=(math.cos(az),math.sin(az),0);up=(-math.sin(az)*math.sin(el),math.cos(az)*math.sin(el),math.cos(el));xx=[];yy=[]
  for p in pts:
   delta=[p[k]-target[k] for k in range(3)];xx.append((sum(delta[k]*right[k] for k in range(3))/scale+.5)*512);yy.append((.5-sum(delta[k]*up[k] for k in range(3))/scale)*512)
  margins=[min(xx),512-max(xx),min(yy),512-max(yy)];records.append({'frame':frame['id'],'projected_vertex_bbox_pixels':[min(xx),min(yy),max(xx),max(yy)],'margins_left_right_top_bottom_pixels':margins,'all_geometry_inside_frame':min(margins)>0})
 results.append({'asset_id':aid,'glb_sha256':hashlib.sha256(raw).hexdigest(),'frame_config_sha256':hashlib.sha256((d/'views/render-config.json').read_bytes()).hexdigest(),'frames':records,'all_pass':all(r['all_geometry_inside_frame'] for r in records)})
(O/'independent-framing.json').write_text(json.dumps({'observed_at_executor_clock':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Decode exact GLB POSITION accessors and all scene node transforms, axis-convert Y-up to source Z-up, apply published fixed-orbit orthographic basis per frame and target/scale. All actual vertices, not AABB corners.','assets':results},indent=2)+'\n');print([(r['asset_id'],r['all_pass'],min(min(x['margins_left_right_top_bottom_pixels']) for x in r['frames'])) for r in results])
