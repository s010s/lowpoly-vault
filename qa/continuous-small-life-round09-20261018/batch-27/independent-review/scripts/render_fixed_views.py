import bpy, sys, json, hashlib
from pathlib import Path

glb_path=Path(sys.argv[sys.argv.index('--')+1]).resolve()
output_dir=Path(sys.argv[sys.argv.index('--')+2]).resolve()
asset_id=sys.argv[sys.argv.index('--')+3]
helper_dir=Path(sys.argv[sys.argv.index('--')+4]).resolve()
sys.path.insert(0,str(helper_dir))
from asset_common import setup_scene, link_object, render_previews

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

views=('hero','reversehero','front','side','rear','top','clay','silhouette')
output_dir.mkdir(parents=True,exist_ok=True)
collection=setup_scene(asset_id+'-independent-qa')
before=set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(glb_path))
for obj in set(bpy.data.objects)-before: link_object(obj,collection,parent=False)
files=render_previews(collection,output_dir,views=views,resolution=512,samples=16,transparent=False)
manifest={'asset_id':asset_id,'source_glb_sha256':sha(glb_path),'blender_version':bpy.app.version_string,'render_engine':'Cycles CPU','threads':2,'samples':16,'resolution_px':[512,512],'fixed_views':list(views),'turntable_frames':0,'preview_helper_sha256':sha(helper_dir/'asset_common.py'),'images':[{'path':Path(f).name,'sha256':sha(f),'bytes':Path(f).stat().st_size} for f in files]}
(output_dir/'render-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest))
