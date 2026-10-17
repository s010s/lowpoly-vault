#!/usr/bin/env python3
"""Read-only integration proof against a real repository GLB, never fake approval."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECORD = 'qa/pipeline-pilot/legacy-natural-arch/candidate.json'

class RealAssetPilot(unittest.TestCase):
    def test_real_asset_is_valid_but_unknown_is_not_approved(self):
        cmd = [sys.executable, str(ROOT/'scripts/validate_candidate.py'), RECORD, '--root', str(ROOT), '--json']
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(p.returncode, 0, p.stdout+p.stderr)
        result = json.loads(p.stdout)
        self.assertTrue(result['valid'])
        self.assertFalse(result['approved_for_brief'])
        self.assertEqual(result['measurements']['triangles'], 672)
        self.assertEqual(result['measurements']['glb_bytes'], 40656)
        self.assertIn('visual: unknown', result['approval_blockers'])
        p = subprocess.run(cmd+['--require-approved'], capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(p.returncode, 1, p.stdout+p.stderr)
        self.assertFalse(json.loads(p.stdout)['approved_for_brief'])

if __name__ == '__main__':
    unittest.main()
