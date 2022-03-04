#!/usr/bin/env python3
""" Tests for watchio module """

import os
import time
import sys

import pytest

sys.path = ["../src"] + sys.path

import watchio


def test_constructor():
    """Tests for constructor"""

    ## Checks defaults
    iow = watchio.WatchIO([1])
    assert str(iow) == "<WatchIO pids=[1] timeout=600 step=1>"

    iow = watchio.WatchIO([2], timeout=3456, step=7)
    assert str(iow) == "<WatchIO pids=[2] timeout=3456 step=7>"


def test_delay():
    """Tests for delays in polling"""

    iow = watchio.WatchIO([os.getpid()])

    print("// First time calling, poll should exit immediately")
    start_time = time.time()
    ret = iow.poll(timeout=3)
    print(f"// Returned {ret}. Elapsed = {time.time() - start_time:.3f}s")
    assert (time.time() - start_time) < 0.1

    print("// Now we run again. It should timeout")
    iow.update()  ### To flush out changes print print statments
    start_time = time.time()
    ret = iow.poll(timeout=0.2, step=0.1)
    elapsed = time.time() - start_time
    print(f"// Returned {ret}. Elapsed = {elapsed:.3f}s")
    assert 0.2 < elapsed < 0.3


def test_exception():
    """Test for exception cases"""

    print("// Polling not-accesible or non-existent process should return immediately")
    start_time = time.time()
    watcher = watchio.WatchIO([1])
    watcher.poll()
    watcher = watchio.WatchIO([1, 2, 3, 4])
    watcher.poll()
    watcher = watchio.WatchIO([1, 2, 3, 999999])
    watcher.poll()
    elapsed = time.time() - start_time
    assert elapsed < 0.1


def test_get_io_data():
    """Misc tests"""

    watcher = watchio.WatchIO([os.getpid()])
    data = watcher.get_io_data(os.getpid())
    assert list(data.keys()) == [
        "rchar",
        "wchar",
        "syscr",
        "syscw",
        "read_bytes",
        "write_bytes",
        "cancelled_write_bytes",
    ]
    ## Non-accessible or non-existent
    assert None == watchio.WatchIO().get_io_data(1)
    assert None == watchio.WatchIO().get_io_data(9999999)

def test_misc():

    print("dir(watchio):", dir(watchio))
    print(watchio.__version__)


if __name__ == "__main__":

    pytest.main()
