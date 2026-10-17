#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("record_checker", ROOT / "scripts/check_budget_record.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
SCHEMA = json.loads((ROOT / "proposals/asset-budget-record.schema.json").read_text())
EXAMPLE = json.loads((ROOT / "proposals/triceratops-light.example.json").read_text())

class BudgetRecordTests(unittest.TestCase):
    def setUp(self):
        self.r = copy.deepcopy(EXAMPLE)
    def check(self):
        return module.check(SCHEMA, self.r)
    def approve_fixture(self):
        self.r["release_status"] = "approved_for_context"
        self.r["budget_contract"]["status"] = "frozen_after_calibration"
        self.r["budget_contract"]["limits"] = {"stored_glb_bytes": 500000}
        for gate in self.r["gates"].values():
            gate.update(status="pass", summary="Synthetic test evidence only",
                        evidence_refs=["test-fixture://not-real-approval"])
    def test_held_example_valid(self):
        self.assertEqual(self.check(), [])
    def test_unknown_gate_cannot_approve(self):
        self.r["release_status"] = "approved_for_context"
        self.assertTrue(self.check())
    def test_synthetic_approved_fixture(self):
        self.approve_fixture()
        self.assertEqual(self.check(), [])
    def test_mismatched_evidence_hash(self):
        self.r["gates"]["technical"]["artifact_sha256"] = "0" * 64
        self.assertTrue(self.check())
    def test_unknown_not_zero(self):
        self.r["metrics"]["decode_ms"]["value"] = 0
        self.assertTrue(self.check())
    def test_negative_metric(self):
        self.r["metrics"]["stored_glb_bytes"]["value"] = -1
        self.assertTrue(self.check())
    def test_wrong_unit(self):
        self.r["metrics"]["stored_glb_bytes"]["unit"] = "count"
        self.assertTrue(self.check())
    def test_pass_needs_reference(self):
        self.r["gates"]["technical"]["evidence_refs"] = []
        self.assertTrue(self.check())
    def test_extra_field_rejected(self):
        self.r["unreviewed_auto_pass"] = True
        self.assertTrue(self.check())
    def test_exceeded_frozen_limit(self):
        self.approve_fixture()
        self.r["budget_contract"]["limits"]["stored_glb_bytes"] = 450000
        self.assertTrue(self.check())
    def test_unknown_bounded_metric(self):
        self.approve_fixture()
        self.r["budget_contract"]["limits"]["decode_ms"] = 20
        self.assertTrue(self.check())
    def test_explicit_exception(self):
        self.approve_fixture()
        self.r["budget_contract"]["limits"]["stored_glb_bytes"] = 450000
        self.r["exceptions"] = [{
            "metric": "stored_glb_bytes", "approved_limit": 475000,
            "artifact_sha256": self.r["artifact"]["sha256"],
            "reason": "Synthetic test only", "evidence_ref": "test-fixture://synthetic",
            "approved_by": "test-only", "validity_condition": "test-only",
            "fallback": "test-only"
        }]
        self.assertEqual(self.check(), [])
    def test_empty_frozen_contract_rejected(self):
        self.approve_fixture()
        self.r["budget_contract"]["limits"] = {}
        self.assertTrue(self.check())

    def test_all_unknown_frozen_limits_rejected(self):
        self.approve_fixture()
        self.r["budget_contract"]["limits"] = {"stored_glb_bytes": None}
        self.assertTrue(self.check())
    def test_fractional_byte_count_rejected(self):
        self.r["metrics"]["stored_glb_bytes"]["value"] = 471784.5
        self.assertTrue(self.check())

if __name__ == "__main__":
    unittest.main()
