#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon Made This / s010s
"""Temporary synthetic records test evidence integrity, never real asset acceptance."""
import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

from test_qa_glb import encode, fixture
from validate_concept_evidence import STAGES, validate


def png(color):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 2, 2, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress((b'\x00' + bytes(color) * 2) * 2)) + chunk(b'IEND', b''))


class ConceptEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.record = self.bundle()

    def put(self, path, value):
        full = self.root / path
        full.parent.mkdir(parents=True, exist_ok=True)
        raw = value if isinstance(value, bytes) else json.dumps(value).encode()
        full.write_bytes(raw)
        return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest()}

    def bundle(self):
        artifacts = {k: self.put(p, b'synthetic test input') for k, p in
                     {'source': 'source.blend', 'generator': 'generator.py', 'config': 'config.json',
                      'brief': 'brief.md', 'references': 'references.json'}.items()}
        artifacts['glb'] = self.put('model.glb', encode(*fixture()))
        subject = {'revision': 'r1', **{k + '_sha256': artifacts[k]['sha256'] for k in ('glb', 'brief', 'references')}}
        frames = []
        for i, (view, angles) in enumerate((('hero', [35, 20]), ('right', [90, 0]), ('top', [0, 90]))):
            raw = png((i * 30, 40, 50))
            frame = self.put('proof/' + view + '.png', raw)
            frame['path'] = view + '.png'
            frames.append({**frame, 'id': view, 'view': view, 'angle_degrees': angles,
                           'width': 2, 'height': 2, 'byte_length': len(raw)})
        config = self.put('proof/render-config.json', {'renderer': 'synthetic test', 'version': '1',
            'color_management': {'view_transform': 'Standard'}, 'lighting': {'test': True},
            'camera': {'type': 'ORTHO'}, 'frames': [{k: f[k] for k in ('id', 'view', 'angle_degrees')} for f in frames]})
        config['path'] = 'render-config.json'
        manifest = self.put('proof/render-manifest.json', {'schema_version': 1, 'kind': 'render_manifest',
            'stage': 'visual', 'subject': subject, 'source_glb_sha256': artifacts['glb']['sha256'],
            'source_unchanged': True, 'render_config': config, 'frames': frames})
        return {'schema_version': 1, 'kind': 'concept_evidence', 'scope': 'provisional-study',
            'asset_id': 'fixture', 'revision': 'r1', 'labels': {'en': 'Fixture', 'zh-CN': '测试'},
            'artifacts': artifacts, 'concept': {'provider': 'ImageGen',
                'prompt': self.put('concept/prompt.txt', b'Synthetic prompt fixture'),
                'generation_record': self.put('concept/generation.json', {'synthetic': True}),
                'images': [{'id': 'concept', 'view': 'hero', **self.put('concept/image.png', png((250, 1, 2)))}],
                'cross_view_consistency_note': 'Only one synthetic image.',
                'hidden_surface_decisions': 'Synthetic fixture cannot establish real geometry.'},
            'chronology': {'concept_generated_at': '2026-10-19T10:00:00Z',
                'concept_inspected_at': '2026-10-19T10:01:00Z', 'modeling_started_at': '2026-10-19T10:02:00Z'},
            'stage_timings': [{'stage': s, 'status': 'not_run' if s == 'target_browser' else 'unrecorded',
                'wall_seconds': None, 'measurement_record': None, 'note': 'Synthetic timing fixture.'} for s in STAGES],
            'coverage': {'required_views': ['hero', 'right', 'top'], 'turntable_frames': 0},
            'render_manifest': manifest,
            'thumbnail': {**self.put('thumb.png', (self.root / 'proof/hero.png').read_bytes()), 'source_frame_id': 'hero'},
            'review_note': self.put('review.md', b'Test record; never actual visual approval.'),
            'inspected_frames': ['hero', 'right', 'top'],
            'khronos': {'glb_sha256': artifacts['glb']['sha256'], 'warning_review': [],
                'report': self.put('validator.json', {'validatorVersion': 'synthetic-fixture',
                    'issues': {'numErrors': 0, 'numWarnings': 0, 'messages': [], 'truncated': False}})},
            'budget': {'target_glb_bytes': 1000000, 'enforcement': 'advisory', 'rationale': 'Synthetic target.'}}

    def run_record(self):
        self.put('evidence.json', self.record)
        return validate('evidence.json', self.root)

    def test_complete_record_remains_nonapproval_and_browser_unchecked(self):
        result = self.run_record()
        self.assertTrue(result['valid'], result)
        self.assertTrue(result['evidence_complete'], result)
        self.assertEqual(result['runtime_qa'], 'not_checked_by_this_tool')
        self.assertEqual(result['measurements']['triangles'], 1)
        self.assertNotIn('approved_for_brief', result)

    def test_unknown_chronology_is_honest_incomplete(self):
        self.record['chronology']['concept_generated_at'] = None
        result = self.run_record()
        self.assertTrue(result['valid'])
        self.assertFalse(result['evidence_complete'])

    def test_missing_historical_receipt_and_manifest_remain_incomplete(self):
        self.record['concept']['generation_record'] = None
        self.record['render_manifest'] = None
        result = self.run_record()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['evidence_complete'])
        self.assertEqual(len(result['blockers']), 2)

    def test_pending_preview_and_review_remain_incomplete(self):
        self.record['thumbnail'] = None
        self.record['review_note'] = None
        result = self.run_record()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['evidence_complete'])

    def test_wrong_order_is_invalid(self):
        self.record['chronology']['modeling_started_at'] = '2026-10-19T09:00:00Z'
        self.assertFalse(self.run_record()['valid'])

    def test_stale_input_is_invalid(self):
        (self.root / 'model.glb').write_bytes(b'changed')
        self.assertFalse(self.run_record()['valid'])

    def test_concept_cannot_be_thumbnail(self):
        self.record['thumbnail'] = {**self.record['concept']['images'][0], 'source_frame_id': 'hero'}
        self.assertFalse(self.run_record()['valid'])

    def test_concept_cannot_be_render(self):
        self.record['concept']['images'][0].update(self.put('concept/image.png', (self.root / 'proof/hero.png').read_bytes()))
        self.assertFalse(self.run_record()['valid'])

    def test_missing_visual_inspection_blocks_completion(self):
        self.record['inspected_frames'].remove('top')
        result = self.run_record()
        self.assertTrue(result['valid'])
        self.assertFalse(result['evidence_complete'])

    def test_missing_planned_frame_blocks_completion(self):
        path = self.root / 'proof/render-manifest.json'
        manifest = json.loads(path.read_text())
        manifest['frames'] = manifest['frames'][:-1]
        self.record['render_manifest'] = self.put('proof/render-manifest.json', manifest)
        self.record['inspected_frames'].remove('top')
        result = self.run_record()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['evidence_complete'])

    def test_orbit_frames_with_zero_frozen_count_rejected(self):
        manifest = json.loads((self.root / 'proof/render-manifest.json').read_text())
        manifest['frames'][1]['view'] = 'turntable'
        self.record['render_manifest'] = self.put('proof/render-manifest.json', manifest)
        self.assertFalse(self.run_record()['valid'])

    def test_stale_manifest_subject_is_invalid(self):
        manifest = json.loads((self.root / 'proof/render-manifest.json').read_text())
        manifest['subject']['glb_sha256'] = '0' * 64
        self.record['render_manifest'] = self.put('proof/render-manifest.json', manifest)
        self.assertFalse(self.run_record()['valid'])

    def test_thumbnail_path_escape_and_symlink_rejected(self):
        original = copy.deepcopy(self.record['thumbnail'])
        for path in ('../outside.png', '/tmp/outside.png', 'symlink.png'):
            with self.subTest(path=path):
                self.record['thumbnail'] = {**original, 'path': path}
                if path == 'symlink.png':
                    (self.root / path).symlink_to(self.root / 'thumb.png')
                self.assertFalse(self.run_record()['valid'])

    def test_size_target_advisory(self):
        self.record['budget']['target_glb_bytes'] = 1
        result = self.run_record()
        self.assertTrue(result['evidence_complete'], result)
        self.assertTrue(result['advisories'])

    def test_measured_time_requires_actual_record(self):
        item = self.record['stage_timings'][0]
        item.update(status='measured', wall_seconds=2.5)
        self.assertFalse(self.run_record()['valid'])
        item['measurement_record'] = self.put('timing.json', {'wall_seconds': 2.5, 'synthetic': True})
        self.assertTrue(self.run_record()['valid'])

    def test_unrun_browser_cannot_be_recorded_as_pass(self):
        self.record['stage_timings'][-1]['status'] = 'pass'
        self.assertFalse(self.run_record()['valid'])

    def test_khronos_error_blocks_completion(self):
        self.record['khronos']['report'] = self.put('validator.json', {'validatorVersion': 'fixture',
            'issues': {'numErrors': 1, 'numWarnings': 0, 'messages': [{'severity': 0, 'code': 'TEST'}], 'truncated': False}})
        result = self.run_record()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['evidence_complete'])

    def test_khronos_warning_requires_exact_review(self):
        warning = {'severity': 1, 'code': 'TEST_WARNING'}
        self.record['khronos']['report'] = self.put('validator.json', {'validatorVersion': 'fixture',
            'issues': {'numErrors': 0, 'numWarnings': 1, 'messages': [warning], 'truncated': False}})
        self.assertFalse(self.run_record()['valid'])
        self.record['khronos']['warning_review'] = [{'warning': warning, 'rationale': 'Synthetic test review.'}]
        self.assertTrue(self.run_record()['valid'])

    def test_duplicate_json_and_nonfinite_values_rejected(self):
        for raw in (b'{"schema_version":1,"schema_version":1}', b'{"x":NaN}', b'{"x":1e309}'):
            with self.subTest(raw=raw):
                self.put('bad.json', raw)
                self.assertFalse(validate('bad.json', self.root)['valid'])

    def test_cli_default_and_require_complete(self):
        self.record['chronology']['concept_generated_at'] = None
        self.run_record()
        args = [sys.executable, str(Path(__file__).with_name('validate_concept_evidence.py')),
                'evidence.json', '--root', str(self.root)]
        self.assertEqual(subprocess.run(args, capture_output=True).returncode, 0)
        self.assertEqual(subprocess.run(args + ['--require-complete'], capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
