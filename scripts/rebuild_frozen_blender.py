#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run a frozen generator on installed Blender without editing its source.

Blender 5.2 Boolean evaluation may append unused empty material slots. Remove
only those slots before the existing source audit. Referenced empty slots fail.
This is a new local build, never a replacement for historical execution logs.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--generator', required=True, type=Path)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    spec = importlib.util.spec_from_file_location('frozen_asset_generator', args.generator.resolve())
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_export = module.export_asset

    def export_with_compatible_slots(asset_id, names, category, collection, **kwargs):
        removed = []
        for obj in collection.all_objects:
            if obj.type != 'MESH':
                continue
            used = {polygon.material_index for polygon in obj.data.polygons}
            empty = [i for i, material in enumerate(obj.data.materials) if material is None]
            if used.intersection(empty):
                raise RuntimeError(f'{obj.name}: referenced empty material slot; refusing cleanup')
            for index in reversed(empty):
                obj.data.materials.pop(index=index)
                removed.append({'object':obj.name, 'unused_empty_slot':index})
        print('LOCAL_BLENDER_COMPAT=' + json.dumps({'removed_unused_empty_slots':removed}), flush=True)
        return original_export(asset_id, names, category, collection, **kwargs)

    module.export_asset = export_with_compatible_slots
    sys.argv = [str(args.generator), '--', '--config', str(args.config), '--output-dir', str(args.output_dir)]
    module.main()


if __name__ == '__main__':
    main()
