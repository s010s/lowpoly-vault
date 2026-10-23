#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Current content-release audit; inherited legacy guards plus scale regressions."""
import struct
import tempfile
import unittest
from pathlib import Path
import test_qa_glb as legacy
from test_qa_glb import fixture, encode
from qa_glb_scale_aware import audit_glb


class TestScaleAwareGLBAudit(legacy.TestGLBAudit):
    def audit(self,doc=None,binary=None,**kwargs):
        base_doc,base_binary=fixture()
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'fixture.glb'
            path.write_bytes(encode(doc or base_doc,binary if binary is not None else base_binary))
            return audit_glb(path,**kwargs)

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

if __name__=='__main__': unittest.main()
