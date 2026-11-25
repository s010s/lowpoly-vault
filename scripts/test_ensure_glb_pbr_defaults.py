#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Unit tests for scripts/ensure_glb_pbr_defaults.py."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ensure_glb_pbr_defaults import (
    CHUNK_BIN,
    ensure_glb_pbr_defaults,
    normalize_glb_materials_bytes,
    pack_glb,
    read_glb_chunks,
)


def make_glb(materials, bin_payload=b'\x01\x02\x03\x04\x05\x06\x07\x08'):
    doc = {'asset': {'version': '2.0'}, 'materials': materials}
    return pack_glb(doc, [(CHUNK_BIN, bin_payload)])


class TestEnsureGlbPbrDefaults(unittest.TestCase):
    def test_sets_explicit_metallic_and_roughness_preserving_bin(self):
        bin_data = bytes(range(32))
        raw = make_glb([{'name': 'm0', 'pbrMetallicRoughness': {'baseColorFactor': [0.5, 0.5, 0.5, 1.0]}}], bin_data)
        patched, report = normalize_glb_materials_bytes(raw, asset_id='scutellosaurus')
        self.assertTrue(report['changed'])
        doc, trailing = read_glb_chunks(patched)
        pbr = doc['materials'][0]['pbrMetallicRoughness']
        self.assertEqual(pbr['metallicFactor'], 0.0)
        self.assertEqual(pbr['roughnessFactor'], 0.9)
        self.assertEqual(trailing[0][1], bin_data)
        self.assertEqual(len(patched) % 4, 0)

    def test_normalizes_high_explicit_metallic(self):
        raw = make_glb([{'name': 'm0', 'pbrMetallicRoughness': {'metallicFactor': 0.65, 'roughnessFactor': 0.85}}])
        patched, report = normalize_glb_materials_bytes(raw, asset_id='conglomerate-outcrop')
        self.assertTrue(report['changed'])
        doc, _ = read_glb_chunks(patched)
        self.assertEqual(doc['materials'][0]['pbrMetallicRoughness']['metallicFactor'], 0.0)
        self.assertEqual(doc['materials'][0]['pbrMetallicRoughness']['roughnessFactor'], 0.85)

    def test_respects_metallic_roughness_texture(self):
        raw = make_glb([{'name': 'pbr', 'pbrMetallicRoughness': {'metallicRoughnessTexture': {'index': 0}}}])
        patched, report = normalize_glb_materials_bytes(raw, asset_id='tyrannosaurus')
        self.assertFalse(report['changed'])
        self.assertEqual(patched, raw)

    def test_exempts_true_metal_whitelist(self):
        raw = make_glb([{'name': 'pyrite', 'pbrMetallicRoughness': {'metallicFactor': 0.95, 'roughnessFactor': 0.3}}])
        for asset_id in ('pyrite-cube-cluster', 'native-copper-dendrite'):
            patched, report = normalize_glb_materials_bytes(raw, asset_id=asset_id)
            self.assertTrue(report['exempt'])
            self.assertFalse(report['changed'])
            self.assertEqual(patched, raw)

    def test_supports_crystal_roughness_override(self):
        raw = make_glb([{'name': 'quartz', 'pbrMetallicRoughness': {'roughnessFactor': 0.9}}])
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'quartz.glb'
            p.write_bytes(raw)
            report = ensure_glb_pbr_defaults(p, asset_id='quartz-prism-cluster', roughness_override=0.25)
            self.assertTrue(report['changed'])
            doc, _ = read_glb_chunks(p.read_bytes())
            pbr = doc['materials'][0]['pbrMetallicRoughness']
            self.assertEqual(pbr['metallicFactor'], 0.0)
            self.assertEqual(pbr['roughnessFactor'], 0.25)


if __name__ == '__main__':
    unittest.main()
