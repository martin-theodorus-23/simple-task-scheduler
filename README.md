# Simple Task Scheduler

A minimal, single-file Python background task scheduler. Point it at a
script and an interval, run it, and it repeats that script forever —
restarting your task on the next tick if it crashed, and logging
everything to `scheduler.log`.

No dependencies. No install. Just one ~100-line Python file.

## What it does

- Runs a script every N seconds (`interval_seconds` in `tasks.json`)
- Won't start a second run of a task while the previous one is still going
- Logs start/finish/crash events with timestamps to `scheduler.log`
- Supports any number of tasks in one config file

That's it. This is the whole feature set — it's meant to be small enough
to read end-to-end in a couple of minutes.

## What it does NOT do

To keep this genuinely simple and free, this version deliberately leaves
out:

- Daily-time triggers (e.g. "run at 22:00") or one-off scheduled dates
- A CLI for adding/editing/removing tasks without touching JSON
- Bundled example scripts beyond one tiny demo

If you need those, see "Want more?" below.

## Requirements

- Python 3.7+
- Windows, Linux, or macOS

## Quick start

```bash
git clone https://github.com/martin-theodorus-23/simple-task-scheduler.git
cd simple-task-scheduler
python scheduler.py
```

This runs the bundled `tasks.json`, which fires the included
`heartbeat.py` demo every 30 seconds and prints/logs a timestamp. Press
`Ctrl+C` to stop.

## Configuring your own tasks

Edit `tasks.json`:

```json
{
    "python": "python",
    "tasks": [
        {
            "name": "my_task",
            "script": "my_script.py",
            "interval_seconds": 3600
        }
    ]
}
```

- `python` — the interpreter used to run every task's script (use a full
  path if `python` isn't on your PATH, e.g.
  `"C:\\Python311\\python.exe"`)
- `name` — a label used in log messages
- `script` — path to the script to run (relative to where you launch
  the scheduler, or absolute)
- `interval_seconds` — how often to run it

Add as many task objects to the `"tasks"` array as you want. Each script
just needs to run and exit; exit code `0` is logged as success, anything
else is logged as a failure (and the scheduler will try it again on the
next interval tick).

## Running at startup

This lite version doesn't include install-at-boot tooling. On Windows
you can wire it up with Task Scheduler (`taskschd.msc` → "Create Basic
Task" → run `python scheduler.py` at startup, working directory set to
this folder). On Linux, a basic `systemd` unit or a cron `@reboot` line
pointing at `python3 scheduler.py` works the same way.

## Want more?

If you outgrow the single interval trigger, need the CLI (`manage.py`)
to add/edit/delete tasks without touching JSON, and want daily-time and
one-off-date triggers plus a set of ready-made example scripts, the full
**Pack A** version covers that. It's a one-time $9, paid via BTC through
a self-hosted checkout: **https://edennexus.in/checkout/**

## License

MIT — see [LICENSE](LICENSE). Use it, modify it, ship it.
