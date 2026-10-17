#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Research-only schema + cross-field checker. Not glTF/device/visual validation.
Usage: python check_budget_record.py schema.json record.json
Requires jsonschema (tested version must be recorded separately).
"""
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator

def check(schema, record):
    Draft202012Validator.check_schema(schema)
    errors = [f"{'/'.join(map(str, e.absolute_path))}: {e.message}"
              for e in Draft202012Validator(schema).iter_errors(record)]
    if errors:
        return errors
    sha = record["artifact"]["sha256"]
    for name, gate in record["gates"].items():
        if gate["artifact_sha256"] != sha:
            errors.append(f"gates/{name}: evidence hash differs from artifact")
    for exc in record["exceptions"]:
        if exc["artifact_sha256"] != sha:
            errors.append("exception evidence hash differs from artifact")
    if len({e["metric"] for e in record["exceptions"]}) != len(record["exceptions"]):
        errors.append("duplicate metric exceptions")
    if record["release_status"] == "approved_for_context":
        if not record["gates"]["technical"]["required"]:
            errors.append("technical gate must be required for approval")
        if not any(v is not None for v in record["budget_contract"]["limits"].values()):
            errors.append("approval needs explicit frozen limits")
        exception_limits = {e["metric"]: e["approved_limit"] for e in record["exceptions"]}
        for key, limit in record["budget_contract"]["limits"].items():
            if limit is None:
                continue
            value = record["metrics"][key]["value"]
            allowed = exception_limits.get(key, limit)
            if value is None:
                errors.append(f"{key}: bounded metric is unknown")
            elif value > allowed:
                errors.append(f"{key}: {value} exceeds effective limit {allowed}")
    return errors

if __name__ == "__main__":
    schema, record = (json.loads(Path(p).read_text()) for p in sys.argv[1:3])
    errors = check(schema, record)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    raise SystemExit(1 if errors else 0)
