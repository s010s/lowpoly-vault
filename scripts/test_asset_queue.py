#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tiny subprocess fixtures only; these tests do not measure Blender throughput."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest

RUNNER = Path(__file__).with_name('run_asset_queue.py')
FIXTURE = '''import json, os, pathlib, subprocess, sys, time
out = pathlib.Path(sys.argv[1]); mode = sys.argv[2]
started = time.monotonic()
(out / 'frame-000.png').write_bytes(b'tiny subprocess fixture, not a rendered image')
(out / 'started.json').write_text(json.dumps({'pid':os.getpid(),'started':started}))
if mode == 'fail': raise SystemExit(7)
if mode in ('timeout', 'cancel', 'orphan'):
    child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'])
    (out / 'child.pid').write_text(str(child.pid))
    if mode != 'orphan': time.sleep(30)
if mode == 'mutate': pathlib.Path(sys.argv[3]).write_text('changed while running')
if mode == 'escape':
    (out / 'result.json').symlink_to(sys.argv[3]); raise SystemExit(0)
if mode == 'memory':
    allocation = bytearray(512 * 1024 * 1024)
time.sleep(0.15)
(out / 'result.json').write_text(json.dumps({'start':started,'end':time.monotonic(),'threads':os.environ['OMP_NUM_THREADS']}))
'''


class QueueTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='asset-queue-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.fixture = self.base / 'fixture.py'
        self.fixture.write_text(FIXTURE)
        self.data = self.base / 'input.txt'
        self.data.write_text('original')
        self.manifest = self.base / 'jobs.json'
        self.root = self.base / 'runs'

    def spec(self, asset='asset', mode='success'):
        return {'asset_id':asset, 'revision':'r1', 'job_id':'preview',
                'argv':[sys.executable,'{input:script}','{output_dir}',mode,'{input:data}'],
                'inputs':{'script':str(self.fixture),'data':str(self.data)},
                'outputs':['result.json'], 'config':{'resolution':256}}

    def save(self, jobs):
        self.manifest.write_text(json.dumps({'schema_version':1,'lane':'preview','jobs':jobs}))

    def command(self, *extra):
        return [sys.executable,str(RUNNER),str(self.manifest),'--runs-root',str(self.root),
                '--allow-executable',sys.executable,'--threads','1','--kill-grace-seconds','0.1',*extra]

    def invoke(self, *extra, expected=0):
        result = subprocess.run(self.command(*extra),capture_output=True,text=True,timeout=15)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        lines = [json.loads(line) for line in result.stdout.splitlines()]
        return json.loads(Path(lines[-1]['summary']).read_text()) if lines else None

    def test_success_bounded_concurrency_collision_isolation(self):
        self.save([self.spec('asset-' + str(i)) for i in range(5)])
        summary = self.invoke('--workers','2')
        self.assertEqual(summary['peak_active_jobs'],2)
        self.assertLessEqual(summary['sampled_peak_processes'],2)
        self.assertEqual(len(summary['results']),5)
        folders = [Path(record['attempt_dir']) for record in summary['results']]
        self.assertEqual(len(set(folders)),5)
        spans = [json.loads((folder/'outputs/result.json').read_text()) for folder in folders]
        peak = max(sum(span['start'] <= event < span['end'] for span in spans)
                   for event in [span['start'] for span in spans])
        self.assertEqual(peak,2)
        self.assertTrue(all(span['threads']=='1' for span in spans))

    def test_resume_hashes_and_immutable_records(self):
        jobs = [self.spec()]
        self.save(jobs)
        first = self.invoke()
        original = Path(first['results'][0]['attempt_dir'])
        frozen_result = (original/'result.json').read_bytes()
        self.assertEqual(self.invoke('--resume')['results'][0]['status'],'reused')
        self.assertEqual((original/'result.json').read_bytes(),frozen_result)
        (original/'outputs/result.json').write_text('tampered')
        rerun = self.invoke('--resume')
        self.assertEqual(rerun['results'][0]['status'],'succeeded')
        self.assertNotEqual(rerun['results'][0]['attempt_dir'],str(original))
        self.data.write_text('new input')
        changed = self.invoke('--resume')
        self.assertNotEqual(changed['results'][0]['fingerprint'],first['results'][0]['fingerprint'])
        jobs[0]['config']['resolution'] = 512
        self.save(jobs)
        config = self.invoke('--resume')
        self.assertNotEqual(config['results'][0]['fingerprint'],changed['results'][0]['fingerprint'])
        self.fixture.write_text(FIXTURE + '\n# helper change\n')
        script = self.invoke('--resume')
        self.assertNotEqual(script['results'][0]['fingerprint'],config['results'][0]['fingerprint'])

    def test_malformed_typed_resume_records_start_new_attempt(self):
        for index, (filename, value) in enumerate((('result.json', []),
                ('request.json', []), ('request.json', {'identity': []}),
                ('result.json', {'status':'succeeded', 'outputs':[]}))):
            with self.subTest(filename=filename, value=value):
                self.save([self.spec('malformed-' + str(index))])
                first = self.invoke()['results'][0]
                (Path(first['attempt_dir'])/filename).write_text(json.dumps(value))
                second = self.invoke('--resume')['results'][0]
                self.assertEqual(second['status'], 'succeeded')
                self.assertNotEqual(second['attempt_dir'], first['attempt_dir'])

    def test_undeclared_frame_tampering_invalidates_resume(self):
        self.save([self.spec()])
        first = self.invoke()['results'][0]
        folder = Path(first['attempt_dir'])
        unchanged_manifest = (folder/'outputs/result.json').read_bytes()
        (folder/'outputs/frame-000.png').write_bytes(b'tampered frame')
        second = self.invoke('--resume')['results'][0]
        self.assertEqual(second['status'],'succeeded')
        self.assertNotEqual(second['attempt_dir'],first['attempt_dir'])
        self.assertEqual((folder/'outputs/result.json').read_bytes(),unchanged_manifest)
        (Path(second['attempt_dir'])/'outputs/frame-000.png').unlink()
        third = self.invoke('--resume')['results'][0]
        self.assertEqual(third['status'],'succeeded')
        self.assertNotEqual(third['attempt_dir'],second['attempt_dir'])

    def test_root_lock_rejects_overlapping_invocation(self):
        self.save([self.spec(mode='cancel')])
        process = subprocess.Popen(self.command(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        deadline = time.monotonic()+5
        while not list(self.root.glob('preview/**/child.pid')) and time.monotonic()<deadline:
            time.sleep(0.01)
        other = subprocess.run(self.command(),capture_output=True,text=True,timeout=5)
        self.assertEqual(other.returncode,2)
        self.assertIn('Another queue is active',other.stderr)
        process.send_signal(signal.SIGTERM)
        process.communicate(timeout=5)

    def test_failure_retry_is_new_attempt_and_not_resumed(self):
        self.save([self.spec(mode='fail')])
        result = self.invoke('--retries','1',expected=1)
        self.assertEqual([item['status'] for item in result['results']],['failed','failed'])
        self.assertEqual(len({item['attempt_dir'] for item in result['results']}),2)
        resumed = self.invoke('--resume',expected=1)
        self.assertEqual(resumed['results'][0]['status'],'failed')
        self.assertNotIn(resumed['results'][0]['attempt_dir'],{x['attempt_dir'] for x in result['results']})

    def test_timeout_kills_process_group(self):
        self.save([self.spec(mode='timeout')])
        result = self.invoke('--timeout-seconds','0.3',expected=1)['results'][0]
        self.assertEqual(result['status'],'timed_out')
        self.assertLess(result['wall_seconds'],3)
        child = int((Path(result['attempt_dir'])/'outputs/child.pid').read_text())
        self.assert_process_gone(child)

    def test_success_cleans_orphan_descendant(self):
        self.save([self.spec(mode='orphan')])
        result = self.invoke()['results'][0]
        child = int((Path(result['attempt_dir'])/'outputs/child.pid').read_text())
        self.assert_process_gone(child)

    def assert_process_gone(self, pid):
        stat = Path(f'/proc/{pid}/stat')
        if stat.exists():
            self.assertEqual(stat.read_text().rsplit(')',1)[1].split()[0],'Z')

    def test_cancel_stops_new_jobs_and_cleans_children(self):
        self.save([self.spec('first','cancel'), self.spec('never-launched')])
        process = subprocess.Popen(self.command(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        deadline = time.monotonic()+5
        child_files = []
        while not child_files and time.monotonic()<deadline:
            child_files = list(self.root.glob('preview/**/child.pid'))
            time.sleep(0.03)
        self.assertTrue(child_files)
        process.send_signal(signal.SIGTERM)
        stdout,stderr = process.communicate(timeout=5)
        self.assertEqual(process.returncode,143,stdout+stderr)
        result = json.loads(Path(json.loads(stdout.splitlines()[-1])['summary']).read_text())
        self.assertEqual(result['results'][0]['status'],'cancelled')
        self.assertEqual(result['unstarted'][0]['asset_id'],'never-launched')
        self.assertEqual(result['unstarted'][0]['status'],'cancelled_before_launch')
        self.assert_process_gone(int(child_files[0].read_text()))

    def test_cancel_drain_finishes_active_only(self):
        self.save([self.spec('first'), self.spec('never-launched')])
        process = subprocess.Popen(self.command('--on-cancel','drain'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        deadline = time.monotonic()+5
        while not list(self.root.glob('preview/**/started.json')) and time.monotonic()<deadline:
            time.sleep(0.01)
        process.send_signal(signal.SIGTERM)
        stdout,stderr = process.communicate(timeout=5)
        self.assertEqual(process.returncode,143,stdout+stderr)
        result = json.loads(Path(json.loads(stdout.splitlines()[-1])['summary']).read_text())
        self.assertEqual(result['results'][0]['status'],'succeeded')
        self.assertEqual(len(result['unstarted']),1)

    def test_input_mutation_not_successful(self):
        self.save([self.spec(mode='mutate')])
        self.assertEqual(self.invoke(expected=1)['results'][0]['status'],'inputs_changed')

    def test_missing_and_escaping_outputs_rejected(self):
        spec = self.spec()
        spec['outputs'] = ['not-produced.png']
        self.save([spec])
        self.assertEqual(self.invoke(expected=1)['results'][0]['status'],'outputs_invalid')
        self.save([self.spec(mode='escape')])
        self.assertEqual(self.invoke(expected=1)['results'][0]['status'],'outputs_invalid')
        spec['outputs'] = ['../escape.png']
        self.save([spec])
        self.invoke(expected=2)

    def test_memory_limit_applied(self):
        self.save([self.spec(mode='memory')])
        result = self.invoke('--memory-mb','128',expected=1)['results'][0]
        self.assertEqual(result['status'],'failed')
        self.assertIn('MemoryError',(Path(result['attempt_dir'])/'stderr.log').read_text())

    def test_duplicate_identity_and_unbounded_requests_rejected(self):
        self.save([self.spec(),self.spec()])
        self.invoke(expected=2)
        self.save([self.spec()])
        self.invoke('--workers','1000',expected=2)
        self.invoke('--cpu-budget','1','--workers','2',expected=2)
        spec = self.spec(); spec['argv'][0] = '/bin/sh'
        self.save([spec]); self.invoke(expected=2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
