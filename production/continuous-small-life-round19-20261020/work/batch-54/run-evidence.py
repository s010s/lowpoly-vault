# SPDX-License-Identifier: MIT
import pathlib,json,shutil,subprocess,datetime
R=pathlib.Path.cwd();B=R/'production/continuous-small-life-round19-20261020/work/batch-54';A=R/'assets/candidates/continuous-small-life-round19-20261020/batch-54'
for d in sorted(A.glob('*/r002')):
 s=d.parent.name;at=list((B/'runs/build'/s/'r002/build-r002').glob('*/*'))[0]
 result=json.loads((at/'result.json').read_text());assert result['status']=='succeeded',result
 for f in (at/'outputs'/s).iterdir():shutil.copy2(f,d/f.name)
 shutil.copy2(d/'qa.json',d/'build-qa.json');m=json.loads((d/'metadata.json').read_text());m.update(glb=str((d/(s+'.glb')).relative_to(R)),blend=str((d/(s+'.blend')).relative_to(R)),preview=str((d/'proof/hero.png').relative_to(R)),nominal_design_envelope_blender_xyz_m=json.loads((d/'build-config.json').read_text())['nominal_design_envelope_blender_xyz_m'],measurement_note='Nominal artistic design envelope calibrated to actual Blender XYZ. GLB XYZ axes converted separately; not natural specimen measurement.');(d/'metadata.json').write_text(json.dumps(m,indent=2)+'\n');print(s,m['blender_dimensions_m'],flush=True)
subprocess.run(['node','scripts/validate_gltf.cjs',str(A)],check=True)
for name,root in [('proof-jobs-r002','proof-runs'),('source-jobs-r002','source-runs'),('rebuild-jobs-r002','rebuild-runs')]:
 p=subprocess.run(['python3','scripts/run_asset_queue.py',str(B/(name+'.json')),'--runs-root',str(B/root),'--workers','1','--threads','2']);print(name,p.returncode,flush=True)
