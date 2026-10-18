#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Both contracts exercise complete synthetic evidence; no real asset is approved."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from candidate_profile import create_contract
import test_validate_candidate as legacy
from test_validate_candidate import build_fixture, digest
from validate_candidate import validate_candidate, STATIC_PROFILE, PROFILE_RULE_VERSION, approval_snapshot_sha256


class StaticProfileTests(unittest.TestCase):
    mutate_report = legacy.CandidateGateTests.mutate_report
    rebind_brief = legacy.CandidateGateTests.rebind_brief
    rebind_review_evidence = legacy.CandidateGateTests.rebind_review_evidence

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.policy = self.root / 'policy.json'
        self.policy.write_text(json.dumps({'schema_version': 1, 'scope': 's010s/lowpoly-vault',
            'authority': 'owner_authorized_qa_passed_batch_release', 'candidate_gate_grants_publication': False,
            'authorization_source': 'SYNTHETIC TEST ONLY'}))
        self.contract_path = self.root / 'profile-contract.json'
        self.reset()

    def reset(self, approved=True, textured=False):
        self.candidate, self.path = build_fixture(self.root, static_contract=True, approved=approved, textured=textured)
        if approved:
            self.candidate['approval'].update(validation_profile=STATIC_PROFILE, rule_version=PROFILE_RULE_VERSION)

    def run_gate(self, refresh=True):
        if refresh:
            self.path.write_text(json.dumps(self.candidate))
            self.contract_path.write_text(json.dumps(create_contract(self.root, self.path.relative_to(self.root).as_posix(), 'policy.json')))
        return validate_candidate(self.path, self.root, validation_profile=STATIC_PROFILE, profile_contract=self.contract_path)

    def assertRejected(self, match):
        result = self.run_gate()
        self.assertFalse(result['valid'], result)
        self.assertFalse(result['approved_for_brief'], result)
        self.assertIn(match, '; '.join(result['errors']))

    def references(self, change):
        pin = self.candidate['artifacts']['references']
        path = self.root / pin['path']
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))
        pin['sha256'] = digest(path.read_bytes())
        subject = self.candidate['approval'].get('subject')
        if subject:
            subject['references_sha256'] = pin['sha256']
        for stage in self.candidate['stages'].values():
            if stage.get('subject'):
                stage['subject']['references_sha256'] = pin['sha256']
        for item in self.candidate['evidence']:
            item['subject']['references_sha256'] = pin['sha256']
            if item['kind'] != 'rendered_image':
                self.mutate_report(item['id'], lambda report: report['subject'].update(references_sha256=pin['sha256']))
        self.rebind_review_evidence()
        if subject:
            self.candidate['approval']['review_snapshot_sha256'] = approval_snapshot_sha256(self.candidate)

    def consulted(self, data):
        data['no_incorporated_third_party_assets'] = True
        source = data['sources'][0]
        source.pop('license', None)
        source.update(use='consulted-only', rights_note='SYNTHETIC: no license grant inferred, no media incorporated.')

    def test_complete_static_evidence_approved_and_legacy_failure_preserved(self):
        self.references(self.consulted)
        result = self.run_gate()
        self.assertTrue(result['valid'], result)
        self.assertTrue(result['approved_for_brief'], result)
        self.assertEqual(result['rule_version'], PROFILE_RULE_VERSION)
        self.assertFalse(result['legacy_result']['valid'])
        self.assertIn('license', result['legacy_result']['errors'][0])

    def test_default_legacy_still_rejects_zero_turntable(self):
        self.run_gate()
        old = validate_candidate(self.path, self.root)
        self.assertFalse(old['valid'])
        self.assertIn('integer >= 2', old['errors'][0])

    def test_both_profiles_keep_legacy_production_approval(self):
        candidate, path = build_fixture(self.root, base='legacy')
        result = validate_candidate(path, self.root)
        self.assertTrue(result['valid'], result)
        self.assertTrue(result['approved_for_brief'], result)
        self.assertFalse(validate_candidate(path, self.root, validation_profile=STATIC_PROFILE)['valid'])

    def test_full_turntable_contract_cannot_silently_select_static(self):
        self.candidate,self.path=build_fixture(self.root)
        self.assertRejected('exactly eight fixed views and zero turntable')

    def test_pending_remains_pending_and_cli_require_approved_fails(self):
        self.reset(approved=False)
        self.rebind_brief(lambda b: (b.update(publication_authority='Owner project policy; maker does not release.'), b.pop('required_deliverables')))
        result = self.run_gate()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['approved_for_brief'])
        self.assertIn('gpu: unknown', result['approval_blockers'])
        run = subprocess.run([sys.executable, str(Path(__file__).with_name('validate_candidate.py')), str(self.path), '--root', str(self.root), '--profile', STATIC_PROFILE, '--profile-contract', str(self.contract_path), '--require-approved', '--json'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(json.loads(run.stdout)['approved_for_brief'])

    def test_explicit_authority_normalization_does_not_change_original_files(self):
        self.rebind_brief(lambda b: (b.update(publication_authority='Project authorization is separate from this maker task.'), b.pop('required_deliverables')))
        before = (self.root / self.candidate['artifacts']['brief']['path']).read_bytes()
        result = self.run_gate()
        self.assertTrue(result['approved_for_brief'], result)
        self.assertIn('publication authority must remain separate', result['legacy_result']['errors'][0])
        self.assertEqual(before, (self.root / self.candidate['artifacts']['brief']['path']).read_bytes())

    def test_no_fallback_without_contract_or_with_unknown_profile(self):
        self.run_gate()
        self.assertFalse(validate_candidate(self.path, self.root, validation_profile=STATIC_PROFILE)['valid'])
        self.assertFalse(validate_candidate(self.path, self.root, validation_profile='static-unknown')['valid'])

    def test_unknown_rule_version_candidate_pin_policy_and_path_rejected(self):
        self.run_gate()
        original = self.contract_path.read_text()
        changes = [lambda c: c.update(rule_version='future'), lambda c:c.update(schema_version=True), lambda c: c['candidate'].update(sha256='0'*64), lambda c: c['candidate'].update(path='../escape'), lambda c: c.update(publication_authority='publish'), lambda c: c['publication_policy'].update(sha256='0'*64), lambda c: c.update(extra=True)]
        for change in changes:
            with self.subTest(change=change):
                contract = json.loads(original);change(contract);self.contract_path.write_text(json.dumps(contract))
                result = self.run_gate(False)
                self.assertFalse(result['valid'], result)
                self.assertFalse(result['approved_for_brief'])
        self.contract_path.write_text(original)

    def test_policy_cannot_grant_candidate_gate_publication(self):
        p = json.loads(self.policy.read_text());p['candidate_gate_grants_publication'] = True;self.policy.write_text(json.dumps(p))
        self.assertRejected('invalid separate publication policy')

    def test_missing_or_duplicate_fixed_view_and_nonzero_turntable_rejected(self):
        for change in [lambda b: b['required_views'].pop(),lambda b: b['required_views'].append(b['required_views'][0]),lambda b:b.update(turntable_frames=2),lambda b:b.update(turntable_frames=False)]:
            with self.subTest(change=change):
                self.reset();self.rebind_brief(change)
                self.assertFalse(self.run_gate()['valid'])

    def test_geometry_threshold_not_relaxed(self):
        self.rebind_brief(lambda b:b['geometry_policy'].update(max_glb_bytes=1))
        self.assertRejected('unresolved obligations')

    def test_source_generator_config_required_without_legacy_role_list(self):
        self.rebind_brief(lambda b:b.pop('required_deliverables'))
        self.candidate['artifacts'].pop('source')
        self.assertRejected('source/generator/config')

    def test_declared_deliverables_mismatch_is_not_normalized_away(self):
        self.rebind_brief(lambda b:b['required_deliverables'][0].update(sha256='0'*64))
        self.assertRejected('exact frozen artifact')

    def test_consulted_record_requires_no_incorporation_and_rights_note(self):
        for change in [lambda d:d.pop('no_incorporated_third_party_assets'),lambda d:d['sources'][0].pop('rights_note'),lambda d:d['sources'][0].update(incorporated=True)]:
            with self.subTest(change=change):
                self.reset();self.references(self.consulted);self.references(change)
                self.assertFalse(self.run_gate()['valid'])

    def test_incorporated_source_still_requires_license(self):
        self.references(lambda d:d['sources'][0].pop('license'))
        self.assertRejected('license')

    def test_consulted_source_cannot_supply_embedded_texture(self):
        self.reset(textured=True);self.references(self.consulted)
        self.assertRejected('incorporated texture')

    def test_versioned_approval_required_and_gpu_not_waived(self):
        self.candidate['approval'].pop('validation_profile')
        self.assertRejected('exact static validation profile')
        self.reset();self.mutate_report('gpu-report', lambda r:r['runtime'].update(rendered=False))
        self.assertRejected('actual GPU context')

    def test_static_render_manifest_missing_duplicate_or_extra_view_rejected(self):
        for mode in ['missing','duplicate','extra']:
            self.reset()
            def mutate(report):
                if mode=='missing': report['frames'].pop()
                elif mode=='duplicate': report['frames'][-1]['view']=report['frames'][0]['view']
                else: report['frames'].append({**report['frames'][0], 'id':'extra'})
            self.mutate_report('visual-renders',mutate)
            entry=next(e for e in self.candidate['evidence'] if e['id']=='visual-renders')
            manifest=json.loads((self.root/entry['path']).read_text())
            config_path=(self.root/entry['path']).parent/manifest['render_config']['path']
            config=json.loads(config_path.read_text())
            config['frames']=[{key:f[key] for key in ('id','view','angle_degrees')} for f in manifest['frames']]
            config_path.write_text(json.dumps(config))
            self.mutate_report('visual-renders',lambda r:r['render_config'].update(sha256=digest(config_path.read_bytes())))
            self.rebind_review_evidence();self.candidate['approval']['review_snapshot_sha256']=approval_snapshot_sha256(self.candidate)
            self.assertFalse(self.run_gate()['valid'])

    def test_profile_compatibility_cannot_hide_malformed_pending_records(self):
        self.reset(approved=False)
        self.candidate['blockers']=['Unresolved historical blocker']
        result=self.run_gate()
        self.assertEqual(result['profile_contract_status'],'pass')
        self.assertFalse(result['valid'])
        self.assertFalse(result['approved_for_brief'])
        self.assertIn('blocker: expected object',result['errors'])
        self.reset(approved=False)
        self.candidate['stages']['technical']['criteria'][0]['id']='unknown-criterion'
        result=self.run_gate()
        self.assertEqual(result['profile_contract_status'],'pass')
        self.assertFalse(result['valid'])
        self.assertIn('wrong-stage or duplicate criterion',result['errors'][0])

    def test_bound_artifact_tamper_and_symlink_rejected(self):
        for key in ['glb','source','brief','references']:
            self.reset();path=self.root/self.candidate['artifacts'][key]['path'];path.write_bytes(path.read_bytes()+b' ')
            self.assertRejected('SHA-256 mismatch')
        self.reset();self.run_gate();path=self.root/self.candidate['artifacts']['source']['path'];target=path.with_suffix('.original');path.rename(target);path.symlink_to(target)
        self.assertFalse(self.run_gate(False)['valid'])


if __name__ == '__main__':
    unittest.main()
