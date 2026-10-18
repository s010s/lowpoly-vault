# SPDX-License-Identifier: MIT
"""Fresh import of exact GLB; eight fixed views and transparent hero."""
import argparse,hashlib,json,sys,time
from pathlib import Path
import bpy
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,link_object,render_previews,audit_source
from qa_glb import audit_glb
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--glb',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--brief',type=Path,required=True);p.add_argument('--references',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output_dir.mkdir(parents=True,exist_ok=True)
if list(a.output_dir.glob('*.png')):raise RuntimeError('Immutable view attempt required')
c=setup_scene('exact-glb-render');root=bpy.data.objects[c['asset_root']];before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(a.glb.resolve()))
imported=[o for o in bpy.data.objects if o not in before]
for o in imported:link_object(o,c,parent=False)
for o in imported:
    if o.parent not in imported:
        matrix=o.matrix_world.copy();o.parent=root;o.matrix_world=matrix
bpy.context.view_layer.update();audit=audit_source(c,14000);glb=audit_glb(a.glb,14000,6,30)
if audit['errors'] or audit['triangles']!=glb['scene_triangles']:raise RuntimeError(repr(audit))
start=time.monotonic();views=('hero','reversehero','front','side','rear','top','clay','silhouette')
files=render_previews(c,a.output_dir,views=views,resolution=512,samples=16,transparent=True)
record={'schema_version':1,'kind':'exact_glb_eight_fixed_views','glb_sha256':sha(a.glb),'brief_sha256':sha(a.brief),'references_sha256':sha(a.references),'renderer_sha256':sha(__file__),'helper_sha256':sha(ROOT/'scripts/asset_common.py'),'blender':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'samples':16,'resolution':512,'silhouette_resolution':128,'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'turntable_frames':0,'wall_seconds':time.monotonic()-start,'reimport_audit':audit,'frames':[{'view':v,'path':Path(f).name,'bytes':Path(f).stat().st_size,'sha256':sha(f)} for v,f in zip(views,files)],'visual_review':'pending; generation is not acceptance'}
(a.output_dir/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
