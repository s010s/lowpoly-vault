import pathlib,json,shutil,datetime
W=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-20261020');P=W/'production/batch91-archaeopteris-repair';E=pathlib.Path('/workspace/shared/lowpoly-batch91-archaeopteris-repair-evidence');D=P/'archaeopteris/r002'
r=list((E/'build-queue/build').rglob('result.json'));assert len(r)==1 and json.loads(r[0].read_text())['status']=='succeeded';src=r[0].parent/'outputs/archaeopteris';shutil.copytree(src,D/'artifacts')
s=pathlib.Path('/workspace/shared/lowpoly-batch91-independent-qa-20261020/reopen_reexport.py').read_text().replace("ROOT=Path('/workspace/shared/lowpoly-batch91-20261020')","ROOT=Path(__file__).resolve().parents[3]")
s=s.replace("(out/'reopen-reexport.report.json').write_text", """# Additional actual world-space measurements and immutable r001 differential.
r['normalization']=json.loads(bpy.context.scene['repair_normalization'])
leafcomps=[c for c in comps if c.get('leaf_base_tip_length_m')]
verts=[o.matrix_world@v.co for o in col.all_objects if o.type=='MESH' for v in o.data.vertices]
connections=[]
for c in leafcomps:
 first=c['first_vertex'];spray=max(x['first_vertex'] for x in comps if x['vertices']==15 and x['first_vertex']<first)
 centers=[sum((verts[spray+5*k+j] for j in range(5)),Vector())/5 for k in range(3)]
 axis=centers[2]-centers[0];base=verts[first];tt=(base-centers[0]).dot(axis)/axis.length_squared;distance=(base-(centers[0]+axis*tt)).length
 connections.append({'first_vertex':first,'spray_first_vertex':spray,'axis_fraction':tt,'base_axis_distance_m':distance,'length_m':c['leaf_base_tip_length_m'],'width_m':c['leaf_width_m'],'width_to_length':c['leaf_width_m']/c['leaf_base_tip_length_m'],'thickness_m':c['leaf_thickness_m']})
r['leaf_connections']=connections
r['leaf_measurements']['width_to_length_range']=[min(x['width_to_length'] for x in connections),max(x['width_to_length'] for x in connections)]
r['leaf_measurements']['maximum_base_axis_distance_m']=max(x['base_axis_distance_m'] for x in connections)
r['leaf_measurements']['float_tolerance_m']=1e-6
r['leaf_measurements']['strict_outside_nominal_float_count']=sum(x['length_m']<.15 or x['length_m']>.23 for x in connections)
r['measured_component_counts']={str(k):v for k,v in collections.Counter((c['vertices'],c['faces']) for c in comps).items()}
r['measured_parameter_interpretations']={'leaf_length_range_m':'Hard final meter range, measured above; tolerance only 1e-6m float precision.','leaf_width_to_length':'Actual side vertex separation divided by actual base-tip length.','leaf_thickness_m':'Actual peak-to-peak local normal separation; preserves 0.009m.','normalized_total_height_m':'Hard final 3.8m height.','trunk_base_diameter_m':'Original construction section before basal flare x1.33 and skeleton normalization. Actual basal ring maximum chord is measured.','trunk_top_height_m':'Original centerline input before skeleton normalization; not total tree height.','root_radius_m':'Original radial envelope input times per-root .84+.14*sin(j*2.2), then skeleton normalization; actual tips are measured.'}
r['actual_skeleton_dimensions']={'trunk_base_flared_max_chord_m':max((a-b).length for a in verts[:10] for b in verts[:10]),'trunk_centerline_height_m':(sum(v.z for v in verts[110:120])-sum(v.z for v in verts[:10]))/10,'root_tip_center_xy_radii_m':[]}
for c in comps:
 if c['vertices']==24:
  first=c['first_vertex'];center=sum((verts[first+18+j] for j in range(6)),Vector())/6;r['actual_skeleton_dimensions']['root_tip_center_xy_radii_m'].append(math.hypot(center.x,center.y))
old=Path('/workspace/shared/lowpoly-batch91-20261020/production/small-life-batch91/archaeopteris/r001/artifacts/archaeopteris.blend');oldsha=sha(old)
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False);bpy.context.view_layer.update();ov=[o.matrix_world@v.co for o in bpy.data.objects if o.type=='MESH' for v in o.data.vertices];assert len(ov)==len(verts)
li={c['first_vertex']+j for c in leafcomps for j in range(8)};scale_ratio=r['normalization']['skeleton_scale']/r['normalization']['old_scale']
r['r001_difference']={'source_sha256':oldsha,'source_unchanged':sha(old)==oldsha,'same_vertex_count':True,'max_vertex_displacement_m':max((a-b).length for a,b in zip(verts,ov)),'max_nonleaf_displacement_m':max((verts[i]-ov[i]).length for i in range(len(verts)) if i not in li),'max_skeleton_expected_uniform_scale_error_m':max((verts[i]-ov[i]*scale_ratio).length for i in range(len(verts)) if i not in li),'max_leaf_base_expected_uniform_scale_error_m':max((verts[c['first_vertex']]-ov[c['first_vertex']]*scale_ratio).length for c in leafcomps),'max_leaf_axis_direction_change_rad':max((verts[c['first_vertex']+3]-verts[c['first_vertex']]).angle(ov[c['first_vertex']+3]-ov[c['first_vertex']]) for c in leafcomps),'note':'Only blade dimensions and the analytically necessary common skeleton scale change. No topology, component counts, palette or orientation design change.'}
assert len(leafcomps)==576 and r['leaf_measurements']['over_frozen_max_0_23']==0 and r['leaf_measurements']['under_frozen_min_0_15']==0
assert all(abs(x['thickness_m']-.009)<1e-6 and abs(x['width_to_length']-.62)<1e-5 for x in connections)
assert r['leaf_measurements']['maximum_base_axis_distance_m']<1e-6
(out/'reopen-reexport.report.json').write_text""")
(P/'tools/measure_repair.py').write_text(s)
base=['/usr/bin/flock','/tmp/lowpoly-production-blender.lock','/usr/bin/blender','--background','--threads','2','--factory-startup','--disable-autoexec','--python-exit-code','1','--python']
jobs=[{'asset_id':'archaeopteris','revision':'r002','job_id':'diagnostic-measure-reopen','argv':base+['{input:checker}','--','{input:source}','{output_dir}'],'inputs':{'checker':str(P/'tools/measure_repair.py'),'source':str(D/'artifacts/archaeopteris.blend'),'glb':str(D/'artifacts/archaeopteris.glb'),'old_source':'/workspace/shared/lowpoly-batch91-20261020/production/small-life-batch91/archaeopteris/r001/artifacts/archaeopteris.blend',**{f:str(W/'scripts'/(f+'.py')) for f in ['asset_common','qa_glb','check_source_export','check_reproducibility']}},'outputs':['reopen-reexport.report.json','archaeopteris-reexport.glb'],'timeout_seconds':1800},{'asset_id':'archaeopteris','revision':'r002','job_id':'diagnostic-shape','argv':base+['{input:renderer}','--','{input:glb}','--output-dir','{output_dir}','--revision','r002-diagnostic','--resolution','256','--samples','8','--turntable-frames','0','--views','hero,top,silhouette'],'inputs':{'renderer':str(P/'tools/render.py'),'glb':str(D/'artifacts/archaeopteris.glb'),'asset_common':str(W/'scripts/asset_common.py'),'qa_glb':str(W/'scripts/qa_glb.py')},'outputs':['hero.png','top.png','silhouette.png','render-manifest.json'],'timeout_seconds':1800}]
(E/'diagnostic-jobs.json').write_text(json.dumps({'schema_version':1,'lane':'preview','jobs':jobs},indent=2)+'\n')
(E/'recovery-progress.json').write_text(json.dumps({'stage':'build_succeeded','host_recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'initial_build_result':str(r[0]),'next':'Queued actual source measurement and low-cost actual three-view diagnostic.'},indent=2)+'\n')
