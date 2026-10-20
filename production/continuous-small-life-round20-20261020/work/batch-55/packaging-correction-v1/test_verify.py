#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Regression mutations occur only in disposable copies, never original assets."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from verify import (ROOT, WORK, ASSETS, POLICY, BASELINE, NEW_BLOCKERS,
                    digest_pin, read, create_contract, verify, verify_package,
                    validate_candidate, STATIC_PROFILE)


class PackagingCorrectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.old_dir = f'{ASSETS}/ventifact/r001'
        self.new_dir = f'{ASSETS}/ventifact/r001-packaging-v1'
        for folder in (self.old_dir, self.new_dir):
            shutil.copytree(ROOT / folder, self.root / folder)
        (self.root / POLICY).parent.mkdir(parents=True)
        shutil.copy2(ROOT / POLICY, self.root / POLICY)
        self.contract = json.loads((self.root / self.new_dir / 'packaging-contract.json').read_text())

    def rewrite(self, pin, change):
        path = self.root / pin['path']
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))
        pin.update(digest_pin(self.root, pin['path']))

    def mutate_candidate(self, change):
        self.rewrite(self.contract['corrected_candidate'], change)
        pin = self.contract['profile_contract']
        (self.root / pin['path']).write_text(json.dumps(create_contract(
            self.root, self.contract['corrected_candidate']['path'], POLICY)))
        pin.update(digest_pin(self.root, pin['path']))

    def mutate_brief(self, change):
        candidate = read(self.root, self.contract['corrected_candidate'], 'candidate')
        pin = candidate['artifacts']['brief']
        self.rewrite(pin, change)
        self.mutate_candidate(lambda record: record['artifacts'].update(brief=pin))

    def reject(self, message):
        with self.assertRaisesRegex(ValueError, message):
            verify_package(self.root, self.contract)

    def test_real_baseline_all_files_and_four_packages(self):
        index = json.loads((ROOT / WORK / 'index.json').read_text())
        result = verify(ROOT, index)
        self.assertEqual(result['baseline_commit'], BASELINE)
        self.assertEqual(result['preserved_baseline_file_count'], 520)
        self.assertEqual(result['historical_missing_log_count'], 20)
        self.assertFalse(result['approved_for_brief'])
        self.assertEqual(len(result['candidates']), 4)

    def test_valid_pending_new_subject_preserves_original_failure(self):
        result = verify_package(self.root, self.contract)
        self.assertTrue(result['corrected_candidate']['valid'])
        self.assertFalse(result['corrected_candidate']['approved_for_brief'])
        self.assertFalse(result['original_candidate']['valid'])
        self.assertIn('concept_generated_at: unknown', '; '.join(result['original_concept_integrity_recheck']['blockers']))

    def test_empty_deliverables_still_rejected_even_with_rehashed_record(self):
        self.mutate_brief(lambda b: b.update(required_deliverables=[]))
        self.reject('corrected brief changed')
        result = validate_candidate(self.contract['corrected_candidate']['path'], self.root,
            validation_profile=STATIC_PROFILE, profile_contract=self.contract['profile_contract']['path'])
        self.assertFalse(result['valid'])
        self.assertIn('required_deliverables missing', result['errors'][0])

    def test_changed_deliverable_pin_rejected(self):
        self.mutate_brief(lambda b: b['required_deliverables'][0].update(sha256='0' * 64))
        self.reject('corrected brief changed')

    def test_budgets_and_criteria_cannot_change(self):
        self.mutate_brief(lambda b: b['geometry_policy'].update(max_triangles=100000))
        self.reject('corrected brief changed')

    def test_backdated_declaration_rejected(self):
        self.contract['declared_at'] = '2026-10-19T00:00:00+00:00'
        self.reject('later than original freeze')

    def test_old_freeze_time_cannot_be_copied_into_new_brief(self):
        self.mutate_brief(lambda b: b.update(frozen_at=self.contract['chronology']['original_brief_frozen_at']))
        self.reject('corrected brief changed')

    def test_changed_approval_or_stage_rejected(self):
        self.mutate_candidate(lambda c: c['stages']['technical'].update(status='pass'))
        self.reject('corrected candidate changed')

    def test_open_log_blocker_cannot_be_removed(self):
        self.mutate_candidate(lambda c: c.update(blockers=c['blockers'][:-2]))
        self.reject('corrected candidate changed')

    def test_same_revision_or_wrong_supersedes_rejected(self):
        self.mutate_candidate(lambda c: c.update(revision='r001'))
        self.reject('corrected candidate changed')

    def test_original_glb_mutation_rejected(self):
        path = self.root / self.old_dir / 'ventifact.glb'
        path.write_bytes(path.read_bytes() + b'SYNTHETIC TEST MUTATION')
        self.reject('SHA-256 mismatch')

    def test_original_image_mutation_rejected(self):
        path = self.root / self.old_dir / 'proof/hero.png'
        path.write_bytes(path.read_bytes() + b'SYNTHETIC TEST MUTATION')
        self.reject('SHA-256 mismatch')

    def test_original_freeze_mutation_rejected(self):
        path = self.root / self.old_dir / 'modeling-freeze.json'
        path.write_bytes(path.read_bytes() + b'\n')
        self.reject('SHA-256 mismatch')

    def test_even_identical_json_cannot_be_fabricated_as_missing_historical_log(self):
        source = self.root / self.old_dir / 'evidence/reproducibility-1.json'
        shutil.copy2(source, source.with_suffix('.log'))
        self.reject('historical missing/present inventory changed')

    def test_stale_profile_or_candidate_hash_rejected(self):
        self.contract['profile_contract']['sha256'] = '0' * 64
        self.reject('SHA-256 mismatch')

    def test_legacy_zero_turntable_and_missing_profile_still_fail(self):
        path = self.contract['corrected_candidate']['path']
        legacy = validate_candidate(path, self.root)
        self.assertEqual(legacy['errors'], ['brief.turntable_frames: integer >= 2 required'])
        no_sidecar = validate_candidate(path, self.root, validation_profile=STATIC_PROFILE)
        self.assertFalse(no_sidecar['valid'])
        self.assertIn('--profile-contract required', no_sidecar['errors'][0])

    def test_cli_require_approved_fails(self):
        run = subprocess.run([sys.executable, str(ROOT / 'scripts/validate_candidate.py'),
            self.contract['corrected_candidate']['path'], '--root', str(self.root),
            '--profile', STATIC_PROFILE, '--profile-contract', self.contract['profile_contract']['path'],
            '--require-approved', '--json'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertTrue(json.loads(run.stdout)['valid'])
        self.assertFalse(json.loads(run.stdout)['approved_for_brief'])

    def test_creator_refuses_to_overwrite_existing_revisions(self):
        run = subprocess.run([sys.executable, str(ROOT / WORK / 'create.py'),
            '--declared-at', self.contract['declared_at']], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('already exists; no overwrite', run.stderr)


if __name__ == '__main__':
    unittest.main()
