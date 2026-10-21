import ast,math,json,pathlib,copy,sys,hashlib
O=pathlib.Path(__file__).parent;R=pathlib.Path('/workspace/shared/lowpoly-batch82-stratovolcano-repair-20261020');P=R/'production/batch82-stratovolcano-repair/stratovolcano/r009';A=pathlib.Path('/workspace/shared/lowpoly-batch82-20261020/production/small-life-batch82/assets/stratovolcano/r006');J=lambda p:json.loads(p.read_text())
sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from qa_glb import audit_glb,read_glb,accessor_values
# Extract only pure geometric stratovolcano functions. No Blender context or original file writes.
def capture(path,cfg):
 tree=ast.parse(path.read_text());fn=copy.deepcopy(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='stratovolcano'))
 fn.body=[n for n in fn.body if not (isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='write_text')]
 got={}
 def ring_surface(name,n,rings,point,matfn,topz):got.update(n=n,rings=rings,point=point,topz=topz);return {}
 env={'math':math,'cfg':cfg,'ring_surface':ring_surface,'json':json}
 exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),env);env['stratovolcano']();return got
old=capture(A/'generator.py',J(A/'build-config.json'));new=capture(P/'generator.py',J(P/'build-config.json'))
def size(g,n=None):
 n=n or g['n'];pts=[g['point'](r,z,math.tau*i/n,j) for j,(r,z) in enumerate(g['rings']) for i in range(n)];pts+=[(0,0,0),(0,0,g['topz'])];return [max(p[i] for p in pts)-min(p[i] for p in pts) for i in range(3)]
sourceold=J(A/'metrics.json')['source']['bounds_blender_m'];sourcenew=J(O/'saved-source/source-reexport.report.json')['source_audit']['bounds_blender_m'];delta=[b-a for a,b in zip(sourceold['size'],sourcenew['size'])]
old96=size(old);old144=size(old,144);new144=size(new)
boundary=[]
for r in [1,.093,.061,.043,.018]:
 jo=next(j for j,(rr,z) in enumerate(old['rings']) if rr==r);jn=next(j for j,(rr,z) in enumerate(new['rings']) if rr==r);zo=old['rings'][jo][1];zn=new['rings'][jn][1]
 diffs=[max(abs(a-b) for a,b in zip(old['point'](r,zo,math.tau*i/48,jo),new['point'](r,zn,math.tau*i/48,jn))) for i in range(48)];boundary.append({'normalized_radius':r,'common_angular_samples':48,'maximum_coordinate_delta_m':max(diffs)})
check=all(x['maximum_coordinate_delta_m']<1e-7 for x in boundary) and all(abs(a-b)<.001 for a,b in zip(new144,sourcenew['size'])) and all(abs(a-b)<1e-7 for a,b in zip(old144,new144))
# Exact exported material/texture comparison, independently decoded geometry bounds.
doc0,bin0,_=read_glb(A/'model.glb');doc1,bin1,_=read_glb(P/'model.glb')
metrics0=audit_glb(A/'model.glb',14000,6,30);metrics1=audit_glb(P/'model.glb',14000,6,30)
graph=J(P/'flank-network.json')['channels'];kinds={k:sum(x['kind']==k for x in graph) for k in set(x['kind'] for x in graph)}
rc0=J(A/'proof-final/render-config.json');rc1=J(P/'proof-final/render-config.json')
lightscale=(rc1['orthographic_scale']/rc0['orthographic_scale'])**2
report={'created_at':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'method':'Independent numeric evaluation of geometric function AST, excluding all top-level execution and file writes; crosschecked actual saved-source and GLB decoded bounds. Shared 48 angle boundary samples directly compared.','old_angular_samples':old['n'],'new_angular_samples':new['n'],'old_measured_blender_xyz_m':sourceold['size'],'new_measured_blender_xyz_m':sourcenew['size'],'measured_delta_m':delta,'relative_percent':[100*d/a for d,a in zip(delta,sourceold['size'])],'analytic_old_at96':old96,'analytic_old_at144':old144,'analytic_new_at144':new144,'original_profile_resampled_at144_reproduces_new_bounds':check,'boundary_and_vent_common_angle_tests':boundary,'explanation':'Outer-foot and vent coordinate formulas are unchanged at common angular samples. The original boundary evaluated at144 rather than96 angles predicts all three new dimensions; float32 rounding accounts for less than0.001m residual. Incision and jitter do not determine overall extrema. This is sampling drift, not a scale change. Local flank silhouette intentionally changes under incisions; it is not claimed pixel-identical.','materials_exactly_identical':doc0.get('materials')==doc1.get('materials'),'textures_exactly_identical':doc0.get('textures',[])==doc1.get('textures',[]),'old_export':metrics0,'new_export':metrics1,'authored_channel_counts':kinds,'camera_same_angles':[(x['view'],x['angle_degrees']) for x in rc0['frames']]==[(x['view'],x['angle_degrees']) for x in rc1['frames']],'ortho_scale_percent_difference':100*(rc1['orthographic_scale']/rc0['orthographic_scale']-1),'light_scaling_explanation':'Radius-dependent light energy follows the identical original renderer algorithm. Expected energy ratio equals square of framing radius ratio.','expected_light_energy_ratio':lightscale,'actual_light_energy_ratios':[b['energy']/a['energy'] for a,b in zip(rc0['lights'],rc1['lights'])],'renderer_color_sampling_unchanged':{k:rc0[k]==rc1[k] for k in ['renderer','engine','samples','resolution','denoising','view_transform','look','exposure','gamma','background','camera_type','base_pose_deg','elevation_deg']}}
(O/'geometry-regression-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['old_export','new_export']},indent=2));assert check;assert report['materials_exactly_identical'];assert all(report['renderer_color_sampling_unchanged'].values())
