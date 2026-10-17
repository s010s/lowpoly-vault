#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Use repository queue on macOS with a declared two-CPU allocation.
macOS has no sched_getaffinity/cgroup; do not invent Linux affinity evidence.
"""
import os,sys
from pathlib import Path
REPO=next(p for p in Path(__file__).resolve().parents if (p/'scripts/run_asset_queue.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
import run_asset_queue as queue
queue.capacity=lambda: {'affinity_cpus':None,'affinity_cpu_count':None,'visible_cgroup_cpu_quota':None,'known_cpu_budget':2,'allocation_source':'explicit task allocation of 2 CPU threads; macOS affinity unobservable','host_logical_cpus':os.cpu_count()}
if __name__=='__main__':queue.main()
