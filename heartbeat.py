"""
Tiny demo task for Simple Task Scheduler.

Prints a timestamp and exits. Run the scheduler with the bundled
tasks.json and this will fire every 30 seconds so you can see it work.
"""

import datetime

print(f"heartbeat: {datetime.datetime.now().isoformat()}")
