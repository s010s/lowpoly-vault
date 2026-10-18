# SPDX-License-Identifier: MIT
import sys,json,hashlib
from pathlib import Path
import bpy
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'lib'))
from asset_common import audit_source,setup_scene,link_object
from qa_glb import audit_glb
p=Path(sys.argv[sys.argv.index('--')+1]).resolve();s=p.name
bpy.ops.wm.open_mainfile(filepath=str(p/(s+'.blend')))
source=audit_source(bpy.data.collections['EXPORT'],14000)
errors=list(source['errors'])
if any(o.type in ('CAMERA','LIGHT') or o.name.startswith('_preview') for o in bpy.data.objects):errors.append('Preview helper leaked into editable source')
report={'source_reopen':{'status':'pass' if not errors else 'fail','errors':errors,'metrics':source},'glb_sha256':hashlib.sha256((p/(s+'.glb')).read_bytes()).hexdigest()}
c=setup_scene('roundtrip');before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(p/(s+'.glb')))
for o in set(bpy.data.objects)-before:link_object(o,c,parent=False)
bpy.context.view_layer.update();rt=audit_source(c,14000);ex=audit_glb(p/(s+'.glb'),14000,6,30);b=rt['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]];delta=max(abs(ex['bounds_m'][k][i]-v[i]) for k,v in [('min',emin),('max',emax)] for i in range(3));er=list(rt['errors']);
if delta>1e-5:er.append('Roundtrip bounds changed')
if rt['triangles']!=ex['scene_triangles']:er.append('Roundtrip triangles changed')
report['glb_roundtrip']={'status':'pass' if not er else 'fail','errors':er,'warnings':rt['warnings'],'triangles':rt['triangles'],'bounds_max_error_m':delta};report['status']='pass' if not errors and not er else 'fail';(p/'source-roundtrip.report.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status']);
if report['status']!='pass':raise RuntimeError('verification failed')
