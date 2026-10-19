# SPDX-License-Identifier: MIT
"""Collect immutable queue evidence without claiming independent acceptance."""
import json,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/check_reproducibility.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from check_reproducibility import compare_rebuild,write_new_report
for revision in ('r001','r002','r003'):
 for s in ['emeraldella','burgessia','tuzoia','sanctacaris']:
    if revision=='r003' and s!='tuzoia':continue
    d=HERE/s/revision
    results=list((HERE/'render-runs/render'/s/revision).rglob('result.json'))
    for r in results:
        if json.loads(r.read_text())['status']!='succeeded':continue
        if not (d/'proof').exists():shutil.copytree(r.parent/'outputs',d/'proof')
    for i in (1,2):
        r=next((HERE/'rebuild-runs/build'/s/revision/('rebuild-'+str(i))).rglob('result.json'),None)
        if not r or json.loads(r.read_text())['status']!='succeeded':continue
        out=d/('reproducibility-'+str(i)+'.json')
        if out.exists():continue
        generator=HERE/({'r001':'generator.py','r002':'generator-r002.py','r003':'generator-r003.py'}[revision])
        report=compare_rebuild(d/(s+'.glb'),r.parent/'outputs'/(s+'.glb'),generator,d/'build-config.json',r.parent/'request.json',r,s+'.glb',REPO)
        write_new_report(out,report);print(s,revision,'rebuild',i,report['status'],flush=True)
