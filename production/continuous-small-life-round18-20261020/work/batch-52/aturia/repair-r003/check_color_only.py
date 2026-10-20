# SPDX-License-Identifier: MIT
"""Compare exact baseline/revision GLBs; allowed differences are one RGB factor and its sRGB metadata."""
import argparse,hashlib,json,struct
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('baseline',type=Path);p.add_argument('revision',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 b=p.read_bytes(); assert b[:4]==b'glTF'; n=struct.unpack_from('<I',b,12)[0]; return json.loads(b[20:20+n]),b[28+n:]
def differences(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):return sum((differences(a.get(k),b.get(k),path+'/'+k) for k in sorted(set(a)|set(b))),[])
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):return sum((differences(v,w,path+'/'+str(i)) for i,(v,w) in enumerate(zip(a,b))),[])
 return [] if a==b else [{'path':path,'baseline':a,'revision':b}]
x,xb=read(a.baseline);y,yb=read(a.revision);d=differences(x,y)
allowed={'/materials/1/extras/palette_srgb',*['/materials/1/pbrMetallicRoughness/baseColorFactor/'+str(i) for i in range(3)]}
ok=xb==yb and {z['path'] for z in d}==allowed and y['materials'][1]['pbrMetallicRoughness']['baseColorFactor']==y['materials'][0]['pbrMetallicRoughness']['baseColorFactor']
r={'schema_version':1,'check':'r002_to_r003_color_only','status':'pass' if ok else 'fail','baseline_glb_sha256':sha(a.baseline),'glb_sha256':sha(a.revision),'binary_chunk_identical':xb==yb,'binary_sha256':hashlib.sha256(yb).hexdigest(),'binary_bytes':len(yb),'json_differences':d,'geometry_and_normals_unchanged':ok,'scene_graph_accessors_buffers_indices_transforms_unchanged':ok,'roughness_metallic_alpha_and_sidedness_unchanged':ok,'shell_and_former_sector_base_colors_equal':y['materials'][1]['pbrMetallicRoughness']['baseColorFactor']==y['materials'][0]['pbrMetallicRoughness']['baseColorFactor'],'limitations':'This compares shipping GLB structure/data; visual quality requires image review.'}
a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));assert ok
