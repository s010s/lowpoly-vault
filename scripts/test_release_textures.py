#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Synthetic embedded-image regressions; no real asset or license is certified."""
import copy,json,tempfile,unittest
from pathlib import Path
from test_validate_candidate import build_fixture,digest
from check_release_textures import check_textures

class ReleaseTextureTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.record,self.path=build_fixture(self.root,textured=True)
        self.refs=self.root/self.record['artifacts']['references']['path'];data=json.loads(self.refs.read_text());data['sources'][0].update(use='original-authored incorporated texture',creator='Leon Made This / s010s',license='CC-BY-4.0',rights_note='SYNTHETIC TEST ONLY; not a real license attestation.');self.refs.write_text(json.dumps(data));self.record['artifacts']['references']['sha256']=digest(self.refs.read_bytes())
        self.record['textures'][0]['provenance'].update(creator='Leon Made This / s010s',license='CC-BY-4.0');self.candidate=self.path.relative_to(self.root).as_posix()
    def run_check(self):self.path.write_text(json.dumps(self.record));return check_textures(self.candidate,self.root)
    def test_exact_image_and_frozen_budget_pass_without_granting_approval(self):
        r=self.run_check();self.assertEqual(r['status'],'pass',r);self.assertEqual(r['measurements']['decoded_texture_bytes_estimate'],4);self.assertFalse(r['grants_approval']);self.assertFalse(r['grants_publication'])
    def test_missing_duplicate_and_wrong_index_records_fail(self):
        original=copy.deepcopy(self.record['textures'])
        for textures in [[],original+original,[{**original[0],'image_index':True}],[{**original[0],'image_index':2}]]:
            self.record['textures']=textures;self.assertEqual(self.run_check()['status'],'fail')
    def test_rehashed_original_file_must_equal_actual_glb_bytes(self):
        row=self.record['textures'][0];p=self.root/row['path'];p.write_bytes(p.read_bytes()+b'changed');row['sha256']=digest(p.read_bytes());self.assertIn('differs from embedded',self.run_check()['errors'][0])
    def test_wrong_dimensions_fail(self):
        self.record['textures'][0]['width']=2;self.assertIn('dimensions/bytes',self.run_check()['errors'][0])
    def test_consulted_reference_cannot_be_reused_as_texture(self):
        data=json.loads(self.refs.read_text());data['sources'][0]['use']='consulted-only';self.refs.write_text(json.dumps(data));self.record['artifacts']['references']['sha256']=digest(self.refs.read_bytes());self.assertIn('Consulted sources',self.run_check()['errors'][0])
    def test_creator_and_license_must_match_original_owner_record(self):
        for key in ['creator','license']:
            old=self.record['textures'][0]['provenance'][key];self.record['textures'][0]['provenance'][key]='unknown';self.assertEqual(self.run_check()['status'],'fail');self.record['textures'][0]['provenance'][key]=old
    def test_all_texture_budgets_are_enforced(self):
        pin=self.record['artifacts']['brief'];p=self.root/pin['path'];original=p.read_bytes()
        for key in ['max_textures','max_dimension','max_total_bytes','max_decoded_bytes']:
            data=json.loads(original);data['texture_policy'][key]=0;p.write_text(json.dumps(data));pin['sha256']=digest(p.read_bytes());self.assertIn('exceeds frozen',self.run_check()['errors'][0])
    def test_duplicate_source_ids_fail(self):
        data=json.loads(self.refs.read_text());data['sources'].append(data['sources'][0]);self.refs.write_text(json.dumps(data));self.record['artifacts']['references']['sha256']=digest(self.refs.read_bytes());self.assertIn('Duplicate source',self.run_check()['errors'][0])
    def test_external_image_path_and_symlink_fail(self):
        row=self.record['textures'][0];original=row['path'];row['path']='../outside.png';self.assertEqual(self.run_check()['status'],'fail');row['path']=original;p=self.root/original;target=p.with_suffix('.original');p.rename(target);p.symlink_to(target);self.assertIn('symlink',self.run_check()['errors'][0])

if __name__=='__main__':unittest.main()
