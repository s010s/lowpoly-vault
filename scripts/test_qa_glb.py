#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Self-contained regression tests. No Blender, third-party assets or downloads."""
import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest
from qa_glb import audit_glb


def fixture():
    positions=[(0.,0.,0.),(1.,0.,0.),(0.,1.,0.)]
    normals=[(0.,0.,1.)]*3
    binary=b''.join(struct.pack('<3f',*p) for p in positions+normals)+struct.pack('<3H',0,1,2)+b'\0\0'
    doc={'asset':{'version':'2.0'},'buffers':[{'byteLength':len(binary)}],
         'bufferViews':[{'buffer':0,'byteOffset':0,'byteLength':36},{'buffer':0,'byteOffset':36,'byteLength':36},{'buffer':0,'byteOffset':72,'byteLength':6}],
         'accessors':[{'bufferView':0,'componentType':5126,'type':'VEC3','count':3,'min':[0,0,0],'max':[1,1,0]},
                      {'bufferView':1,'componentType':5126,'type':'VEC3','count':3},
                      {'bufferView':2,'componentType':5123,'type':'SCALAR','count':3}],
         'materials':[{'pbrMetallicRoughness':{'baseColorFactor':[.5,.5,.5,1],'metallicFactor':0,'roughnessFactor':.85}}],
         'meshes':[{'primitives':[{'attributes':{'POSITION':0,'NORMAL':1},'indices':2,'material':0}]}],
         'nodes':[{'mesh':0}],'scenes':[{'nodes':[0]}],'scene':0}
    return doc,binary


def encode(doc,binary):
    payload=json.dumps(doc,separators=(',',':')).encode()
    payload+=b' '*((-len(payload))%4)
    binary+=b'\0'*((-len(binary))%4)
    return struct.pack('<4sII',b'glTF',2,28+len(payload)+len(binary))+struct.pack('<II',len(payload),0x4E4F534A)+payload+struct.pack('<II',len(binary),0x004E4942)+binary


class TestGLBAudit(unittest.TestCase):
    def audit(self,doc=None,binary=None,**kwargs):
        base_doc,base_binary=fixture()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'fixture.glb'
            path.write_bytes(encode(doc or base_doc,binary if binary is not None else base_binary))
            return audit_glb(path,**kwargs)

    def test_valid_triangle(self):
        r=self.audit(); self.assertEqual(r['errors'],[]); self.assertEqual(r['scene_triangles'],1)
        self.assertEqual(r['bounds_m']['size'],[1.,1.,0.])

    def test_shared_geometry_counts_per_scene_node(self):
        d,b=fixture(); d['nodes'].append({'mesh':0,'translation':[3,0,0]}); d['scenes'][0]['nodes'].append(1)
        r=self.audit(d,b); self.assertEqual(r['unique_mesh_triangles'],1); self.assertEqual(r['scene_triangles'],2)
        self.assertEqual(r['bounds_m']['max'],[4.,1.,0.])

    def test_hierarchy_transform(self):
        d,b=fixture(); d['nodes']=[{'translation':[2,3,4],'children':[1]},{'mesh':0,'scale':[2,2,2]}];
        r=self.audit(d,b); self.assertEqual(r['bounds_m']['min'],[2.,3.,4.]); self.assertEqual(r['bounds_m']['max'],[4.,5.,4.])

    def test_invalid_index(self):
        d,b=fixture(); b=b[:72]+struct.pack('<3H',0,1,10)+b'\0\0'
        self.assertTrue(any('invalid index' in e for e in self.audit(d,b)['errors']))

    def test_missing_normal(self):
        d,b=fixture(); del d['meshes'][0]['primitives'][0]['attributes']['NORMAL']
        self.assertTrue(any('normals' in e for e in self.audit(d,b)['errors']))

    def test_nonfinite_position(self):
        d,b=fixture(); b=struct.pack('<f',float('nan'))+b[4:]
        self.assertTrue(any('Non-finite' in e for e in self.audit(d,b)['errors']))

    def test_bad_normal(self):
        d,b=fixture(); b=b[:36]+struct.pack('<3f',0,0,3)+b[48:]
        self.assertTrue(any('non-unit' in e for e in self.audit(d,b)['errors']))

    def test_degenerate(self):
        d,b=fixture(); b=b[:72]+struct.pack('<3H',0,0,1)+b'\0\0'
        self.assertTrue(any('degenerate' in e for e in self.audit(d,b)['errors']))

    def test_area_validation_is_scale_invariant(self):
        # Includes tiny and huge float32 geometry; no fourth-power under/overflow.
        for scale in (1e-30, 0.0012, 1., 1000., 1e30):
            for height_ratio, valid in ((1., True), (4e-12, True),
                                        (1e-13, False), (0., False)):
                with self.subTest(scale=scale, height_ratio=height_ratio):
                    d,b=fixture()
                    positions=[(0.,0.,0.), (scale,0.,0.), (0.,scale*height_ratio,0.)]
                    b=b''.join(struct.pack('<3f', *p) for p in positions)+b[36:]
                    # Deliberately stale declared bounds must not control tolerance.
                    d['accessors'][0]['min']=[0.,0.,0.]
                    d['accessors'][0]['max']=[1e-35,1e-35,1e-35]
                    r=self.audit(d,b)
                    if valid:
                        self.assertEqual(r['errors'],[])
                    else:
                        self.assertTrue(any('degenerate' in e for e in r['errors']))

    def test_collapsed_primitive_rejected(self):
        d,b=fixture(); b=bytes(36)+b[36:]
        self.assertTrue(any('degenerate' in e for e in self.audit(d,b)['errors']))

    def test_collinear_distinct_vertices_rejected(self):
        d,b=fixture()
        b=b''.join(struct.pack('<3f', *p) for p in [(0.,0.,0.), (1.,0.,0.), (2.,0.,0.)])+b[36:]
        self.assertTrue(any('degenerate' in e for e in self.audit(d,b)['errors']))

    def test_sparse_rejected(self):
        d,b=fixture(); d['accessors'][0]['sparse']={}
        self.assertTrue(any('Sparse' in e for e in self.audit(d,b)['errors']))

    def test_compression_rejected(self):
        d,b=fixture(); d['extensionsUsed']=['KHR_draco_mesh_compression']
        self.assertTrue(any('Compressed' in e for e in self.audit(d,b)['errors']))

    def test_cycle_rejected(self):
        d,b=fixture(); d['nodes'][0]['children']=[0]
        self.assertTrue(any('Cycle' in e for e in self.audit(d,b)['errors']))

    def test_digest_ignores_generator_and_extras(self):
        d,b=fixture(); original=self.audit(d,b)['semantic_sha256']
        d['asset']['generator']='another generator'; d['nodes'][0]['extras']={'note':'changed'}
        self.assertEqual(original,self.audit(d,b)['semantic_sha256'])

    def test_digest_detects_color_change(self):
        d,b=fixture(); original=self.audit(d,b)['semantic_sha256']
        d['materials'][0]['pbrMetallicRoughness']['baseColorFactor'][0]=0.7
        self.assertNotEqual(original,self.audit(d,b)['semantic_sha256'])

    def test_budget_enforced(self):
        self.assertTrue(any('budget' in e for e in self.audit(max_triangles=0)['errors']))

if __name__=='__main__': unittest.main()
