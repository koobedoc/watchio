#!/usr/bin/env python3
""" watchio: Process IO watcher """

import pathlib
import os
import time

__version__ = "0.0.12"
__build__ = "Sun Feb 27 23:08:39 2022 PST"


class WatchIO:
    """
    Process IO watcher
    """

    def __init__(self, pids: list = None, timeout=600, step=1):
        """
        Constructor for WatchIO, call with keyword arguments.

        `pids` is a list of process PIDs to watch. Non-valid PIDs are silently
        ignored.

        `timeout` sets the default value for poll() methed.

        `step` sets the default step value in seconds for the poll() method.

        """
        self.timeout = timeout
        self.step = step
        self.pids = pids if pids else []
        self.procs = {}
        self.pid_self = os.getpid()

    def get_io_data(self, pid: int) -> dict:
        """
        Get IO data from the /proc file system. The method reads and parses the
        file "/proc/<pid>/io" and returns a dictionary with values in int.

        `pid` is the process ID to get the io data. The method returns None
        is the process does not exist. TODO: no read access.
        """
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
        ## Since we have just read in a file, this current process
        ## has some IO activity. The following filters this out.
        if pid in self.procs and pid == os.getpid():
            data["rchar"] = self.procs[pid]["rchar"]
            data["syscr"] = self.procs[pid]["syscr"]

        return data

    def update(self):
        """
        Update IO activities. Returns the number of process with new IO activities.
        """
        changes = 0
        for pid in self.pids:
            data = self.get_io_data(pid)
            if data and data != self.procs.get(pid, {}):  # Has changed
                self.procs[pid] = data
                changes += 1
        return changes

    def __str__(self):
        return f"<WatchIO pids={self.pids} timeout={self.timeout} step={self.step}>"

    # def dump(self):
    #    """Dump out current states for debugging"""

    def poll(self, timeout: int = None, step: int = None) -> int:
        """
        Poll the IO activities. The method returns where there are new IO activities or
        if the wait time has exceeded `timeout` seconds. It checks the IO acitiviies
        every `step` seconds. Returns 0 if timeout, or the number of processes with
        new IO activities.

        `timeout` for waiting. Defaults to instance value if not given.

        `step` for internal checking internval. Defaults to instance value if not given.
        """

        if timeout is None:  ## Use instance value
            timeout = self.timeout
        if step is None:  ## Use instance value
            step = self.step

        for _ in range(timeout):
            if changes := self.update():
                return changes
            time.sleep(1)

        return 0
