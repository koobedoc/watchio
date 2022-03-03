#!/usr/bin/env python3
""" watchio: Process IO watcher """

import argparse
import pathlib
import os
import time

__version__ = "0.0.23"
__build__ = "Wed Mar  2 21:27:04 2022 PST"


class WatchIO:
    """
    Process IO watcher
    """

    def __init__(self, pids: list = None, *, timeout: float = 600, step: float = 1):
        """
        Constructor for WatchIO, call with keyword arguments.

        *pids* is a list of process PIDs to watch. Non-valid PIDs are silently
        ignored.

        *timeout* sets the default timeout value for the poll() methed.

        *step* sets the default step value, the interval we check
        the /proc/ file, in seconds for the poll() method.

        """
        self.args = argparse.Namespace(verbose=0)
        self.timeout = timeout
        self.step = step
        self.pids = pids if pids else []
        self.procs = {}
        self.pid_self = os.getpid()

    def get_io_data(self, pid: int) -> dict:
        """
        Get IO data of the `pid` process. The method reads and parses the
        file "/proc/{pid}/io" and returns a dictionary with values in int.
        See https://man7.org/linux/man-pages/man5/proc.5.html for the definition
        of values.

        *pid* is the process ID to get the io data. The method returns None
        if the process does not exist. TODO: no read access.
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

    def update(self) -> int:
        """
        Update IO activities. Returns the number of process with new IO activities
        since the last update() or poll().
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

    def poll(self, timeout: float = None, step: float = None, clear=False) -> int:
        """
        Poll the IO activities. The method checks for IO activities every
        `step` seconds. It returns the number of processes with new IO
        activities since the last update() or poll(); or returns 0 if
        the wait time has exceeded `timeout` seconds.

        *timeout* defaults to instance value if not given.

        *step* defaults to instance value if not given.

        *clear* (default is False) clears the IO counters so that polling uses
        only IO activities after this function has started.
        """

        if timeout is None:  ## Use instance value
            timeout = self.timeout
        if step is None:  ## Use instance value
            step = self.step
        step = max(0.1, step)

        if clear:
            self.update()

        start_time = time.time()
        elapsed = 0
        while elapsed <= timeout:
            if changes := self.update():
                return changes
            ## Bound step to a reasonable value
            if step > (timeout / 100):
                step = timeout / 100
            if step < 10:
                step = max(0.1, elapsed / 100, step)

            time.sleep(step)
            elapsed = time.time() - start_time
            # step = max(step, elapsed/10)

        return 0

    def parse_cli(self):
        """Parse Unix command line arguments"""
        parser = argparse.ArgumentParser(description="Unix process IO activities watcher.")
        parser.add_argument("command", type=str, help="Command")
        parser.add_argument("pids", nargs="+", help="Unix process IDs")

        parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity for debugging")

        self.args = parser.parse_args()
        if self.args.verbose:
            print(self.args)

    @staticmethod
    def main_cli():
        """Unix command line interface"""
        self = WatchIO()
        self.parse_cli()
        print("// watchio: TBD")


if __name__ == "__main__":
    WatchIO.main_cli()
