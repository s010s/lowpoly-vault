#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Planning/schema/hash checks, not model or scientific acceptance."""
from pathlib import Path
import hashlib,json,unittest
from validate_candidate import check_brief,STAGES
BASE=Path(__file__).resolve().parents[1]/'production/small-fauna-v1'
D=BASE/'remaining-20'
PILOTS={'bothriolepis','waptia','juracimbrophlebia','asteroxylon'}
EXPECTED={'ichthyornis','archaeopteryx','confuciusornis','longipteryx','cephalaspis','dapedium','diplomystus','pycnodus','canadaspis','callichimaera','saccocoma','urasterella','archaeocidaris','burgessomedusa','alienopterus','ceratomyrmex','kalligramma','aglaophyton','onoclea','hydropteris'}
class RemainingTwentyPlanTests(unittest.TestCase):
    def test_exact_scope_and_no_duplicate_variants(self):
        plan=json.loads((D/'batch-plan.json').read_text());ids=[x['asset_id'] for x in plan['jobs']]
        self.assertEqual(len(ids),20);self.assertEqual(set(ids),EXPECTED)
        self.assertEqual(len(set(ids)),20);self.assertFalse(set(ids)&PILOTS)
        queue=json.loads((BASE/'queue.json').read_text())
        self.assertEqual({x['asset_id'] for x in queue['jobs']},EXPECTED|PILOTS)
        self.assertEqual(len(queue['jobs']),24)
        self.assertEqual({x['id'] for x in json.loads((D/'source-snapshot.json').read_text())['assets']},EXPECTED)
    def test_all_twenty_frozen_files_and_existing_brief_contract(self):
        for aid in EXPECTED:
            with self.subTest(asset=aid):
                p=D/aid;b=json.loads((p/'brief.json').read_text());refs=json.loads((p/'references.json').read_text());config=json.loads((p/'build-config.json').read_text());freeze=json.loads((p/'freeze.json').read_text())
                required,_=check_brief(b,{'asset_id':aid},{x['id'] for x in refs['sources']})
                self.assertEqual(required,set(STAGES));self.assertEqual(b['quality_tier'],'environment-prop')
                self.assertEqual(b['required_views'],['hero','front','right','rear','top','clay']);self.assertEqual(b['turntable_frames'],0)
                self.assertEqual(config['required_views'],b['required_views']);self.assertEqual(config['geometry_policy'],b['geometry_policy']);self.assertEqual(config['texture_policy'],b['texture_policy'])
                self.assertEqual(config['maker_model'],'GPT-6 Astra');self.assertEqual(config['maker_reasoning_effort'],'xhigh')
                self.assertTrue(config['motion']['static_only']);self.assertFalse(config['motion']['animation_ready_claim'])
                self.assertLessEqual(config['geometry_policy']['max_triangles'],12000)
                for name,digest in freeze['sha256'].items():self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),digest)
    def test_five_balanced_four_subject_batches_and_bird_priority(self):
        batches=json.loads((D/'batch-plan.json').read_text())['batches']
        self.assertEqual(len(batches),5);self.assertTrue(all(len(x['asset_ids'])==4 for x in batches))
        first_two={x for b in batches[:2] for x in b['asset_ids']}
        self.assertTrue({'ichthyornis','archaeopteryx','confuciusornis','longipteryx'}<=first_two)
        self.assertEqual([b['id'] for b in batches],['batch-a','batch-b','batch-c','batch-d','batch-e'])
    def test_longipteryx_has_updated_diet_reference_without_fishing_scene(self):
        refs=json.loads((D/'longipteryx/references.json').read_text())
        self.assertTrue(any('2024.08.012' in x['url'] for x in refs['sources']))
        config=json.loads((D/'longipteryx/build-config.json').read_text())
        self.assertIn('no captured prey',config['pose'])
if __name__=='__main__':unittest.main()
