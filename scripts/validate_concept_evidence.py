#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Leon Made This / s010s
"""Check a concept-to-GLB study bundle without approving or publishing an asset.

Reuses the candidate gate's safe paths, exact hashes and render-manifest checks.
Recorded timestamps/provenance are attestations, not independent proof of history.
"""
import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

from qa_glb import audit_glb, read_glb
from validate_candidate import (Invalid, arr, checked_file, check_render_manifest,
                                finite_number, identifier, image_size, integer,
                                json_bytes, need, obj, relative_file, text, timestamp, unique)

STAGES = ('imagegen', 'interpretation', 'modeling_export', 'proof_rendering',
          'visual_review', 'target_browser')
LIMITATIONS = ('Evidence integrity only: no visual, factual, browser/GPU, rebuild, '
               'candidate approval or publication decision. ImageGen provenance '
               'and timestamps remain auditable attestations; inspect source records and pixels.')


def read_json(raw, label):
    return obj(json_bytes(raw, label), label)


def validate(record_path, root):
    root = Path(root).resolve()
    result = {'valid': False, 'evidence_complete': False, 'errors': [], 'blockers': [],
              'advisories': [], 'measurements': {}, 'publication_authority': 'separate',
              'runtime_qa': 'not_checked_by_this_tool', 'limitations': LIMITATIONS}
    try:
        path = Path(record_path)
        if path.is_absolute():
            need(path.is_relative_to(root), 'record must be inside --root')
            path = path.relative_to(root)
        path = relative_file(root, path.as_posix(), 'record')
        record = read_json(path.read_bytes(), 'record')
        need(record.get('schema_version') == 1 and record.get('kind') == 'concept_evidence',
             'Expected concept_evidence schema_version 1')
        need(record.get('scope') == 'provisional-study', 'This helper is for provisional studies only')
        asset_id = identifier(record.get('asset_id'), 'asset_id')
        revision = identifier(record.get('revision'), 'revision')
        labels = obj(record.get('labels'), 'labels')
        text(labels.get('en'), 'labels.en')
        if 'zh-CN' in labels:
            text(labels['zh-CN'], 'labels.zh-CN')
        artifacts = obj(record.get('artifacts'), 'artifacts')
        for role in ('glb', 'source', 'generator', 'config', 'brief', 'references'):
            need(role in artifacts, f'artifacts.{role} required')
        files = {role: checked_file(root, entry, f'artifacts.{role}')
                 for role, entry in artifacts.items()}
        need(files['source'][0].suffix == '.blend', 'Editable source must be a .blend file')
        subject = {'revision': revision, **{role + '_sha256': artifacts[role]['sha256']
                                          for role in ('glb', 'brief', 'references')}}
        result.update(asset_id=asset_id, revision=revision, subject=subject)
        concept = obj(record.get('concept'), 'concept')
        need(concept.get('provider') == 'ImageGen', 'Record the actual ImageGen concept source')
        checked_file(root, concept.get('prompt'), 'concept.prompt')
        if concept.get('generation_record') is None:
            result['blockers'].append('ImageGen invocation/result record is unavailable; do not fabricate a historical receipt')
        else:
            checked_file(root, concept['generation_record'], 'concept.generation_record')
        images = arr(concept.get('images'), 'concept.images')
        need(images, 'At least one original concept image is required')
        concept_ids = set()
        concept_hashes = set()
        for image in images:
            obj(image, 'concept image')
            cid = identifier(image.get('id'), 'concept image.id')
            need(cid not in concept_ids, 'Duplicate concept image id')
            concept_ids.add(cid)
            text(image.get('view'), f'{cid}.view')
            _, raw = checked_file(root, image, f'concept image {cid}')
            width, height = image_size(raw)
            need(width > 0 and height > 0, 'Concept image dimensions must be positive')
            concept_hashes.add(image['sha256'])
        text(concept.get('cross_view_consistency_note'), 'concept.cross_view_consistency_note')
        text(concept.get('hidden_surface_decisions'), 'concept.hidden_surface_decisions')
        times = obj(record.get('chronology'), 'chronology')
        ordered = []
        for key in ('concept_generated_at', 'concept_inspected_at', 'modeling_started_at'):
            value = times.get(key)
            if value is None:
                result['blockers'].append(f'{key}: unknown; do not reconstruct times from file mtimes')
            else:
                timestamp(value, key)
                ordered.append((key, datetime.fromisoformat(value.replace('Z', '+00:00'))))
        for (first, a), (second, b) in zip(ordered, ordered[1:]):
            need(a <= b, f'Chronology contradiction: {first} must precede {second}')
        if len(ordered) == 3:
            need(ordered[0][1] < ordered[2][1], 'Concept generation must precede model construction')
        timings = arr(record.get('stage_timings'), 'stage_timings')
        seen = set()
        for stage in timings:
            obj(stage, 'stage timing')
            name = stage.get('stage')
            need(name in STAGES and name not in seen, 'Unknown or duplicate timing stage')
            seen.add(name)
            status = stage.get('status')
            need(status in ('measured', 'unrecorded', 'not_run'), 'Timing status is not an acceptance verdict')
            text(stage.get('note'), f'{name}.note')
            if status == 'measured':
                need(finite_number(stage.get('wall_seconds')) and stage['wall_seconds'] >= 0,
                     f'{name}: nonnegative measured wall_seconds required')
                checked_file(root, stage.get('measurement_record'), f'{name}.measurement_record')
            else:
                need(stage.get('wall_seconds') is None and stage.get('measurement_record') is None,
                     f'{name}: unmeasured time must remain null')
        need(seen == set(STAGES), 'Record all six timing stages, including unrun target browser')
        coverage = obj(record.get('coverage'), 'coverage')
        views = unique(coverage.get('required_views'), 'coverage.required_views')
        need('hero' in views and len(views) >= 2, 'Hero and alternate-angle proof are required')
        integer(coverage.get('turntable_frames'), 'coverage.turntable_frames')
        inspected = unique(record.get('inspected_frames'), 'inspected_frames')
        if record.get('review_note') is None:
            result['blockers'].append('Visual review note is unavailable')
        else:
            checked_file(root, record['review_note'], 'review_note')
        thumb = record.get('thumbnail')
        if thumb is None:
            result['blockers'].append('An exported-GLB thumbnail is unavailable')
        else:
            obj(thumb, 'thumbnail')
            _, thumbnail_raw = checked_file(root, thumb, 'thumbnail')
            image_size(thumbnail_raw)
            need(thumb['sha256'] not in concept_hashes, 'Concept art cannot substitute for a thumbnail')
        descriptor = record.get('render_manifest')
        if descriptor is None:
            result['blockers'].append('Hash-bound render manifest is unavailable; image/source and inspection coverage cannot be verified')
        else:
            obj(descriptor, 'render_manifest')
            _, raw = checked_file(root, descriptor, 'render_manifest')
            manifest = read_json(raw, 'render_manifest')
            orbit_count = sum(isinstance(frame, dict) and frame.get('view') == 'turntable'
                              for frame in arr(manifest.get('frames'), 'render_manifest.frames'))
            need(coverage['turntable_frames'] > 0 or orbit_count == 0,
                 'Orbit frames require a positive frozen turntable count')
            check = check_render_manifest(manifest, {**descriptor, 'id': 'concept-proof'},
                                          subject, coverage, root)
            result['blockers'].extend(check['problems'])
            need(manifest.get('source_glb_sha256') == artifacts['glb']['sha256'],
                 'Render manifest must identify the exact exported GLB')
            need(manifest.get('source_unchanged') is True, 'Render producer did not attest unchanged source')
            frames = manifest['frames']
            need(len({tuple(frame['angle_degrees']) for frame in frames}) >= 2,
                 'Alternate proof must use a distinct camera angle')
            need(not concept_hashes.intersection(check['image_sha256']),
                 'Concept art cannot substitute for an exported-GLB render')
            if thumb is not None:
                selected = [frame for frame in frames if frame['id'] == thumb.get('source_frame_id')]
                need(len(selected) == 1 and selected[0]['sha256'] == thumb['sha256'],
                     'Thumbnail must be an exact proof frame; rerender desired size or keep a derivation record outside this helper')
            need(set(inspected) <= check['frames'], 'Inspected frames include an unknown frame')
            if set(inspected) != check['frames']:
                result['blockers'].append('Not all proof frames have a recorded visual inspection')
        # Use existing static audit, with no universal triangle/material caps.
        audit = audit_glb(files['glb'][0], max_triangles=sys.maxsize,
                          max_materials=sys.maxsize, max_primitives=sys.maxsize)
        result['blockers'].extend('Static GLB: ' + value for value in audit['errors'])
        result['advisories'].extend('Static GLB: ' + value for value in audit['warnings'])
        if not audit['errors']:
            doc, _, _ = read_glb(files['glb'][0])
            result['measurements'] = {'glb_bytes': audit['bytes'],
                'triangles': audit['scene_triangles'], 'materials': audit['materials'],
                'primitives': audit['scene_primitives_estimated_base_draw_calls'],
                'images': len(doc.get('images', [])), 'textures': len(doc.get('textures', [])),
                'bounds_gltf_y_up_m': audit['bounds_m']}
        khronos = obj(record.get('khronos'), 'khronos')
        need(khronos.get('glb_sha256') == artifacts['glb']['sha256'], 'Khronos binding is stale')
        _, raw = checked_file(root, khronos.get('report'), 'khronos.report')
        report = read_json(raw, 'Khronos report')
        text(report.get('validatorVersion'), 'Khronos validatorVersion')
        issues = obj(report.get('issues'), 'Khronos issues')
        for key in ('numErrors', 'numWarnings'):
            integer(issues.get(key), 'Khronos ' + key)
        messages = arr(issues.get('messages'), 'Khronos messages')
        need(issues.get('truncated') is False, 'Truncated Khronos report is insufficient')
        need(all(isinstance(item, dict) for item in messages), 'Invalid Khronos message')
        need(sum(item.get('severity') == 0 for item in messages) == issues['numErrors']
             and sum(item.get('severity') == 1 for item in messages) == issues['numWarnings'],
             'Khronos issue counts do not match messages')
        result['khronos_report'] = {'validator_version': report['validatorVersion'],
                                    'errors': issues['numErrors'], 'warnings': issues['numWarnings']}
        if issues['numErrors']:
            result['blockers'].append('Khronos validator reported errors')
        reviews = arr(khronos.get('warning_review'), 'khronos.warning_review')
        warnings = [item for item in messages if item.get('severity') == 1]
        need(len(reviews) == len(warnings), 'Every Khronos warning needs a review')
        for review, warning in zip(reviews, warnings):
            obj(review, 'warning review')
            need(review.get('warning') == warning, 'Warning review must bind the exact warning')
            text(review.get('rationale'), 'warning rationale')
        target = obj(record.get('budget'), 'budget')
        integer(target.get('target_glb_bytes'), 'budget.target_glb_bytes', minimum=1)
        text(target.get('rationale'), 'budget.rationale')
        need(target.get('enforcement') == 'advisory', 'This pilot target is advisory, not a global cap')
        if result['measurements'].get('glb_bytes', 0) > target['target_glb_bytes']:
            result['advisories'].append('GLB exceeds this study size target; review shape and deployment tradeoffs')
        result['valid'] = True
        result['evidence_complete'] = not result['blockers']
    except (Invalid, OSError, ValueError, TypeError, KeyError, IndexError, OverflowError) as exc:
        result['errors'].append(str(exc))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', help='Concept evidence JSON; paths resolve under --root')
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--require-complete', action='store_true', help='Require complete study evidence, never approval')
    args = parser.parse_args()
    result = validate(args.record, args.root)
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0 if result['valid'] and (not args.require_complete or result['evidence_complete']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
