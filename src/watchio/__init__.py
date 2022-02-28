#!/usr/bin/env python3
""" watchio: Process IO watcher """

import pathlib
import os
import time

__version__ = "0.0.5"


class WatchIO:
    """Process IO watcher"""

    def __init__(self, pids: list = None, timeout=600, step=1):
        self.timeout = timeout
        self.step = step
        self.pids = pids if pids else []
        self.procs = {}
        self.pid_self = os.getpid()

    def get_io_data(self, pid: int) -> dict:
        """Get IO data from the /proc file system"""
        _ = self
        filename = f"/proc/{pid}/io"
        if not os.path.isfile(filename):
            return None

        data = {}
        text = pathlib.Path(filename).read_text(encoding="ascii")
        for line in text.split("\n"):
            if line:
                key, value = line.split(":", 1)
                data[key] = int(value)
        if pid == os.getpid():  ## Ignore self read
            data["rchar"] = data["syscr"] = 1

        return data

    def update(self):
        """Update all io data for all pids"""
        changes = 0
        for pid in self.pids:
            data = self.get_io_data(pid)
            if data and data != self.procs.get(pid, {}):  # Has changed
                self.procs[pid] = data
                changes += 1
        return changes

    def __str__(self):
        return f"<WatchIO pids={self.pids} timeout={self.timeout} step={self.step}>"

    def dump(self):
        """Dump out current states for debugging"""

    def poll(self, timeout: int = None, step: int = None):
        """pool"""

        if timeout is None:
            timeout = self.timeout
        if step is None:
            step = self.step

        for _ in range(timeout):
            if changes := self.update():
                return changes
            time.sleep(1)

        return 0
