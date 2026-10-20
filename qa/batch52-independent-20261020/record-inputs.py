#!/usr/bin/env python3
"""Verify and record the immutable batch-52 subject, concept, and proof inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
QA = Path(__file__).resolve().parent
CANDIDATE_COMMIT = '352d81995b33fc1e7a95980184ab6641dd5738a5'
HANDOFF = 'production/continuous-small-life-round18-20261020/work/batch-52/HANDOFF.json'
HANDOFF_SHA256 = '74a8cd809f19c7150ba2faea2a22b1aa51882b2f9b2eac97688e5b190586e568'
EXPECTED = {
    'aturia': 'r002',
    'phoenicopsis': 'r001',
    'cave-popcorn': 'r003',
    'curvolithus-trilobed-trail': 'r001',
}
CONCEPT_RECORDS = {
    'aturia': 'assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002/concept-evidence.json',
    'phoenicopsis': 'assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/concept-evidence.json',
    'cave-popcorn': 'assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/concept-evidence.json',
    'curvolithus-trilobed-trail': 'production/continuous-small-life-round18-20261020/work/batch-52/curvolithus-trilobed-trail/concept-evidence.json',
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def content_at_commit(path):
    return git('show', f'{CANDIDATE_COMMIT}:{path}')

def resolve_sidecar_path(path, sidecar_path):
    # Sidecars use either repository-root references or paths local to the sidecar.
    if path.startswith(('assets/', 'production/')):
        return path
    return (Path(sidecar_path).parent / path).as_posix()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    git('cat-file', '-e', f'{CANDIDATE_COMMIT}^{{commit}}')
    handoff_bytes = content_at_commit(HANDOFF)
    if sha(handoff_bytes) != HANDOFF_SHA256:
        raise SystemExit('Fixed commit handoff SHA256 differs from the dispatch pin')
    if sha((ROOT / HANDOFF).read_bytes()) != HANDOFF_SHA256:
        raise SystemExit('Working-tree handoff SHA256 differs from the dispatch pin')
    handoff = json.loads(handoff_bytes)
    scope_path = 'production/continuous-small-life-round18-20261020/batch-52-QA-SCOPE.json'
    scope = json.loads(content_at_commit(scope_path))
    items = {item['asset_id']: item for item in handoff['items']}
    if set(items) != set(EXPECTED):
        raise SystemExit('Handoff asset set differs from the four pinned dispatch subjects')
    assets = []
    for asset_id, revision in EXPECTED.items():
        item = items[asset_id]
        if item['revision'] != revision:
            raise SystemExit(f'{asset_id}: handoff revision differs')
        bindings = []
        for role, descriptor in item['artifact_bindings'].items():
            path, expected_hash = descriptor['path'], descriptor['sha256']
            commit_raw = content_at_commit(path)
            working_raw = (ROOT / path).read_bytes()
            if sha(commit_raw) != expected_hash or sha(working_raw) != expected_hash:
                raise SystemExit(f'{asset_id}.{role}: binding differs at fixed commit or working tree')
            bindings.append({'role': role, 'path': path, 'sha256': expected_hash,
                             'bytes': len(commit_raw), 'fixed_commit_verified': True,
                             'working_tree_verified': True})
        manifest_binding = item['render_manifest']
        manifest_raw = content_at_commit(manifest_binding['path'])
        if sha(manifest_raw) != manifest_binding['sha256']:
            raise SystemExit(f'{asset_id}: render manifest hash mismatch')
        manifest = json.loads(manifest_raw)
        glb_hash = item['artifact_bindings']['glb']['sha256']
        if manifest.get('source_glb_sha256') != glb_hash:
            raise SystemExit(f'{asset_id}: render manifest does not bind the pinned GLB')
        frame_records = []
        manifest_dir = str(Path(manifest_binding['path']).parent)
        for frame in manifest['frames']:
            frame_path = f'{manifest_dir}/{frame["path"]}'
            frame_raw = content_at_commit(frame_path)
            if sha(frame_raw) != frame['sha256'] or len(frame_raw) != frame['byte_length']:
                raise SystemExit(f'{asset_id}.{frame["id"]}: rendered proof frame changed')
            frame_records.append({'id': frame['id'], 'view': frame['view'], 'path': frame_path,
                                  'sha256': frame['sha256'], 'bytes': len(frame_raw),
                                  'width': frame['width'], 'height': frame['height']})
        concept_path = CONCEPT_RECORDS[asset_id]
        concept_raw = content_at_commit(concept_path)
        concept = json.loads(concept_raw)
        concept_evidence_inputs = []
        for field in ('prompt', 'generation_record'):
            entry = concept.get('concept', {}).get(field)
            if entry is None:
                continue
            resolved = resolve_sidecar_path(entry['path'], concept_path)
            raw = content_at_commit(resolved)
            if sha(raw) != entry['sha256']:
                raise SystemExit(f'{asset_id}: concept {field} hash mismatch')
            concept_evidence_inputs.append({'role': field, 'path': resolved,
                                            'sha256': entry['sha256'], 'bytes': len(raw)})
        images = []
        for image in concept['concept']['images']:
            image_path = resolve_sidecar_path(image['path'], concept_path)
            image_raw = content_at_commit(image_path)
            if sha(image_raw) != image['sha256']:
                raise SystemExit(f'{asset_id}: concept image hash mismatch')
            images.append({'id': image['id'], 'path': image_path,
                           'sha256': image['sha256'], 'bytes': len(image_raw),
                           'view': image['view']})
        assets.append({
            'asset_id': asset_id, 'revision': revision,
            'candidate': item['candidate'],
            'glb': item['artifact_bindings']['glb'],
            'source': item['artifact_bindings']['source'],
            'brief': item['artifact_bindings']['brief'],
            'references': item['artifact_bindings']['references'],
            'artifact_bindings': bindings,
            'concept_record': {'path': concept_path, 'sha256': sha(concept_raw),
                               'imagegen_generation_time': concept.get('chronology', {}).get('concept_generated_at'),
                               'evidence_complete': False, 'inputs': concept_evidence_inputs,
                               'images': images},
            'render_manifest': {'path': manifest_binding['path'],
                                'sha256': manifest_binding['sha256'],
                                'source_glb_sha256': glb_hash,
                                'frame_count': len(frame_records), 'frames': frame_records},
        })
    record = {
        'schema_version': 1,
        'kind': 'independent_batch52_frozen_input_record',
        'candidate_commit': CANDIDATE_COMMIT,
        'candidate_commit_exists': True,
        'batch_qa_scope': {'path': scope_path, 'expected_source_commit': scope.get('expected_source_commit'),
                           'expected_glb_sha256_by_asset': scope.get('expected_glb_sha256_by_asset'),
                           'ready_for_qa': scope.get('ready_for_qa'),
                           'resolution': 'Dispatch parent supplied the exact commit; this independent record binds it and the exact four handoff GLB hashes.'},
        'handoff': {'path': HANDOFF, 'sha256': HANDOFF_SHA256,
                    'bytes': len(handoff_bytes), 'fixed_commit_verified': True,
                    'working_tree_verified': True},
        'assets': assets,
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise SystemExit(f'Refusing to overwrite immutable evidence: {output}')
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'status': 'pass', 'output': str(output.relative_to(ROOT)),
                      'asset_count': len(assets),
                      'proof_views': sum(len(item['render_manifest']['frames']) for item in assets)}))

if __name__ == '__main__':
    main()
