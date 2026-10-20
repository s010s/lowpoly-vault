# SPDX-License-Identifier: MIT
import pathlib,subprocess,json,shutil
R=pathlib.Path.cwd();B=R/'production/continuous-small-life-round19-20261020/work/batch-54';A=R/'assets/candidates/continuous-small-life-round19-20261020/batch-54'
def queue(name,root):subprocess.run(['python3','scripts/run_asset_queue.py',str(B/(name+'-r003.json')),'--runs-root',str(B/root),'--workers','1','--threads','2'],check=True)
queue('build-jobs','runs')
for s in ['didymoceras','spirematospermum']:
 d=A/s/'r003';at=list((B/'runs/build'/s/'r003/build-r003').glob('*/*'))[0]
 for f in (at/'outputs'/s).iterdir():shutil.copy2(f,d/f.name)
 shutil.copy2(d/'qa.json',d/'build-qa.json');m=json.loads((d/'metadata.json').read_text());m.update(glb=str((d/(s+'.glb')).relative_to(R)),blend=str((d/(s+'.blend')).relative_to(R)),preview=str((d/'proof/hero.png').relative_to(R)),nominal_design_envelope_blender_xyz_m=json.loads((d/'build-config.json').read_text())['nominal_design_envelope_blender_xyz_m'],measurement_note='Actual XYZ bounds calibrated to nominal artistic envelope; no natural specimen measurement asserted.');(d/'metadata.json').write_text(json.dumps(m,indent=2)+'\n');subprocess.run(['node','scripts/validate_gltf.cjs',str(d/(s+'.glb'))],check=True)
for name,root in [('proof-jobs','proof-runs'),('source-jobs','source-runs'),('rebuild-jobs','rebuild-runs')]:queue(name,root)
