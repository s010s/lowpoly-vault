import sys;sys.dont_write_bytecode=True
import bpy,bmesh,json,pathlib,hashlib,os,math,datetime
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
W=pathlib.Path('/workspace/shared/lowpoly-batch100-20261021');B=W/'production/small-life-batch100';Q=pathlib.Path(__file__).parent
sys.path.insert(0,str(W/'scripts'))
from qa_glb import audit_glb
from check_reproducibility import compare_rebuild
from asset_common import audit_source
A=sys.argv[sys.argv.index('--')+1];H=json.loads((B/'handoff.json').read_text());I=next(x for x in H['items']if x['asset_id']==A);P=B/A/I['revision'];O=Q/A
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest();source=W/I['editableBlend']['path'];glb=W/I['glb']['path'];before=sha(source)
bpy.context.preferences.filepaths.use_scripts_auto_execute=False
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);bpy.context.view_layer.update()
obs=[o for o in bpy.data.objects if o.type=='MESH'];dg=bpy.context.evaluated_depsgraph_get();allp=[];alltri=[];groupdata={};counts=[]
for ob in obs:
 ob.data.calc_loop_triangles();vv=[ob.matrix_world@v.co for v in ob.data.vertices];offset=len(allp);allp+=vv;tt=[tuple(t.vertices)for t in ob.data.loop_triangles];alltri += [tuple(offset+i for i in t)for t in tt]
 bm=bmesh.new();bm.from_mesh(ob.data);ev=ob.evaluated_get(dg);me=ev.to_mesh();me.calc_loop_triangles()
 counts.append({'object':ob.name,'authored_vertices':len(ob.data.vertices),'authored_faces':len(ob.data.polygons),'authored_triangles':len(tt),'evaluated_vertices':len(me.vertices),'evaluated_faces':len(me.polygons),'evaluated_triangles':len(me.loop_triangles),'modifiers':len(ob.modifiers),'boundary_edges':sum(len(e.link_faces)==1 for e in bm.edges),'nonmanifold_edges':sum(len(e.link_faces)!=2 for e in bm.edges),'matrix_world':[list(x)for x in ob.matrix_world]});bm.free();ev.to_mesh_clear()
 groups={vg.name:[]for vg in ob.vertex_groups}
 for v in ob.data.vertices:
  for x in v.groups:groups[ob.vertex_groups[x.group].name].append(v.index)
 for name,inds in groups.items():
  ids=set(inds);tr=[t for t in tt if all(i in ids for i in t)];points=np.array([vv[i]for i in inds]);lo=points.min(0);hi=points.max(0);_,ax=np.linalg.eigh(np.cov(points.T));pc=(points-points.mean(0))@ax
  edges={};adj={i:set()for i in inds}
  for t in tr:
   for u,v in zip(t,t[1:]+t[:1]):edges[tuple(sorted([u,v]))]=edges.get(tuple(sorted([u,v])),0)+1;adj[u].add(v);adj[v].add(u)
  left=set(inds);islands=[]
  while left:
   seed=min(left);left.remove(seed);todo=[seed];part=[seed]
   while todo:
    for j in adj[todo.pop()]:
     if j in left:left.remove(j);todo.append(j);part.append(j)
   islands.append(sorted(part))
  volume=sum(vv[t[0]].dot(vv[t[1]].cross(vv[t[2]]))/6 for t in tr)
  groupdata[name]={'vertices':vv,'ids':inds,'triangles':tr,'tree':BVHTree.FromPolygons(vv,tr,all_triangles=True),'islands':islands,'record':{'group':name,'vertices':len(inds),'triangles':len(tr),'connected_solids':len(islands),'world_min':lo.tolist(),'world_max':hi.tolist(),'world_size':(hi-lo).tolist(),'pca_extents':np.ptp(pc,axis=0).tolist(),'nonmanifold_edges':sum(n!=2 for n in edges.values()),'signed_volume_m3':volume}}
globaltree=BVHTree.FromPolygons(allp,alltri,all_triangles=True);bound=np.array(allp);lo=bound.min(0);hi=bound.max(0);span=float(np.max(hi-lo));eps=max(span*1e-7,1e-11)
# Three nonaxis directions and majority parity reduce edge-hit ambiguity.
def inside(pt,tree):
 votes=[]
 for d in [Vector((.381,.527,.759)).normalized(),Vector((-.413,.811,.419)).normalized(),Vector((.713,-.367,.597)).normalized()]:
  hits=0;p=pt.copy()
  for n in range(64):
   hit,_,_,dist=tree.ray_cast(p,d,span*10)
   if hit is None:break
   hits+=1;p=hit+d*eps*2
  votes.append(hits%2)
 return sum(votes)>=2
contacts=[]
for ob in obs:
 for rel in json.loads(ob.get('contact_design','[]')):
  child,parent=rel['child'],rel['parent'];c=groupdata[child];p=groupdata[parent];witness=None
  samples=[('vertex',i,c['vertices'][i])for i in c['ids']]
  samples += [('triangle_center',j,sum([c['vertices'][i]for i in t],Vector())/3)for j,t in enumerate(c['triangles'])]
  for kind,n,v in samples:
   nearest=p['tree'].find_nearest(v)
   if nearest[0] is not None and nearest[3]>eps and inside(v,p['tree']):witness={'kind':kind,'index':n,'position':list(v),'depth_to_parent_surface_m':nearest[3]};break
  contacts.append({'child':child,'parent':parent,'strict_inside_surface_witness':witness,'sample_count_available':len(samples)})
# Global visibility: every triangle is tested on a seven-point barycentric stencil, rays include all objects, not just the parent.
dirs={'front':Vector((0,-1,0)),'rear':Vector((0,1,0)),'hero':Vector((.469846,-.671010,.573576)).normalized(),'reversehero':Vector((-.469846,.671010,.573576)).normalized()}
stencil=[(1/3,1/3,1/3),(.6,.2,.2),(.2,.6,.2),(.2,.2,.6),(.45,.45,.1),(.45,.1,.45),(.1,.45,.45)]
visibility=[]
for tag,c in groupdata.items():
 if not(A=='lygodium' or (A=='chaetocladus' and tag.startswith('lateral_'))):continue
 summary={k:{'tested':0,'visible':0,'visible_area_sample_m2':0.0,'witnesses':[]}for k in dirs}
 for ti,t in enumerate(c['triangles']):
  a,b,cpt=[c['vertices'][i]for i in t];cross=(b-a).cross(cpt-a);area=cross.length*.5
  for bary in stencil:
   p=a*bary[0]+b*bary[1]+cpt*bary[2]
   for view,d in dirs.items():
    if cross.dot(d)<=0:continue
    summary[view]['tested']+=1
    hit,_,index,dist=globaltree.ray_cast(p+d*eps*2,d,span*10)
    if hit is None:
     z=summary[view];z['visible']+=1;z['visible_area_sample_m2']+=area/len(stencil)
     if len(z['witnesses'])<3:z['witnesses'].append({'triangle':ti,'barycentric':bary,'point':list(p)})
 visibility.append({'group':tag,'views':summary,'method':'Positive-area triangle interior stencil plus global ray occlusion. Samples are corroborating evidence, not a percentage pass gate.'})
fold={}
for ob in obs:
 vv=[ob.matrix_world@v.co for v in ob.data.vertices];half=len(vv)//2;front=[];back=[];zero=[]
 for t in ob.data.loop_triangles:
  ids=list(t.vertices);a,b,c=[vv[i]for i in ids];n=(b-a).cross(c-a)
  if n.length<1e-20:zero.append(t.index)
  if A in ['flabellophyton','protosalvinia']:
   if max(ids)<half:front.append(n.y)
   if min(ids)>=half:back.append(n.y)
 fold[ob.name]={'zero_area_triangles':zero,'front_triangles':len(front),'back_triangles':len(back),'reversed_front_count':sum(n>=0 for n in front),'reversed_back_count':sum(n<=0 for n in back)}
features={}
if A=='lygodium':
 for tag,c in groupdata.items():
  if tag.startswith('dichotomous_veins'):
   pieces=[]
   for island in c['islands']:
    rings=[]
    for k in range(0,len(island),4):
     points=[c['vertices'][i]for i in island[k:k+4]];inside_count=sum(inside(p,groupdata['bifid_lamina']['tree'])for p in points);rings.append({'inside':inside_count,'outside':len(points)-inside_count})
    pieces.append(rings)
   features[tag]={'segments':len(pieces),'rings':pieces}
if A=='chaetocladus':
 details=[]
 for tag,c in groupdata.items():
  if not tag.startswith('lateral_'):continue
  centers=[sum([c['vertices'][i]for i in c['ids'][k:k+3]],Vector())/3 for k in range(0,len(c['ids']),3)]
  details.append({'group':tag,'vertices':len(c['ids']),'triangles':len(c['triangles']),'solids':len(c['islands']),'rings':len(centers),'root':list(centers[0]),'tip':list(centers[-1]),'segments_m':[(centers[j+1]-centers[j]).length for j in range(len(centers)-1)]})
 features={'laterals':details,'unique_tips':len(set(tuple(round(x,10)for x in d['tip'])for d in details)),'whorl_count':len(set(x['group'].split('_')[1]for x in details))}
brief=json.loads((W/I['original_brief']['path']).read_text());ranges=brief['scale']['hard_world_bbox_size_ranges_xyz_m'];size=hi-lo
record={'asset_id':A,'source_sha256':before,'source_saved':False,'source_unchanged':sha(source)==before,'glb_sha256':sha(glb),'pid':os.getpid(),'blender_version':bpy.app.version_string,'measured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unit_scale':bpy.context.scene.unit_settings.scale_length,'counts':counts,'actual_world_bounds':{'min':lo.tolist(),'max':hi.tolist(),'size':size.tolist()},'hard_ranges':ranges,'hard_range_pass':[bool(ranges[k][0]<=size[k]<=ranges[k][1])for k in range(3)],'components':[g['record']for g in groupdata.values()],'contacts':contacts,'global_visibility':visibility,'fold_checks':fold,'features':features,'limits':'No arbitrary percent visibility threshold. Seven-point surface samples cannot prove exhaustive visibility; use with individually inspected exact final frames and targeted diagnostics.'}
(O/'geometry-contact-visibility.json').write_text(json.dumps(record,indent=2))
# Re-export freshly reopened editable source without saving or mutating it. Exactly documented exporter options, explicit selected collection.
collection=next(c for c in bpy.data.collections if c.get('asset_root'));bpy.ops.object.select_all(action='DESELECT')
for ob in collection.all_objects:ob.select_set(True)
bpy.context.view_layer.objects.active=bpy.data.objects.get(collection['asset_root'])
reexport=O/'source-reexport.glb'
bpy.ops.export_scene.gltf(filepath=str(reexport),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
comp=compare_rebuild(glb,reexport,W/I['generator']['path'],W/I['config']['path']);comp['kind']='fresh independent source reexport, not generator rebuild';comp['source_sha256']=before;comp['source_unchanged']=sha(source)==before;(O/'source-reexport-semantic.json').write_text(json.dumps(comp,indent=2))
print(json.dumps({'asset':A,'hard_range_pass':record['hard_range_pass'],'contacts':len(contacts),'missing_contact_witness':[x['child']for x in contacts if not x['strict_inside_surface_witness']],'reexport_semantic':comp['semantic_match'],'fold_checks':fold}))
