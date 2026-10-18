#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Bounded, append-only cloud asset queue. See skills/blender-lowpoly-pipeline/references/parallel-queue.md.

Trusted local job specifications only: this is a scheduler, not a code sandbox.
"""
from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import subprocess
import sys
import time
import uuid

VERSION = 1
MAX_WORKERS = 8
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\Z")
TOKEN = re.compile(r"\{(input:[A-Za-z0-9_.-]+|output_dir|threads|blender)\}")
THREAD_ENV = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_once(path, data):
    """Exclusive creation: completed records are never rewritten by this runner."""
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def file_record(path):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"Required file missing: {path}")
    return {"sha256": sha256(path), "bytes": path.stat().st_size}


def capacity():
    affinity = sorted(os.sched_getaffinity(0))
    quota = None
    # A visible cgroup v2 CPU quota may be stricter than affinity. When the
    # runtime hides cgroups, report unknown rather than advertised host cores.
    for base in (Path("/sys/fs/cgroup"),):
        try:
            limit, period = (base / "cpu.max").read_text().split()
            if limit != "max":
                quota = int(limit) / int(period)
        except (OSError, ValueError):
            pass
    return {"affinity_cpus": affinity, "affinity_cpu_count": len(affinity),
            "visible_cgroup_cpu_quota": quota,
            "known_cpu_budget": min(len(affinity), max(1, math.floor(quota))) if quota else len(affinity)}


def bounded_int(value, low, high, label):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{label} must be an integer in [{low}, {high}]")
    return value


def safe_name(value, label):
    if not isinstance(value, str) or not NAME.fullmatch(value) or value in {".", ".."}:
        raise ValueError(f"Invalid {label}: {value!r}")
    return value


def output_path(directory, name):
    path = Path(name)
    if path.is_absolute() or not path.parts or ".." in path.parts or path.as_posix() != name:
        raise ValueError(f"Output must be a normalized relative file path: {name!r}")
    result = directory / path
    if not result.resolve().is_relative_to(directory.resolve()):
        raise ValueError(f"Output escapes attempt directory: {name}")
    return result


def load_jobs(args):
    manifest = json.loads(args.manifest.read_text())
    if not isinstance(manifest, dict) or set(manifest) - {"schema_version", "lane", "jobs"}:
        raise ValueError("Manifest must be an object with only schema_version, lane, and jobs")
    if manifest.get("schema_version") != 1 or manifest.get("lane") not in {"preview", "build", "render"}:
        raise ValueError("Manifest needs schema_version 1 and lane preview, build, or render")
    if not isinstance(manifest.get("jobs"), list) or not manifest["jobs"]:
        raise ValueError("Manifest jobs must be a nonempty list")
    allowed = {Path(value).resolve() for value in args.allow_executable}
    blender = Path(args.blender).resolve()
    if blender.is_file():
        allowed.add(blender)
    seen, jobs = set(), []
    for spec in manifest["jobs"]:
        if not isinstance(spec, dict) or set(spec) - {"asset_id", "revision", "job_id", "argv", "inputs", "outputs", "config", "timeout_seconds"}:
            raise ValueError("Unknown job fields, or job is not an object")
        names = tuple(safe_name(spec.get(key), key) for key in ("asset_id", "revision", "job_id"))
        if names in seen:
            raise ValueError(f"Duplicate asset/revision/job identity: {names}")
        seen.add(names)
        inputs = spec.get("inputs")
        if not isinstance(inputs, dict) or not inputs:
            raise ValueError("Every job must declare all file inputs, including scripts/helpers")
        records = {}
        for key, value in inputs.items():
            safe_name(key, "input key")
            if not isinstance(value, str):
                raise ValueError("Input paths must be strings")
            path = (args.manifest.parent / value).resolve()
            records[key] = {"path": str(path), **file_record(path)}
        argv = spec.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and "\0" not in x for x in argv):
            raise ValueError("argv must be a nonempty list of strings; no shell command strings")
        if not any("{output_dir}" in arg for arg in argv):
            raise ValueError("argv must explicitly use the isolated {output_dir}")
        exe = blender if argv[0] == "{blender}" else Path(argv[0])
        if not exe.is_absolute() or exe.resolve() not in allowed or not os.access(exe, os.X_OK):
            raise ValueError(f"Executable must be an absolute allowlisted executable: {exe}")
        exe = exe.resolve()
        if exe == blender:
            pre = argv[1:argv.index("--")] if "--" in argv else argv[1:]
            if any(x in {"-t", "--threads", "-b", "--background", "--python-exit-code"} for x in pre):
                raise ValueError("Runner owns Blender background, threads, and python-exit-code flags")
        for arg in argv:
            for token in TOKEN.findall(arg):
                if token.startswith("input:") and token[6:] not in records:
                    raise ValueError(f"Undeclared input placeholder: {token}")
        outputs = spec.get("outputs")
        if not isinstance(outputs, list) or not outputs or not all(isinstance(x, str) for x in outputs):
            raise ValueError("outputs must list required files")
        if len(set(outputs)) != len(outputs):
            raise ValueError("Duplicate output path")
        for name in outputs:
            output_path(Path("/tmp/queue-validation"), name)
        if any(a.startswith(b + "/") for a in outputs for b in outputs if a != b):
            raise ValueError("Output paths overlap as file/directory")
        timeout = spec.get("timeout_seconds", args.timeout_seconds)
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout_seconds must be positive and finite")
        identity = {"runner_schema": VERSION, "runner_sha256": sha256(Path(__file__)),
                    "lane": manifest["lane"], "job": spec, "inputs": records,
                    "executable": {"path": str(exe), **file_record(exe)},
                    "threads": args.threads, "memory_mb": args.memory_mb, "timeout_seconds": timeout}
        digest = hashlib.sha256(canonical(identity)).hexdigest()
        jobs.append({"names": names, "spec": spec, "inputs": records, "executable": str(exe),
                     "identity": identity, "fingerprint": digest, "timeout_seconds": timeout,
                     "base": args.runs_root / manifest["lane"] / names[0] / names[1] / names[2] / digest})
    return manifest, jobs


def inputs_match(job):
    try:
        return sha256(Path(__file__)) == job["identity"]["runner_sha256"] and all(file_record(item["path"]) == {"sha256": item["sha256"], "bytes": item["bytes"]}
                   for item in job["inputs"].values()) and file_record(job["executable"]) == {
                       key: job["identity"]["executable"][key] for key in ("sha256", "bytes")}
    except (ValueError, OSError):
        return False


def collect_outputs(job, attempt):
    """Required outputs are a contract; hash the whole tree to catch undeclared frames too."""
    directory = attempt / "outputs"
    for name in job["spec"]["outputs"]:
        file_record(output_path(directory, name))
    records = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Output symlink is not allowed: {path}")
        if path.is_file():
            name = path.relative_to(directory).as_posix()
            records[name] = file_record(output_path(directory, name))
        elif not path.is_dir():
            raise ValueError(f"Output is not a regular file/directory: {path}")
    return records


def resume_result(job):
    if not inputs_match(job):
        return None
    for path in sorted(job["base"].glob("*/result.json"), reverse=True):
        try:
            record = json.loads(path.read_text())
            request = json.loads((path.parent / "request.json").read_text())
            if not isinstance(record, dict) or not isinstance(request, dict):
                continue
            if not isinstance(request.get("identity"), dict) or not isinstance(record.get("outputs"), dict):
                continue
            if (record.get("status") == "succeeded" and record.get("fingerprint") == job["fingerprint"]
                    and request["identity"] == job["identity"]
                    and record.get("outputs") == collect_outputs(job, path.parent)):
                return record, path.parent
        except (OSError, ValueError, KeyError):
            continue
    return None


def group_sample(pgid):
    """Sample Linux process-group RSS, excluding zombies; not a kernel high-water mark."""
    pids, rss = [], 0
    page = os.sysconf("SC_PAGE_SIZE")
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            fields = (entry / "stat").read_text().rsplit(")", 1)[1].split()
            if int(fields[2]) == pgid and fields[0] != "Z":
                pids.append(int(entry.name))
                rss += int(fields[21]) * page
        except (OSError, ValueError, IndexError, ProcessLookupError):
            continue
    return pids, rss


def signal_group(process, sig):
    try:
        os.killpg(process.pid, sig)
    except ProcessLookupError:
        pass


def stop_group(process, grace):
    """Also clean descendants left by an already-exited direct child."""
    signal_group(process, signal.SIGTERM)
    deadline = time.monotonic() + grace
    while group_sample(process.pid)[0] and time.monotonic() < deadline:
        process.poll()
        time.sleep(0.02)
    signal_group(process, signal.SIGKILL)
    process.wait()


def command_for(job, attempt, args):
    values = {"output_dir": str(attempt / "outputs"), "threads": str(args.threads), "blender": str(Path(args.blender).resolve())}
    values.update({f"input:{key}": item["path"] for key, item in job["inputs"].items()})
    command = [TOKEN.sub(lambda match: values[match.group(1)], value) for value in job["spec"]["argv"]]
    command[0] = job["executable"]
    if command[0] == str(Path(args.blender).resolve()):
        command[1:1] = ["--background", "-t", str(args.threads), "--python-exit-code", "1"]
    return command


def launch(job, args, run_id, attempt_number):
    attempt = job["base"] / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex)
    attempt.mkdir(parents=True, exist_ok=False)
    for folder in ("outputs", "work", "tmp"):
        (attempt / folder).mkdir()
    command = command_for(job, attempt, args)
    write_once(attempt / "request.json", {"identity": job["identity"], "fingerprint": job["fingerprint"],
               "run_id": run_id, "argv": command, "created_at": utc_now()})
    active = {"job": job, "attempt": attempt, "attempt_number": attempt_number,
              "started": time.monotonic(), "started_at": utc_now(), "process": None,
              "peak_rss": 0, "peak_processes": 0, "status_override": None}
    if not inputs_match(job):
        active["status_override"] = "inputs_changed"
        return active
    env = os.environ.copy()
    env.update({key: str(args.threads) for key in THREAD_ENV})
    env.update({"TMPDIR": str(attempt / "tmp"), "PYTHONDONTWRITEBYTECODE": "1"})
    wrapper = [sys.executable, str(Path(__file__).resolve()), "--_exec", str(args.memory_mb), "--", *command]
    try:
        with (attempt / "stdout.log").open("xb") as stdout, (attempt / "stderr.log").open("xb") as stderr:
            active["process"] = subprocess.Popen(wrapper, cwd=attempt / "work", env=env,
                                                  stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                                  start_new_session=True, shell=False)
    except OSError as error:
        active["status_override"] = "launch_failed"
        active["error"] = str(error)
    return active


def finish(active, args):
    process, job = active["process"], active["job"]
    if process is not None:
        stop_group(process, args.kill_grace_seconds)
    status = active["status_override"] or ("succeeded" if process.returncode == 0 else "failed")
    outputs, error = {}, active.get("error")
    if status == "succeeded":
        if not inputs_match(job):
            status = "inputs_changed"
        else:
            try:
                outputs = collect_outputs(job, active["attempt"])
            except (OSError, ValueError) as exception:
                status, error = "outputs_invalid", str(exception)
    record = {"schema_version": VERSION, "fingerprint": job["fingerprint"], "asset_id": job["names"][0],
              "revision": job["names"][1], "job_id": job["names"][2], "status": status,
              "started_at": active["started_at"], "finished_at": utc_now(),
              "wall_seconds": round(time.monotonic() - active["started"], 4),
              "returncode": process.returncode if process else None, "pid": process.pid if process else None,
              "sampled_peak_group_rss_bytes": active["peak_rss"],
              "sampled_peak_group_processes": active["peak_processes"],
              "outputs": outputs, "error": error}
    write_once(active["attempt"] / "result.json", record)
    return {**record, "attempt_dir": str(active["attempt"])}


def run(args):
    if sys.platform != "linux":
        raise ValueError("This cloud queue currently requires Linux process groups, /proc, and flock")
    bounded_int(args.workers, 1, MAX_WORKERS, "workers")
    bounded_int(args.threads, 1, 64, "threads")
    bounded_int(args.retries, 0, 3, "retries")
    bounded_int(args.memory_mb, 0, 1048576, "memory-mb")
    if not math.isfinite(args.kill_grace_seconds) or args.kill_grace_seconds < 0:
        raise ValueError("kill-grace-seconds must be finite and nonnegative")
    available = capacity()
    cpu_budget = args.cpu_budget or available["known_cpu_budget"]
    bounded_int(cpu_budget, 1, available["known_cpu_budget"], "cpu-budget")
    if args.workers * args.threads > cpu_budget:
        raise ValueError(f"workers × threads exceeds known/declared CPU budget {cpu_budget}")
    args.manifest = args.manifest.resolve()
    args.runs_root = args.runs_root.resolve()
    args.runs_root.mkdir(parents=True, exist_ok=True)
    # Prevent two invocations from racing in one store. Separate stores are
    # independent; their combined budget must be coordinated by the operator.
    lock = (args.runs_root / ".queue.lock").open("a+")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        raise ValueError("Another queue is active in this runs root")
    active, completed, cancelled, handlers = [], [], [], {}
    state = {"signal": None, "count": 0}
    started = time.monotonic()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex
    peak_workers, peak_rss, peak_processes = 0, 0, 0
    run_dir = args.runs_root / "runs" / run_id
    try:
        manifest, jobs = load_jobs(args)
        pending = deque((job, 0) for job in jobs)
        run_dir.mkdir(parents=True, exist_ok=False)
        write_once(run_dir / "manifest.json", manifest)
        def cancel(signum, _frame):
            state["signal"] = signum
            state["count"] += 1
        for sig in (signal.SIGINT, signal.SIGTERM):
            handlers[sig] = signal.signal(sig, cancel)
        while pending or active:
            if state["signal"]:
                while pending:
                    job, _ = pending.popleft()
                    cancelled.append({"asset_id": job["names"][0], "revision": job["names"][1],
                                      "job_id": job["names"][2], "status": "cancelled_before_launch"})
            while pending and len(active) < args.workers and not state["signal"]:
                job, attempt_number = pending.popleft()
                reused = resume_result(job) if args.resume and attempt_number == 0 else None
                if reused:
                    record, directory = reused
                    completed.append({**record, "status": "reused", "attempt_dir": str(directory)})
                    continue
                active.append(launch(job, args, run_id, attempt_number))
                peak_workers = max(peak_workers, sum(item["process"] is not None for item in active))
            total_rss = total_processes = 0
            for item in list(active):
                process = item["process"]
                if process:
                    pids, rss = group_sample(process.pid)
                    item["peak_rss"] = max(item["peak_rss"], rss)
                    item["peak_processes"] = max(item["peak_processes"], len(pids))
                    total_rss += rss
                    total_processes += len(pids)
                    if state["signal"] and (args.on_cancel == "terminate" or state["count"] > 1):
                        item["status_override"] = "cancelled"
                    elif time.monotonic() - item["started"] >= item["job"]["timeout_seconds"]:
                        item["status_override"] = "timed_out"
                if process is None or item["status_override"] or process.poll() is not None:
                    record = finish(item, args)
                    completed.append(record)
                    active.remove(item)
                    print(json.dumps({"job_id": record["job_id"], "asset_id": record["asset_id"],
                                      "status": record["status"], "attempt_dir": record["attempt_dir"]}), flush=True)
                    if (record["status"] in {"failed", "timed_out", "launch_failed", "outputs_invalid"}
                            and item["attempt_number"] < args.retries and not state["signal"]
                            and inputs_match(item["job"])):
                        pending.append((item["job"], item["attempt_number"] + 1))
            peak_rss, peak_processes = max(peak_rss, total_rss), max(peak_processes, total_processes)
            if active:
                time.sleep(0.05)
        final = {}
        for record in completed:
            final[(record["asset_id"], record["revision"], record["job_id"])] = record
        failed = any(item["status"] not in {"succeeded", "reused"} for item in final.values())
        summary = {"schema_version": VERSION, "run_id": run_id, "lane": manifest["lane"],
                   "status": "cancelled" if state["signal"] else "failed" if failed else "succeeded",
                   "workers": args.workers, "threads_per_job": args.threads, "cpu_budget": cpu_budget,
                   "capacity": available, "memory_limit_mb_per_process": args.memory_mb or None,
                   "wall_seconds": round(time.monotonic() - started, 4), "peak_active_jobs": peak_workers,
                   "sampled_peak_group_rss_bytes": peak_rss, "sampled_peak_processes": peak_processes,
                   "sampling_interval_seconds": 0.05, "signal": state["signal"],
                   "results": completed, "unstarted": cancelled, "finished_at": utc_now()}
        write_once(run_dir / "summary.json", summary)
        print(json.dumps({"summary": str(run_dir / "summary.json"), "status": summary["status"]}), flush=True)
        return 128 + state["signal"] if state["signal"] else 1 if failed else 0
    finally:
        for item in active:
            if item["process"]:
                stop_group(item["process"], args.kill_grace_seconds)
        for sig, handler in handlers.items():
            signal.signal(sig, handler)
        lock.close()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--_exec":
        # Run in a fresh single-threaded Python process, avoiding unsafe
        # preexec_fn use if this scheduler later gains threads.
        memory = int(sys.argv[2])
        if memory:
            limit = memory * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        command = sys.argv[4:]
        os.execv(command[0], command)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--runs-root", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--threads", type=int, default=2)
    parser.add_argument("--cpu-budget", type=int, help="Optional shared-host allocation; cannot exceed known capacity")
    parser.add_argument("--memory-mb", type=int, default=0, help="Linux RLIMIT_AS per process, 0 disables; not aggregate tree RSS")
    parser.add_argument("--timeout-seconds", type=float, default=600)
    parser.add_argument("--kill-grace-seconds", type=float, default=2)
    parser.add_argument("--on-cancel", choices=("terminate", "drain"), default="terminate")
    parser.add_argument("--retries", type=int, default=0)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--blender", default=shutil.which("blender") or "/usr/bin/blender")
    parser.add_argument("--allow-executable", action="append", default=[], help="Explicit additional trusted executable, repeatable")
    args = parser.parse_args()
    try:
        return run(args)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(2, f"asset queue: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
