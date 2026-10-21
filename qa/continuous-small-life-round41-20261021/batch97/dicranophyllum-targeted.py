import pathlib,sys
P=pathlib.Path(__file__).parent
s=(P/'inspect_source.py').read_text();exec(compile(s.split('records=[];relations=')[0],str(P/'inspect_source.py'),'exec'))
# Dense original cushion surface sampling; no source modification.
results=[]
for tag,ids in groups.items():
 if not tag.startswith('cushion_'):continue
 witnesses=[];outside_parent=0;tests=0;nearest_blockers=collections.Counter();max_radial=0
 for ti in tby[tag]:
  a,b,c=[v[i] for i in tris[ti]];normal=(b-a).cross(c-a).normalized()
  for ia in range(1,12):
   for ib in range(1,12-ia):
    u=ia/12;w=ib/12;p=a*u+b*w+c*(1-u-w)
    if signed(p,trees['slender_axis'])<=eps:continue
    outside_parent+=1
    for ray in [normal,*directions]:
     if ray.dot(normal)<=.05:continue
     tests+=1;hit,_,idx,dist=whole.ray_cast(p+ray*eps,ray,extent*4)
     if idx is None:witnesses.append({'triangle':ti,'barycentric':[u,w,1-u-w],'point':list(p),'direction':list(ray)});break
     nearest_blockers[owner[tris[idx][0]]]+=1
 results.append({'tag':tag,'sample_grid_denominator':12,'outside_parent_samples':outside_parent,'visibility_rays_tested':tests,'visible_samples':len(witnesses),'first_visible_witness':witnesses[0] if witnesses else None,'blocker_counts':dict(nearest_blockers)})
(out/'cushion-dense-exposure.json').write_text(json.dumps({'source_sha256':H(src),'glb_sha256':H(glb),'pid':os.getpid(),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Grid barycentric samples on all8 actual triangular cushion faces. Test outside actual stem, then normal plus10 directions against entire exact mesh. No negative sample result alone is proof of complete burial.','items':results,'no_visible_sample':[x['tag'] for x in results if not x['visible_samples']]},indent=2)+'\n')
print('Dense cushion visible',sum(x['visible_samples']>0 for x in results),'of',len(results),flush=True)
# Every twice-forked leaf, unchanged actual source triangle subset. Diagnostic only, not full-asset acceptance.
from asset_common import _look_at
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=False;scene.render.resolution_x=scene.render.resolution_y=256;scene.render.resolution_percentage=100;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
for o in list(bpy.data.objects):
 if o.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(o,do_unlink=True)
world=bpy.data.worlds.new('independent-world');world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.8,.8,.8,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5;scene.world=world
camd=bpy.data.cameras.new('independent-camera');cam=bpy.data.objects.new('independent-camera',camd);scene.collection.objects.link(cam);camd.type='ORTHO';camd.clip_start=.0001;camd.clip_end=10;scene.camera=cam
ld=bpy.data.lights.new('directional-key','AREA');ld.energy=15;ld.size=.35;light=bpy.data.objects.new('directional-key',ld);scene.collection.objects.link(light)
views=[];detail=out/'leaf-diagnostics';detail.mkdir(exist_ok=True)
for tag,ids in groups.items():
 if not tag.startswith('leaf_'):continue
 mapping={i:j for j,i in enumerate(ids)};faces=[tuple(mapping[q] for q in tris[i]) for i in tby[tag]];me=bpy.data.meshes.new(tag+'-unchanged-triangles');me.from_pydata([v[i] for i in ids],[],faces);me.update();isolated=bpy.data.objects.new(tag+'-diagnostic-only',me);scene.collection.objects.link(isolated)
 for mat in obj.data.materials:me.materials.append(mat)
 for p,ti in zip(me.polygons,tby[tag]):p.material_index=obj.data.loop_triangles[ti].material_index
 obj.hide_render=True;pts=np.array([v[i] for i in ids]);center=Vector(pts.mean(axis=0));cov=np.cov(pts.T);val,vec=np.linalg.eigh(cov);normal=Vector(vec[:,0]);longaxis=Vector(vec[:,-1]);normal.normalize();longaxis.normalize();cam.location=center+normal*.6;_look_at(cam,center);camd.ortho_scale=float(max(np.ptp((pts-np.array(center))@vec,axis=0)))*1.15
 light.location=center+normal*.35+Vector((-.15,-.12,.25));_look_at(light,center);f=detail/(tag+'.png');scene.render.filepath=str(f);bpy.ops.render.render(write_still=True);views.append({'tag':tag,'path':str(f),'sha256':H(f),'camera_position':list(cam.location),'target':list(center),'ortho_scale_m':camd.ortho_scale,'source_vertex_ids':ids,'source_triangle_ids':tby[tag],'diagnostic_subset_only':True});bpy.data.objects.remove(isolated,do_unlink=True);bpy.data.meshes.remove(me)
# Full source remains unhidden in closeups, aimed radial outward at original attachment sites.
obj.hide_render=False;scene.render.resolution_x=scene.render.resolution_y=512;context_views=[]
for idx in [0,9,10,23,47]:
 tag=f'cushion_{idx:02d}';pts=[v[i] for i in groups[tag]];center=sum(pts,Vector())/len(pts);rad=(pts[4]-pts[5]).normalized();cam.location=center+rad*.5+Vector((0,0,.02));_look_at(cam,center);camd.ortho_scale=.04;light.location=center+rad*.25+Vector((-.08,-.09,.12));ld.energy=4;ld.size=.12;_look_at(light,center);f=out/(tag+'-full-context.png');scene.render.filepath=str(f);bpy.ops.render.render(write_still=True);context_views.append({'tag':tag,'path':str(f),'sha256':H(f),'camera_position':list(cam.location),'target':list(center),'ortho_scale_m':camd.ortho_scale,'entire_original_mesh_visible':True})
(out/'targeted-render-manifest.json').write_text(json.dumps({'source_sha256':H(src),'glb_sha256':H(glb),'pid':os.getpid(),'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'blender':bpy.app.version_string,'renderer':'Cycles CPU','gpu':'unknown','scene':'unknown','leaf_images':views,'full_context_attachment_images':context_views,'limitations':'Isolated unchanged leaf subsets are explicitly diagnostic of fork morphology only; they cannot prove assembled leaf contact or whole-asset visibility. Full-context frames retain all exact geometry. No candidate saved or modified.'},indent=2)+'\n')
