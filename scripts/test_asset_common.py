# SPDX-License-Identifier: MIT
"""Run with: blender --background --factory-startup --python-exit-code 1 --python scripts/test_asset_common.py

Only temporary fixtures are produced. Multi-mesh rendering catches depsgraph
lifetime errors that a one-object export smoke test cannot reveal.
"""
from pathlib import Path
import json
import sys
import tempfile

sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from asset_common import setup_scene,make_material,mesh_object,export_asset,ground_asset

FACES=[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]


def build(output,render):
    collection=setup_scene('pipeline-fixture',seed=42)
    material=make_material('fixture-clay','#79624B')
    for index in range(3):
        x=index*0.9-0.9
        h=0.5+index*0.25
        vertices=[(x-.3,-.4,2),(x+.3,-.4,2),(x+.3,.4,2),(x-.3,.4,2),
                  (x-.3,-.4,2+h),(x+.3,-.4,2+h),(x+.3,.4,2+h),(x-.3,.4,2+h)]
        mesh_object('fixture-part-'+str(index),vertices,FACES,material,collection)
    ground_asset(collection)
    return export_asset('pipeline-fixture',{'en':'Pipeline QA fixture','zh':'管线测试夹具'},'test',collection,
        metadata={'description':{'en':'Temporary QA geometry.','zh':'临时测试几何。'}},output_root=output,
        render=render,views=('hero','front','side','rear','top'),resolution=128,samples=1)


with tempfile.TemporaryDirectory(prefix='lowpoly-pipeline-test-') as temporary:
    base=Path(temporary)
    first=build(base/'first',True)
    folder=base/'first'/'pipeline-fixture'
    qa=json.loads((folder/'qa.json').read_text())
    assert qa['source']['errors']==[] and qa['glb']['errors']==[],qa
    assert first['triangles']==36,first['triangles']
    assert qa['bounds_roundtrip_max_error_m']<1e-6
    for view in ('hero','reversehero','front','side','rear','top','silhouette','clay','clay-alt','wireframe'):
        assert (folder/f'preview-{view}.png').is_file(),view
    assert bpy.data.collections.get('_PREVIEW_ONLY') is None
    assert not any(obj.type in {'CAMERA','LIGHT'} for obj in bpy.context.scene.objects)
    second=build(base/'second',False)
    assert first['sha256']['glb']==second['sha256']['glb'],'GLB rebuild changed'
    bpy.ops.wm.open_mainfile(filepath=str(folder/'pipeline-fixture.blend'))
    assert bpy.data.collections.get('_PREVIEW_ONLY') is None
    assert not any(obj.type in {'CAMERA','LIGHT'} for obj in bpy.context.scene.objects)
    assert bpy.context.scene.unit_settings.scale_length==1.0
    print('ASSET_COMMON_TEST_PASSED: 3 meshes; 36 triangles; 10 preview modes; exact bounds; deterministic GLB; clean editable blend')
