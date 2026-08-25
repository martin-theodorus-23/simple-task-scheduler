#!/usr/bin/env python3
"""
Simple Task Scheduler
======================
A minimal, single-file background task scheduler. It runs a script on a
fixed interval, restarts it on the next tick if it crashed, and logs
everything to scheduler.log.

Usage:
    python scheduler.py [path/to/tasks.json]

If no config path is given, it looks for tasks.json in the current
directory.

Config format (tasks.json):
{
    "python": "python",
    "tasks": [
        {
            "name": "heartbeat",
            "script": "heartbeat.py",
            "interval_seconds": 30
        }
    ]
}

Only one trigger type is supported: interval_seconds — run every N
seconds, skipping a run if the previous one is still going. There is no
CLI task manager and no daily-time / one-off-date triggers here; this is
the intentionally small, free version. See README.md if you want those.
"""

import subprocess
import datetime
import json
import time
import sys
import os

DEFAULT_CONFIG = "tasks.json"
LOG_FILE = "scheduler.log"


def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class Task:
    """Tracks scheduling state for a single interval-based task."""

    def __init__(self, cfg):
        self.name = cfg["name"]
        self.script = cfg["script"]
        self.interval = cfg["interval_seconds"]
        self.last_run = 0.0
        self.proc = None

    def poll(self, interpreter):
        # If a previous run is still going, check whether it finished.
        if self.proc is not None:
            code = self.proc.poll()
            if code is None:
                return  # still running, nothing to do this tick
            if code == 0:
                log(f"[{self.name}] finished normally (exit 0).")
            else:
                log(f"[{self.name}] exited with code {code}.")
            self.proc = None

        now = time.time()
        if now - self.last_run >= self.interval:
            self.last_run = now
            self.start(interpreter)

    def start(self, interpreter):
        try:
            self.proc = subprocess.Popen([interpreter, self.script])
            log(f"[{self.name}] started.")
        except Exception as e:
            log(f"[{self.name}] failed to start: {e}")


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG

    if not os.path.exists(config_path):
        print(f"Config file not found: {config_path}")
        print("See README.md for the tasks.json format.")
        sys.exit(1)

    config = load_config(config_path)
    interpreter = config.get("python", sys.executable)
    tasks = [Task(t) for t in config.get("tasks", [])]

    if not tasks:
        print("No tasks defined in config. Add at least one to tasks.json.")
        sys.exit(1)

    log(f"Scheduler started with {len(tasks)} task(s). Press Ctrl+C to stop.")
    try:
        while True:
            for task in tasks:
                task.poll(interpreter)
            time.sleep(1)
    except KeyboardInterrupt:
        log("Scheduler stopped by user.")


if __name__ == "__main__":
    main()
