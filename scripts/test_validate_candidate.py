#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Behavioral tests with synthetic temporary evidence. No real asset is approved."""
import base64
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

from test_qa_glb import fixture, encode
from qa_glb import audit_glb
from validate_candidate import STAGES, REPORT_KIND, PRODUCTION_VIEWS, ENVIRONMENT_PROP_VIEWS, validate_candidate, image_size, json_bytes, check_render_manifest, approval_snapshot_sha256


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def png():
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b'\0\xff\0\0')) + chunk(b'IEND', b''))


def build_fixture(root, base='candidate-fixture', glb_name='model.glb', approved=True, profile='production', textured=False, quality_tier=None):
    """Fake assertions intentionally marked synthetic; only exercise the gate's behavior."""
    root = Path(root)
    folder = root / base
    folder.mkdir(parents=True, exist_ok=True)
    def save(name, value):
        raw = value if isinstance(value, bytes) else (json.dumps(value, indent=2) + '\n').encode()
        (folder / name).write_bytes(raw)
        return {'path': f'{base}/{name}', 'sha256': digest(raw)}
    doc, binary = fixture()
    texture_descriptor = None
    if textured:
        embedded = png()
        doc['images'] = [{'bufferView': len(doc['bufferViews']), 'mimeType': 'image/png'}]
        doc['bufferViews'].append({'buffer': 0, 'byteOffset': len(binary), 'byteLength': len(embedded)})
        binary += embedded
        doc['buffers'][0]['byteLength'] = len(binary)
        doc['textures'] = [{'source': 0}]
        doc['materials'][0]['pbrMetallicRoughness']['baseColorTexture'] = {'index': 0}
        texture_descriptor = {'image_index': 0, 'width': 1, 'height': 1, 'byte_length': len(embedded),
                              'provenance': {'source_id': 'reference-a', 'creator': 'Synthetic fixture', 'license': 'CC0', 'usage': 'test texture'},
                              **save('texture.png', embedded)}
    artifact = save(glb_name, encode(doc, binary))
    deliverables = {role: save(role + '.fixture', ('SYNTHETIC TEST ONLY ' + role).encode()) for role in ('source', 'generator', 'config')}
    references = save('references.json', {'schema_version': 1, 'sources': [
        {'id': 'reference-a', 'title': 'SYNTHETIC TEST ONLY', 'url': 'https://example.invalid/fixture', 'license': 'CC0'}]})
    brief = {'schema_version': 1, 'asset_id': 'test-only', 'brief_version': 'brief-v001', 'profile': profile,
             'publication_authority': 'separate', 'required_stages': [],
             'required_deliverables': [{'role': role, **item} for role, item in deliverables.items()], 'required_views': sorted(PRODUCTION_VIEWS),
             'turntable_frames': 24 if profile == 'production' else 4,
             'coverage_justification': 'Synthetic fixture only; not an asset-quality recommendation.',
             'geometry_policy': {'max_triangles': 10, 'max_materials': 8, 'max_primitives': 8, 'max_glb_bytes': 100000},
             'texture_policy': {'max_textures': 1 if textured else 0, 'max_dimension': 1 if textured else 0, 'max_total_bytes': len(png()) if textured else 0, 'max_decoded_bytes': 4 if textured else 0},
             'criteria': [{'id': stage + '-criterion', 'stage': stage, 'critical': stage not in ('gpu', 'scene') or profile == 'production',
                           'description': 'SYNTHETIC TEST ONLY: ' + stage, 'required_sources': ['reference-a'] if stage in ('visual', 'factual') else []}
                          for stage in STAGES]}
    if quality_tier is not None:
        brief['quality_tier'] = quality_tier
    if quality_tier == 'environment-prop':
        brief.update(required_views=sorted(ENVIRONMENT_PROP_VIEWS), turntable_frames=0)
    brief_artifact = save('brief.json', brief)
    subject = {'revision': 'v001', 'glb_sha256': artifact['sha256'], 'brief_sha256': brief_artifact['sha256'],
               'references_sha256': references['sha256']}
    independent = {'id': 'synthetic-reviewer', 'task_id': 'synthetic-review-task'}
    candidate = {'schema_version': 1, 'asset_id': 'test-only', 'revision': 'v001',
                 'maker': {'id': 'synthetic-maker', 'task_id': 'synthetic-maker-task'},
                 'artifacts': {'glb': artifact, 'brief': brief_artifact, 'references': references, **deliverables}, 'textures': [texture_descriptor] if textured else [],
                 'supersedes': None, 'evidence': [], 'stages': {}, 'blockers': [], 'approval': {'status': 'pending'}}
    if approved:
        candidate['approval'] = {'status': 'approved_for_brief', 'reviewer': independent.copy(),
                                 'reviewed_at': '2026-10-17T00:00:00Z', 'subject': subject.copy(), 'note': 'SYNTHETIC TEST ONLY'}
    def evidence(eid, kind, stage, name, content):
        item = {'id': eid, 'kind': kind, 'stage': stage, 'subject': subject.copy(), **save(name, content)}
        candidate['evidence'].append(item)
        return eid
    image = png()
    measured = {'triangles': 1, 'materials': 1, 'primitives': 1, 'glb_bytes': (folder / glb_name).stat().st_size,
                'texture_count': 1 if textured else 0, 'texture_max_dimension': 1 if textured else 0, 'texture_bytes': len(png()) if textured else 0}
    for stage in STAGES:
        entry = {'status': 'pass' if approved else 'unknown', 'reviewer': independent.copy() if approved else None,
                 'reviewed_at': '2026-10-17T00:00:00Z' if approved else None, 'subject': subject.copy() if approved else None,
                 'evidence': [], 'inspected_references': ['reference-a'] if approved else [], 'criteria': [], 'note': 'SYNTHETIC TEST ONLY'}
        candidate['stages'][stage] = entry
        if approved:
            report = {'schema_version': 1, 'kind': REPORT_KIND[stage], 'stage': stage, 'subject': subject.copy(),
                      'status': 'pass', 'method': 'SYNTHETIC TEST ONLY', 'observations': ['Synthetic fixture exercised.'], 'errors': []}
            if stage == 'technical':
                audit = audit_glb(folder / glb_name)
                identity = {'runner_schema': 1, 'lane': 'build', 'inputs': {role: {'path': str(folder / (role + '.fixture')), 'sha256': deliverables[role]['sha256']} for role in ('generator', 'config')},
                            'job': {'asset_id': 'test-only', 'revision': 'v001', 'job_id': 'synthetic-build'}}
                fingerprint = digest(json.dumps(identity, sort_keys=True, separators=(',', ':')).encode())
                request = {'identity': identity, 'fingerprint': fingerprint, 'argv': [str(folder / 'generator.fixture'), str(folder / 'config.fixture')]}
                result = {'schema_version': 1, 'fingerprint': fingerprint, **identity['job'], 'status': 'succeeded', 'returncode': 0, 'error': None,
                          'outputs': {glb_name: {'sha256': subject['glb_sha256'], 'bytes': measured['glb_bytes']}}}
                build_run = {'request': save('build-request.json', request), 'result': save('build-result.json', result), 'output': glb_name}
                raw_checks = {
                    'static_glb': audit,
                    'khronos_validator': {'validatorVersion': 'SYNTHETIC TEST ONLY', 'issues': {'numErrors': 0, 'numWarnings': 0, 'messages': [], 'truncated': False}},
                    'source_export': {'status': 'pass', 'glb_sha256': subject['glb_sha256'], 'source_sha256': deliverables['source']['sha256'], 'errors': [], 'triangles_match': True, 'bounds_match': True},
                    'reproducibility': {'status': 'pass', 'glb_sha256': subject['glb_sha256'], 'generator_sha256': deliverables['generator']['sha256'], 'config_sha256': deliverables['config']['sha256'],
                                        'errors': [], 'semantic_sha256': audit['semantic_sha256'], 'rebuilt_semantic_sha256': audit['semantic_sha256'],
                                        'rebuilt_glb_sha256': subject['glb_sha256'], 'build_run': build_run}}
                report.update(measurements=measured, checks=[{'name': name, 'status': 'pass', 'glb_sha256': subject['glb_sha256'],
                              'report': save(name + '-raw.json', raw), 'warning_review': []} for name, raw in raw_checks.items()])
            if stage == 'runtime_parse':
                report['runtime'] = {'engine': 'Three.js', 'version': 'test', 'loader': 'GLTFLoader', 'parsed': True}
            if stage in ('gpu', 'scene'):
                shot = evidence(stage + '-shot', 'rendered_image', stage, stage + '.png', image)
                entry['evidence'].append(shot)
                report['screenshots'] = [shot]
                report['runtime'] = {'engine': 'Three.js', 'version': 'test', 'renderer': 'SYNTHETIC', 'device': 'SYNTHETIC',
                                     'browser': 'SYNTHETIC', 'context': 'webgl2', 'output_color_space': 'srgb', 'tone_mapping': 'none',
                                     'exposure': 1, 'context_created': True, 'rendered': True, 'rendered_frames': 1,
                                     'draw_calls': 1, 'triangles': 1}
            if stage == 'scene':
                report['scene_description'] = 'SYNTHETIC TEST ONLY composite'
                report['scene_assets'] = [{'glb_sha256': subject['glb_sha256'], 'instances': 1}]
            if stage == 'visual':
                config = save('render-config.json', {'renderer': 'SYNTHETIC', 'version': '1', 'color_management': 'standard',
                                                     'lighting': 'synthetic', 'camera': 'synthetic'})
                config['path'] = 'render-config.json'
                canonical = {'front': [0, 0], 'right': [90, 0], 'rear': [180, 0], 'left': [270, 0], 'top': [0, 90], 'bottom': [0, -90]}
                frames = []
                for i, view in enumerate(brief['required_views'] + ['turntable'] * brief['turntable_frames']):
                    frame = {'id': f'frame-{i:03}', 'view': view, 'angle_degrees': [
                        (i - len(brief['required_views'])) * 360 / brief['turntable_frames'] if view == 'turntable' else 0, 0],
                        'width': 1, 'height': 1, 'byte_length': len(image), **save(f'frame-{i:03}.png', image)}
                    if view in canonical:
                        frame['angle_degrees'] = canonical[view]
                    frame['path'] = f'frame-{i:03}.png'
                    frames.append(frame)
                config_doc = json.loads((folder / 'render-config.json').read_text())
                config_doc['frames'] = [{key: frame[key] for key in ('id', 'view', 'angle_degrees')} for frame in frames]
                config = save('render-config.json', config_doc)
                config['path'] = 'render-config.json'
                manifest = {'schema_version': 1, 'kind': 'render_manifest', 'stage': 'visual', 'subject': subject.copy(),
                            'render_config': config, 'frames': frames}
                entry['evidence'].append(evidence('visual-renders', 'render_manifest', stage, 'render-manifest.json', manifest))
                entry['inspected_frames'] = [frame['id'] for frame in frames]
            report['reviewed_evidence'] = [{'id': eid, 'sha256': next(item['sha256'] for item in candidate['evidence'] if item['id'] == eid)} for eid in entry['evidence']]
            entry['evidence'].append(evidence(stage + '-report', REPORT_KIND[stage], stage, stage + '-report.json', report))
        entry['criteria'] = [{'id': stage + '-criterion', 'status': 'pass' if approved else 'unknown',
                              'evidence': list(entry['evidence']), 'note': 'SYNTHETIC TEST ONLY'}]
    if approved:
        candidate['approval']['review_snapshot_sha256'] = approval_snapshot_sha256(candidate)
    save('candidate.json', candidate)
    return candidate, folder / 'candidate.json'


class CandidateGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.candidate, self.path = build_fixture(self.root)

    def run_gate(self):
        self.path.write_text(json.dumps(self.candidate))
        return validate_candidate(self.path, self.root)

    def assertRejected(self, match):
        result = self.run_gate()
        self.assertFalse(result['approved_for_brief'], result)
        self.assertFalse(result['valid'], result)
        self.assertIn(match, '; '.join(result['errors']))

    def mutate_report(self, eid, mutate):
        entry = next(e for e in self.candidate['evidence'] if e['id'] == eid)
        path = self.root / entry['path']
        report = json.loads(path.read_text())
        mutate(report)
        raw = json.dumps(report).encode()
        path.write_bytes(raw)
        entry['sha256'] = digest(raw)

    def rebind_brief(self, mutate):
        artifact = self.candidate['artifacts']['brief']
        path = self.root / artifact['path']
        brief = json.loads(path.read_text())
        mutate(brief)
        raw = json.dumps(brief).encode()
        path.write_bytes(raw)
        artifact['sha256'] = digest(raw)
        # Simulate a newly reviewed frozen brief, including every report binding.
        subject = self.candidate['approval'].get('subject')
        if subject:
            subject['brief_sha256'] = artifact['sha256']
        for stage in self.candidate['stages'].values():
            if stage.get('subject'):
                stage['subject']['brief_sha256'] = artifact['sha256']
        for item in self.candidate['evidence']:
            item['subject']['brief_sha256'] = artifact['sha256']
            if item['kind'] != 'rendered_image':
                self.mutate_report(item['id'], lambda report: report['subject'].update(brief_sha256=artifact['sha256']))

        self.rebind_review_evidence()
        if self.candidate['approval'].get('status') == 'approved_for_brief':
            self.candidate['approval']['review_snapshot_sha256'] = approval_snapshot_sha256(self.candidate)

    def rebind_review_evidence(self):
        for stage, entry in self.candidate['stages'].items():
            external = [item for item in self.candidate['evidence'] if item['id'] in entry['evidence'] and item['kind'] != REPORT_KIND[stage]]
            for item in self.candidate['evidence']:
                if item['id'] in entry['evidence'] and item['kind'] == REPORT_KIND[stage]:
                    self.mutate_report(item['id'], lambda report: report.update(reviewed_evidence=[{'id': e['id'], 'sha256': e['sha256']} for e in external]))

    def test_complete_fixture_is_approved_without_publication_authority(self):
        result = self.run_gate()
        self.assertTrue(result['valid'], result)
        self.assertTrue(result['approved_for_brief'], result)
        self.assertIn('Publication authority is always separate', result['limitations'])

    def test_pending_is_valid_but_require_approved_cli_fails(self):
        self.candidate, self.path = build_fixture(self.root, approved=False)
        result = self.run_gate()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['approved_for_brief'])
        command = [sys.executable, str(Path(__file__).with_name('validate_candidate.py')), str(self.path), '--root', str(self.root), '--json']
        normal = subprocess.run(command, capture_output=True, text=True)
        strict = subprocess.run(command + ['--require-approved'], capture_output=True, text=True)
        self.assertEqual(normal.returncode, 0, normal.stdout)
        self.assertEqual(strict.returncode, 1, strict.stdout)

    def test_image_tamper_invalidates_approval(self):
        (self.root / 'candidate-fixture/frame-000.png').write_bytes(png() + b'tampered')
        self.assertRejected('SHA-256 mismatch')

    def test_glb_tamper_invalidates_approval(self):
        with (self.root / self.candidate['artifacts']['glb']['path']).open('ab') as stream:
            stream.write(b'tamper')
        self.assertRejected('SHA-256 mismatch')

    def test_brief_tamper_invalidates_approval(self):
        with (self.root / self.candidate['artifacts']['brief']['path']).open('ab') as stream:
            stream.write(b' ')
        self.assertRejected('SHA-256 mismatch')

    def test_reference_ledger_tamper_invalidates_approval(self):
        with (self.root / self.candidate['artifacts']['references']['path']).open('ab') as stream:
            stream.write(b' ')
        self.assertRejected('SHA-256 mismatch')

    def test_self_review_identity_rejected(self):
        self.candidate['stages']['visual']['reviewer']['id'] = self.candidate['maker']['id']
        self.assertRejected('independent reviewer')

    def test_self_review_task_rejected(self):
        self.candidate['stages']['factual']['reviewer']['task_id'] = self.candidate['maker']['task_id']
        self.assertRejected('independent reviewer')

    def test_technical_automation_may_share_maker_task(self):
        self.candidate['stages']['technical']['reviewer'] = {'id': 'tool:qa-glb', 'task_id': self.candidate['maker']['task_id']}
        self.candidate['approval']['review_snapshot_sha256'] = approval_snapshot_sha256(self.candidate)
        self.assertTrue(self.run_gate()['approved_for_brief'])

    def test_relabeled_parse_report_is_not_gpu_rendering(self):
        self.mutate_report('gpu-report', lambda report: report.update(runtime={'engine': 'Three.js', 'version': 'test', 'loader': 'GLTFLoader', 'parsed': True}))
        self.assertRejected('runtime.renderer')

    def test_gpu_no_frame_rejected(self):
        self.mutate_report('gpu-report', lambda report: report['runtime'].update(rendered_frames=0))
        self.assertRejected('rendered_frames')

    def test_gpu_no_screenshot_rejected(self):
        self.mutate_report('gpu-report', lambda report: report.update(screenshots=[]))
        self.assertRejected('screenshot evidence')

    def test_gpu_context_failure_rejected(self):
        self.mutate_report('gpu-report', lambda report: report['runtime'].update(context_created=False))
        self.assertRejected('actual GPU context')

    def test_missing_evidence_file_rejected(self):
        (self.root / self.candidate['evidence'][0]['path']).unlink()
        self.assertRejected('missing file')

    def test_zero_evidence_pass_rejected(self):
        self.candidate['stages']['factual']['evidence'] = []
        self.assertRejected('zero-evidence')

    def test_unrelated_evidence_subject_rejected(self):
        self.candidate['evidence'][0]['subject']['glb_sha256'] = 'a' * 64
        self.assertRejected('stale or unrelated evidence')

    def test_unrelated_report_internals_rejected_despite_descriptor(self):
        self.mutate_report('factual-report', lambda report: report['subject'].update(glb_sha256='b' * 64))
        self.assertRejected('stale or unrelated evidence')

    def test_unrelated_stage_evidence_rejected(self):
        self.candidate['stages']['factual']['evidence'] = ['technical-report']
        self.assertRejected('unrelated evidence')

    def test_open_blocker_prevents_approval(self):
        self.candidate['blockers'] = [{'id': 'bad-foot', 'status': 'open', 'description': 'Visible placement problem'}]
        self.assertRejected('open blocker')

    def test_stale_stage_prevents_approval(self):
        self.candidate['stages']['visual']['status'] = 'stale'
        self.assertRejected('visual: stale')

    def test_unknown_gpu_is_honest_pending_not_approved(self):
        self.candidate['approval'] = {'status': 'pending'}
        self.candidate['stages']['gpu']['status'] = 'unknown'
        result = self.run_gate()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['approved_for_brief'])

    def test_fake_status_rejected(self):
        self.candidate['stages']['gpu']['status'] = 'pass_with_fallback'
        self.assertRejected('invalid status')

    def test_production_runtime_cannot_be_waived(self):
        self.candidate['stages']['gpu']['status'] = 'not_applicable'
        self.assertRejected('mandatory stage cannot be waived')

    def test_missing_stage_rejected(self):
        del self.candidate['stages']['scene']
        self.assertRejected('all seven')

    def test_missing_criterion_rejected(self):
        self.candidate['stages']['factual']['criteria'] = []
        self.assertRejected('missing explicit criterion')

    def test_uninspected_source_rejected(self):
        self.candidate['stages']['factual']['inspected_references'] = []
        self.assertRejected('actual inspected reference')

    def test_critical_source_obligation_cannot_be_removed(self):
        self.rebind_brief(lambda brief: brief['criteria'][2].update(required_sources=[]))
        self.assertRejected('critical factual criterion needs required_sources')

    def test_numeric_budget_independently_enforced(self):
        self.rebind_brief(lambda brief: brief['geometry_policy'].update(max_glb_bytes=1))
        self.assertRejected('max_glb_bytes')

    def test_fake_numeric_measurement_rejected(self):
        self.mutate_report('technical-report', lambda report: report['measurements'].update(triangles=999))
        self.assertRejected('differs from measured')

    def test_inspection_frame_omission_rejected(self):
        self.candidate['stages']['visual']['inspected_frames'].pop()
        self.assertRejected('all planned frames')

    def test_missing_view_rejected(self):
        self.mutate_report('visual-renders', lambda report: report.update(frames=[frame for frame in report['frames'] if frame['view'] != 'bottom']))
        self.rebind_review_evidence()
        self.assertRejected('required views missing')

    def test_insufficient_turntable_rejected(self):
        self.mutate_report('visual-renders', lambda report: report.update(frames=report['frames'][:-1]))
        self.rebind_review_evidence()
        self.assertRejected('insufficient distinct turntable')

    def test_clustered_turntable_rejected(self):
        def mutate(report):
            for i, frame in enumerate(f for f in report['frames'] if f['view'] == 'turntable'):
                frame['angle_degrees'][0] = i
        self.mutate_report('visual-renders', mutate)
        self.assertRejected('frozen render-config plan')

    def test_reduced_turntable_plan_requires_justification(self):
        self.rebind_brief(lambda brief: brief.update(turntable_frames=4, coverage_justification=''))
        self.assertRejected('coverage_justification')

    def test_config_tamper_invalidates_render_evidence(self):
        (self.root / 'candidate-fixture/render-config.json').write_text('{}')
        self.assertRejected('SHA-256 mismatch')

    def test_old_stage_hashes_fail_after_rehashing_new_brief(self):
        path = self.root / self.candidate['artifacts']['brief']['path']
        path.write_bytes(path.read_bytes() + b' ')
        self.candidate['artifacts']['brief']['sha256'] = digest(path.read_bytes())
        self.assertRejected('stale or unrelated evidence')

    def test_immutable_revision_detected_with_previous_snapshot(self):
        self.candidate, self.path = build_fixture(self.root, approved=False)
        old = copy.deepcopy(self.candidate)
        old['artifacts']['glb']['sha256'] = 'a' * 64
        previous = self.root / 'previous.json'
        previous.write_text(json.dumps(old))
        self.path.write_text(json.dumps(self.candidate))
        result = validate_candidate(self.path, self.root, previous)
        self.assertFalse(result['valid'])
        self.assertIn('immutable revision', result['errors'][0])

    def test_no_external_path_escape(self):
        self.candidate['artifacts']['glb']['path'] = '../outside.glb'
        self.assertRejected('safe repository-relative')

    def test_no_symlink_substitution(self):
        original = self.root / 'candidate-fixture/model.glb'
        moved = self.root / 'candidate-fixture/other.glb'
        original.rename(moved)
        original.symlink_to(moved)
        self.assertRejected('symlink substitutions')

    def test_approval_identity_must_be_independent(self):
        self.candidate['approval']['reviewer'] = self.candidate['maker'].copy()
        self.assertRejected('independent reviewer')

    def test_screenshot_is_not_factual_report(self):
        self.candidate['evidence'] = [entry for entry in self.candidate['evidence'] if entry['id'] != 'factual-report']
        shot = {'id': 'factual-shot', 'kind': 'rendered_image', 'stage': 'factual',
                'subject': self.candidate['approval']['subject'].copy(),
                'path': 'candidate-fixture/gpu.png', 'sha256': digest(png())}
        self.candidate['evidence'].append(shot)
        self.candidate['stages']['factual']['evidence'] = ['factual-shot']
        self.assertRejected('passing structured reference_comparison')


    def mutate_raw_check(self, name, mutate):
        def update(report):
            check = next(check for check in report['checks'] if check['name'] == name)
            path = self.root / check['report']['path']
            raw = json.loads(path.read_text())
            mutate(raw)
            data = json.dumps(raw).encode()
            path.write_bytes(data)
            check['report']['sha256'] = digest(data)
        self.mutate_report('technical-report', update)

    def test_arbitrary_technical_check_is_insufficient(self):
        self.mutate_report('technical-report', lambda report: report.update(checks=[{'name': 'anything', 'status': 'pass'}]))
        self.assertRejected('named static_glb')

    def test_khronos_errors_prevent_pass(self):
        self.mutate_raw_check('khronos_validator', lambda raw: raw['issues'].update(numErrors=1))
        self.assertRejected('Khronos report has errors')

    def test_khronos_truncated_prevents_pass(self):
        self.mutate_raw_check('khronos_validator', lambda raw: raw['issues'].update(truncated=True))
        self.assertRejected('must not be truncated')

    def test_khronos_warnings_require_rationale(self):
        self.mutate_raw_check('khronos_validator', lambda raw: raw['issues'].update(numWarnings=1, messages=[{'severity': 1, 'code': 'SYNTHETIC_WARNING'}]))
        self.assertRejected('every raw warning needs explicit review')

    def test_source_export_comparison_required(self):
        self.mutate_raw_check('source_export', lambda raw: raw.update(bounds_match=False))
        self.assertRejected('axis-converted bounds comparison')

    def test_rebuild_semantic_mismatch_prevents_pass(self):
        self.mutate_raw_check('reproducibility', lambda raw: raw.update(rebuilt_semantic_sha256='a' * 64))
        self.assertRejected('rebuilt semantic digest')

    def test_production_missing_source_deliverable_prevents_pass(self):
        self.rebind_brief(lambda brief: brief.update(required_deliverables=[]))
        self.assertRejected('source/generator/config')

    def test_source_tamper_invalidates_approval(self):
        (self.root / self.candidate['artifacts']['source']['path']).write_text('changed source')
        self.assertRejected('SHA-256 mismatch')

    def test_texture_bytes_dimensions_provenance_and_budget_pass(self):
        self.candidate, self.path = build_fixture(self.root, textured=True)
        result = self.run_gate()
        self.assertTrue(result['approved_for_brief'], result)
        self.assertEqual(result['measurements']['texture_count'], 1)
        self.assertEqual(result['measurements']['decoded_texture_bytes_estimate'], 4)

    def test_missing_texture_provenance_rejected(self):
        self.candidate, self.path = build_fixture(self.root, textured=True)
        self.candidate['textures'] = []
        self.assertRejected('provenance entry required')

    def test_unknown_texture_provenance_source_rejected(self):
        self.candidate, self.path = build_fixture(self.root, textured=True)
        self.candidate['textures'][0]['provenance']['source_id'] = 'unrelated-source'
        self.assertRejected('provenance source')

    def test_texture_budget_cannot_be_faked(self):
        self.candidate, self.path = build_fixture(self.root, textured=True)
        self.rebind_brief(lambda brief: brief['texture_policy'].update(max_total_bytes=0))
        self.assertRejected('max_total_bytes')

    def test_decoded_texture_budget_enforced_with_explicit_assumptions(self):
        self.candidate, self.path = build_fixture(self.root, textured=True)
        self.rebind_brief(lambda brief: brief['texture_policy'].update(max_decoded_bytes=0))
        self.assertRejected('max_decoded_bytes')

    def test_render_manifest_partial_is_valid_if_review_pending(self):
        self.mutate_report('visual-renders', lambda report: report.update(frames=report['frames'][:1]))
        self.candidate['stages']['visual']['status'] = 'unknown'
        self.candidate['approval'] = {'status': 'pending'}
        result = self.run_gate()
        self.assertTrue(result['valid'], result)
        self.assertFalse(result['approved_for_brief'])

    def test_case_whitespace_cannot_disguise_self_review(self):
        self.candidate['stages']['visual']['reviewer']['id'] = self.candidate['maker']['id'].upper() + ' '
        self.assertRejected('independent reviewer')

    def test_study_can_waive_noncritical_gpu_scene_but_not_core(self):
        self.candidate, self.path = build_fixture(self.root, profile='study', approved=False)
        for stage in ('gpu', 'scene'):
            self.candidate['stages'][stage]['status'] = 'not_applicable'
        result = self.run_gate()
        self.assertTrue(result['valid'], result)
        self.candidate['stages']['runtime_parse']['status'] = 'not_applicable'
        self.assertRejected('mandatory stage cannot be waived')


    def test_webp_lossy_lossless_extended_dimensions(self):
        # Real 7x3 WebP encodes; fixtures are embedded so Pillow is not a test dependency.
        fixtures = [
            'UklGRjwAAABXRUJQVlA4IDAAAADQAQCdASoHAAMAAUAmJaACdLoB+AADsAD+8ut//NgVzXPv9//S4P0uD9Lg/9KQAAA=',
            'UklGRhwAAABXRUJQVlA4TA8AAAAvBoAAAAcQ/Y/+ByKi/wEA',
            'UklGRmAAAABXRUJQVlA4WAoAAAAQAAAABgAAAgAAQUxQSAoAAAABB1DAiAhERP8DVlA4IDAAAADQAQCdASoHAAMAAUAmJaACdLoB+AADsAD+8ut//NgVzXPv9//S4P0uD9Lg/9KQAAA=']
        for encoded in fixtures:
            self.assertEqual(image_size(base64.b64decode(encoded)), (7, 3))

    def test_truncated_webp_rejected(self):
        raw = base64.b64decode('UklGRhwAAABXRUJQVlA4TA8AAAAvBoAAAAcQ/Y/+ByKi/wEA')
        with self.assertRaisesRegex(ValueError, 'invalid WebP RIFF length'):
            image_size(raw[:-1])

    def test_unsupported_image_format_fails_honestly(self):
        with self.assertRaisesRegex(ValueError, 'PNG/JPEG/WebP'):
            image_size(b'not-an-image')

    def test_manifest_angles_must_match_frozen_config(self):
        self.mutate_report('visual-renders', lambda report: report['frames'][0].update(angle_degrees=[12, 13]))
        self.assertRejected('frozen render-config plan')

    def test_reduced_production_plan_allowed_with_coverage_justification(self):
        self.rebind_brief(lambda brief: brief.update(turntable_frames=12, coverage_justification='Simple synthetic shape; extra existing frame coverage retained.'))
        self.assertTrue(self.run_gate()['approved_for_brief'])

    def test_explicit_detail_exemption_allowed_for_inapplicable_subject(self):
        self.rebind_brief(lambda brief: brief.update(required_views=[v for v in brief['required_views'] if v != 'detail'],
                                                    view_exemptions={'detail': 'Synthetic featureless fixture; no discrete subject detail.'}))
        self.assertTrue(self.run_gate()['approved_for_brief'])

    def test_core_angle_view_cannot_be_exempt(self):
        self.rebind_brief(lambda brief: brief.update(view_exemptions={'bottom': 'Skipped'}))
        self.assertRejected('only detail')


    def test_json_overflow_rejected_at_any_nesting_depth(self):
        for raw in (b'{"unused":1e309}', b'{"unused":[{"deep":-1e309}]}'):
            with self.assertRaisesRegex(ValueError, 'nonfinite JSON number'):
                json_bytes(raw, 'overflow fixture')

    def test_gpu_exposure_numeric_overflow_cannot_approve(self):
        self.mutate_report('gpu-report', lambda report: report['runtime'].update(exposure=float('inf')))
        entry = next(entry for entry in self.candidate['evidence'] if entry['id'] == 'gpu-report')
        path = self.root / entry['path']
        # A valid JSON exponent, not the already-rejected nonstandard Infinity token.
        raw = path.read_bytes().replace(b'Infinity', b'1e309')
        path.write_bytes(raw)
        entry['sha256'] = digest(raw)
        self.assertRejected('nonfinite JSON number')

    def test_matching_config_manifest_overflow_angles_cannot_approve(self):
        entry = next(entry for entry in self.candidate['evidence'] if entry['id'] == 'visual-renders')
        path = self.root / entry['path']
        manifest = json.loads(path.read_text())
        config_path = path.parent / manifest['render_config']['path']
        config = json.loads(config_path.read_text())
        for frame in config['frames'] + manifest['frames']:
            if frame['view'] == 'turntable':
                frame['angle_degrees'] = [float('inf'), 0]
        raw = json.dumps(config).replace('Infinity', '1e309').encode()
        config_path.write_bytes(raw)
        manifest['render_config']['sha256'] = digest(raw)
        raw = json.dumps(manifest).replace('Infinity', '1e309').encode()
        path.write_bytes(raw)
        entry['sha256'] = digest(raw)
        self.assertRejected('nonfinite JSON number')

    def test_direct_manifest_api_also_rejects_nonfinite_angles(self):
        entry = next(entry for entry in self.candidate['evidence'] if entry['id'] == 'visual-renders')
        manifest = json.loads((self.root / entry['path']).read_text())
        manifest['frames'][0]['angle_degrees'] = [float('inf'), 0]
        brief = json.loads((self.root / self.candidate['artifacts']['brief']['path']).read_text())
        with self.assertRaisesRegex(ValueError, 'finite azimuth/elevation'):
            check_render_manifest(manifest, entry, entry['subject'], brief, self.root)


    def test_rehashed_reviewed_frame_invalidates_unchanged_review(self):
        entry = next(e for e in self.candidate['evidence'] if e['id'] == 'visual-renders')
        path = self.root / entry['path']
        manifest = json.loads(path.read_text())
        frame = manifest['frames'][0]
        image_path = path.parent / frame['path']
        raw = image_path.read_bytes() + b'changed exact image bytes'
        image_path.write_bytes(raw)
        frame.update(sha256=digest(raw), byte_length=len(raw))
        encoded = json.dumps(manifest).encode()
        path.write_bytes(encoded)
        entry['sha256'] = digest(encoded)
        self.assertRejected('stale reviewed evidence')

    def test_rehashed_gpu_screenshot_invalidates_unchanged_review(self):
        entry = next(e for e in self.candidate['evidence'] if e['id'] == 'gpu-shot')
        path = self.root / entry['path']
        raw = path.read_bytes() + b'changed bytes'
        path.write_bytes(raw)
        entry['sha256'] = digest(raw)
        self.assertRejected('stale reviewed evidence')

    def test_changed_review_report_requires_new_final_approval(self):
        self.mutate_report('factual-report', lambda report: report['observations'].append('New review observation.'))
        self.assertRejected('stale review snapshot')

    def test_changed_criterion_requires_new_final_approval(self):
        self.candidate['stages']['factual']['criteria'][0]['note'] = 'Changed review decision rationale.'
        self.assertRejected('stale review snapshot')

    def test_suppressed_current_static_warning_rejected(self):
        # Supply a fresh audit with a known warning, then keep raw status pass.
        # This uses the real GLB bytes and rebinding steps, never a mock audit.
        from qa_glb import read_glb
        glb = self.root / self.candidate['artifacts']['glb']['path']
        document, binary, _ = read_glb(glb)
        document['materials'][0]['doubleSided'] = True
        glb.write_bytes(encode(document, binary))
        sha = digest(glb.read_bytes())
        audit = audit_glb(glb)
        self.candidate['artifacts']['glb']['sha256'] = sha
        self.candidate['approval']['subject']['glb_sha256'] = sha
        for stage in self.candidate['stages'].values():
            stage['subject']['glb_sha256'] = sha
        for entry in self.candidate['evidence']:
            entry['subject']['glb_sha256'] = sha
            if entry['kind'] == 'rendered_image':
                continue
            def update(report):
                report['subject']['glb_sha256'] = sha
                if report.get('stage') == 'scene':
                    report['scene_assets'][0]['glb_sha256'] = sha
                if report.get('stage') == 'technical':
                    report['measurements']['glb_bytes'] = glb.stat().st_size
                    for check in report['checks']:
                        check['glb_sha256'] = sha
                        raw_path = self.root / check['report']['path']
                        raw = json.loads(raw_path.read_text())
                        if check['name'] == 'static_glb':
                            raw = dict(audit)
                            raw.update(status='pass', warnings=[])
                        elif check['name'] in ('source_export', 'reproducibility'):
                            raw['glb_sha256'] = sha
                            if check['name'] == 'reproducibility':
                                raw['semantic_sha256'] = raw['rebuilt_semantic_sha256'] = audit['semantic_sha256']
                        data = json.dumps(raw).encode()
                        raw_path.write_bytes(data)
                        check['report']['sha256'] = digest(data)
            self.mutate_report(entry['id'], update)
        self.assertRejected('current independent audit')


    def test_null_rebuilt_hash_cannot_match_null_run_output(self):
        def mutate(raw):
            raw['rebuilt_glb_sha256'] = None
            path = self.root / raw['build_run']['result']['path']
            result = json.loads(path.read_text())
            result['outputs'][raw['build_run']['output']]['sha256'] = None
            encoded = json.dumps(result).encode()
            path.write_bytes(encoded)
            raw['build_run']['result']['sha256'] = digest(encoded)
        self.mutate_raw_check('reproducibility', mutate)
        self.assertRejected('nonempty exact rebuilt GLB SHA-256')

    def test_duplicate_json_keys_rejected(self):
        self.path.write_text('{"schema_version":1,"schema_version":1}')
        result = validate_candidate(self.path, self.root)
        self.assertFalse(result['valid'])
        self.assertIn('duplicate JSON key', result['errors'][0])


class RecoveredEnvironmentPropTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.candidate, self.path = build_fixture(self.root, quality_tier='environment-prop')

    def test_six_views_zero_orbit_preserves_all_stages(self):
        result = validate_candidate(self.path, self.root)
        self.assertTrue(result['approved_for_brief'], result)
        self.assertEqual(set(result['required_stages']), set(STAGES))

    def test_gpu_still_cannot_be_waived(self):
        self.candidate['stages']['gpu']['status'] = 'not_applicable'
        self.path.write_text(json.dumps(self.candidate))
        result = validate_candidate(self.path, self.root)
        self.assertFalse(result['approved_for_brief'], result)
        self.assertIn('mandatory stage cannot be waived', str(result))

    def test_missing_meaningful_view_rejected(self):
        item = self.candidate['artifacts']['brief']
        path = self.root / item['path']
        brief = json.loads(path.read_text())
        brief['required_views'].remove('clay')
        path.write_text(json.dumps(brief))
        item['sha256'] = digest(path.read_bytes())
        self.path.write_text(json.dumps(self.candidate))
        result = validate_candidate(self.path, self.root)
        self.assertFalse(result['valid'], result)
        self.assertIn('hero/front/right/rear/top/clay', str(result))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--write-fixture':
        _, path = build_fixture(sys.argv[2], base=sys.argv[3] if len(sys.argv) > 3 else 'candidate-fixture',
                                glb_name=sys.argv[4] if len(sys.argv) > 4 else 'model.glb')
        print(path)
    else:
        unittest.main()
