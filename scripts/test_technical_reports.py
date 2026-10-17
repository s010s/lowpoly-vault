#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Temporary-fixture checks for raw technical evidence producers; no Blender needed."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from check_source_export import compare_source_audit
from check_reproducibility import compare_rebuild, file_hash, write_new_report, validate_build_run
from test_qa_glb import fixture, encode


class TechnicalReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.glb, self.rebuilt = self.root / 'original.glb', self.root / 'rebuilt.glb'
        self.generator, self.config = self.root / 'generator.py', self.root / 'config.json'
        self.glb.write_bytes(encode(*fixture()))
        self.rebuilt.write_bytes(encode(*fixture()))
        self.generator.write_text("raise RuntimeError('Must never execute this generator')\n")
        self.config.write_text('{"fixture":true}')
        self.source = {'errors': [], 'warnings': [], 'triangles': 1,
                       'bounds_blender_m': {'min': [0, -3, 0], 'max': [1, 0, 2]}}
        self.exported = {'errors': [], 'warnings': [], 'scene_triangles': 1,
                         'bounds_m': {'min': [0, 0, 0], 'max': [1, 2, 3]}}

    def compare(self):
        return compare_source_audit(self.source, self.exported, 'a' * 64, 'b' * 64)

    def test_source_axis_conversion_count_and_hashes(self):
        result = self.compare()
        self.assertEqual(result['status'], 'pass', result)
        self.assertTrue(result['triangles_match'])
        self.assertTrue(result['bounds_match'])
        self.assertEqual(result['source_sha256'], 'a' * 64)

    def test_source_count_mismatch_fails(self):
        self.exported['scene_triangles'] = 2
        self.assertEqual(self.compare()['status'], 'fail')

    def test_source_wrong_axis_bounds_fail(self):
        self.exported['bounds_m']['max'] = [1, 3, 2]
        self.assertEqual(self.compare()['status'], 'fail')

    def test_source_bounds_nonfinite_fail(self):
        self.source['bounds_blender_m']['min'][0] = float('inf')
        self.assertEqual(self.compare()['status'], 'fail')

    def test_source_cannot_loosen_tolerance_or_use_infinity(self):
        for tolerance in (1, float('inf'), float('nan'), -1):
            self.assertEqual(compare_source_audit(self.source, self.exported, 'a' * 64, 'b' * 64, tolerance)['status'], 'fail')

    def test_source_errors_are_not_hidden_by_equal_bounds(self):
        self.source['errors'] = ['invalid geometry']
        self.assertEqual(self.compare()['status'], 'fail')

    def test_source_warnings_preserved_for_review(self):
        self.source['warnings'] = ['Intentional boundary']
        result = self.compare()
        self.assertEqual(result['status'], 'pass_with_warnings')
        self.assertEqual(result['warnings'], ['source: Intentional boundary'])

    def test_separate_rebuild_semantic_equality_does_not_run_generator(self):
        before = {path: file_hash(path) for path in (self.glb, self.rebuilt, self.generator, self.config)}
        result = compare_rebuild(self.glb, self.rebuilt, self.generator, self.config)
        self.assertEqual(result['status'], 'unknown', result)
        self.assertTrue(result['semantic_match'])
        self.assertFalse(result['generator_executed'])
        self.assertEqual(result['generator_sha256'], file_hash(self.generator))
        self.assertEqual(before, {path: file_hash(path) for path in before})

    def test_rebuild_material_change_fails(self):
        document, binary = fixture()
        document['materials'][0]['pbrMetallicRoughness']['baseColorFactor'][0] = 0.9
        self.rebuilt.write_bytes(encode(document, binary))
        result = compare_rebuild(self.glb, self.rebuilt, self.generator, self.config)
        self.assertEqual(result['status'], 'fail')
        self.assertFalse(result['semantic_match'])

    def test_rebuild_metadata_change_can_match_semantics(self):
        document, binary = fixture()
        document['asset']['generator'] = 'synthetic alternate metadata'
        self.rebuilt.write_bytes(encode(document, binary))
        result = compare_rebuild(self.glb, self.rebuilt, self.generator, self.config)
        self.assertEqual(result['status'], 'unknown')
        self.assertFalse(result['byte_identical'])
        self.assertTrue(result['semantic_match'])

    def test_same_file_cannot_be_its_own_rebuild(self):
        result = compare_rebuild(self.glb, self.glb, self.generator, self.config)
        self.assertEqual(result['status'], 'fail')
        self.assertIn('distinct separately rebuilt', result['errors'][0])

    def test_hardlink_cannot_be_its_own_rebuild(self):
        self.rebuilt.unlink()
        self.rebuilt.hardlink_to(self.glb)
        self.assertEqual(compare_rebuild(self.glb, self.rebuilt, self.generator, self.config)['status'], 'fail')

    def test_invalid_rebuilt_glb_cannot_pass(self):
        self.rebuilt.write_bytes(b'not a glb')
        self.assertEqual(compare_rebuild(self.glb, self.rebuilt, self.generator, self.config)['status'], 'fail')

    def test_missing_generator_or_config_cannot_pass(self):
        self.config.unlink()
        self.assertEqual(compare_rebuild(self.glb, self.rebuilt, self.generator, self.config)['status'], 'fail')


    def build_run(self):
        identity = {'runner_schema': 1, 'lane': 'build', 'inputs': {key: {'path': str(path), 'sha256': file_hash(path)} for key, path in [('generator', self.generator), ('config', self.config)]},
                    'job': {'asset_id': 'fixture', 'revision': 'v001', 'job_id': 'rebuild'}}
        fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        request = {'identity': identity, 'fingerprint': fingerprint, 'argv': [str(self.generator), str(self.config)]}
        result = {'schema_version': 1, 'fingerprint': fingerprint, **identity['job'], 'status': 'succeeded', 'returncode': 0, 'error': None,
                  'outputs': {'rebuilt.glb': {'sha256': file_hash(self.rebuilt), 'bytes': self.rebuilt.stat().st_size}}}
        return request, result

    def test_success_requires_bound_successful_build_run(self):
        request, result = self.build_run()
        req, res = self.root / 'request.json', self.root / 'result.json'
        req.write_text(json.dumps(request));res.write_text(json.dumps(result))
        report = compare_rebuild(self.glb, self.rebuilt, self.generator, self.config, req, res, 'rebuilt.glb', self.root)
        self.assertEqual(report['status'], 'pass', report)
        self.assertEqual(report['build_run']['request']['sha256'], file_hash(req))
        self.assertFalse(report['generator_executed'])

    def test_failed_build_record_cannot_certify_rebuild(self):
        request, result = self.build_run()
        result['returncode'] = 1
        with self.assertRaisesRegex(ValueError, 'returncode 0'):
            validate_build_run(request, result, file_hash(self.generator), file_hash(self.config), file_hash(self.rebuilt), 'rebuilt.glb')

    def test_build_output_hash_mismatch_rejected(self):
        request, result = self.build_run()
        result['outputs']['rebuilt.glb']['sha256'] = 'a' * 64
        with self.assertRaisesRegex(ValueError, 'rebuilt GLB output'):
            validate_build_run(request, result, file_hash(self.generator), file_hash(self.config), file_hash(self.rebuilt), 'rebuilt.glb')

    def test_build_inputs_hash_mismatch_rejected(self):
        request, result = self.build_run()
        with self.assertRaisesRegex(ValueError, 'exact generator'):
            validate_build_run(request, result, 'b' * 64, file_hash(self.config), file_hash(self.rebuilt), 'rebuilt.glb')

    def test_report_output_is_no_clobber(self):
        output = self.root / 'raw-report.json'
        report = self.compare()
        write_new_report(output, report)
        with self.assertRaises(FileExistsError):
            write_new_report(output, {'status': 'pass'})
        self.assertEqual(json.loads(output.read_text()), report)


if __name__ == '__main__':
    unittest.main()
