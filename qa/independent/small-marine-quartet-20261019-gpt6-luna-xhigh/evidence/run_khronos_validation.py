#!/usr/bin/env python3
"""Validate the exact frozen GLBs through the pinned Khronos validator without touching them."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT=Path.cwd()
QA=Path('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence/khronos')
INPUTS=json.loads(Path('qa/independent/small-marine-quartet-20261019-gpt6-luna-xhigh/evidence/inputs.json').read_text())

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def main():
    QA.mkdir(parents=True,exist_ok=True)
    summary={'schema_version':1,'kind':'independent_khronos_validation','created_at_utc':datetime.now(timezone.utc).isoformat(),'command_template':['node','scripts/validate_gltf.cjs','<temporary-identical-copy.glb>'],'validator_package':'gltf-validator','validator_version':'2.0.0-dev.3.10','method':'Pinned project wrapper and official validator; input bytes copied to a temporary directory because the wrapper writes qa.json and gltf-validator.report.json beside its input.','warning_policy':'Project wrapper applies the checked-in ACCESSOR_INDEX_TRIANGLE_DEGENERATE severity override; all emitted issues are retained.','results':[]}
    with tempfile.TemporaryDirectory(prefix='s010s-marine-qa-') as temp:
        tmp=Path(temp)
        for spec in INPUTS['assets']:
            src=ROOT/spec['glb']; before=digest(src); start=datetime.now(timezone.utc).isoformat(); t0=time.monotonic()
            dest=tmp/f'{spec["asset_id"]}.glb';shutil.copyfile(src,dest)
            if digest(dest)!=before:raise SystemExit(f'{spec["asset_id"]}: temporary validation copy is not byte-identical')
            proc=subprocess.run(['node','scripts/validate_gltf.cjs',str(dest)],cwd=ROOT,text=True,capture_output=True)
            elapsed=round(time.monotonic()-t0,6);finish=datetime.now(timezone.utc).isoformat()
            raw_report=dest.parent/'gltf-validator.report.json';raw_qa=dest.parent/'qa.json'
            if not raw_report.exists() or not raw_qa.exists():raise SystemExit(f'{spec["asset_id"]}: validator emitted no report')
            report_out=QA/f'{spec["asset_id"]}.gltf-validator.report.json';qa_out=QA/f'{spec["asset_id"]}.validator-qa.json'
            if report_out.exists() or qa_out.exists():raise FileExistsError('Choose fresh immutable report paths')
            shutil.copyfile(raw_report,report_out);shutil.copyfile(raw_qa,qa_out)
            parsed=json.loads(raw_qa.read_text())['khronos_validator']
            raw=json.loads(raw_report.read_text());issues=raw['issues']
            result={'asset_id':spec['asset_id'],'revision':spec['revision'],'input_path':spec['glb'],'input_sha256':before,'input_bytes':src.stat().st_size,'copied_input_sha256':digest(dest),'started_at_utc':start,'finished_at_utc':finish,'elapsed_wall_seconds_monotonic':elapsed,'returncode':proc.returncode,'stdout':proc.stdout.strip(),'stderr':proc.stderr.strip(),'status':parsed['status'],'validator_version':parsed['validator_version'],'num_errors':parsed['num_errors'],'num_warnings':parsed['num_warnings'],'truncated':parsed.get('truncated',False),'issue_messages':issues.get('messages',[]),'raw_report':report_out.as_posix(),'raw_report_sha256':digest(report_out),'raw_qa':qa_out.as_posix(),'raw_qa_sha256':digest(qa_out),'source_glb_unchanged':digest(src)==before}
            summary['results'].append(result)
            if proc.returncode or parsed['status'] not in ('pass','pass_with_warnings') or not result['source_glb_unchanged']:
                raise SystemExit(f'{spec["asset_id"]}: Khronos validation failed')
    summary['finished_at_utc']=datetime.now(timezone.utc).isoformat();summary['status']='pass'
    output=QA/'summary.json';output.write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(json.dumps({'status':summary['status'],'assets':len(summary['results']),'output':output.as_posix()},indent=2))

if __name__=='__main__':main()
