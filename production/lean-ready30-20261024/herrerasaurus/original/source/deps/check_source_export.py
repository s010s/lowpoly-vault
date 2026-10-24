#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Audit a .blend's actual export collection against the exact shipped static GLB.

blender -b --factory-startup --disable-autoexec --python-exit-code 1 \
  --python scripts/check_source_export.py -- --source model.blend --glb model.glb \
  --output source-export.report.json

Reads the source, never saves it or exports a replacement. No visual/factual approval.
"""
import argparse
from datetime import datetime, timezone
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_reproducibility import file_hash, write_new_report
from qa_glb import audit_glb


def compare_source_audit(source, exported, source_sha256, glb_sha256, tolerance=0.0001):
    """Pure comparison for regression tests; live producer supplies fresh audit results."""
    report = {'schema_version': 1, 'check': 'source_export', 'status': 'fail', 'source_sha256': source_sha256,
              'glb_sha256': glb_sha256, 'errors': [], 'warnings': [], 'triangles_match': False, 'bounds_match': False,
              'tolerance_m': tolerance, 'created_at': datetime.now(timezone.utc).isoformat(),
              'limitations': 'Compares evaluated source count and axis-converted bounds. Does not establish material equivalence, scientific accuracy or visual quality.'}
    try:
        if not math.isfinite(tolerance) or not 0 <= tolerance <= 0.0001:
            raise ValueError('Tolerance must be finite, nonnegative and no looser than 0.0001 meter')
        report['errors'] += [f'source: {error}' for error in source['errors']]
        report['errors'] += [f'glb: {error}' for error in exported['errors']]
        report['warnings'] += [f'source: {warning}' for warning in source.get('warnings', [])]
        report['warnings'] += [f'glb: {warning}' for warning in exported.get('warnings', [])]
        report['source_triangles'] = source['triangles']
        report['glb_triangles'] = exported['scene_triangles']
        report['triangles_match'] = type(source['triangles']) is int and source['triangles'] > 0 and source['triangles'] == exported['scene_triangles']
        if not report['triangles_match']:
            report['errors'].append('Source/export scene triangle counts differ or are invalid')
        bounds = source['bounds_blender_m']
        expected = {'min': [bounds['min'][0], bounds['min'][2], -bounds['max'][1]],
                    'max': [bounds['max'][0], bounds['max'][2], -bounds['min'][1]]}
        measured = exported['bounds_m']
        values = [value for side in ('min', 'max') for value in (*expected[side], *measured[side])]
        if not all(type(value) in (int, float) and math.isfinite(value) for value in values):
            raise ValueError('Source/export bounds must be finite numbers')
        delta = max(abs(measured[side][i] - expected[side][i]) for side in ('min', 'max') for i in range(3))
        report.update(bounds_max_error_m=delta, expected_glb_bounds_m=expected, measured_glb_bounds_m=measured,
                      source_bounds_blender_m=bounds, bounds_match=delta <= tolerance)
        if not report['bounds_match']:
            report['errors'].append(f'Source/export axis-converted bounds differ by {delta} m')
        if not report['errors']:
            report['status'] = 'pass_with_warnings' if report['warnings'] else 'pass'
    except (ValueError, KeyError, TypeError, IndexError, OverflowError) as exc:
        report['errors'].append(str(exc))
    return report


def main():
    argv = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--glb', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path, help='new evidence path; never overwrites')
    parser.add_argument('--collection', help='exact export collection name; otherwise requires one asset_root-marked collection')
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.exit(1, 'Report already exists; choose a new immutable evidence path.\n')
    result = {'schema_version': 1, 'check': 'source_export', 'status': 'fail', 'errors': [], 'warnings': [],
              'triangles_match': False, 'bounds_match': False}
    try:
        import bpy
        from asset_common import audit_source
        source, glb = args.source.resolve(), args.glb.resolve()
        source_hash, glb_hash = file_hash(source), file_hash(glb)
        result.update(source_sha256=source_hash, glb_sha256=glb_hash)
        bpy.context.preferences.filepaths.use_scripts_auto_execute = False
        bpy.ops.wm.open_mainfile(filepath=str(source), load_ui=False, use_scripts=False)
        bpy.context.view_layer.update()
        if args.collection:
            collection = bpy.data.collections.get(args.collection)
            if collection is None:
                raise ValueError(f'Export collection not found: {args.collection}')
        else:
            candidates = [collection for collection in bpy.data.collections if collection.get('asset_root')]
            if len(candidates) != 1:
                raise ValueError('Exactly one asset_root-marked export collection required; pass --collection explicitly')
            collection = candidates[0]
        source_audit = audit_source(collection, max_triangles=10**9)
        exported = audit_glb(glb, max_triangles=10**9, max_materials=10**6, max_primitives=10**6)
        result = compare_source_audit(source_audit, exported, source_hash, glb_hash)
        result.update(blender_version=bpy.app.version_string, source_path=str(source), glb_path=str(glb),
                      export_collection=collection.name, script_autoexec=False, source_saved=False,
                      source_audit=source_audit, glb_audit=exported)
        if file_hash(source) != source_hash or file_hash(glb) != glb_hash:
            result['errors'].append('Source or GLB changed during audit')
            result['status'] = 'fail'
    except (ImportError, OSError, ValueError, RuntimeError, KeyError, TypeError) as exc:
        result['errors'].append(str(exc))
        result['status'] = 'fail'
    write_new_report(args.output, result)
    print(f'Source/export {result["status"]}: {args.output}')
    if result['errors']:
        # Blender's --python-exit-code makes this a reliable failing process.
        raise RuntimeError('; '.join(result['errors']))


if __name__ == '__main__':
    main()
