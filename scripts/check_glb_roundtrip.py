# SPDX-License-Identifier: MIT
"""Fresh Blender import/bounds check plus isolated export-artifact previews.

blender -b --factory-startup --python-exit-code 1 --python scripts/check_glb_roundtrip.py -- model.glb
This is a Blender roundtrip test, never a substitute for Three.js verification.
"""
import argparse
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from asset_common import setup_scene,link_object,audit_source,render_previews
from qa_glb import audit_glb

args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('glb',type=Path)
p.add_argument('--output-dir',type=Path)
p.add_argument('--samples',type=int,default=32)
p.add_argument('--resolution',type=int,default=512)
p.add_argument('--no-render',action='store_true')
a=p.parse_args(args)
glb=a.glb.resolve(); output=(a.output_dir or glb.parent).resolve(); output.mkdir(parents=True,exist_ok=True)
exported=audit_glb(glb,max_triangles=10**9,max_materials=10**6,max_primitives=10**6)
if exported['errors']: raise RuntimeError('GLB static audit failed: '+repr(exported['errors']))
collection=setup_scene('roundtrip-fixture')
root=bpy.data.objects[collection['asset_root']]
before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(glb))
imported=[obj for obj in bpy.data.objects if obj not in before]
for obj in imported: link_object(obj,collection,parent=False)
for obj in imported:
    if obj.parent not in imported:
        matrix=obj.matrix_world.copy(); obj.parent=root; obj.matrix_world=matrix
bpy.context.view_layer.update()
source=audit_source(collection,max_triangles=10**9)
errors=list(source['errors'])
bounds=source['bounds_blender_m']
expected_min=[bounds['min'][0],bounds['min'][2],-bounds['max'][1]]
expected_max=[bounds['max'][0],bounds['max'][2],-bounds['min'][1]]
delta=max(abs(exported['bounds_m'][side][i]-expected[i]) for side,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
if delta>0.0001: errors.append(f'Imported bounds mismatch: {delta} m')
if source['triangles']!=exported['scene_triangles']: errors.append('Imported triangle count changed')
report={'status':'fail' if errors else 'pass_with_warnings' if source['warnings'] else 'pass','viewer':'Blender glTF importer','blender_version':bpy.app.version_string,
        'glb_sha256':exported['sha256'],'semantic_sha256':exported['semantic_sha256'],
        'errors':errors,'warnings':source['warnings'],'triangles':source['triangles'],'bounds_max_error_m':delta,
        'previews':[],'visual_review':'pending'}
if not errors and not a.no_render:
    with tempfile.TemporaryDirectory(prefix='.roundtrip-',dir=output) as temporary:
        rendered=render_previews(collection,temporary,views=('hero','wireframe'),resolution=a.resolution,samples=a.samples)
        for rendered_file in rendered:
            source_path=Path(rendered_file)
            filename='preview-glb-roundtrip.png' if source_path.name=='preview-hero.png' else 'preview-glb-wireframe.png'
            source_path.replace(output/filename); report['previews'].append(filename)
(output/'glb-roundtrip.report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(report,ensure_ascii=False))
if errors: raise RuntimeError('GLB roundtrip failed')
