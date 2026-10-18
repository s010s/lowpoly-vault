#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Recovered plan/code checks only; not asset or scientific acceptance."""
from pathlib import Path
import hashlib,json,unittest
from validate_candidate import check_brief,STAGES
BASE=Path(__file__).resolve().parents[1]/'production/small-fauna-v1'
class RecoveredPlanTests(unittest.TestCase):
    def test_queue_has_twenty_four_unique_subjects(self):
        queue=json.loads((BASE/'queue.json').read_text());ids=[x['asset_id'] for x in queue['jobs']]
        self.assertEqual(len(ids),24);self.assertEqual(len(set(ids)),24)
    def test_recovered_briefs_hash_and_keep_all_stages(self):
        for folder in (BASE/'pilot').iterdir():
            with self.subTest(asset=folder.name):
                brief=json.loads((folder/'brief.json').read_text());refs=json.loads((folder/'references.json').read_text());freeze=json.loads((folder/'freeze.json').read_text())
                required,_=check_brief(brief,{'asset_id':folder.name},{x['id'] for x in refs['sources']})
                self.assertEqual(required,set(STAGES));self.assertEqual(brief['turntable_frames'],0)
                self.assertEqual(len(brief['required_views']),6);self.assertFalse(brief['recovery']['byte_identical_to_old_brief'])
                for name,digest in freeze['sha256'].items():self.assertEqual(hashlib.sha256((folder/name).read_bytes()).hexdigest(),digest)
    def test_policy_preserves_creative_scope_and_bounded_review(self):
        policy=json.loads((BASE/'acceptance-profile.json').read_text())
        self.assertIn('No per-model user review',policy['review_policy']['escalation'])
        self.assertIn('one planned cosmetic repair',policy['review_policy']['revision_bound'])
if __name__=='__main__':unittest.main()
