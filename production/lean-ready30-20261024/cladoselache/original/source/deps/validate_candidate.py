#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fail-closed evidence/obligation gate, NOT an artistic or scientific oracle.

A valid pending record is not an approval. Hashes bind reports to exact inputs;
review identities and observations remain auditable attestations, not proof that
someone looked at an image. This command never publishes or edits any file.
"""
import argparse
import copy
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import struct
import sys

from qa_glb import audit_glb, read_glb
from check_reproducibility import validate_build_run

STAGES = ('technical', 'visual', 'factual', 'specification', 'runtime_parse', 'gpu', 'scene')
CORE = frozenset(STAGES[:5])
INDEPENDENT = frozenset(('visual', 'factual', 'specification'))
STATUSES = frozenset(('pass', 'fail', 'unknown', 'not_applicable', 'stale'))
REPORT_KIND = dict(zip(STAGES, ('technical_report', 'visual_report', 'reference_comparison',
                              'spec_report', 'runtime_parse_report', 'gpu_report', 'scene_report')))
GEOMETRY = {'triangles': 'max_triangles', 'materials': 'max_materials',
            'primitives': 'max_primitives', 'glb_bytes': 'max_glb_bytes'}
TEXTURE = {'texture_count': 'max_textures', 'texture_max_dimension': 'max_dimension',
           'texture_bytes': 'max_total_bytes'}
PRODUCTION_VIEWS = frozenset(('front', 'rear', 'left', 'right', 'top', 'bottom', 'clay', 'wire', 'detail'))
LEGACY_PROFILE = 'legacy-v1'
STATIC_PROFILE = 'static-stylized-v1'
PROFILE_RULE_VERSION = '2026-10-18.1'
STATIC_VIEWS = frozenset(('hero', 'reversehero', 'front', 'side', 'rear', 'top', 'clay', 'silhouette'))
CONSULTED_USE = 'consulted-only; no source media, mesh or texture incorporated'
SHA = re.compile(r'^[a-f0-9]{64}$')
ID = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._:-]*$')
LIMITATIONS = ('Checks evidence integrity and recorded obligations only; it does not prove visual quality, '
               'scientific truth, reviewer identity, or actual human inspection. Approval is for the frozen '
               'brief only. Publication authority is always separate.')


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def obj(value, label):
    need(isinstance(value, dict), f'{label}: expected object')
    return value


def arr(value, label):
    need(isinstance(value, list), f'{label}: expected array')
    return value


def text(value, label):
    need(isinstance(value, str) and bool(value.strip()), f'{label}: nonempty text required')
    return value


def integer(value, label, minimum=0):
    need(type(value) is int and value >= minimum, f'{label}: integer >= {minimum} required')
    return value


def identifier(value, label):
    need(isinstance(value, str) and bool(ID.fullmatch(value)), f'{label}: invalid identifier')
    return value


def unique(values, label):
    arr(values, label)
    for item in values:
        text(item, label)
    need(len(values) == len(set(values)), f'{label}: duplicate entries')
    return values


def timestamp(value, label):
    text(value, label)
    try:
        stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
        need(stamp.tzinfo is not None, f'{label}: timezone required')
    except ValueError as exc:
        raise Invalid(f'{label}: invalid ISO timestamp') from exc


def identity(value, label, maker=None):
    obj(value, label)
    text(value.get('id'), f'{label}.id')
    text(value.get('task_id'), f'{label}.task_id')
    if maker:
        need(value['id'].strip().casefold() != maker['id'].strip().casefold() and value['task_id'].strip().casefold() != maker['task_id'].strip().casefold(),
             f'{label}: independent reviewer identity AND task must differ from maker')


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Invalid(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def finite_float(token):
    # JSON numeric syntax permits 1e309; Python's float decoder otherwise turns
    # it into infinity even though the nonstandard Infinity token is rejected.
    value = float(token)
    need(math.isfinite(value), f'nonfinite JSON number: {token}')
    return value


def finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except (OverflowError, ValueError):
        return False


def json_bytes(raw, label):
    try:
        return json.loads(raw, object_pairs_hook=no_duplicates, parse_float=finite_float,
                          parse_constant=lambda value: (_ for _ in ()).throw(Invalid(f'nonfinite JSON: {value}')))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Invalid(f'{label}: invalid JSON: {exc}') from exc


def relative_file(root, name, label):
    text(name, f'{label}.path')
    path = PurePosixPath(name)
    need(not path.is_absolute() and '\\' not in name and all(p not in ('.', '..') for p in name.split('/')),
         f'{label}: safe repository-relative path required')
    full = root.joinpath(*path.parts)
    need(full.resolve().is_relative_to(root), f'{label}: path escapes root')
    # Do not silently change the file identity through a symlink at any level.
    current = root
    for part in path.parts:
        current = current / part
        need(not current.is_symlink(), f'{label}: symlink substitutions are not allowed')
    need(full.is_file(), f'{label}: missing file {name}')
    return full


def checked_file(root, entry, label):
    obj(entry, label)
    need(isinstance(entry.get('sha256'), str) and bool(SHA.fullmatch(entry['sha256'])), f'{label}: exact SHA-256 required')
    full = relative_file(root, entry.get('path'), label)
    raw = full.read_bytes()
    need(bool(raw), f'{label}: empty evidence/artifact')
    need(hashlib.sha256(raw).hexdigest() == entry['sha256'], f'{label}: SHA-256 mismatch (stale input/evidence)')
    return full, raw


def image_size(raw):
    """Measure PNG/JPEG/WebP headers without optional image packages; not an image-quality test."""
    if raw.startswith(b'\x89PNG\r\n\x1a\n') and len(raw) >= 24 and raw[12:16] == b'IHDR':
        return struct.unpack('>II', raw[16:24])
    if raw.startswith(b'\xff\xd8'):
        offset = 2
        while offset + 4 <= len(raw):
            if raw[offset] != 255:
                break
            while offset < len(raw) and raw[offset] == 255:
                offset += 1
            if offset >= len(raw):
                break
            marker = raw[offset]
            offset += 1
            if marker in (0xd8, 0xd9) or 0xd0 <= marker <= 0xd7:
                continue
            if offset + 2 > len(raw):
                break
            length = int.from_bytes(raw[offset:offset+2], 'big')
            if length < 2 or offset + length > len(raw):
                break
            if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf) and length >= 7:
                height, width = struct.unpack('>HH', raw[offset+3:offset+7])
                return width, height
            offset += length
    if raw.startswith(b'RIFF') and len(raw) >= 20 and raw[8:12] == b'WEBP':
        need(int.from_bytes(raw[4:8], 'little') + 8 == len(raw), 'image: invalid WebP RIFF length')
        offset = 12
        while offset + 8 <= len(raw):
            kind, length = raw[offset:offset+4], int.from_bytes(raw[offset+4:offset+8], 'little')
            data = raw[offset+8:offset+8+length]
            need(len(data) == length, 'image: truncated WebP chunk')
            if kind == b'VP8X' and len(data) >= 10:
                return 1 + int.from_bytes(data[4:7], 'little'), 1 + int.from_bytes(data[7:10], 'little')
            if kind == b'VP8L' and len(data) >= 5 and data[0] == 0x2f:
                bits = int.from_bytes(data[1:5], 'little')
                return (bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1
            if kind == b'VP8 ' and len(data) >= 10 and data[3:6] == b'\x9d\x01\x2a':
                return int.from_bytes(data[6:8], 'little') & 0x3fff, int.from_bytes(data[8:10], 'little') & 0x3fff
            offset += 8 + length + (length % 2)
    raise Invalid('image: supported PNG/JPEG/WebP dimensions could not be read')


def check_subject(value, expected, label):
    need(value == expected, f'{label}: subject differs from exact revision/GLB/brief/reference hashes (stale or unrelated evidence)')


def check_brief(brief, record, sources, validation_profile=LEGACY_PROFILE):
    obj(brief, 'brief')
    need(brief.get('schema_version') == 1, 'brief: unsupported schema_version')
    need(brief.get('asset_id') == record['asset_id'], 'brief: asset_id mismatch')
    identifier(brief.get('brief_version'), 'brief.brief_version')
    need(brief.get('profile') in ('study', 'production'), 'brief: profile must be study or production')
    need(brief.get('publication_authority') == 'separate', 'brief: publication authority must remain separate')
    requested = unique(brief.get('required_stages'), 'brief.required_stages')
    need(set(requested) <= set(STAGES), 'brief: unknown required stage')
    required = set(CORE) | set(requested)
    if brief['profile'] == 'production':
        required |= {'gpu', 'scene'}
    views = unique(brief.get('required_views'), 'brief.required_views')
    need(views and 'turntable' not in views, 'brief: named required views exclude turntable frames')
    if validation_profile == STATIC_PROFILE:
        frames = integer(brief.get('turntable_frames'), 'brief.turntable_frames')
        need(frames == 0 and set(views) == STATIC_VIEWS,
             'static-stylized-v1: exactly eight fixed views and zero turntable frames required')
    else:
        frames = integer(brief.get('turntable_frames'), 'brief.turntable_frames', 2)
    exemptions = obj(brief.get('view_exemptions', {}), 'brief.view_exemptions')
    need(set(exemptions) <= {'detail'}, 'brief: only detail may be explicitly inapplicable')
    for view, reason in exemptions.items():
        text(reason, f'brief.view_exemptions.{view}')
        need(view not in views, f'brief: {view} cannot be required and exempt')
    if brief['profile'] == 'production' and validation_profile == LEGACY_PROFILE:
        need(PRODUCTION_VIEWS - set(exemptions) <= set(views),
             'brief: production requires full front/rear/left/right/top/bottom/clay/wire/detail coverage')
    if frames < 24:
        text(brief.get('coverage_justification'), 'brief.coverage_justification for fewer than 24 turntable frames')
    criteria = {}
    for item in arr(brief.get('criteria'), 'brief.criteria'):
        obj(item, 'brief criterion')
        cid = identifier(item.get('id'), 'criterion.id')
        need(cid not in criteria, f'brief: duplicate criterion {cid}')
        need(item.get('stage') in STAGES, f'{cid}: unknown stage')
        need(type(item.get('critical')) is bool, f'{cid}: explicit critical boolean required')
        text(item.get('description'), f'{cid}.description')
        refs = unique(item.get('required_sources', []), f'{cid}.required_sources')
        need(set(refs) <= sources, f'{cid}: unknown required source')
        if item['stage'] == 'factual' and item['critical']:
            need(refs, f'{cid}: critical factual criterion needs required_sources')
        if 'allow_not_applicable' in item:
            need(type(item['allow_not_applicable']) is bool, f'{cid}: allow_not_applicable must be boolean')
        need(not (item['critical'] and item.get('allow_not_applicable')), f'{cid}: critical criterion cannot be waived')
        if item['critical']:
            required.add(item['stage'])
        criteria[cid] = item
    for stage in required:
        need(any(c['stage'] == stage for c in criteria.values()), f'brief: required {stage} stage needs explicit criteria')
    need(any(c['stage'] == 'factual' and c['critical'] for c in criteria.values()),
         'brief: at least one critical factual/reference obligation required')
    for policy, keys in (('geometry_policy', GEOMETRY.values()), ('texture_policy', TEXTURE.values())):
        obj(brief.get(policy), f'brief.{policy}')
        for key in keys:
            integer(brief[policy].get(key), f'brief.{policy}.{key}', 1 if policy == 'geometry_policy' else 0)
    if 'max_decoded_bytes' in brief['texture_policy']:
        integer(brief['texture_policy']['max_decoded_bytes'], 'brief.texture_policy.max_decoded_bytes')
    return required, criteria


def approval_snapshot_sha256(record):
    # Approval is outside this snapshot, so no evidence/report self-hash cycle.
    snapshot = {key: record.get(key) for key in ('asset_id', 'revision', 'maker', 'artifacts', 'textures',
                                               'evidence', 'stages', 'blockers', 'supersedes')}
    encoded = json.dumps(snapshot, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def check_report(report, evidence, expected, stage, measured, evidence_by_id, root, artifacts, profile, fresh_audit):
    label = evidence['id']
    obj(report, label)
    need(report.get('schema_version') == 1, f'{label}: report schema_version required')
    need(report.get('kind') == REPORT_KIND[stage] and report.get('stage') == stage,
         f'{label}: report content kind/stage mismatch')
    check_subject(report.get('subject'), expected, label)
    need(report.get('status') in ('pass', 'fail', 'unknown', 'stale'), f'{label}: invalid report status')
    text(report.get('method'), f'{label}.method')
    observations = arr(report.get('observations'), f'{label}.observations')
    need(observations, f'{label}: report must record actual observations')
    for observation in observations:
        text(observation, f'{label}.observation')
    if report['status'] != 'pass':
        return
    need(arr(report.get('errors'), f'{label}.errors') == [], f'{label}: passing report has errors')
    warnings = arr(report.get('warnings', []), f'{label}.warnings')
    reviews = arr(report.get('warning_review', []), f'{label}.warning_review')
    for review in reviews:
        text(obj(review, 'warning review').get('rationale'), 'warning review rationale')
    need(all(any(review.get('warning') == warning for review in reviews) for warning in warnings),
         f'{label}: every report warning needs explicit review rationale')
    if stage == 'technical':
        metrics = obj(report.get('measurements'), f'{label}.measurements')
        for key in (*GEOMETRY, *TEXTURE):
            integer(metrics.get(key), f'{label}.{key}')
            need(metrics[key] == measured.get(key), f'{label}: {key} differs from measured GLB/texture bytes')
        checks = arr(report.get('checks'), f'{label}.checks')
        names = [obj(check, 'check').get('name') for check in checks]
        expected_checks = {'static_glb', 'khronos_validator', 'source_export', 'reproducibility'}
        need(len(names) == len(set(names)) and expected_checks <= set(names),
             f'{label}: named static_glb/khronos_validator/source_export/reproducibility checks required')
        report_paths = [obj(check.get('report'), 'check.report').get('path') for check in checks]
        need(len(report_paths) == len(set(report_paths)), f'{label}: technical checks need distinct raw report files')
        for check in checks:
            text(check.get('name'), 'check.name')
            need(check.get('status') == 'pass', f'{label}: unresolved technical check')
            need(check.get('glb_sha256') == expected['glb_sha256'], f'{label}: raw check GLB binding mismatch')
            _, check_raw = checked_file(root, check.get('report'), f'{label}.{check["name"]}')
            raw = obj(json_bytes(check_raw, check['name']), check['name'])
            warnings = arr(raw.get('warnings', []), 'check.warnings')
            if check['name'] == 'khronos_validator':
                text(raw.get('validatorVersion'), 'Khronos validatorVersion')
                issues = obj(raw.get('issues'), 'Khronos issues')
                need(type(issues.get('numErrors')) is int and issues['numErrors'] == 0,
                     'Khronos report has errors or missing numErrors')
                need(issues.get('truncated') is False, 'Khronos report must not be truncated')
                integer(issues.get('numWarnings'), 'Khronos numWarnings')
                messages = arr(issues.get('messages'), 'Khronos messages')
                need(not any(obj(message, 'Khronos message').get('severity') == 0 for message in messages),
                     'Khronos report contains error messages')
                warnings = [message for message in messages if message.get('severity') == 1]
                need(len(warnings) == issues['numWarnings'], 'Khronos warning count mismatch')
            else:
                need(raw.get('status') in ('pass', 'pass_with_warnings'), f'{check["name"]}: nonpassing raw report status')
                need(raw.get('sha256', raw.get('glb_sha256')) == expected['glb_sha256'], f'{check["name"]}: raw GLB hash mismatch')
                need(arr(raw.get('errors'), 'check.errors') == [], f'{check["name"]}: raw report errors')
                if check['name'] == 'source_export':
                    need('source' in artifacts and raw.get('source_sha256') == artifacts['source']['sha256'],
                         'source_export: editable source hash missing/mismatched')
                    need(raw.get('triangles_match') is True and raw.get('bounds_match') is True,
                         'source_export: actual source/export count and axis-converted bounds comparison required')
                elif check['name'] == 'reproducibility':
                    for key in ('generator', 'config'):
                        need(key in artifacts and raw.get(key + '_sha256') == artifacts[key]['sha256'],
                             f'reproducibility: {key} hash missing/mismatched')
                    need(raw.get('semantic_sha256') == measured['semantic_sha256']
                         and raw.get('rebuilt_semantic_sha256') == measured['semantic_sha256'],
                         'reproducibility: rebuilt semantic digest differs or missing')
                    run = obj(raw.get('build_run'), 'reproducibility.build_run')
                    _, request_raw = checked_file(root, run.get('request'), 'reproducibility.build_run.request')
                    _, result_raw = checked_file(root, run.get('result'), 'reproducibility.build_run.result')
                    validate_build_run(json_bytes(request_raw, 'build request'), json_bytes(result_raw, 'build result'),
                                       artifacts['generator']['sha256'], artifacts['config']['sha256'],
                                       raw.get('rebuilt_glb_sha256'), run.get('output'))
            if check['name'] == 'static_glb':
                # A hash-bound wrapper must not suppress warnings measured now.
                need(raw.get('status') == fresh_audit['status'] and raw.get('errors') == fresh_audit['errors'],
                     'static_glb: raw status/errors differ from current independent audit')
                need(sorted(json.dumps(w, sort_keys=True) for w in warnings) ==
                     sorted(json.dumps(w, sort_keys=True) for w in fresh_audit['warnings']),
                     'static_glb: raw warnings differ from current independent audit')
            reviews = arr(check.get('warning_review', []), 'check.warning_review')
            for review in reviews:
                text(obj(review, 'warning review').get('rationale'), 'warning review rationale')
            need(all(any(review.get('warning') == warning for review in reviews) for warning in warnings),
                 f'{check["name"]}: every raw warning needs explicit review rationale')
    if stage == 'runtime_parse':
        runtime = obj(report.get('runtime'), f'{label}.runtime')
        for key in ('engine', 'version', 'loader'):
            text(runtime.get(key), f'{label}.runtime.{key}')
        need(runtime.get('parsed') is True, f'{label}: parser did not succeed')
    if stage in ('gpu', 'scene'):
        runtime = obj(report.get('runtime'), f'{label}.runtime')
        for key in ('engine', 'version', 'renderer', 'device', 'browser', 'context', 'output_color_space', 'tone_mapping'):
            text(runtime.get(key), f'{label}.runtime.{key}')
        need(runtime.get('context_created') is True and runtime.get('rendered') is True,
             f'{label}: actual GPU context and rendered frame required; parsing is insufficient')
        for key in ('rendered_frames', 'draw_calls', 'triangles'):
            integer(runtime.get(key), f'{label}.runtime.{key}', 1)
        need(finite_number(runtime.get('exposure')), f'{label}: finite exposure required')
        screenshots = unique(report.get('screenshots'), f'{label}.screenshots')
        need(screenshots, f'{label}: rendered-frame screenshot evidence required')
        for eid in screenshots:
            shot = evidence_by_id.get(eid)
            need(shot is not None and shot['kind'] == 'rendered_image' and shot['stage'] == stage,
                 f'{label}: screenshot {eid} must be same-stage rendered image evidence')
        if stage == 'scene':
            text(report.get('scene_description'), f'{label}.scene_description')
            assets = arr(report.get('scene_assets'), f'{label}.scene_assets')
            need(any(isinstance(asset, dict) and asset.get('glb_sha256') == expected['glb_sha256']
                     and type(asset.get('instances')) is int and asset['instances'] >= 1 for asset in assets),
                 f'{label}: composed scene must include exact candidate GLB')


def check_render_manifest(manifest, evidence, expected, brief, root, validation_profile=LEGACY_PROFILE):
    label = evidence['id']
    obj(manifest, label)
    need(manifest.get('schema_version') == 1 and manifest.get('kind') == 'render_manifest', f'{label}: invalid render manifest')
    need(manifest.get('stage') == 'visual', f'{label}: render manifest must belong to visual stage')
    check_subject(manifest.get('subject'), expected, label)
    manifest_root = (root / evidence['path']).parent
    _, config_raw = checked_file(manifest_root, manifest.get('render_config'), f'{label}.render_config')
    config = obj(json_bytes(config_raw, 'render config'), 'render config')
    for key in ('renderer', 'version', 'color_management', 'lighting', 'camera'):
        need(key in config and bool(config[key]), f'{label}: render config missing {key}')
    planned = {}
    for frame in arr(config.get('frames'), 'render config.frames'):
        obj(frame, 'planned frame')
        fid = identifier(frame.get('id'), 'planned frame.id')
        need(fid not in planned, 'render config: duplicate planned frame id')
        planned[fid] = {key: frame.get(key) for key in ('id', 'view', 'angle_degrees')}
    need(planned, 'render config: planned frame list required')
    frames = arr(manifest.get('frames'), f'{label}.frames')
    canonical = {'front': (0, 0), 'right': (90, 0), 'rear': (180, 0), 'left': (270, 0),
                 'top': (0, 90), 'bottom': (0, -90)}
    seen, views, turntable_angles = set(), set(), set()
    for frame in frames:
        obj(frame, 'frame')
        fid = identifier(frame.get('id'), 'frame.id')
        need(fid not in seen, f'{label}: duplicate frame id {fid}')
        seen.add(fid)
        view = text(frame.get('view'), f'{fid}.view')
        views.add(view)
        angles = arr(frame.get('angle_degrees'), f'{fid}.angle_degrees')
        need(len(angles) == 2 and all(finite_number(a) for a in angles), f'{fid}: finite azimuth/elevation required')
        need(planned.get(fid) == {key: frame.get(key) for key in ('id', 'view', 'angle_degrees')},
             f'{fid}: frame differs from frozen render-config plan')
        if view in canonical:
            azimuth, elevation = canonical[view]
            need(abs((angles[0] - azimuth + 180) % 360 - 180) <= 1e-6 and abs(angles[1] - elevation) <= 1e-6,
                 f'{fid}: canonical {view} camera angle mismatch')
        if view == 'turntable':
            need(-89 <= angles[1] <= 89, f'{fid}: turntable elevation cannot collapse to a pole')
            turntable_angles.add(angles[0] % 360)
        _, raw = checked_file(manifest_root, frame, f'frame {fid}')
        width, height = image_size(raw)
        need(width > 0 and height > 0 and frame.get('width') == width and frame.get('height') == height
             and frame.get('byte_length') == len(raw), f'{fid}: frame dimensions/bytes mismatch')
    problems = []
    if seen != set(planned):
        problems.append(f'{label}: planned render-config frames missing')
    if not set(brief['required_views']) <= views:
        problems.append(f'{label}: required views missing')
    if len(turntable_angles) < brief['turntable_frames']:
        problems.append(f'{label}: insufficient distinct turntable angles')
    if validation_profile == STATIC_PROFILE and (views != STATIC_VIEWS or len(frames) != len(STATIC_VIEWS)):
        problems.append(f'{label}: static-stylized-v1 requires exactly one frame for each fixed view')
    # Full orbit coverage: distinct angles cannot all cluster on a single side.
    angles = sorted(turntable_angles)
    if len(angles) > 1:
        gaps = [b-a for a, b in zip(angles, angles[1:])] + [angles[0]+360-angles[-1]]
        if max(gaps) > 360 / brief['turntable_frames'] * 1.5 + 1e-6:
            problems.append(f'{label}: turntable coverage has an uninspected angular gap')
    return {'frames': seen, 'problems': problems, 'image_sha256': [frame['sha256'] for frame in frames]}


def static_contract(root, contract_path, candidate_path, brief, artifacts):
    """Explicit, hash-bound interpretation of frozen records; never grants approval."""
    need(contract_path is not None, 'static-stylized-v1: --profile-contract required')
    path = Path(contract_path)
    if path.is_absolute():
        need(path.is_relative_to(root), 'profile contract must be inside root')
        path = path.relative_to(root)
    path = relative_file(root, path.as_posix(), 'profile contract')
    raw = path.read_bytes()
    contract = obj(json_bytes(raw, 'profile contract'), 'profile contract')
    need(set(contract) == {'schema_version', 'validation_profile', 'rule_version', 'candidate',
                           'publication_authority', 'publication_policy', 'rationale'},
         'profile contract: exact versioned fields required')
    need(type(contract['schema_version']) is int and contract['schema_version'] == 1 and contract['validation_profile'] == STATIC_PROFILE
         and contract['rule_version'] == PROFILE_RULE_VERSION, 'profile contract: unknown profile/rule version')
    need(contract['publication_authority'] == 'separate', 'profile contract: publication authority must remain separate')
    text(contract['rationale'], 'profile contract.rationale')
    frozen_path, frozen_bytes = checked_file(root, contract['candidate'], 'profile contract.candidate')
    need(frozen_path == candidate_path and frozen_bytes == candidate_path.read_bytes(),
         'profile contract: different candidate')
    _, policy_raw = checked_file(root, contract['publication_policy'], 'profile contract.publication_policy')
    policy = obj(json_bytes(policy_raw, 'publication policy'), 'publication policy')
    need(type(policy.get('schema_version')) is int and policy.get('schema_version') == 1 and policy.get('scope') == 's010s/lowpoly-vault'
         and policy.get('authority') == 'owner_authorized_qa_passed_batch_release'
         and policy.get('candidate_gate_grants_publication') is False, 'profile contract: invalid separate publication policy')
    text(policy.get('authorization_source'), 'publication policy.authorization_source')
    brief = obj(brief, 'brief')
    need(brief.get('profile') == 'production', 'static-stylized-v1: production obligations required')
    effective = copy.deepcopy(brief)
    # Keep original bytes/subject hashes. A contract names the source record and the
    # separate policy instead of interpreting free-text authority as permission.
    effective['publication_authority'] = 'separate'
    if 'required_deliverables' not in effective:
        effective['required_deliverables'] = [{'role': role, **artifacts[role]}
                                              for role in ('source', 'generator', 'config') if role in artifacts]
    return effective, {'path': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(raw).hexdigest()}


def validate_candidate(candidate, root=None, previous=None, validation_profile=LEGACY_PROFILE, profile_contract=None):
    """Return JSON-safe diagnostics. Never modify files or grant publication authority."""
    root = Path(root or Path(__file__).resolve().parents[1]).resolve()
    result = {'valid': False, 'approved_for_brief': False, 'errors': [], 'approval_blockers': [],
              'required_stages': [], 'measurements': {}, 'limitations': LIMITATIONS,
              'validation_profile': validation_profile, 'rule_version': PROFILE_RULE_VERSION,
              'profile_contract_status': 'not_checked'}
    try:
        need(validation_profile in (LEGACY_PROFILE, STATIC_PROFILE), 'Unknown validation profile')
        need(validation_profile == STATIC_PROFILE or profile_contract is None, 'Legacy profile cannot use a profile contract')
        path = Path(candidate)
        if path.is_absolute():
            need(path.is_relative_to(root), 'candidate record must be inside root')
            path = relative_file(root, path.relative_to(root).as_posix(), 'candidate')
        else:
            path = relative_file(root, str(path), 'candidate')
        record = obj(json_bytes(path.read_bytes(), 'candidate'), 'candidate')
        need(record.get('schema_version') == 1, 'candidate: unsupported schema_version')
        identifier(record.get('asset_id'), 'asset_id')
        identifier(record.get('revision'), 'revision')
        identity(record.get('maker'), 'maker')
        artifacts = obj(record.get('artifacts'), 'artifacts')
        for key in ('glb', 'brief', 'references'):
            need(key in artifacts, f'artifacts: {key} required')
        files = {key: checked_file(root, item, f'artifacts.{key}') for key, item in artifacts.items()}
        expected = {'revision': record['revision'], **{f'{key}_sha256': artifacts[key]['sha256'] for key in ('glb', 'brief', 'references')}}
        result['asset_id'], result['revision'], result['subject'] = record['asset_id'], record['revision'], expected
        result['artifact_sha256'] = {key: item['sha256'] for key, item in artifacts.items()}
        result['approved_visual_image_sha256'] = []
        brief = json_bytes(files['brief'][1], 'brief')
        if validation_profile == STATIC_PROFILE:
            brief, result['profile_contract'] = static_contract(root, profile_contract, path, brief, artifacts)
        references = obj(json_bytes(files['references'][1], 'references'), 'references')
        need(references.get('schema_version') == 1, 'references: unsupported schema_version')
        sources = set()
        for source in arr(references.get('sources'), 'references.sources'):
            obj(source, 'source')
            sid = identifier(source.get('id'), 'source.id')
            need(sid not in sources, f'duplicate reference source: {sid}')
            sources.add(sid)
            for key in ('title', 'url'):
                text(source.get(key), f'{sid}.{key}')
            consulted = validation_profile == STATIC_PROFILE and source.get('use') in ('consulted-only', CONSULTED_USE)
            if consulted:
                need(references.get('no_incorporated_third_party_assets') is True,
                     f'{sid}: consulted-only requires explicit no-incorporated-assets declaration')
                text(source.get('rights_note'), f'{sid}.rights_note')
                need(source.get('incorporated', False) is False, f'{sid}: consulted-only source cannot be incorporated')
                need(not any(obj(obj(t, 'texture').get('provenance'), 'texture.provenance').get('source_id') == sid for t in arr(record.get('textures'), 'textures')),
                     f'{sid}: consulted-only source cannot supply an incorporated texture')
            else:
                text(source.get('license'), f'{sid}.license')
            if source.get('local') is not None:
                checked_file(root, source['local'], f'reference {sid}')
        required, definitions = check_brief(brief, record, sources, validation_profile)
        result['required_stages'] = sorted(required)
        result['profile'] = brief['profile']
        result['profile_contract_status'] = 'pass'  # Compatibility only, not candidate validity or approval.
        deliverables = arr(brief.get('required_deliverables', []), 'brief.required_deliverables')
        roles = set()
        for deliverable in deliverables:
            obj(deliverable, 'required deliverable')
            role = identifier(deliverable.get('role'), 'deliverable.role')
            need(role not in roles, 'duplicate required deliverable role')
            roles.add(role)
            need(artifacts.get(role) == {key: deliverable.get(key) for key in ('path', 'sha256')},
                 f'deliverable {role}: exact frozen artifact path/hash required')
        if brief['profile'] == 'production':
            need({'source', 'generator', 'config'} <= roles,
                 'production: frozen source/generator/config required_deliverables missing')
        # The validator audits the static baseline itself so a fabricated numeric budget report cannot pass.
        doc, binary, raw = read_glb(files['glb'][0])
        audit = audit_glb(files['glb'][0], max_triangles=brief['geometry_policy']['max_triangles'],
                          max_materials=brief['geometry_policy']['max_materials'],
                          max_primitives=brief['geometry_policy']['max_primitives'])
        measured = {'triangles': audit.get('scene_triangles'), 'materials': audit.get('materials'),
                    'primitives': audit.get('scene_primitives_estimated_base_draw_calls'), 'glb_bytes': len(raw),
                    'texture_count': len(doc.get('images', [])), 'texture_max_dimension': 0, 'texture_bytes': 0,
                    'decoded_texture_bytes_estimate': 0, 'semantic_sha256': audit.get('semantic_sha256')}
        textures = arr(record.get('textures'), 'textures')
        need(len(textures) == measured['texture_count'], 'textures: provenance entry required for every embedded GLB image')
        indexes = set()
        for texture in textures:
            obj(texture, 'texture')
            index = integer(texture.get('image_index'), 'texture.image_index')
            need(index < len(textures) and index not in indexes, 'texture: duplicate or invalid image_index')
            indexes.add(index)
            _, image = checked_file(root, texture, f'texture {index}')
            width, height = image_size(image)
            need(width > 0 and height > 0, 'texture: nonzero dimensions required')
            need(texture.get('width') == width and texture.get('height') == height and texture.get('byte_length') == len(image),
                 'texture: recorded dimensions/bytes differ from actual image')
            source = obj(texture.get('provenance'), 'texture.provenance')
            need(source.get('source_id') in sources, 'texture: provenance source must exist in reference ledger')
            for key in ('creator', 'license', 'usage'):
                text(source.get(key), f'texture.provenance.{key}')
            exported = doc['images'][index]
            need('uri' not in exported and 'bufferView' in exported, 'texture: standalone embedded image required')
            view = doc['bufferViews'][exported['bufferView']]
            start, size = view.get('byteOffset', 0), view['byteLength']
            need(view.get('buffer', 0) == 0 and start >= 0 and size > 0 and start+size <= len(binary), 'texture: invalid embedded range')
            need(binary[start:start+size] == image, 'texture: provenance bytes differ from actual embedded GLB image')
            measured['texture_max_dimension'] = max(measured['texture_max_dimension'], width, height)
            measured['texture_bytes'] += len(image)
            mip_width, mip_height = width, height
            while True:
                measured['decoded_texture_bytes_estimate'] += mip_width * mip_height * 4
                if mip_width == mip_height == 1:
                    break
                mip_width, mip_height = max(1, mip_width // 2), max(1, mip_height // 2)
        result['measurements'] = measured
        result['decoded_memory_assumptions'] = 'RGBA8 per embedded image with full mip chain; estimate excludes GPU duplication, driver overhead and device compression.'
        blockers = result['approval_blockers']
        blockers.extend(f'GLB audit: {error}' for error in audit['errors'])
        for mapping, policy in ((GEOMETRY, 'geometry_policy'), (TEXTURE, 'texture_policy')):
            for key, limit in mapping.items():
                if measured.get(key) is None or measured[key] > brief[policy][limit]:
                    blockers.append(f'{key}: exceeds or cannot establish frozen {limit}={brief[policy][limit]}')
        if ('max_decoded_bytes' in brief['texture_policy'] and
                measured['decoded_texture_bytes_estimate'] > brief['texture_policy']['max_decoded_bytes']):
            blockers.append('decoded texture estimate exceeds frozen max_decoded_bytes')
        # Reports and previews are immutable by checksum and must bind internally to the exact subject.
        evidence_by_id, report_by_id, render_frames = {}, {}, {}
        for evidence in arr(record.get('evidence'), 'evidence'):
            obj(evidence, 'evidence item')
            eid = identifier(evidence.get('id'), 'evidence.id')
            need(eid not in evidence_by_id, f'duplicate evidence: {eid}')
            stage = evidence.get('stage')
            need(stage in STAGES, f'{eid}: unknown evidence stage')
            allowed = ('rendered_image', REPORT_KIND[stage]) + (('render_manifest',) if stage == 'visual' else ())
            need(evidence.get('kind') in allowed, f'{eid}: evidence kind cannot establish {stage}')
            check_subject(evidence.get('subject'), expected, eid)
            _, data = checked_file(root, evidence, eid)
            if evidence['kind'] == 'rendered_image':
                width, height = image_size(data)
                need(width > 0 and height > 0, f'{eid}: image has no pixels')
            elif evidence['kind'] == 'render_manifest':
                render_frames[eid] = check_render_manifest(json_bytes(data, eid), evidence, expected, brief, root, validation_profile)
            else:
                report_by_id[eid] = json_bytes(data, eid)
            evidence_by_id[eid] = evidence
        for eid, report in report_by_id.items():
            evidence = evidence_by_id[eid]
            check_report(report, evidence, expected, evidence['stage'], measured, evidence_by_id, root, artifacts, brief['profile'], audit)
        stages = obj(record.get('stages'), 'stages')
        need(set(stages) == set(STAGES), 'stages: all seven distinct stage records required (unknown is honest)')
        for stage, entry in stages.items():
            obj(entry, stage)
            status = entry.get('status')
            need(status in STATUSES, f'{stage}: invalid status {status!r}')
            text(entry.get('note'), f'{stage}.note')
            eids = unique(entry.get('evidence'), f'{stage}.evidence')
            inspected = unique(entry.get('inspected_references'), f'{stage}.inspected_references')
            need(set(inspected) <= sources, f'{stage}: unknown inspected reference')
            for eid in eids:
                need(eid in evidence_by_id and evidence_by_id[eid]['stage'] == stage,
                     f'{stage}: missing or unrelated evidence {eid}')
            if status == 'pass':
                identity(entry.get('reviewer'), f'{stage}.reviewer', record['maker'] if stage in INDEPENDENT else None)
                timestamp(entry.get('reviewed_at'), f'{stage}.reviewed_at')
                check_subject(entry.get('subject'), expected, stage)
                need(eids, f'{stage}: zero-evidence passing forbidden')
                need(any(eid in report_by_id and report_by_id[eid]['status'] == 'pass' for eid in eids),
                     f'{stage}: passing structured {REPORT_KIND[stage]} required')
                need(all(report_by_id[eid]['status'] == 'pass' for eid in eids if eid in report_by_id),
                     f'{stage}: passing stage cites nonpassing report')
                reviewed = sorted([{'id': eid, 'sha256': evidence_by_id[eid]['sha256']}
                                   for eid in eids if eid not in report_by_id], key=lambda item: item['id'])
                for eid in eids:
                    if eid in report_by_id:
                        bindings = arr(report_by_id[eid].get('reviewed_evidence'), f'{eid}.reviewed_evidence')
                        need(all(isinstance(binding, dict) and set(binding) == {'id', 'sha256'}
                                 and isinstance(binding['id'], str) for binding in bindings),
                             f'{eid}: reviewed_evidence needs exact id/sha256 pairs')
                        need(sorted(bindings, key=lambda item: item['id']) == reviewed,
                             f'{eid}: stale reviewed evidence; report does not bind current evidence digests')
                if stage in ('visual', 'factual'):
                    need(inspected, f'{stage}: actual inspected reference IDs must be recorded')
                if stage == 'visual':
                    manifests = [eid for eid in eids if eid in render_frames]
                    need(manifests, 'visual: hash-bound complete render_manifest required')
                    inspected_frames = unique(entry.get('inspected_frames'), 'visual.inspected_frames')
                    for eid in manifests:
                        need(not render_frames[eid]['problems'], '; '.join(render_frames[eid]['problems']))
                    expected_frames = set().union(*(render_frames[eid]['frames'] for eid in manifests))
                    need(set(inspected_frames) == expected_frames, 'visual: all planned frames must be explicitly inspected')
                    result['approved_visual_image_sha256'] = sorted(set(
                        [evidence_by_id[eid]['sha256'] for eid in eids if evidence_by_id[eid]['kind'] == 'rendered_image']
                        + [sha for eid in manifests for sha in render_frames[eid]['image_sha256']]))
                if stage == 'technical':
                    need(not audit['errors'], 'technical: passing stage conflicts with GLB audit errors')
            elif status == 'not_applicable':
                need(stage not in required, f'{stage}: mandatory stage cannot be waived as not_applicable')
            if stage in required and status != 'pass':
                blockers.append(f'{stage}: {status}')
            outcomes = {}
            for criterion in arr(entry.get('criteria'), f'{stage}.criteria'):
                obj(criterion, 'criterion outcome')
                cid = criterion.get('id')
                need(cid in definitions and definitions[cid]['stage'] == stage and cid not in outcomes,
                     f'{stage}: unknown, wrong-stage or duplicate criterion {cid}')
                need(criterion.get('status') in STATUSES, f'{cid}: invalid criterion status')
                text(criterion.get('note'), f'{cid}.note')
                ceids = unique(criterion.get('evidence'), f'{cid}.evidence')
                need(set(ceids) <= set(eids), f'{cid}: criterion evidence must be in its stage')
                definition = definitions[cid]
                if criterion['status'] == 'pass':
                    need(ceids, f'{cid}: zero-evidence passing forbidden')
                    need(set(definition.get('required_sources', [])) <= set(inspected),
                         f'{cid}: required reference sources not inspected')
                if criterion['status'] == 'not_applicable':
                    need(not definition['critical'] and definition.get('allow_not_applicable') is True,
                         f'{cid}: criterion cannot be waived')
                if criterion['status'] not in ('pass', 'not_applicable'):
                    if stage in required or definition['critical']:
                        blockers.append(f'{cid}: {criterion["status"]}')
                    need(status != 'pass', f'{stage}: passing stage has unresolved criterion {cid}')
                outcomes[cid] = criterion
            need(set(outcomes) == {cid for cid, definition in definitions.items() if definition['stage'] == stage},
                 f'{stage}: missing explicit criterion outcomes')
        for blocker in arr(record.get('blockers'), 'blockers'):
            obj(blocker, 'blocker')
            identifier(blocker.get('id'), 'blocker.id')
            text(blocker.get('description'), 'blocker.description')
            need(blocker.get('status') in ('open', 'resolved'), 'blocker: status must be open or resolved')
            if blocker['status'] == 'open':
                blockers.append(f'open blocker: {blocker["id"]}')
            else:
                text(blocker.get('resolution'), 'blocker.resolution')
        approval = obj(record.get('approval'), 'approval')
        need(approval.get('status') in ('pending', 'rejected', 'approved_for_brief'), 'approval: invalid status')
        result['approval_status'] = approval['status']
        if previous:
            previous_path = Path(previous)
            if not previous_path.is_absolute():
                previous_path = root / previous_path
            old = obj(json_bytes(previous_path.read_bytes(), 'previous'), 'previous')
            need(old.get('asset_id') == record['asset_id'], 'previous: different asset')
            if old.get('revision') == record['revision']:
                need(old.get('artifacts') == artifacts and old.get('textures') == textures,
                     'immutable revision changed artifacts/textures; create a new revision')
        if record.get('supersedes') is not None:
            supersedes = obj(record['supersedes'], 'supersedes')
            _, prior_raw = checked_file(root, supersedes, 'supersedes')
            prior = obj(json_bytes(prior_raw, 'supersedes'), 'supersedes record')
            need(prior.get('asset_id') == record['asset_id'] and prior.get('revision') != record['revision'],
                 'supersedes: same asset and a different immutable revision required')
            need(prior.get('revision') == supersedes.get('revision'), 'supersedes: prior revision mismatch')
        if approval['status'] == 'approved_for_brief':
            if validation_profile == STATIC_PROFILE:
                need(approval.get('validation_profile') == STATIC_PROFILE and approval.get('rule_version') == PROFILE_RULE_VERSION,
                     'approval: exact static validation profile/rule version required')
            identity(approval.get('reviewer'), 'approval.reviewer', record['maker'])
            timestamp(approval.get('reviewed_at'), 'approval.reviewed_at')
            check_subject(approval.get('subject'), expected, 'approval')
            text(approval.get('note'), 'approval.note')
            need(not blockers, 'approval: claimed approved with unresolved obligations: ' + '; '.join(blockers))
            need(approval.get('review_snapshot_sha256') == approval_snapshot_sha256(record),
                 'approval: stale review snapshot; evidence or stage decisions changed after approval')
            result['approved_for_brief'] = True
        else:
            blockers.append(f'approval: {approval["status"]}')
        result['valid'] = True
    except (Invalid, OSError, ValueError, TypeError, KeyError, IndexError, struct.error, OverflowError) as exc:
        result['errors'].append(str(exc))
    if validation_profile == STATIC_PROFILE:
        # Separate diagnostics are deliberately not rewritten to fit the new profile.
        result['legacy_result'] = validate_candidate(candidate, root, previous)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', help='candidate record path; relative paths are resolved under --root')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--profile', choices=(LEGACY_PROFILE, STATIC_PROFILE), default=LEGACY_PROFILE)
    parser.add_argument('--profile-contract', help='frozen candidate/policy sidecar required by static-stylized-v1')
    parser.add_argument('--previous', help='previous record snapshot; enforce immutable inputs within the same revision')
    parser.add_argument('--require-approved', action='store_true', help='fail unless independent evidence establishes approved_for_brief')
    parser.add_argument('--json', action='store_true', help='emit machine-readable diagnostics')
    args = parser.parse_args()
    result = validate_candidate(args.candidate, args.root, args.previous, args.profile, args.profile_contract)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    else:
        state = 'approved for frozen brief; publication separate' if result['approved_for_brief'] else 'pending/not approved'
        print(f'Candidate {"valid" if result["valid"] else "INVALID"}: {state}')
        for error in result['errors']:
            print(f'ERROR: {error}')
        for blocker in result['approval_blockers']:
            print(f'BLOCKER: {blocker}')
        print(LIMITATIONS)
    return 0 if result['valid'] and (not args.require_approved or result['approved_for_brief']) else 1


if __name__ == '__main__':
    sys.exit(main())
