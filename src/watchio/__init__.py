#!/usr/bin/env python3
""" watchio: Process IO watcher """

import argparse
import os
import pathlib
import re
import time
import sys

import psutil

__version__ = "0.0.40"
__build__ = "Fri Mar 11 22:02:55 2022 PST"


class WatchIO:
    """
    Process IO watcher.
    """

    def __init__(self, pids: list = None, *, timeout: float = 600, step: float = 1, check=False):
        """
        Constructor for WatchIO, call with keyword arguments.

        *pids* is a list of process PIDs to watch. Non-valid PIDs are silently
        ignored unless `check` is enabled.

        *timeout* sets the default timeout value for the poll() method.

        *step* sets the default step value, the interval we check
        the /proc/{pid}/io file, in seconds for the poll() method.

        *check* raises exceptions (PermissionError if not accessible or FileNotFoundError for
        non-existent process) instead of silently ignoring bad pids by default.

        """
        self.args = argparse.Namespace(verbose=0)
        self.timeout = timeout
        self.step = step
        self.check = check
        self.pids = pids if pids else []
        self.procs = {}
        self.pid_self = os.getpid()

    def find_pids(self, name: str) -> list:
        """
        Get a list of PIDs by *name*. Name can be a numerical pid or the name
        of the process. Returns a (possibly empty) list.
        """
        _ = self
        pids = []
        for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
            if (re.search(r"^\d+$", name) and name == str(proc.info["pid"])) or (name == proc.info["name"]):
                pids.append(proc.info["pid"])
        return pids
        # print(p.info['pid'], p.info['name'], p.info['exe'], p.info['cmdline'])

    def get_io_data(self, pid: int) -> dict:
        """
        Get IO data of the `pid` process. The method reads and parses the
        file "/proc/{pid}/io" and returns a dictionary with values in int.
        See https://www.kernel.org/doc/html/latest/filesystems/proc.html#proc-pid-io-display-the-io-accounting-fields
        for a description of the fields.

        *pid* is the process ID to get the io data. The method returns None
        if the process does not exist. TODO: no read access.
        """
        filename = f"/proc/{pid}/io"
        # if not os.path.isfile(filename):
        #    return None

        data = {}
        try:
            text = pathlib.Path(filename).read_text(encoding="ascii")
        except Exception as err:  # pylint: disable=broad-except
            if self.check:
                raise err
            return None

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
        since the last update() or poll(). Returns -1 if no PID is valid.
        """
        changes = 0
        valid = 0
        for pid in self.pids:
            data = self.get_io_data(pid)
            if data:
                valid += 1
                if data != self.procs.get(pid, {}):  # Has changed
                    self.procs[pid] = data
                    changes += 1

        return changes if valid else -1

    def __str__(self):
        return f"<WatchIO pids={self.pids} timeout={self.timeout:.1f} step={self.step:.1f} check={self.check}>"

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
        parser.add_argument("command", choices=("poll",), help="Command")
        parser.add_argument("pids", nargs="+", help="Unix process IDs")
        parser.add_argument("--timeout", type=float, help="timeout in seconds")
        parser.add_argument("--step", type=float, help="internal polling step in seconds")

        parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity for debugging")

        self.args = parser.parse_args()
        if self.args.verbose > 2:
            print(self.args)

    @staticmethod
    def main_cli():
        """Unix command line interface"""
        self = WatchIO()
        self.parse_cli()
        if self.args.verbose:
            print(f"// watchio: {self}")
        for pid in self.args.pids:
            self.pids += self.find_pids(pid)
        if not self.pids:
            print("// No valid process to watch. Exit 1", file=sys.stderr)
            sys.exit(1)

        self.poll(timeout=self.args.timeout, step=self.args.timeout, clear=True)


if __name__ == "__main__":
    WatchIO.main_cli()
