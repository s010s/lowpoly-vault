# SPDX-License-Identifier: MIT
"""Regression of tiny but nondegenerate geometry versus truly collinear faces.
Run in Blender: --python check_scale_tolerance.py -- OUTPUT_JSON
"""
from pathlib import Path
import json, math, struct, sys, tempfile
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from asset_common import setup_scene,mesh_object,make_material,audit_source
from qa_glb import audit_glb
out=Path(sys.argv[sys.argv.index('--')+1]);out.parent.mkdir(parents=True,exist_ok=True)
L=.0012;eps=L**2*1e-12
records=[]
def encode(positions):
    binary=b''.join(struct.pack('<3f',*p) for p in positions+[(0.,0.,1.)]*3)+struct.pack('<3H',0,1,2)+b'\0\0'
    doc={'asset':{'version':'2.0'},'buffers':[{'byteLength':len(binary)}],'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':36},{'buffer':0,'byteOffset':36,'byteLength':36},{'buffer':0,'byteOffset':72,'byteLength':6}],'accessors':[{'bufferView':0,'componentType':5126,'type':'VEC3','count':3,'min':[min(p[k] for p in positions) for k in range(3)],'max':[max(p[k] for p in positions) for k in range(3)]},{'bufferView':1,'componentType':5126,'type':'VEC3','count':3},{'bufferView':2,'componentType':5123,'type':'SCALAR','count':3}],'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[.5,.5,.5,1],'metallicFactor':0,'roughnessFactor':.85}}],'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1},'indices':2,'material':0}]}],'nodes':[{'mesh':0}],'scenes':[{'nodes':[0]}],'scene':0}
    payload=json.dumps(doc,separators=(',',':')).encode();payload+=b' '*(-len(payload)%4)
    return struct.pack('<4sII',b'glTF',2,28+len(payload)+len(binary))+struct.pack('<II',len(payload),0x4E4F534A)+payload+struct.pack('<II',len(binary),0x004E4942)+binary
for label,positions,expected in [('small_valid',[(0.,0.,0.),(1e-6,0.,0.),(0.,1e-6,0.)],False),('exact_zero_collinear',[(0.,0.,0.),(1e-6,0.,0.),(2e-6,0.,0.)],True),('subthreshold_nonzero',[(0.,0.,0.),(1e-10,0.,0.),(0.,1e-10,0.)],True)]:
    c=setup_scene('tolerance-fixture');m=make_material('gray','#888888')
    mesh_object('fixture_triangle',positions,[(0,1,2)],m,c,recalculate_normals=False)
    src=audit_source(c,triangle_area_epsilon=eps);src_rejected=any('degenerate' in e for e in src['errors'])
    with tempfile.TemporaryDirectory(prefix='tolerance-fixture-') as td:
        p=Path(td)/'fixture.glb';p.write_bytes(encode(positions));glb=audit_glb(p,triangle_area_epsilon=eps);glb_rejected=any('degenerate' in e for e in glb['errors'])
    assert src_rejected==expected and glb_rejected==expected,(label,src,glb)
    records.append({'fixture':label,'vertices_m':positions,'source_degenerate_rejected':src_rejected,'glb_degenerate_rejected':glb_rejected,'expected_rejection':expected,'source_errors':src['errors'],'glb_errors':glb['errors']})
out.write_text(json.dumps({'status':'PASS','formula':'body_length_m ** 2 * 1e-12','body_length_m':L,'area_epsilon_m2':eps,'cross_squared_epsilon_m4':(2*eps)**2,'original_source_threshold_m2':1e-10,'original_glb_threshold_m2':5e-11,'reason':'Fixed absolute thresholds incorrectly reject legitimate micron-scale detail on a 1.2 mm animal. Relative tolerance retains exact-zero and subthreshold rejection. No scaling of delivered geometry.','fixtures':records,'limits':'Regression proves behavior for these fixtures, not anatomical accuracy or rendered acceptance.'},indent=2)+'\n')
print('TOLERANCE_REGRESSION_PASS')
